# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 18:20:36 2019

@author: ebarreto
"""
#Timestamp library
from datetime import datetime

#Import library for SQLite
import sqlite3
#define the path for instaling the sqlite database
path = r'/home/ebarreto/Desktop/teste/Kamonohash/Projeto_Kamonobot/RPI/IOTA_SEED_ELIABEL0'
#create an object to conection
conn = sqlite3.connect(path)
#create the object to control the database
cursor = conn.cursor()

#Create a table for storage the Iota Info
cursor.execute('''
CREATE TABLE IF NOT EXISTS Eliabel0 (
    Hash Text PRIMARY KEY NOT NULL UNIQUE,
    Timestamp Integer NOT NULL,
    Hash_first TEXT NOT NULL,
    Hash_last TEXT NOT NULL,
	Name TEXT DEFAULT "Not identified",
	Number TEXT DEFAULT "Not identified",
    Color TEXT DEFAULT "Not identified",
    Value Integer DEFAULT 0,
    Confirmed Integer DEFAULT 1,
    Requested Integer DEFAULT 0,
    Delivery  Integer DEFAULT 0  
);
''')

#Import library for Iota
from iota import Iota

#define API - para realizar as comunicações
Eliabel0 = Iota('https://nodes.thetangle.org:443',b'SEEDS9GOES9HERE')
Eliabel1 = Iota('https://nodes.thetangle.org:443',b'SEEDS9GOES9HERE')


#Lê todas as informações da rede TANGLE referente aquela SEED
print("Collecting info from Tangle. Wait please...")
now = datetime.now()
print("Start collecting at:  ", now.strftime("%Y/%m/%d - %H:%M:%S"))

while True:
    while True:
        try:
            bundles_info = Eliabel0.get_transfers()
            now = datetime.now()
            print("Last info updated at: ", now.strftime("%Y/%m/%d - %H:%M:%S"))
            break
        except:
            print('  Conection error on Tangle/Node. Trying again, please wait...')
            now = datetime.now()
            print("  Errot at: ", now.strftime("%Y/%m/%d - %H:%M:%S"))
    
    #Reading bundle transactions
    num_bundle = 0
    list_test = list()
    list_db = list()
    for bundle in bundles_info['bundles']:
        num_transaction = 0
        if bundle.tail_transaction.bundle_hash == b'999999999999999999999999999999999999999999999999999999999999999999999999999999999':
            continue
        if bundle.tail_transaction.bundle_hash in list_test:
            continue
        list_test.append(bundle.tail_transaction.bundle_hash)
        Message=str(bundle.tail_transaction.signature_message_fragment.decode())
        try:
            Name, Number, Color = Message.split(" ")#Separate message by space, format like "Name Number Type"
        except:
            Name, Number, Color = "Not identified", "Not identified", "Not identified"
        hash_first = str(bundle.tail_transaction.bundle_hash)[0:4:1] #First numbers from hash
        hash_last = str(bundle.tail_transaction.bundle_hash)[-4::1]#Last numbers from hash
        list_db.append((str(bundle.tail_transaction.bundle_hash), 
                        int(bundle.tail_transaction.attachment_timestamp), 
                        hash_first, 
                        hash_last, 
                        Name, 
                        Number, 
                        Color, 
                        int(bundle.tail_transaction.value)))
    #to print information on terminal uncoment next lines
    #    print('\n'+50*'-')
    #    print("Numero da info: " + str(num_bundle))
    #    print("Endereço: " + str(bundle.tail_transaction.address))
    #    print("Numero de caracteres do endereço: " +str(len(bundle.tail_transaction.address)))
    #    print("Timestamp anexado: " + str(bundle.tail_transaction.attachment_timestamp))
    #    print("Hash da Transação: " + str(bundle.tail_transaction.bundle_hash))
    #    print("Confirmado: " + str(bundle.tail_transaction.is_confirmed))
    #    print("Ultimo endereço da Bundle: " + str(bundle.tail_transaction.last_index))
    #    print("Mensagem: " + str(bundle.tail_transaction.signature_message_fragment.decode()))
    #    print("Realizado por: " + str(bundle.tail_transaction.tag))
    #    print("Timestamp: " + str(bundle.tail_transaction.timestamp))
    #    print("Valor da transação: ", bundle.tail_transaction.value)
    #    print(50*'-'+'\n') 
        num_bundle += 1
    
    #To see the data before insert on database, uncomment next line
#    print(list_db)
    
    #Insert a several datas on database
    cursor.executemany("""
    INSERT OR IGNORE INTO Eliabel0 (Hash, Timestamp, Hash_first, Hash_last, Name, Number, Color,  Value)
    VALUES  (?,?,?,?,?,?,?,?)
    """, list_db)
    
    #update info on database
    conn.commit()
    
    #Restart the proccess of collecting
    now = datetime.now()
    print("Start collecting at:  ", now.strftime("%Y/%m/%d - %H:%M:%S"))

#fecha a conexão do banco de dados 
conn.close()
