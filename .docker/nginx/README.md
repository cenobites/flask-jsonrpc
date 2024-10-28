# nginx

### Creating the SSL Certificate

```
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/nginx-ssl.key -out ssl/nginx-ssl.crt
$ openssl dhparam -out ssl/ssl-dhparam.pem 4096
```

### Creating Root CA and Domain Certifications

See [here](https://github.com/FiloSottile/mkcert#installation) how to install mkcert.
```
$ mkcert -install
$ mkcert -key-file ssl/flask-jsonrpc.cenobit.es.key -cert-file ssl/flask-jsonrpc.cenobit.es.crt '*.flask-jsonrpc.cenobit.es'
$ cp -rf "$(mkcert -CAROOT)/rootCA.pem" ../certs/Cenobit_Root_CA.pem
```
