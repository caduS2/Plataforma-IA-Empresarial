from asyncio import Lock
from collections import defaultdict, deque
from time import monotonic

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import (
    assistente,
    auth,
    automacoes,
    convites,
    dashboard,
    documentos,
    empresas,
    health,
    mercado,
    redefinicao_senha,
    usuarios,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origem.strip() for origem in settings.CORS_ORIGINS.split(",") if origem.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_requests: dict[str, deque[float]] = defaultdict(deque)
_requests_lock = Lock()


@app.middleware("http")
async def proteger_requisicao(request: Request, call_next):
    path = request.url.path
    limit = settings.RATE_LIMIT_AI_REQUESTS if path == "/assistente/perguntar" else settings.RATE_LIMIT_AUTH_REQUESTS
    if path in {"/auth/login", "/senha/solicitar-redefinicao", "/assistente/perguntar"}:
        chave = f"{path}:{request.client.host if request.client else 'desconhecido'}"
        agora = monotonic()
        async with _requests_lock:
            fila = _requests[chave]
            while fila and fila[0] <= agora - settings.RATE_LIMIT_WINDOW_SECONDS:
                fila.popleft()
            if len(fila) >= limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Muitas solicitações. Tente novamente em breve."},
                    headers={"Retry-After": str(settings.RATE_LIMIT_WINDOW_SECONDS)},
                )
            fila.append(agora)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


app.include_router(health.router)
app.include_router(empresas.router)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(documentos.router)
app.include_router(assistente.router)
app.include_router(mercado.router)
app.include_router(convites.router)
app.include_router(redefinicao_senha.router)
app.include_router(automacoes.router)
app.include_router(dashboard.router)


@app.get("/")
def inicio() -> dict:
    return {
        "mensagem": "API do Assistente de Vendas Empresarial funcionando.",
        "porta": settings.PORT,
    }
