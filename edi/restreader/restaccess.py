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

if __name__ == "__main__":
    hostname = 'localhost'
    username = 'seppowalther'
    database = 'gefahrstoff'

    erg = getHersteller()
    conn = psycopg2.connect(host = hostname, user=username, dbname=database)
    for i in erg:
        hersteller_title = i.get('title')
        hersteller_desc = i.get('description')
        hersteller_uid = i.get('UID')
        hersteller_link = i.get('@id')
        cur = conn.cursor()
        #cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO manufacturer (title, description, webcode, manufacturer_image_id) VALUES (%s, %s, %s, NULL);", (hersteller_title, hersteller_desc, hersteller_uid))
        conn.commit()
        print(hersteller_title)# correct
        cur.close()

    #    insert = "INSERT INTO manufacturer(title, description) (%s, %s)" % (hersteller_title, hersteller_desc)
    #    cur.execute(insert)
    #    cur.fetchall()
    conn.close()