-- scripts/init.sql
CREATE TABLE IF NOT EXISTS precos_crypto (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    price_brl NUMERIC,
    market_cap_brl NUMERIC,
    volume_brl NUMERIC,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);