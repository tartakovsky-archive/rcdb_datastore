WITH self_volumes AS (
    SELECT
        date_trunc(:timeframe, timestamp) as ts,
        symbol,
        sum(volume_base_sell + volume_base_buy) as volume,
        sum(volume_sell + volume_buy) as volume_quote
    FROM account_trades
    WHERE timestamp >= :start_datetime
      AND timestamp <= :end_datetime
    GROUP BY ts, symbol
),
market_volumes AS (
    SELECT
        date_trunc(:timeframe, timestamp) as ts,
        symbol,
        sum(volume) as volume,
        sum(volume * close) as volume_quote
    FROM markets_data
    WHERE timestamp >= :start_datetime
      AND timestamp <= :end_datetime
      AND exchange = 'BINANCE'
      AND instrument = 'SPOT'
      AND (:unfilled OR symbol IN (SELECT symbol FROM self_volumes GROUP BY symbol))
    GROUP BY ts, symbol
),
merged_volumes as (
    SELECT
        self_volumes.ts as self_timestamp,
        self_volumes.symbol as self_symbol,
        self_volumes.volume as self_volume,
        self_volumes.volume_quote as self_volume_quote,
        market_volumes.ts as market_timestamp,
        market_volumes.symbol as market_symbol,
        market_volumes.volume as market_volume,
        market_volumes.volume_quote as market_volume_quote
    FROM self_volumes
    LEFT JOIN market_volumes ON self_volumes.ts = market_volumes.ts
                            AND self_volumes.symbol = market_volumes.symbol
    UNION ALL
    SELECT
        self_volumes.ts as self_timestamp,
        self_volumes.symbol as self_symbol,
        self_volumes.volume as self_volume,
        self_volumes.volume_quote as self_volume_quote,
        market_volumes.ts as market_timestamp,
        market_volumes.symbol as market_symbol,
        market_volumes.volume as market_volume,
        market_volumes.volume_quote as market_volume_quote
    FROM self_volumes
    RIGHT JOIN market_volumes ON self_volumes.ts = market_volumes.ts
                             AND self_volumes.symbol = market_volumes.symbol
    WHERE self_volumes.ts IS NULL
),
null_clean_report AS (
    SELECT
        CASE
            WHEN self_timestamp is NULL THEN market_timestamp
            ELSE self_timestamp
        END as timestamp,
        CASE
           WHEN self_symbol is NULL THEN market_symbol
           ELSE self_symbol
        END as symbol,
        CASE
           WHEN market_volume IS NULL THEN 0
           ELSE market_volume
        END as report_market_volume,
        CASE
           WHEN market_volume_quote IS NULL THEN 0
           ELSE market_volume_quote
        END as report_market_volume_quote,
        CASE
           WHEN self_volume IS NULL THEN 0
           ELSE self_volume
        END as report_self_volume,
        CASE
           WHEN self_volume_quote IS NULL THEN 0
           ELSE self_volume_quote
        END as report_self_volume_quote
    FROM merged_volumes
)
SELECT
    timestamp,
    symbol,
    report_market_volume as market_volume,
    report_self_volume as self_volume,
    report_market_volume_quote as market_volume_quote,
    report_self_volume_quote as self_volume_quote,
    CASE
        WHEN report_market_volume = 0 OR report_self_volume = 0 THEN 0
        ELSE report_self_volume / report_market_volume
    END as pct
FROM null_clean_report;
