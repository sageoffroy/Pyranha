#!/bin/bash
echo "Instalando librerias"
apt-get install python-pip
apt-get install python-opencv
apt-get install python-pyaudio
pip install pyglet
apt-get install python-xlib
cd PyUserInput-master
python setup.py build
python setup.py install
cd ..
echo "Finalizando Instalacion"
