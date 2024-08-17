# GeoPi=3.14!

![](https://cdn.icon-icons.com/icons2/1144/PNG/96/pinumber1_80899.png)

 #### 面向中国的时空位置数据处理工具包

 可在离线环境下，无需联网，即可快速获取地理坐标点（经纬度）所在位置点（省市区县），查询速度毫秒级。

:octocat: [Github链接地址](https://github.com/KaffeeCat/geopi)

:rocket: [pypi.org链接地址](https://pypi.org/project/geopi/)

:alien: [test.pypi.org链接地址](https://test.pypi.org/project/geopi/)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![PyPI](https://img.shields.io/pypi/v/geopi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geopi)
![PyPI - Downloads](https://img.shields.io/pypi/dd/geopi)
![PyPI - License](https://img.shields.io/pypi/l/geopi)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/geopi)

## 1. 功能

获取地理坐标点（经纬度）所在位置点（省市区县）
> 中国地区数据来源于阿里云DataV.GeoAtlas，确保地理数据的准确性，地图坐标系采用高德坐标系。

## 2. 安装

```bash
pip install geopi
```
或者

```bash
pip install geopi -i https://test.pypi.org/simple/
```

## 3. 使用

```python
from geopi import GeoPi

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 118.79, 32.06

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

## 4. 可视化

首先确保安装了GeoPandas，你可以通过下面命令进行安装
```bash
pip install geopandas
```

以下代码围绕第3节中经纬度坐标查询所在区域的例子，进一步进行地图可视化：

```python

from geopi import GeoPi
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 118.79, 32.06

# 获取所在地址
ret = geopi.city_search(lat, lng)

# 获取经纬度坐标所在区域的边界数据
province_boundary = geopi.get_boundary_data(ret['province'][1])
city_boundary = geopi.get_boundary_data(ret['city'][1])
area_boundary = geopi.get_boundary_data(ret['area'][1])

gdf = GeoDataFrame({'geometry': [province_boundary, city_boundary, area_boundary]}, index=['province', 'city', 'area'])
ax = gdf.plot(color=['#4A90E2', '#50E3C2', '#B8E986'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Boundary of China')

# 在地图上绘制经纬度位置点
plt.scatter(lat, lng, color='#D2691E', marker='*', s=100, zorder=10, label='Location')
ax.legend()
plt.show()

```
![boundary](https://raw.githubusercontent.com/KaffeeCat/geopi/main/images/visualize.png)