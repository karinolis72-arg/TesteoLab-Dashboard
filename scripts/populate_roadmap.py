# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
populate_roadmap.py — Crea ítems en el Roadmap Master de Notion.
Uso: python scripts/populate_roadmap.py
Requiere: NOTION_TOKEN en .env

Propiedades reales de la DB (verificadas 2026-04-12):
  title     → Name
  select    → Estado: Pendiente / En Progreso / Bloqueado / Completado
  select    → Fase: FASE 0 / FASE 1 / FASE 2
  select    → Módulo: M1 / M2 / M3 / M4 / NAUTA / SISTEMA / GENERAL
  select    → Prioridad: P0 / P1 / P2 / Alta / Crítica
  select    → BLAST Step: Blueprint / Links / Architecture / Stylize / Transfer
  select    → Esfuerzo: XS / S / M / L / XL
  rich_text → Notas (descripción del ítem)
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

ROADMAP_MASTER_DB_ID = "ed93c7e668c94d938b932b40970d55c1"
notion = Client(auth=os.environ.get("NOTION_TOKEN"))

# Mapeo de prioridad legible → valor real en Notion
PRIORIDAD_MAP = {"Alta": "Alta", "Media": "P1", "Baja": "P2", "Crítica": "P0"}
# Mapeo de fase semántica → valor real en Notion
FASE_MAP = {"v1.1": "FASE 1", "v1.2": "FASE 1", "v1.3": "FASE 1", "v2.0": "FASE 2", "v3.0": "FASE 2"}
# BLAST Step → valor real en Notion
BLAST_MAP = {
    "B - Bosquejo": "Blueprint",
    "L - Lazos": "Links",
    "A - Arquitectura": "Architecture",
    "S - Stilización": "Stylize",
    "T - Transferencia": "Transfer",
}

ITEMS = [
    # ── FASE 1 — M1 Espía ────────────────────────────────────────────────────
    {"nombre": "M1 P1: Definir búsqueda (país, keywords, filtros)",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "S",
     "notas": "Input: país/región (default AR), keywords o nombre empresa. Filtros: plataforma, días activos (default 30+), presupuesto estimado."},

    {"nombre": "M1 P2: Integración Meta Ads Library API",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "L - Lazos", "esfuerzo": "M",
     "notas": "GET /ads_library?ad_status=ACTIVE&country=AR&search_terms=... Rate limit: 50 req/min. Retorna: ad_id, advertiser, días activos, copy, media, CTA, landing URL."},

    {"nombre": "M1 P3: Motor de análisis IA (scoring 0-100, CPM)",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "L",
     "notas": "Scoring: días activos (40pts) + presupuesto CPM-based (30pts) + señales de éxito (30pts). <30d=amarillo | 30-90d=verde | 90+=verde fuerte."},

    {"nombre": "M1 P4: Vista filtrar/clasificar con comparador",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Media", "estado": "Pendiente",
     "blast": "S - Stilización", "esfuerzo": "M",
     "notas": "Smart Sort: Ganadores 80+ | Potencial Alto 61-79 | Experimental 31-60. Comparador hasta 3 anuncios lado a lado."},

    {"nombre": "M1 P5: Selección y output JSON hacia M2",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "S",
     "notas": "Output: offer_type, price_point, target_market, key_message, viability_score, estimated_investment, competitive_analysis."},

    {"nombre": "M1: Historial de búsquedas (Supabase)",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Baja", "estado": "Pendiente",
     "blast": "L - Lazos", "esfuerzo": "M",
     "notas": "Tablas: competitor_accounts, competitor_ads, ad_metrics, ad_analysis. Deduplicación automática."},

    {"nombre": "M1: Tips automáticos inteligentes en UI",
     "modulo": "M1", "fase": "v1.1", "prioridad": "Baja", "estado": "Pendiente",
     "blast": "S - Stilización", "esfuerzo": "XS",
     "notas": "Sugerencias contextuales basadas en score y datos del anuncio analizado."},

    # ── FASE 1 — M2 Crea ─────────────────────────────────────────────────────
    {"nombre": "M2: Landing HTML builder (Shopify/Hotmart-ready)",
     "modulo": "M2", "fase": "v1.2", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "L",
     "notas": "Recibe JSON de M1. Landing con urgencia + escasez + testimonios + 2 precios. Entrega en 24h. Copy persuasivo: pain → promesa → producto → testimonios → garantía → CTA."},

    {"nombre": "M2: MVP generator (guía PDF 10-20 páginas)",
     "modulo": "M2", "fase": "v1.2", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "M",
     "notas": "Estructura Gamma-style. Integración con Gamma App API. Precio target USD $7-47."},

    {"nombre": "M2: Estructura de oferta (SKU, bonus, order bumps)",
     "modulo": "M2", "fase": "v1.2", "prioridad": "Media", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "M",
     "notas": "SKU, precio USD $7-47, descripción, hasta 3 order bumps. Subida automática a Hotmart."},

    # ── FASE 1 — M3 Creativo ──────────────────────────────────────────────────
    {"nombre": "M3: Generador de 62 ángulos creativos",
     "modulo": "M3", "fase": "v1.3", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "L",
     "notas": "P1-P8 del flujo M3. Distintos hooks, dolores, públicos. 24h desde que M2 entrega. Campaign briefs completos."},

    {"nombre": "M3: Scripts de video (hook <3seg + desarrollo + CTA)",
     "modulo": "M3", "fase": "v1.3", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "M",
     "notas": "Variaciones para A/B testing. Formatos: noticiero / infografía / UGC / testimonial."},

    {"nombre": "M3: Fábrica de imágenes con prompts IA",
     "modulo": "M3", "fase": "v1.3", "prioridad": "Media", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "M",
     "notas": "Prompts para Midjourney, DALL-E, Flux. Estilos: realista / ilustrado / 3D / UGC."},

    # ── FASE 2 — M4 Analista Meta ─────────────────────────────────────────────
    {"nombre": "M4: Dashboard ROAS en tiempo real",
     "modulo": "M4", "fase": "v2.0", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "L - Lazos", "esfuerzo": "XL",
     "notas": "Integración Meta Ads Manager API. ROAS objetivo >3:1. Diagnóstico automático de embudo (landing/checkout/oferta)."},

    {"nombre": "M4: A/B testing ($2/conjunto, 10-12 anuncios)",
     "modulo": "M4", "fase": "v2.0", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "A - Arquitectura", "esfuerzo": "L",
     "notas": "Winner: 3+ días + 50+ clicks. Escalado progresivo 20-30% cada 48h. Meta final: $10k/mes USD."},

    # ── FASE 2 — NAUTA Scheduled Tasks ────────────────────────────────────────
    {"nombre": "NAUTA: Cierre Diario 21:00 ART automatizado",
     "modulo": "NAUTA", "fase": "v3.0", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "T - Transferencia", "esfuerzo": "M",
     "notas": "Lee Rueda de Vida, calcula scores 8 áreas, genera reflexión del día, registra en Notion Logs (NAUTA_LOGS_DB_ID)."},

    {"nombre": "NAUTA: Planificación Semanal DOM 19:00 ART",
     "modulo": "NAUTA", "fase": "v3.0", "prioridad": "Alta", "estado": "Pendiente",
     "blast": "T - Transferencia", "esfuerzo": "L",
     "notas": "Ingesta FrameworkIA (3 Excel), analiza semana, genera 3-5 objetivos, crea 7 ofertas para testear, crea eventos GCal, actualiza dashboard."},

    {"nombre": "Business OS: Context Engineering (FrameworkIA completo)",
     "modulo": "NAUTA", "fase": "v3.0", "prioridad": "Media", "estado": "Pendiente",
     "blast": "B - Bosquejo", "esfuerzo": "XL",
     "notas": "Carpetas: sobre-mi/, personas/, proyectos/, transcripciones/, notas-diarias/. Memoria evolutiva que mejora sola con el tiempo."},
]


def create_item(item):
    properties = {
        "Name": {"title": [{"text": {"content": item["nombre"]}}]},
    }
    if item.get("estado"):
        properties["Estado"] = {"select": {"name": item["estado"]}}
    if item.get("fase"):
        properties["Fase"] = {"select": {"name": FASE_MAP.get(item["fase"], "FASE 1")}}
    if item.get("modulo"):
        properties["Módulo"] = {"select": {"name": item["modulo"]}}
    if item.get("prioridad"):
        properties["Prioridad"] = {"select": {"name": PRIORIDAD_MAP.get(item["prioridad"], item["prioridad"])}}
    if item.get("blast"):
        properties["BLAST Step"] = {"select": {"name": BLAST_MAP.get(item["blast"], item["blast"])}}
    if item.get("esfuerzo"):
        properties["Esfuerzo"] = {"select": {"name": item["esfuerzo"]}}
    if item.get("notas"):
        properties["Notas"] = {"rich_text": [{"text": {"content": item["notas"][:2000]}}]}

    try:
        page = notion.pages.create(
            parent={"database_id": ROADMAP_MASTER_DB_ID},
            properties=properties
        )
        print(f"  ✅ {item['nombre']}")
        return page["id"]
    except Exception as e:
        print(f"  ❌ {item['nombre']}: {e}")
        return None


if __name__ == "__main__":
    print(f"\n🚀 Creando {len(ITEMS)} ítems en Roadmap Master...\n")
    ok = sum(1 for item in ITEMS if create_item(item))
    print(f"\n{'='*50}")
    print(f"✅ {ok}/{len(ITEMS)} ítems creados en Notion Roadmap Master")
    if ok < len(ITEMS):
        print("⚠️  Algunos fallaron — revisá las opciones select en Notion.")
    print(f"{'='*50}\n")
