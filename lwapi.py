import requests
import json
import random
import time
import sys

from utils import bcolors, g, strategy

#################################################################
# leekwars API
#################################################################
class lwapi:
	def __init__(self, account):
		self.login = account.get('login')
		self.password = account.get('password')
		self.strategy = account.get('strategy', None)
		self.version = account.get('synchronize', None)
		if self.version != None:
			self.version = self.version.get('version', '1.1')
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

	# launch a solo fight against an adv, return fight_id
	def solo_fight(self, leekid):
		# pick a rand adv from sologarden
		r = self.s.get("%s/garden/get-leek-opponents/%s"%(self.rooturl,leekid), headers=self.headers, data={'leek_id':leekid})
		garden = r.json()['opponents']
		if len(garden) < 1:
			print("%sNo one in the garden%s when trying to do a solo fight with %s%s%s"%(bcolors.FAIL,bcolors.ENDC,bcolors.OKBLUE,self.farmer['leeks'][leek_id]['name'],bcolors.ENDC))
			sys.stdout.flush()
			return None
		e = self.get_opponent(garden)
		eid = e['id']
		# launch the fight
		r = self.s.post("%s/garden/start-solo-fight/%s/%s"%(self.rooturl,leekid,eid), headers=self.headers, data={'leek_id':leekid, 'target_id':eid})
		fight_id = r.json()['fight']
		return fight_id
		
	# launch a farmer fight against an adv, return fight_id
	def farmer_fight(self):
		# pick a rand adv from farmergarden
		r = self.s.get("%s/garden/get-farmer-opponents"%self.rooturl, headers=self.headers)
		garden = r.json()['opponents']
		if len(garden) < 1:
			print("%sNo one in the garden%s when trying to do a farmer fight with %s%s%s"%(bcolors.FAIL,bcolors.ENDC,bcolors.OKBLUE,self.farmer["name"],bcolors.ENDC))
			sys.stdout.flush()
			return None
		e = self.get_opponent(garden)
		eid = e['id']
		# launch the fight
		r = self.s.post("%s/garden/start-farmer-fight/%s"%(self.rooturl,eid), headers=self.headers, data={'target_id':eid})
		fight_id = r.json()['fight']
		return fight_id

	# launch a team fight against an adv, return fight_id
	def team_fight(self, team_id):
		# pick a rand adv from farmergarden
		r = self.s.get("%s/garden/get-composition-opponents/%s"%(self.rooturl,team_id), headers=self.headers, data={'composition':team_id})
		garden = r.json()['opponents']
		e = self.get_opponent(garden)
		eid = e['id']
		# launch the fight
		r = self.s.post("%s/garden/start-team-fight/%s"%(self.rooturl,eid), headers=self.headers, data={'composition_id':team_id,'target_id':eid})
		fight_id = r.json()['fight']
		return fight_id

	# pick an adv in the garden
	def get_opponent(self, garden):
		enemy = None
		if self.strategy == None or self.strategy == strategy.RANDOM:
			enemy = random.choice(garden)
		elif self.strategy == strategy.WORST:
			for e in garden:
				if enemy == None or e['talent']<enemy['talent']:
					enemy = e
		elif self.strategy == strategy.BEST:
			for e in garden:
				if enemy == None or e['talent']>enemy['talent']:
					enemy = e
		return enemy

	# wait for fight result then print it
	def wait_fight_result(self, fight_id, fight_type):
		firstwait = True
		while True:
			r = self.s.get("%s/fight/get/%s"%(self.rooturl,fight_id), headers=self.headers, data={'fight_id':fight_id})
			result = r.json()
			winner = result['winner']
			if winner==-1: # Fight isn't resolved yet
				if firstwait:
					if fight_type == g.FIGHT_TYPE_FARMER:
						sys.stdout.write("%s vs %s."%(result['team1_name'], result['team2_name']))
					elif fight_type == g.FIGHT_TYPE_SOLO:
						sys.stdout.write("%s -lvl%s (%s) vs %s (%s)."%(result['leeks1'][0]['name'], result['leeks1'][0]['level'], result['leeks1'][0]['talent'], result['leeks2'][0]['name'], result['leeks2'][0]['talent']))
					elif fight_type == g.FIGHT_TYPE_TEAM:
						sys.stdout.write("%s vs %s."%(result['team1_name'], result['team2_name']))
					else:
						print("\r%sunknown fight_type:%s %s%s%s"%(bcolors.FAIL,bcolors.ENDC,bcolors.HEADER,fight_type,bcolors.ENDC))
					firstwait = False
				else:
					sys.stdout.write('.')
				sys.stdout.flush()
				time.sleep(g.DELAY)
				continue
			elif winner>=0:
				win = g.WINNERSWITCH.get(winner, 'WTF?')
				if fight_type == g.FIGHT_TYPE_FARMER:
					myTalent = result['report']['farmer1']['talent'] + result['report']['farmer1']['talent_gain']
					enTalent = result['report']['farmer2']['talent'] + result['report']['farmer2']['talent_gain']
					print("\r%s %s (%s) vs %s (%s)"%(win, result['report']['farmer1']['name'], myTalent, result['report']['farmer2']['name'], enTalent))
				elif fight_type == g.FIGHT_TYPE_SOLO:
					print("\r%s %s -lvl%s (%s) vs %s (%s)"%(win, result['leeks1'][0]['name'], result['leeks1'][0]['level'], result['leeks1'][0]['talent'], result['leeks2'][0]['name'], result['leeks2'][0]['talent']))
				elif fight_type == g.FIGHT_TYPE_TEAM:
					myTalent = result['report']['team1']['talent'] + result['report']['team1']['talent_gain']
					enTalent = result['report']['team2']['talent'] + result['report']['team2']['talent_gain']
					print("\r%s %s (%s) vs %s (%s)"%(win, result['report']['team1']['name'], myTalent, result['report']['team2']['name'], enTalent))
				else:
					print("\r%sunknown fight_type:%s %s%s%s"%(bcolors.FAIL,bcolors.ENDC,bcolors.HEADER,fight_type,bcolors.ENDC))
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
		sys.stdout.flush()
		return leeks_to_ID

	def refresh_account_state(self):
		r = self.s.post("%s/farmer/login-token/"%self.rooturl, data={'login':self.login,'password':self.password})
		self.farmer = r.json()['farmer']

	def spend_capital(self, leek_id, stats):
		r = self.s.post("%s/leek/spend-capital"%self.rooturl, data={'leek':leek_id,'characteristics':stats})
		if r:
			print("%s%s%s spent %s"%(bcolors.OKBLUE,self.farmer['leeks'][leek_id]['name'],bcolors.ENDC,stats))
		else:
			print("%s%s%s when trying to spend %s on %s%s%s"%(bcolors.FAIL,r.json(),bcolors.ENDC,stats,bcolors.OKBLUE,self.farmer['leeks'][leek_id]['name'],bcolors.ENDC))

	def buy_fights(self):
		r = self.s.post("%s/market/buy-habs"%self.rooturl, data={'item_id':'100-fights'})
		if r:
			self.refresh_account_state()
			print("%sbuying 100 fights%s: %s"%(bcolors.OKBLUE,bcolors.ENDC,r.text))
		else:
			print("%s%s%s when trying to buy %s100 fights%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.OKBLUE,bcolors.ENDC))


	def get_leek(self, leek_id):
		r = self.s.get("%s/leek/get/%s"%(self.rooturl,leek_id), data={'leek':leek_id})
		return r.json()

	def get_team_composition(self):
		r = self.s.get("%s/garden/get"%self.rooturl)
		if r:
			return r.json()['garden']['my_compositions']
		else:
			print("%s%s%s when trying to get team composition on %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.OKBLUE,self.farmer["name"],bcolors.ENDC))
			return []

	def register_tournament(self, leek_id):
		if leek_id == None:
			print("%sleek_id_none%s when trying to register tournament"%(bcolors.FAIL,bcolors.ENDC))
		elif leek_id == g.FARMER:
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

	def get_ais(self):
		r = self.s.get("%s/ai/get-farmer-ais"%self.rooturl)
		#print(r.json())
		return r.json()

	def get_ai(self, ai_id):
		r = self.s.get("%s/ai/get/%s"%(self.rooturl,ai_id), data={'ai_id':ai_id})
		return r.json()['ai']['code']

	def create_ai(self, file_path, file_name, dir_id,  lw_item):
		if lw_item == None:
			#reminder false is for v1, should be a param of every account when v2 is out !
			r = self.s.post("%s/ai/new/%s/%s"%(self.rooturl,dir_id,'false'), data={'folder_id':dir_id, 'version':self.version})
			if r:
				lw_id = r.json()['ai']['id']
				r = self.s.post("%s/ai/rename/%s/%s"%(self.rooturl,lw_id,file_name), data={'ai_id':lw_id, 'new_name':file_name})
			if r:
				print("%screated%s file %s%s%s"%(bcolors.OKBLUE,bcolors.ENDC,bcolors.HEADER,file_name,bcolors.ENDC))
			else:
				print("%s%s%s when trying to create file %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.HEADER,file_name,bcolors.ENDC))
		else:
			lw_id = lw_item['id']
		with open(file_path, 'r') as reader:
			code = reader.read()
			r = self.s.post("%s/ai/save"%self.rooturl, data={'ai_id':lw_id,'code':code})
			if r:
				print("%supdated%s file %s%s%s"%(bcolors.OKBLUE,bcolors.ENDC,bcolors.HEADER,file_name,bcolors.ENDC))
			else:
				print("%s%s%s when trying to update file %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.HEADER,file_name,bcolors.ENDC))
			sys.stdout.flush()

	def create_dir(self, dir_path, dir_name, dir_id,  lw_item):
		if lw_item == None:
			r = self.s.post("%s/ai-folder/new/%s"%(self.rooturl,dir_id), data={'folder_id':dir_id})
			if r:
				lw_id = r.json()['id']
				r = self.s.post("%s/ai-folder/rename/%s/%s"%(self.rooturl,lw_id,dir_name), data={'folder_id':lw_id, 'new_name':dir_name})
			if r:
				print("%screated%s directory %s%s%s"%(bcolors.OKBLUE,bcolors.ENDC,bcolors.HEADER,dir_name,bcolors.ENDC))
			else:
				print("%s%s%s when trying to create directory %s%s%s"%(bcolors.FAIL,r.json()['error'],bcolors.ENDC,bcolors.HEADER,dir_name,bcolors.ENDC))
			sys.stdout.flush()
		else:
			lw_id = lw_item['id']
		return lw_id
