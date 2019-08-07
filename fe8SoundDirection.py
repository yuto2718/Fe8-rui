import pyaudio
import wave
from numpy import *
from matplotlib.pyplot import *
import math

CHUNK = 1024*12
fs = 44100;

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=fs,
                output=True,
                input=True)

c = 340
threshold = 65536/100
d = 0.3

framesR = []
framesL = []

while(True):
    idataOrg = stream.read(CHUNK)
    idata = frombuffer(idataOrg, dtype=int16)
    idataR = idata[0::2]
    idataL = idata[1::2]

    if mean(abs(idataR)+abs(idataL)) > threshold:
        idataR = array(idataR, dtype=double)
        idataL = array(idataL, dtype=double)
        correlated = correlate(idataR-mean(idataR),idataL-mean(idataL),"full")
        t = argmax(correlated)-CHUNK
        t = t/(fs*2)
        L = c*t;
        deg = math.degrees(arcsin(L/d))
        print(deg)

print(argmax(correlated)-CHUNK,t)
plot(correlated)
show()
plot(idataR-mean(idataR))
plot(idataL-mean(idataL))
show()

stream.stop_stream()
stream.close()
p.terminate()
