
from pyftpdlib.authorizers import DummyAuthorizer

def add_user(authorizer: DummyAuthorizer, data: dict, base_path: str = '/'):
    username = data.get('user')
    password = data.get('pass')
    authorizer.add_user(username, password, base_path, perm="elradfmwMT")

