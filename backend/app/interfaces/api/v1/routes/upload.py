"""Routes d'upload de fichiers."""

import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.interfaces.api.v1.dependencies import get_current_admin

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "interfaces" / "web" / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/svg+xml", "image/gif", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/admin/upload")
async def upload_file(
    file: UploadFile = File(...),
    dossier: str = "general",
    _admin = Depends(get_current_admin),
):
    """Upload un fichier (admin uniquement)."""
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Type non autorisé. Types: {', '.join(ALLOWED_TYPES)}")
    
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, f"Fichier trop volumineux. Max {MAX_SIZE // 1024 // 1024}MB")
    
    ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else 'jpg'
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    dossier_path = UPLOAD_DIR / dossier
    dossier_path.mkdir(parents=True, exist_ok=True)
    
    filepath = dossier_path / filename
    with open(filepath, "wb") as f:
        f.write(content)
    
    url = f"/static/uploads/{dossier}/{filename}"
    
    return {
        "success": True,
        "url": url,
        "filename": filename,
        "size": len(content),
        "type": file.content_type,
    }