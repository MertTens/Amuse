# Amuse
*Scripts for connecting to the Muse 2 headset.*

So far, the only way I have been able to get any sort of handshake between this computer and the muse is via `bluepy`. 

I am starting on my own version of this whole muse interace thing using bluepy in `amuse`. 

Fortunately, it looks like `bluepy` was released under the GNU Public License.

My goals for this are as follows:
[x] - Connect to the Muse
[x] - Print the services the Muse offers
[x] - Get some sort of information from one of the services.
[ ] - Clarify the EEG vs. other data from the services.
... 

## EEG Output Channels (BluePy 'Services')
The hierarchy appears to be `Peripheral` -> `Services` -> `Characteristics`. You get actual data out of the characteristics. I will now enumerate the different Services and each of their Characteristics.

Service #0, Characteristic #0 is NON-READ
Service #1, Characteristic #0 Value: b'Muse-0D79'
Service #1, Characteristic #1 Value: b'\x00\x00'
Service #1, Characteristic #2 Value: b'\xff\xff\xff\xff\x00\x00\xff\xff'
Service #2, Characteristic #0 is NON-READ
Service #2, Characteristic #1 is NON-READ
Service #2, Characteristic #2 is NON-READ
Service #2, Characteristic #3 is NON-READ
Service #2, Characteristic #4 is NON-READ
Service #2, Characteristic #5 is NON-READ
Service #2, Characteristic #6 is NON-READ
Service #2, Characteristic #7 is NON-READ
Service #2, Characteristic #8 is NON-READ
Service #2, Characteristic #9 is NON-READ
Service #2, Characteristic #10 is NON-READ
Service #2, Characteristic #11 is NON-READ
Service #2, Characteristic #12 is NON-READ
Service #2, Characteristic #13 is NON-READ
Service #2, Characteristic #14 is NON-READ
Service #2, Characteristic #15 is NON-READ
Service #2, Characteristic #16 is NON-READ

My working hypothesis is that Service 1, Characteristic 2 is where our data is hiding. I'm going to go and see what I can get.

Well, none of the readable properties are changing over time when I have it on my head... I'm going to take a look at the code that uses bluepy and see how they decode the input.


## References
Bluepy: https://github.com/IanHarvey/bluepy
Documentation: http://ianharvey.github.io/bluepy-doc/ 

## Files
