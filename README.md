## start:dev

```bash
$ uvicorn main:app --reload
```

## setup
```bash
pip install fastapi 'uvicorn[standard]' 'databases[postgresql]' 

# oauth 2.0
$ pip install python-multipart 'python-jose[cryptography]' 'passlib[bcrypt]'
$ openssl rand -hex 32
```