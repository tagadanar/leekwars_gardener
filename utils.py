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
	LW_ROOT_DIR= 0 # reminder: id 0 is the root dir for leekwars
	DOWNLOAD= "download"
	UPLOAD  = "upload"

class behavior:
	BALANCED = 'BALANCED' # split fights between each leeks + farmer
	EQUALIZE = 'EQUALIZE' # regroup levels then focus on farmer
	FARMING  = 'FARMING'  # focus on farmer
	TODOLIST = 'TODOLIST' # do the todolist (ignore limit)
	SOLO_BALANCED = 'SOLO_BALANCED' # split fights between each leeks
	SOLO_1 = 'SOLO_1' # only solo with first leek
	SOLO_2 = 'SOLO_2' # only solo with second leek
	SOLO_3 = 'SOLO_3' # only solo with third leek
	SOLO_4 = 'SOLO_4' # only solo with fourth leek
	NONE = 'NONE' # do nothing, only refresh connection and display account status

class state:
	OFF= 0
	ASK= 1
	ON = 2

class strategy:
	RANDOM = 'random'
	BEST = 'best'
	WORST = 'worst'

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
