# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 23:57:41 2019

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

while True:
    first_hash = input('Insert the 4 first numbers of your Bundle Hash: ')
    last_hash = input('Insert the 4 last numbers of your Bundle Hash: ')
    cursor.execute('''
                   UPDATE Eliabel0
                   SET Requested = 1
                   WHERE Hash_first = ? AND Hash_last = ?
                   ''', (first_hash, last_hash,))
    conn.commit()
    print()
    print('Take your piece in the table')
    