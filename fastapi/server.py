import subprocess
import argparse
import uvicorn

from dotenv import load_dotenv, find_dotenv
from os import getenv

from src.auth import add_new_api_user, get_user_token
from src.database import SessionLocal

load_dotenv(find_dotenv())


MAIN_APP = 'src.main:app'


def export_requirements():
    cmd = ['poetry', 'export', '-f requirements.txt', '--output requirements.txt']
    subprocess.run(cmd)
    return


def run_prod():
    env = getenv('PY_ENV')
    port = getenv('PORT')
    if env != 'prod':
        return 1
    
    # ! gunicorn is not available on Windows
    cmd = f'gunicorn {MAIN_APP} --workers=2 --threads=8 --timeout 360 --worker-class uvicorn.workers.UvicornWorker -b :{port}'
    subprocess.run(cmd)


def run():
    port = int(getenv('PORT'))
    env = getenv('PY_ENV')
    if env == 'prod':
        return run_prod()

    auto_refresh = False
    log_level = 'info'
    if env == 'local':
        auto_refresh = True
        log_level = 'debug'

    uvicorn.run(MAIN_APP, host="127.0.0.1", port=port, log_level=log_level, reload=auto_refresh)
    return


def create_api_user():
    parser = argparse.ArgumentParser(description='Create API User.')
    parser.add_argument('username', type=str, help='New User to be authorized to use our API')

    args = parser.parse_args()
    db_session = SessionLocal()
    print(f'Creating API User ({args.username})')
    token = add_new_api_user(args.username, db_session)
    print(f'Token: {token}')
    print('Use this as Bearer Token when sending requests to the API')
    db_session.close()


def get_api_user_token():
    parser = argparse.ArgumentParser(description='Create API User.')
    parser.add_argument('username', type=str, help='New User to be authorized to use our API')

    args = parser.parse_args()
    db_session = SessionLocal()
    print(f'Retrieving API User Token for ({args.username})')
    token = get_user_token(args.username, db_session)
    print(f'Token: {token}')
    print('Use this as Bearer Token when sending requests to the API')
    db_session.close()
