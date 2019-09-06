# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 17:41:52 2019

@author: ebarreto
"""
#Import library for SQLite
import sqlite3
#define the path for instaling the sqlite database
path = r'C:\Users\ebarreto\Desktop\Kamonohash\Projeto_Kamonobot\RPI\Iota_seed_info.db'
#create an object to conection
conn = sqlite3.connect(path)
#create the object to control the database
cursor = conn.cursor()

#Import library for connection
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host ="192.168.201.20"
host ="127.0.0.1"
port = 10009

print("IP: ", host)
print("Port: ", str(port))

while True:
    print("Trying connection with application. Please, wait...")
    try:
        s.connect((host,port))
        print("   Conected")
        break
    except:
        print("   Conection failed. Trying again..")
        s.close()

while True:
    while True:
        try:
            cursor.execute('''
                           SELECT Color, Hash 
                           FROM Eliabel0
                           WHERE Confirmed=1 AND Requested=1 AND Delivery=0
                           ORDER BY Timestamp
                           ''')
            rows = cursor.fetchall()
            if rows == []:
                print('No new info.')
                continue
            print('New info receive.')
            break
        except:
            print('No new info.')
            continue
    
    if rows[0][0] == 'Not identified':
        s.send('White'.encode())
        print('White')
    else:
        s.send(rows[0][0].encode())
        print(rows[0][0])
    data = s.recv(4).decode()
    if data == 'DONE':
        print('Delivered')
        cursor.execute('''
                       UPDATE Eliabel0
                       SET Delivery = 1
                       WHERE Hash = ?
                       ''', (rows[0][1],))
        print('Updated')
        conn.commit()
    else:
        print('Trying again.')
        pass


s.close ()