# https://pyftpdlib.readthedocs.io/en/latest/tutorial.html#debug-logging
import argparse
import json
import os
import pathlib

import logging


from pyftpdlib.authorizers import DummyAuthorizer

from src.ftp_server.s3 import cleanup_s3, load_s3
from src.ftp_server.os import load_os

from pyftpdlib.servers import FTPServer


CONFIG = {}

CONFIG_PATH = pathlib.Path(__file__).parent / 'config.json'
DEBUG = os.environ.get('debug', False)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

LOAD_METHOD = {'s3': load_s3, 'os': load_os}


def get_authorizer() -> DummyAuthorizer:
    authorizer = DummyAuthorizer()
    accesses = CONFIG.get('accesses', [])

    for i in accesses:
        fs = i['fs']
        if fs in LOAD_METHOD:
            LOAD_METHOD[fs](authorizer, i)
        else:
            logging.warning(f'{fs} file system is not supported.')

    # authorizer.add_user("user", "12345", "/home/giampaolo", perm="elradfmwMT")
    # authorizer.add_anonymous("/home/nobody")
    return authorizer


def get_server() -> FTPServer:
    authorizer = get_authorizer()

    ssl_config = CONFIG.get(
        'tls', {"server_cert": {"cert": "cert.pem", "key": "key.pem"}}).get('server_cert')
    cert = pathlib.Path(ssl_config['cert'])
    key_pem = pathlib.Path(ssl_config['key'])
    if cert.exists() and key_pem.exists():
        from pyftpdlib.handlers import TLS_FTPHandler
        handler = TLS_FTPHandler
        handler.certfile = cert.__str__()
        handler.keyfile = key_pem.__str__()
        handler.tls_control_required = True
        handler.tls_data_required = True
    else:
        from pyftpdlib.handlers import FTPHandler
        handler = FTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 65535)
    address = CONFIG.get('listen_address', '127.0.0.1:2121').split(":")

    return FTPServer(tuple(address), handler)


def init() -> FTPServer:
    return get_server()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=f'Ftp server.')
    parser.add_argument("--config", type=str,
                        required=False, help="config.json")
    parser.add_argument("-t",  action="store_true")
    args = parser.parse_args()
    config = args.config

    if args.config:
        CONFIG_PATH = pathlib.Path(args.config)

    CONFIG = json.loads(CONFIG_PATH.read_text())

    server = init()
    if args.t:
        print(
            f"ftp-server: configuration file {CONFIG_PATH} test is successful")
        exit(0)
    server.serve_forever()
    
    # cleanup
    cleanup_s3()
    
