from fastapi import Cookie, HTTPException

from datetime import datetime, timedelta

from config import simple_db


def check_cookie_session(secret: str | None = Cookie(default=None)):
    if secret in simple_db['sessions']:
        is_ex = simple_db['sessions'][secret]['date'] + timedelta(hours=2)
        if datetime.now() < is_ex:
            return secret
    raise HTTPException(
        status_code=401,
        detail={'message': 'Not allowed'}
    )
