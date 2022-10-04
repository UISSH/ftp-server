# QuickStart

![CI](https://github.com/uissh/ftp-server/actions/workflows/test_install.yml/badge.svg)

This project is one of UISSH-backend suites.

## Feature

This is an ftp server developed based on [pyftpdlib]([pyftpdlib](https://github.com/giampaolo/pyftpdlib)). through it, the following file systems can be accessed through the ftp interface.

 - [x] Local file system
 - [x] S3 object
 - [ ] FTP(S)
 - [ ] SFTP
 - [ ] OSS object

## Install


```bash
cd /usr/local/uissh/
git clone https://github.com/UISSH/ftp-server.git

cd ftp-server
make
make install
```

## Test

```bash
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out cert.pem  -keyout key.pem -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=uissh.com"
cp example.config.json config.json 
pip install -r requirements.txt
python3 ftpserver.py
```