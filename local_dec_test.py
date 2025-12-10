import numpy as np
from lut import NL
from haversine import haversine,Unit
def local_decoding(lat_r,lon_r,lat,lon,i):## itt lat lon már 0-1 közti érték kell legyen
    if lat > 2:
        lat = lat/(2**17)
    if lon > 2:
        lon = lon/(2**17)
    
    dLat = 360/(4*15-i)
    j = np.floor(lat_r/dLat)+ np.floor((np.mod(lat_r,dLat)/dLat)-lat+0.5) 
    latitude_ = dLat*(j+lat)
    dLon = 360/(max(NL(lat)-i,1))
    m = np.floor(lon_r/dLon)+ np.floor((np.mod(lon_r,dLon)/dLon)-lon+0.5)
    longitude_ = dLon*(m+lon)
    pos = dict(latitude = latitude_,longitude = longitude_)
    
    ref = (lat_r,lon_r)
    actual = (latitude_,longitude_)
    dist = haversine(ref,actual,unit=Unit.NAUTICAL_MILES)
    if dist > 180:
        eredmeny = 0
    else:
        eredmeny = 1 
    return pos