# RedisClient  
一个通过浏览器即可查看数据的Redis客户端，支持单机、集群查询。
![example.png](https://github.com/nloneday/RedisClient/blob/master/example.png)

### 运行
1. `cd $RedisClient_Home`
2. `pip3 install -r requirements.txt`
3. `python3 manage.py runserver 0.0.0.0:8000 #default 8000`
4. 浏览器登录`http://your-ip:8000`使用

### 登录 
1. host:port  
192.168.1.104:6379，展开更多可设置password、db。
2. 成功  
登录成功之后，Redis的所有KEYS都会被读取至页面缓存并展示。

### 检索 
1. keywords  
可通过关键字模糊检索，不区分大小写。检索不会与服务器交互，通过前端缓存获得。
2. 服务器KEYS变动  
因为在登录成功后，所有KEYS都会在前端缓存，所以要查询最新的KEYS，点击登录一次即可。
  

### K-V  
1. key  
点击左侧列表即可查询K-V，每一次查询都是从服务器获取最新值。
2. 返回值 
Key: key, Type: 数据类型, Size: 通过sys.getsizeof(key)获取内存大小, Value: 通过`Json, Text`形式展示

### Docker
1. `docker pull nandy/redisclient`
2. `docker run -d -p 8000:8000 nandy/redisclient`
4. 浏览器登录`http://your-ip:8000`使用
3. Go to [Docker Hub](https://hub.docker.com/r/nandy/redisclient/) for more details.

### 其他  
1. 框架  
python(3.6.5), django(2.0.8), jquery(3.2.1, js, ECMAScript6), spectre(0.5.3 css)
2. 只读？   
一些Redis服务器没有设置密码或防火墙，如果提供写操作以免误操作或恶意攻击。
