"""
定时探活脚本：读取 data/services.json，逐个请求，写出 data/status.json
状态判定：
  green  - 200 且 3 秒内响应
  yellow - 200 但 3~8 秒响应（慢/拥挤）
  red    - 超时 / 非 200 / 请求异常
可用 Windows 计划任务或 GitHub Actions 定时执行： python monitor.py
"""
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
SERVICES_FILE = BASE_DIR / "data" / "services.json"
STATUS_FILE = BASE_DIR / "data" / "status.json"

TIMEOUT_RED = 8
TIMEOUT_YELLOW = 3
# 部分站点对脚本请求做反爬拦截（403/401），这不代表真的打不开，
# 只是无法用简单请求判断，归为 yellow（不确定）而非 red，避免误判。
BOT_BLOCKED_CODES = {401, 403, 429}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def check_one(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_RED) as resp:
            elapsed = time.monotonic() - start
            if elapsed <= TIMEOUT_YELLOW:
                return {"status": "green", "latency": round(elapsed, 2), "code": resp.status}
            return {"status": "yellow", "latency": round(elapsed, 2), "code": resp.status}
    except urllib.error.HTTPError as e:
        elapsed = time.monotonic() - start
        if e.code in BOT_BLOCKED_CODES:
            return {"status": "yellow", "latency": round(elapsed, 2), "code": e.code, "note": "可能是反爬拦截，非真实故障"}
        return {"status": "red", "latency": round(elapsed, 2), "code": e.code}
    except Exception as e:
        elapsed = time.monotonic() - start
        return {"status": "red", "latency": round(elapsed, 2), "error": str(e)}


def main():
    services = json.loads(SERVICES_FILE.read_text(encoding="utf-8"))
    result = {}
    for svc in services:
        result[svc["id"]] = check_one(svc["url"])
        print(f"{svc['id']}: {result[svc['id']]}")

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "services": result,
    }
    STATUS_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
