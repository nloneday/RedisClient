# RedisClient  
一个通过浏览器查看`Redis`数据的客户端，支持单机、集群查询。
![example.png](https://github.com/nloneday/RedisClient/blob/master/example.png)
---
### 运行
- [x] 本机
- `git clone https://github.com/nloneday/RedisClient.git`
- `cd $RedisClient_Home`  
- `pip3 install -r requirements.txt`  
- `python3 manage.py runserver 0.0.0.0:8000 #default 8000`


- [x] 容器
- `docker pull nandy/redisclient`
- `docker run --name redisclient --restart always -d -p 8000:8000 nandy/redisclient`


- [ ] 访问
- `http://your-host:8000`

---
### 登录 
- 选择`standalone, cluster`，填写`host:port(192.168.1.104:6379)`，点击`===`展开更多设置`password, db`。
- 登录成功之后，所有`KEYS`将以列表形式展示在页面左侧，同时在`JS`中缓存。

---
### 检索 
- 通过关键字（不区分大小写）模糊检索，但检索是在`JS`缓存中而不是在`Redis`服务器中进行筛选。
- 登录成功之后，所有`KEYS`都在`JS`中缓存，所以要获取最新的`KEYS`，点击重新登录一次即可。

---
### 键值 
- 点击页面左侧列表即可查询键值，键值查询每次都是从`Redis`服务器中获取。
- 只有`HASH`类型会显示二级`KEYS`，点击下方`Go Back`可切换回正常模式。
- 查询结果额外信息：`Key`：键, `Type`：数据类型。
- `Value`：值，可选择`Json, Text`形式展示。

---
### 其他  
- 框架，`python(3.6.5), django(2.0.8), jquery.js(3.2.1), spectre.css(0.5.3)`。
- 一些Redis服务器没有设置密码、防火墙、堡垒机等保护措施，如果提供写操作可能会引发误操作或恶意攻击等严重后果。
