import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import json

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", 8000))

async def echo_handler(request: Request):
    # Parse URL components
    raw_path = request.url.path
    query_string = str(request.url.query)
    query_params = request.query_params

    # Simplify query params: unwrap single-item lists
    simplified_query = {
        k: v if len(v) > 1 else v[0] if v else ""
        for k, v in query_params.lists()
    }

    # Read body
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8", errors="replace") if body_bytes else ""
    body_length = len(body_bytes)

    # Try to parse JSON body
    body_json = None
    if body_bytes:
        try:
            body_json = json.loads(body_bytes)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass  # Not valid JSON

    # Build response data
    response_data = {
        "method": request.method,
        "path": str(request.url),
        "raw_path": raw_path,
        "query_string": query_string,
        "query_params": simplified_query,
        "headers": dict(request.headers),
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

# Create app with CORS middleware
app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single route to catch all paths and methods
app.add_route("/{full_path:path}", echo_handler, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])

if __name__ == "__main__":
    print(f"Echo server running on http://localhost:{PORT}")
    print("Send any request - it will respond with full details as JSON")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
