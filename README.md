## start:dev

```bash
$ uvicorn app.main:app --reload --log-level=debug
```

## setup
```bash
pip install fastapi 'uvicorn[standard]' 'databases[postgresql]' 

# oauth 2.0
$ pip install python-multipart 'python-jose[cryptography]' 'passlib[bcrypt]'

# dev sqlite
$ pip install 'databases[sqlite]'

$ openssl rand -hex 32
```