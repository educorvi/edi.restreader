# -*- coding: utf-8 -*-
import unicodedata
import re
from restclient import GET, POST, PUT, DELETE
import requests
import json
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from plone.memoize import ram
from time import time
from plone import api as ploneapi

login = {'login': 'restaccess', 'password': 'H9jCg768'}
#login = {'login': 'admin', 'password': 'Bg2011eteM'}
authurl = u'https://emissionsarme-produkte.bgetem.de/@login'
#authurl = u'http://10.33.202.24:8080/portal/@login'
searchurl = u'https://emissionsarme-produkte.bgetem.de/@search'
#searchurl = u'http://10.33.202.24:8080/portal/@search'

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
    print len(results.json().get('items'))
    #exampleid: https://emissionsarme-produkte.bgetem.de/datenbank-chemie-dp/produktliste-wasch-und-reinigungsmittel-im-offsetdruck/win-wash-hsac
    return results.json().get('items')

@ram.cache(lambda *args: time() // (60 * 60))
def possibleGefahrstoffe(context):
    terms = []
    #terms.append(SimpleVocabulary.createTerm(u'auswahl', u'auswahl', u'bitte auswählen'))
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    for i in entries:
        print(i.get('@id'))
        terms.append(SimpleVocabulary.createTerm(i.get('@id'), i.get('UID'), i.get('title')))
    return SimpleVocabulary(terms)
directlyProvides(possibleGefahrstoffe, IContextSourceBinder)

def getExternalGefahrstoffe():
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    return entries

def getNewAuthToken():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    dburl = 'https://praevention.uv-kooperation.de/@login'
    dblogin = {'login': 'admin', 'password': 'Bg2011eteM'}
    token = requests.post(dburl, headers=headers, json=dblogin, verify=False)
    print 'Token',token
    return token.json().get('token')

def getNewGefahrstoffe():
    token = getNewAuthToken()
    print(token)
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % token,
        }
    dataurl = 'https://praevention.uv-kooperation.de/emissionsarme-produkte/gefahrstoffliste'
    results = requests.get(dataurl, headers=headers, verify=False)
    return results.json()

def externalGefahrstoffList():
    terms = []
    #entries = getExternalGefahrstoffe()
    entries = getNewGefahrstoffe()
    clearids = []
    for i in entries:
        testid = i.get('@id').replace('https://', 'http://')
        clearid = i.get('@id').split('/')[-1]
        if clearid not in clearids:
            clearids.append(clearid)
            #if ploneapi.content.find(portal_type='Schutzhandschuh', Gefahrstoffe=i.get('@id')):
            terms.append(SimpleVocabulary.createTerm(testid, clearid, i.get('title')))
        else:
            print(clearid)
    return terms

def getExternalGefahrstoff(url):
    url = url.replace('http://', 'https://')
    payload = {'gemischid': url}
    newurl = 'https://praevention.uv-kooperation.de/emissionsarme-produkte/gefahrstoff'
    token = getAuthToken()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % token,
        }
    result = requests.get(newurl, params=payload, auth=('admin', 'Bg2011eteM'), headers=headers, verify=False)
    print(result.json())
    return result.json() 
