import numpy as np
import graycode as gc

def type_code_lut(a):
    type_code = str()
    a = int(a,2)
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
    return a
## type_code
def capability_lut(a):
    capability = str()
    a = int(a,2)
    if (a == 0):
        capability = "Level 1 transponder"
    elif (1 <=a<= 3):
        capability = "Reserved"
    elif (a == 4):
        capability = "Level 2+ transponder, with ability to set CA to 7, on ground"
    elif (a == 5):
        capability = "Level 2+ transponder,with ability to set CA to 7,airborne"
    elif (a == 6):
        capability = "Level 2+ transponder,with ability to set CA to 7,either on-ground or airborne"
    elif (a == 7):
        capability = "Signifies the Downlink Request value is 0,or the Flight Status is 2, 3, 4, or 5,either airborne or on the ground"     
    return a

def df_lut(a):
    df = str()
    a = ''.join(str(b) for b in a.astype(int))
    a = int(a,2)
    if (a == 0):
        df = "Short ACAS"
    elif (a == 4):
        df = "Surveillance, altitude reply"
    elif (a == 5):
        df = "Surveillance, identity reply"
    elif (a ==11):
        df = "All Call reply"
    elif (a == 16):
        df = "Long ACAS"
    elif (a == 17):
        df = "Extended squitter"
    elif (a == 18):
        df = "Extended squitter, non transponder"
    elif (a == 19):
        df = "Military extended squitter"     
    elif (a == 20):
        df = "Comm-B altitude reply"
    elif (a == 21):
        df = "Comm-B identity reply"
    elif (a == 24):
        df = "Comm-D"
    else:
        df = "--" 
    return df,a


def icao_lut(a):
    a = hex(int(a,2))
    a = a[2:]
    return a

def message_lut(message,tc): 
    from lut import message_velocity_lut
    tc = int(tc,2)   
    #print("hello")
    if (tc == 19):
        reply = message_velocity_lut(message)
    elif (9 <= tc <= 18) or (20<= tc<= 22):
        reply = message_pos_baro_lut(message,tc)
    elif (tc == 29):
        reply = "Target state and status information"
    elif (tc == 28) or (tc == 29) or (tc == 31):
        reply = "Státus információ 28/29/31"
    elif (1<=tc<=4):
        reply = "Aircraft identification/Gép azonosítás"
    elif (5<=tc<=8):
        reply = "Surface position/Felszíni pozíció"
    return reply

def message_velocity_lut(message): ## függőleges sebesség minden esetben van, és vízszintes sebesség vagy földi vagy légi
  
    """tipus = str()
    legi_foldi = str()"""
    VrSrc = message[35]
    Svr = int(message[36],2)
    VR = int(message[37:46],2)
    #print("VR: ",VR," Svr: ",Svr)
    if (VR == 0):
        v_vertikal = "no information"
        #print(VR)
    if (Svr == 0):
        v_vertikal = 64*(VR-1)
    else:
        v_vertikal = -64*(VR-1)
    v_vertikal = round(v_vertikal,2)
    v_vert = "Vertikális sebesség: " + str(v_vertikal) + "láb/perc"
    sub_type = message[5:8]
    sub_type = int(sub_type,2)
    Vx = Vy = 0
    # itt a sub type-ok a horizontális / tehát vízszintes sebességre vonatkoznak #
    if ((sub_type == 1)or(sub_type == 2)): ## ground speed
        legi_foldi = "ground speed"
        if ((sub_type == 1)): ## subsonic
            tipus = "subsonic"
            Dew = message[13]
            Dns = message[24]
            Vew = message[14:24]
            Vns = message[25:35]
            if Dew == "0":
                Vx = int(Vew,2) - 1
            else:
                Vx = - int(Vew,2) + 1
            if Dns == "0":
                Vy = int(Vns,2) - 1
            else:
                Vy = -int(Vns,2) + 1
            
        if ((sub_type == 2)): ## supersonic
            tipus = "supersonic"
            if Dew == "0":
                Vx = 4*(int(Vew,2) - 1)
            else:
                Vx = -4*(int(Vns,2) - 1)
            if Dns == "0":
                Vy = 4*(int(Vew,2) - 1)
            else:
                Vy = -4*(int(Vns,2) - 1)    
            
        v_hor = round(np.sqrt(Vx**2+Vy**2),2)
        angle_hor = round(np.mod((np.arctan2(Vx,Vy)*(360/(2*np.pi))),360),2)
        v_hor="Sebesség: "+str(v_hor) + "csomó"
        angle_hor ="Szög: "+ str(angle_hor) + " fok"## tipus,legi_foldi kell returnbe
        return v_hor,angle_hor, v_vert,tipus,legi_foldi
    if ((sub_type == 3) or (sub_type == 4)): ## airspeed
        legi_foldi = "air speed"
        angle_hor = round(int(message[14:24],2)*360/1024,2)
        if (sub_type == 3): ##subsonic
            tipus = "subsonic"
            v_hor = round(int(message[25:35],2)-1,2)
    
        if (sub_type == 4): ## supersonic
            tipus = "supersonic" 
            v_hor = round(4*(int(message[25:35],2)-1),2)
               
        v_hor="Sebesség: "+str(v_hor) + " csomó"
        angle_hor ="Szög: "+ str(angle_hor) + " fok"##tipus,legi_foldi is visszaadja csak azért vettem ki mert nem kell overleafbe
        return v_hor,angle_hor,v_vert,tipus,legi_foldi
    #-------------------------------------------------------------------------------#

def message_pos_baro_lut(message,tc):#message altitude helyett
    feet = 0
    if (20 <= tc <=22): #gnss
        altitude = message[8:20]
        altitude = int(altitude,2)    
        feet = altitude
    else:#baro
        altitude = message[8:20]
        q = altitude[7]
        if (q == '1'):
            altitude = altitude[0:7]+altitude[8:]
            altitude = int(altitude,2)
            feet = (25*altitude)-1000
        else:
            altitude = altitude[0:7]+altitude[8:]
            #print(altitude)
            altitude = int(altitude,2)
            
            ## altitude string és bináris számot kéne csinálni belőle

            altitude = gc.gray_code.gray_code_to_tc(altitude)
            print("GRAY CODE",altitude)
            feet = (100 * altitude) - 1000
            print("FEET",feet)
    feet = round(feet,2)
    feet = "Magasság: " + str(feet) + " láb / " + str(feet*0.3048) + " méter"
    cpr = message[21]
    
    cpr = int(cpr)
    #cpr = "paritás: "+str(cpr)## nem kell csak overleafhez
    lat_cpr = int(message[22:39],2)
    #lat_cpr = "szélesség CPR: "+str(lat_cpr) ## nem kell csak overleafhez
    lon_cpr = int(message[39:],2)  
    #lon_cpr = "hosszúság CPR: "+str(lon_cpr) ## nem kell csak overleafhez
    return feet,lat_cpr,lon_cpr,cpr

def NL(lat):
    Nz = 15
    no_long = np.floor(2*np.pi/np.arccos(1-((1-np.cos(np.pi/(2*Nz)))/np.cos(lat*(np.pi/180))**2)))
    return no_long


def position (icao,lat_even,lat_odd,lon_even,lon_odd,cntr): ## ez a sima CPR érték
    lat__even = lat_even
    lat__odd = lat_odd
    lon__even = lon_even
    lon__odd = lon_odd

    #print(lat_even,lat_odd,lon_even,lon_odd)

    #print("GLOBALY",icao,lat_even,lat_odd,lon_even,lon_odd)

    lat_even = lat_even/(2**17)
    lat_odd = lat_odd/(2**17)
    lon_even = lon_even/(2**17)
    lon_odd = lon_odd/(2**17)

    #print(lat_even,lat_odd,lon_even,lon_odd)


    j = np.floor(59*lat_even - 60*lat_odd + 1/2)    
    
    #print(j)

    Nz = 15
    latitude = 0
    
    d_lat_even = 360/(4*Nz)
    d_lat_odd = 360/(4*Nz-1)
    
    #print(d_lat_even,d_lat_odd)

    lat_even = d_lat_even*(np.mod(j,60)+ lat_even)
    lat_odd = d_lat_odd*(np.mod(j,59)+ lat_odd)
    
    #print(lat_even,lat_odd)

    if lat_even >= 270:
        #print("KORREKCIO",lat_even,"alapadatok: late,lato, lone,lono: ", lat__even,lat__odd,lon__even,lon__odd)
        lat_even = lat_even - 360
    if lat_odd >= 270:
        #print("KORREKCIO",lat_odd)
        lat_odd = lat_odd - 360

    if (NL(lat_even) == NL(lat_odd)):
        latitude = lat_even
    else:
        return "latitude-ok nem egyeznek"
    
    m = np.floor(lon_even*(NL(latitude)-1)-lon_odd*NL(latitude)+1/2)
    print("m:",m)
    n_even = max(NL(latitude),1)
    print("n_even:",n_even)
    dlon_even = 360/n_even
    print("dLoneve: ",dlon_even)
    longitude_even = dlon_even*(np.mod(m,n_even)+lon_even)
    print("mod: ",np.mod(m,n_even))
    print("loneven: ",lon_even)
    print("longitude: ",longitude_even)
    if longitude_even >= 180:
        print(longitude_even)
        longitude_even = longitude_even - 360
        print(longitude_even)

    n_odd = max(NL(latitude-1),1)
    dlon_odd =360/n_odd
    longitude_odd = dlon_odd*(np.mod(m,n_odd)+lon_odd)
    
    nem_jo = 0
    if (latitude < 0) or (longitude_even < 0):
        nem_jo = 1
    pos = dict(latitude = str(latitude), longitude = str(longitude_even))
    print(longitude_even,pos["longitude"])
    return pos,icao,cntr,nem_jo

import math

def egyszerusit(a, b):


    g = math.gcd(a, b)
    up = a // g
    down = b // g
    return up, down
