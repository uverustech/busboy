import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Get port from environment variable, default to 8000 if not set
PORT = int(os.getenv("PORT", 8000))

async def homepage(request):
    return JSONResponse({"message": "Hello, Starlette!"})

app = Starlette(routes=[
    Route("/", homepage)
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
