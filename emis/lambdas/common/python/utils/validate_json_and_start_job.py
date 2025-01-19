from repository.s3_utils import get_s3_file_informations, validate_input_files, get_s3_folder_location_to_start_job
from repository.glue_utils import invoke_glue_job
from exception.emis_exception import NoDataFoundError, NonJsonFormatError
import os
import logging
logger = logging.getLogger()
logger.setLevel((logging.DEBUG if eval(
    os.environ.get('IS_LOGLEVEL_DEBUG')) else logging.INFO))


def validate_json_and_invoke_jobs(event, MIGRATION_JOB_NAME):
    patient_files = validate_input_files(
        event.get('location'))
    for key in range(len(patient_files)):
        if patient_files[key]['Key'].endswith('json'):
            no_of_rows, content_type = get_s3_file_informations(
                key, patient_files)
            if no_of_rows == 0:
                logger.info("No patient data found in file %s", patient_files[key])
                raise NoDataFoundError(f"No patient data found in provided file {patient_files[key]['Key']}")
            if content_type != 'application/json':
                logger.info("File found in non json format %s", patient_files[key])
                raise NonJsonFormatError(f"File found in non json format {patient_files[key]['Key']}")
        s3_location = get_s3_folder_location_to_start_job(patient_files)
        job_response = invoke_glue_job(MIGRATION_JOB_NAME, s3_location)
    return job_response