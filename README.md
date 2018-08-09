# RedisClient  
Read only web client for standalone and cluster redis.

### Run
1. `cd $RedisClient_Home`
2. `pip3 install -r requirements.txt`
3. `python3 manage.py runserver 0.0.0.0:8000 #default 8000`

### Log On  
1. ip:port  
192.168.1.104:6379  
2. ip:port:password  
192.168.1.104:6379:secret  
3. keys  
When you log on successfully, all keys in the redis db0 will be cached in `client.js`, the variable named `raw_keys`.  

### Search  
1. keywords  
You can use keywords instead of redis key to search from redis, in fact from the cached `raw_keys`.  
2. up to date  
As you know, all keys was cached in the `raw_keys`, so, if you want to see all the newest keys, please click Log On button again.  

### Value  
1. key  
If you click the key, the returned value will be newest because of real-time communication with redis server.  
2. returned  
Key: key, Type: datatype of key, Length: length of returned string, Size: `sys.getsizeof(key)`, Value: value of key and shown as Text and Json

### Docker
1. `docker pull nandy/redisclient`
2. `docker run -d -p 8000:8000 nandy/redisclient`
4. View http://your ip:8000 to use.
3. Go to [Docker Hub](https://hub.docker.com/r/nandy/redisclient/) for more details.

### Others  
1. framework  
python(3.6.5), django(2.0.2), jquery(3.2.1, js, ECMAScript6), spectre(0.5.3 css)
2. read only  
Some of redis server was not protected by password or firewall, if the anonymous, meaning unsafe or inexpert, logs on redis server via the web RedisClient, some baleful or unconscious operations may be a disaster..., so, read only.