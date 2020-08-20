import sys
import logging
import json
import azure.functions as func

from .Result import Result
from .DigitsCalculator import pi_digits_Python

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    digits_param = req.params.get('digits')

    if digits_param is None:
        return func.HttpResponse(
            "Please pass URL parameter ?digits= to specify a positive number of digits",
            status_code=400)

    pi = Result(digits_param, "")
    try:
        digits = int(digits_param)
        if digits > 0:
            digits_string = pi_digits_Python(digits)
            pi.output = digits_string[:1] + '.' + digits_string[1:]
            pi.raw = digits_string
    except ValueError:
        pi.output = "" + traceback.format_exc() # .encode("utf-8")

    return func.HttpResponse(json.dumps(pi.__dict__))


