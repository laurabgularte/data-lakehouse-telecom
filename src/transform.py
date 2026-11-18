import os
import pandas as pd


def transform_to_silver(bronze_path: str) -> str:
    """Lê a camada Bronze, aplica limpeza, regras de negócio e salva na Camada Silver."""
    os.makedirs("data/silver", exist_ok=True)

    df = pd.read_parquet(bronze_path)

    # Regra 1: Remover duplicatas baseadas no ID da conexão
    df = df.drop_duplicates(subset=["connection_id"])

    # Regra 2: Filtrar apenas conexões válidas e sem nulos críticos
    df = df.dropna(subset=["connection_id", "city"])

    # Regra 3: Adicionar coluna analítica de qualidade de link
    df["sla_compliant"] = df["latency_ms"].apply(lambda x: True if x < 50.0 else False)

    file_path = "data/silver/network_silver.parquet"
    df.to_parquet(file_path, index=False)
    print(f"[SILVER] Dados limpos e transformados salvos em {file_path}")

    return file_path
