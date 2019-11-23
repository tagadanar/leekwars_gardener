#!/usr/bin/env python3
from settings import Accounts
from todolist import Todolist
from utils import bcolors, g, behavior, shutdown
from lwapi import lwapi
import os
import sys, argparse

#################################################################
# Main program
#################################################################

# main loop

parser = argparse.ArgumentParser(description='sync remote directories with local ones in folder ias')
parser.add_argument('--sync','-s',  metavar='FOLDERS',help='sync folders (you can give multiple folders with -s folder1,folder2,....')
parser.add_argument('--get', '-g', metavar='FOLDERS',help='retrieve remote folders from leekwars.com (you can give multiple arguments with -g folder1,folder2,...')
args = parser.parse_args()

if args.get:
    print('getting folders', args.get);
    dirs = args.get.split(',')
    getsync = 1
elif args.sync:
    print('syncing folder', args.sync);
    dirs = args.sync.split(',')
    getsync = 0
else :
    print('wrong arguments !')
    sys.exit(2)
for account in Accounts.list:
    login = account.get('login')
    password = account.get('password')

    api = lwapi(login, password)
    # connecting to leekwars
    farmer = api.connect()
    os.chdir("ais");
    if getsync:
        print('directories',dirs,'are going to be retrieved')
    else :
        print('directories',dirs,'are going to be synced')
    validation = input('are you sure ?(Y/n)')
    if validation!="Y" :
        break;
    if getsync:
        for directory in dirs:
            if not os.path.isdir(directory):
                os.mkdir(directory)
            fid = api.create_folder(directory);
            print('id of foler',directory, ':',fid)
            ais = api.listais(fid)
            for ai in ais:
                name = ai['name']
                print('Retrieving ai',name)
                content = api.getai(ai['id'])
                code = content.json()['ai']['code']
                aifile = open(directory+"/"+name+".js",'w');
                aifile.write(code)
    else:
        for directory in dirs:
            fid = api.create_folder(directory);
            print('id of foler',directory, ':',fid)
            ais = os.listdir(directory)
            for ai in ais:
                name = ai.split('.')[0];
                aifile = open(directory+"/"+ai,"r")
                code = aifile.read()
                aiid = api.create_ai(fid,name)
                print('Writing to ',aiid,name)
                r = api.saveai(aiid, code).json()
                print(r)
