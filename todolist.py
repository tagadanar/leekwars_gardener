import math
import json
import os
from utils import g, bcolors, behavior, goal

class Todolist:
	def __init__(self, account, api):
		self.behavior = account.get('behavior')
		self.todolist = account.get('todolist')
		self.goals = account.get('goals')
		self.tournaments = account.get('tournaments')
		self.limit = account.get('limit')
		self.team_limit = account.get('team_limit')
		self.synchronize = account.get('synchronize')
		self.api = api
		self.fights = api.farmer['fights']
		self.size = len(api.farmer['leeks'])
		if self.size != 1: # can do farmer fights
			self.size += 1

	def getGenerator(self):
		if self.behavior == behavior.NONE:
			return []
		elif self.behavior == behavior.TODOLIST:
			return self.todolistGenerator()
		elif self.behavior == behavior.BALANCED:
			return self.balancedGenerator()
		elif self.behavior == behavior.EQUALIZE:
			return self.equalizeGenerator()
		elif self.behavior == behavior.FARMING:
			return self.farmingGenerator()
		elif self.behavior == behavior.SOLO_BALANCED:
			return self.solobalancedGenerator()
		elif self.behavior.startswith('SOLO_'):
			return self.soloGenerator(int(self.behavior[5]))
		else:
			print("%s/!\\ UNKNOWN BEHAVIOR /!\\%s"%(bcolors.FAIL, bcolors.ENDC))
			return []

	def todolistGenerator(self):
		for leekid, nb_fight in self.todolist.items():
			while nb_fight > 0:
				yield leekid
				nb_fight -= 1

	def balancedGenerator(self):
		nb = max(self.fights - self.limit, 0)
		if self.size == 1:
			while nb > 0:
				yield g.LEEK_1
				nb -= 1
		else:
			while nb > 0:
				for x in range(self.size):
					yield x
					nb -= 1

	def solobalancedGenerator(self):
		nb = max(self.fights - self.limit, 0)
		if self.size == 1:
			while nb > 0:
				yield g.LEEK_1
				nb -= 1
		else:
			while nb > 0:
				for x in range(1, self.size):
					yield x
					nb -= 1

	def soloGenerator(self, leek):
		nb = max(self.fights - self.limit, 0)
		while nb > 0:
			yield leek
			nb -= 1

	def equalizeGenerator(self):
		nb = max(self.fights - self.limit, 0)
		if self.size == 1:
			while nb > 0:
				yield g.LEEK_1
				nb -= 1
		else:
			while nb > 0:
				# check same level
				is_same_level = True
				baselvl = -1
				for leekid, leekinfo in self.api.farmer['leeks'].items():
					if baselvl == -1:
						baselvl = leekinfo['level']
					if baselvl != leekinfo['level']:
						is_same_level = False
						break
				if is_same_level:
					yield g.FARMER
					nb -= 1
				else:
					# not same lvl, focus on lower
					index = g.LEEK_1
					lowestIndex = g.FARMER
					lowestLevel = 302
					for leekid, leekinfo in self.api.farmer['leeks'].items():
						lLevel = leekinfo['level']
						if lowestLevel > lLevel:
							lowestIndex = index
							lowestLevel = lLevel
						index += 1
					yield lowestIndex
					nb -= 1

	def farmingGenerator(self):
		nb = max(self.fights - self.limit, 0)
		while nb > 0:
			yield g.FARMER
			nb -= 1 

	def getTeamGenerator(self):
		for compo in self.api.get_team_composition():
			max_fight = compo['fights'] - self.team_limit
			for fight in range(0, max_fight):
				yield compo['id']

	def registerTournaments(self):
		for leek in self.tournaments:
			if leek == g.FARMER:
				self.api.register_tournament(leek)
			else:
				self.api.register_tournament(self.api.leeks_to_ID.get(leek, None))
	
	def trySpendCapital(self):
		indexleek = 0
		for leekid, leekinfo in self.api.farmer['leeks'].items():
			indexleek += 1
			lCapital = leekinfo['capital']
			if lCapital > 0:
				lgoal = self.goals[indexleek]
				if lgoal == goal.NONE:
					return
				else:
					leek = self.api.get_leek(leekid)
					stats = {}
					if lgoal == goal.FOCUS_LIFE:
						base_life = 100 + ((leek['level']-1) * 3)
						added_life = leek['life']-base_life
						if added_life >= 2000:
							final = lCapital*2
						elif added_life >= 1000:
							# bugged if I overcap to 2k+ feeling lazy... TODO fixme
							final = lCapital*3
						elif added_life < 1000:
							# bugged if I overcap to 1k+ feeling lazy... TODO fixme
							final = lCapital*4
						stats[lgoal] = final

					elif lgoal == goal.FOCUS_STRENGTH or \
						 lgoal == goal.FOCUS_WISDOM or \
						 lgoal == goal.FOCUS_AGILITY or \
						 lgoal == goal.FOCUS_RESISTANCE or \
						 lgoal == goal.FOCUS_SCIENCE or \
						 lgoal == goal.FOCUS_MAGIC:
						currentValue = leek[lgoal]
						if currentValue >= 600:
							final = math.floor(lCapital/3)
						elif currentValue >= 400:
							# bugged if I overcap to 600+ feeling lazy... TODO fixme
							final = math.floor(lCapital/2)
						elif currentValue >= 200:
							# bugged if I overcap to 400+
							final = lCapital
						else:
							# bugged if I overcap to 200+
							final = lCapital*2
						stats[lgoal] = final

					elif lgoal == goal.FOCUS_FREQUENCY:
						# you weirdo !
						stats[lgoal] = lCapital
						
					elif lgoal == FOCUS_TP or \
 						lgoal == FOCUS_MP:
						# lazy me doing stoopid shit, TODO fixme
						stats[lgoal] = 1
					if final > 0:
						stats = json.dumps(stats)
						self.api.spend_capital(leekid, stats)

	def trySynchronize(self):
		transfer = self.synchronize['transfer']
		directory = self.synchronize['directory']
		if transfer == g.DOWNLOAD:
			if not os.path.isdir(directory):
				os.mkdir(directory)
				print("%smkdir%s %s"%(bcolors.OKBLUE, bcolors.ENDC, directory))
			ais = self.api.get_ais()
			self.recursiv_create(ais['ais'], ais['folders'], g.LW_ROOT_DIR, directory)
		elif transfer == g.UPLOAD:
			ignored = self.synchronize['ignore']
			ais = self.api.get_ais()
			self.recursiv_read(ais, g.LW_ROOT_DIR, directory, ignored)
		else:
			print("%sunknown transfer direction:%s %s"%(bcolors.FAIL, bcolors.ENDC, transfer))

	def recursiv_read(self, ais, dir_id, directory, ignored):
		ldir = [x for x in os.listdir(directory) if x not in ignored]
		for name in ldir:
			file_path = os.path.join(directory,name)
			if os.path.isfile(file_path):
				lw_item = next((ai for ai in ais['ais'] if ai['name'] == name), None)
				self.api.create_ai(file_path, name, dir_id, lw_item)
		for name in ldir:
			dir_path = os.path.join(directory,name)
			if os.path.isdir(dir_path):
				lw_item = next((fd for fd in ais['folders'] if fd['name'] == name), None)
				folder_id = self.api.create_dir(dir_path, name, dir_id, lw_item)
				self.recursiv_read(ais, folder_id, dir_path, ignored)

	def recursiv_create(self, ais, folders, parent_id, root_id):
		for ai in ais:
			if ai['folder'] == parent_id:
				code = self.api.get_ai(ai['id'])
				file_path = os.path.join(root_id,ai['name'])
				with open(file_path, 'w') as writer: 
					writer.write(code.encode('utf-8'))
					print("%swriting%s %s"%(bcolors.OKBLUE, bcolors.ENDC, file_path))
		for d in folders:
			if d['folder'] == parent_id:
				dir_name = os.path.join(root_id,d['name'])
				if not os.path.isdir(dir_name):
					os.mkdir(dir_name)
					print("%smkdir%s %s"%(bcolors.OKBLUE, bcolors.ENDC, dir_name))
				self.recursiv_create(ais, folders, d['id'], dir_name)

