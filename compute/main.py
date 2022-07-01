from textwrap import wrap
from typing import Tuple, Union
from fastapi import FastAPI, HTTPException, Header
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
import jwt
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FRONTEND_API_URL = "https://clerk.active.shrimp-85.lcl.dev/.well-known/jwks.json"
# PUBLIC_KEY_RAW = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0ruZrCXrxSA11kzwV0gpKzbkyP+yfapmzLlpZDMsYg4U2dp6TMoqpPklbHfLfSRQ4JgMat6X6vNd9mWOb2riZyqTs/xkClxWOwESrnOR68dQamrFgPBdHT/JrfKgBB98d+ne9L+190gEpHfFPSBesn8+4XntRFMK7nM7ouFvQuIIXGg2arjdPDYrILnJE16VEy6xpU2aUw+9dZyq2jaco+hvkS4efO3Vid26OkXWcwZyiJjmO9TUDHc86KUbKsGnHo2uTssw4GiUEJsJqWmZlVnbN6ZUZISFCtjlt6nYxPjMgusGiMkYx+CixkZrXUC2EsfcUjQMdQW7/ObjFP/5rwIDAQAB"
# SPLIT_PUBLIC_KEY = "\n".join(wrap(PUBLIC_KEY_RAW, 64))
# FORMATTED_KEY = (
#     "-----BEGIN PUBLIC KEY-----\n" + SPLIT_PUBLIC_KEY + "\n-----END PUBLIC KEY-----"
# )
# KID = "ins_2AQHEwin3Hn58OTsKwZPilZASNG"

# KEYSTORE_URLS = {
#     "firebase": "https://clerk.active.shrimp-85.lcl.dev/.well-known/jwks.json",
# }


@app.get("/")
def root_get(authorization: Union[str, None] = Header(default=None)):
    token = get_token_from_header(authorization)
    token_claims = get_token_claims(token)
    return {"token_claims": token_claims}


@app.get("/verify")
def verify(
    audience: str, cert_str: str, authorization: Union[str, None] = Header(default=None)
):

    token = get_token_from_header(authorization)
    token_claims = get_token_claims(token)
    is_token_valid, details = get_token_validity(token, audience, cert_str)

    return {
        "token_claims": token_claims,
        "is_token_valid": is_token_valid,
        "details": details,
    }


def get_token_validity(token: str, audience: str, cert_str: str) -> Tuple[bool, str]:
    try:
        cert_obj = load_pem_x509_certificate(
            cert_str.encode("utf-8"), default_backend()
        )
        public_key_str = cert_obj.public_key()

        jwt.decode(
            token,
            public_key_str,
            algorithms=["RS256"],
            audience=audience,
            options={
                "verify_exp": False,
            },
        )
        return True, "Success"
    except Exception as e:
        return False, str(e)


def get_token_claims(token: str):
    try:
        token_claims = jwt.decode(token, options={"verify_signature": False})
        return token_claims
    except Exception:
        raise HTTPException(400, detail="Unable to decode token.")


def get_token_from_header(authorization: str) -> str:
    if authorization is None:
        raise HTTPException(401, detail="Authorization token is missing.")

    authorization_parts = authorization.split(" ")
    if len(authorization_parts) < 2 or authorization_parts[0].lower() != "bearer":
        raise HTTPException(400, detail="Authorization header is malformed.")

    return authorization_parts[1]


def get_public_key(url: str, kid: str):
    jwks_client = jwt.PyJWKClient(url)
    signing_key = jwks_client.get_signing_key(kid).key
    return signing_key
