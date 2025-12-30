import os
from dotenv import load_dotenv
from utils import g, behavior, state, goal, strategy

load_dotenv()

#################################################################
# Declaring accounts
#################################################################
class Accounts:
	fight = state.OFF
	shutdown = state.OFF
	synchronize = state.OFF
	speedrun = state.OFF
	list= [
		{
			'login': os.getenv('LEEKWARS_LOGIN'),
			'password': os.getenv('LEEKWARS_PASSWORD'),
			'behavior': behavior.EQUALIZE, # how we spend fights in the garden
			'strategy': strategy.RANDOM, # how we choose opponent in the garden
			'buy_fight': False, # will try to buy fights if set to True
			'limit': 50, # if behavior != TODOLIST, how many fights we always keep in stock
			'team_limit': 10, # to not do any team fight, comment this line, or set it to 20 or above (0 is minimum)
			'todolist': { # only needed if behavior = TODOLIST
				g.FARMER: 0,
				g.LEEK_1: 0,
				g.LEEK_2: 0,
				g.LEEK_3: 0,
				g.LEEK_4: 0,
			},
			'tournaments': [ # will try to register tournament for everything listed here
				g.FARMER,
				g.LEEK_1,
				g.LEEK_2,
				g.LEEK_3,
				g.LEEK_4,
			],
			'goals': { # will try to speed capital according to this
				g.LEEK_1: goal.NONE,
				g.LEEK_2: goal.FOCUS_LIFE,
				g.LEEK_3: goal.FOCUS_STRENGTH,
				g.LEEK_4: goal.FOCUS_WISDOM,
			},
			'synchronize': { # /!\ careful with this /!\
				'directory': './path_to_ia_dir', # local directory to read/write
				'transfer': g.DOWNLOAD,
			},
		},
		# Example of a second account:
		# {
		# 	'login': os.getenv('LEEKWARS_LOGIN_2'),
		# 	'password': os.getenv('LEEKWARS_PASSWORD_2'),
		# 	'behavior': behavior.NONE,
		# 	'synchronize': { # /!\ careful with this /!\
		# 		'directory': './path_to_ia_dir', # local directory to read/write
		# 		'transfer': g.UPLOAD,
		# 		'version': '4', # leekscript version when creating new files
		# 		'ignore': [
		# 			'.git', # files to ignore when uploading
		# 			'README.MD'
		# 		],
		# 	},
		# },
	]
