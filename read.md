---
to run start docker
docker run --rm -p 6379:6379 redis:7
and 
python3 manage.py runserver
---
pip install -U channels["daphne"]
pip install python-dotenv
pip install channels_redis
pip install pymongo[snappy,gssapi,srv,tls]