from shapely.geometry import shape, Point
import requests
import json
import time
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CITYDICT_FILE = './data/city_dict.json'
CITYDICT_FILE = os.path.join(PROJECT_DIR, CITYDICT_FILE)
BOUNDARY_PATH = './data/city_boundary'
BOUNDARY_PATH = os.path.join(PROJECT_DIR, BOUNDARY_PATH)

# 下载json文件到指定路径
def download_json(code, path):

    # 判断文件是否存在，避免重复下载
    if os.path.exists(f"{path}/{code}.json"):
        return True
        
    # 如果不存在则下载
    url = f"https://geo.datav.aliyun.com/areas_v3/bound/{code}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(f"{path}/{code}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            return True
    
    return False
                
class GeoPi:
    
    def __init__(self):
    
        if not os.path.exists(CITYDICT_FILE):
            # Download city_dict.json from github automatically
            pass
        
        self.city_data = None
        with open(CITYDICT_FILE, 'r', encoding='utf-8') as f:
            self.city_data = json.load(f)
            
        if not os.path.exists(BOUNDARY_PATH):
            os.makedirs(BOUNDARY_PATH)

        # 加载所有省的边界数据，用于加速查询
        self.boundary_kv_cache = {}
        for province in self.city_data:
            province_code = province['code']
            province_data = self.get_boundary_data(province_code)
            if province_data != None:
                self.boundary_kv_cache[province_code] = province_data

    def download_boundary(self, province_only=False):
        # try to download boundary data
        province_num = len(self.city_data)
        for i, province in enumerate(self.city_data):

            # 获取省级行政区边界
            province_name = province['name']
            province_code = province['code']
            print(f"\r{i+1}/{province_num} {province_name} {province_code} is downloading")
            download_json(province_code, BOUNDARY_PATH)

            if province_only:
                continue

            # 遍历市级行政区边界
            cityList = province['cityList']
            for city in cityList:
                city_code = city['code']
                download_json(city_code, BOUNDARY_PATH)

                # 遍历县级行政区边界
                areas = city['areaList']
                for area in areas:
                    area_code = area['code']
                    ret = download_json(area_code, BOUNDARY_PATH)
                    print("✔" if ret else "✖", end="")

            print("")

        print("Download finished")

    # 通过区域编码，从KV库中查询区域边界
    def get_boundary_data(self, code):
        if code not in self.boundary_kv_cache:
            try:
                with open(f"{BOUNDARY_PATH}/{code}.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    features = data['features']
                    return shape(features[0]['geometry'])
            except FileNotFoundError as e:
                if download_json(code, BOUNDARY_PATH):
                    return self.get_boundary_data(code)
        else:
            return self.boundary_kv_cache[code]
        return None
    
    # 判断位置点是否在指定编码的区域内
    def is_point_in_region(self, pt, code):
        bound = self.get_boundary_data(code)
        if bound != None:
            if pt.within(bound):
                return True
        return False

    def city_search(self, lat, lng):
        
        pt = Point(lat, lng)

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
                        for area in areas:
                            area_code = area['code']
                            if self.is_point_in_region(pt, area_code):

                                return {
                                    'province': [province['name'], province_code],
                                    'city': [city['name'], city_code],
                                    'area': [area['name'], area_code]
                                    }
        return None


if __name__ == '__main__':
    geopi = GeoPi()

    start_time = time.time()
    ret = geopi.city_search(118.79, 32.06)
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000
    print(f"Executed in {elapsed_time:.2f} ms")

    print(ret)
