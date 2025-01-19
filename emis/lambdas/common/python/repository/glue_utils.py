import boto3
from http import HTTPStatus
import logging
from response.craft_response import craft_response
from exception.emis_exception import JobFailedError
logger = logging.getLogger()
logger.setLevel(logging.INFO)
glue_client = boto3.client('glue')
mysql_connector = os.environ['MYSQL_CONNECTOR_JAR']

def invoke_glue_job(job_name, s3_location):
    try:
        job_arguments = {
            "--s3_loc": s3_location
            "--jars": mysql_connector
        }
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments=job_arguments
        )
        job_run_id = response['JobRunId']
        
        print(f"Glue job {job_name} started successfully with JobRunId: {job_run_id}")
        
        return job_run_id
            
    except Exception as e:
        logger.error("Error occurred while invoking glue job %s ", e)
        raise JobFailedError(f"Cannot able to start Glue job. Please try again later.")
