## start:dev

```bash
$ uvicorn src.asgi:app --host 127.0.0.1 --port 8000
```

## setup
```bash
pip install fastapi 'uvicorn[standard]' 'databases[postgresql]' 

# oauth 2.0
$ pip install python-multipart 'python-jose[cryptography]' 'passlib[bcrypt]' itsdangerous

# dev sqlite
$ pip install 'databases[sqlite]'

$ openssl rand -hex 32
```

## `2LO`(Kakao)

## `3LO`(Google)

## refs

- [landlords-server](https://github.com/Nexters/landlords-server/)