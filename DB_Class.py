#!/usr/bin/env python
import os
import sqlite3 as lite

path = os.getcwd()
# print path

class dataBase():
    ## Clase que interactua con la base de datos

    def createCon(self):
        global con
#        con = lite.connect('ClubMarsellosa.db')
        con = lite.connect('registro')


    def interAct(self, query):
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def closeCon(self):
        if con:
            con.close()

    def crearTablas(self): pass

    # codigo para crear o formatear tablas en la bd

    def fillTables(self): pass

    def last_row_id(self): pass

