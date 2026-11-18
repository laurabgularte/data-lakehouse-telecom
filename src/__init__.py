"""Pacote core do pipeline ETL da arquitetura Medallion (Bronze -> Silver -> Gold)."""

from .extract import extract_raw_telecom_data
from .load import load_to_gold
from .transform import transform_to_silver

__all__ = [
    "extract_raw_telecom_data",
    "transform_to_silver",
    "load_to_gold",
]
