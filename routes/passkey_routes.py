import requests
from flask import Blueprint, request, Response
from config import BACKEND_URL

passkey_bp = Blueprint("passkey", __name__, url_prefix="/passkey")

# Forward Requests to backend
def forward_request(path):
    """
    Forward an iOS request from tichuFrontServer to tichuServer.

    The iOS client never needs to know the backend server URL.
    """

    url = f"{BACKEND_URL}{path}"

    headers = {}

    authorization = request.headers.get("Authorization")
    if authorization:
        headers["Authorization"] = authorization

    content_type = request.headers.get("Content-Type")
    if content_type:
        headers["Content-Type"] = content_type

    # Forward JSON body when present.
    json_data = None

    if request.is_json:
        json_data = request.get_json(silent=True)

    try:
        backend_response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            json=json_data,
            params=request.args,
            timeout=15,
        )

    except requests.RequestException as exc:
        return Response(
            '{"error":"backend_unavailable"}',
            status=502,
            content_type="application/json",
        )

    # Return backend's response directly 
    response = Response(
        backend_response.content,
        status=backend_response.status_code,
    )

    # Preserve backend content type.
    content_type = backend_response.headers.get("Content-Type")

    if content_type:
        response.headers["Content-Type"] = content_type
    else:
        response.headers["Content-Type"] = "application/json"

    return response

@passkey_bp.post("/register/options")
def passkey_register_options():
    return forward_request("/passkey/register/options")

@passkey_bp.post("/register/verify")
def passkey_register_verify():
    return forward_request("/passkey/register/verify")

@passkey_bp.post("/add/options")
def passkey_add_options():
    return forward_request("/passkey/add/options")

@passkey_bp.post("/add/verify")
def passkey_add_verify():
    return forward_request("/passkey/add/verify")

@passkey_bp.post("/login/options")
def passkey_login_options():
    return forward_request("/passkey/login/options")

@passkey_bp.post("/login/verify")
def passkey_login_verify():
    return forward_request("/passkey/login/verify")

@passkey_bp.get("/credentials")
def passkey_credentials():
    return forward_request("/passkey/credentials")

@passkey_bp.delete("/credentials/<int:credential_id>")
def passkey_delete_credential(credential_id):
    return forward_request(f"/passkey/credentials/{credential_id}")

@passkey_bp.patch("/connect_email")
def passkey_connect_email():
    return forward_request("/passkey/connect_email")