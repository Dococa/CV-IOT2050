# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:23:02 2023

@author: D0C0C4
"""
import time
import cv2
import numpy as np
import snap7


botella_roja=0
botella_amarilla=0
botella_azul=0

#información del PLC
IP = '192.168.1.200'
RACK = 0
SLOT = 1

DB_NUMBER = 26
START_ADDRESS = 0
SIZE = 6

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

state = plc.get_cpu_state()
print(f'State: {state}')

#lee toda la DB 26
db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)


#dibujar contornos, mostrar informacion y mandar datos al PLC
def dibujar(mask,color,valor):
    
  global botella_roja
  global botella_amarilla
  global botella_azul
  
  global enviar_azul
  global enviar_amarilla
  global enviar_roja
  
  enviar_azul = bytearray(2)
  enviar_amarilla = bytearray(2)
  enviar_roja = bytearray(2)
    
  
    
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 1000: #area minima a tener en cuenta
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1 #detecta centro del objeto
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      nuevoContorno = cv2.convexHull(c) #crea el contorno
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
    
      if valor==1 and botella_azul==0:
          print("azul")
          botella_roja=0
          botella_amarilla=0
          botella_azul=1
          
          #enviar info al PLC botella azul
          snap7.util.set_int(enviar_amarilla,0,0)#ultimo parametro es la informacion a transmitir
          plc.db_write(26,0,enviar_amarilla)  #el segundo parametro es el byte que queremos cambiar
          snap7.util.set_int(enviar_roja,0,0)#enviar 0
          plc.db_write(26,2,enviar_roja)  #al bye 2
          snap7.util.set_int(enviar_azul,0,1)#enviar 1
          plc.db_write(26,4,enviar_azul)  #al byte 4
          print("byte enviado a botella azul")
          #muestra el byte
          '''
          product_status1 = int.from_bytes(db[0:2], byteorder='big')
          print(f'Botella_roja: {product_status1}')
          product_status2 = int.from_bytes(db[2:4], byteorder='big')
          print(f'Botella_amarilla: {product_status2}')
          product_status3 = int.from_bytes(db[4:6], byteorder='big')
          print(f'Botella_azul: {product_status3}')
          '''
          
      if valor==2 and botella_amarilla==0:
          print("amarillo")
          botella_roja=0
          botella_amarilla=1
          botella_azul=0
          
          #enviar info al PLC botella amarilla
          snap7.util.set_int(enviar_amarilla,0,1)#ultimo parametro es la informacion a transmitir
          plc.db_write(26,0,enviar_amarilla)  #el segundo parametro es el byte que queremos cambiar
          snap7.util.set_int(enviar_roja,0,0)#enviar 0
          plc.db_write(26,2,enviar_roja)  #al bye 2
          snap7.util.set_int(enviar_azul,0,0)#enviar 0
          plc.db_write(26,4,enviar_azul)  #al byte 4
          print("byte enviado a botella amarilla")
          #muestra el byte
          '''
          product_status1 = int.from_bytes(db[0:2], byteorder='big')
          print(f'Botella_roja: {product_status1}')
          product_status2 = int.from_bytes(db[2:4], byteorder='big')
          print(f'Botella_amarilla: {product_status2}')
          product_status3 = int.from_bytes(db[4:6], byteorder='big')
          print(f'Botella_azul: {product_status3}')
         '''
          
      if valor==3 and botella_roja==0:
          print("rojo")
          botella_roja=1
          botella_amarilla=0
          botella_azul=0
          #enviar info al PLC botella roja
          snap7.util.set_int(enviar_amarilla,0,0)#ultimo parametro es la informacion a transmitir
          plc.db_write(26,0,enviar_amarilla)  #el segundo parametro es el byte que queremos cambiar
          snap7.util.set_int(enviar_roja,0,1)#enviar 1
          plc.db_write(26,2,enviar_roja)  #al bye 2
          snap7.util.set_int(enviar_azul,0,0)#enviar 0
          plc.db_write(26,4,enviar_azul)  #al byte 4
          print("byte enviado a botella roja")
          #muestra el byte
          '''
          product_status1 = int.from_bytes(db[0:2], byteorder='big')
          print(f'Botella_roja: {product_status1}')
          product_status2 = int.from_bytes(db[2:4], byteorder='big')
          print(f'Botella_amarilla: {product_status2}')
          product_status3 = int.from_bytes(db[4:6], byteorder='big')
          print(f'Botella_azul: {product_status3}')
          '''

cap = cv2.VideoCapture(0)
azulBajo = np.array([105,100,20],np.uint8)
azulAlto = np.array([130,255,255],np.uint8)
amarilloBajo = np.array([25,100,20],np.uint8)
amarilloAlto = np.array([35,255,255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)
redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
  ret,frame = cap.read()
  if ret == True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
    maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskAzul,(255,0,0),1)
    dibujar(maskAmarillo,(0,255,255),2)
    dibujar(maskRed,(0,0,255),3)
    cv2.imshow('Detector de color',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      snap7.util.set_int(enviar_amarilla,0,0)#ultimo parametro es la informacion a transmitir
      plc.db_write(26,0,enviar_amarilla)  #el segundo parametro es el byte que queremos cambiar
      snap7.util.set_int(enviar_roja,0,0)#enviar 0
      plc.db_write(26,2,enviar_roja)  #al bye 2
      snap7.util.set_int(enviar_azul,0,0)#enviar 0
      plc.db_write(26,4,enviar_azul)  #al byte 4
      break
  
cap.release()
cv2.destroyAllWindows()