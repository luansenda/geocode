# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 14:51:37 2020

@author: Senda

E-mail: luansenda@buaa.edu.cn
"""
## ------------------------ 地理编码，将经纬度转换为地址-------------------

import requests

#高德地图
def gaode_geocode(location):
    parameters = {'output': 'json', 'location': location, 'key': '您申请的key','extensions':'all'}
    base = 'https://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    answer = response.json()    
    #print('url:' + response.url)
    #print(answer)
    return answer['regeocode']['addressComponent']['province'],answer['regeocode']['addressComponent']['city'],answer['regeocode']['addressComponent']['district']


#百度地图
def baidu_geocode(location):
    parameters = {'location': location, 'output': 'json', 'coordtype': 'wgs84',  'pois': '0', 'latest_admin': '1', 'ak': 'FUu6OTikvprEEwd1qL9X23a9PGq05efW','extensions_road':'true'}
    base = 'http://api.map.baidu.com/geocoder/v2/'
    response = requests.get(base, parameters)
    #print('url:' + response.url)    
    answer = response.json()    
    #print(answer)    
    return answer['result']['addressComponent']['province'],answer['result']['addressComponent']['city'],answer['result']['addressComponent']['district'] 


# example
xtmp = 119.37649
ytmp = 39.88686

province,city,district = gaode_geocode(str(xtmp)+','+str(ytmp)) ## 高德：配额受限
print(province,city,district)

province,city,district = baidu_geocode(str(ytmp)+','+str(xtmp))
print(province,city,district)


## ------------------------- 逆地理编码，把地址转换为经纬度 ---------------------
def geocode(address):
    parameters = {'address': address, 'key': '您申请的key'}
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    response = requests.get(url, parameters)
    # answer = response.geocodes['location']
    # print(answer)
    answer = response.json()
    if answer['count'] == str(1):
        print(address + "的经纬度：", answer['geocodes'][0]['location'])
        location = answer['geocodes'][0]['location'].split(',')
        lat = float(location[1])       #纬度
        lng = float(location[0])       #经度
    return [lng,lat]

## ------------------------ 获取公交线路站点信息 ------------------------
"""
按关键字查线路,返回所有相关线路，如‘300路’：返回‘300路快外’，‘300路快内’，‘300路外环’，‘300路内环’
然后依次遍历每条线路，获取站点信息，经纬度为高德坐标系
"""

line_name = []
stop_name = []
lng = []
lat = []

import requests

def busstations(lineID):
    # 服务接口，其中city对应城市编号
    url = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=010&keywords=' + lineID + '%E8%B7%AF'
    json_obj = requests.get(url)
    
    data = json_obj.json()
    if (data["data"]["message"]) and (data["data"]["busline_list"]):
        buslines = data["data"]["busline_list"]  # busline列表
        #return buslines  # 选择方向        
    
    for line in buslines:
        buslinename = line["name"]
        stations = line["stations"]
        for station in stations:
            line_name.append(buslinename)
            stop_name.append(station["name"])
            lng.append(float(station["xy_coords"].split(";")[0]))
            lat.append(float(station["xy_coords"].split(";")[1]))
    return [line_name,stop_name,lng,lat]

## 调用，查询
stations_loc = busstations('300路') # '300'也可以

"""
注意：如果要查询多个线路，用循环多次执行busstations()函数即可，最终结果都append到前面定义的四个list中了
"""                          
                          
                          
## 最后把所有查询结果保存本地csv
import pandas as pd
data = {"lineName":stations_loc[0],
        "stopName":stations_loc[1],
        "lng":stations_loc[2],
        "lat":stations_loc[3]}
data = pd.DataFrame(data) # 字典转dataframe，列顺序会混乱
data = data[["lineName","stopName","lng","lat"]] # 重新排列
data.to_csv(r'C:\Users\Administrator\Desktop\stop_loc.csv',header=True,index=False)









