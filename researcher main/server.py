import re
import socket
import json
import os
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse, urlencode, urljoin
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # 允许跨域请求，供前端 Vanilla JS 调用

# 模拟真实浏览器 User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

GAZE_RESULTS = []
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "").strip()
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "").strip().rstrip("/")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "").strip()
TRANSLATION_BATCH_SIZE = 25

def is_safe_url(url):
    """
    SSRF 防护逻辑：
    1. 必须是 http 或 https 协议
    2. 域名不能解析到私有 IP (localhost, 127.0.0.1, 192.168.x.x 等)
    """
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ["http", "https"]:
            return False
        
        hostname = parsed_url.hostname
        if not hostname:
            return False
        
        # 解析主机名为 IP 地址
        ip_address = socket.gethostbyname(hostname)
        
        # 私有 IP 地址段正则表达式
        private_ip_patterns = [
            r"^127\.",              # Loopback
            r"^10\.",               # Private class A
            r"^172\.(1[6-9]|2[0-9]|3[01])\.", # Private class B
            r"^192\.168\.",         # Private class C
            r"^169\.254\.",         # Link-local
            r"^0\.",                # Zero address
            r"^localhost$"          # Localhost string
        ]
        
        for pattern in private_ip_patterns:
            if re.match(pattern, ip_address) or re.match(pattern, hostname):
                return False
        
        return True
    except Exception:
        return False

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

def first_value(*sources_and_keys):
    for source, keys in sources_and_keys:
        if not isinstance(source, dict):
            continue
        for key in keys:
            value = source.get(key)
            if value is not None:
                return value
    return None

def normalize_gaze_payload(payload):
    if not isinstance(payload, dict):
        return None

    raw_payload = payload.get("rawPayload") or payload.get("raw_payload")
    if not isinstance(raw_payload, dict):
        raw_payload = payload

    survey_id = first_value(
        (payload, ["surveyId", "survey_id"]),
        (raw_payload, ["surveyId", "survey_id"])
    )
    if not survey_id:
        return None

    gaze_data = first_value(
        (payload, ["gazeData", "gaze_data", "gazeLogs", "gaze_logs", "samples"]),
        (raw_payload, ["gazeData", "gaze_data", "gazeLogs", "gaze_logs", "samples"])
    )
    if not isinstance(gaze_data, list):
        gaze_data = []

    closed_at = first_value(
        (payload, ["closedAt", "closed_at", "studyEndedAt", "study_ended_at"]),
        (raw_payload, ["closedAt", "closed_at", "studyEndedAt", "study_ended_at"])
    )
    received_at = utc_now_iso()
    started_at = first_value(
        (payload, ["startedAt", "started_at", "studyStartedAt", "study_started_at"]),
        (raw_payload, ["startedAt", "started_at", "studyStartedAt", "study_started_at"])
    )
    participant_id = first_value(
        (payload, ["participantId", "participant_id"]),
        (raw_payload, ["participantId", "participant_id"])
    )
    participant_label = first_value(
        (payload, ["participantLabel", "participant_label"]),
        (raw_payload, ["participantLabel", "participant_label"])
    )
    quality_metrics = first_value(
        (payload, ["qualityMetrics", "quality_metrics"]),
        (raw_payload, ["qualityMetrics", "quality_metrics"])
    )
    if not isinstance(quality_metrics, dict):
        quality_metrics = {}

    sample_count = first_value((payload, ["sampleCount", "sample_count"]))
    try:
        sample_count = int(sample_count)
    except (TypeError, ValueError):
        sample_count = len(gaze_data)

    return {
        "id": payload.get("id") or payload.get("resultId") or f"gaze_{uuid.uuid4().hex[:12]}",
        "surveyId": survey_id,
        "inviteCode": first_value(
            (payload, ["inviteCode", "invite_code"]),
            (raw_payload, ["inviteCode", "invite_code"])
        ) or "",
        "participantId": participant_id or "",
        "participantLabel": participant_label or participant_id or "Participant",
        "status": payload.get("status") or ("completed" if closed_at else "received"),
        "startedAt": started_at,
        "closedAt": closed_at or received_at,
        "receivedAt": received_at,
        "sampleCount": sample_count,
        "gazeData": gaze_data,
        "qualityScore": payload.get("qualityScore") or payload.get("quality_score") or quality_metrics.get("scorePercent"),
        "metadata": payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
        "rawPayload": raw_payload
    }

def read_json_payload():
    payload = request.get_json(silent=True)
    if payload is not None:
        return payload

    raw_body = request.get_data(as_text=True)
    if not raw_body:
        return None

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return None

@app.route('/api/scrape', methods=['POST'])
def scrape_news():
    data = request.get_json()
    url = data.get("url") if data else None
    
    if not url:
        return jsonify({"success": False, "error": "Missing URL"}), 400
    
    # 1. 安全性检查 (SSRF 防护)
    if not is_safe_url(url):
        return jsonify({"success": False, "error": "Security Alert: Invalid or Restricted URL"}), 403

    try:
        # 2. 发起请求 (带超时和伪造 UA)
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        
        # 3. 结构化解析 (BeautifulSoup)
        soup = BeautifulSoup(response.text, "lxml")
        
        # 4. 层级提取逻辑 (Open Graph -> Twitter -> Standard)
        
        # Title 提取
        title = ""
        # 首选 Open Graph
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"]
        # 次选 Twitter Card
        if not title:
            tw_title = soup.find("meta", name="twitter:title")
            if tw_title and tw_title.get("content"):
                title = tw_title["content"]
        # 兜底 Standard <title>
        if not title:
            title = soup.title.string if soup.title else ""

        # Image 提取
        image = ""
        # 首选 Open Graph
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image = og_image["content"]
        # 次选 Twitter Card
        if not image:
            tw_image = soup.find("meta", name="twitter:image")
            if tw_image and tw_image.get("content"):
                image = tw_image["content"]
        if image:
            image = urljoin(url, image.strip())
        
        # 规范化返回
        return jsonify({
            "success": True,
            "title": title.strip() if title else "No Title Found",
            "image": image if image else ""
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Request timed out (8s limit)"}), 408
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/gaze-data', methods=['POST'])
def receive_gaze_data():
    payload = read_json_payload()
    if payload is None:
        return jsonify({"success": False, "error": "Missing or invalid JSON payload"}), 400

    payload_items = payload if isinstance(payload, list) else [payload]
    normalized_results = []
    for item in payload_items:
        normalized = normalize_gaze_payload(item)
        if normalized:
            GAZE_RESULTS.append(normalized)
            normalized_results.append(normalized)

    if not normalized_results:
        return jsonify({"success": False, "error": "Missing surveyId"}), 400

    return jsonify({
        "success": True,
        "count": len(normalized_results),
        "results": normalized_results
    })

@app.route('/api/gaze-data', methods=['GET'])
def list_gaze_data():
    survey_id = request.args.get("surveyId")
    if survey_id:
        results = [result for result in GAZE_RESULTS if result.get("surveyId") == survey_id]
    else:
        results = GAZE_RESULTS

    return jsonify({
        "success": True,
        "count": len(results),
        "results": results
    })

PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Za-z0-9_]+\}\}")

def protect_translation_placeholders(text):
    placeholders = {}

    def replace_placeholder(match):
        token = f"ZXQPLACEHOLDER{len(placeholders)}XQZ"
        placeholders[token] = match.group(0)
        return token

    return PLACEHOLDER_PATTERN.sub(replace_placeholder, text), placeholders

def restore_translation_placeholders(text, placeholders):
    restored_text = text
    for token, placeholder in placeholders.items():
        restored_text = restored_text.replace(token, placeholder)
    return restored_text

def normalize_translation_entries(entries):
    normalized_entries = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue

        key = str(entry.get("key") or "").strip()
        text = str(entry.get("text") or "").strip()
        if not key or not text:
            continue
        protected_text, placeholders = protect_translation_placeholders(text)

        normalized_entries.append({
            "key": key,
            "text": protected_text,
            "placeholders": placeholders
        })

    return normalized_entries

def chunk_items(items, chunk_size):
    for start in range(0, len(items), chunk_size):
        yield items[start:start + chunk_size]

def build_azure_translation_url(source_locale, target_locales):
    query_pairs = [("api-version", "3.0"), ("from", source_locale)]
    query_pairs.extend(("to", locale) for locale in target_locales)
    return f"{AZURE_TRANSLATOR_ENDPOINT}/translate?{urlencode(query_pairs)}"

def translate_entries_with_azure(source_locale, target_locales, entries):
    translations = {
        locale: {
            "status": "ready",
            "sourceLocale": source_locale,
            "locale": locale,
            "entries": {}
        }
        for locale in target_locales
    }

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Content-Type": "application/json"
    }
    if AZURE_TRANSLATOR_REGION:
        headers["Ocp-Apim-Subscription-Region"] = AZURE_TRANSLATOR_REGION

    translation_url = build_azure_translation_url(source_locale, target_locales)
    for entry_batch in chunk_items(entries, TRANSLATION_BATCH_SIZE):
        response = requests.post(
            translation_url,
            headers=headers,
            json=[{"Text": entry["text"]} for entry in entry_batch],
            timeout=20
        )
        response.raise_for_status()
        response_payload = response.json()
        if not isinstance(response_payload, list) or len(response_payload) != len(entry_batch):
            raise ValueError("Unexpected Azure Translator response shape")

        for entry, translated_item in zip(entry_batch, response_payload):
            translated_values = translated_item.get("translations") if isinstance(translated_item, dict) else []
            translated_by_locale = {
                translated_value.get("to"): translated_value.get("text", "")
                for translated_value in translated_values or []
                if isinstance(translated_value, dict)
            }
            for locale in target_locales:
                translations[locale]["entries"][entry["key"]] = restore_translation_placeholders(
                    translated_by_locale.get(locale, ""),
                    entry.get("placeholders", {})
                )

    return translations

@app.route('/api/translations/generate', methods=['POST'])
def generate_translations():
    payload = read_json_payload()
    if not isinstance(payload, dict):
        return jsonify({"success": False, "error": "Missing or invalid JSON payload"}), 400

    survey_id = payload.get("surveyId") or payload.get("survey_id")
    source_locale = payload.get("sourceLocale") or payload.get("source_locale")
    target_locales = payload.get("targetLocales") or payload.get("target_locales")
    entries = normalize_translation_entries(payload.get("entries"))

    if not survey_id or not source_locale:
        return jsonify({"success": False, "error": "Missing surveyId or sourceLocale"}), 400
    if not isinstance(target_locales, list) or not target_locales:
        return jsonify({"success": False, "error": "Select at least one target locale"}), 400
    target_locales = [
        str(locale).strip()
        for locale in target_locales
        if str(locale).strip() and str(locale).strip() != source_locale
    ]
    if not target_locales:
        return jsonify({"success": False, "error": "Target locales must differ from sourceLocale"}), 400
    if not entries:
        return jsonify({"success": False, "error": "No translatable survey content was provided"}), 400
    if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_ENDPOINT:
        return jsonify({
            "success": False,
            "error": "Azure Translator is not configured. Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_ENDPOINT in the backend environment.",
            "translations": {}
        }), 503

    try:
        translations = translate_entries_with_azure(source_locale, target_locales, entries)
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Azure Translator request timed out"}), 504
    except requests.exceptions.HTTPError as error:
        response = error.response
        status_code = response.status_code if response is not None else 502
        provider_message = ""
        if response is not None:
            try:
                provider_payload = response.json()
                provider_message = provider_payload.get("error", {}).get("message", "")
            except (ValueError, AttributeError):
                provider_message = response.text[:300]
        return jsonify({
            "success": False,
            "error": provider_message or "Azure Translator request failed"
        }), status_code
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 502

    return jsonify({
        "success": True,
        "surveyId": survey_id,
        "sourceLocale": source_locale,
        "targetLocales": target_locales,
        "translations": translations
    })

if __name__ == '__main__':
    # 启动 Flask 服务，默认 5000 端口
    app.run(port=5001, debug=True)
