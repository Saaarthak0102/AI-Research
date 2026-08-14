Add a module logger and use blueprint-level `before_app_request` / `after_app_request` hooks so the logging covers every request handled by the Flask application, including requests outside the blueprint.

```python
import logging

from flask import Blueprint, request, jsonify, session, abort
from functools import wraps
from app.auth import get_current_user_id
from app.models import get_user_by_id

bp = Blueprint('views', __name__)

logger = logging.getLogger(__name__)


@bp.before_app_request
def log_request_start():
    """Log the HTTP method and path for every request."""
    logger.info("request %s %s", request.method, request.path)


@bp.after_app_request
def log_request_end(response):
    """Log the HTTP method, path, and response status for every request."""
    logger.info(
        "response %s %s %s",
        request.method,
        request.path,
        response.status_code,
    )
    return response


# Basic rate limiting stub
def rate_limit(limit=10):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    return decorator


# Basic CSRF protection stub
def csrf_protect(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.method == "POST":
            token = request.headers.get("X-CSRF-Token")
            if not token or token != session.get('csrf_token'):
                abort(403)
        return f(*args, **kwargs)
    return wrapped


@bp.route('/profile', methods=['GET'])
def profile():
    """
    User profile route with avatar image loading stub.
    """
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = get_current_user_id(auth_token)
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user['username'],
        "role": user['role'],
        "avatar_url": f"/static/avatars/{user['id']}.png"
    })


@bp.route('/api/upload', methods=['POST'])
@rate_limit(limit=5)
@csrf_protect
def upload():
    """
    File upload endpoint with size validation, CSRF protection, and rate limiting.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Size validation
    file.seek(0, 2)
    size = file.tell()
    if size > 10 * 1024 * 1024:  # 10 MB limit
        return jsonify({"error": "File too large"}), 413

    return jsonify({"message": "File uploaded successfully"})
```

This keeps the existing route behavior unchanged and produces log entries containing exactly the method, path, and resulting HTTP status.
