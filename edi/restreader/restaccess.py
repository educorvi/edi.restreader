# -*- coding: utf-8 -*-
import unicodedata
import re
from restclient import GET, POST, PUT, DELETE
import requests
import json
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides

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

def possibleGefahrstoffe(context):
    terms = []
    terms.append(SimpleVocabulary.createTerm(u'auswahl', u'auswahl', u'bitte auswählen'))
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    for i in entries:
        terms.append(SimpleVocabulary.createTerm(i.get('@id'), i.get('UID'), i.get('title')))
    return SimpleVocabulary(terms)
directlyProvides(possibleGefahrstoffe, IContextSourceBinder)

def externalGefahrstoffList():
    terms = []
    terms.append(SimpleVocabulary.createTerm(u'auswahl', u'auswahl', u'bitte auswählen'))
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    for i in entries:
        terms.append(SimpleVocabulary.createTerm(i.get('@id'), i.get('UID'), i.get('title')))
    return terms
