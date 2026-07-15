"""Routes SEO : sitemap.xml, robots.txt"""

from fastapi import APIRouter, Request
from fastapi.responses import Response
from datetime import datetime

router = APIRouter()


@router.get("/sitemap.xml")
async def sitemap(request: Request):
    """Sitemap dynamique."""
    base_url = str(request.base_url).rstrip("/")
    
    urls = [
        {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "/projets", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/services", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/blog", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/contact", "priority": "0.7", "changefreq": "monthly"},
    ]
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{url["loc"]}</loc>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return Response(content=xml, media_type="application/xml")


@router.get("/robots.txt")
async def robots():
    """Robots.txt."""
    content = """User-agent: *
Allow: /
Sitemap: https://bridge-portfolio.onrender.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")