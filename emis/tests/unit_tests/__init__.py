import os
import sys

sys.path.append(os.getcwd() + '/lambdas/common/python')
os.environ['s3_upload_bucket'] = 'emis_patients_bucket'
os.environ['s3_url_expiry_in_seconds'] = '300'

