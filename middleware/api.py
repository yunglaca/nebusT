from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        # Исключение для маршрутов документации
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Проверка API-ключа
        provided_key = request.headers.get("x-api-key")
        if provided_key != self.api_key:
            return JSONResponse({"detail": "Invalid API key"}, status_code=401)
        return await call_next(request)
