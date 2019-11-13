def setupMuse(self, muse): #sets preset for muse and return characteristic objects for all eeg GATT channels
        services = muse.getServices()
        preset1 = bytearray([0x02, 0x64, 0x0a]) #this preset is for 4 channels and aux
        preset2 = bytearray([0x04, 0x70, 0x32, 0x30, 0x0a])
        #channels = [0,0] #zero'ed array to hold the 5 eeg channels
        for service in services:
            print("uuid:", service.uuid)
            characteristics = service.getCharacteristics()
            for characteristic in characteristics:
                handle = characteristic.getHandle()
                print("Handle: {}, Properties: {}".format(handle, characteristic.propertiesToString()))
                if handle == 14:
                    characteristic.write(preset2) #specify the preset
                    characteristic.write(preset1) #specify the preset
                    print("Wrote preset to GATT 14")

        #sample are received in this order : 44, 41, 38, 32, 35 #we send a byte code 1 to the characteristic ONE AFTER each eeg characteristic to enable notify
        eegChannels = [44,41,38,32,35]
        for channel in eegChannels:
            #print("Setup notify on GATT {}".format(channel))
            try:
                muse.writeCharacteristic(channel+1 , (1).to_bytes(2, byteorder='little'))
            except Exception:
                print("---E1---")
            finally:
                pass



def setupMuse(self, muse): #sets preset for muse and return characteristic objects for all eeg GATT channels
        services = muse.getServices()
        preset1 = bytearray([0x02, 0x64, 0x0a]) #this preset is for 4 channels and aux
        preset2 = bytearray([0x04, 0x70, 0x32, 0x30, 0x0a])
        #channels = [0,0] #zero'ed array to hold the 5 eeg channels
        for service in services:
            print("uuid:", service.uuid)
            characteristics = service.getCharacteristics()
            for characteristic in characteristics:
                handle = characteristic.getHandle()
                print("Handle: {}, Properties: {}".format(handle, characteristic.propertiesToString()))
                if handle == 14:
                    characteristic.write(preset2) #specify the preset
                    characteristic.write(preset1) #specify the preset
                    print("Wrote preset to GATT 14")

        #sample are received in this order : 44, 41, 38, 32, 35 #we send a byte code 1 to the characteristic ONE AFTER each eeg characteristic to enable notify
        eegChannels = [44,41,38,32,35]
        for channel in eegChannels:
            #print("Setup notify on GATT {}".format(channel))
            try:
                muse.writeCharacteristic(channel+1 , (1).to_bytes(2, byteorder='little'))
            except Exception:
                print("---E1---")
            finally:
                pass
