from http import HTTPStatus
import logging
import json
import os
from response.craft_response import craft_response
from exception import JobFailedError
from utils.validate_json_and_start_job import validate_json_and_invoke_jobs
from repository.s3_utils import generate_pre_signedUrl
logger = logging.getLogger()
logger.setLevel((logging.DEBUG if eval(os.environ.get('IS_LOGLEVEL_DEBUG')) else logging.INFO))
MIGRATION_JOB_NAME = os.environ['migration_job_name']


def handle(api_name, event):
    try:
        logger.info(
            "Api request received for emis process event %s, %s ", api_name, event)
        if api_name == 'upload':
            logger.info(
                "Api request received for getUrl event %s, %s ", api_name, event)
            if event.get('folder_name') is None or event.get('file_name') is None:
                return craft_response(HTTPStatus.BAD_REQUEST, json.dumps({'errorMessage': "folder_name and file_name are required"}))
            if event.get('folder_name').find('//') != -1:
                return craft_response(HTTPStatus.BAD_REQUEST, json.dumps({'errorMessage': "folder_name and file_name is not valid"}))
            return generate_pre_signedUrl(event, 'put_object', upload=True)
        elif api_name == 'processRecord':
            request_event = json.loads(event.get('body'))
            try:
                response = validate_json_and_invoke_jobs(
                    request_event, MIGRATION_JOB_NAME)
                return craft_response(HTTPStatus.OK, json.dumps({
                    'message': 'Emis process started successfully',
                    'JobRunId': response
                    }))
            except Exception as e:
                logger.error("Error occurred while starting emis process %s ", e)
                raise e
    except JobFailedError as e:
        return craft_response(HTTPStatus.SERVICE_UNAVAILABLE, 
                              json.dumps({'errorMessage': str(e)}))
    except Exception as e:
        return craft_response(HTTPStatus.INTERNAL_SERVER_ERROR, 
                              json.dumps({'errorMessage': str(e)}))