import os, uuid
from pymongo import MongoClient
from datetime import datetime, timedelta
#from ig_utils import download_profile
import pandas as pd



mongodb = MongoClient('mongodb://localhost:27017')
db = mongodb['website_bs']
db_accounts = db.accounts
db_devices = db.devices

def register_acc(user):
    try:
        res = [x for x in db_accounts.find({"user":user['email']})]
        return False
    except:
        print('USER')
        print(user)
        user['password'] = str(uuid.uuid4())
        user['ref'] = 'nope'

        db_accounts.insert_one({'password': user['password'],
                                'register_time': datetime.now(),
                                'plan': 'normal',
                                'email': user['email'],
                                'user_name': user['name'],
                                'referrer': user['ref']})
        print('Succesfully register new user > {}'.format(user['email']))
        return True
        #res = [x for x in db_accounts.find({"email": user['email']})]
        #return False

def get_devices(user):
    res = [x for x in db_devices.find({'email':user['email']})]
    if len(res) == 0:
        return False
    else:
        return res
def add_device(user):
    db_devices.insert_one({'phone_id':user['uid'],
                           'email':user['email'],
                           'registered_device_time':datetime.now(),
                           'actions_done':0})
    print('Succesfully added new instance > {}'.format(user['email']))
def check_device_user():

    ''
#add_device({'email':'polarcoding',
#            'uid':'randomvaina.'})
#print(get_devices({'email':'polarcoding'}))

'''
print(register_acc({'user':'polarcoding',
              'password':'Hhi237375.',
              'email':'polarsourccode.contact@gmail.com',
              'ref':False,
              'name':'Moises Samuel'}))
'''