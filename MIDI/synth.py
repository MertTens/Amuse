import pygame
import pygame.midi as midi
from midi import MidiConnector
from synthesizer import Player, Synthesizer, Waveform
import math

player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sawtooth, osc2_volume=0.5)

pygame.midi.init()
print(pygame.midi.get_device_info(1))

input_id = pygame.midi.get_default_input_id()
print ("using input_id {}".format(input_id))

i = pygame.midi.Input( input_id )

val = 0
note_list = []
num_list = []

main_list = [[], []]

def update_list(list_in, num_list, midi_dat):
    note_num = midi_dat[0][1]
    note = 2**((note_num-69)/12.0)*440

    if(midi_dat[0][0] != 144):
        return list_in, num_list
    if(midi_dat[0][2] == 0):
        try:
            while(True):
                ind = num_list.index(note_num)
                if ind != -1:
                    list_in.pop(ind)
                    num_list.pop(ind)
        except: 
            return list_in, num_list
    else:
        list_in += [note]
        num_list += [note_num]
    return list_in, num_list
    

while(True):
    if(i.poll()):
        # read = midi.device.read(1)[0];
        read = i.read(10)[0]
        # print(read)
        # if(read[0][0] == 144 and read[0][1] != 0):
        #     val = int(read[0][1]);

        note_list, num_list = update_list(note_list, num_list, read)
    if(len(note_list) > 0):
        player.play_wave(synthesizer.generate_chord(note_list, 0.1)) # using chord to be able to play more notes as once
