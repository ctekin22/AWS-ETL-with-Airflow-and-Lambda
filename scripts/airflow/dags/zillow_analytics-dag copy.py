from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
import json 
import requests

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 1),  # adjust date as needed
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15),
}

now = datetime.now()
dt_now_string = now.strftime("%d%m%Y%H%M%S")  # Use a dt_string string for filenames

# Define S3 bucket for transformed data
s3_bucket = 'transformed-json-data-to-csv-bucket'

# Define your Python callable for the task
# Write the API response to a JSON file in your EC2 instance inside your DAG?s Python function.
def extract_zillow_data(**kwargs):
    url =kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']

    #return headers
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()

    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    file_str = f"response_data_{dt_string}.csv"

    # Write the JSON response to a file
    with open(output_file_path, 'w') as output_file:
        json.dump(response_data, output_file, indent=4)
    output_list = [output_file_path,  file_str]
    return output_list

    # Load config file
with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)

# Instantiate the DAG
with DAG(
    dag_id='zillow_analytics_dag',
    default_args=default_args,
    description='A DAG to extract data from Zero API via RapidAPI',
    schedule='@daily',
    catchup=False,
) as dag:

    # Create the PythonOperator task
    extract_zillow_data_var = PythonOperator(
    task_id='tsk_extract_zillow_data_var',
    python_callable=extract_zillow_data,
    op_kwargs={'url': "https://zillow56.p.rapidapi.com/search_polygon", 'querystring': {"polygon":"34.03959576441558 -118.50636536779786,34.0418716916327 -118.50276047888184,34.042440663894304 -118.49846894445801,34.04201393505594 -118.49417741003418,34.04087598099002 -118.4897142142334,34.03945351693672 -118.48525101843262,34.03788877892429 -118.48095948400879,34.03618175908096 -118.47683961096192,34.034190192514366 -118.47271973791504,34.031629538228394 -118.46962983312989,34.02835747861639 -118.4677415579834,34.02465847668084 -118.46671158972168,34.02081703478521 -118.46636826696778,34.01697541902413 -118.46636826696778,34.01341821237762 -118.4673982352295,34.011283816847104 -118.47100312414551,34.01057233974687 -118.47563798132325,34.01043004361143 -118.47992951574707,34.01071463564384 -118.48439271154786,34.01156840601794 -118.48868424597168,34.01270675316253 -118.49297578039551,34.01398737545716 -118.49709565344239,34.01555255425154 -118.50104386511231,34.01754455825562 -118.50464875402832,34.02039019717532 -118.50756699743653,34.02352028980117 -118.50962693395996,34.02707707311613 -118.51065690222168,34.03063370735633 -118.50997025671387,34.034190192514366 -118.5091119498291,34.03774652858273 -118.50825364294434,34.03959576441558 -118.50636536779786","output":"json","status":"forSale","sortSelection":"priorityscore","listing_type":"by_agent","doz":"any"}, 'headers':api_host_key, 'date_string':dt_now_string}
    )

    load_to_s3 = BashOperator(
       task_id = 'tsk_load_to_s3',
       bash_command = 'aws s3 mv {{ti.xcom_pull("tsk_extract_zillow_data_var")[0]}} s3://zillow-landing-stage/',
    )
    
    is_file_in_s3_available = S3KeySensor(
        task_id = 'tsk_is_file_in_s3_available',
        bucket_key = '{{ti.xcom_pull("tsk_extract_zillow_data_var")[1]}}',
        bucket_name = s3_bucket,
        aws_conn_id = 'aws_s3_conn', # will create this in Airflow
        wildcard_match = False,
        timeout = 120,
        poke_interval=5,
    )

    transfer_s3_to_redshift = S3ToRedshiftOperator(
        task_id = 'tsk_transfer_s3_to_redshift',
        aws_conn_id = 'aws_s3_conn', 
        redshift_conn_id = 'redshift_conn_id', # will create this in Airflow
        s3_bucket = s3_bucket,
        s3_key = '{{ti.xcom_pull("tsk_extract_zillow_data_var")[1]}}',
        schema = 'public',
        table = 'zillowdata',
        copy_options=['CSV', 'IGNOREHEADER 1', 'EMPTYASNULL', 'BLANKSASNULL'],
    )

    # Set task dependency so that upload runs after extraction
    extract_zillow_data_var >> load_to_s3 >> is_file_in_s3_available >>  transfer_s3_to_redshift