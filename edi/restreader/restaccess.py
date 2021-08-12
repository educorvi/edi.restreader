# -*- coding: utf-8 -*-
import requests
import psycopg2
import random
import datetime
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

def getItemData(entry):
    token = getAuthToken()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % token,
    }
    results = requests.get(entry.get('@id'), headers=headers)
    return results.json()

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
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched MANUFACTURER: "+i.get('title'))
    return newentries

"""
def getMachines():
    payload = {'portal_type': 'nva.chemiedp.maschine',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched MACHINE: "+i.get('title'))
    return newentries
    
"""

def getPowders():
    payload = {'portal_type': 'nva.chemiedp.druckbestaeubungspuder',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched POWDER: "+i.get('title'))
    return newentries

def getEtiketten():
    payload = {'portal_type': 'nva.chemiedp.reinigungsmitteletiketten',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        #import pdb; pdb.set_trace()
        print("Fetched DETERGENT_LABEL: "+i.get('title'))
    return newentries

def getManuell():
    payload = {'portal_type': 'nva.chemiedp.reinigungsmittelmanuell',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched DETERGENT_MANUAL: "+i.get('title'))
    return newentries

def getProduktdatenblatt():
    payload = {'portal_type': 'nva.chemiedp.produktdatenblatt',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched PRODUCT_DATASHEET: "+i.get('title'))
    return newentries

def getHeatset():
    payload = {'portal_type': 'nva.chemiedp.heatsetwaschmittel',
           'b_size': 500,
           'sort_on': 'sortable_title',
           'metadata_fields':'UID'}
    entries = getCatalogData(payload)
    newentries = list()
    for i in entries:
        data = getItemData(i)
        newentries.append(data)
        print("Fetched DETERGENT_HEATSET: "+i.get('title'))
    return newentries

if __name__ == "__main__":

    print("Starting data migration...")
    hostname = 'localhost'
    username = 'seppo'
    password = 'reldbpassword'
    database = 'gefahrstoffdb'

    erg = getHersteller()
    #erg2 = getMachines()
    erg3 = getPowders()
    erg4 = getEtiketten()
    erg5 = getManuell()
    erg6 = getProduktdatenblatt()
    erg7 = getHeatset()
    conn = psycopg2.connect(host = hostname, user=username, password=password, dbname=database)

    for i in erg:
        hersteller_title = i.get('title')
        hersteller_desc = i.get('description')
        hersteller_uid = i.get('UID')
        hersteller_homepage = i.get('homepage')
        cur = conn.cursor()
        #cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO manufacturer (title, description, webcode, homepage) VALUES (%s, %s, %s, %s);", (hersteller_title, hersteller_desc, hersteller_uid, hersteller_homepage))
        conn.commit()
        #print(hersteller_title)# correct
        cur.close()

    print('Successfully migrated MANUFACTURER')

    """
    for i in erg2:
        machine_title = i.get('title')
        machine_desc = i.get('description')
        machine_uid = i.get('UID')
        machine_link = i.get('@id')
        machine_manufacturer_name = i.get('hersteller')['title']
        #import pdb; pdb.set_trace()

        cur = conn.cursor()
        cur.execute("SELECT manufacturer_id FROM manufacturer WHERE title = '{0}';".format(machine_manufacturer_name))
        machine_manufacturer_id = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO printing_machine (title, description, webcode, image_url, manufacturer_id) VALUES (%s, %s, %s, NULL, %s);",
                    (machine_title, machine_desc, machine_uid, machine_manufacturer_id[0]))
        conn.commit()
        # print(machine_title)  # correct
        cur.close()

    print('Successfully migrated PRINTING_MACHINE')

    """

    for i in erg3:
        powder_title = i.get('title')
        powder_desc = i.get('description')
        powder_uid = i.get('UID')
        powder_link = i.get('@id')
        powder_product_class = i.get('produktklasse')
        powder_starting_material = i.get('ausgangsmaterial')
        powder_median_value = i.get('medianwert')
        powder_volume_share = i.get('volumenanteil')
        powder_checked_emissions = i.get('emissionsgeprueft')
        powder_date_checked = i.get('pruefdateum')
        powder_manufacturer_name = i.get('hersteller')['title']

        successfuluid = False
        while successfuluid == False:
            random_number = str(random.randint(100000, 999999))

            fullyear = datetime.datetime.now().year
            shortyear = str(fullyear)[2:]

            generated_uid = "PD" + shortyear + random_number

            cur = conn.cursor()
            cur.execute("SELECT spray_powder_id FROM spray_powder WHERE title = '{0}';".format(generated_uid))
            useduid = cur.fetchall()
            cur.close()

            if useduid == []:
                successfuluid = True

        cur = conn.cursor()
        cur.execute("SELECT manufacturer_id FROM manufacturer WHERE title = '{0}';".format(powder_manufacturer_name))
        powder_manufacturer_id = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        cur.execute("INSERT INTO spray_powder (title, description, webcode, manufacturer_id, image_url, product_class, starting_material, median_value, volume_share, checked_emissions, date_checked) VALUES (%s, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s);",
                    (powder_title, powder_desc, generated_uid, powder_manufacturer_id[0], powder_product_class, powder_starting_material, powder_median_value, powder_volume_share, powder_checked_emissions, powder_date_checked))
        conn.commit()
        cur.close()

    print('Successfully migrated SPRAY_POWDER')

    for i in erg4:
        etikett_title = i.get('title')
        etikett_desc = i.get('description')
        etikett_uid = i.get('UID')
        etikett_skin_category = i.get('hskategorie')
        etikett_checked_emissions = i.get('emissionsgeprueft')
        etikett_flashpoint = i.get('flammpunkt')
        etikett_values_range = i.get('wertebereich')
        etikett_classifications = i.get('einstufungen')
        etikett_usecases = i.get('verwendungszweck')
        etikett_manufacturer_name = i.get('hersteller')['title']

        cur = conn.cursor()
        cur.execute("SELECT manufacturer_id FROM manufacturer WHERE title = '{0}';".format(etikett_manufacturer_name))
        etikett_manufacturer_id = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO substance_mixture (title, description, webcode, branch, substance_type, image_url, skin_category, checked_emissions, flashpoint, values_range, usecases, manufacturer_id) VALUES (%s, %s, %s, 'branch', 'detergent_labels', NULL, %s, %s, %s, %s, %s, %s);",
                    (etikett_title, etikett_desc, etikett_uid, etikett_skin_category, etikett_checked_emissions, etikett_flashpoint, etikett_values_range, etikett_usecases, etikett_manufacturer_id[0]))
        conn.commit()
        #print(etikett_title)  # correct
        cur.close()

    print('Successfully migrated DETERGENT_LABELS')
        
    for i in erg5:
        manuell_title = i.get('title')
        manuell_desc = i.get('description')
        manuell_uid = i.get('UID')
        manuell_link = i.get('@id')
        manuell_skin_category = i.get('hskategorie')
        manuell_checked_emissions = i.get('emissionsgeprueft')
        manuell_flashpoint = i.get('flammpunkt')
        manuell_values_range = i.get('wertebereich')
        manuell_usecases = i.get('verwendungszweck')
        manuell_application_areas = i.get('anwendungsgebiete')
        manuell_manufacturer_name = i.get('hersteller')['title']

        cur = conn.cursor()
        cur.execute("SELECT manufacturer_id FROM manufacturer WHERE title = '{0}';".format(manuell_manufacturer_name))
        manuell_manufacturer_id = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute("INSERT INTO substance_mixture (title, description, webcode, branch, substance_type, image_url, skin_category, checked_emissions, flashpoint, values_range, usecases, application_areas, manufacturer_id) VALUES (%s, %s, %s, 'branch', 'detergent_manual', NULL, %s, %s, %s, %s, %s, %s, %s);",
                    (manuell_title, manuell_desc, manuell_uid, manuell_skin_category, manuell_checked_emissions, manuell_flashpoint, manuell_values_range, manuell_usecases, manuell_application_areas, manuell_manufacturer_id[0]))
        conn.commit()
        #print(manuell_title)  # correct
        cur.close()

    print('Successfully migrated DETERGENT_MANUAL')

    for i in erg6:
        datenblatt_title = i.get('title')
        datenblatt_desc = i.get('description')
        datenblatt_uid = i.get('UID')
        datenblatt_link = i.get('@id')
        datenblatt_skin_category = i.get('hskategorie')
        datenblatt_checked_emissions = i.get('emissionsgeprueft')
        datenblatt_product_category = i.get('produktkategorie')
        datenblatt_product_class = i.get('produktklasse')
        datenblatt_flashpoint = i.get('flammpunkt')
        datenblatt_values_range = i.get('wertebereich')
        datenblatt_material_compatibility = i.get('materialvertraeglichkeit')
        datenblatt_comments = i.get('bemerkungen')

        #import pdb; pdb.set_trace()
        cur = conn.cursor()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute(
            "INSERT INTO substance_mixture (title, description, webcode, branch, substance_type, image_url, skin_category, checked_emissions, flashpoint, values_range, comments) VALUES (%s, %s, %s, 'branch', 'product_datasheet', NULL, %s, %s, %s, %s, %s);",
            (datenblatt_title, datenblatt_desc, datenblatt_uid, datenblatt_skin_category, datenblatt_checked_emissions, datenblatt_flashpoint, datenblatt_values_range, str(datenblatt_comments)))
        conn.commit()
        #print(datenblatt_title)  # correct
        cur.close()

    print('Successfully migrated PRODUCT_DATASHEET')

    for i in erg7:
        heatset_title = i.get('title')
        heatset_desc = i.get('description')
        heatset_uid = i.get('UID')
        heatset_link = i.get('@id')
        heatset_ueg = i.get('ueg')
        heatset_response = i.get('response')
        heatset_skin_category = i.get('hskategorie')
        heatset_date_checked = i.get('pruefdateum')
        heatset_checked_emissions = i.get('emissionsgeprueft')

        cur = conn.cursor()
        #import pdb; pdb.set_trace()
        # cur.execute("INSERT INTO manufacturer (title, description, webcode) VALUES (%s, %s, %s)") % (hersteller_title, hersteller_desc, hersteller_uid)
        cur.execute(
            "INSERT INTO substance_mixture (title, description, webcode, branch, substance_type, image_url, ueg, response, skin_category, date_checked, checked_emissions) VALUES (%s, %s, %s, 'branch', 'detergent_heatset', NULL, %s, %s, %s, %s, %s);",
            (heatset_title, heatset_desc, heatset_uid, heatset_ueg, heatset_response, heatset_skin_category, heatset_date_checked, heatset_checked_emissions))
        conn.commit()
        #print(heatset_title)  # correct
        cur.close()

    print('Successfully migrated DETERGENT_HEATSET')
    print('CHEERS! DATA MIGRATION SUCCESSFULLY COMPLETED :)')

    #    insert = "INSERT INTO manufacturer(title, description) (%s, %s)" % (hersteller_title, hersteller_desc)
    #    cur.execute(insert)
    #    cur.fetchall()
    conn.close()
