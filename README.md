# GeoPi = 3.14!

![](https://cdn.icon-icons.com/icons2/1144/PNG/96/pinumber1_80899.png)


![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![PyPI](https://img.shields.io/pypi/v/geopi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geopi)
![PyPI - Downloads](https://img.shields.io/pypi/dd/geopi)
![PyPI - License](https://img.shields.io/pypi/l/geopi)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/geopi)


 #### 面向中国的时空位置数据处理工具包

在分析时空位置数据时，逆向地理编码（也称为逆地址编码、逆地址解析）是一项频繁使用且非常重要的能力，它可以将地理位置的经纬度坐标（Latitude, Longitude）转化为用户易于理解的地址描述信息，如下所示：

#### WHERE IS THIS PLACE ? = f(LATITUDE, LONGITUDE)

但是，业内各大地图厂商推出的逆地理位置编码基本都属于收费能力，或者每日有免费的使用次数上限，亦或者是必须接入互联网调用网络API进行查询。

有没有一个无限次数、无需网络、开箱即用的开源逆向地理编码库呢？

# Yes! Its [GeoPi](https://pypi.org/project/geopi/) !

## 1. 安装

你只需稍稍出手 😎

```bash
pip install geopi
```

它就可以轻松安装到你的电脑，包括其内置的中国区位置数据：

- 地图坐标系采用GCJ02坐标系，也被称为火星坐标系（Mars coordinate system），是中国国家标准的地理坐标系统，用于网络地图服务。该坐标系统是由中国国家测绘地理信息局（现国家测绘地理信息局）开发，主要应用于中国大陆地区；
- 中国区数据来源于阿里云DataV.GeoAtlas，确保地理位置数据的准确性；
POI数据来源于OSM的中国地图数据，且坐标系已经从WGS84转换为GCJ02坐标系，确保位置数据与POI数据坐标系的一致性；

## 2. 查询位置点所在地省/市/区(县)

只需一个函数，即可快速查询位置经纬度坐在的区域

```python
from geopi import GeoPi

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 32.043787, 118.797437

# 获取所在地址
ret = geopi.search_city(lat, lng)
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

## 3. 查询位置所在区域的可视化展示

GeoPi内置了全国所有省市区的地理空间位置信息，通过 geopi.get_boundary_data(province_code) 函数，既可以获得对应行政区域编码的几何边界信息，结合GeoPandas和Matplotlib，可以轻松对位置及所在区域进行上图可视化

```python

from geopi import GeoPi
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 32.043787, 118.797437

# 获取所在地址
ret = geopi.search_city(lat, lng)

# 获取经纬度坐标所在区域的边界数据
province_boundary = geopi.get_boundary_data(ret['province'][1])
city_boundary = geopi.get_boundary_data(ret['city'][1])
area_boundary = geopi.get_boundary_data(ret['area'][1])

gdf = GeoDataFrame({'geometry': [province_boundary, city_boundary, area_boundary]}, index=['province', 'city', 'area'])
ax = gdf.plot(color=['#4A90E2', '#50E3C2', '#B8E986'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Boundary of Province/City/Area')

# 在地图上绘制经纬度位置点
plt.scatter(lng, lat, color='#D2691E', marker='*', s=100, zorder=10, label='Location')
ax.legend()
plt.show()

```

输出地图如下所示，红色五角星为查询的位置处，同时将所在的省市区区域也进行了绘制：

![boundary](https://picx.zhimg.com/80/v2-2c6be5556643541cb83b29e009ea3879_720w.png?source=d16d100b)

## 4. 查询位置点附近的POI信息

POI是“Point of Interest”的缩写，中文意思是“兴趣点”或“兴趣地点”。在地理信息系统（GIS）和位置服务中，POI指的是具有特定地理坐标的地点或对象，这些地点通常对人们有特定的意义或用途，例如餐馆、电影院、博物馆、公园、历史地标等。

GeoPi内置了全国所有常见的POI地理位置信息，通过 geopi.search_nearest_poi(lat, lng, topk) 函数，可以快速查询位置点附近Top K条POI位置数据：

```python
from geopi import GeoPi

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 32.043787, 118.797437

# 查询经纬度位置附近的POI信息
ret = geopi.search_nearest_poi(lat, lng, topk=10)

```

POI查询输出信息如下所示：

![pois](https://pic1.zhimg.com/80/v2-df0d34662debe287f9de00b3d60a1390_720w.png?source=d16d100b)

其中，fclass为POI的类型，name为POI名称，wgs84和gcj为POI在不同坐标系的坐标点经纬度坐标，dist为距离查询位置点的距离，距离单位为米(Meters)。

## 5. 通过folium对查询位置及附近的POI进行可视化

结合folium库对查询位置和附近POI在地图上进行绘制，通过可视化，可以帮助用户快速找到目的地，并了解周边环境。

```python
from geopi import GeoPi
import folium

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat, lng = 32.043787, 118.797437

# 查询经纬度位置附近的POI信息
ret = geopi.search_nearest_poi(lat, lng, topk=10)

map = folium.Map(location=[lat, lng], 
           tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
           attr='高德-中英文对照',
           zoom_start=15)

folium.Marker(location=[lat, lng], icon=folium.Icon(color='red')).add_to(map)

for index, row in ret.iterrows():
    pt = row['gcj']
    folium.Marker(location=[pt.y, pt.x], icon=folium.Icon(color='blue'), popup=row['name']).add_to(map)
map
```

查询位置附近POI可视化如下图所示：

![pois](https://picx.zhimg.com/80/v2-e73b4fb530d2d22a36c47b69b0b47b9c_720w.png?source=d16d100b)


##### 如果你觉得这个项目很赞，请不要吝啬你的小星星Star哦，谢谢 :smile: 
