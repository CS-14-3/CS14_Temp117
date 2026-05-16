#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse
from project_database.db_bridge import db_bridge


BRIDGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BRIDGE_DIR.parent

RESEARCHER_LOGIN_HTML = ROOT_DIR / "researcher login" / "researcher-login.html"
RESEARCHER_REGISTER_HTML = ROOT_DIR / "researcher login" / "researcher-register.html"
RESEARCHER_EDIT_HTML = ROOT_DIR / "researcher main" / "index.html"
RESEARCHER_SCRAPER_BACKEND = ROOT_DIR / "researcher main" / "server.py"
PARTICIPANT_HTML = ROOT_DIR / "CS14_Temp117-Backend" / "participant.html"
CAMERA_BACKEND = ROOT_DIR / "CS14_Temp117-Backend" / "app.py"
SERVER_STARTED_AT = datetime.now(timezone.utc).isoformat()

# Legacy JSON files, no longer used after DB integration
# ACCOUNTS_FILE = BRIDGE_DIR / "fake_researcher_accounts.json"
# PUBLISHED_POSTS_FILE = BRIDGE_DIR / "published_posts.json"



ASSET_PREFIX = "/__prototype2_assets/"
SESSION_COOKIE = "prototype2_researcher_session"
SESSION_MAX_AGE = 60 * 60 * 8
RESEARCHER_EDIT_PATHS = {
    "/edit",
    "/dashboard",
    "/index.html",
    "/researcher-main",
    "/researcher-main/",
    "/researcher-main/index.html",
    "/researcher%20main/index.html",
    "/researcher main/index.html",
}
SCRAPER_PORT = int(os.environ.get("SCRAPER_PORT", "5001"))
DEFAULT_CAMERA_PORT = int(os.environ.get("CV_BACKEND_PORT", "5050"))
INTERNAL_BACKEND_HOST = os.environ.get("INTERNAL_BACKEND_HOST", "127.0.0.1")

SCRAPER_INTERNAL_URL = os.environ.get(
    "SCRAPER_INTERNAL_URL",
    f"http://{INTERNAL_BACKEND_HOST}:{SCRAPER_PORT}"
)

ASSET_TAG_PATTERNS = (
    re.compile(r'(<script\b[^>]*\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(<link\b[^>]*\bhref=["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(<img\b[^>]*\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(<source\b[^>]*\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE),
)


@dataclass(frozen=True)
class PageTarget:
    kind: str
    entry: Path

    @property
    def directory(self) -> Path:
        return self.entry.parent


@dataclass
class AppState:
    root: Path
    researcher_origin: str
    participant_origin: str
    camera_origin: str
    store: "PrototypeStore"
    login_page: PageTarget
    register_page: PageTarget
    edit_page: PageTarget
    participant_page: PageTarget

    def page_for_kind(self, kind: str) -> PageTarget:
        if kind == "login":
            return self.login_page
        if kind == "register":
            return self.register_page
        if kind == "edit":
            return self.edit_page
        if kind == "participant":
            return self.participant_page
        raise KeyError(kind)


# 根据数据库对登录功能的支持进行了修改
class PrototypeStore:
    def __init__(self) -> None:
        self.db = db_bridge

    def register_user(self, payload: dict[str, Any]) -> dict[str, str]:
        email = normalize_email(payload.get("email"))
        password = str(payload.get("password") or "").strip()
        name = str(payload.get("name") or "").strip() or derive_name(email)

        result = self.db.register_researcher(
            name=name,
            email=email,
            password=password,
        )

        return {
            "email": result["email"],
            "name": result["name"],
            "initial": result["initial"],
            "session_token": result["session_token"],
        }

    def login_user(self, payload: dict[str, Any]) -> dict[str, str] | None:
        email = normalize_email(payload.get("email"))
        password = str(payload.get("password") or "").strip()

        result = self.db.login_researcher(
            email=email,
            password=password,
        )
        if result is None:
            return None

        return {
            "email": result["email"],
            "name": result["name"],
            "initial": result["initial"],
            "session_token": result["session_token"],
        }

    def publish_post(self, payload: dict[str, Any], session: dict[str, str]) -> dict[str, Any]:
        publish_result = self.db.publish_survey_snapshot(
            researcher_email=session.get("email", ""),
            snapshot=payload,
        )

        publication = publish_result["publication"]
        posts = publish_result.get("posts") or []
        lead_post = posts[0] if posts else {}

        return {
            "id": publication["publication_id"],
            "inviteCode": publication["invite_code"],
            "platform": lead_post.get("platform", "instagram"),
            "caption": lead_post.get("caption", ""),
            "image": lead_post.get("image", ""),
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "version": lead_post.get("versionKey") or publication.get("published_version_key") or "",
            "username": lead_post.get("username") or "sydney_news_hub",
            "location": lead_post.get("location") or "",
            "time": lead_post.get("time") or "Just now",
            "previewLabel": "" if lead_post.get("image") else "[News Image Preview]",
            "avatarLetter": "S",
            "commentsList": [
                "This post was published from the researcher prototype.",
                f"Platform mapping: {lead_post.get('platform', 'instagram')}.",
            ],
            "publishedBy": session.get("email", ""),
            "createdAt": publication["published_at"],
            "surveyId": publish_result["survey"]["survey_id"],
        }

    def posts_for_invite(self, invite_code: str) -> list[dict[str, Any]]:
        return self.db.get_published_posts_by_invite_code(invite_code)

    def generate_invite_code(self) -> str:
        return self.db.generate_unique_invite_code()


class BasePrototypeHandler(BaseHTTPRequestHandler):
    server_version = "Prototype2Bridge/1.0"

    @property
    def app_state(self) -> AppState:
        return self.server.app_state  # type: ignore[attr-defined]

    @property
    def server_label(self) -> str:
        return self.server.server_label  # type: ignore[attr-defined]

    def log_message(self, format: str, *args: Any) -> None:
        sys.stdout.write(f"[prototype2:{self.server_label}] {self.address_string()} - {format % args}\n")

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length") or "0")
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        return json.loads(raw_body or "{}")

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html_text: str) -> None:
        body = html_text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, path: str) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", path)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def serve_asset(self, request_path: str) -> None:
        tail = request_path[len(ASSET_PREFIX):]
        parts = tail.split("/", 2)
        if len(parts) != 3:
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found")
            return

        page_kind, mode, relative_path = parts
        try:
            page = self.app_state.page_for_kind(page_kind)
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found")
            return

        base_dir = self.app_state.root if mode == "root" else page.directory
        asset_path = resolve_asset_path(self.app_state.root, base_dir, relative_path)
        if asset_path is None or not asset_path.exists() or not asset_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found")
            return

        content_type = mimetypes.guess_type(asset_path.name)[0] or "application/octet-stream"
        body = asset_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_invite_posts(self, code: str) -> None:
        try:
            posts = self.app_state.store.posts_for_invite(code)
        except Exception as exc:
            self.send_json(
                {
                    "success": False,
                    "posts": [],
                    "inviteCode": normalize_invite_code(code),
                    "error": f"Invite lookup failed: {exc}",
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        self.send_json({"success": True, "posts": posts})

    def send_invite_lookup(self, code: str) -> None:
        try:
            posts = self.app_state.store.posts_for_invite(code)
        except Exception as exc:
            self.send_json(
                {
                    "success": False,
                    "inviteCode": normalize_invite_code(code),
                    "posts": [],
                    "error": f"Invite lookup failed: {exc}",
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        self.send_json(
            {
                "success": bool(posts),
                "inviteCode": normalize_invite_code(code),
                "posts": posts,
                "error": "" if posts else "No published prototype posts match that invite code.",
            }
        )


class ResearcherHandler(BasePrototypeHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/login", "/researcher"}:
            self.serve_login()
            return
        
        if path == "/participant":
            self.serve_participant()
            return

        if path in {"/register", "/signup", "/request-access"}:
            self.serve_register()
            return

        if path in RESEARCHER_EDIT_PATHS:
            session = self.get_session()
            if session is None:
                self.redirect("/")
                return
            self.serve_edit(session)
            return

        if path == "/api/server-info":
            self.send_json(
                {
                    "success": True,
                    "start_time": SERVER_STARTED_AT,
                    "startedAt": SERVER_STARTED_AT,
                }
            )
            return

        if path.startswith("/api/posts/"):
            code = path[len("/api/posts/"):]
            self.send_invite_posts(code)
            return

        if path == "/api/invite":
            code = parse_qs(parsed.query).get("code", [""])[0]
            self.send_invite_lookup(code)
            return

        if path == "/logout":
            self.logout()
            return

        if path.startswith(ASSET_PREFIX):
            self.serve_asset(path)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        try:
            if parsed.path == "/api/register":
                session = self.app_state.store.register_user(self.read_json_body())
                self.set_session_cookie(session)
                self.send_json({"success": True, "user": session})
                return

            if parsed.path == "/api/login":
                session = self.app_state.store.login_user(self.read_json_body())
                if session is None:
                    self.send_json(
                        {"success": False, "error": "wrong password, please try again"},
                        HTTPStatus.UNAUTHORIZED,
                    )
                    return
                self.set_session_cookie(session)
                self.send_json({"success": True, "user": session})
                return

            if parsed.path == "/api/scrape":
                payload = self.read_json_body()
                result = forward_json_request(
                    f"{SCRAPER_INTERNAL_URL}/api/scrape",
                    payload,
                )
                self.send_json(result)
                return

            if parsed.path == "/api/translations/generate":
                payload = self.read_json_body()
                result = forward_json_request(
                    f"{SCRAPER_INTERNAL_URL}/api/translations/generate",
                    payload,
                )
                self.send_json(result)
                return

            if parsed.path == "/api/publish":
                session = self.get_session()
                if session is None:
                    self.send_json({"success": False, "error": "Please log in before publishing."}, HTTPStatus.UNAUTHORIZED)
                    return

                post = self.app_state.store.publish_post(self.read_json_body(), session)
                public_base_url = os.environ.get("PUBLIC_BASE_URL", self.app_state.researcher_origin).rstrip("/")
                participant_url = f"{public_base_url}/participant?invite={quote(post['inviteCode'])}"
                self.send_json(
                    {
                        "success": True,
                        "post": post,
                        "inviteCode": post["inviteCode"],
                        "participantUrl": participant_url,
                    },
                    HTTPStatus.CREATED,
                )
                return

        except json.JSONDecodeError:
            self.send_json({"success": False, "error": "Invalid JSON payload."}, HTTPStatus.BAD_REQUEST)
            return
        except ValueError as exc:
            self.send_json({"success": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    def get_session(self) -> dict[str, str] | None:
        raw_cookie = self.headers.get("Cookie")
        if not raw_cookie:
            return None

        cookie = SimpleCookie()
        try:
            cookie.load(raw_cookie)
        except Exception:
            return None

        morsel = cookie.get(SESSION_COOKIE)
        if morsel is None:
            return None

        return decode_session(morsel.value)

    def set_session_cookie(self, session: dict[str, str]) -> None:
        encoded = encode_session(session)
        self.extra_session_cookie = (
            f"{SESSION_COOKIE}={encoded}; Max-Age={SESSION_MAX_AGE}; Path=/; SameSite=Lax"
        )

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        cookie = getattr(self, "extra_session_cookie", None)
        if cookie:
            self.send_header("Set-Cookie", cookie)
            delattr(self, "extra_session_cookie")
        self.end_headers()
        self.wfile.write(body)

    def serve_login(self) -> None:
        page = self.app_state.login_page
        html_text = rewrite_page_assets(page, load_text(page.entry))
        html_text = inject_before_body_end(html_text, researcher_login_bridge_script())
        self.send_html(html_text)

    def serve_register(self) -> None:
        page = self.app_state.register_page
        html_text = rewrite_page_assets(page, load_text(page.entry))
        html_text = inject_before_body_end(html_text, researcher_register_bridge_script())
        self.send_html(html_text)

    def serve_edit(self, session: dict[str, str]) -> None:
        page = self.app_state.edit_page
        html_text = rewrite_page_assets(page, load_text(page.entry))
        html_text = inject_before_app_script(html_text, researcher_edit_pre_app_script())
        html_text = inject_before_body_end(
            html_text,
            researcher_edit_bridge_script(session, self.app_state.participant_origin),
        )
        self.send_html(html_text)

    def serve_participant(self) -> None:
        page = self.app_state.participant_page
        html_text = rewrite_page_assets(page, load_text(page.entry))
        html_text = inject_before_head_end(html_text, participant_bridge_styles())
        html_text = inject_before_participant_runtime(
            html_text,
            participant_socket_bootstrap_script(self.app_state.camera_origin),
        )
        html_text = inject_before_body_end(
            html_text,
            participant_bridge_script(),
        )
        self.send_html(html_text)

    def logout(self) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/")
        self.send_header("Set-Cookie", f"{SESSION_COOKIE}=; Max-Age=0; Path=/; SameSite=Lax")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()


class ParticipantHandler(BasePrototypeHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/participant"}:
            self.serve_participant()
            return

        if path.startswith("/api/posts/"):
            code = path[len("/api/posts/"):]
            self.send_invite_posts(code)
            return

        if path == "/api/invite":
            code = parse_qs(parsed.query).get("code", [""])[0]
            self.send_invite_lookup(code)
            return

        if path.startswith(ASSET_PREFIX):
            self.serve_asset(path)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    def serve_participant(self) -> None:
        page = self.app_state.participant_page
        html_text = rewrite_page_assets(page, load_text(page.entry))
        html_text = inject_before_head_end(html_text, participant_bridge_styles())
        html_text = inject_before_participant_runtime(
            html_text,
            participant_socket_bootstrap_script(self.app_state.camera_origin),
        )
        html_text = inject_before_body_end(
            html_text,
            participant_bridge_script(),
        )
        self.send_html(html_text)


def researcher_login_bridge_script() -> str:
    return """
<script>
(function () {
  const form = document.getElementById("researcher-login-form");
  const emailInput = document.getElementById("researcher-email") || document.getElementById("researcher-username");
  const passwordInput = document.getElementById("researcher-password");

  if (!form || !emailInput || !passwordInput) {
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    event.stopImmediatePropagation();

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      alert("Please enter both username and password.");
      return;
    }

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
      });
      const result = await response.json();

      if (!result.success) {
        alert(result.error || "Login failed.");
        return;
      }

      window.location.assign("/edit");
    } catch (error) {
      alert("Prototype login service is not available.");
    }
  }, true);
})();
</script>
""".strip()


def researcher_register_bridge_script() -> str:
    return """
<script>
(function () {
  const form = document.getElementById("researcher-register-form");
  const nameInput = document.getElementById("researcher-name");
  const emailInput = document.getElementById("researcher-email") || document.getElementById("researcher-username");
  const passwordInput = document.getElementById("researcher-password");

  if (!form || !emailInput || !passwordInput) {
    return;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    event.stopImmediatePropagation();

    const name = nameInput ? nameInput.value.trim() : "";
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      alert("Please enter username and password.");
      return;
    }

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, email: email, password: password })
      });
      const result = await response.json();

      if (!result.success) {
        alert(result.error || "Sign up failed.");
        return;
      }

      alert("Account created successfully. Please return to the login page");
      window.location.assign("/login");
    } catch (error) {
      alert("Prototype registration service is not available.");
    }
  }, true);
})();
</script>
""".strip()


def researcher_edit_pre_app_script() -> str:
    return """
<script>
(function () {
  window.lucide = window.lucide || { createIcons: function () {} };

  const originalFetch = window.fetch.bind(window);
  window.fetch = function (resource, options) {
    if (resource === "http://localhost:5001/api/scrape" ||
        resource === "http://127.0.0.1:5001/api/scrape") {
      return originalFetch("/api/scrape", options);
    }
    if (resource === "http://localhost:5001/api/translations/generate" ||
        resource === "http://127.0.0.1:5001/api/translations/generate") {
      return originalFetch("/api/translations/generate", options);
    }
    return originalFetch(resource, options);
  };
})();
</script>
""".strip()


def researcher_edit_bridge_script(session: dict[str, str], participant_origin: str) -> str:
    session_json = json_for_script(session)
    participant_origin_json = json_for_script(participant_origin)

    return f"""
<script>
(function () {{
  const session = {session_json};
  const participantOrigin = {participant_origin_json};
  
  function statusPanel() {{
    let panel = document.getElementById("prototype2-publish-status");
    if (panel) return panel;

    panel = document.createElement("div");
    panel.id = "prototype2-publish-status";
    panel.className = "mt-3 rounded-md border border-sky-200 bg-sky-50 p-3 text-xs text-sky-800";
    // 适配新版前端的面板位置
    const accessBox = document.getElementById("btn-generate-code")?.closest(".p-4") 
                   || document.querySelector(".p-4.bg-blue-50");
    if (accessBox) {{
      accessBox.appendChild(panel);
    }}
    return panel;
  }}

  function setUserDetails() {{
    const userButton = document.getElementById("user-menu-btn");
    if (userButton) {{
      userButton.textContent = session.initial || "R";
    }}

    const dropdownEmail = document.querySelector("#user-dropdown span.text-sm.text-gray-300")
                       || document.querySelector("#user-dropdown div.text-gray-400"); // 适配新版
    if (dropdownEmail) {{
      dropdownEmail.textContent = session.email || "researcher@example.com";
    }}

    const greeting = document.querySelector("#user-dropdown h2.text-xl.font-medium")
                  || document.querySelector("#user-dropdown h2.text-xl"); // 适配新版
    if (greeting) {{
      greeting.textContent = "Hi, " + (session.name || "Researcher") + "!";
    }}

    const logoutBtn = document.getElementById("researcher-sign-out-btn");
    if (logoutBtn) {{
      logoutBtn.addEventListener("click", function () {{
        window.location.assign("/logout");
      }});
    }}
  }}

  // 拦截 fetch 以处理发布成功的状态显示
  const originalFetch = window.fetch;
  window.fetch = async function (resource, options) {{
    const response = await originalFetch(resource, options);
    
    if (resource === "/api/publish" && response.ok) {{
      const clone = response.clone();
      try {{
        const result = await clone.json();
        if (result.success && result.participantUrl) {{
          const panel = statusPanel();
          if (panel) {{
            panel.innerHTML =
              "<strong>Published.</strong> Invite code <strong>" + result.inviteCode +
              "</strong> is ready.<br>Participant Link: <a class=\\"underline\\" href=\\"" + result.participantUrl +
              "\\" target=\\"_blank\\">" + result.participantUrl + "</a>";
          }}
        }}
      }} catch (e) {{}}
    }}
    return response;
  }};

  setUserDetails();
}})();
</script>
""".strip()


def participant_bridge_styles() -> str:
    return """
<style>
  .prototype2-style-rail {
    position: fixed;
    left: 18px;
    top: 50%;
    z-index: 1200;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transform: translateY(-50%);
  }

  .prototype2-style-btn {
    width: 52px;
    height: 52px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    box-shadow: var(--shadow-soft);
    transition: 0.18s ease;
  }

  .prototype2-style-btn:hover {
    transform: translateY(-1px);
  }

  .prototype2-style-btn.active {
    border-color: var(--text);
    color: var(--surface);
    background: var(--text);
  }

  .prototype2-style-btn svg {
    width: 24px;
    height: 24px;
  }

  .prototype2-empty-platform {
    width: min(100%, 420px);
    margin: 0 auto;
    padding: 28px;
    border: 1px solid var(--border);
    border-radius: 22px;
    background: var(--surface);
    box-shadow: var(--shadow-soft);
    text-align: center;
    color: var(--muted-2);
  }

  .prototype2-media-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .prototype2-card {
    width: min(100%, 430px);
    margin: 0 auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    background: var(--surface);
    box-shadow: var(--shadow-soft);
  }

  .prototype2-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 14px;
  }

  .prototype2-card button {
    color: inherit;
  }

  .prototype2-user {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
  }

  .prototype2-avatar {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border-radius: 999px;
    background: var(--story-gradient);
    color: #fff;
    font-weight: 800;
  }

  .prototype2-name {
    font-size: 14px;
    font-weight: 800;
    line-height: 1.2;
  }

  .prototype2-subline {
    color: var(--muted-2);
    font-size: 12px;
    line-height: 1.25;
  }

  .prototype2-media {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: var(--placeholder-bg);
  }

  .prototype2-media.square {
    aspect-ratio: 1 / 1;
  }

  .prototype2-media.landscape {
    aspect-ratio: 16 / 9;
  }

  .prototype2-media.portrait {
    aspect-ratio: 9 / 16;
    max-height: 620px;
  }

  .prototype2-placeholder {
    color: var(--muted);
    font-size: 14px;
  }

  .prototype2-empty-media {
    display: grid;
    place-items: center;
    gap: 8px;
    color: var(--muted);
    font-size: 14px;
  }

  .prototype2-empty-media svg {
    width: 44px;
    height: 44px;
    opacity: 0.5;
  }

  .prototype2-body {
    padding: 14px;
  }

  .prototype2-actions {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    color: var(--muted-2);
    font-size: 13px;
  }

  .prototype2-action-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
  }

  .prototype2-action-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .prototype2-platform-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: var(--muted-2);
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
    position: relative;
  }

  .prototype2-platform-action svg {
    width: 22px;
    height: 22px;
  }

  .prototype2-icon-filled {
    fill: currentColor;
  }

  .prototype2-caption {
    margin-top: 12px;
    font-size: 14px;
    line-height: 1.45;
  }

  .prototype2-instagram .prototype2-card-header {
    border-bottom: 1px solid var(--border-soft);
  }

  .prototype2-instagram .prototype2-body {
    padding: 12px 14px;
  }

  .prototype2-instagram .prototype2-like-line {
    margin-top: 10px;
    font-size: 14px;
    font-weight: 700;
  }

  .prototype2-instagram .prototype2-caption {
    margin-top: 8px;
  }

  .prototype2-instagram .prototype2-comments-link {
    margin-top: 8px;
    color: var(--muted-2);
    font-size: 14px;
  }

  .prototype2-instagram-time {
    margin-top: 8px;
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .prototype2-facebook {
    border-radius: 12px;
  }

  .prototype2-facebook .prototype2-avatar {
    background: #1877f2;
  }

  .prototype2-facebook-caption {
    padding: 0 16px 12px;
    font-size: 14px;
    line-height: 1.45;
  }

  .prototype2-facebook-stats {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    padding: 9px 16px;
    border-bottom: 1px solid var(--border);
    color: var(--muted-2);
    font-size: 13px;
  }

  .prototype2-facebook-reaction {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    margin-right: 6px;
    border-radius: 999px;
    background: #1877f2;
    color: #fff;
    vertical-align: middle;
  }

  .prototype2-facebook-reaction svg {
    width: 11px;
    height: 11px;
  }

  .prototype2-facebook-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    padding: 4px 12px;
  }

  .prototype2-facebook-buttons .prototype2-platform-action {
    color: var(--muted-2);
    padding: 7px 0;
  }

  .prototype2-x {
    border-radius: 0;
    width: min(100%, 500px);
    padding: 16px;
  }

  .prototype2-x .prototype2-avatar {
    background: #111;
  }

  .prototype2-x-layout {
    display: flex;
    gap: 12px;
  }

  .prototype2-x-content {
    flex: 1;
    min-width: 0;
  }

  .prototype2-x-meta {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    line-height: 1.25;
  }

  .prototype2-x-verified {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    border-radius: 999px;
    background: #1d9bf0;
    color: #fff;
  }

  .prototype2-x-verified svg {
    width: 11px;
    height: 11px;
  }

  .prototype2-x-handle {
    color: var(--muted-2);
    font-size: 14px;
  }

  .prototype2-x-caption {
    margin: 4px 0 12px;
    font-size: 15px;
    line-height: 1.35;
  }

  .prototype2-x .prototype2-media {
    border: 1px solid var(--border);
    border-radius: 16px;
  }

  .prototype2-x-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    color: var(--muted-2);
  }

  .prototype2-x-actions .prototype2-platform-action {
    min-height: 24px;
    font-weight: 500;
  }

  .prototype2-x-actions svg {
    width: 18px;
    height: 18px;
  }

  .prototype2-tiktok {
    width: min(100%, 320px);
    height: 580px;
    border-radius: 8px;
    background: #050505;
    color: #fff;
    position: relative;
    border: 0;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
  }

  .prototype2-tiktok .prototype2-media {
    position: absolute;
    inset: 0;
    height: 100%;
    background: #111;
  }

  .prototype2-tiktok .prototype2-media-img {
    opacity: 0.86;
  }

  .prototype2-tiktok-side {
    position: absolute;
    right: 10px;
    bottom: 72px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }

  .prototype2-tiktok-avatar {
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border: 2px solid #fff;
    border-radius: 999px;
    background: linear-gradient(135deg, #fb7185, #7c3aed);
    color: #fff;
    font-size: 20px;
    font-weight: 800;
    position: relative;
  }

  .prototype2-tiktok-plus {
    position: absolute;
    left: 50%;
    bottom: -9px;
    width: 18px;
    height: 18px;
    display: grid;
    place-items: center;
    transform: translateX(-50%);
    border: 1px solid #fff;
    border-radius: 999px;
    background: #ec4899;
    color: #fff;
    font-size: 12px;
    line-height: 1;
  }

  .prototype2-tiktok-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    min-height: auto;
    color: #fff;
    text-shadow: 0 1px 10px rgba(0, 0, 0, 0.75);
    font-size: 12px;
    font-weight: 700;
  }

  .prototype2-tiktok-action svg {
    width: 32px;
    height: 32px;
    filter: drop-shadow(0 1px 6px rgba(0, 0, 0, 0.45));
  }

  .prototype2-tiktok-copy {
    position: absolute;
    left: 16px;
    right: 68px;
    bottom: 14px;
    z-index: 2;
    color: #fff;
    text-shadow: 0 1px 10px rgba(0, 0, 0, 0.75);
  }

  .prototype2-tiktok-copy strong {
    display: block;
    margin-bottom: 5px;
    font-size: 15px;
  }

  .prototype2-tiktok-copy p {
    margin: 0;
    font-size: 14px;
    line-height: 1.3;
  }

  .prototype2-tiktok-sound {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
    font-size: 13px;
    font-weight: 600;
  }

  .prototype2-tiktok-sound svg {
    width: 16px;
    height: 16px;
  }

  .prototype2-detail-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  @media (max-width: 900px) {
    .prototype2-style-rail {
      left: 50%;
      top: auto;
      bottom: 14px;
      flex-direction: row;
      transform: translateX(-50%);
    }
  }
</style>
""".strip()


def participant_socket_bootstrap_script(camera_origin: str) -> str:
    camera_origin_json = json_for_script(camera_origin)
    return f"""
<script>
(function () {{
  const cameraOrigin = {camera_origin_json};

  function createSocketIoLite(origin) {{
    if (typeof WebSocket !== "function") {{
      return null;
    }}

    const handlers = {{}};
    const socket = {{
      connected: false,
      on: function (eventName, handler) {{
        handlers[eventName] = handlers[eventName] || [];
        handlers[eventName].push(handler);
      }},
      emit: function (eventName, payload) {{
        if (!socket.connected || !socket.rawSocket || socket.rawSocket.readyState !== WebSocket.OPEN) return;
        socket.rawSocket.send("42" + JSON.stringify([eventName, payload]));
      }}
    }};

    function fire(eventName, payload) {{
      (handlers[eventName] || []).forEach(function (handler) {{
        handler(payload);
      }});
    }}

    const rawSocket = new WebSocket(origin.replace(/^http/i, "ws") + "/socket.io/?EIO=4&transport=websocket");
    socket.rawSocket = rawSocket;
    rawSocket.onmessage = function (message) {{
      const text = String(message.data || "");
      if (text === "2") {{
        rawSocket.send("3");
        return;
      }}
      if (text.startsWith("0")) {{
        rawSocket.send("40");
        return;
      }}
      if (text.startsWith("40")) {{
        socket.connected = true;
        fire("connect");
        return;
      }}
      if (text.startsWith("42")) {{
        try {{
          const packet = JSON.parse(text.slice(2));
          fire(packet[0], packet[1]);
        }} catch (error) {{}}
      }}
    }};
    rawSocket.onerror = function () {{
      fire("connect_error");
    }};
    rawSocket.onclose = function () {{
      socket.connected = false;
      fire("disconnect");
    }};
    return socket;
  }}

  const originalIo = window.io;
  window.io = function (url, options) {{
    if (typeof originalIo === "function") {{
      return originalIo(url || cameraOrigin, options || {{ transports: ["websocket", "polling"] }});
    }}
    return createSocketIoLite(url || cameraOrigin);
  }};
}})();
</script>
""".strip()


def participant_bridge_script() -> str:
    return """
<script>
(function () {
  const hasCalibrationFlow = document.getElementById("calScreen") && document.getElementById("cal-id-badge");
  if (!hasCalibrationFlow) {
    return;
  }

  const platformOrder = ["instagram", "facebook", "x", "tiktok"];
  const platformNames = { instagram: "Instagram", facebook: "Facebook", x: "X", tiktok: "TikTok" };
  const platformIcons = {
    instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.5" cy="6.5" r="1"></circle></svg>',
    facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-3 0-5 2-5 5v3H6v4h3v4h4v-4h3.2l.8-4H13V9c0-.7.3-1 1-1z"></path></svg>',
    x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4l7.2 8.5L4.5 20h3.1l5-5.9L17.5 20H20l-7.4-8.8L19 4h-3.1l-4.7 5.6L6.6 4H4z"></path></svg>',
    tiktok: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4c.7 1.7 2.1 3 4 3.5V11c-1.5-.1-2.9-.6-4-1.5v5.7a4.7 4.7 0 1 1-4.7-4.7c.3 0 .7 0 1 .1v3.1a2 2 0 1 0 1.7 2V4h2z"></path></svg>'
  };
  let activeInviteCode = "";
  let activePlatform = "instagram";
  let platformPosts = { instagram: [], facebook: [], x: [], tiktok: [] };

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizePlatform(value) {
    const platform = String(value || "instagram").toLowerCase();
    return platformOrder.includes(platform) ? platform : "instagram";
  }

  function normalizePost(raw, index) {
    const username = raw.username || "sydney_news_hub";
    return {
      username: username,
      location: raw.location || "Sydney, Australia",
      time: raw.time || "Just now",
      caption: raw.caption || "",
      likes: Number(raw.likes || 0),
      comments: Number(raw.comments || 0),
      shares: Number(raw.shares || 0),
      previewLabel: raw.image ? "" : (raw.previewLabel || "[News Image Preview]"),
      image: raw.image || "",
      platform: normalizePlatform(raw.platform),
      avatarLetter: raw.avatarLetter || username.charAt(0).toUpperCase() || "S",
      commentsList: Array.isArray(raw.commentsList) && raw.commentsList.length
        ? raw.commentsList
        : ["Published from the researcher prototype.", "Shown only in its matching platform module."],
      prototypePostId: raw.id || String(index + 1)
    };
  }

  const postIcons = {
    image: '<rect x="3" y="3" width="18" height="18" rx="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><path d="M21 15l-5-5L5 21"></path>',
    heart: '<path d="m12 21-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.18z"></path>',
    messageCircle: '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 17 0z"></path>',
    messageSquare: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>',
    send: '<line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>',
    bookmark: '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>',
    thumbsUp: '<path d="M7 10v10"></path><path d="M15 6.5 14 10h5.2a2 2 0 0 1 2 2.3l-1 6A2 2 0 0 1 18.2 20H7a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2h2.2L12 4.5a2 2 0 0 1 3 .3c.2.5.2 1.1 0 1.7z"></path>',
    share2: '<circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><path d="M8.6 13.5 15.4 17.5"></path><path d="M15.4 6.5 8.6 10.5"></path>',
    repeat2: '<path d="m17 1 4 4-4 4"></path><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><path d="m7 23-4-4 4-4"></path><path d="M21 13v2a4 4 0 0 1-4 4H3"></path>',
    barChart: '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>',
    globe: '<circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15 15 0 0 1 0 20"></path><path d="M12 2a15 15 0 0 0 0 20"></path>',
    check: '<path d="m5 12 4 4L19 6"></path>',
    forward: '<path d="m15 17 5-5-5-5"></path><path d="M4 18v-2a4 4 0 0 1 4-4h12"></path>',
    music: '<path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle>'
  };

  function icon(name, className) {
    return '<svg' + (className ? ' class="' + className + '"' : '') + ' viewBox="0 0 24 24" aria-hidden="true">' + postIcons[name] + '</svg>';
  }

  function compactCount(value) {
    const number = Number(value || 0);
    if (number >= 1000) {
      return (number / 1000).toFixed(1).replace(/\\.0$/, "") + "K";
    }
    return fc(number);
  }

  function handleFor(username) {
    const handle = String(username || "news").replace(/[^a-zA-Z0-9_]/g, "").slice(0, 14).toLowerCase();
    return "@" + (handle || "news");
  }

  function mediaHtml(data) {
    if (data.image) {
      return '<img class="prototype2-media-img" src="' + escapeHtml(data.image) + '" alt="Published post media">';
    }
    return '<div class="prototype2-empty-media">' + icon("image") + '<span>' + escapeHtml(data.previewLabel || "[News Image Preview]") + '</span></div>';
  }

  function headerHtml(d, name, subtitle) {
    return '<div class="prototype2-card-header">' +
      '<div class="prototype2-user">' +
        '<div class="prototype2-avatar">' + escapeHtml(d.avatarLetter || "S") + '</div>' +
        '<div><div class="prototype2-name">' + escapeHtml(name) + '</div><div class="prototype2-subline">' + escapeHtml(subtitle) + '</div></div>' +
      '</div>' +
      '<button class="icon-btn more-btn-preview" type="button">•••</button>' +
    '</div>';
  }

  function renderInstagramCard(id, d) {
    return '<article class="prototype2-card prototype2-instagram" data-post-id="' + id + '">' +
      headerHtml(d, d.username, d.location) +
      '<button class="prototype2-media square open-post-modal" type="button" data-post="' + id + '">' + mediaHtml(d) + '</button>' +
      '<div class="prototype2-body">' +
        '<div class="prototype2-action-row">' +
          '<div class="prototype2-action-group">' +
            '<button class="prototype2-platform-action like-btn" type="button" data-liked="false">' + icon("heart") + '<span class="action-inline-count like-count" style="display:none">' + fc(d.likes) + '</span><span class="count-float">+1</span></button>' +
            '<button class="prototype2-platform-action open-post-modal" type="button" data-post="' + id + '">' + icon("messageCircle") + '</button>' +
            '<button class="prototype2-platform-action" type="button">' + icon("send") + '</button>' +
          '</div>' +
          '<button class="prototype2-platform-action" type="button">' + icon("bookmark") + '</button>' +
        '</div>' +
        '<div class="prototype2-like-line"><span class="like-count-text">' + fc(d.likes) + '</span> likes</div>' +
        '<div class="prototype2-caption"><strong>' + escapeHtml(d.username) + '</strong> ' + escapeHtml(d.caption) + '</div>' +
        '<button class="prototype2-comments-link open-post-modal" type="button" data-post="' + id + '">View all ' + fc(d.comments) + ' comments</button>' +
        '<div class="prototype2-instagram-time">' + escapeHtml(d.time) + '</div>' +
      '</div>' +
    '</article>';
  }

  function renderFacebookCard(id, d) {
    return '<article class="prototype2-card prototype2-facebook" data-post-id="' + id + '">' +
      headerHtml(d, "Sydney News Hub", d.time + " · Public") +
      '<div class="prototype2-facebook-caption">' + escapeHtml(d.caption) + '</div>' +
      '<button class="prototype2-media landscape open-post-modal" type="button" data-post="' + id + '">' + mediaHtml(d) + '</button>' +
      '<div class="prototype2-facebook-stats">' +
        '<div><span class="prototype2-facebook-reaction">' + icon("thumbsUp") + '</span><span class="like-count-text">' + fc(d.likes) + '</span></div>' +
        '<div>' + fc(d.comments) + ' comments · ' + fc(d.shares || 0) + ' shares</div>' +
      '</div>' +
      '<div class="prototype2-facebook-buttons">' +
        '<button class="prototype2-platform-action like-btn" type="button" data-liked="false">' + icon("thumbsUp") + '<span>Like</span><span class="action-inline-count like-count" style="display:none">' + fc(d.likes) + '</span><span class="count-float">+1</span></button>' +
        '<button class="prototype2-platform-action open-post-modal" type="button" data-post="' + id + '">' + icon("messageSquare") + '<span>Comment</span></button>' +
        '<button class="prototype2-platform-action" type="button">' + icon("share2") + '<span>Share</span></button>' +
      '</div>' +
    '</article>';
  }

  function renderXCard(id, d) {
    const handle = handleFor(d.username);
    return '<article class="prototype2-card prototype2-x" data-post-id="' + id + '">' +
      '<div class="prototype2-x-layout">' +
        '<div class="prototype2-avatar">' + escapeHtml(d.avatarLetter || "S") + '</div>' +
        '<div class="prototype2-x-content">' +
          '<div class="prototype2-x-meta"><strong>Sydney News Hub</strong><span class="prototype2-x-verified">' + icon("check") + '</span><span class="prototype2-x-handle">' + escapeHtml(handle) + ' · ' + escapeHtml(d.time) + '</span></div>' +
          '<div class="prototype2-x-caption">' + escapeHtml(d.caption) + '</div>' +
          '<button class="prototype2-media landscape open-post-modal" type="button" data-post="' + id + '">' + mediaHtml(d) + '</button>' +
          '<div class="prototype2-x-actions">' +
            '<button class="prototype2-platform-action open-post-modal" type="button" data-post="' + id + '">' + icon("messageCircle") + '<span>' + fc(d.comments) + '</span></button>' +
            '<button class="prototype2-platform-action" type="button">' + icon("repeat2") + '<span>' + fc(d.shares || 0) + '</span></button>' +
            '<button class="prototype2-platform-action like-btn" type="button" data-liked="false">' + icon("heart") + '<span class="action-inline-count like-count">' + fc(d.likes) + '</span><span class="count-float">+1</span></button>' +
            '<button class="prototype2-platform-action" type="button">' + icon("barChart") + '<span>12K</span></button>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</article>';
  }

  function renderTikTokCard(id, d) {
    const handle = handleFor(d.username);
    return '<article class="prototype2-card prototype2-tiktok" data-post-id="' + id + '">' +
      '<button class="prototype2-media portrait open-post-modal" type="button" data-post="' + id + '">' + mediaHtml(d) + '</button>' +
      '<div class="prototype2-tiktok-side">' +
        '<div class="prototype2-tiktok-avatar">' + escapeHtml(d.avatarLetter || "S") + '<span class="prototype2-tiktok-plus">+</span></div>' +
        '<button class="prototype2-tiktok-action like-btn" type="button" data-liked="false">' + icon("heart") + '<span class="action-inline-count like-count">' + compactCount(d.likes) + '</span><span class="count-float">+1</span></button>' +
        '<button class="prototype2-tiktok-action open-post-modal" type="button" data-post="' + id + '">' + icon("messageCircle") + '<span>' + compactCount(d.comments) + '</span></button>' +
        '<button class="prototype2-tiktok-action" type="button">' + icon("bookmark") + '<span>Save</span></button>' +
        '<button class="prototype2-tiktok-action" type="button">' + icon("forward") + '<span>' + fc(d.shares || 0) + '</span></button>' +
      '</div>' +
      '<div class="prototype2-tiktok-copy">' +
        '<strong>' + escapeHtml(handle) + '</strong>' +
        '<p>' + escapeHtml(d.caption) + '</p>' +
        '<div class="prototype2-tiktok-sound">' + icon("music") + '<span>original sound - Sydney News</span></div>' +
      '</div>' +
    '</article>';
  }

  function renderPlatformCard(id) {
    const d = postData[id];
    if (!d) return "";
    const p = activePlatform;
    if (p === "facebook") return renderFacebookCard(id, d);
    if (p === "x") return renderXCard(id, d);
    if (p === "tiktok") return renderTikTokCard(id, d);
    return renderInstagramCard(id, d);
  }

  function renderEmptyPlatform(platform) {
    currentPostId = 0;
    sPC.innerHTML =
      '<div class="prototype2-empty-platform">' +
        '<strong>' + platformNames[platform] + '</strong><br>' +
        'No researcher post has been published for this platform yet.' +
      '</div>';
    updateStoryBar([]);
  }

  function updateStoryBar(posts) {
    Array.from(document.querySelectorAll(".story-button")).forEach(function (button, index) {
      const post = posts[index];
      const item = button.closest(".story-item");
      if (!post) {
        button.dataset.prototype2Hidden = "true";
        if (item) item.style.display = "none";
        return;
      }
      delete button.dataset.prototype2Hidden;
      if (item) item.style.display = "";
      const label = button.querySelector(".story-label");
      const photo = button.querySelector(".story-avatar-photo");
      if (label) label.textContent = platformNames[activePlatform] + " " + (index + 1);
      if (photo) photo.textContent = String(index + 1);
    });
    storyPage = 0;
    updateStoryTrack();
  }

  function applyPlatform(platform) {
    activePlatform = normalizePlatform(platform);
    const posts = platformPosts[activePlatform] || [];
    postData = {};
    posts.slice(0, 12).forEach(function (post, index) {
      postData[index + 1] = post;
    });
    totalPages = Math.max(1, Math.ceil(Math.max(posts.length, 1) / storiesPerPage));
    updateStyleRail();
    if (!posts.length) {
      renderEmptyPlatform(activePlatform);
      return;
    }
    updateStoryBar(posts);
    renderCurrentPost(1);
  }

  function installStyleRail() {
    if (document.getElementById("prototype2StyleRail")) return;
    const rail = document.createElement("div");
    rail.id = "prototype2StyleRail";
    rail.className = "prototype2-style-rail";
    rail.style.display = "none";
    rail.innerHTML = platformOrder.map(function (platform) {
      return '<button class="prototype2-style-btn" type="button" data-platform="' + platform + '" aria-label="' + platformNames[platform] + ' style">' + platformIcons[platform] + '</button>';
    }).join("");
    rail.addEventListener("click", function (event) {
      const button = event.target.closest("[data-platform]");
      if (!button) return;
      applyPlatform(button.dataset.platform);
    });
    document.body.appendChild(rail);
  }

  function updateStyleRail() {
    installStyleRail();
    document.querySelectorAll(".prototype2-style-btn").forEach(function (button) {
      button.classList.toggle("active", button.dataset.platform === activePlatform);
    });
  }

  function firstPlatformWithPosts() {
    return platformOrder.find(function (platform) {
      return platformPosts[platform] && platformPosts[platform].length;
    }) || "instagram";
  }

  function applyPublishedPosts(posts) {
    platformPosts = { instagram: [], facebook: [], x: [], tiktok: [] };
    posts.map(normalizePost).forEach(function (post) {
      platformPosts[post.platform].push(post);
    });
    installStyleRail();
    applyPlatform(firstPlatformWithPosts());
  }

  mkPost = function (id) {
    return renderPlatformCard(id);
  };

  fillDetail = function (id) {
    const d = postData[id];
    if (!d) return;
    document.getElementById("detailUsername").textContent = d.username;
    document.getElementById("detailLocation").textContent = platformNames[activePlatform] + " · " + d.time;
    document.getElementById("detailCaptionUser").textContent = d.username;
    document.getElementById("detailCaptionText").textContent = d.caption;
    document.getElementById("detailLikeCount").textContent = fc(d.likes);
    document.getElementById("detailCommentCount").textContent = fc(d.comments);
    document.getElementById("detailLikeCountText").textContent = fc(d.likes);
    document.getElementById("detailCommentCountText").textContent = fc(d.comments);
    document.getElementById("detailBottomTime").textContent = fbt(d.time);
    document.getElementById("detailAvatarText").textContent = d.avatarLetter || avl(d.username, "S");
    document.getElementById("detailComments").innerHTML = commentLines(d);
    const media = document.querySelector(".detail-media-placeholder");
    if (media) {
      media.innerHTML = d.image
        ? '<img class="prototype2-detail-img" src="' + escapeHtml(d.image) + '" alt="Published post media">'
        : '<div class="preview-image-placeholder"><span id="detailMediaText">' + escapeHtml(d.previewLabel || "[News Image Preview]") + '</span></div>';
    }
  };

  if (typeof enterStudy === "function") {
    const originalEnterStudy = enterStudy;
    enterStudy = function () {
      originalEnterStudy();
      installStyleRail();
      updateStyleRail();
      const rail = document.getElementById("prototype2StyleRail");
      if (rail) rail.style.display = "flex";
    };
  }

  async function verifyInvite(event) {
    if (event) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
    const code = document.getElementById("inviteInput").value.trim().toUpperCase();
    if (!code) {
      alert("Please enter an invitation code.");
      return;
    }
    try {
      const response = await fetch("/api/invite?code=" + encodeURIComponent(code));
      const result = await response.json();
      if (!result.success || !result.posts.length) {
        alert(result.error || "Invite code not found.");
        return;
      }
      activeInviteCode = result.inviteCode || code;
      participantId = activeInviteCode;
      studyData.participantId = activeInviteCode;
      document.getElementById("cal-id-badge").textContent = "ID: " + activeInviteCode;
      applyPublishedPosts(result.posts);
      hide("inviteScreen");
      show("calScreen");
      appPhase = "CAL_WELCOME";
    } catch (error) {
      alert("Participant prototype service is not available.");
    }
  }

  document.getElementById("verifyInviteBtn").addEventListener("click", verifyInvite, true);
  document.getElementById("inviteInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") verifyInvite(event);
  }, true);

  const queryInvite = new URLSearchParams(window.location.search).get("invite");
  if (queryInvite) {
    document.getElementById("inviteInput").value = queryInvite.toUpperCase();
  }
})();
</script>
""".strip()


def forward_json_request(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    import urllib.error
    import urllib.request

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body or "{}")
    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read().decode("utf-8")
            return json.loads(error_body or "{}")
        except Exception:
            return {"success": False, "error": f"Scraper API returned HTTP {exc.code}."}
    except Exception as exc:
        return {"success": False, "error": f"Scraper API is not available: {exc}"}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def inject_before_body_end(html_text: str, injected: str) -> str:
    marker = "</body>"
    if marker in html_text:
        return html_text.replace(marker, f"{injected}\n{marker}", 1)
    return html_text + "\n" + injected


def inject_before_head_end(html_text: str, injected: str) -> str:
    marker = "</head>"
    if marker in html_text:
        return html_text.replace(marker, f"{injected}\n{marker}", 1)
    return injected + "\n" + html_text


def inject_before_participant_runtime(html_text: str, injected: str) -> str:
    marker = "<script>\n/* ══════════════════════════════════════════════════\n   SOCKET.IO"
    if marker in html_text:
        return html_text.replace(marker, f"{injected}\n{marker}", 1)
    return inject_before_body_end(html_text, injected)


def inject_before_app_script(html_text: str, injected: str) -> str:
    pattern = re.compile(r'(<script\b[^>]*\bsrc=["\'][^"\']*app\.js["\'][^>]*>\s*</script>)', re.IGNORECASE)
    match = pattern.search(html_text)
    if not match:
        return inject_before_body_end(html_text, injected)
    return html_text[:match.start()] + injected + "\n" + html_text[match.start():]


def is_external_asset_url(value: str) -> bool:
    stripped = value.strip().lower()
    return (
        not stripped
        or stripped.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "javascript:", "#"))
    )


def build_asset_route(page: PageTarget, original_value: str) -> str:
    mode = "root" if original_value.startswith("/") else "page"
    relative = original_value[1:] if mode == "root" else original_value
    encoded = quote(relative, safe="/._-~")
    return f"{ASSET_PREFIX}{page.kind}/{mode}/{encoded}"


def rewrite_page_assets(page: PageTarget, html_text: str) -> str:
    rewritten = html_text

    def replace_match(match: re.Match[str]) -> str:
        prefix, value, suffix = match.groups()
        if is_external_asset_url(value):
            return match.group(0)
        return f"{prefix}{build_asset_route(page, value)}{suffix}"

    for pattern in ASSET_TAG_PATTERNS:
        rewritten = pattern.sub(replace_match, rewritten)

    return rewritten


def resolve_asset_path(root: Path, base_dir: Path, relative_path: str) -> Path | None:
    candidate = (base_dir / Path(unquote(relative_path))).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def json_for_script(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def normalize_email(value: Any) -> str:
    return str(value or "").strip().lower()


def derive_name(email: str) -> str:
    local = email.split("@", 1)[0].strip()
    parts = [part for part in re.split(r"[-_.]+", local) if part]
    if not parts:
        return "Researcher"
    return " ".join(part[:1].upper() + part[1:] for part in parts[:2])


def session_for_user(user: dict[str, Any]) -> dict[str, str]:
    name = str(user.get("name") or derive_name(str(user.get("email") or ""))).strip() or "Researcher"
    session = {
        "email": normalize_email(user.get("email")),
        "name": name,
        "initial": (name[:1] or "R").upper(),
    }
    if user.get("session_token"):
        session["session_token"] = str(user.get("session_token"))
    return session


def encode_session(session: dict[str, str]) -> str:
    raw = json.dumps(session, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_session(value: str) -> dict[str, str] | None:
    try:
        padded = value + "=" * (-len(value) % 4)
        decoded = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        data = json.loads(decoded)
        email = normalize_email(data.get("email"))
        if not email:
            return None
        return session_for_user(data)
    except Exception:
        return None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_platform(value: Any) -> str:
    platform = str(value or "instagram").strip().lower()
    return platform if platform in {"instagram", "facebook", "x", "tiktok"} else "instagram"


def normalize_invite_code(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(value or "").upper())[:12]


def parse_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def extract_published_variant(news_item: dict[str, Any], version_label: str) -> dict[str, Any]:
    legacy_variant = news_item.get("variant")
    if isinstance(legacy_variant, dict) and legacy_variant:
        return legacy_variant

    versions = news_item.get("versions")
    if not isinstance(versions, dict) or not versions:
        return {}

    version = versions.get(version_label) or versions.get("vA") or next(iter(versions.values()))
    if not isinstance(version, dict):
        return {}

    platform = normalize_platform(version.get("platform"))
    platform_variants = version.get("platformVariants")
    if isinstance(platform_variants, dict):
        platform_variant = platform_variants.get(platform)
        if not isinstance(platform_variant, dict):
            platform_variant = next(
                (value for value in platform_variants.values() if isinstance(value, dict)),
                None,
            )
        if isinstance(platform_variant, dict) and platform_variant:
            return {
                **version,
                **platform_variant,
                "platform": normalize_platform(platform_variant.get("platform") or platform),
            }

    return version


def display_origin(host: str, port: int) -> str:
    display_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    if ":" in display_host and not display_host.startswith("["):
        display_host = f"[{display_host}]"
    return f"http://{display_host}:{port}"


def ensure_required_files() -> None:
    required = (
        RESEARCHER_LOGIN_HTML,
        RESEARCHER_REGISTER_HTML,
        RESEARCHER_EDIT_HTML,
        RESEARCHER_SCRAPER_BACKEND,
        PARTICIPANT_HTML,
        CAMERA_BACKEND,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        joined = "\n  ".join(missing)
        raise FileNotFoundError(f"Prototype bridge is missing required source files:\n  {joined}")


def python_for_backend(script_path: Path) -> str:
    venv_python = script_path.parent / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def port_is_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.35):
            return True
    except OSError:
        return False


def bridge_ports_in_use(host: str, labelled_ports: tuple[tuple[str, int], ...]) -> list[tuple[str, int]]:
    return [(label, port) for label, port in labelled_ports if port_is_open(host, port)]


def stream_process_output(name: str, process: subprocess.Popen[str]) -> None:
    if process.stdout is None:
        return
    for line in process.stdout:
        sys.stdout.write(f"[{name}] {line}")


def start_internal_process(
    name: str,
    command: list[str],
    cwd: Path,
    host: str,
    port: int,
    env: dict[str, str] | None = None,
) -> subprocess.Popen[str] | None:
    if port_is_open(host, port):
        print(f"[internal] {name} already appears to be running on {host}:{port}; reusing it.")
        return None

    process_env = os.environ.copy()
    process_env.setdefault("PYTHONUNBUFFERED", "1")
    if env:
        process_env.update(env)

    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        env=process_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    threading.Thread(target=stream_process_output, args=(name, process), daemon=True).start()
    time.sleep(1.2)

    if process.poll() is not None:
        print(f"[internal] {name} exited early with code {process.returncode}.")
    else:
        print(f"[internal] {name} started on {host}:{port}.")

    return process


def stop_processes(processes: list[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()

    deadline = time.time() + 5
    for process in processes:
        while process.poll() is None and time.time() < deadline:
            time.sleep(0.1)
        if process.poll() is None:
            process.kill()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the isolated Prototype 2.0 researcher/participant bridge.")
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host for the two user-facing bridge servers.",
)
    parser.add_argument("--researcher-port", type=int, default=8120, help="Researcher URL port.")
    parser.add_argument("--participant-port", type=int, default=8121, help="Participant URL port.")
    parser.add_argument("--camera-port", type=int, default=DEFAULT_CAMERA_PORT, help="Internal camera backend port.")
    parser.add_argument("--no-backends", action="store_true", help="Do not auto-start existing scraper/camera backends.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if len({args.researcher_port, args.participant_port, SCRAPER_PORT, args.camera_port}) != 4:
        parser.error("researcher, participant, scraper, and camera ports must all be different.")

    ensure_required_files()

    public_base_url = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

    researcher_origin = public_base_url or display_origin(args.host, args.researcher_port)
    participant_origin = display_origin(args.host, args.participant_port)
    camera_origin = os.environ.get(
        "CAMERA_PUBLIC_ORIGIN",
        display_origin(args.host, args.camera_port),
    ).rstrip("/")

    occupied_bridge_ports = bridge_ports_in_use(
        args.host,
        (
            ("Researcher", args.researcher_port),
            ("Participant", args.participant_port),
        ),
    )
    if occupied_bridge_ports:
        print("Prototype could not start because a previous server is still using:")
        for label, port in occupied_bridge_ports:
            print(f"  {label}: {display_origin(args.host, port)}/")
        print("\nStop the previous run with Ctrl+C, then start again.")
        print("Or choose different ports, for example:")
        print("  python run_prototype.py --researcher-port 8122 --participant-port 8123")
        return 1

    store = PrototypeStore()
    state = AppState(
        root=ROOT_DIR,
        researcher_origin=researcher_origin,
        participant_origin=participant_origin,
        camera_origin=camera_origin,
        store=store,
        login_page=PageTarget("login", RESEARCHER_LOGIN_HTML),
        register_page=PageTarget("register", RESEARCHER_REGISTER_HTML),
        edit_page=PageTarget("edit", RESEARCHER_EDIT_HTML),
        participant_page=PageTarget("participant", PARTICIPANT_HTML),
    )

    processes: list[subprocess.Popen[str]] = []
    if not args.no_backends:
        scraper = start_internal_process(
            "researcher-scraper",
            [
                python_for_backend(RESEARCHER_SCRAPER_BACKEND),
                "-c",
                f"from server import app; app.run(host='{INTERNAL_BACKEND_HOST}', port={SCRAPER_PORT}, debug=False, use_reloader=False)",
            ],
            RESEARCHER_SCRAPER_BACKEND.parent,
            INTERNAL_BACKEND_HOST,
            SCRAPER_PORT,
        )
        if scraper is not None:
            processes.append(scraper)

        if os.environ.get("CAMERA_PUBLIC_ORIGIN"):
            print("[internal] CAMERA_PUBLIC_ORIGIN is configured; using the external camera backend.")
        else:
            camera = start_internal_process(
                "camera-backend",
                [
                    python_for_backend(CAMERA_BACKEND),
                    "-c",
                    (
                        "from app import socketio, app; "
                        f"socketio.run(app, host='{INTERNAL_BACKEND_HOST}', port={args.camera_port}, allow_unsafe_werkzeug=True)"
                    ),
                ],
                CAMERA_BACKEND.parent,
                INTERNAL_BACKEND_HOST,
                args.camera_port,
                env={
                    "HOST": INTERNAL_BACKEND_HOST,
                    "PORT": str(args.camera_port),
                    "CV_BACKEND_PORT": str(args.camera_port),
                },
            )
            if camera is not None:
                processes.append(camera)

    researcher_httpd = ThreadingHTTPServer((args.host, args.researcher_port), ResearcherHandler)
    participant_httpd = ThreadingHTTPServer((args.host, args.participant_port), ParticipantHandler)
    researcher_httpd.app_state = state  # type: ignore[attr-defined]
    participant_httpd.app_state = state  # type: ignore[attr-defined]
    researcher_httpd.server_label = "researcher"  # type: ignore[attr-defined]
    participant_httpd.server_label = "participant"  # type: ignore[attr-defined]

    servers = ((researcher_httpd, "researcher-server"), (participant_httpd, "participant-server"))
    for server, thread_name in servers:
        threading.Thread(target=server.serve_forever, name=thread_name, daemon=True).start()

    def shutdown_handler(signum: int, frame: Any) -> None:
        raise KeyboardInterrupt

    previous_sigint = signal.getsignal(signal.SIGINT)
    previous_sigterm = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        print("Prototype bridge is running.")
        print("Open only these two URLs:")
        print(f"  Researcher   {researcher_origin}/")
        print(f"  Participant  {participant_origin}/")
        print("Internal services used by the bridge:")
        print(f"  Scraper API port: {SCRAPER_PORT}")
        print(f"  Camera IO port: {args.camera_port}")
        print("Database-backed researcher accounts are enabled.")
        print("Database-backed published posts are enabled.")

        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nStopping Prototype 2.0 bridge...")
    finally:
        signal.signal(signal.SIGINT, previous_sigint)
        signal.signal(signal.SIGTERM, previous_sigterm)
        researcher_httpd.shutdown()
        participant_httpd.shutdown()
        stop_processes(processes)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
