import os
import duckdb


def load_to_gold(silver_path: str) -> str:
    """Consome a camada Silver via DuckDB, agrega métricas de negócio e materializa a Camada Gold."""
    os.makedirs("data/gold", exist_ok=True)

    con = duckdb.connect(database=":memory:", read_only=False)

    # Cria tabela analítica baseada na camada Silver
    con.execute(f"""
        CREATE TABLE silver_data AS 
        SELECT * FROM read_parquet('{silver_path}')
    """)

    # Agregação de Negócio: Visão consolidada por cidade para relatórios executivos/BI
    gold_df = con.execute("""
        SELECT 
            city,
            COUNT(connection_id) AS total_connections,
            SUM(CASE WHEN status = 'ATIVO' THEN 1 ELSE 0 END) AS active_connections,
            ROUND(AVG(latency_ms), 2) AS avg_latency_ms,
            ROUND(100.0 * SUM(CASE WHEN sla_compliant THEN 1 ELSE 0 END) / COUNT(*), 2) AS sla_compliance_rate_pct
        FROM silver_data
        GROUP BY city
        ORDER BY active_connections DESC
    ;""").fetchdf()

    gold_path = "data/gold/kpi_city_performance.parquet"
    gold_df.to_parquet(gold_path, index=False)

    # Exporta também uma cópia limpa em CSV para consumo direto de ferramentas de BI
    csv_path = "data/gold/kpi_city_performance.csv"
    gold_df.to_csv(csv_path, index=False)

    con.close()
    print(f"[GOLD] Camada Gold materializada com sucesso em {gold_path} e {csv_path}")

    return gold_path
