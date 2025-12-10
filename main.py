from functions import open,resample,preamble,search,messages,decoder,planes,planes_coordinates, coordinates, map,map_ss,messages_megujabb
from collections import defaultdict
from lut import position
from ber_snr import tesztjelek
from helymeghat import coordinates_jo,mi_a_tc


filename = "adsb_downloaded.wav"## ide kell a fájl neve
#print("elkezdte")
iq_samples,num_frames,fs = open(filename)
#print(iq_samples[0:10000])
#print(type(iq_samples),len(iq_samples))
#print(fs)
"""
Ps = 95
SNR = 0
x = 1000
iq_samples,snr,p = tesztjelek(x,SNR,Ps)
print("SNR: ",snr,"\n","P: ",p,"\n","Üzenetek száma: ",x)
dev_snr = 100*abs(SNR-snr)/SNR
dev_p = 100*abs(Ps-p)/Ps
print(dev_snr,dev_p)
fs = 2000000
num_frames = 1
"""

iq_samples,up,down,Ts = resample(iq_samples,fs)
#print(Ts)

preamble_df,Ts = preamble(up=up,down=down,num_frames=num_frames,Ts=Ts)
#print(len(preamble_df))

arg = search(iq_samples,preamble_df)

#print("Arg: ",len(arg))
#messages_,df_bits,ca_bits,icao_bits,me_bits,pi_bits,type_code_bits,err_mess,num_good,num_err,num_osszes,num_sum2,raw_messages= messages(arg,iq_samples,Ts)
#print("idáig eljutott, arg megvan")

#Választani a két keresési algoritmus közt#
#messages_ ,num_good= messages_megujabb(arg,iq_samples,Ts)
messages_ ,num_good= messages(arg,iq_samples,Ts)


"""
#print("ÜZENETEK HOSSZA",len(messages_))
#print("Összes üzenet/Preamble egyezések: ",num_osszes,num_sum2 )
#print("Jó/beadott: ", 100*num_good/x)
#print("Jó üzenetek: ",num_good)
#print("Hibás üzenetek: ",num_err)
#print("Találati ráta: ", 100*num_good/num_osszes)
#print(len(messages_))"""
"""for i in messages_:
    typecode, cap,icao,message = decoder(i)
    print(icao,"&",cap,"&",typecode,"&",message," hline")
"""
#print(len(messages_))
#print("kerestünk")

coords = coordinates_jo(messages_)


#for i in coords:
#    if (i[1] == "AE145F") or (i[1] == "4CA92D") or (i[1] == "4401B7"):
#        print(i[1], i[0]["latitude"],i[0]["longitude"])
#coords = coordinates(messages_)
#print(coords)5
#print("koordinatak megvannal")
#map(coords)

#Kirajzoláshoz#
map_ss(coords)

#Üzenetek kiírása#
"""
for i in messages_:
    typecode,cap,icao,mess = decoder(i)
    if (9 <= typecode <= 18):
        print(typecode,mess)"""