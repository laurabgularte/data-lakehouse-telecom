import pandas as pd
from src.transform import transform_to_silver


def test_transform_to_silver_sla_and_deduplication(tmp_path):
    # Cria dado bruto temporário com duplicata e latências distintas
    raw_file = tmp_path / "raw_test.parquet"
    df_raw = pd.DataFrame(
        {
            "connection_id": [1, 1, 2],
            "city": ["Ibirubá", "Ibirubá", "Carazinho"],
            "plan_speed_mbps": [300, 300, 500],
            "status": ["ATIVO", "ATIVO", "ATIVO"],
            "latency_ms": [15.0, 15.0, 65.0],
            "extracted_at": ["2026-11-18 10:00:00"] * 3,
        }
    )
    df_raw.to_parquet(raw_file, index=False)

    silver_path = transform_to_silver(str(raw_file))
    df_silver = pd.read_parquet(silver_path)

    assert len(df_silver) == 2
    assert (
        bool(df_silver.loc[df_silver["connection_id"] == 1, "sla_compliant"].iloc[0])
        is True
    )
    assert (
        bool(df_silver.loc[df_silver["connection_id"] == 2, "sla_compliant"].iloc[0])
        is False
    )
