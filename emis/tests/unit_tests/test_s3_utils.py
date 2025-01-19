import pytest
from unittest.mock import patch, MagicMock
from repository.s3_utils import validate_input_files, get_s3_file_informations, get_s3_folder_location_to_start_job
from exception.emis_exception import NoDataFoundError, NoFileFoundError
import datetime
from dateutil.tz import tzutc
import os
S3_UPLOAD_BUCKET_NAME = os.environ.get('S3_UPLOAD_BUCKET_NAME')


@patch("repository.s3_utils.s3_client")
def test_validate_input_files_success(mock_s3_client):
    # Mock response for list_objects
    mock_s3_client.list_objects.return_value = {
        'Contents': [{'Key': 'test_folder/folder1/', 'LastModified': datetime.datetime(2025, 1, 19, 6, 49, 11, tzinfo=tzutc()), 'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cwad183ae9282468f489675d1ffc0fc8e4a4e752b9e4'}}, 
                     {'Key': 'test_folder/folder1/Beth967_Hansen121_4e343b0a-8698-b6dd-64c6-c2d2d0959e6e.json', 'LastModified': datetime.datetime(2025, 1, 19, 6, 50, 10, tzinfo=tzutc()), 'ETag': '"87f0eb699a41a55945a8ae8349751e11"', 'Size': 2662144, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cdad183qe9282468f489675d1ffc0fc8e4a4e752b9e4'}}, 
                     {'Key': 'test_folder/folder1/Bette450_Anderson154_6e4ac285-2a8d-a30d-5ecb-e32cb595a876.json', 'LastModified': datetime.datetime(2025, 1, 19, 6, 50, 14, tzinfo=tzutc()), 'ETag': '"28be0c8dace408b898a2b9449dbcb803"', 'Size': 1576110, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cdad183ae1282468f489675d1ffc0fc8e4a4e752b9e4'}}]
    }
    
    # Call the function with a valid folder
    result = validate_input_files("test_folder/folder1")
    
    # Assert that the result matches the mocked S3 response
    assert result == [{'Key': 'test_folder/folder1/', 'LastModified': datetime.datetime(2025, 1, 19, 6, 49, 11, tzinfo=tzutc()), 'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cdad183ae9282468f489675d1ffc0fc8e4a4e752b9e4'}}, 
                     {'Key': 'test_folder/folder1/Beth967_Hansen121_4e343b0a-8698-b6dd-64c6-c2d2d0959e6e.json', 'LastModified': datetime.datetime(2025, 1, 19, 6, 50, 10, tzinfo=tzutc()), 'ETag': '"87f0eb699a43a55945a8ae8349751e11"', 'Size': 2662144, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cdad183ae928e468f489675d1ffc0fc8e4a4e752b9e4'}}, 
                     {'Key': 'test_folder/folder1/Bette450_Anderson154_6e4ac285-2a8d-a30d-5ecb-e32cb595a876.json', 'LastModified': datetime.datetime(2025, 1, 19, 6, 50, 14, tzinfo=tzutc()), 'ETag': '"28be0c8dace478b898a2b9449dbcb803"', 'Size': 1576110, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'emis-dev-ug', 'ID': 'bff6ea052377c5c7afa4cdad183ae92824k8f489675d1ffc0fc8e4a4e752b9e4'}}]


@patch("repository.s3_utils.s3_client")
def test_validate_input_files_no_data(mock_s3_client):
    # Mock response with no data
    mock_s3_client.list_objects.return_value = {"Contents": None}
    
    try:
        validate_input_files("test-folder/")
    except NoDataFoundError as e:
        assert str(e) == "No data found in provided location test-folder/"
    

@patch("repository.s3_utils.s3_client")
def test_validate_input_files_invalid_file_name(mock_s3_client):
    # Mock response with one file matching the folder name
    mock_s3_client.list_objects.return_value = {
        "Contents": [{"Key": "test-folder.json"}]
    }
    try:
        validate_input_files("test-folder")
    except NoFileFoundError as e:
        assert str(e) == "File name not supported in location field, kindly provide valid folder details"
    

@patch("repository.s3_utils.s3_client")
def test_get_s3_file_informations(mock_s3_client):
    # Mock patient_files
    patient_files = [
        {"Key": "test-folder/test-file.json"}
    ]

    # Mock S3 get_object response
    mock_s3_client.get_object.return_value = {'ResponseMetadata': {'RequestId': 'HQ8C6TXW1A0HX0R6', 'HostId': 'fOeWReFpPCX+CT3Qqd+b6noBOZ71XFPNgCENsc7oUREWrdCAh4/Z5OsFynn+mKnBXfJc31HXKLORoqOMYa83Bg==', 
                                                                   'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'fOeWReFpPCX+CT3Qqd+b6noBOZ71XFPNgCENsc7oUREWrdCAh4o20OsFynn+mKnBXfJc31HXKLORoqOMYa83Bg==', 
                                                                   'x-amz-request-id': 'HQ8C6TXW1M9HX0R6', 'date': 'Sun, 19 Jan 2025 10:07:03 GMT', 'last-modified': 'Sun, 19 Jan 2025 10:06:42 GMT', 'etag': '"81051bcc2cf1bedf078224b0a93e2877"', 
                                                                   'x-amz-server-side-encryption': 'AES256', 'accept-ranges': 'bytes', 'content-type': 'application/json', 'content-length': '2', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 
                                                                   'AcceptRanges': 'bytes', 'LastModified': datetime.datetime(2025, 1, 19, 10, 6, 42, tzinfo=tzutc()), 'ContentLength': 2, 'ETag': '"81051bcc2cf1pedf378224b0a93e2877"', 
                                                                    'ContentType': 'application/json', 'ServerSideEncryption': 'AES256', 'Metadata': {}, 'Body': MagicMock(read=lambda: b"{ 'Patient': \n 'sample','resourceUrl':\n'https://sample.details.emis/'}\n")}

    # Call the function
    for key in range(len(patient_files)):
        no_of_rows, content_type = get_s3_file_informations(key, patient_files)

        # Expected results
        expected_no_of_rows = 2  
        expected_content_type = "application/json"

        # Assertions
        assert no_of_rows == expected_no_of_rows
        assert content_type == expected_content_type


def test_get_s3_folder_location_to_start_job():
    # Mock patient_files
    patient_files = [
        {"Key": "test-folder/empty-file.json"}
    ]

    # Call the function
    s3_location = get_s3_folder_location_to_start_job(patient_files)

    # Expected results
    expected_s3_location = "s3://emis_patients_bucket/test-folder"

    # Assertions
    assert s3_location == expected_s3_location
