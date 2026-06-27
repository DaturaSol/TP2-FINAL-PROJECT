# ./src/back_end/src/engine/routes/__init__.py
"""We save routes here.

Routes are actions that can occur given a http method
given on a certain route, we save those in a list to
register those in the app.
"""

from ._handle_login import handle_login_bp
from ._handle_payload import handle_webhook_payload_bp

routers = [
    handle_webhook_payload_bp,
    handle_login_bp,
]
