#!/bin/bash
echo "Instalando librerias"
apt-get install python-pip python-opencv python-qt4 python-pyaudio python-requests python-numpy python-xlib
echo 's'
pip install pyglet

cd PyUserInput-master
python setup.py build
python setup.py install
cd ..
cd ..
cd sound
mkdir tmp
chmod 777 -R tmp
cd ..
echo "Finalizando Instalacion"
