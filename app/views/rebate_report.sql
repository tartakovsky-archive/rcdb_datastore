SELECT
    DATE_TRUNC(
        :timeframe,
        CASE
            WHEN expected_rebates.ts is NULL
                THEN rebates.timestamp
            ELSE expected_rebates.ts
        END
    ) as report_timestamp,
    CASE
        WHEN expected_rebates.name is NULL THEN rebates.name
        ELSE expected_rebates.name
    END as report_name,
    CASE
        WHEN expected_rebates.sym is NULL THEN rebates.symbol
        ELSE expected_rebates.sym
    END as report_symbol,
    CASE
        WHEN expected_rebates.account_type is NULL THEN rebates.account_type
        ELSE expected_rebates.account_type
    END as report_account_type,
    SUM(COALESCE(volume, 0.0)) as volume,
    SUM(COALESCE(volume_usd, 0.0)) as volume_usd,
    SUM(COALESCE(expected_rebates.expected_rebate, 0.0)) as report_expected_rebate,
    SUM(COALESCE(rebates.rebate, 0.0)) as report_rebate,
    SUM(COALESCE(expected_rebates.expected_rebate_usd, 0.0)) as report_expected_rebate_usd,
    SUM(COALESCE(rebates.rebate_usd, 0.0)) as report_rebate_usd,
    SUM(COALESCE(rebates.rebate, 0.0)) - SUM(COALESCE(expected_rebates.expected_rebate, 0.0)) as report_difference,
    SUM(COALESCE(rebates.rebate_usd, 0.0)) - SUM(COALESCE(expected_rebates.expected_rebate_usd, 0.0)) as report_difference_usd
FROM rebates
    FULL OUTER JOIN (
        SELECT
            trades.*, volume * 0.00005 as expected_rebate, volume_usd * 0.00005 as expected_rebate_usd
        FROM (
            SELECT
                time_bucket('1 hour'::interval, timestamp) as ts,
                name,
                sym,
                account_type,
                SUM(
                    CASE
                        WHEN symbol ilike ANY (
                            select s || '%'
                            from unnest(ARRAY ['EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'RUB', 'UAH']::text[]) s(s))
                        THEN
                            (CASE WHEN price_avg_buy = 0 THEN 0.0 ELSE volume_buy / price_avg_buy END) +
                            (CASE WHEN price_avg_sell = 0 THEN 0.0 ELSE volume_sell / price_avg_sell END)
                        ELSE volume_buy + volume_sell
                    END
                ) as volume,
                SUM(volume_buy_usd + volume_sell_usd) as volume_usd
            FROM (
                SELECT
                    *,
                    (CASE
                        WHEN symbol LIKE 'EUR/%' OR symbol LIKE '%/EUR' THEN 'EUR'
                        WHEN symbol LIKE 'GBP/%' OR symbol LIKE '%/GBP' THEN 'GBP'
                        WHEN symbol LIKE 'AUD/%' OR symbol LIKE '%/AUD' THEN 'AUD'
                        WHEN symbol LIKE 'BRL/%' OR symbol LIKE '%/BRL' THEN 'BRL'
                        WHEN symbol LIKE 'TRY/%' OR symbol LIKE '%/TRY' THEN 'TRY'
                        WHEN symbol LIKE 'RUB/%' OR symbol LIKE '%/RUB' THEN 'RUB'
                        WHEN symbol LIKE 'UAH/%' OR symbol LIKE '%/UAH' THEN 'UAH'
                        ELSE 'NON_FIAT'
                    END) as sym
                FROM db.public.account_trades
                WHERE timestamp >= :start_datetime
                  AND timestamp <= :end_datetime
                  AND (:param_account IS NULL OR :param_account = name || '_' || account_type)
                  AND name || '_' || account_type NOT IN :excluded_accounts
            ) as account_tr
            WHERE sym in :currencies
            GROUP BY ts, name, sym, account_type
        ) as trades
        WHERE trades.sym <> 'NON_FIAT'
    ) as expected_rebates ON rebates.timestamp = expected_rebates.ts
                         AND rebates.symbol = expected_rebates.sym
                         AND rebates.account_type = expected_rebates.account_type
                         AND rebates.name = expected_rebates.name
WHERE rebates.timestamp >= :start_datetime
  AND rebates.timestamp <= :end_datetime
  AND rebates.symbol IN :currencies
  AND (:param_account IS NULL OR :param_account = rebates.name || '_' || rebates.account_type)
  AND (rebates.name || '_' || rebates.account_type) NOT IN :excluded_accounts
GROUP BY report_timestamp, report_name, report_account_type, report_symbol
