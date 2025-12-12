from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
import os
import json

from token_manager import TokenManager

# Configuration
CISCO_BASE_URL = "https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini"
CISCO_CLIENT_ID = os.getenv("CISCO_CLIENT_ID", "")
CISCO_CLIENT_SECRET = os.getenv("CISCO_CLIENT_SECRET", "")
CISCO_APP_KEY = os.getenv("CISCO_APP_KEY", "")

def init_token_manager():

    token_manager = None

    if not all([CISCO_CLIENT_ID, CISCO_CLIENT_SECRET, CISCO_APP_KEY]):
        logging.getLogger().error(
           "ERROR: Missing Cisco credentials. Please set CISCO_CLIENT_ID, CISCO_CLIENT_SECRET, and CISCO_APP_KEY environment variables."
        )
    else:
        token_manager = TokenManager(
            CISCO_CLIENT_ID, CISCO_CLIENT_SECRET, CISCO_APP_KEY
        )
        return token_manager

cisco_token_manager = init_token_manager()

app = FastAPI(title="OpenAI-Compatible Proxy to Cisco Endpoint")

def get_cisco_headers() -> dict:
    cisco_access_token = cisco_token_manager.get_token()
    return {
        "api-key": cisco_access_token,
        "Content-Type": "application/json",
    }


def inject_model_kwargs_and_user(payload: dict) -> dict:
    """
    Ensure both:
    - top-level `user` field (required by upstream schema),
    - `model_kwargs.user` field, as requested.
    """
    # Top-level user: a JSON string with appkey.
    payload.setdefault(
        "user",
        json.dumps({"appkey": CISCO_APP_KEY})
    )

    # model_kwargs.user: same JSON string.
    model_kwargs = payload.get("model_kwargs", {})
    model_kwargs["user"] = json.dumps({"appkey": CISCO_APP_KEY})
    payload["model_kwargs"] = model_kwargs

    return payload


async def forward_request(
    request: Request,
    upstream_path: str,
    stream: bool = False,
) -> Response:
    body = await request.body()
    try:
        payload = json.loads(body.decode("utf-8")) if body else {}
    except json.JSONDecodeError:
        payload = {}

    payload = inject_model_kwargs_and_user(payload)

    method = request.method.upper()
    target_url = f"{CISCO_BASE_URL}{upstream_path}"
    upstream_headers = get_cisco_headers()

    async with httpx.AsyncClient(timeout=60.0) as client:
        if stream:
            async with client.stream(
                method,
                target_url,
                headers=upstream_headers,
                json=payload if payload else None,
            ) as upstream_response:
                content_type = upstream_response.headers.get(
                    "content-type", "application/json"
                )

                async def iter_content():
                    async for chunk in upstream_response.aiter_bytes():
                        yield chunk

                return StreamingResponse(
                    iter_content(),
                    status_code=upstream_response.status_code,
                    media_type=content_type,
                )
        else:
            upstream_response = await client.request(
                method,
                target_url,
                headers=upstream_headers,
                json=payload if payload else None,
            )

    content_type = upstream_response.headers.get(
        "content-type", "application/json"
    )

    if "application/json" in content_type.lower():
        try:
            data = upstream_response.json()
            return JSONResponse(
                content=data,
                status_code=upstream_response.status_code,
            )
        except json.JSONDecodeError:
            return Response(
                content=upstream_response.content,
                status_code=upstream_response.status_code,
                media_type=content_type,
            )
    else:
        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            media_type=content_type,
        )


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    upstream_path = "/chat/completions"
    return await forward_request(request, upstream_path, stream=False)


@app.post("/v1/chat/completions/stream")
async def chat_completions_stream(request: Request):
    upstream_path = "/chat/completions"
    return await forward_request(request, upstream_path, stream=True)