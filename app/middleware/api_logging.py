import time
import json
import structlog

from django.utils.deprecation import MiddlewareMixin

logger = structlog.get_logger("api")

SAFE_METHODS = {"POST", "PUT", "PATCH"}
MAX_BODY_SIZE = 10_000

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        try:
            duration_ms = round(
                (time.monotonic() - request._start_time) * 1000, 2
            )

            log_data = {
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }

            # user context
            if hasattr(request, "user") and request.user.is_authenticated:
                log_data["user_id"] = request.user.id

            # request body (safe methods only)
            if request.method in SAFE_METHODS:
                body = request.body[:MAX_BODY_SIZE]
                if body:
                    try:
                        log_data["request_body"] = json.loads(body)
                    except Exception:
                        log_data["request_body"] = body.decode("utf-8", errors="ignore")

            # response body (JSON + small only)
            content_type = response.get("Content-Type", "")
            if (
                "application/json" in content_type
                and hasattr(response, "content")
                and len(response.content) <= MAX_BODY_SIZE
            ):
                try:
                    log_data["response_body"] = json.loads(response.content)
                except Exception:
                    pass

            logger.info("api_request", **log_data)

        except Exception:
            logger.exception("api_logging_failed")

        return response