# Data Acquisition & Pre-processing for AI Systems (2026 Notes)

## 1. Why Data Matters in AI Systems
- Data is the foundation of AI — models learn patterns from data, not rules.
- Quality of AI ≈ Quality + Quantity + Diversity of data
- Garbage In → Garbage Out (GIGO principle)

### Key Roles of Data:
- Training (learn patterns)
- Validation (tune models)
- Testing (evaluate performance)
- Continuous learning (feedback loops)

### Types of Data:
- Structured (tables, SQL)
- Semi-structured (JSON, XML)
- Unstructured (text, images, audio, video)

---

## 2. Data Acquisition (Data Collection)

### Definition
Data acquisition is the process of collecting raw data from various internal and external sources for analysis or model training.

### Data Sources
#### Internal Sources
- Application databases
- Logs (server, user behavior)
- CRM / ERP systems

#### External Sources
- APIs (e.g., Twitter, weather APIs)
- Public datasets (Kaggle, UCI)
- Web scraping

#### Streaming / Real-time Data
- IoT sensors
- Kafka streams
- Event-driven systems

### Data Acquisition Methods
- Batch ingestion (scheduled)
- Real-time ingestion (streaming)
- Change Data Capture (CDC)
- Webhooks

### Common Tools
- Apache Kafka
- Apache NiFi
- Airbyte / Fivetran
- REST APIs / GraphQL

---

## 3. Data Pre-processing

### Definition
Transforming raw data into a clean, structured, usable format for machine learning.

### Steps
#### Data Cleaning
- Handle missing values (drop/impute)
- Remove duplicates
- Fix inconsistencies

#### Data Transformation
- Normalization / Standardization
- Encoding (Label / One-hot)
- Feature scaling

#### Feature Engineering
- Create new features
- Aggregations
- Domain-specific transformations

#### Data Reduction
- Sampling
- Dimensionality reduction (PCA)

#### Data Splitting
- Train / Validation / Test split

### Challenges
- Missing data
- Noisy data
- Imbalanced datasets
- Data drift

---

## 4. Data Storage Techniques

### Databases (OLTP)
- Relational: MySQL, PostgreSQL
- NoSQL: MongoDB, Redis, Cassandra, Neo4j
- Use case: transactional systems

### Data Warehouse (OLAP)
- Structured data, schema-on-write
- Examples: Snowflake, Redshift, BigQuery

### Data Lake
- Raw structured + unstructured data
- Schema-on-read
- Examples: AWS S3, Azure Data Lake, Hadoop HDFS

### Data Lakehouse
- Hybrid of lake + warehouse
- Examples: Delta Lake, Apache Iceberg, Apache Hudi

### Data Vault
- Hubs, Links, Satellites
- Enterprise-grade historical tracking

### Feature Store
- Stores ML features
- Examples: Feast, Tecton

### Vector Databases
- Store embeddings
- Examples: Pinecone, Weaviate, FAISS

### Data Pipelines
- ETL / ELT
- Tools: Spark, dbt, Airflow

---

## 5. Data Lifecycle
1. Data Collection
2. Storage
3. Processing
4. Feature Engineering
5. Model Training
6. Deployment
7. Monitoring

---

## 6. Role of Pandas

### What is Pandas?
A Python library for data manipulation and analysis.

### Features
- DataFrame and Series
- Cleaning: dropna(), fillna()
- Transformation: groupby(), merge(), pivot
- File handling: CSV, Excel, JSON, SQL

### Example
```python
import pandas as pd

df = pd.read_csv("data.csv")
df = df.dropna()
df["age_group"] = df["age"] // 10
summary = df.groupby("age_group").mean()
```

---

## 7. Industry Challenges (2026)
- Data privacy regulations
- Data bias
- Real-time processing
- Scaling pipelines
- Data observability

---

## Final Summary
- Data acquisition = collecting data
- Preprocessing = cleaning + transformation
- Storage types vary by use-case
- Pandas is essential for data workflows
- Data quality directly impacts AI performance
