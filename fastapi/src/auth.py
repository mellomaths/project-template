import pandas as pd
import uuid
import base64
import os

from bcrypt import gensalt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from logging import Logger
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.dependencies import get_database_session, get_logger, get_auth_scheme, get_environment
from src.security.models.api_user import ApiUser
from fastapi.src.environment import Environment


def grant_access_to_api_user(
    credentials: HTTPAuthorizationCredentials = Depends(get_auth_scheme()),
    db_session: Session = Depends(get_database_session), 
    logger: Logger =Depends(get_logger),
    env: Environment = Depends(get_environment),
):
    logger = logger.getChild("grant_access_to_api_user")
    token = credentials.credentials
    username, token, salt = read_token(token)
    query = select(ApiUser.id, ApiUser.name, ApiUser.token).where(ApiUser.name == username)
    df = pd.read_sql(
        query,
        db_session.bind,
    )
    if (df.shape[0] == 0):
        logger.error(f'User (token={token}) not registered in Database')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    private_key = env.token_crypt_private_key
    saltB = salt.encode('latin-1')
    decrypted_token = decrypt_token(df['token'][0], private_key, saltB)
    if (decrypted_token != token):
        logger.error(f'User token is invalid')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    logger.info(f'Granting access to user (name={username})')


def gen_fernet_key(private_key: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(private_key.encode('latin-1')))
    return key


def encrypt_token(token: str, private_key: str, salt: bytes):
    fernet_key = gen_fernet_key(private_key, salt)
    fernet = Fernet(fernet_key)
    encrypted_token = fernet.encrypt(token.encode('latin-1'))
    return encrypted_token.decode('latin-1')


def decrypt_token(encrypted_token: str, private_key: str, salt: bytes):
    fernet_key = gen_fernet_key(private_key, salt)
    fernet = Fernet(fernet_key)
    decrypted_token = fernet.decrypt(encrypted_token).decode('latin-1')
    return decrypted_token


def read_token(token: str):
    decoded_token = base64.urlsafe_b64decode(token).decode('latin-1')
    sep = ':'
    username, token, salt = decoded_token.split(sep)
    return username, token, salt


def gen_user_token(username: str, token: str, salt: str):
    user_token = f'{username}:{token}:{salt}'
    return base64.urlsafe_b64encode(user_token.encode('latin-1')).decode('latin-1')


def get_user_token(username: str, db_session: Session):
    env = get_environment()
    query = select(ApiUser.id, ApiUser.name, ApiUser.token, ApiUser.token_salt).where(ApiUser.name == username)
    df = pd.read_sql(
        query,
        db_session.bind,
    )
    if (df.shape[0] == 0):
        print(f'User not registered in Database')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    private_key = env.token_crypt_private_key
    salt = df.token_salt[0]
    decrypted_token = decrypt_token(df.token[0], private_key, salt.encode('latin-1'))
    user_token = gen_user_token(username, decrypted_token, salt)
    return user_token



def add_new_api_user(username: str, db_session: Session):
    env = get_environment()
    query = select(ApiUser.id, ApiUser.name).where(ApiUser.name == username)
    df = pd.read_sql(
        query,
        db_session.bind,
    )
    if (df.shape[0] != 0):
        print(f'User {username} already created')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {username} already created')

    token = str(uuid.uuid4())
    salt = gensalt(12)
    salt_decoded = salt.decode('latin-1')
    private_key = env.token_crypt_private_key
    encrypted_token = encrypt_token(token, private_key, salt)

    api_user = ApiUser(name=username, token=encrypted_token, token_salt=salt_decoded)
    db_session.add(api_user)
    db_session.commit()
    print(f'User {username} successfully saved with hashed token')
    user_token = gen_user_token(username, token, salt_decoded)
    return user_token
