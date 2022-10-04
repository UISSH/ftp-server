## config

Basic configuration 

> **passive_transfer_port_range** is not supported.

For the configuration content of accesses, please read the file containing the "Config" name.

```json
{
  "version": 1,
  "listen_address": "0.0.0.0:21",
  "passive_transfer_port_range": {
    "start": 2122,
    "end": 2130
  },
  "tls": {
    "server_cert": {
      "cert": "cert.pem",
      "key": "key.pem"
    }
  },

  "accesses": [
    {    
        "user": "test",
        "pass": "test",
        "fs": "os",
        "params": {
            "basePath": "/tmp"
        }
    }
  ]
}
```