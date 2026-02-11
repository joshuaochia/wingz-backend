import json
import boto3
from botocore.exceptions import ClientError
from .base import *


def get_secret(secret_name):
    region_name = ""

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return json.loads(get_secret_value_response['SecretString'])


db_secret = get_secret(os.environ.get("SECRET_MANAGER_RDS_ID"))
general_secret = get_secret(os.environ.get("SECRET_MANAGER_WINEAPP_ID"))
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
                "USER": db_secret["username"],
                "PASSWORD": db_secret["password"],
                "HOST": general_secret["DB_HOST"],
                "PORT": 5432,
    }
}
