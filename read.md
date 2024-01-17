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

---
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=192.168.0.239 connectport=8000 connectaddress=172.20.195.188
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=192.168.0.239