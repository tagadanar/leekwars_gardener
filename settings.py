from utils import g, behavior, shutdown, goal

#################################################################
# Declaring accounts
#################################################################
class Accounts:
	shutdown = shutdown.OFF
	list= [
		{
			'login': 'myAccount',
			'password': 'myPassword',
			'behavior': behavior.EQUALIZE,
			'limit': 50, # if behavior != TODOLIST, how many fights we always keep in stock
			'todolist': { # only needed if behavior = TODOLIST
				g._FARMER_: 0,
				g._LEEK_1_: 0,
				g._LEEK_2_: 0,
				g._LEEK_3_: 0,
				g._LEEK_4_: 0,
			},
			'goals': {
				g._LEEK_1_: goal.NONE,
				g._LEEK_2_: goal.FOCUS_LIFE,
				g._LEEK_3_: goal.FOCUS_STRENGTH,
				g._LEEK_4_: goal.FOCUS_WISDOM,
			},
		},
		{
			'login': 'myAccount2',
			'password': 'myPassword2',
			'behavior': behavior.NONE,
		},
	]
