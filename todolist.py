import math
import json
from utils import g, behavior, goal

class Todolist:
	def __init__(self, account, api):
		self.behavior = account.get('behavior')
		self.todolist = account.get('todolist')
		self.goals = account.get('goals')
		self.limit = account.get('limit')
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
				yield g._LEEK_1_
				nb -= 1
		else:
			while nb > 0:
				for x in range(self.size):
					yield x
					nb -= 1

	def equalizeGenerator(self):
		nb = max(self.fights - self.limit, 0)
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
				yield g._FARMER_
				nb -= 1
			else:
				# not same lvl, focus on lower
				index = g._LEEK_1_
				lowestIndex = g._FARMER_
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
			yield g._FARMER_
			nb -= 1 

	
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
							missing_life = 2002 - added_life
							if missing_life < lCapital*3:
								final = lCapital*3
							else:
								before_threshold_capital = missing_life/3
								final = missing_life + (lCapital - before_threshold_capital)*2
						elif added_life < 1000:
							missing_life = 1000 - added_life
							if missing_life < lCapital*4:
								final = lCapital*4
							else:
								# note to self : if I'm in a case where I can add over 2k pv this will bug
								before_threshold_capital = missing_life/4
								final = missing_life + (lCapital - before_threshold_capital)*3
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
