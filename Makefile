init:
	apt install  s3fs python3-venv -y
	python3 -m venv venv
	rm -rf /etc/systemd/system/ftp_server.service /etc/systemd/system/ftp-server.service
	venv/bin/pip install -U pip wheel setuptools
	venv/bin/pip install -r requirements.txt
	cp example.config.json config.json 
	openssl req -new -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out cert.pem  -keyout key.pem -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=uissh.com"

install:
	cp ftp-server.service /lib/systemd/system/ftp-server.service
	ln -s /lib/systemd/system/ftp-server.service  /etc/systemd/system/ftp-server.service
	systemctl daemon-reload
	systemctl enable --now ftp-server