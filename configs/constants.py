import datetime

TOKEN_EXPIRES = datetime.timedelta(hours=8)

SALE_STATUS_CODE = {
    "PAID": "PAID",
    "PARTIAL_PAID": "PARTIAL_PAID",
    "REFUND": "REFUND",
    "PENDING": "PENDING",
    "NOT_PAID": "NOT_PAID",
}

SALE_STATUS_CLOSE = (SALE_STATUS_CODE['PAID'],
                     SALE_STATUS_CODE['PARTIAL_PAID'],
                     SALE_STATUS_CODE['NOT_PAID'],
                     )

SALE_STATUS = list(SALE_STATUS_CODE.values())

SALE_TYPES = ["retail", "wholesale", "custom"]

DATE_FORMAT_STR = "%Y/%m/%d, %H:%M:%S"

MAX_PER_PAGE = 10