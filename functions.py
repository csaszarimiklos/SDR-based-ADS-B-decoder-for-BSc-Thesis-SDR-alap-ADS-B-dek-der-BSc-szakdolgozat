import numpy as np
import matplotlib.pyplot as plt
import wave_bwf_rf64 
import contextlib
import math
from scipy import signal
from collections import defaultdict
from crccheck.crc import Crc
def open(filename):
    with contextlib.closing(wave_bwf_rf64.open(filename,'rb')) as f:
        fs = f.getframerate()
        num_frames = f.getnframes()
        iq_samples = f.readframes(num_frames)
    iq_samples = np.frombuffer(iq_samples, dtype=np.int16) 
    I = iq_samples[0::2]
    Q = iq_samples[1::2]
    iq_samples = I + 1j * Q
    iq_samples = np.abs(iq_samples)
    return iq_samples,num_frames,fs

def resample(iq_samples,fs_):
    efes = fs_
    up = 5
    down = 3
    iq_samples = signal.resample_poly(iq_samples,up = up,down=down)
    fs = efes*up
    fs = fs/down
    Ts = 1/fs
    return iq_samples,up,down,Ts

def preamble(up,down,num_frames,Ts):
    #fs = fs_*up/down
    #Ts = 1/fs
    #length = num_frames*Ts
    #--------PREAMBLE--------#
    a1 = 0
    a2 = 0.5*10**-6
    b1 = 1*10**-6
    b2 = 1.5*10**-6
    c1 = 3.5*10**-6
    c2 = 4*10**-6
    d1 = 4.5*10**-6
    d2 = 5*10**-6
    #------------------------#
    #-----------DF-----------##     10 01 01 01 10       #
    e1 = 8*10**-6
    e2 = 8.5*10**-6
    f1 = 9.5*10**-6
    f2 = 10*10**-6
    g1 = 10.5*10**-6
    g2 = 11*10**-6
    h1 = 11.5*10**-6
    h2 = 12.5*10**-6
    #------------------------#
    preamble_df = np.arange(0*10**-6,13*10**-6,Ts)
    #print(Ts)
    for i in range(len(preamble_df)):
        if  ((a1 <= preamble_df[i] < a2) or (d1 <= preamble_df[i] < d2) or (c1 <= preamble_df[i] < c2) or (b1 <= preamble_df[i] < b2)) or ((e1 <= preamble_df[i] < e2) or (f1 <= preamble_df[i] < f2) or (g1 <= preamble_df[i] < g2) or (h1 <= preamble_df[i] < h2)):
            preamble_df[i] = 1
        else:
            preamble_df[i] = 0
    time_preamble = np.arange(0,len(preamble_df)*Ts,Ts)
    
    return preamble_df,Ts

def search(iq_samples,preamble_df):
    arg = list()
    for i in range(len(iq_samples)-len(preamble_df)-1):
    # az 1 esek nagyobbak mint a 0-k
        if (iq_samples[i] > iq_samples[i+2] and
            iq_samples[i+1] > iq_samples[i+2] and
            iq_samples[i+3] < iq_samples[i+4] and
            iq_samples[i+5] > iq_samples[i+3] and

            iq_samples[i+14] > iq_samples[i+13] and
            iq_samples[i+15] > iq_samples[i+13] and
            iq_samples[i+17] < iq_samples[i+19] and
            iq_samples[i+17] < iq_samples[i+18] and  

            iq_samples[i+32] > iq_samples[i+31] and
            iq_samples[i+33] > iq_samples[i+31] and

            iq_samples[i+38] > iq_samples[i+37] and
            iq_samples[i+39] > iq_samples[i+37] and

            iq_samples[i+42] > iq_samples[i+41] and
            iq_samples[i+43] > iq_samples[i+41] and

            iq_samples[i+49] > iq_samples[i+45] and
            iq_samples[i+46] > iq_samples[i+45]):
                arg.append(i)
    return arg

    conv = list()
    max_arg = 0
    for i in range(len(arg)):
        a = np.correlate(preamble_df,iq_samples[arg[i]:arg[i]+len(preamble_df)],mode="full")
        a = np.max(a)
        conv.append(a)
    max_iq = np.argmax(conv)
    max_value = np.max(conv)
    #print(len(conv))
    # az iq_samples ezen mintasoroazta az arg[max_iq]-adik eleme az iq_samples nek
    # ki kellene listázni az összes 0 hibás üzenetet
    # a minták az iq_samples[arg[i]:arg[i]+len(preamble_df)]

def messages(arg,iq_samples,Ts):
    from crccheck.crc import Crc
    messages = list()
    print("messages elkezdődött")
    raw_messages = list()
    szamlalo = 1
    átment = nem_ment = 0
    for i in arg:
        print("ennyiszer fut le",szamlalo)
        szamlalo += 1
        start = i
        stop1 = start + math.floor(8*10**-6/Ts)
        PREAMBLE = iq_samples[start:stop1]
        #----------------DF mintái------------------#
        stop2 = stop1 + math.floor(5*10**-6/Ts)
        DF = iq_samples[stop1:stop2]
        #----------------CA mintái------------------#
        stop3 = stop2 + math.floor(3*10**-6/Ts)
        CA = iq_samples[stop2:stop3]
        #----------------ICAO mintái------------------#
        stop4 = stop3 + math.floor(24*10**-6/Ts)
        ICAO = iq_samples[stop3:stop4]
        #----------------ME mintái------------------#
        stop5 = stop4 + math.floor(56*10**-6/Ts)
        ME = iq_samples[stop4:stop5]
        #----------------PI mintái------------------#
        stop6 = stop5 + math.floor(24*10**-6/Ts)
        PI = iq_samples[stop5:stop6]
        full = np.concatenate([PREAMBLE,DF,CA,ICAO,ME,PI])
        
        bits = np.zeros(112,dtype = np.int64)
        full_bitek = full
        preamble_bits = full_bitek[:16*2]
        full_bitek = full_bitek[16*2:]
        #-------valahogy nyerjük ki a nyers üzenetet-------------------#
        #--------------------------------------------------------------#
        raw_mess = list()
        #-------------------------4 MSPS-------------------------------#
        for n in range(112):
            raw_mess.append(full_bitek[4*n:4*n+4])
            if (sum(full_bitek[4*n:4*n+2]) <= sum(full_bitek[4*n+2:4*n+4])):
                bits[n] = 0
            elif (sum(full_bitek[4*n:4*n+2]) > sum(full_bitek[4*n+2:4*n+4])):
                bits[n] = 1
            else:
                bits[n] = -1
        df_bits = bits[:5]
        #df_bits = ''.join(str(b) for b in df_bits.astype(int))
        ca_bits = bits[5:8]
        #ca_bits = ''.join(str(b) for b in ca_bits.astype(int))
        icao_bits = bits[8:32]
        #icao_bits = ''.join(str(b) for b in icao_bits.astype(int))
        me_bits = bits[32:88]
        pi_bits = bits[88:]
        type_code_bits = me_bits[:5]
        type_code_bits = ''.join(str(b) for b in type_code_bits.astype(int))
        #print(df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits)

        ADS_B = Crc(width=24,poly=0x1FFF409,initvalue=0,xor_output=0,reflect_input=False,reflect_output=False)
        
        df_bits_string = ''.join(str(b) for b in df_bits)
        ca_bits_string = ''.join(str(b) for b in ca_bits)
        icao_bits_string = ''.join(str(b) for b in icao_bits)
        me_bits_string = ''.join(str(b) for b in me_bits)
        pi_bits_string = ''.join(str(b) for b in pi_bits)
        data = df_bits_string+ca_bits_string+icao_bits_string+me_bits_string+pi_bits_string
        bin_data = data
        data = hex(int(data, 2))[2:]
        if len(data) % 2 != 0:
            data = "0" + data
        data_ = bytes.fromhex(data)    
        err_mess = list()
        remainder = ADS_B.calc(data_)

        if (remainder == 0):
            messages.append(data)
            átment += 1
            raw_messages.append(raw_mess)
        else:
            #print("nem ment át")
            nem_ment += 1
            #err_mess.append(data)
            """df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits,err_mess,"""""",len(err_mess),(len(messages)+len(err_mess)),len(arg),raw_messages"""
    #print("lenarg,eljutott, átment, nem ment át",len(arg),eljutott_crc_ig,átment,nem_ment)
    print("messages végzett")
    return messages,len(messages)

import math
import numpy as np
def messages_uj(arg,iq_samples,Ts):
    from crccheck.crc import Crc
    messages = list()
    raw_messages = list()
    mennyi = 0
    volt_baj = 0
    baj_javitva = 0
    elsokor = 0
    bitek = list()
    for i in arg:
        baj = 0
        start = i
        stop1 = start + math.floor(8*10**-6/Ts)
        PREAMBLE = iq_samples[start:stop1]
        #----------------DF mintái------------------#
        stop2 = stop1 + math.floor(5*10**-6/Ts)
        DF = iq_samples[stop1:stop2]
        #----------------CA mintái------------------#
        stop3 = stop2 + math.floor(3*10**-6/Ts)
        CA = iq_samples[stop2:stop3]
        #----------------ICAO mintái------------------#
        stop4 = stop3 + math.floor(24*10**-6/Ts)
        ICAO = iq_samples[stop3:stop4]
        #----------------ME mintái------------------#
        stop5 = stop4 + math.floor(56*10**-6/Ts)
        ME = iq_samples[stop4:stop5]
        #----------------PI mintái------------------#
        stop6 = stop5 + math.floor(24*10**-6/Ts)
        PI = iq_samples[stop5:stop6]
        full = np.concatenate([PREAMBLE,DF,CA,ICAO,ME,PI])
        
        ### itt kellene egy olyan hogy vesszük az 1esek átlagát és a 0k átlagát
        avg_ones = np.average([iq_samples[i],iq_samples[i+1],iq_samples[i+4],iq_samples[i+5],iq_samples[i+14],iq_samples[i+15],iq_samples[i+18],iq_samples[i+19],
                    iq_samples[i+32],iq_samples[i+33],iq_samples[i+38],iq_samples[i+39],
                    iq_samples[i+42],iq_samples[i+43],iq_samples[i+46],iq_samples[i+49]])
        
        avg_zeros = np.average([iq_samples[i+2],iq_samples[i+3],iq_samples[i+6],iq_samples[i+7],iq_samples[i+8],iq_samples[i+9],iq_samples[i+10],iq_samples[i+11],
                    iq_samples[i+12],iq_samples[i+13],iq_samples[i+16],iq_samples[i+17],
                    iq_samples[i+20],iq_samples[i+21],iq_samples[i+22],iq_samples[i+23],iq_samples[i+24],iq_samples[i+25],iq_samples[i+26],iq_samples[i+27],
                    iq_samples[i+28],iq_samples[i+29],iq_samples[i+30],iq_samples[i+31],iq_samples[i+34],iq_samples[i+35],iq_samples[i+36],iq_samples[i+37],
                    iq_samples[i+40],iq_samples[i+41],iq_samples[i+44],iq_samples[i+45],iq_samples[i+47],iq_samples[i+48],iq_samples[i+50],iq_samples[i+51]])
        avg = np.average([iq_samples[i:i+51]])
        #limit = np.average([avg_ones,avg_zeros])
        limit = avg
        #print("avg,avg1, avg0, limit: ",avg,avg_ones,avg_zeros,limit)

        ### +-1 közé normáljuk az egész üzenetet és 0 felett 1nek, 0 alatt 0

        bits = np.zeros(112,dtype = np.int64)
        full_bitek = full
        preamble_bits = full_bitek[:16*2]
        full_bitek = full_bitek[16*2:]
        #print("full bitek hossza",len(full_bitek))
        full_bitek = full_bitek/max(abs(full_bitek))
        #print("max és min: ",max(full_bitek),min(full_bitek))       
        limit = (max(full_bitek)+min(full_bitek))/2
        #print("limit: ",limit)
        #-------valahogy nyerjük ki a nyers üzenetet-------------------#
        #--------------------------------------------------------------#
        raw_mess = list()
        #-------------------------4 MSPS-------------------------------#

        for j in range(len(full_bitek)):
            #print("j típusa és j: ",type(j),full_bitek[j])
            if (full_bitek[j] <= limit):
                full_bitek[j] = 0
            else:
                full_bitek[j] = 1
            #print("j a konvertálás után",full_bitek[j])
        #print("most jön a döntés")

        ### most kellene eldönteni a hibás eseteket is
        #1:     0001/0010/0111/1011/0000/0101/0110 ---------->    0011
        #2:     0100/1000/1101/1110/1111/1010/1001 ---------->    1100
        jo_1 = np.array([0,0,1,1])
        jo_2 = np.array([1,1,0,0])
        rossz_11 = np.array([0,0,0,1])
        rossz_12 = np.array([0,0,1,0])
        rossz_13 = np.array([0,1,1,1])
        rossz_14 = np.array([1,0,1,1])
        rossz_15 = np.array([0,0,0,0])
        rossz_16 = np.array([0,1,0,1])
        rossz_17 = np.array([0,1,1,0])

        rossz_21 = np.array([0,1,0,0])
        rossz_22 = np.array([1,0,0,0])
        rossz_23 = np.array([1,1,0,1])
        rossz_24 = np.array([1,1,1,0])
        rossz_25 = np.array([1,1,1,1])
        rossz_26 = np.array([1,0,1,0])
        rossz_27 = np.array([1,0,0,1])
        
         
        # átalakítjuk a lehetséges opcióra 50/50 százalékkal
        for j in range(112): # 0011/1100 esetén nincs baj
            if np.array_equal(full_bitek[4*j:4*j+4],rossz_11) or np.array_equal(full_bitek[4*j:4*j+4],rossz_12) or np.array_equal(full_bitek[4*j:4*j+4],rossz_13) or np.array_equal(full_bitek[4*j:4*j+4],rossz_14) or np.array_equal(full_bitek[4*j:4*j+4],rossz_15) or np.array_equal(full_bitek[4*j:4*j+4],rossz_16) or np.array_equal(full_bitek[4*j:4*j+4],rossz_17):
                #print(full_bitek[4*j:4*j+4])
                volt_baj += 1
                full_bitek[4*j:4*j+4] = jo_1
                baj_javitva += 1

                #print(full_bitek[4*j:4*j+4]) 
            elif np.array_equal(full_bitek[4*j:4*j+4],rossz_21) or np.array_equal(full_bitek[4*j:4*j+4],rossz_22) or np.array_equal(full_bitek[4*j:4*j+4],rossz_23) or np.array_equal(full_bitek[4*j:4*j+4],rossz_24) or np.array_equal(full_bitek[4*j:4*j+4],rossz_25) or np.array_equal(full_bitek[4*j:4*j+4],rossz_26) or np.array_equal(full_bitek[4*j:4*j+4],rossz_27):
                volt_baj += 1
                full_bitek[4*j:4*j+4] = jo_2
                baj_javitva += 1

        for n in range(112):
            raw_mess.append(full_bitek[4*n:4*n+4])
            if (full_bitek[4*n] == 0 and full_bitek[4*n+1] == 0 and full_bitek[4*n+2] == 1 and full_bitek[4*n+3] == 1):
                bits[n] = 0
            elif (full_bitek[4*n] == 1 and full_bitek[4*n+1] == 1 and full_bitek[4*n+2] == 0 and full_bitek[4*n+3] == 0):
                bits[n] = 1
            else:
                bits[n] = -1
            #print("full bitek adat: ",full_bitek[4*n:4*n+4])
            if ((full_bitek[4*n] == 1)and(full_bitek[4*n+1] == 1)and(full_bitek[4*n+2] == 0)and(full_bitek[4*n+3] == 0))or((full_bitek[4*n] == 0)and(full_bitek[4*n+1] == 0)and(full_bitek[4*n+2] == 1)and(full_bitek[4*n+3] == 1)):
                baj += 1
        #print("hány lett jó, ez lett belőlük: ",baj,bits[n])
        bitek.append(bits)
        
        df_bits = bits[:5]
        #df_bits = ''.join(str(b) for b in df_bits.astype(int))
        ca_bits = bits[5:8]
        #ca_bits = ''.join(str(b) for b in ca_bits.astype(int))
        icao_bits = bits[8:32]
        #icao_bits = ''.join(str(b) for b in icao_bits.astype(int))
        me_bits = bits[32:88]
        pi_bits = bits[88:]
        type_code_bits = me_bits[:5]
        type_code_bits = ''.join(str(b) for b in type_code_bits.astype(int))
        #print("a kinyert bitek: ",df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits)

        ADS_B = Crc(width=24,poly=0x1FFF409,initvalue=0,xor_output=0,reflect_input=False,reflect_output=False)
        
        df_bits_string = ''.join(str(b) for b in df_bits)
        ca_bits_string = ''.join(str(b) for b in ca_bits)
        icao_bits_string = ''.join(str(b) for b in icao_bits)
        me_bits_string = ''.join(str(b) for b in me_bits)
        pi_bits_string = ''.join(str(b) for b in pi_bits)
        data = df_bits_string+ca_bits_string+icao_bits_string+me_bits_string+pi_bits_string
        
        #print("data az összefűzésből: ",data)
        bin_data = data
        data = hex(int(data, 2))[2:]
        #print("hex data: ",data)
        if len(data) % 2 != 0:
            data = "0" + data
            
        #print(data)
        data_ = bytes.fromhex(data) 
        ellenorizendo_data = list()
        err_mess = list()
        remainder = ADS_B.calc(data_)
        if (remainder == 0):
            messages.append(data)
            if elsokor == 0:
                ellenorizendo_data.append(data_)
                elsokor = 1
            #print("és ez volt az eredeti: ",data)
            mennyi += 1
            raw_messages.append(raw_mess)
        else:
            err_mess.append(data)

    print("boltbaj,bajjavitva,hanyszor volt sikeres a crc,mit",volt_baj,baj_javitva,mennyi,ellenorizendo_data)

    #return messages,df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits,err_mess,len(messages),len(err_mess),(len(messages)+len(err_mess)),len(arg),raw_messages
    return bitek

def messages_megujabb(arg,iq_samples,Ts):   
    #print("belép ide egyáltalán",Ts)
    from crccheck.crc import Crc
    messages = list()
    szamlalo = 1
    raw_messages = list()
    a = 2
    modositott = 0
    nem_modositott_uzenet = 0
    #print("idáig is")
    for i in arg:
        #print("ennyiszer futott le: ",szamlalo)
        szamlalo += 1
        kellett_e_modositani = False
        start = i
        stop1 = start + math.floor(8*10**-6/Ts)
        PREAMBLE = iq_samples[start:stop1]
        #----------------DF mintái------------------#
        stop2 = stop1 + math.floor(5*10**-6/Ts)
        DF = iq_samples[stop1:stop2]
        #----------------CA mintái------------------#
        stop3 = stop2 + math.floor(3*10**-6/Ts)
        CA = iq_samples[stop2:stop3]
        #----------------ICAO mintái------------------#
        stop4 = stop3 + math.floor(24*10**-6/Ts)
        ICAO = iq_samples[stop3:stop4]
        #----------------ME mintái------------------#
        stop5 = stop4 + math.floor(56*10**-6/Ts)
        ME = iq_samples[stop4:stop5]
        #----------------PI mintái------------------#
        stop6 = stop5 + math.floor(24*10**-6/Ts)
        PI = iq_samples[stop5:stop6]
        full = np.concatenate([PREAMBLE,DF,CA,ICAO,ME,PI])
        #print("Hossz",len(full))
        if len(full)< 480:
            continue
        bits = np.zeros(112,dtype = np.int64)
        full_bitek = full
        preamble_bits = full_bitek[:16*2]
        full_bitek = full_bitek[16*2:]
        #-------valahogy nyerjük ki a nyers üzenetet-------------------#
        #--------------------------------------------------------------#
        raw_mess = list()
        #-------------------------4 MSPS-------------------------------#
        for n in range(112): ## korrigálunk az ellentétes esetre ha van 1 kiugró érték
            raw_mess.append(full_bitek[4*n:4*n+4])
            avg = np.average(full_bitek[4*n:4*n+4])
            #print("itt lenne a hiba?ADSDSADD",n,len(full))
            delta1 = full_bitek[4*n]-avg
            delta2 = full_bitek[4*n+1]-avg
            delta3 = full_bitek[4*n+2]-avg
            delta4 = full_bitek[4*n+3]-avg
            deltas = np.array([delta1,delta2,delta3,delta4])
            avg_delta = np.average(np.abs(deltas))
            upper_bound = a*avg_delta
            #print(deltas,avg_delta,upper_bound)
            if (sum(full_bitek[4*n:4*n+2]) <= sum(full_bitek[4*n+2:4*n+4])):
                bits[n] = 0

                #print(bits[n])
            elif (sum(full_bitek[4*n:4*n+2]) > sum(full_bitek[4*n+2:4*n+4])):
                bits[n] = 1
                #print(bits[n])
            else:
                bits[n] = -1
            if (sum(full_bitek[4*n:4*n+2]) <= sum(full_bitek[4*n+2:4*n+4])):
                if ((delta1 > upper_bound) and (delta2 <= upper_bound) and (delta3 <= upper_bound) and (delta4 <= upper_bound)) or ((delta2 > upper_bound) and (delta1 <= upper_bound) and(delta3 <= upper_bound) and (delta4 <= upper_bound)):
                    bits[n] = 1
                    kellett_e_modositani = True
                    #print("modositott, bit: ",bits[n])
            elif (sum(full_bitek[4*n:4*n+2]) > sum(full_bitek[4*n+2:4*n+4])):
                if ((delta3 > upper_bound) and (delta4 <= upper_bound)and(delta2 <= upper_bound)and(delta1 <= upper_bound)) or ((delta4 > upper_bound) and (delta3 <= upper_bound)and(delta2 <= upper_bound)and(delta1 <= upper_bound)):
                    bits[n] = 0       
                    #print("modositott,bit: ",bits[n])
                    kellett_e_modositani = True
        if kellett_e_modositani:
            modositott += 1
        else:
            nem_modositott_uzenet += 1
        df_bits = bits[:5]
        #df_bits = ''.join(str(b) for b in df_bits.astype(int))
        ca_bits = bits[5:8]
        #ca_bits = ''.join(str(b) for b in ca_bits.astype(int))
        icao_bits = bits[8:32]
        #icao_bits = ''.join(str(b) for b in icao_bits.astype(int))
        me_bits = bits[32:88]
        pi_bits = bits[88:]
        type_code_bits = me_bits[:5]
        type_code_bits = ''.join(str(b) for b in type_code_bits.astype(int))
        #print(df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits)

        ADS_B = Crc(width=24,poly=0x1FFF409,initvalue=0,xor_output=0,reflect_input=False,reflect_output=False)
        
        df_bits_string = ''.join(str(b) for b in df_bits)
        ca_bits_string = ''.join(str(b) for b in ca_bits)
        icao_bits_string = ''.join(str(b) for b in icao_bits)
        me_bits_string = ''.join(str(b) for b in me_bits)
        pi_bits_string = ''.join(str(b) for b in pi_bits)
        data = df_bits_string+ca_bits_string+icao_bits_string+me_bits_string+pi_bits_string
        bin_data = data
        data = hex(int(data, 2))[2:]
        if len(data) % 2 != 0:
            data = "0" + data
        
        bit_array = np.array([int(b) for b in bin_data], dtype=np.uint8)
        data_bytes = np.packbits(bit_array).tobytes()


        data_ = bytes.fromhex(data) 
        #print(bin_data,data,data_bytes)
        err_mess = list()
        remainder = ADS_B.calc(data_bytes)
        #print("remainder",remainder)
        if (remainder == 0):
            messages.append(data)
            #print("0 lett")
            raw_messages.append(raw_mess)
        else:
            err_mess.append(data)        
        #print("idáig is és keresi az üzeneteket")    
    return messages,len(messages)

## dekódol egy üzenetet
def decoder(data):
    from lut import capability_lut,type_code_lut,df_lut,icao_lut,message_lut
    #print("ASDASD, data típusa: ",type(data),type(data[0]))
    data = bin(int(data,16))[2:]
    df = data[:5]
    ca = data[5:8]
    icao = data[8:32]
    me = data[32:88]
    pi = data[88:]
    tc = me[:5]
    type_code = type_code_lut(tc)
    capability = capability_lut(ca)
    icao = icao_lut(icao)
    message = message_lut(me,tc)       
    return type_code, capability, icao,message

def planes(messages_):
    planes = defaultdict(list)
    for i in messages_:
        icao = i[2:8]       
        planes[icao].append(i)
    return planes

class plane_pos_:
    def __init__(self, lat_cpr_,lon_cpr_,cpr_):
        self.lat_cpr = lat_cpr_
        self.lon_cpr = lon_cpr_
        self.cpr = cpr_
    def print_(self):
        print(self.lat_cpr,self.lon_cpr,self.cpr)

## az üzeneteken végigmenve kinyeri a pozíciós adatokat és csoportosítja az egy géphez tartozókat
def planes_coordinates(messages_):    
    plane_coord = defaultdict(list)
    for i in messages_:
        typecode,cap,icao,mess = decoder(i)
        if typecode[1] == 11:
            icao_ = i[2:8]       
            plane_coord[icao_].append(plane_pos_(mess[1], mess[2], mess[3]))## magasság, szélesség, hosszúság, páros/páratlan ### ????????????????
    return plane_coord

def coordinates(messages):## az összes üzenet alapján visszaadja egy gép valódi pozícióit
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
        if (9 <= typecode <= 18):##ITT KELLENE 20-22 TC is mivel azt is ugyanígy kell dekdolni, csak az GNSS magasság
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
    counter = 1
    i = len(planes)-1
    while i >= 0: ## GLOBALLY UNAMBIGUOUS POSITIONING
        found = False
        j = i - 1
        while j >= 0:     
            if (planes[i].icao == planes[j].icao):
                if (planes[i].cpr == "1" and planes[j].cpr == "0"): # 0 even 1 odd
                    full_posik.append(full_pos(cntr=counter,icao_=  planes[i].icao,lat_e_=planes[j].lat_cpr,lon_e_ = planes[j].lon_cpr,lat_o_ = planes[i].lat_cpr,lon_o_ = planes[i].lon_cpr))
                    i = j - 1
                    counter += 1
                    found = True
                    break
                    #print(i.icao,j.lat_cpr, j.lon_cpr, i.lat_cpr,i.lon_cpr)
                if (planes[i].cpr == "0" and planes[j].cpr == "1"):
                    full_posik.append(full_pos(cntr=counter,icao_ =planes[i].icao,lat_e_=planes[i].lat_cpr,lon_e_ = planes[i].lon_cpr,lat_o_ = planes[j].lat_cpr,lon_o_ = planes[j].lon_cpr))
                    i = j - 1
                    counter += 1
                    found = True
                    break
            j = j - 1
        if not found:
            i = i - 1 
    from lut import position
    coordinates = list()
    for i in full_posik:
        coordinates.append(position(lat_even= i.lat_e ,   lat_odd=i.lat_o    ,   lon_even=i.lon_e   ,   lon_odd=i.lon_o,icao=i.icao,cntr=i.cntr))
        #i.print_()
    return coordinates

def map(coordinates):
    import folium
    import webbrowser
    from collections import defaultdict

    lat0 = float(coordinates[0][0]["latitude"])
    lon0 = float(coordinates[0][0]["longitude"])
    map = folium.Map(location=[lat0, lon0], zoom_start=7)
    
    #map = folium.Map(location=[coordinates[0][0]["latitude"],coordinates[0][0]["longitude"]],zoom_start=7)
    
    utvonal = defaultdict(list)
    
    for i in coordinates:
        lat = float(i[0]["latitude"])
        lon = float(i[0]["longitude"])
        icao = i[1]
        utvonal[icao].append((lat,lon))

        popup_text = f"{icao}<br>{lat:.5f}, {lon:.5f}"

        marker = folium.Marker(
            location=(lat, lon),
            popup=popup_text
        )
        marker.add_to(map)

        folium.map.Popup(popup_text, show=True).add_to(marker)
        #folium.CircleMarker(location=(lat,lon),radius=4,color="blue",fill = True,fill_opacity=0.8,popup = f"{icao}\n{lat:.5f}, {lon:.5f}").add_to(map)

    for icao, coords in utvonal.items():
        folium.PolyLine(coords, tooltip=f"Path of {icao}",weight=3).add_to(map)
    map.save("map3.html")
    webbrowser.open("map3.html")
    return 

def map_ss(coordinates):
    import folium
    import webbrowser
    from collections import defaultdict

    lat0 = float(coordinates[0][0]["latitude"])
    lon0 = float(coordinates[0][0]["longitude"])
    map = folium.Map(location=[lat0, lon0], zoom_start=7)
    
    utvonal = defaultdict(list)
    start_points = {}
    stop_points = {}

    for ponto in coordinates:
        pos = ponto[0]
        icao = ponto[1]
        lat = float(pos["latitude"])
        lon = float(pos["longitude"])
        utvonal[icao].append((lat, lon))

        if icao not in stop_points:
            stop_points[icao] = (lat, lon)

        start_points[icao] = (lat, lon)

        popup_text = f"{icao}<br>{lat:.5f}, {lon:.5f}"
        marker = folium.Marker(location=(lat, lon), popup=popup_text)
        marker.add_to(map)
        folium.Popup(popup_text, show=True).add_to(marker)

    for icao, coords in utvonal.items():
        folium.PolyLine(coords, tooltip=f"Path of {icao}", weight=3).add_to(map)

    for icao in utvonal.keys():
        latS, lonS = start_points[icao]
        folium.Marker(
            location=(latS, lonS),
            popup=f"{icao} START",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(map)

        latE, lonE = stop_points[icao]
        folium.Marker(
            location=(latE, lonE),
            popup=f"{icao} STOP",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(map)

    map.save("map3_sajat.html")
    webbrowser.open("map3_sajat.html")
    return