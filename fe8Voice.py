import sys
import string
import base64
import urllib.request
import urllib.response
import urllib.error
import urllib.parse
import json
import wave
import pyaudio

#音声合成する言葉を入力
n = input(">>>")

#URL
tts_url ="http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"

#音声合成
tts_command = { 'method':'speak',
'params':['1.1',
 {'language':'ja','text':n,'voiceType':"*",'audioType':"audio/x-wav"}]}

obj_command = json.dumps(tts_command)     # string to json object
obj_command = obj_command.encode('utf-8')
req = urllib.request.Request(tts_url, obj_command)
response = urllib.request.urlopen(req)
received = response.read().decode('utf-8')  # conv bytes to str by decode()
# extract wav file
obj_received = json.loads(received)
tmp = obj_received['result']['audio'] # extract result->audio
speech = base64.decodestring(tmp.encode('utf-8'))

#.waveで出力
f = open ("out.wav",'wb')
f.write(speech)
f.close

#音声合成の音声データを再生
input_filename = 'out.wav'
buffer_size = 4096
wav_file = wave.open ( input_filename , 'rb' )
p = pyaudio.PyAudio ()
stream = p.open (
                 format = p.get_format_from_width ( wav_file . getsampwidth ()) ,
                 channels = wav_file.getnchannels () ,
                 rate = wav_file.getframerate () ,
                 output = True
                 )
remain = wav_file.getnframes ()

while remain > 0:
    buf = wav_file.readframes ( min ( buffer_size , remain ))
    stream.write ( buf )
    remain -= buffer_size

stream.close ()
p.terminate ()
wav_file.close ()
