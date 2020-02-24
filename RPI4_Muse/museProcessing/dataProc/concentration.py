import time

from museProcessing.dataProc.psd import fftPSDBands


def calculateConcenIndex(beta_Sum, smr_Sum, theta_Sum):
    concenIndex = (beta_Sum + smr_Sum) * 10 / theta_Sum
    return concenIndex


def processConcentration(arr, samplingFreq):
    global concen_base
    global start_time
    global first_time
    global guide_index
    global concen_series
    guide_index = 0

    freq, psd, beta_Sum, smr_Sum, theta_Sum = fftPSDBands(arr, sample_f=int(samplingFreq));

    # print("betaSum is {0}, smrSum is {1}, thetaSum is {2}".format(beta_Sum,smr_Sum,theta_Sum))
    # win_len=0
    if (beta_Sum > 0):
        if (smr_Sum > 0):
            if (theta_Sum > 0):
                temp_index = calculateConcenIndex(beta_Sum, smr_Sum, theta_Sum)
                concen_base.append(temp_index)
                """temp=np.mean(concen_base)
                #print("concentration Value=",temp_index)
                #print("concen average is {0}".format(temp))
                #print("current_time is {0}, start_time is {1} ".format(time.time(), start_time+30))
                if((time.time() > start_time + 30) and (first_time)):
                    #print("start_time is {0}, current time is{1}".format(start_time, time.time))
                    print("inside if")
                    first_time=False
                    guide_index=1.3*temp
                if(time.time()-start_time)>30:
                    #print("guide index is {0}".format(guide_index))
                    #print("concenIndex is {0}".format(temp_index))
                    if(temp_index>1.7):
                        print("on!")
                        #GPIO.output(18,GPIO.HIGH)
                    else:
                        print("off!")
                       # GPIO.output(18,GPIO.LOW)
                """


def concentrationIndexOutput():
    global concen_base
    concen_len = len(concen_base)
    # print("length:{0}".format(concen_len))
    cnt_5 = 0
    cnt_10 = 0
    cnt_15 = 0
    cnt_20 = 0
    cnt_30 = 0
    cnt_final = 0;

    for j in range(len(concen_base)):
        if (concen_base[j] < 5):
            cnt_5 += 1
        elif (concen_base[j] < 10):
            cnt_10 += 1
        elif (concen_base[j] < 15):
            cnt_15 += 1
        elif (concen_base[j] < 20):
            cnt_20 += 1
        elif (concen_base[j] < 30):
            cnt_30 += 1
        else:
            cnt_final += 1
    concen_base = []
    outputStr = "0-5:{0},6-10:{1},11-15:{2},16-20:{3},21-30:{4},Over 30:{5}".format(cnt_5, cnt_10,
                                                                                    cnt_15, cnt_20,
                                                                                    cnt_30,
                                                                                    cnt_final)
    return outputStr


def initConcentration():
    global first_time
    global start_time
    global concen_base
    first_time = True
    concen_base = []
    start_time = time.time()
