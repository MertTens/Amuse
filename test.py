from muse2 import *
import delegate
import time

museAddress = '00:55:da:b5:0d:79'


def eeg(data,trash=True):
	global callbackTime
	callbackTime=time.time()
	eeg1 = data[0]
	eeg2 = data[1]
	eeg3 = data[2]
	eeg4 = data[3]
	eeg5 = data[4]
	for i in range(12):
		print("{0}\n".format(eeg5[i]))
		# processEEG( eeg1[i], eeg2[i], eeg3[i], eeg4[i], eeg5[i])




muse = Muse(callback=eeg, address=museAddress)

while True:
	time.sleep(1)
