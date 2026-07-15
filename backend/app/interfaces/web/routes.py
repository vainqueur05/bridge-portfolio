"""
Routes web pour les templates Jinja2.
Pages publiques et interface d'administration.
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.interfaces.api.v1.dependencies import get_current_user, get_current_admin
from app.infrastructure.database.models import User

# Configuration des templates
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

web_router = APIRouter()


# ============================================
# PAGES PUBLIQUES
# ============================================

@web_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil du portfolio avec toutes les sections."""
    return templates.TemplateResponse(
        "public/accueil.html",
        {"request": request, "title": "Bridge Afrika | Portfolio Arcade"}
    )


@web_router.get("/projets", response_class=HTMLResponse)
async def projets_page(request: Request):
    """Page liste des projets."""
    return templates.TemplateResponse(
        "public/base.html",
        {"request": request, "title": "Projets | Bridge Afrika"}
    )


@web_router.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    """Page blog."""
    return templates.TemplateResponse(
        "public/base.html",
        {"request": request, "title": "Blog | Bridge Afrika"}
    )
           
@web_router.get("/admin/liens-sociaux", response_class=HTMLResponse)
async def admin_liens_sociaux(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/liens_sociaux.html", {"request": request, "user": user, "active_page": "liens_sociaux"})

@web_router.get("/admin/articles/new", response_class=HTMLResponse)
async def admin_article_new(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/article_form.html", {"request": request, "user": user, "article_id": None, "is_new": True})

@web_router.get("/admin/articles/{id}/edit", response_class=HTMLResponse)
async def admin_article_edit(id: int, request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/article_form.html", {"request": request, "user": user, "article_id": id, "is_new": False})

# ============================================
# PAGE LOGIN (DOIT ÊTRE AVANT LES ROUTES PROTÉGÉES)
# ============================================

@web_router.get("/admin/technologies", response_class=HTMLResponse)
async def admin_technologies(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/technologies.html", {"request": request, "user": user, "active_page": "technologies"})

@web_router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Page de connexion admin."""
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


# ============================================
# PAGES ADMIN (PROTÉGÉES)
# ============================================

@web_router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: User = Depends(get_current_admin)):
    """Dashboard administrateur."""
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "user": user, "active_page": "dashboard"}
    )


@web_router.get("/admin/projets", response_class=HTMLResponse)
async def admin_projets(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des projets."""
    return templates.TemplateResponse(
        "admin/projets.html",
        {"request": request, "user": user, "active_page": "projets"}
    )


@web_router.get("/admin/projets/new", response_class=HTMLResponse)
async def admin_projet_new(request: Request, user: User = Depends(get_current_admin)):
    """Créer un nouveau projet."""
    return templates.TemplateResponse(
        "admin/projet_form.html",
        {"request": request, "user": user, "projet": None, "is_new": True}
    )


@web_router.get("/admin/projets/{id}/edit", response_class=HTMLResponse)
async def admin_projet_edit(id: int, request: Request, user: User = Depends(get_current_admin)):
    """Éditer un projet existant."""
    return templates.TemplateResponse(
        "admin/projet_form.html",
        {"request": request, "user": user, "projet_id": id, "is_new": False}
    )


@web_router.get("/admin/articles", response_class=HTMLResponse)
async def admin_articles(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des articles."""
    return templates.TemplateResponse(
        "admin/articles.html",
        {"request": request, "user": user, "active_page": "articles"}
    )


@web_router.get("/admin/temoignages", response_class=HTMLResponse)
async def admin_temoignages(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des témoignages."""
    return templates.TemplateResponse(
        "admin/temoignages.html",
        {"request": request, "user": user, "active_page": "temoignages"}
    )


@web_router.get("/admin/services", response_class=HTMLResponse)
async def admin_services(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des services."""
    return templates.TemplateResponse(
        "admin/services.html",
        {"request": request, "user": user, "active_page": "services"}
    )


@web_router.get("/admin/messages", response_class=HTMLResponse)
async def admin_messages(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des messages/leads."""
    return templates.TemplateResponse(
        "admin/messages.html",
        {"request": request, "user": user, "active_page": "messages"}
    )


@web_router.get("/admin/medias", response_class=HTMLResponse)
async def admin_medias(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des médias."""
    return templates.TemplateResponse(
        "admin/medias.html",
        {"request": request, "user": user, "active_page": "medias"}
    )


@web_router.get("/admin/parametres", response_class=HTMLResponse)
async def admin_parametres(request: Request, user: User = Depends(get_current_admin)):
    """Paramètres généraux."""
    return templates.TemplateResponse(
        "admin/parametres.html",
        {"request": request, "user": user, "active_page": "parametres"}
    )


@web_router.get("/admin/utilisateurs", response_class=HTMLResponse)
async def admin_utilisateurs(request: Request, user: User = Depends(get_current_admin)):
    """Gestion des utilisateurs."""
    return templates.TemplateResponse(
        "admin/utilisateurs.html",
        {"request": request, "user": user, "active_page": "utilisateurs"}
    )

@web_router.get("/projet/{slug}", response_class=HTMLResponse)
async def projet_detail(slug: str, request: Request):
    return templates.TemplateResponse("public/projet_detail.html", {"request": request})

@web_router.get("/projets", response_class=HTMLResponse)
async def projets_list(request: Request):
    return templates.TemplateResponse("public/projets.html", {"request": request})

@web_router.get("/services", response_class=HTMLResponse)
async def services_list(request: Request):
    return templates.TemplateResponse("public/services.html", {"request": request})

@web_router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse("public/contact.html", {"request": request})

@web_router.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request):
    return templates.TemplateResponse("public/blog.html", {"request": request})

@web_router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_detail(slug: str, request: Request):
    return templates.TemplateResponse("public/article_detail.html", {"request": request})
