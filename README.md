# RedisClient  
Read only client for standalone and cluster redis in risk of security.   
  
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
  
### Others  
1. framework  
python3.6.5, django, jquery(js), spectre(css)  
2. read only  
Some of redis server was not protected by password or firewall, if the anonymous, meaning unsafe or inexpert, logs on redis server via the web RedisClient, some baleful or unconscious operations may be a disaster..., so, read only.  