from fastapi import (APIRouter,
                     Response,
                     Depends,
                     Path,
                     Form,
                     Body)

from fastapi.exceptions import HTTPException

from datetime import datetime
from uuid import uuid4

from web.dependecies import check_cookie_session
from web.api import enums
from config import simple_db

router = APIRouter(tags=['LDAP'])


# base operation
@router.post('/bind')
async def bind(response: Response, email: str = Form(...), password: str = Form(...)):
    user = simple_db['users'].get(email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail={'message': 'authentication failed'}
        )

    if user['password'] != password:
        raise HTTPException(
            status_code=401,
            detail={'message': 'authentication failed'}
        )

    session_key = f'secret-{str(uuid4())}'
    simple_db['sessions'][session_key] = {
        'email': email,
        'date': datetime.today(),
    }

    response.set_cookie(key='secret', value=session_key)
    return {'ok': True}


@router.post('/unbind')
async def unbind(response: Response, secret: str = Depends(check_cookie_session)):
    if secret:
        simple_db['sessions'].pop(secret)
        response.delete_cookie(secret)
    else:
        raise HTTPException(
            status_code=403,
            detail={'message': 'Not allowed!'}
        )
    return {'message': 'logged out!'}


@router.post('/item/{item_type}/{item_id}')
async def create_item(item_type: enums.ItemType,
                      item_id: str = Path(...),
                      body: dict = Body(...),
                      _: str = Depends(check_cookie_session)):
    _list = simple_db['dbs'][item_type]
    if item_id in _list:
        raise HTTPException(
            status_code=400,
            detail={'message': 'item with such id already exist'}
        )

    if item_type is enums.ItemType.msisdn:
        if len(item_id) != 12:
            raise HTTPException(
                status_code=400,
                detail={'message': 'item_id length for msisdn must be 12'}
            )

    if item_type is enums.ItemType.sim:
        if len(item_id) != 20:
            raise HTTPException(
                status_code=400,
                detail={'message': 'item_id length for sim must be 20'}
            )
    _list[item_id] = body
    return {item_id: body}


@router.get('/items/{item_type}')
async def get_items(item_type: enums.ItemType,
                    _: str = Depends(check_cookie_session)):
    return {'results': simple_db['dbs'][item_type]}


@router.get('/item/{item_type}/{item_id}')
async def get_item(item_type: enums.ItemType,
                   item_id: str = Path(...),
                   _: str = Depends(check_cookie_session)):
    _item = simple_db['dbs'][item_type].get(item_id)
    if not _item:
        raise HTTPException(
            status_code=404,
            detail={'message': 'not found'}
        )
    return {'result': _item}
