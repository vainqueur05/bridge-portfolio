"""
Bridge Afrika Portfolio - Application FastAPI
Version 4.0 "The Arcade"
Auteur : Vainqueur Kalema
Date : Juillet 2026

Lancement auto du seed si la DB est vide.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# -------- env ----------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# -------- routes ----------
from app.interfaces.api.v1.routes import (
    health, projets, articles, temoignages, services, messages,
    auth, bridgescan, agent, liens_sociaux, technologies, upload,
    config_admin, config_public,
)
from app.interfaces.web.routes import web_router
from app.infrastructure.database.session import engine, Base
from app.infrastructure.database.models import Projet
from app.interfaces.api.v1.routes import seo
from app.interfaces.api.v1.routes import seed_trigger

# -------- logging ----------
logging.basicConfig(
    level=logging.INFO if not os.getenv("RENDER") else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ===================== LIFESPAN =====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Démarrage de Bridge Afrika Portfolio v4.0")
    logger.info(
        f"Environnement : {'RENDER (Production)' if os.getenv('RENDER') else 'Local (Développement)'}"
    )

    # ---------- Création des tables (dev) ----------
    if not os.getenv("RENDER"):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("📦 Tables créées/vérifiées (mode développement)")
        except Exception as e:
            logger.error(f"❌ Erreur création tables : {e}")
            raise

    # ---------- Vérification connexion DB ----------
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Base de données connectée avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur connexion DB : {e}")
        if os.getenv("RENDER"):
            raise

    # ---------- Seed automatique ----------
    try:
        from sqlalchemy import select, func
        async with engine.begin() as conn:
            result = await conn.execute(select(func.count()).select_from(Projet))
            count = result.scalar()
        if count == 0:
            logger.info("🌱 DB vide → lancement du seed automatique…")
            from app.infrastructure.database.seed import seed_database
            await seed_database()
        else:
            logger.info(f"📊 DB déjà peuplée ({count} projets) → seed ignoré")
    except Exception as e:
        logger.warning(f"⚠️ Impossible de vérifier/seed la DB : {e}")

    yield

    # ---------- SHUTDOWN ----------
    logger.info("🛑 Arrêt de l'application")
    await engine.dispose()
    logger.info("🔌 Connexions fermées")


# ===================== APP =====================
app = FastAPI(
    title="Bridge Afrika Portfolio API",
    description="API du portfolio arcade de Vainqueur Kalema",
    version="4.0.0",
    docs_url="/docs" if not os.getenv("RENDER") else None,
    redoc_url="/redoc" if not os.getenv("RENDER") else None,
    lifespan=lifespan,
)

# ===================== MIDDLEWARES =====================

# 1. GZip Compression - rend le site plus rapide
app.add_middleware(GZipMiddleware, minimum_size=500)

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://vainqueurkalema.com",
        "https://www.vainqueurkalema.com",
        os.getenv("RENDER_EXTERNAL_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    max_age=3600,
)

# 3. Session Middleware
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    request.state.user = None
    request.state.is_authenticated = False

    session_cookie = request.cookies.get("bridge_session")
    if session_cookie:
        try:
            from app.interfaces.api.v1.dependencies import decode_token
            payload = decode_token(session_cookie)
            request.state.user = payload
            request.state.is_authenticated = True
        except Exception:
            request.state.user = None
            request.state.is_authenticated = False

    response = await call_next(request)

    if request.url.path.startswith("/admin") or request.url.path.startswith("/api/v1/admin"):
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        user_info = request.state.user
        username = (user_info or {}).get("sub", "Anonymous") if isinstance(user_info, dict) else "Anonymous"
        logger.info(
            f"ADMIN | {request.method} {request.url.path} | "
            f"User: {username} | Status: {response.status_code} | {elapsed:.3f}s"
        )

    return response


# 4. Security Headers Middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    # Cache navigateur pour les fichiers statiques
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response


# ===================== STATIC =====================
static_dir = Path(__file__).resolve().parent / "interfaces" / "web" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ===================== ROUTERS =====================
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(config_public.router, prefix="/api/v1", tags=["Config Public"])
app.include_router(projets.router, prefix="/api/v1", tags=["Projets"])
app.include_router(articles.router, prefix="/api/v1", tags=["Articles"])
app.include_router(temoignages.router, prefix="/api/v1", tags=["Témoignages"])
app.include_router(services.router, prefix="/api/v1", tags=["Services"])
app.include_router(messages.router, prefix="/api/v1", tags=["Messages"])
app.include_router(liens_sociaux.router, prefix="/api/v1", tags=["Liens Sociaux"])
app.include_router(technologies.router, prefix="/api/v1", tags=["Technologies"])
app.include_router(bridgescan.router, prefix="/api/v1", tags=["BridgeScan"])
app.include_router(agent.router, prefix="/api/v1", tags=["Agent IA"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(config_admin.router, prefix="/api/v1", tags=["Config Admin"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(web_router, tags=["Web"])
app.include_router(seo.router, tags=["SEO"])
app.include_router(seed_trigger.router, prefix="/api/v1", tags=["Seed"])

# ===================== ERROR HANDLERS =====================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "Ressource non trouvée", "path": request.url.path})
    try:
        templates_dir = Path(__file__).resolve().parent / "interfaces" / "web" / "templates"
        templates = Jinja2Templates(directory=str(templates_dir))
        return templates.TemplateResponse("public/404.html", {"request": request}, status_code=404)
    except Exception:
        return HTMLResponse(content="<h1>404 - Page non trouvée</h1><p><a href='/'>Retour à l'accueil</a></p>", status_code=404)


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Erreur 500 sur {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Erreur interne du serveur."})


# ===================== MAIN =====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=not os.getenv("RENDER"),
        log_level="info",
    )