# GeoPi=3.14!

 面向中国的时空位置数据处理工具包

[Github链接地址](https://github.com/KaffeeCat/geopi)
[pypi.org链接地址](https://test.pypi.org/project/geopi/0.0.1/)

## 安装

```bash
pip install -i https://test.pypi.org/simple/ geopi
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
```

输出经纬度坐标所在为支点：

```python
{
    'province': ['江苏省', '320000'], 
    'city': ['南京市', '320100'], 
    'area': ['玄武区', '320102']
}
```