#tiek importētas nepieciešamas bibliotēkas
import PySimpleGUI as sg
import sqlite3
import json

#datubāzes izveidošana, tabulu pasūtījums un pasūtītājs aprakstīšana
conn=sqlite3.connect('kontaktinfo.db')
query=('''CREATE TABLE IF NOT EXISTS PASUTIJUMS
          (ID INTEGER PRIMARY KEY,
          NOSAUKUMS TEXT NOT NULL,
          AUTORS TEXT NOT NULL);''')
conn.execute(query)

query=(''' CREATE TABLE  IF NOT EXISTS PASUTITAJS
           (ID  INTEGER PRIMARY KEY,
           VARDS TEXT NOT NULL,
           UZVARDS TEXT NOT NULL,
           TEL_NR  INTEGER NOT NULL,
           ADRESE TEXT NOT NULL,
           GRAMATAS_ID INTEGER NOT NULL,
           FOREIGN KEY(GRAMATAS_ID) REFERENCES PASUTIJUMS(ID));''' )
conn.execute(query)


#Ievadīta teksta no pasūtījums importēšana teksta failā,izmantojot json
cursor = conn.cursor()
datne1=open('pasutijums.txt','w')
sqlite_select_query = """SELECT * from PASUTIJUMS"""
cursor.execute(sqlite_select_query )
results = cursor.fetchall()
json.dump(results,datne1)
datne1.close()

# Ievadīta teksta no pasūtītājs importēšana teksta failā,izmantojot json
datne2 = open('pasutitajs.txt', 'w')
sqlite_select_query2 = """SELECT * from PASUTITAJS"""
cursor.execute(sqlite_select_query2 )
results2 = cursor.fetchall()
json.dump(results2,datne2)
datne2.close()

'''
cursor = conn.cursor()
f = open('pasutijums.txt', 'w')
sqlite_select_query = """SELECT * from PASUTIJUMS"""
cursor.execute(sqlite_select_query )
results = cursor.fetchall()
for row in results:
    s = str(row)
    f.write(s)
f.close()
'''

'''
# to txt from pasutitajs
f = open('pasutitajs.txt', 'w')
sqlite_select_query = """SELECT * from PASUTITAJS"""
cursor.execute(sqlite_select_query )
results = cursor.fetchall()
for row in results:
    s = str(row)
    f.write(s)
f.close()
'''

#Programmas trešā loga aprakstīšana, ievadīto vērtību ievietošana datubāzē

def izdarit():
    sg.theme('LightBlue')
    tresais_logs_layout=[[sg.Text('Lai pasūtītu grāmatu,ievadi savus datus!')],
                         [sg.Text('Ievadi savu vārdu: ')],
                         [sg.Input(key='-VARDS-')],
                         [sg.Text('Ievadi savu uzvārdu: ')],
                         [sg.Input(key='-UZVARDS-')],
                         [sg.Text('Ievadi savu telefona numuru: ')],
                         [sg.Input(key='-TEL_NR-')],
                         [sg.Text('Ievadi savu adresi: ')],
                         [sg.Input(key='-ADRESE-')],
                         [sg.Button('Pasūtīt!'), sg.Button('Iziet!')]]
    tresais_logs=sg.Window('Datu ievadīšana',tresais_logs_layout,modal=True)
    while True:
         event,values=tresais_logs.read()
         if event=='Iziet!' or event==sg.WINDOW_CLOSED:
              break
         elif event=='Pasūtīt!':
            gramatas_id = 1
            sg.Popup('Paldies par pasūtījumu!')
            ievietot_info1(values['-VARDS-'],values['-UZVARDS-'],values['-TEL_NR-'],values['-ADRESE-'], gramatas_id)
            window.close()
            break
            

def ievietot_info1(vards,uzvards,tel_nr,adrese, gramatas_id):
    conn=sqlite3.connect('kontaktinfo.db')
    conn.execute("INSERT INTO PASUTITAJS(VARDS,UZVARDS,TEL_NR,ADRESE, GRAMATAS_ID)\
                 VALUES(?,?,?,?,?)",(vards,uzvards,tel_nr,adrese, gramatas_id))
    conn.commit()
    conn.close()
    
    
#Programmas otrā loga aprakstīšana,ievadīto vērtību ievietošana datubāzē
def darit():
     sg.theme('LightBlue')
     otrais_logs_layout=[[sg.Text('Ievadi grāmatas nosaukumu: ')],
                       [sg.Input(key='-NOSAUKUMS-')],
                       [sg.Text('Ievadi grāmatas autoru:')],
                       [sg.Input(key='-AUTORS-')],
          [sg.Button('Ievadīt'),sg.Button('Iziet!')]
          ]  
     otrais_logs=sg.Window('Random grāmata',otrais_logs_layout, modal=True)  
     while True:
         event,values=otrais_logs.read()
         if event=='Iziet!' or event==sg.WINDOW_CLOSED:
              break
         elif event=='Ievadīt':
              ievietot_info(values['-NOSAUKUMS-'],values['-AUTORS-'])
              window.close()
              izdarit()
              break
        
     otrais_logs.close()
def ievietot_info(nosaukums,autors):
    conn=sqlite3.connect('kontaktinfo.db')
    conn.execute("INSERT INTO PASUTIJUMS(NOSAUKUMS,AUTORS)\
                 VALUES(?,?)",(nosaukums,autors))
    conn.commit()
    conn.close()


#Programmas pirmā loga aprakstīšana
sg.theme('Reddit')
layout=[
    [sg.Text('Esi sveicināts grāmatu pasūtīšanas sistēmā! Seko noradījumiem, lai pasūtītu grāmatu!Ja esi gatavs, spied pogu "Uz priekšu!" ')],
    [sg.Button('Uz priekšu!'), sg.Button('Iziet!')]
]
window=sg.Window('Grāmatas',layout)

while True:
     event,values=window.read()
     if event=='Iziet!' or event==sg.WINDOW_CLOSED:
          break
     elif event == 'Uz priekšu!':
       darit() 
window.close()
