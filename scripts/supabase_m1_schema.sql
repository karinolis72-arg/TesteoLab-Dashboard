-- ============================================================
-- M1 ESPÍA — Tablas Supabase
-- Correr en: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- 1. BÚSQUEDAS GUARDADAS
-- Historial de búsquedas realizadas por la usuaria
CREATE TABLE IF NOT EXISTS m1_searches (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT now(),
    country     TEXT NOT NULL DEFAULT 'AR',
    keywords    TEXT,
    advertiser  TEXT,
    filters     JSONB DEFAULT '{}'::jsonb,
    result_count INTEGER DEFAULT 0
);

-- 2. ANUNCIOS ENCONTRADOS
-- Cada anuncio retornado por Meta Ads Library
CREATE TABLE IF NOT EXISTS m1_ads (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at      TIMESTAMPTZ DEFAULT now(),
    search_id       UUID REFERENCES m1_searches(id) ON DELETE CASCADE,
    ad_id           TEXT UNIQUE NOT NULL,
    advertiser      TEXT,
    advertiser_url  TEXT,
    copy            TEXT,
    days_active     INTEGER DEFAULT 0,
    start_date      DATE,
    platform        TEXT[],
    media_type      TEXT,
    media_url       TEXT,
    thumbnail_url   TEXT,
    cta             TEXT,
    landing_url     TEXT,
    raw_data        JSONB DEFAULT '{}'::jsonb
);

-- 3. ANÁLISIS IA POR ANUNCIO
-- Resultado del scoring + detección de oferta
CREATE TABLE IF NOT EXISTS m1_analysis (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at          TIMESTAMPTZ DEFAULT now(),
    ad_id               TEXT NOT NULL REFERENCES m1_ads(ad_id) ON DELETE CASCADE,
    viability_label     TEXT,              -- 'experimental' | 'probable' | 'muy_rentable' | 'ganador'
    estimated_budget    NUMERIC(10,2),     -- presupuesto estimado invertido USD
    offer_type          TEXT,              -- 'curso' | 'ebook' | 'membresia' | 'producto' | 'servicio'
    detected_price      TEXT,
    target_market       TEXT,
    success_signals     JSONB DEFAULT '[]'::jsonb,   -- lista de señales detectadas
    score               INTEGER DEFAULT 0,           -- 0-100
    score_breakdown     JSONB DEFAULT '{}'::jsonb,   -- desglose de puntos
    ai_recommendation   TEXT,
    analyzed_by         TEXT DEFAULT 'sistema'
);

-- 4. OFERTAS SELECCIONADAS
-- Las que la usuaria eligió para pasar a M2
CREATE TABLE IF NOT EXISTS m1_selected_offers (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at      TIMESTAMPTZ DEFAULT now(),
    ad_id           TEXT NOT NULL,
    analysis_id     UUID REFERENCES m1_analysis(id),
    offer_type      TEXT,
    price_point     TEXT,
    target_market   TEXT,
    key_message     TEXT,
    bonus_detected  TEXT[],
    score           INTEGER,
    days_active     INTEGER,
    estimated_investment TEXT,
    advertiser_url  TEXT,
    competitive_analysis JSONB DEFAULT '{}'::jsonb,
    sent_to_m2      BOOLEAN DEFAULT false,
    notion_page_id  TEXT    -- ID de la página en Notion "Oferta Seleccionada"
);

-- ============================================================
-- ÍNDICES para performance
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_m1_ads_search_id   ON m1_ads(search_id);
CREATE INDEX IF NOT EXISTS idx_m1_ads_days_active  ON m1_ads(days_active DESC);
CREATE INDEX IF NOT EXISTS idx_m1_analysis_ad_id   ON m1_analysis(ad_id);
CREATE INDEX IF NOT EXISTS idx_m1_analysis_score   ON m1_analysis(score DESC);
CREATE INDEX IF NOT EXISTS idx_m1_selected_sent    ON m1_selected_offers(sent_to_m2);

-- ============================================================
-- RLS (Row Level Security) — desactivado por ahora
-- La app accede con service key desde el backend
-- ============================================================
ALTER TABLE m1_searches         DISABLE ROW LEVEL SECURITY;
ALTER TABLE m1_ads              DISABLE ROW LEVEL SECURITY;
ALTER TABLE m1_analysis         DISABLE ROW LEVEL SECURITY;
ALTER TABLE m1_selected_offers  DISABLE ROW LEVEL SECURITY;
