# Telecom Data Lakehouse & ETL Pipeline

Pipeline moderno de Engenharia de Dados estruturado na **Arquitetura Medallion (`Bronze -> Silver -> Gold`)** para ingestão, saneamento e modelagem analítica de métricas de infraestrutura e desempenho de redes de telecomunicações.

## Arquitetura do Sistema

```mermaid
flowchart LR
    A[Fonte Transacional / Rede] -->|Extração Python| B[(Camada Bronze<br/>Raw Parquet)]
    B -->|Limpeza & SLA Rules| C[(Camada Silver<br/>Validated Parquet)]
    C -->|Agregação SQL DuckDB| D[(Camada Gold<br/>KPIs Parquet & CSV)]
    D -->|Consumo Analítico| E[Power BI / Dashboards]
    
    subgraph Orquestração & Storage
    F[Prefect Flow] -.-> A
    F -.-> B
    F -.-> C
    G[MinIO S3 Local] -.-> B
    end