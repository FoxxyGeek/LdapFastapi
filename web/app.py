from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI


from web.api import ldap

# app & routes init
app = FastAPI()
app.include_router(ldap.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

