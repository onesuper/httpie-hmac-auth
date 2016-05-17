Auth plugin for debugging ODPS API with [httpie](https://github.com/jkbrzt/httpie)

### Usage

```bash
$ git clone <repo>
$ python setup.py install
$ http -v  --auth-type=hmac --auth="{{access_id}}:{{access_key}}" GET {{endpoint}}/projects/project_name
```
