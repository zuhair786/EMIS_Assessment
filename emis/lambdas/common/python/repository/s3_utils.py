from http import HTTPStatus
import boto3
import os
from exception.emis_exception import NoDataFoundError, NoFileFoundError
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
S3_URL_EXPIRY = int(os.environ['s3_url_expiry_in_seconds'])
S3_UPLOAD_BUCKET_NAME = os.environ['s3_upload_bucket']
s3_client = boto3.client('s3')

def generate_pre_signedUrl(input_data, event_type, upload=None):
    response = {}
    try:
        if input_data.get('folder_name').startswith('/'):
            input_data['folder_name'] = input_data['folder_name'].replace(
                '/', '', 1)
        if not input_data.get('folder_name').endswith('/'):
            input_data['folder_name'] = input_data['folder_name'] + '/'
        if input_data.get('file_name').startswith('/'):
            input_data['file_name'] = input_data['file_name'].replace('/', '')
        param = {'Bucket': S3_UPLOAD_BUCKET_NAME,
                 'Key': input_data.get('folder_name')+input_data.get('file_name')}
        if upload:
            param['ContentType'] = 'application/json'
        url = s3_client.generate_presigned_url(
            ClientMethod=event_type,
            Params=param,
            ExpiresIn=S3_URL_EXPIRY
        )
        response["statuscode"] = 200
        response["url"] = url
        logger.info("Got presigned URL: %s", url)
    except Exception as e:
        logger.error(
            "Couldn't get a presigned URL for client method %s ", e)
        raise e
    return response

def validate_input_files(file_location):
    patient_files = \
        s3_client.list_objects(
            Bucket=S3_UPLOAD_BUCKET_NAME, Prefix=file_location).get('Contents')
    logger.info("patient files retrived from s3 bucket %s", patient_files)
    if patient_files is None:
        raise NoDataFoundError(f"No data found in provided location {file_location}")
    if len(patient_files) == 1:
        file_name = patient_files[0]['Key'].rstrip('.json')
        if file_name == file_location:
            raise NoFileFoundError(f"File name not supported in location field, kindly provide valid folder details")
    return patient_files
    
def get_s3_file_informations(key,patient_files):
    s3_response = s3_client.get_object(
        Bucket=S3_UPLOAD_BUCKET_NAME, Key=patient_files[key]['Key'])
    no_of_rows = s3_response['Body'].read().decode(
        'utf8').count('\n') - 1
    content_type = s3_response['ContentType']
    return no_of_rows, content_type

def get_s3_folder_location_to_start_job(patient_files):
    if patient_files[0]['Key'].endswith('.json'):
        folder_path = patient_files[0]['Key'].split('/')
        folder_path.pop()
        folder_path = '/'.join(folder_path)
        s3_location = 's3://' + S3_UPLOAD_BUCKET_NAME + \
            '/' + folder_path
    else:
        s3_location = 's3://' + S3_UPLOAD_BUCKET_NAME + \
            '/' + patient_files[0]['Key']
    return s3_location