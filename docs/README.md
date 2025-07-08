# Zillow Real Estate Data Pipeline with Airflow, AWS Lambda, Redshift, and QuickSight

This project demonstrates an end-to-end data engineering pipeline that extracts real estate data from the **Zillow API**, transforms it using **AWS Lambda**, stores it in **Amazon Redshift**, and visualizes it with **Amazon QuickSight** — all orchestrated via **Apache Airflow**.

---

## Architecture Overview

\`\`\`
Zillow API → EC2 (Airflow DAG) 
    → S3 (Landing Zone) 
        → Lambda (Transform JSON → CSV) 
            → S3 (Intermediate Zone) 
                → Airflow Sensor 
                    → Redshift COPY 
                        → QuickSight
\`\`\`

---

## Tech Stack

- **Apache Airflow** (ETL Orchestration)
- **AWS EC2** (Airflow Host)
- **AWS Lambda** (ETL Transformation Function)
- **AWS S3** (Data Lake: Raw and Transformed Zones)
- **Amazon Redshift** (Data Warehouse)
- **Amazon QuickSight** (BI & Visualization)
- **Python** (API Extraction + Lambda Transform)

---

# 🔧 Key Features

- ✅ Extracts Zillow real estate listings from a RapidAPI source  
- ✅ Transforms and cleans the raw JSON data to CSV using AWS Lambda  
- ✅ Dynamically loads transformed data into Amazon Redshift via Airflow  
- ✅ Visualizes median price, rent estimates, and location-based insights with QuickSight  
- ✅ Modular DAG using Airflow \`BashOperator\`, \`PythonOperator\`, \`S3KeySensor\`, and \`S3ToRedshiftOperator\`

---


