# GeoPi=3.14!

![](https://cdn.icon-icons.com/icons2/1144/PNG/96/pinumber1_80899.png)

 #### 面向中国的时空位置数据处理工具包

 离线环境下，无需联网，即可快速获取地理坐标点（经纬度）所在位置点（省市区县），查询速度毫秒级。

[:octocat: Github链接地址](https://github.com/KaffeeCat/geopi)

[:rocket: pypi.org链接地址](https://test.pypi.org/project/geopi/0.0.1/)


## 功能

获取地理坐标点（经纬度）所在位置点（省市区县）
> 中国地区数据来源于阿里云DataV.GeoAtlas，确保地理数据的准确性，地图坐标系采用高德坐标系。

## 安装

```bash
pip install geopi
```
或者

```bash
pip install geopi -i https://test.pypi.org/simple/
```

## 使用

```python
from geopi import GeoPi

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat = 118.79
lng = 32.06

# 获取所在地址
ret = geopi.city_search(lat, lng)
print(ret)
```

输出经纬度坐标所在位置点（省市区县）：

```python
{
    'province': ['江苏省', '320000'], 
    'city': ['南京市', '320100'], 
    'area': ['玄武区', '320102']
}
```