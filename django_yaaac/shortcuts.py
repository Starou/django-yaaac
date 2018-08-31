from builtins import str
import datetime
import decimal
import json
from django.http import HttpResponse


def encode_default(d):
    if isinstance(d, decimal.Decimal): 
        return float(str(d))
    elif  isinstance(d, datetime.date) or isinstance(d, datetime.datetime):
        return d.isoformat()
    raise TypeError


def json_response(data):
    return HttpResponse(json.dumps(data, default=encode_default),
                        content_type='application/json')
