# Data Acquisition, Pre-processing & Analysis (Advanced Notes – 2026)

---

# 1. Importance of Data in AI Systems

Data is the core driver of AI systems. Modern AI (especially deep learning and LLMs) is **data-centric**, meaning performance improvements often come more from better data than better algorithms.

## Key Concepts
- Data-centric AI: Focus on improving data quality rather than model complexity
- Data Flywheel: More usage → more data → better models → more usage
- Feedback loops: Reinforcement learning, human feedback (RLHF)

## Data Quality Dimensions
- Accuracy
- Completeness
- Consistency
- Timeliness
- Uniqueness
- Validity

---

# 2. Data Acquisition (Deep Dive)

## Advanced Data Sources
- Synthetic data (generated using models like GANs, simulators)
- Third-party data providers (Snowflake Marketplace, AWS Data Exchange)
- Open data ecosystems (government, research)
- User-generated content (UGC)

## Acquisition Patterns
- Batch ingestion: periodic loads
- Streaming ingestion: real-time systems
- Micro-batching: hybrid model
- Event sourcing: store state changes as events

## Modern Stack (2026)
- Streaming: Kafka, Pulsar
- Connectors: Airbyte, Fivetran
- APIs: REST, GraphQL, gRPC
- Scraping: Playwright, Scrapy

## Data Contracts
- Schema agreements between producers and consumers
- Prevents pipeline breakage
- Tools: JSON Schema, Protocol Buffers

---

# 3. Data Pre-processing (Advanced)

## Missing Data Strategies
- MCAR, MAR, MNAR understanding
- Imputation techniques:
  - Mean/median/mode
  - KNN imputation
  - Model-based imputation

## Outlier Detection
- Z-score
- IQR method
- Isolation Forest

## Feature Engineering (Advanced)
- Feature crosses
- Embeddings
- Time-based features
- Window functions (rolling averages)

## Encoding Techniques
- One-hot encoding
- Target encoding
- Embedding encoding (deep learning)

## Scaling Techniques
- Min-Max scaling
- Standardization
- Robust scaling

---

# 4. Data Storage & Architecture (2026)

## Modern Data Stack
- Data ingestion → Data lake → Transformation → Warehouse → BI/ML

## Data Lakehouse Architecture
- Combines:
  - Storage (cheap, scalable)
  - Compute (query engines)
- Enables:
  - BI + ML on same data

## Medallion Architecture
- Bronze: raw data
- Silver: cleaned data
- Gold: business-ready data

## Data Mesh
- Domain-oriented ownership
- Data as a product
- Self-serve infrastructure

## Data Fabric
- Metadata-driven integration layer
- AI-powered data discovery

---

# 5. Data Processing

## ETL vs ELT
- ETL: transform before load
- ELT: transform after load (modern)

## Distributed Processing
- Apache Spark
- Flink (stream processing)

## Query Engines
- Trino
- Presto
- DuckDB (local analytics)

---

# 6. Data Analysis

## Exploratory Data Analysis (EDA)
- Summary statistics
- Distribution analysis
- Correlation analysis

## Statistical Techniques
- Hypothesis testing
- A/B testing
- Regression analysis

## Visualization
- Matplotlib, Seaborn, Plotly

## Advanced Analytics
- Time series analysis
- Causal inference
- Graph analytics

---

# 7. Pandas (Advanced Usage)

## Performance Optimization
- Vectorization
- Avoid loops
- Use categorical types

## Large Data Handling
- Chunking
- Dask (parallel pandas)
- Polars (faster alternative)

## Integration
- Works with NumPy, scikit-learn
- Connects to SQL databases

---

# 8. Data Governance & Observability

## Governance
- Data lineage
- Data catalog
- Access control

## Observability
- Data quality monitoring
- Drift detection
- Pipeline health

## Tools
- Great Expectations
- Monte Carlo
- DataHub

---

# 9. AI-Specific Data Concepts

## Feature Stores
- Offline vs Online store
- Feature versioning

## Vector Databases
- Embeddings
- Similarity search

## RAG Pipelines
- Retrieval + Generation
- Chunking strategies
- Embedding pipelines

---

# 10. Challenges in 2026

- Data privacy (GDPR, DPDP India)
- Data bias & fairness
- Real-time scalability
- Cost optimization
- Data security

---

# Final Summary

- Data acquisition: collecting from multiple sources
- Pre-processing: cleaning + transforming
- Storage: lakehouse is dominant
- Analysis: EDA + statistical methods
- Pandas: essential but evolving
- Governance & observability: critical in production AI

