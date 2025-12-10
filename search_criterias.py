#len(arg)
    #átlagosan a 0-k legyenek kisebbek mint az 1-esek
    max_zeros = 0
    min_ones = 0
    for i in arg:
        max_zeros = np.max([iq_samples[i+2],iq_samples[i+3],
                            iq_samples[i+3*2],iq_samples[i+3*2+1],
                            iq_samples[i+4*2],iq_samples[i+4*2+1],
                            iq_samples[i+5*2],iq_samples[i+5*2+1],
                            iq_samples[i+6*2],iq_samples[i+6*2+1],
                            iq_samples[i+10*2],iq_samples[i+10*2+1],
                        iq_samples[i+11*2],iq_samples[i+11*2+1],
                        iq_samples[i+12*2],iq_samples[i+12*2+1],
                        iq_samples[i+13*2],iq_samples[i+13*2+1],
                        iq_samples[i+14*2],iq_samples[i+14*2+1],
                        iq_samples[i+15*2],iq_samples[i+15*2+1]
                        ])
        min_ones = np.min([iq_samples[i],iq_samples[i+1],iq_samples[i+4],iq_samples[i+5],iq_samples[i+7*2],iq_samples[i+7*2+1],iq_samples[i+9*2],
                        iq_samples[i+9*2+1],iq_samples[i+16*2],iq_samples[i+16*2+1],
                        iq_samples[i+19*2],iq_samples[i+19*2+1],iq_samples[i+21*2],iq_samples[i+21*2+1],iq_samples[i+23*2],iq_samples[i+23*2+1],
                        iq_samples[i+24*2],iq_samples[i+24*2+1]
                        ])
        if (min_ones < max_zeros):
            arg.remove(i)
    #len(arg)

    # átlagosan legyenek elég messze a 0-k és 1-esek
    A  = 0
    for i in arg:
        min =np.min([iq_samples[i+3*2],iq_samples[i+3*2+1],
                            iq_samples[i+4*2],iq_samples[i+4*2+1],
                            iq_samples[i+5*2],iq_samples[i+5*2+1],
                            iq_samples[i+6*2],iq_samples[i+6*2+1],
                            iq_samples[i+10*2],iq_samples[i+10*2+1],
                        iq_samples[i+11*2],iq_samples[i+11*2+1],
                        iq_samples[i+12*2],iq_samples[i+12*2+1],
                        iq_samples[i+13*2],iq_samples[i+13*2+1],
                        iq_samples[i+14*2],iq_samples[i+14*2+1],
                        iq_samples[i+15*2],iq_samples[i+15*2+1]
                        ])
        max = np.max([iq_samples[i],iq_samples[i+1],iq_samples[i+4],iq_samples[i+5],iq_samples[i+7*2],iq_samples[i+7*2+1],iq_samples[i+9*2],
                        iq_samples[i+9*2+1],iq_samples[i+16*2],iq_samples[i+16*2+1],
                        iq_samples[i+19*2],iq_samples[i+19*2+1],iq_samples[i+21*2],iq_samples[i+21*2+1],iq_samples[i+23*2],iq_samples[i+23*2+1],
                        iq_samples[i+24*2],iq_samples[i+24*2+1]
                        ])
        A = max-min
        avg_zeros = np.average([iq_samples[i+3*2],iq_samples[i+3*2+1],
                            iq_samples[i+4*2],iq_samples[i+4*2+1],
                            iq_samples[i+5*2],iq_samples[i+5*2+1],
                            iq_samples[i+6*2],iq_samples[i+6*2+1],
                            iq_samples[i+10*2],iq_samples[i+10*2+1],
                        iq_samples[i+11*2],iq_samples[i+11*2+1],
                        iq_samples[i+12*2],iq_samples[i+12*2+1],
                        iq_samples[i+13*2],iq_samples[i+13*2+1],
                        iq_samples[i+14*2],iq_samples[i+14*2+1],
                        iq_samples[i+15*2],iq_samples[i+15*2+1]
                        ])
        avg_ones = np.average([iq_samples[i],iq_samples[i+1],iq_samples[i+4],iq_samples[i+5],iq_samples[i+7*2],iq_samples[i+7*2+1],iq_samples[i+9*2],
                        iq_samples[i+9*2+1],iq_samples[i+16*2],iq_samples[i+16*2+1],
                        iq_samples[i+19*2],iq_samples[i+19*2+1],iq_samples[i+21*2],iq_samples[i+21*2+1],iq_samples[i+23*2],iq_samples[i+23*2+1],
                        iq_samples[i+24*2],iq_samples[i+24*2+1]
                        ])
        if ((avg_ones-avg_zeros) < (3*A/4)):
            arg.remove(i)
    #len(arg)
    # az összes 0 legyen az átlag 1 alatt
    for i in arg:
        avg_ones = np.average([iq_samples[i],iq_samples[i+1],iq_samples[i+4],iq_samples[i+5],iq_samples[i+7*2],iq_samples[i+7*2+1],iq_samples[i+9*2],
                        iq_samples[i+9*2+1],iq_samples[i+16*2],iq_samples[i+16*2+1],
                        iq_samples[i+19*2],iq_samples[i+19*2+1],iq_samples[i+21*2],iq_samples[i+21*2+1],iq_samples[i+23*2],iq_samples[i+23*2+1],
                        iq_samples[i+24*2],iq_samples[i+24*2+1]
                        ])
        if (iq_samples[i+3*2] > avg_ones or
            iq_samples[i+3*2+1] > avg_ones or
            iq_samples[i+4*2] > avg_ones or
            iq_samples[i+4*2+1] > avg_ones or
            iq_samples[i+5*2] > avg_ones or
            iq_samples[i+5*2+1] > avg_ones or
            iq_samples[i+6*2] > avg_ones or
            iq_samples[i+6*2+1] > avg_ones or
            iq_samples[i+10*2] > avg_ones or
            iq_samples[i+10*2+1] > avg_ones or
            iq_samples[i+11*2] > avg_ones or
            iq_samples[i+11*2+1] > avg_ones or
            iq_samples[i+12*2] > avg_ones or
            iq_samples[i+12*2+1] > avg_ones or
            iq_samples[i+13*2] > avg_ones or
            iq_samples[i+13*2+1] > avg_ones or
            iq_samples[i+14*2] > avg_ones or
            iq_samples[i+14*2+1] > avg_ones or
            iq_samples[i+15*2] > avg_ones or
            iq_samples[i+15*2+1] > avg_ones
            ):
            arg.remove(i)
    #len(arg)