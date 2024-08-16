# geopi
 时空位置数据处理工具包

[GeoPi on Github](https://github.com/KaffeeCat/geopi)

## 安装

```bash
pip install geopi
```

## 使用

```python
from geopi import GeoPi

geopi = GeoPi()

# 设置要查询的经纬度坐标
lat = 118.79
lng = 32.06

# 获取地址
ret = geopi.city_search(118.79, 32.06)
print(ret['province'][0])
print(ret['city'][0])
print(ret['area'][0])
