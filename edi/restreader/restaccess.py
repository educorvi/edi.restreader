# -*- coding: utf-8 -*-
import requests
import psycopg2
import json
from time import time

login = {'login': 'restaccess', 'password': 'H9jCg768'}
authurl = u'http://emissionsarme-produkte.bgetem.de/@login'
searchurl = u'http://emissionsarme-produkte.bgetem.de/@search'

def getAuthToken():
    headers = {'Accept': 'application/json'}
    token = requests.post(authurl, headers=headers, json=login)
    return token.json().get('token')

def getCatalogData(query):
    token = getAuthToken()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % token,
        }
    results = requests.get(searchurl, headers=headers, params=query)
    return results.json().get('items')

def possibleGefahrstoffe():
    terms = []
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    for i in entries:
        print(i)

def getHersteller():
    payload = {'portal_type': 'nva.chemiedp.hersteller',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getMachines():
    payload = {'portal_type': 'nva.chemiedp.maschine',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getPowders():
    payload = {'portal_type': 'nva.chemiedp.druckbestaeubungspuder',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getEtiketten():
    payload = {'portal_type': 'nva.chemiedp.reinigungsmitteletiketten',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getManuell():
    payload = {'portal_type': 'nva.chemiedp.reinigungsmittelmanuell',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getProduktdatenblatt():
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getHeatset():
    payload = {'portal_type': 'nva.chemiedp.heatsetwaschmittel',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

if __name__ == "__main__":
    hostname = 'localhost'
    username = 'postgres'
    database = 'gefahrstoff'

    erg = getHersteller()
    erg2 = getMachines()
    erg3 = getPowders()
    erg4 = getEtiketten()
    erg5 = getManuell()
    erg6 = getProduktdatenblatt()
    erg7 = getHeatset()
    conn = psycopg2.connect(host = hostname, user=username, dbname=database)

    for i in erg:
        hersteller_title = i.get('title')
        hersteller_desc = i.get('description')
        hersteller_uid = i.get('UID')
        hersteller_link = i.get('@id')
        cur = conn.cursor()
        #cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO manufacturer (title, description, webcode, image_id) VALUES (%s, %s, %s, NULL);", (hersteller_title, hersteller_desc, hersteller_uid))
        conn.commit()
        print(hersteller_title)# correct
        cur.close()

    for i in erg2:
        machine_title = i.get('title')
        machine_desc = i.get('description')
        machine_uid = i.get('UID')
        machine_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO printing_machine (title, description, webcode, image_url) VALUES (%s, %s, %s, NULL);",
                    (machine_title, machine_desc, machine_uid))
        conn.commit()
        print(machine_title)  # correct
        cur.close()

    for i in erg3:
        powder_title = i.get('title')
        powder_desc = i.get('description')
        powder_uid = i.get('UID')
        powder_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO spray_powder (title, description, webcode, image_url) VALUES (%s, %s, %s, NULL);",
                    (powder_title, powder_desc, powder_uid))
        conn.commit()
        print(powder_title)  # correct
        cur.close()

    for i in erg4:
        etikett_title = i.get('title')
        etikett_desc = i.get('description')
        etikett_uid = i.get('UID')
        etikett_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO substance_mixture (title, description, webcode, substance_type, image_url) VALUES (%s, %s, %s, 'detergent_labels', NULL);",
                    (etikett_title, etikett_desc, etikett_uid))
        conn.commit()
        print(etikett_title)  # correct
        cur.close()
        
    for i in erg5:
        manuell_title = i.get('title')
        manuell_desc = i.get('description')
        manuell_uid = i.get('UID')
        manuell_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO substance_mixture (title, description, webcode, substance_type, image_url) VALUES (%s, %s, %s, 'detergent_manual', NULL);",
                    (manuell_title, manuell_desc, manuell_uid))
        conn.commit()
        print(manuell_title)  # correct
        cur.close()
    
    for i in erg6:
        datenblatt_title = i.get('title')
        datenblatt_desc = i.get('description')
        datenblatt_uid = i.get('UID')
        datenblatt_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute(
            "INSERT INTO substance_mixture (title, description, webcode, substance_type, image_url) VALUES (%s, %s, %s, 'product_datasheet', NULL);",
            (datenblatt_title, datenblatt_desc, datenblatt_uid))
        conn.commit()
        print(datenblatt_title)  # correct
        cur.close()

    for i in erg7:
        heatset_title = i.get('title')
        heatset_desc = i.get('description')
        heatset_uid = i.get('UID')
        heatset_link = i.get('@id')
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute(
            "INSERT INTO substance_mixture (title, description, webcode, substance_type, image_url) VALUES (%s, %s, %s, 'detergent_heatset', NULL);",
            (heatset_title, heatset_desc, heatset_uid))
        conn.commit()
        print(heatset_title)  # correct
        cur.close()

    #    insert = "INSERT INTO manufacturer(title, description) (%s, %s)" % (hersteller_title, hersteller_desc)
    #    cur.execute(insert)
    #    cur.fetchall()
    conn.close()