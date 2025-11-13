import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import json
from urllib.parse import parse_qs, urlparse

load_dotenv()
PORT = int(os.getenv("PORT", 8000))

async def echo_handler(request: Request):
    # --- URL & Query Parsing (like stdlib) ---
    full_url = str(request.url)
    parsed_url = urlparse(full_url)
    raw_path = parsed_url.path
    query_string = parsed_url.query

    # Parse query string with full list support
    query_params_raw = parse_qs(query_string, keep_blank_values=True)
    query_params = {
        k: v if len(v) > 1 else v[0] for k, v in query_params_raw.items()
    }

    # --- Headers ---
    headers = dict(request.headers)

    # --- Body ---
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8", errors="replace") if body_bytes else ""
    body_length = len(body_bytes)

    body_json = None
    if body_bytes:
        try:
            body_json = json.loads(body_bytes)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # --- Response Data ---
    response_data = {
        "method": request.method,
        "path": full_url,
        "raw_path": raw_path,
        "query_string": query_string,
        "query_params": query_params,
        "headers": headers,
        "body_raw": body_str,
        "body_bytes_length": body_length,
    }
    if body_json is not None:
        response_data["body_json"] = body_json

    return JSONResponse(
        response_data,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# App setup
app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Catch-all route
app.add_route("/{full_path:path}", echo_handler, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])

if __name__ == "__main__":
    print(f"Echo server running on http://localhost:{PORT}")
    print("Send any request - it will respond with full details as JSON")
    uvicorn.run(app, host="0.0.0.0", port=PORT)