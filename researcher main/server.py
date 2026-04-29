import os
import re
import socket
from urllib.parse import urlparse
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
        
        # 规范化返回
        return jsonify({
            "success": True,
            "title": title.strip() if title else "No Title Found",
            "image": image.strip() if image else ""
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Request timed out (8s limit)"}), 408
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("SCRAPER_PORT", "5001"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(host=host, port=port, debug=debug)

