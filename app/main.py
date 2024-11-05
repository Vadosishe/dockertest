import fastapi.responses
import requests
from fastapi import FastAPI, Request, status

from app.config import token

# creating app
app = FastAPI()

# Whitelisted IPs
WHITELISTED_IPS = ["127.0.0.1", "172.17.0.1"]

# creating headers
headers = {"Authorization": f"Bearer {token}"}


# ip checking
@app.middleware('http')
async def validate_ip(request: Request, call_next):
    # Get client IP
    ip = str(request.client.host)

    # Check if IP is allowed
    if ip not in WHITELISTED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return fastapi.responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

    # Proceed if IP is allowed
    return await call_next(request)


@app.get("/form/{form_id}")
async def main(form_id):
    url = f"https://api.hubapi.com/forms/v2/forms/{form_id}"
    response = requests.get(url=url, headers=headers)
    data = response.json()
    try:
        form_name = data["name"]
        result = {"status": "success",
                  "form_name": form_name}
    except (ValueError, KeyError) as error:
        result = {"status": "error",
                  "message": data["message"]}
        print(type(error))
    return result


@app.get("/")
async def main():
    data = "Напиши /docs для документации"
    return fastapi.responses.PlainTextResponse(content=data)
