import os
from threading import Thread

from pyftpdlib.authorizers import DummyAuthorizer
from src.ftp_server.helper import add_user


DEBUG = os.environ.get('debug', False)

def load_s3(authorizer: DummyAuthorizer, data: dict):
    """
    :param authorizer
    :param data: {
        "user": "s3",
        "pass": "s3",
        "fs": "s3",
        "params": {
            "basePath": "/s3-fuse",
            "bucket": "my-bucket",
            "access_key_id": "AKIA....",
            "secret_access_key": "IDxd...."
        }
    }
    """
    user = data.get('user')
    access_key_id = data.get('params').get('access_key_id')
    secret_access_key = data.get('params').get('secret_access_key')
    passwd = f'./.passwd-s3fs/{user}'
    with open(passwd, 'w') as f:
        f.write(f'{access_key_id}:{secret_access_key}')

    os.system(f'chmod 600 {passwd}')
    bucket = data.get('params').get('bucket')

    # if basePath is not set, use bucket name as basePath
    base_path = data.get('params').get('basePath',f'/{bucket}')
    
    
    os.system(f'mkdir -p {base_path}')
    cmd = f's3fs {bucket} {base_path} -o passwd_file={passwd} -o use_cache=/tmp'
    
    if DEBUG:
        cmd += ' -o dbglevel=info -f -o curldbg'
        
    Thread(target=os.system, args=(cmd,)).start()
    add_user(authorizer, data, base_path)
