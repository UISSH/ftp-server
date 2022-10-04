from pyftpdlib.authorizers import DummyAuthorizer
from src.ftp_server.helper import add_user

def load_os(authorizer: DummyAuthorizer, data: dict):
    """
    :param authorizer
    :param data: {'fs': 'os',
               'params': {'basePath': '/'},
               'pass': 'test',
               'user': 'test'}
    """
    base_path = data.get('params').get('basePath')
    add_user(authorizer, data, base_path)