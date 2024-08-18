from geopi import GeoPi
import time

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