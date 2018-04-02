### ucloud api

[官方文档地址](https://docs.ucloud.cn/index)

### 用法


#### 初始化实例
# 用户密码认证
```python
    from Ucloud import Ucloud
    uc = Ucloud(<EMAIL>, <PASSWORD>)
	# d登录
    uc.login()
```
# key方式认证
    from Ucloud_key import Ucloud
    uc = Ucloud(<PUBLIC_KEY>, <PRIVATE_KEY>)
	# d登录
    uc.login()


#### 直接传参数
参数参考ucloud api 官方文档
```python
    rev = uc.DescribeUHostInstance(ProjectId=<PROJECT_ID>, Region=<REGION>, Offset=0, Limit=10)
    print rev
```
#### 以字典为参数
```python
    params = {'ProjectId': <PROJRECT_ID>, 'Region': <REGION>, 'Offset': 0, 'Limit': 10}
    rev = uc.DescribeUHostInstance(params)
    print rev
```

