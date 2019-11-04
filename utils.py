class bcolors:
	HEADER = '\033[95m'		# purple
	OKBLUE = '\033[94m'		# blue
	OKGREEN = '\033[92m'	# green
	WARNING = '\033[93m' 	# yellow
	FAIL = '\033[91m'		# red
	ENDC = '\033[0m'		# end char
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class g:
	# keep those IDS as is, I use this implicitly in id detection & behavior
	FARMER= 0
	LEEK_1= 1
	LEEK_2= 2
	LEEK_3= 3
	LEEK_4= 4
	DELAY = 2 # seconds between each check when waiting for fight result
	WINNERSWITCH = {
		0: bcolors.WARNING+"DRAW"+bcolors.ENDC,
		1: bcolors.OKGREEN+"WIN "+bcolors.ENDC,
		2: bcolors.FAIL+"LOSE"+bcolors.ENDC,
	}

class behavior:
	BALANCED = 'BALANCED' # split fights in 5 for each leeks + farmer
	EQUALIZE = 'EQUALIZE' # regroup levels then focus on farmer
	FARMING  = 'FARMING'  # focus on farmer
	TODOLIST = 'TODOLIST' # do the todolist (ignore limit)
	NONE = 'NONE'

class shutdown:
	OFF= 0
	ASK= 1
	ON = 2

class goal:
	NONE = 'NONE'
	FOCUS_LIFE = 'life'
	FOCUS_STRENGTH = 'strength'
	FOCUS_WISDOM = 'wisdom'
	FOCUS_AGILITY = 'agility'
	FOCUS_RESISTANCE = 'resistance'
	FOCUS_FREQUENCY = 'frequency'
	FOCUS_SCIENCE = 'science'
	FOCUS_MAGIC = 'magic'
	FOCUS_TP = 'tp'
	FOCUS_MP = 'mp'
	ADVANCED = { # todo
		'STR': [
			{"life":0,"strength":0,"wisdom":0,"agility":0,"resistance":0,"frequency":0,"science":0,"magic":0,"tp":10,"mp":3},
		]
	}
