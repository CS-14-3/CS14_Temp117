import gevent.monkey

gevent.monkey.patch_all()

import base64  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402
import urllib.request  # noqa: E402
from datetime import datetime  # noqa: E402

# Add project root to path so project_database is importable
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Resolve runtime paths early so third-party libraries can use writable caches.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_CACHE_DIR = os.path.join(BASE_DIR, ".runtime_cache")
os.makedirs(os.path.join(RUNTIME_CACHE_DIR, "matplotlib"), exist_ok=True)
os.makedirs(os.path.join(RUNTIME_CACHE_DIR, "xdg"), exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(RUNTIME_CACHE_DIR, "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(RUNTIME_CACHE_DIR, "xdg"))

import cv2  # noqa: E402
import mediapipe as mp  # noqa: E402
import numpy as np  # noqa: E402
from flask import Flask, jsonify, send_from_directory  # noqa: E402
from flask_socketio import SocketIO, emit  # noqa: E402
from mediapipe.tasks import python  # noqa: E402
from mediapipe.tasks.python import vision  # noqa: E402
from project_database.db_bridge import db_bridge  # noqa: E402

# ── Always resolve paths relative to THIS script file ──────────────────────
CALIBRATION_FILE = "Mediapipe.html"
if not os.path.exists(os.path.join(BASE_DIR, CALIBRATION_FILE)):
    print(f"[WARN] Missing {CALIBRATION_FILE}; the / route will return 404 until this file is added.")

# ==================== Flask App ====================
app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
app.config["SECRET_KEY"] = "cs14-eye-tracking"
socketio = SocketIO(app, cors_allowed_origins="*")

# ==================== MediaPipe Tasks API ====================
MODEL_PATH = os.path.join(BASE_DIR, "face_landmarker.task")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", os.environ.get("CV_BACKEND_PORT", "5050")))
CAMERA_BUILD_VERSION = "camera-startup-fix-2026-05-16"

if not os.path.exists(MODEL_PATH):
    print(f"[INFO] Downloading model {MODEL_PATH} ...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, MODEL_PATH)
    print("[INFO] Model download complete!")

# Force CPU inference so the server can start on machines where MediaPipe
# cannot initialize the macOS OpenGL path.
base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH,
    delegate=python.BaseOptions.Delegate.CPU,
)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1,
)
detector = None
detector_error = None


def get_detector():
    global detector, detector_error
    if detector is not None:
        return detector
    if detector_error is not None:
        return None

    try:
        detector = vision.FaceLandmarker.create_from_options(options)
        return detector
    except Exception as error:
        detector_error = str(error)
        print(f"[ERROR] MediaPipe FaceLandmarker unavailable: {detector_error}")
        return None


# ==================== Routes ====================

@app.route("/")
def calibration_page():
    return send_from_directory(BASE_DIR, CALIBRATION_FILE)


@app.route("/healthz")
def healthz():
    return jsonify({
        "success": True,
        "service": "cs14-camera",
        "build": CAMERA_BUILD_VERSION,
        "detectorReady": detector is not None,
        "detectorError": detector_error,
    })


@app.route("/participant")
def participant_page():
    return send_from_directory(BASE_DIR, "participant.html")


# ==================== WebSocket Events ====================

@socketio.on("frame")
def handle_frame(data):
    try:
        face_detector = get_detector()
        if face_detector is None:
            emit("landmarks", {"detected": False, "error": detector_error or "Face detector is not available."})
            return

        header, encoded = data.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            emit("landmarks", {"detected": False})
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        detection_result = face_detector.detect(mp_image)

        if detection_result.face_landmarks:
            lm = detection_result.face_landmarks[0]
            pts = [[round(p.x, 5), round(p.y, 5), round(p.z, 5)] for p in lm]
            emit("landmarks", {"detected": True, "pts": pts})
        else:
            emit("landmarks", {"detected": False})

    except Exception as e:
        print(f"[ERROR] frame processing: {e}")
        emit("landmarks", {"detected": False})


@socketio.on("save_data")
def handle_save_data(data):
    try:
        data_dir = os.path.join(BASE_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        pid = data.get("participantId", "unknown")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = "STUDY" if "gazeLogs" in data else "CAL"
        filename = os.path.join(data_dir, f"CS14_{prefix}_{pid}_{ts}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {filename}  "
              f"(gaze: {len(data.get('gazeLogs', []))}, "
              f"cal: {len(data.get('calibrationLogs', []))})")

        # Write to database
        try:
            invite_code = str(pid).strip()
            survey_id = db_bridge.get_survey_id_by_invite_code(invite_code)
            payload_type = "study" if data.get("studyEndedAt") else "autosave"
            result = db_bridge.upsert_full_study_payload(
                participant_code=invite_code,
                survey_id=survey_id,
                invite_code=invite_code,
                payload_type=payload_type,
                payload=data,
            )
            print(f"[DB] saved — gaze: {result['gaze_records_saved']}, "
                  f"cal_samples: {result['calibration_samples_saved']}, "
                  f"interactions: {result['interaction_logs_saved']}")
        except Exception as db_err:
            print(f"[DB ERROR] {db_err}")

        emit("save_result", {"success": True, "filename": filename})
    except Exception as e:
        print(f"[ERROR] save: {e}")
        emit("save_result", {"success": False, "error": str(e)})


@socketio.on("connect")
def handle_connect():
    print("[CONNECTED] Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("[DISCONNECTED] Client disconnected")


# ==================== Main ====================
if __name__ == "__main__":
    print("=" * 55)
    print("  CS14 Eye Tracking System")
    print(f"  Files served from: {BASE_DIR}")
    print(f"  Calibration  →  http://localhost:{PORT}/")
    print(f"  Participant   →  http://localhost:{PORT}/participant")
    print("=" * 55)
    socketio.run(app, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
