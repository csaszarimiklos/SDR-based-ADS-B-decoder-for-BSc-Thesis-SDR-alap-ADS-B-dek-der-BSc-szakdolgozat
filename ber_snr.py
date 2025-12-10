import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from crccheck.crc import Crc
def crc(mess):
    byte_data = np.packbits(mess).tobytes()
    my_crc = Crc(width=24,poly=0x1FFF409,initvalue=0,xor_output=0,reflect_input=False,reflect_output=False)
    checksum = my_crc.calc(byte_data)
    checksum = format(checksum,"024b")
    checksum = np.array([int(b) for b in checksum], dtype=np.uint8)
    bits = np.concatenate((mess,checksum))
    #print("ez az eredeti bitsorozat crcve: ",bits)
    return bits

def jelgenerator(amp):
    preamble = amp*np.array([1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0])
    df = np.array([1,0,0,0,1])
    random = np.random.randint(0,2,83)
    mess = np.concatenate((df,random))
    mess =crc(mess)
    mess = amp*mess
    mess_new = np.array(preamble)
    for n in range(112):
        if mess[n] == 0:
            mess_new = np.append(mess_new,0)
            mess_new = np.append(mess_new,amp)
        else:
            mess_new = np.append(mess_new,amp)
            mess_new = np.append(mess_new,0)
    mess = mess_new
    Ps = np.sum(mess**2)/len(mess)
    Ps = 10*np.log10(Ps)
    return mess,Ps


def zajgenerator (Ps,SNR,length):
    sigma_negyzet = Ps-SNR
    sigma_negyzet = 10**(sigma_negyzet/10)
    sigma = np.sqrt(sigma_negyzet)
    noise = np.random.normal(0,sigma,length)
    Pn = np.sum(noise**2)/length
    return noise,Pn


def tesztjel(Ps,SNR):
    amp = np.sqrt(2*(10**(Ps/10)))
    sig,Psig = jelgenerator(amp)
    noise,Pn = zajgenerator(Ps,SNR,len(sig))
   
    Pn = 10*np.log10(Pn)
    SNR_ = Psig-Pn
    s_n = sig+noise 
    p = np.sum(s_n**2)/len(s_n)
    p = 10*np.log10(p)
    return s_n,SNR_,p

def tesztjelek(x,SNR,Ps):
    iq_samples = np.array([0])
    avgSNR = avgP = 0
    for i in range(x):
        sig, SNR_sig, p_sig = tesztjel(Ps,SNR)   
        noise,Pn = zajgenerator(Ps,SNR,240)
        iq_samples = np.append(iq_samples,sig)
        iq_samples = np.append(iq_samples,noise)
        avgSNR = avgSNR + SNR_sig
        avgP = avgP + p_sig
    avgSNR = avgSNR/x
    avgP = avgP/x
    return iq_samples, avgSNR,avgP



from functions import open,resample,preamble,search,messages,decoder,planes,planes_coordinates, coordinates, map,messages_megujabb
from collections import defaultdict
from lut import position
from ber_snr import tesztjelek

def ber__snr(snr_,Ps_,x_):
    
    Ps = Ps_
    SNR = snr_
    x = x_
    iq_samples,snr,p = tesztjelek(x,SNR,Ps)
    #print("HOSSZ",len(iq_samples))
    """dev_snr = 100*abs(SNR-snr)/SNR
    dev_p = 100*abs(Ps-p)/Ps
    print(dev_snr,dev_p)"""

    #fs = 2000000
    fs = 2400000
    num_frames = 1
    #print(fs)

    iq_samples,up,down,Ts = resample(iq_samples,fs)
    #print("HOSSZ UJRAMINTAVETEL UTAN",len(iq_samples))

    preamble_df,Ts = preamble(up=up,down=down,num_frames=num_frames,Ts=Ts)
    #print(len(preamble_df))

    arg = search(iq_samples,preamble_df)
    #print("SSSSS",Ts)
    #print("arg: elvileg ennyi stimmelő preamble rész van",len(arg))
    messages_,num_good= messages_megujabb(arg,iq_samples,Ts)
    #messages_,num_good= messages(arg,iq_samples,Ts)
    """print("Összes üzenet/Preamble egyezések: ",num_osszes,num_sum2 )
    print("Jó/beadott: ", 100*num_good/x)
    """
    rate = 100*num_good/x
    #print("num_good, x: ",num_good,x)
    return rate

def fgv(start,stop,delta,Ps_,x_):
    x = np.array([0])
    y = np.array([0])
    for i in range(start,stop,delta):
        rate = ber__snr(i,Ps_,x_)
        x = np.append(x,i)
        y = np.append(y,rate)
    return x,100-y