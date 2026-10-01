"""
M1 Espía — Operaciones de base de datos (Supabase)
"""
import logging
from datetime import datetime
from supabase_client import get_supabase

logger = logging.getLogger(__name__)


# ── BÚSQUEDAS ────────────────────────────────────────────────

def save_search(country: str, keywords: str = None, advertiser: str = None,
                filters: dict = None, result_count: int = 0) -> str | None:
    """Guarda una búsqueda y retorna su UUID."""
    try:
        sb = get_supabase()
        result = sb.table("m1_searches").insert({
            "country": country,
            "keywords": keywords,
            "advertiser": advertiser,
            "filters": filters or {},
            "result_count": result_count
        }).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        logger.error(f"Error guardando búsqueda M1: {e}")
        return None


def get_recent_searches(limit: int = 10) -> list:
    """Retorna las últimas búsquedas guardadas."""
    try:
        sb = get_supabase()
        result = sb.table("m1_searches") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Error obteniendo búsquedas M1: {e}")
        return []


# ── ANUNCIOS ─────────────────────────────────────────────────

def save_ads(search_id: str, ads: list) -> int:
    """
    Guarda lista de anuncios de Meta Ads Library.
    Ignora duplicados (ad_id único).
    Retorna cantidad insertada.
    """
    if not ads:
        return 0
    try:
        sb = get_supabase()
        rows = []
        for ad in ads:
            rows.append({
                "search_id": search_id,
                "ad_id": ad.get("id") or ad.get("ad_id"),
                "advertiser": ad.get("page_name") or ad.get("advertiser"),
                "advertiser_url": ad.get("advertiser_url"),
                "copy": _extract_copy(ad),
                "days_active": ad.get("days_active", 0),
                "start_date": ad.get("ad_creation_date"),
                "platform": ad.get("publisher_platforms", []),
                "media_type": _extract_media_type(ad),
                "media_url": _extract_media_url(ad),
                "thumbnail_url": _extract_thumbnail(ad),
                "cta": _extract_cta(ad),
                "landing_url": ad.get("link_url") or _extract_landing(ad),
                "raw_data": ad
            })
        result = sb.table("m1_ads").upsert(rows, on_conflict="ad_id").execute()
        return len(result.data or [])
    except Exception as e:
        logger.error(f"Error guardando anuncios M1: {e}")
        return 0


def get_ads_by_search(search_id: str) -> list:
    """Retorna todos los anuncios de una búsqueda."""
    try:
        sb = get_supabase()
        result = sb.table("m1_ads") \
            .select("*, m1_analysis(*)") \
            .eq("search_id", search_id) \
            .order("days_active", desc=True) \
            .execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Error obteniendo anuncios M1: {e}")
        return []


# ── ANÁLISIS IA ──────────────────────────────────────────────

def save_analysis(ad_id: str, analysis: dict) -> str | None:
    """Guarda el análisis IA de un anuncio. Retorna UUID."""
    try:
        sb = get_supabase()
        result = sb.table("m1_analysis").upsert({
            "ad_id": ad_id,
            "viability_label": analysis.get("viability_label"),
            "estimated_budget": analysis.get("estimated_budget"),
            "offer_type": analysis.get("offer_type"),
            "detected_price": analysis.get("detected_price"),
            "target_market": analysis.get("target_market"),
            "success_signals": analysis.get("success_signals", []),
            "score": analysis.get("score", 0),
            "score_breakdown": analysis.get("score_breakdown", {}),
            "ai_recommendation": analysis.get("ai_recommendation"),
        }, on_conflict="ad_id").execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        logger.error(f"Error guardando análisis M1: {e}")
        return None


def get_analysis(ad_id: str) -> dict | None:
    """Retorna el análisis de un anuncio si existe."""
    try:
        sb = get_supabase()
        result = sb.table("m1_analysis") \
            .select("*") \
            .eq("ad_id", ad_id) \
            .limit(1) \
            .execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error obteniendo análisis M1: {e}")
        return None


# ── OFERTAS SELECCIONADAS ────────────────────────────────────

def save_selected_offer(offer_data: dict) -> str | None:
    """Guarda la oferta seleccionada para pasar a M2. Retorna UUID."""
    try:
        sb = get_supabase()
        result = sb.table("m1_selected_offers").insert(offer_data).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        logger.error(f"Error guardando oferta seleccionada M1: {e}")
        return None


def get_latest_selected_offer() -> dict | None:
    """Retorna la última oferta seleccionada."""
    try:
        sb = get_supabase()
        result = sb.table("m1_selected_offers") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error obteniendo oferta seleccionada M1: {e}")
        return None


def mark_offer_sent_to_m2(offer_id: str, notion_page_id: str = None):
    """Marca una oferta como enviada a M2."""
    try:
        sb = get_supabase()
        sb.table("m1_selected_offers").update({
            "sent_to_m2": True,
            "notion_page_id": notion_page_id
        }).eq("id", offer_id).execute()
    except Exception as e:
        logger.error(f"Error marcando oferta M1 como enviada: {e}")


# ── HELPERS PRIVADOS ─────────────────────────────────────────

def _extract_copy(ad: dict) -> str:
    bodies = ad.get("ad_creative_bodies") or []
    if isinstance(bodies, list) and bodies:
        return bodies[0]
    return ad.get("copy", "")


def _extract_media_type(ad: dict) -> str:
    media = ad.get("ad_creative_media") or []
    if isinstance(media, list) and media:
        return media[0].get("type", "")
    return ""


def _extract_media_url(ad: dict) -> str:
    media = ad.get("ad_creative_media") or []
    if isinstance(media, list) and media:
        return media[0].get("url", "")
    return ""


def _extract_thumbnail(ad: dict) -> str:
    media = ad.get("ad_creative_media") or []
    if isinstance(media, list) and media:
        return media[0].get("thumbnail", "")
    return ""


def _extract_cta(ad: dict) -> str:
    cta = ad.get("ad_creative_link_captions") or []
    if isinstance(cta, list) and cta:
        return cta[0]
    return ""


def _extract_landing(ad: dict) -> str:
    urls = ad.get("ad_snapshot_url", "")
    return urls
