import datetime

TOKEN_EXPIRES = datetime.timedelta(hours=8)

STATUS_CODE = {"SUCCESS": "S", "FAILURE": "F", "PENDING": "P"}

CODE_STATUS = {"S": "SUCCESS", "F": "FAILURE", "P": "PENDING"}
SALE_TYPES = ["retail", "wholesale", "custom"]

DATE_FORMAT_STR = "%Y/%m/%d, %H:%M:%S"
