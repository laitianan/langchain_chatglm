# coding: utf-8
from typing import Optional
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
import config

app = FastAPI()
get_bearer_token = HTTPBearer(auto_error=False)

async def check_api_key(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    if config.api_keys:
        if auth is None or (token := auth.credentials) not in config.api_keys:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": {
                        "message": "",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "invalid_api_key",
                    }
                },
            )
        return token
    else:
        # api_keys not set; allow all
        return None


@app.get(path='/root',dependencies=[Depends(check_api_key)])
async def root(p):
    print(p)
    return "Hello world"+p

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)