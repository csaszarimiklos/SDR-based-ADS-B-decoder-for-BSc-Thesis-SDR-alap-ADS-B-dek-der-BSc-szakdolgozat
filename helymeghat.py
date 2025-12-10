from functions import decoder
from lut import position
from collections import defaultdict
"""
def coordinates_jo(messages):
    class plane_pos:
        def __init__(self, icao_, lat_cpr_,lon_cpr_,cpr_):
            self.icao = icao_
            self.lat_cpr = lat_cpr_
            self.lon_cpr = lon_cpr_
            self.cpr = cpr_
        def print_(self):
            print(self.icao,self.lat_cpr,self.lon_cpr,self.cpr)
    planes = list()

    for i in messages:
        typecode,cap,icao,mess = decoder(i)
        if (9 <= typecode <= 18) or (20 <= typecode <= 22):
            print(typecode,icao,mess[3])
            planes.append(plane_pos(icao,mess[1],mess[2],mess[3]))

    class full_pos():
        def __init__(self,icao_,lat_e_,lon_e_,lat_o_,lon_o_,cntr):
            self.icao = icao_  
            self.lat_e = lat_e_  
            self.lon_e = lon_e_
            self.lat_o = lat_o_
            self.lon_o = lon_o_
            self.cntr = cntr
        def print_(self):
            print(self.icao,self.lat_e,self.lon_e,self.lat_o,self.lon_o)
    full_posik = list()

    class referencia():
        def __init__(self,lat,lon):
            self.lat = lat  
            self.lon = lon
        def __repr__(self):
            return (f"referencia("
                    f"lat_e={self.lat}, "
                    f"lon_e={self.lon}, ")
    from collections import defaultdict 

    ref_helyek = defaultdict(referencia)
    coordinates = list()

    counter = 1
    i = len(planes)-1

    while i >= 0:
        j = i-1
        if (planes[i].icao) in ref_helyek: # van ref
            eredmeny = local_decoding(ref_helyek[planes[i].icao].lat,ref_helyek[planes[i].icao].lon,planes[i].lat_cpr,planes[i].lon_cpr,planes[i].cpr,icao=planes[i].icao,cntr=counter)
            if eredmeny[2] == 1: 
                eredmeny_ = (eredmeny[0],eredmeny[3],eredmeny[4])
                
                print("Van ref, local decoding eredménye: ", eredmeny_)
                
                coordinates.append(eredmeny_)
                i = j
            else: ## nem sikerült, kell még egy ,majd globally kell
                while j >= 0:
                    if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                        if(planes[i].cpr == 1): 
                            ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[j].lat_cpr,lon_even=planes[j].lon_cpr,lat_odd=planes[i].lat_cpr,lon_odd=planes[i].lon_cpr)
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                        else:
                            ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[i].lat_cpr,lon_even=planes[i].lon_cpr,lat_odd=planes[j].lat_cpr,lon_odd=planes[j].lon_cpr)
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                        i = j - 1
                        
                        print("Van ref, nem lehet local decoding, kell még egy üzenet ", planes[j].icao,planes[i].icao)

                    else:
                        j = j - 1
                #i = i - 1
        else: # nincs ref
            while j >= 0:
                if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                    if(planes[i].cpr == 1): 
                        ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[j].lat_cpr,lon_even=planes[j].lon_cpr,lat_odd=planes[i].lat_cpr,lon_odd=planes[i].lon_cpr)
                        coordinates.append(ered)
                        ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])                    
                    else:
                        ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[i].lat_cpr,lon_even=planes[i].lon_cpr,lat_odd=planes[j].lat_cpr,lon_odd=planes[j].lon_cpr)
                        coordinates.append(ered)
                        ref_helyek[planes[i].icao] =  referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"]) 
                    i = j - 1

                    print("Nincs ref, talált globally ", planes[j].icao, planes[i].icao)

                else:
                    j = j - 1
            i = i - 1
            print("nincs ref, nem talált párt ", planes[i].icao)
    return coordinates



def coordinates_jo(messages):
    class plane_pos:
        def __init__(self, icao_, lat_cpr_,lon_cpr_,cpr_):
            self.icao = icao_
            self.lat_cpr = lat_cpr_
            self.lon_cpr = lon_cpr_
            self.cpr = cpr_
        def print_(self):
            print(self.icao,self.lat_cpr,self.lon_cpr,self.cpr)
    planes = list()
    
    repulok = defaultdict(list)

    for i in messages:
        typecode,cap,icao,mess = decoder(i)
        if (9 <= typecode <= 18) or (20 <= typecode <= 22):
            #print(icao,mess[1:4])
            #planes.append(plane_pos(icao,mess[1],mess[2],mess[3]))
            repulok[icao].append(plane_pos(icao,mess[1],mess[2],mess[3]))

        print(repulok)
    for icao, mess in repulok.items():
        print(icao)
        for i in mess:
            print(type(mess))
            print(type(i))

    class full_pos():
        def __init__(self,icao_,lat_e_,lon_e_,lat_o_,lon_o_,cntr):
            self.icao = icao_  
            self.lat_e = lat_e_  
            self.lon_e = lon_e_
            self.lat_o = lat_o_
            self.lon_o = lon_o_
            self.cntr = cntr
        def print_(self):
            print(self.icao,self.lat_e,self.lon_e,self.lat_o,self.lon_o)
    full_posik = list()

    class referencia():
        def __init__(self,lat,lon):
            self.lat = lat  
            self.lon = lon
        def __repr__(self):
            return (f"referencia("
                    f"lat_e={self.lat}, "
                    f"lon_e={self.lon}, ")


    ref_helyek = defaultdict(referencia)
    coordinates = list()

    counter = 1
    valami = 0
    
    for icao, planes in repulok.items():
        print(icao,len(planes))
        i = len(planes) - 1
        while i >= 0:
            planes[i].print_()
            j = i-1
            if planes[i].icao in ref_helyek: 
                print("van ref",icao)
                eredmeny = local_decoding(ref_helyek[planes[i].icao].lat,ref_helyek[planes[i].icao].lon,planes[i].lat_cpr,planes[i].lon_cpr,planes[i].cpr,icao=planes[i].icao,cntr=counter)
                if eredmeny[0] == 1: 
                    eredmeny_ = (eredmeny[1],eredmeny[2],eredmeny[3])
                    print("Van ref, local decoding siekrült",icao)
                    coordinates.append(eredmeny_)
                    i = j
                else: # nem sikerült, globally kell
                    talalt = False
                    while j >= 0:
                        if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                            if(planes[i].cpr == 1): 
                                ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[j].lat_cpr,lon_even=planes[j].lon_cpr,lat_odd=planes[i].lat_cpr,lon_odd=planes[i].lon_cpr)
                                coordinates.append(ered)
                                ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                            else:
                                ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[i].lat_cpr,lon_even=planes[i].lon_cpr,lat_odd=planes[j].lat_cpr,lon_odd=planes[j].lon_cpr)
                                coordinates.append(ered)
                                ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                            i = j - 1 ## ha talált is globally módon később, túl fog lépni más üzeneteken!!!!!!!!!!!!!!!!!!!!! i = i - 1 kell
                            print("Van ref, nem lehet locally, globally sikerült",icao)
                            talalt = True
                            break## itt kellene kilpni mivel i-t mégegyszer léptetni fogja
                        else:
                            print("Nincs ref, nem jo globally-hoz",icao,planes[j].lat_cpr,planes[j].lon_cpr,)
                            j = j - 1
                    if talalt:
                        continue
                    print("Van ref, locally nem globally nem sikerült",icao)
                    i = i - 1
            else: 
                print("nincs ref",icao)
                talalt = False
                van_koztes = False
                while j >= 0:
                    if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                        for k in range(j + 1,i):
                            print(k) 
                            if (planes[k].icao == planes[j].icao) and (planes[k].cpr != planes[j].cpr):# van közelebbi akkor azzal
                                print("van közelebbi")
                                if(planes[k].cpr == 1): 
                                    ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[j].lat_cpr,lon_even=planes[j].lon_cpr,lat_odd=planes[k].lat_cpr,lon_odd=planes[k].lon_cpr)
                                    coordinates.append(ered)
                                    ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])                    
                                else:
                                    ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[k].lat_cpr,lon_even=planes[k].lon_cpr,lat_odd=planes[j].lat_cpr,lon_odd=planes[j].lon_cpr)
                                    coordinates.append(ered)
                                    ref_helyek[planes[i].icao] =  referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                                i = j - 1
                                print(i)
                                talalt = True
                                van_koztes = True
                                break
                        if van_koztes:
                            break
                        if(planes[i].cpr == 1): 
                            ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[j].lat_cpr,lon_even=planes[j].lon_cpr,lat_odd=planes[i].lat_cpr,lon_odd=planes[i].lon_cpr)
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])                    
                        else:
                            ered = position(cntr=counter,icao=planes[j].icao,lat_even=planes[i].lat_cpr,lon_even=planes[i].lon_cpr,lat_odd=planes[j].lat_cpr,lon_odd=planes[j].lon_cpr)
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] =  referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"]) 
                        i = j - 1
                        print("Nincs ref, talált globally",icao,planes[j].lat_cpr,planes[j].lon_cpr,)
                        talalt = True
                        break## ki kellene lépni mivel i-t mégegyzser léptetni fogja
                    else:
                        print("Nincs ref, nem jo globally-hoz",icao,planes[j].lat_cpr,planes[j].lon_cpr,)
                        j = j - 1
                if talalt:
                    continue
                print("Nincs ref nem talált globally",icao)
                i = i - 1
    
    return coordinates"""


def coordinates_jo(messages):
    class plane_pos:
        def __init__(self, icao_, lat_cpr_,lon_cpr_,cpr_):
            self.icao = icao_
            self.lat_cpr = lat_cpr_
            self.lon_cpr = lon_cpr_
            self.cpr = cpr_
        def print_(self):
            print(self.icao,self.lat_cpr,self.lon_cpr,self.cpr)
    planes = list()
    
    repulok = defaultdict(list)

    for i in messages:
        typecode,cap,icao,mess = decoder(i)
        if (9 <= typecode <= 18) or (20 <= typecode <= 22):
            #if icao == "4CA92D":
                #print(icao,mess[1:4])
            planes.append(plane_pos(icao,mess[1],mess[2],mess[3]))
            repulok[icao].append(plane_pos(icao,mess[1],mess[2],mess[3]))

    """    print(repulok)
    for icao, mess in repulok.items():
        print(icao)
        for i in mess:
            print(type(mess))
            print(type(i))"""

    """class full_pos():
        def __init__(self,icao_,lat_e_,lon_e_,lat_o_,lon_o_,cntr):
            self.icao = icao_  
            self.lat_e = lat_e_  
            self.lon_e = lon_e_
            self.lat_o = lat_o_
            self.lon_o = lon_o_
            self.cntr = cntr
        def print_(self):
            print(self.icao,self.lat_e,self.lon_e,self.lat_o,self.lon_o)
    full_posik = list()"""

    class referencia():
        def __init__(self,lat,lon):
            self.lat = lat  
            self.lon = lon
        def __repr__(self):
            return (f"referencia("
                    f"lat_e={self.lat}, "
                    f"lon_e={self.lon}, ")


    ref_helyek = defaultdict(referencia)
    coordinates = list()

    counter = 1
    valami = 0
    
    for icao, planes in repulok.items():
        #print(icao,len(planes))
        i = len(planes) - 1
        while i >= 0:
            planes[i].print_()
            j = i-1
            if planes[i].icao in ref_helyek: 
                print("van ref: ",ref_helyek[planes[i].icao].lat,ref_helyek[planes[i].icao].lon)
                #print(planes[i].icao,planes[i].lat_cpr,planes[i].lon_cpr)
                eredmeny = local_decoding(ref_helyek[planes[i].icao].lat,ref_helyek[planes[i].icao].lon,planes[i].lat_cpr,planes[i].lon_cpr,planes[i].cpr,icao=planes[i].icao,cntr=counter)
                """if planes[i].icao == "4ca92d":
                    print("HALLO: ",eredmeny)"""
                if eredmeny[0] == 1: 
                    eredmeny_ = (eredmeny[1],eredmeny[2],eredmeny[3])
                    #print("Van ref, local decoding siekrült",icao)
                    ref_helyek[planes[i].icao] = referencia(lat=eredmeny[1]["latitude"],lon=eredmeny[1]["longitude"])
                    coordinates.append(eredmeny_)
                    i = j
                else: # nem sikerült, globally kell
                    print("HALLO")
                    talalt = False
                    while j >= 0:
                        if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                            if(planes[i].cpr == 1): # i-edik elem odd 
                                ered = position(planes[j].icao,planes[j].lat_cpr,planes[i].lat_cpr,planes[j].lon_cpr,planes[i].lon_cpr,counter)
                                #print(ered[3])
                                coordinates.append(ered)
                                ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                            else: # i-edik elem even
                                ered = position(planes[j].icao,planes[i].lat_cpr,planes[j].lat_cpr,planes[i].lon_cpr,planes[j].lon_cpr,counter)
                                #print(ered[3])
                                coordinates.append(ered)
                                ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                            i = j - 1 ## ha talált is globally módon később, túl fog lépni más üzeneteken!!!!!!!!!!!!!!!!!!!!! i = i - 1 kell
                            #print("Van ref, nem lehet locally, globally sikerült",icao)
                            talalt = True
                            break## itt kellene kilpni mivel i-t mégegyszer léptetni fogja
                        else:
                            #print("Nincs ref, nem jo globally-hoz",icao,planes[j].lat_cpr,planes[j].lon_cpr,i,j)
                            j = j - 1
                    if talalt:
                        continue
                    #print("Van ref, locally nem globally nem sikerült",icao)
                    i = i - 1
            else: 
                #print("nincs ref",icao)
                talalt = False
                van_koztes = False
                while j >= 0:
                    if (planes[j].icao == planes[i].icao) and (planes[j].cpr != planes[i].cpr): # kell egy ODD és EVEN ugyanattól
                        if ((j+1) != i):
                            for k in range(j + 1,i):
                                #print("i,j,k: ",i,j,k) 
                                if (planes[k].icao == planes[j].icao) and (planes[k].cpr != planes[j].cpr):# van közelebbi akkor azzal
                                    #print("van közelebbi ", planes[k].lat_cpr,planes[k].lon_cpr,planes[j].lat_cpr,planes[j].lon_cpr)
                                    if(planes[k].cpr == 1): # k-adik elem odd
                                        ered = position(planes[j].icao,planes[j].lat_cpr,planes[k].lat_cpr,planes[j].lon_cpr,planes[k].lon_cpr,counter)
                                        print(ered[0]["latitude"],ered[0]["longitude"])
                                        coordinates.append(ered)
                                        ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                                        print("ref: ",ref_helyek[planes[i].icao])                    
                                    else: # k-adik elem even
                                        ered = position(planes[j].icao,planes[k].lat_cpr,planes[j].lat_cpr,planes[k].lon_cpr,planes[j].lon_cpr,counter)
                                        print(ered[0]["latitude"],ered[0]["longitude"])
                                        coordinates.append(ered)
                                        ref_helyek[planes[i].icao] =  referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])
                                        print("ref: ",ref_helyek[planes[i].icao])
                                    i = j - 1
                                    #print(i, ered)
                                    talalt = True
                                    van_koztes = True
                                    break
                        if van_koztes:
                            break
                        if(planes[i].cpr == 1): # i-edik elem odd
                            #print("i odd",planes[i].cpr,planes[i].lat_cpr,planes[i].lon_cpr)
                            ered = position(planes[j].icao,planes[j].lat_cpr,planes[i].lat_cpr,planes[j].lon_cpr,planes[i].lon_cpr,counter)
                            print(ered[0]["latitude"],ered[0]["longitude"])
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] = referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"])   
                            print("ref: ",ref_helyek[planes[i].icao])
                        else: # i-edik elem even
                            #print("i even",type(planes[i].cpr),planes[i].lat_cpr,planes[i].lon_cpr)
                            ered = position(planes[j].icao,planes[i].lat_cpr,planes[j].lat_cpr,planes[i].lon_cpr,planes[j].lon_cpr,counter)
                            print(ered[0]["latitude"],ered[0]["longitude"])
                            coordinates.append(ered)
                            ref_helyek[planes[i].icao] =  referencia(lat=ered[0]["latitude"],lon=ered[0]["longitude"]) 
                            print("ref: ",ref_helyek[planes[i].icao])
                        i = j - 1
                        #print("Nincs ref, talált globally",icao,planes[j].lat_cpr,planes[j].lon_cpr,)
                        talalt = True
                        break## ki kellene lépni mivel i-t mégegyzser léptetni fogja
                    else:
                        #print("Nincs ref, nem jo globally-hoz",icao,planes[j].lat_cpr,planes[j].lon_cpr,i,j)
                        j = j - 1
                if talalt:
                    continue
                #print("Nincs ref nem talált globally",icao)
                i = i - 1
    
    return coordinates  

import numpy as np
from lut import NL
from haversine import haversine,Unit
def local_decoding(lat_r,lon_r,lat,lon,i,icao,cntr):## itt lat lon már 0-1 közti érték kell legyen

    if lat > 2:
        lat = lat/(2**17)
    if lon > 2:
        lon = lon/(2**17)
    
    i = int(i)
    lat_r = float(lat_r)
    lon_r = float(lon_r)
    lat = float(lat)
    lon = float(lon)

    dLat = 360/(4*15-i)
    j = np.floor(lat_r/dLat)+ np.floor((np.mod(lat_r,dLat)/dLat)-lat+0.5) 
    latitude_ = dLat*(j+lat)
    dLon = 360/(max(NL(latitude_)-i,1))
    m = np.floor(lon_r/dLon)+ np.floor((np.mod(lon_r,dLon)/dLon)-lon+0.5)
    longitude_ = dLon*(m+lon)
    pos = dict(latitude = latitude_,longitude = longitude_)
    
    ref = (lat_r,lon_r)
    actual = (latitude_,longitude_)
    
    print(ref,actual,)
    
    dist = haversine(ref,actual,unit=Unit.NAUTICAL_MILES)
    if dist > 180:
        eredmeny = 0
    else:
        eredmeny = 1 
    return eredmeny,pos,icao,cntr

def mi_a_tc(a):
    if (1 <= a <= 4):
        type_code = "Aircraft identification"
    elif (5 <= a <= 8):
        type_code = "Surface position"
    elif (9 <= a <= 18):
        type_code = "Airborne position (Baro Altitude)"
    elif (a == 19):
        type_code = "Airborne velocities"
    elif (20 <= a <= 22):
        type_code = "Airborne position (GNSS height)"
    elif (23 <= a <= 27):
        type_code = "Reserved"
    elif (a == 28):
        type_code = "Aircraft status"
    elif (a == 29):
        type_code = "Target state and status information"
    elif (a == 31):
        type_code = "Aircraft operation status"
    else:
        type_code = "------"
    return type_code