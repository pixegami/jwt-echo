from textwrap import wrap
from typing import Union
from fastapi import FastAPI, HTTPException, Header
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
import jwt


app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_API_URL = "https://clerk.active.shrimp-85.lcl.dev/.well-known/jwks.json"
PUBLIC_KEY_RAW = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0ruZrCXrxSA11kzwV0gpKzbkyP+yfapmzLlpZDMsYg4U2dp6TMoqpPklbHfLfSRQ4JgMat6X6vNd9mWOb2riZyqTs/xkClxWOwESrnOR68dQamrFgPBdHT/JrfKgBB98d+ne9L+190gEpHfFPSBesn8+4XntRFMK7nM7ouFvQuIIXGg2arjdPDYrILnJE16VEy6xpU2aUw+9dZyq2jaco+hvkS4efO3Vid26OkXWcwZyiJjmO9TUDHc86KUbKsGnHo2uTssw4GiUEJsJqWmZlVnbN6ZUZISFCtjlt6nYxPjMgusGiMkYx+CixkZrXUC2EsfcUjQMdQW7/ObjFP/5rwIDAQAB"
SPLIT_PUBLIC_KEY = "\n".join(wrap(PUBLIC_KEY_RAW, 64))
FORMATTED_KEY = (
    "-----BEGIN PUBLIC KEY-----\n" + SPLIT_PUBLIC_KEY + "\n-----END PUBLIC KEY-----"
)
KID = "ins_2AQHEwin3Hn58OTsKwZPilZASNG"


@app.get("/")
def root_get(authorization: Union[str, None] = Header(default=None)):

    if authorization is None:
        raise HTTPException(401, detail="Authorization token is missing.")

    authorization_parts = authorization.split(" ")
    print(authorization_parts)

    if len(authorization_parts) != 2 or authorization_parts[0].lower() != "bearer":
        raise HTTPException(400, detail="Authorization header is malformed.")

    token = authorization_parts[1]
    token_claims = None
    is_token_valid = False

    try:
        token_claims = jwt.decode(token, options={"verify_signature": False})
    except Exception:
        raise HTTPException(400, detail="Unable to decode token.")

    try:
        jwt.decode(
            token, FORMATTED_KEY, algorithms=["RS256"], options={"verify_exp": False}
        )
        is_token_valid = True
    except Exception as e:
        print(f"Could not validate token: {e}")

    return {"token_claims": token_claims, "is_token_valid": is_token_valid}


def get_public_key():
    jwks_client = jwt.PyJWKClient(FRONTEND_API_URL)
    signing_key = jwks_client.get_signing_key(KID).key
    print("Caching sign key: ", signing_key)
    return signing_key
