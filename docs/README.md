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

## Tools & Technologies Used

| Category            | Tool / Service                          |
|---------------------|------------------------------------------|
| **Orchestration**   | Apache Airflow                          |
| **Data Extraction** | Python + Zillow API via RapidAPI        |
| **Cloud Platform**  | Amazon Web Services (AWS)               |
| **Storage**         | Amazon S3 (Multi-Zone: Raw, Processed)  |
| **ETL Logic**       | AWS Lambda (JSON to CSV)                |
| **Data Warehouse**  | Amazon Redshift                         |
| **Visualization**   | Amazon QuickSight                       |
| **IAM Roles**       | Granular permissions for Lambda, S3, Redshift |
| **Security**        | VPC, Security Groups, IAM               |

---

## Key Features

- Automated extraction of real estate data from a public API  
- Lambda-powered data transformation: JSON ➝ CSV  
- Serverless, event-driven pipeline: S3 triggers Lambda functions  
- Orchestrated with Airflow using `PythonOperator`, `BashOperator`, `S3KeySensor`, and `S3ToRedshiftOperator`  
- Secure and scalable ingestion into Amazon Redshift  
- Dynamic dashboards and visualizations in QuickSight  
- IAM-based access control and least privilege configuration

---

## Example Visualizations in QuickSight

- **Median home prices by ZIP code**
- **Average price vs bedroom count**
- **Rent Zestimate by home type**
- **Comparative analysis by city or home status**

---

## Testing & Validation

- Airflow DAGs tested end-to-end on EC2-hosted Airflow instance  
- Redshift queries validated via Query Editor v2  
- QuickSight dashboards are configured to refresh dynamically  

---

## Folder Structure

├── dags/ # Airflow DAG for the pipeline

├── scripts/ # Python scripts for API data extraction and lambda functions

├── datasets/ # (Optional) Sample transformed data

├── docs/ # Architecture diagrams, visuals

├── README.md




