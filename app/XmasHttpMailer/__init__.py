import logging
import os

import azure.functions as func
from sendgrid import SendGridAPIClient


SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', default='')
SENDGRID_TEMPLATE_ID = os.getenv('SENDGRID_TEMPLATE_ID', default='')

def extract_param(req, param):
    value = req.params.get(param)

    if not value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            value = req_body.get(param)

    return value

def send_mail_to(name, email):
    message = {
        "from": { "email": "no-reply@programmers.com.br" },
        "personalizations": [
            {
                "to": [
                    { "email": email }
                ],
                "dynamic_template_data": {
                    "name": name,
                },
            },
        ],
        "template_id": SENDGRID_TEMPLATE_ID
    }
    SendGridAPIClient(SENDGRID_API_KEY).send(message)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = extract_param(req, 'name')
    email = extract_param(req, 'email')

    if email and name:
        send_mail_to(name, email)
        return func.HttpResponse(f"Merry Xmas, {name}!")

    return func.HttpResponse(
            "Please pass email and name on the query string or in the request body",
            status_code=400)
