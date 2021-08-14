import datetime

TOKEN_EXPIRES = datetime.timedelta(hours=8)

SALE_STATUS_CODE = {
    "PAID": "PAID",
    "PENDING": "PENDING",
    "NOT_PAID": "NOT_PAID",
    "PARTIAL_PAID": "PARTIAL_PAID",
    "REFUND": "REFUND",
   }

SALE_STATUS = list(SALE_STATUS_CODE.values())

SALE_TYPES = ["retail", "wholesale", "custom"]

DATE_FORMAT_STR = "%Y/%m/%d, %H:%M:%S"
