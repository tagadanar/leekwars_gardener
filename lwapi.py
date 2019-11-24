import requests
import json
import random
import time
import sys

from utils import bcolors, g

#################################################################
# leekwars API
#################################################################
class lwapi:
        def __init__(self, login, password):
                self.login = login
                self.password = password
                self.s = requests.session()
                self.rooturl = "https://leekwars.com/api"

        # connecting to leekwars
        def connect(self):
                r = self.s.post("%s/farmer/login-token/"%self.rooturl, data={'login':self.login,'password':self.password})
                self.headers = {'Authorization': 'Bearer %s'%r.json()['token']}
                self.farmer = r.json()['farmer']
                self.farmer_id = self.farmer['id']
                # this get refresh connected status on account (for NONE behavior)
                self.s.get("%s/garden/get-farmer-opponents"%self.rooturl, headers=self.headers)
                return self.farmer

        # launch a solo fight against random adv, return fight_id
        def solo_fight(self, leekid):
                # pick a rand adv from sologarden
                r = self.s.get("%s/garden/get-leek-opponents/%s"%(self.rooturl,leekid), headers=self.headers, data={'leek_id':leekid})
                garden = r.json()['opponents']
                e = random.choice(garden)
                eid = e['id'] # launch the fight r = self.s.post("%s/garden/start-solo-fight/%s/%s"%(self.rooturl,leekid,eid), headers=self.headers, data={'leek_id':leekid, 'target_id':eid})
                fight_id = r.json()['fight']
                return fight_id

        # launch a farmer fight against random adv, return fight_id
        def farmer_fight(self):
                # pick a rand adv from farmergarden
                r = self.s.get("%s/garden/get-farmer-opponents"%self.rooturl, headers=self.headers)
                garden = r.json()['opponents']
                e = random.choice(garden)
                eid = e['id']
                # launch the fight
                r = self.s.post("%s/garden/start-farmer-fight/%s"%(self.rooturl,eid), headers=self.headers, data={'target_id':eid})
                fight_id = r.json()['fight']
                return fight_id

        def compo_fight(self, compo_id):
                # pick a rand adv from farmergarden
                r = self.s.get("%s/garden/get-composition-opponents/%s"%(self.rooturl,compo_id),data={'composition':compo_id}, headers=self.headers)
                garden = r.json()['opponents']
                e = random.choice(garden)
                eid = e['id']
                # launch the fight
                r = self.s.post("%s/garden/start-team-fight/%s"%(self.rooturl,eid), headers=self.headers, data={'composition_id':compo_id,'target_id':eid})
                breakpoint()
                fight_id = r.json()['fight']
                return fight_id


        # wait for fight result then print it
        def wait_fight_result(self, fight_id, kind):
                firstwait = True
                while True:
                        r = self.s.get("%s/fight/get/%s"%(self.rooturl,fight_id), headers=self.headers, data={'fight_id':fight_id})
                        result = r.json()['fight']
                        winner = result['winner']
                        if winner==-1: # Fight isn't resolved yet
                                if firstwait:
                                        sys.stdout.write('waiting.')
                                        firstwait = False
                                else:
                                        sys.stdout.write('.')
                                sys.stdout.flush()
                                time.sleep(g.DELAY)
                                continue
                        elif winner>=0:
                                win = g.WINNERSWITCH.get(winner, 'WTF?')
                                if kind == 1:
                                        myTalent = result['report']['farmer1']['talent'] + result['report']['farmer1']['talent_gain']
                                        enTalent = result['report']['farmer2']['talent'] + result['report']['farmer2']['talent_gain']
                                        print("\r%s %s (%s) vs %s (%s)"%(win, result['report']['farmer1']['name'], myTalent, result['report']['farmer2']['name'], enTalent))
                                elif kind == 0:
                                        print("\r%s %s -lvl%s (%s) vs %s (%s)"%(win, result['leeks1'][0]['name'], result['leeks1'][0]['level'], result['leeks1'][0]['talent'], result['leeks2'][0]['name'], result['leeks2'][0]['talent']))
                                elif kind == 2:#compo fights
                                         print("\r%s %s -lvl%s (%s) vs %s (%s)"%(win, result['team1'][0]['name'], result['team1'][0]['level'], result['team1'][0]['talent'], result['team2'][0]['name'], result['team2'][0]['talent']))
                                        
                                sys.stdout.flush()
                                self.refresh_account_state()
                                return

        # print a resume of the account state & return leeks number to ID association
        def display_status(self):
                # handling farmer infos
                fName = self.farmer['login']
                fTalent = self.farmer['talent']
                fLevel = self.farmer['total_level']
                fHabs = self.farmer['habs']
                nbFights = self.farmer['fights']
                isOutOfGarden = self.farmer['in_garden'] != 1
                
                print("%sCurrent: %s%s%s - lvl%s | talent: %s | habs: %s | fights left: %s%s"%(bcolors.BOLD, bcolors.HEADER, fName, bcolors.ENDC, fLevel, fTalent, fHabs, nbFights, bcolors.ENDC))
                if isOutOfGarden:
                        print("%s/!\\%s farmer not in garden ! %s/!\\%s"%(bcolors.FAIL, bcolors.WARNING, bcolors.FAIL, bcolors.ENDC))
                        
                leeks_to_ID = {}
                index = g.LEEK_1
                for leekid, leekinfo in self.farmer['leeks'].items():
                        # saving leek realID
                        leeks_to_ID[index] = leekid
                        index += 1
                        
                        # display welcome info
                        lName = leekinfo['name']
                        lLevel = leekinfo['level']
                        lTalent = leekinfo['talent']
                        lCapital = leekinfo['capital']
                        warn = ""
                        if lCapital > 0:
                                warn = "%s/!\\%s %s capital points unused %s/!\\%s"%(bcolors.FAIL, bcolors.WARNING, lCapital, bcolors.FAIL, bcolors.ENDC)
                        print("%s - lvl%s | talent: %s %s"%(lName, lLevel, lTalent, warn))
                self.leeks_to_ID = leeks_to_ID
                   
                return leeks_to_ID

        def get_compos_fights(self):
                garden = self.get_garden();
                compositions = garden['garden']['my_compositions']
                for compo in compositions:
                        for fight in range(0,compo['fights']):     
                                yield compo['id'] 

        def refresh_account_state(self):
                r = self.s.post("%s/farmer/login-token/"%self.rooturl, data={'login':self.login,'password':self.password})
                self.farmer = r.json()['farmer']

        def spend_capital(self, leek_id, stats):
                r = self.s.post("%s/leek/spend-capital"%self.rooturl, data={'leek':leek_id,'characteristics':stats})
                if r:
                        print("%s%s%s spent %s"%(bcolors.OKBLUE,self.farmer['leeks'][leek_id]['name'],bcolors.ENDC,stats))
                else:
                        print("%s%s%s when trying to spend %s on %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,stats,bcolors.OKBLUE,self.farmer['leeks'][leek_id]['name'],bcolors.ENDC))

        def get_leek(self, leek_id):
                r = self.s.get("%s/leek/get/%s"%(self.rooturl,leek_id), data={'leek':leek_id})
                return r.json()

        def register_tournament(self, leek_id):
                if leek_id == g.FARMER:
                        r = self.s.post("%s/farmer/register-tournament"%self.rooturl)
                        if r:
                                print("%s%s%s registered to tournament"%(bcolors.OKBLUE,self.farmer["name"],bcolors.ENDC))
                        else:
                                print("%s%s%s when trying to register tournament on %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.OKBLUE,self.farmer["name"],bcolors.ENDC))
                else:
                        r = self.s.post("%s/leek/register-tournament"%self.rooturl, data={'leek_id':leek_id})
                        if r:
                                print("%s%s%s registered to tournament"%(bcolors.OKBLUE,self.farmer['leeks'][leek_id]["name"],bcolors.ENDC))
                        else:
                                print("%s%s%s when trying to register tournament on %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.OKBLUE,self.farmer['leeks'][leek_id]["name"],bcolors.ENDC))
                        
        def makeRequest(self, url, args):
                r = self.s.post("%s/%s"%(self.rooturl,url), data=args)
                return r
        def get_garden(self):
                r = self.makeRequest('garden/get', {});
                return r.json()
        def create_folder(self,folderName):
                r = self.makeRequest('ai/get-farmer-ais', {})
                for folder in r.json()['folders']:
                        if folder['name']==folderName:
                                return folder['id']
                r = self.s.post("%s/ai-folder/new"%self.rooturl, data={'folder_id':0})
                fid = r.json()['id'];
                r = self.s.post("%s/ai-folder/rename"%self.rooturl, data={'folder_id':fid, 'new_name':folderName})
                return fid
        def create_ai(self, folderid, name):
                r = self.makeRequest('ai/get-farmer-ais', {})
                for ai in r.json()['ais']:
                        if ai['name']==name:
                                return ai['id']
                r = self.s.post("%s/ai/new"%self.rooturl, data={'folder_id':folderid, 'v2':0})
                fid = r.json()['id'];
                r = self.s.post("%s/ai/rename"%self.rooturl, data={'ai_id':fid, 'new_name':name})
                return r
        def saveai(self, ai, code):
                r = self.makeRequest('ai/save', {'ai_id':ai,'code':code})
                return r
        def getai(self, ai):
                r = self.makeRequest('ai/get', {'ai_id':ai})
                return r
        def listais(self, folderid):
                r = self.makeRequest('ai/get-farmer-ais', {})
                ailist = []
                for ai in r.json()['ais']:
                        if ai['folder']==folderid:
                                ailist.append(ai)
                return ailist
