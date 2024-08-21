import geopandas as gpd
from shapely.geometry import shape, Point
from coord_convert.transform import gcj2wgs, wgs2gcj
from geopy.distance import geodesic
import zipfile
import pyproj
import json
import time
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CITYDICT_FILE = 'data/city_dict.json'
CITYDICT_FILE = os.path.join(PROJECT_DIR, CITYDICT_FILE)
BOUNDARY_PATH = 'data/city_boundary'
BOUNDARY_PATH = os.path.join(PROJECT_DIR, BOUNDARY_PATH)
BOUNDARY_ZIPFILE = os.path.join(BOUNDARY_PATH, "city_boundary.zip")
CITY_SHP_PATH = 'data/city_shp'
CITY_SHP_PATH = os.path.join(PROJECT_DIR, CITY_SHP_PATH)
CITY_SHP_NAME = 'china_poi'
CITY_SHP_FILE = os.path.join(CITY_SHP_PATH, f"{CITY_SHP_NAME}.shp")
CITY_SHP_ZIPFILE = os.path.join(CITY_SHP_PATH, f"{CITY_SHP_NAME}.zip")
                
class GeoPi:
    
    def __init__(self):
        
        self.city_data = None
        with open(CITYDICT_FILE, 'r', encoding='utf-8') as f:
            self.city_data = json.load(f)
            
        if not os.path.exists(BOUNDARY_PATH):
            os.makedirs(BOUNDARY_PATH)

        # 第一次运行是初始化数据文件
        if not os.path.exists(CITY_SHP_FILE):

            # 初始化边界文件
            with zipfile.ZipFile(BOUNDARY_ZIPFILE, 'r') as zip_ref:
                zip_ref.extractall(BOUNDARY_PATH)

            # 初始化SHP文件
            with zipfile.ZipFile(CITY_SHP_ZIPFILE, 'r') as zip_ref:
                zip_ref.extractall(CITY_SHP_PATH)

        # 加载所有省的边界数据，用于加速查询
        self.boundary_kv_cache = {}
        for province in self.city_data:
            province_code = province['code']
            province_data = self.get_boundary_data(province_code)
            if province_data != None:
                self.boundary_kv_cache[province_code] = province_data


        # 创建高德坐标系（GCJ-02）和 WGS84 坐标系的转换对象
        self.gcj_to_wgs = pyproj.Transformer.from_crs(
            "epsg:4490",  # GCJ-02 坐标系的 EPSG 代码
            "epsg:4326",  # WGS84 坐标系的 EPSG 代码
            always_xy=True
        )

    # 通过区域编码，从KV库中查询区域边界
    def get_boundary_data(self, code):
        if code not in self.boundary_kv_cache:
            try:
                with open(f"{BOUNDARY_PATH}/{code}.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    features = data['features']
                    return shape(features[0]['geometry'])
            except FileNotFoundError as e:
                return None
        else:
            return self.boundary_kv_cache[code]
    
    # 判断位置点是否在指定编码的区域内
    def is_point_in_region(self, pt, code):
        bound = self.get_boundary_data(code)
        if bound != None:
            if pt.within(bound):
                return True
        return False

    # 查询经纬度为位置所在的省市区
    def search_city(self, lat, lng):
        
        pt = Point(lng, lat)

        # 先判断在哪个省
        for province in self.city_data:
            province_code = province['code']
            if self.is_point_in_region(pt, province_code):

                # 判断在下属哪个城市
                cityList = province['cityList']
                for city in cityList:
                    city_code = city['code']
                    if self.is_point_in_region(pt, city_code):

                        # 判断在下属哪个区县
                        areas = city['areaList']
                        if len(areas) == 0:
                            return {
                                'province': [province['name'], province_code],
                                'city': [city['name'], city_code],
                                'area': [city['name'], city_code]
                            }
                        else:
                            for area in areas:
                                area_code = area['code']
                                if self.is_point_in_region(pt, area_code):

                                    return {
                                        'province': [province['name'], province_code],
                                        'city': [city['name'], city_code],
                                        'area': [area['name'], area_code]
                                        }
        return None
    
    # 查询经纬度位置附近的POI信息
    def search_nearest_poi(self, lat, lng, topk=10, delta=0.05):

        def transform_geometry(row):
            lat, lng = row.wgs84.y, row.wgs84.x
            gcj_lng, gcj_lat = wgs2gcj(lng, lat)
            return Point(gcj_lng, gcj_lat)
        
        # 转换为 WGS84 坐标系
        wgs_lng, wgs_lat = gcj2wgs(lng, lat)

        # 加载地理数据框
        bbox = (wgs_lng-delta, wgs_lat-delta, wgs_lng+delta, wgs_lat+delta)
        gdf = gpd.read_file(CITY_SHP_FILE, bbox=bbox)
        gdf = gdf[gdf['name'].notnull()]

        # 将 geometry 列转换为 WGS84 坐标系，并转化为 GCJ02 坐标系
        gdf = gdf.rename(columns={'geometry': 'wgs84'})
        gdf['gcj'] = gdf.apply(transform_geometry, axis=1)

        # 计算位置点距离每个POI的距离
        gdf['dist'] = gdf.wgs84.apply(lambda geom: geodesic((wgs_lat, wgs_lng), (geom.y, geom.x)).meters)
        return gdf.nsmallest(topk, 'dist')

if __name__ == '__main__':
    
    geopi = GeoPi()

    lat, lng = 32.043787, 118.797437

    # 查询经纬度为位置所在的省市区
    start_time = time.time()
    ret = geopi.search_city(lat, lng)
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    print(f"Executed in {elapsed_time:.2f} ms")
    print(ret)

    # 查询经纬度位置附近的POI信息
    start_time = time.time()
    ret = geopi.search_nearest_poi(lat, lng, topk=10)
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    print(f"Executed in {elapsed_time:.2f} ms")
    print(ret)