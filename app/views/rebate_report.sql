WITH expected_rebates AS (
    SELECT
        trades.*, volume * 0.00005 as expected_rebate, volume_usd * 0.00005 as expected_rebate_usd
    FROM (
        SELECT
            time_bucket('1 hour'::interval, timestamp) as ts,
            name,
            CASE
                WHEN symbol LIKE 'EUR/%' OR symbol LIKE '%/EUR' THEN 'EUR'
                WHEN symbol LIKE 'GBP/%' OR symbol LIKE '%/GBP' THEN 'GBP'
                WHEN symbol LIKE 'AUD/%' OR symbol LIKE '%/AUD' THEN 'AUD'
                WHEN symbol LIKE 'BRL/%' OR symbol LIKE '%/BRL' THEN 'BRL'
                WHEN symbol LIKE 'TRY/%' OR symbol LIKE '%/TRY' THEN 'TRY'
                WHEN symbol LIKE 'RUB/%' OR symbol LIKE '%/RUB' THEN 'RUB'
                WHEN symbol LIKE 'UAH/%' OR symbol LIKE '%/UAH' THEN 'UAH'
                ELSE 'NON_FIAT'
            END as sym,
            account_type,
            SUM(
                CASE
                    WHEN symbol ilike ANY (
                        select s || '%'
                        from unnest(ARRAY ['EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'RUB', 'UAH']::text[]) s(s)
                    )
                    THEN volume_base_buy + volume_base_sell
                    ELSE volume_buy + volume_sell
                END
            ) as volume,
            SUM(volume_buy_usd + volume_sell_usd) as volume_usd
        FROM account_trades
        WHERE timestamp >= :start_datetime
          AND timestamp <= :end_datetime
          AND (:param_account IS NULL OR :param_account = name || '_' || account_type)
          AND name || '_' || account_type NOT IN :excluded_accounts
        GROUP BY ts, name, sym, account_type
    ) as trades
    WHERE trades.sym in :currencies
),
recieved_rebates AS (
    SELECT
        *
    FROM rebates
    WHERE rebates.timestamp >= :start_datetime
      AND rebates.timestamp <= :end_datetime
      AND rebates.symbol IN :currencies
      AND (:param_account IS NULL OR :param_account = rebates.name || '_' || rebates.account_type)
      AND (rebates.name || '_' || rebates.account_type) NOT IN :excluded_accounts
),
merged_rebates AS (
    SELECT
        recieved_rebates.timestamp as rec_timestamp,
        expected_rebates.ts as exp_timestamp,
        recieved_rebates.symbol as rec_symbol,
        expected_rebates.sym as exp_symbol,
        recieved_rebates.account_type as rec_account_type,
        expected_rebates.account_type as exp_account_type,
        recieved_rebates.name as rec_name,
        expected_rebates.name as exp_name,
        expected_rebates.volume as volume,
        expected_rebates.volume_usd as volume_usd,
        recieved_rebates.rebate as rebate,
        recieved_rebates.rebate_usd as rebate_usd,
        expected_rebates.expected_rebate as expected_rebate,
        expected_rebates.expected_rebate_usd as expected_rebate_usd
    FROM recieved_rebates
    LEFT JOIN expected_rebates ON recieved_rebates.timestamp = expected_rebates.ts
                              AND recieved_rebates.symbol = expected_rebates.sym
                              AND recieved_rebates.account_type = expected_rebates.account_type
                              AND recieved_rebates.name = expected_rebates.name
    UNION ALL
    SELECT
        recieved_rebates.timestamp as rec_timestamp,
        expected_rebates.ts as exp_timestamp,
        recieved_rebates.symbol as rec_symbol,
        expected_rebates.sym as exp_symbol,
        recieved_rebates.account_type as rec_account_type,
        expected_rebates.account_type as exp_account_type,
        recieved_rebates.name as rec_name,
        expected_rebates.name as exp_name,
        expected_rebates.volume as volume,
        expected_rebates.volume_usd as volume_usd,
        recieved_rebates.rebate as rebate,
        recieved_rebates.rebate_usd as rebate_usd,
        expected_rebates.expected_rebate as expected_rebate,
        expected_rebates.expected_rebate_usd as expected_rebate_usd
    FROM recieved_rebates
    RIGHT JOIN expected_rebates ON recieved_rebates.timestamp = expected_rebates.ts
                               AND recieved_rebates.symbol = expected_rebates.sym
                               AND recieved_rebates.account_type = expected_rebates.account_type
                               AND recieved_rebates.name = expected_rebates.name
    WHERE recieved_rebates.timestamp IS NULL
)
SELECT
    DATE_TRUNC(
        :timeframe,
        CASE
            WHEN rec_timestamp is NULL THEN exp_timestamp
            ELSE rec_timestamp
        END
    ) as report_timestamp,
    CASE
        WHEN rec_name is NULL THEN exp_name
        ELSE rec_name
    END as report_name,
    CASE
        WHEN rec_symbol is NULL THEN exp_symbol
        ELSE rec_symbol
    END as report_symbol,
    CASE
        WHEN rec_account_type is NULL THEN exp_account_type
        ELSE rec_account_type
    END as report_account_type,
    SUM(COALESCE(volume, 0.0)) as volume,
    SUM(COALESCE(volume_usd, 0.0)) as volume_usd,
    SUM(COALESCE(expected_rebate, 0.0)) as report_expected_rebate,
    SUM(COALESCE(rebate, 0.0)) as report_rebate,
    SUM(COALESCE(expected_rebate_usd, 0.0)) as report_expected_rebate_usd,
    SUM(COALESCE(rebate_usd, 0.0)) as report_rebate_usd,
    SUM(COALESCE(rebate, 0.0)) - SUM(COALESCE(expected_rebate, 0.0)) as report_difference,
    SUM(COALESCE(rebate_usd, 0.0)) - SUM(COALESCE(expected_rebate_usd, 0.0)) as report_difference_usd
FROM merged_rebates
GROUP BY report_timestamp, report_name, report_account_type, report_symbol;
