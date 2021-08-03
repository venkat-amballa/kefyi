import datetime

TOKEN_EXPIRES = datetime.timedelta(hours=8)

STATUS = {
    'SUCCESS':1,
    'FAILURE':0,
    'PENDING':2
}

SALE_TYPES = ['retail', 'wholesale', 'custom']