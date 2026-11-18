from prefect import flow, task
import sys
import os

# Garante que o interpretador encontre os módulos na pasta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.extract import extract_raw_telecom_data
from src.transform import transform_to_silver
from src.load import load_to_gold


@task(name="Extract Task", retries=2, retry_delay_seconds=5)
def run_extraction():
    return extract_raw_telecom_data()


@task(name="Transform Task")
def run_transformation(bronze_path: str):
    return transform_to_silver(bronze_path)


@task(name="Load Task")
def run_load(silver_path: str):
    return load_to_gold(silver_path)


@flow(name="Telecom Lakehouse Medallion Flow", log_prints=True)
def main_lakehouse_pipeline():
    print("Iniciando pipeline de Engenharia de Dados (Medallion Architecture)...")

    bronze_file = run_extraction()
    silver_file = run_transformation(bronze_file)
    gold_file = run_load(silver_file)

    print(f"Pipeline executado com sucesso! Artefato final gerado em: {gold_file}")


if __name__ == "__main__":
    main_lakehouse_pipeline()
