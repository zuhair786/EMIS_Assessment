import json
import logging
from handler.processing_handler import handle
logger = logging.getLogger()
import os
logger.setLevel((logging.DEBUG if eval(os.environ.get('IS_LOGLEVEL_DEBUG')) else logging.INFO))

def lambda_handler(event, context):
    logger.info("Request received to process patient record %s", event)
    try:
        if 'POST' in event['routeKey'] and 'upload' in event['routeKey']:
            return handle('upload',json.loads(event.get('body')))
        elif 'processRecord' in event['routeKey']:
            return handle('processRecord',event)
    except Exception as e:
        logger.error('Error while processing patient record %s', str(e))
        raise e