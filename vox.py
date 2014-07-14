import sys
import requests
from pyaudio import PyAudio, paInt16
from wave import open as open_audio
from os import system
from json import loads
from ruido import *

class Vox:
    
    def __init__(self, file="sound/tmp/audio"):
        self.format = paInt16
        #self.rate = 48000
        self.rate = 16000
        self.channel = 1
        self.chunk = 1024
        self.file = file
        #final es una palabra reservada para nosotros
        self.IGNORE = ['confidence','transcript','result_index','final',':true}],',':0}\n','}],',':','},{','{','']

    def record(self, time, device_i=None):
        audio = PyAudio()
        print audio.get_device_info_by_index(1)
        stream = audio.open(input_device_index=device_i,output_device_index=device_i,format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        playDing()
        print "REC: "
        frames = []
        for i in range(0, self.rate / self.chunk * time):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        print "END"
        stream.close()
        audio.terminate()
        write_frames = open_audio(self.file, 'wb')
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(audio.get_sample_size(self.format))
        write_frames.setframerate(self.rate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()


    def cadenas(self,lista):
        """Metodo que toma la respuesta de la api de google y toma solo los resultados del reconocimiento de voz"""
        listax = []
        for l in lista:
	    if l not in self.IGNORE and not(l.startswith(':'))and not(l.startswith(','))and not(l.startswith('{')):
	        listax.append(l)
	return listax

    def voz_a_texto(self):
        """Metodo para convertir grabaciones de voz a texto, usando la api de google a traves de internet"""
        #rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 test.wav
        url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=es-ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'
        audio = open("sound/tmp/audio",'rb').read()
        headers = {'Content-Type': 'audio/l16; rate=16000;'}
        respuesta = requests.post(url,data=audio,headers=headers)
        try:
	    listaux = respuesta.content.split('{"result":[]}\n{"result":[{"alternative":[{"transcript":')
	    listaux = listaux[1].split('"')
	    resultados = self.cadenas(listaux)
	    return resultados
	except:
	    print "Error de grabacion o grabacion nula:", sys.exc_info()[0]
	    return ['','']


    def commandAnalysis(self,rta,commands):
        """
        Metodo que realiza un analisis de la respuesta obtenida de convertir la voz a texto.
        Aqui se realiza un analisis de esta respuesta y si contiene un comando valido se ejecuta en consecuencia
        """
        #print rta
        opc=0
	for r in rta:
            for c in commands:
                if c in r:
                    if c == 'pesta':
                        #createTab(self, url)
                        return 1
                    elif c == 'inicio':
		        #loadHome(self)
		        return 2
		    elif c == 'detener':
                        #stop(self)
                        return 3
                    elif c == 'recarga':
		        #reload(self)
		        return 4
        return opc
      
    def start(self,commands):
        """
        Metodo que realiza la toma del audio, realiza una analisis sobre el mismo
        y retorna un comando valido para la ejecucion o 'none' en caso contrario.
        """
        self.record(3)
        rta = self.voz_a_texto()
        return self.commandAnalysis(rta,commands)
        
    