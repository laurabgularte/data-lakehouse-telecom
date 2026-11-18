import os
import pandas as pd
import boto3
from datetime import datetime


def extract_raw_telecom_data() -> str:
    """Extrai dados brutos simulados de infraestrutura/telecom e salva na Camada Bronze."""
    os.makedirs("data/bronze", exist_ok=True)

    # Dados simulados de rede / clientes
    data = {
        "connection_id": [101, 102, 103, 104, 105, 106],
        "city": [
            "Ibirubá",
            "Carazinho",
            "Não-Me-Toque",
            "Ibirubá",
            "Espumoso",
            "Carazinho",
        ],
        "plan_speed_mbps": [300, 500, 300, 700, 500, 300],
        "status": ["ATIVO", "ATIVO", "SUSPENSO", "ATIVO", "CANCELADO", "ATIVO"],
        "latency_ms": [12.5, 8.1, 45.0, 9.3, 110.2, 7.8],
        "extracted_at": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * 6,
    }

    df = pd.DataFrame(data)
    file_path = "data/bronze/network_raw.parquet"
    df.to_parquet(file_path, index=False)
    print(f"[BRONZE] Dados brutos extraídos com sucesso para {file_path}")

    return file_path
