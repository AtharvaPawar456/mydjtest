import logging

from django.http import HttpResponse
from django.utils import timezone
from xml.sax.saxutils import escape

from .models import Businesswebinfo, InternDetails, YTvideos, AccessoriesProd, AicontentProd
from .product_catalog import ALL_PRODUCT_MODELS, count_products

logger = logging.getLogger(__name__)

SITE_FALLBACK = "https://www.handmadeprojects.in"


def _abs(request, path: str) -> str:
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return request.build_absolute_uri(path)


def _first_real_image_url(value):
    """
    Returns the first http(s) image URL found in a `;`/newline-separated media
    field, or None if the field is empty, the "*" placeholder, or a base64
    data URI (which can't be represented in an image sitemap).
    """
    if not value:
        return None
    text = value.strip()
    if not text or text == "*":
        return None
    first = text.replace("\r", "\n").split("\n")[0].split(";")[0].strip()
    if first.startswith("http://") or first.startswith("https://"):
        return first
    return None


def _warn_if_truncated(label, total, cap):
    if total > cap:
        logger.warning(
            "Sitemap: %s has %d rows, exceeding the %d-row cap — %d row(s) are silently excluded from sitemap.xml",
            label, total, cap, total - cap,
        )


def robots_txt(request):
    host = request.get_host()
    scheme = "https" if request.is_secure() or "handmadeprojects" in host else request.scheme
    # Prefer production sitemap when on local/dev host name is generic
    if host in ("127.0.0.1:8000", "localhost:8000") or host.startswith("127.0.0.1") or host.startswith("localhost"):
        sitemap = f"{SITE_FALLBACK}/sitemap.xml"
    else:
        sitemap = f"{scheme}://{host}/sitemap.xml"
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /hpmadmin/\n"
        "Disallow: /logout/\n"
        "Disallow: /addproduct/\n"
        "Disallow: /add-developer/\n"
        "Disallow: /add-intern/\n"
        "Disallow: /edit-product/\n"
        "Disallow: /edit-developer/\n"
        "Disallow: /edit_hero_images/\n"
        "Disallow: /analysis/\n"
        f"Sitemap: {sitemap}\n"
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """Dynamic XML sitemap for core pages + products + visible shops."""
    now = timezone.now().date().isoformat()
    urls = []

    def add(path, priority="0.5", changefreq="weekly", lastmod=None, images=None):
        loc = _abs(request, path)
        urls.append(
            {
                "loc": loc,
                "priority": priority,
                "changefreq": changefreq,
                "lastmod": lastmod or now,
                "images": [_abs(request, img) for img in (images or [])],
            }
        )

    # Core public pages
    static_paths = [
        ("/", "1.0", "daily"),
        ("/aboutus/", "0.8", "monthly"),
        ("/contactus/", "0.7", "monthly"),
        ("/ourteam/", "0.7", "weekly"),
        ("/internship/", "0.9", "weekly"),
        ("/internship/opportunities/", "0.9", "weekly"),
        ("/kids-projects/", "0.8", "weekly"),
        ("/engineering-projects/", "0.9", "weekly"),
        ("/youtube-projects/", "0.7", "weekly"),
        ("/productlist/", "0.9", "daily"),
        ("/productlist/?productcat=software", "0.8", "weekly"),
        ("/productlist/?productcat=hardware", "0.8", "weekly"),
        ("/productlist/?productcat=mechanical", "0.7", "weekly"),
        ("/productlist/?productcat=simulation", "0.7", "weekly"),
        ("/productlist/?productcat=science", "0.7", "weekly"),
        ("/productlist/?productcat=craft", "0.7", "weekly"),
        ("/accessories/", "0.6", "weekly"),
        ("/aicontent/", "0.7", "weekly"),
        ("/gallery/", "0.6", "weekly"),
        ("/allshops/", "0.8", "weekly"),
        ("/affiliateinfo/", "0.5", "monthly"),
        ("/dashboard/", "0.6", "weekly"),
    ]
    for path, pri, freq in static_paths:
        add(path, pri, freq)

    PRODUCT_CAP = 2000
    total_products = count_products()
    _warn_if_truncated("Products (all categories)", total_products, PRODUCT_CAP)
    product_rows = []
    for Model in ALL_PRODUCT_MODELS:
        for p in Model.objects.only("prodid", "timestamp", "mainimgbasetxt").order_by("-timestamp")[
            :PRODUCT_CAP
        ]:
            product_rows.append(p)
    product_rows.sort(key=lambda x: x.timestamp, reverse=True)
    for p in product_rows[:PRODUCT_CAP]:
        last = p.timestamp.date().isoformat() if getattr(p, "timestamp", None) else now
        image = _first_real_image_url(p.mainimgbasetxt)
        add(
            f"/productinfo/{p.category_slug}/{p.prodid}/",
            "0.8",
            "weekly",
            last,
            images=[image] if image else None,
        )

    SHOP_CAP = 1000
    _warn_if_truncated("Businesswebinfo (visible)", Businesswebinfo.objects.filter(is_visible=True).count(), SHOP_CAP)
    for s in Businesswebinfo.objects.filter(is_visible=True).only("bname", "btimestamp", "bmainimg").order_by("-btimestamp")[:SHOP_CAP]:
        last = s.btimestamp.date().isoformat() if getattr(s, "btimestamp", None) else now
        # URL name is path segment
        image = _first_real_image_url(s.bmainimg)
        add(f"/shop/{s.bname}/", "0.7", "weekly", last, images=[image] if image else None)

    INTERN_CAP = 1000
    _warn_if_truncated("InternDetails", InternDetails.objects.count(), INTERN_CAP)
    for i in InternDetails.objects.all().only("internid", "timestamp").order_by("-timestamp")[:INTERN_CAP]:
        last = i.timestamp.date().isoformat() if getattr(i, "timestamp", None) else now
        add(f"/internship/profile/{i.internid}/", "0.5", "monthly", last)

    VIDEO_CAP = 1000
    _warn_if_truncated("YTvideos", YTvideos.objects.count(), VIDEO_CAP)
    for v in YTvideos.objects.all().only("ytid", "timestamp").order_by("-timestamp")[:VIDEO_CAP]:
        last = v.timestamp.date().isoformat() if getattr(v, "timestamp", None) else now
        add(f"/video-player/{v.ytid}/", "0.6", "monthly", last)

    ACCESSORY_CAP = 1000
    _warn_if_truncated("AccessoriesProd", AccessoriesProd.objects.count(), ACCESSORY_CAP)
    for a in AccessoriesProd.objects.all().only("apid", "timestamp", "apimglink").order_by("-timestamp")[:ACCESSORY_CAP]:
        last = a.timestamp.date().isoformat() if getattr(a, "timestamp", None) else now
        image = _first_real_image_url(a.apimglink)
        add(f"/accessoriesview/{a.apid}/", "0.6", "weekly", last, images=[image] if image else None)

    AICONTENT_CAP = 1000
    _warn_if_truncated("AicontentProd", AicontentProd.objects.count(), AICONTENT_CAP)
    for c in AicontentProd.objects.all().only("aiid", "timestamp", "aiimglink").order_by("-timestamp")[:AICONTENT_CAP]:
        last = c.timestamp.date().isoformat() if getattr(c, "timestamp", None) else now
        image = _first_real_image_url(c.aiimglink)
        add(f"/aicontent/{c.aiid}/", "0.6", "weekly", last, images=[image] if image else None)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(u['loc'])}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        for img in u["images"]:
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{escape(img)}</image:loc>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return HttpResponse("\n".join(lines) + "\n", content_type="application/xml; charset=utf-8")
