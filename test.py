import pymongo
import math
import copy

connection = pymongo.Connection('localhost',27017)
db = connection.weather
temperature = db.temperature

# gets the next number in a sequence
def getRange(lat , lon , distance):
    PI = 3.14159265359
    DEF_R = 6370693.5
    radius = DEF_R

    lat = lat * PI /180
    lon = lon * PI /180
    rad_dist = distance / radius
    lat_min = lat - rad_dist
    lat_max = lat + rad_dist

    if(lat_min > -PI/2 and lat_max < PI/2):
        lon_t = math.asin( math.sin(rad_dist) / math.cos(lat) )
        lon_min = lon - lon_t
        if lon_min < -PI:
            lon_min = 2 * PI +lon_min
        lon_max = lon + lon_t
        if lon_max > PI:
             lon_max = 2 * PI - lon_max

    else:
        lat_min = max (lat_min , -PI/2)
        lat_max = min (lat_max, PI/2)
        lon_min = -PI
        lon_max = PI

    lat_min = lat_min * 180 / PI
    lat_max = lat_max * 180 / PI
    lon_min = lon_min * 180 / PI
    lon_max = lon_max *180 / PI
    print(lat_max, lat_min, lon_max, lon_min)
    result = (lat_max, lat_min, lon_max, lon_min)
    return result

def getLAT_AND_LON(city):

    result = temperature.find_one({"STATION_NAME":city})
    latitude = result["LATITUDE"]
    longitude = result["LONGITUDE"]
    
    return (latitude,longitude)

def get_average_temperature(Range,earliest,latest):

    i = latest - earliest
    tmpMax = 0
    tmpMin = 0
    count1 = 0
    x = 0
    flag =0

    cityInfo = []
    citynum = temperature.find({"LATITUDE" : {'$gt': Range[1], '$lt': Range[0]}, "LONGITUDE" : {'$gt':Range[3], '$lt': Range[2]}, "DATE" : {'$gt': earliest, '$lt': latest}}).count()
    row = [0]*3
    cityInfo.append(copy.copy(row))
   
 
    for result in temperature.find({"LATITUDE" : {'$gt': Range[1], '$lt': Range[0]}, "LONGITUDE" : {'$gt':Range[3], '$lt': Range[2]}, "DATE" : {'$gt': earliest, '$lt': latest}}):
 
        tmp = temperature.find({"STATION_NAME": result["STATION_NAME"]}).count()
        tmpHigh = tmp
        tmpLow = tmp
        
        #for count in range(tmp):
        if result["TMAX"] != "-9,999":
            tmpMax = int(result["TMAX"]) + tmpMax
        else:
            tmpHigh = tmpHigh - 1
        if result["TMIN"] != "-9,999":
            tmpMin = int(result["TMIN"]) + tmpMin
        else:
            tmpLow = tmpLow - 1
        if flag == 0:
            cityInfo[count1][0] = result["STATION_NAME"]
            flag =1
        if count1 ==0 and result["STATION_NAME"] != cityInfo[count1][0]:
            cityInfo[count1][1] = str(tmpMax/tmpHigh)
            cityInfo[count1][2] = str(tmpMin/tmpLow)
            tmpMax = 0
            tmpMin = 0
            count1 = count1+1
            cityInfo.append(copy.copy(row))
            cityInfo[count1][0] = result["STATION_NAME"]
            continue
        if count1 != 0 and result["STATION_NAME"] != cityInfo[count1-1][0]:
            cityInfo.append(copy.copy(row))
            cityInfo[count1][0] = result["STATION_NAME"]
            cityInfo[count1][1] = str(tmpMax/tmpHigh)
            cityInfo[count1][2] = str(tmpMin/tmpLow)
            tmpMax = 0
            tmpMin = 0
            count1 = count1+1       

  

    return cityInfo

def createArray(m,n):
    
 
    return cityInfo
            
def get_sutable_cities(AVER_TEMP,MAXT,MINT):
    return 0
    
central_city = raw_input("please input central city's name :")
LAT_AND_LON = getLAT_AND_LON(central_city)
distance = raw_input("please input limit of distance :")
distance = float(distance)
Range = getRange(LAT_AND_LON[0], LAT_AND_LON[1], distance)
earliest = int(raw_input("please input earliest date:"))
latest = int(raw_input("please input latest date:"))
MAX_TEMP = float(raw_input("please input MAX temperature that you can tolerate :"))
MIN_TEMP = float(raw_input("please input MIN temperature that you can tolerate :"))
AVER_TEMP = get_average_temperature(Range,earliest,latest)
sutable_cities = get_sutable_cities(AVER_TEMP,MAX_TEMP,MIN_TEMP)

print("Sutable cities are: \n")
#for city in sutable_cities:
#    print(city)

print("\n\n other cities' information :\n")
for item in AVER_TEMP:
    print(item)
