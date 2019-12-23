#!/usr/bin/env python3
from settings import Accounts
from todolist import Todolist
from utils import bcolors, g, behavior, state
from lwapi import lwapi
import os, sys

def main():
	#################################################################
	# handling command line arguments
	#################################################################
	should_fight = False
	if Accounts.fight == state.ON:
		should_fight = True
	elif Accounts.fight == state.ASK:
		answer = input('Should fight in the garden ? y/N')
		if answer == "y":
			should_fight = True

	should_synchronize = False
	if Accounts.synchronize == state.ON:
		should_synchronize = True
	elif Accounts.synchronize == state.ASK:
		answer = input('Should synchronize ia before running todolist ? y/N')
		if answer == "y":
			should_synchronize = True

	should_shutdown = False
	if Accounts.shutdown == state.ON:
		should_shutdown = True
	elif Accounts.shutdown == state.ASK:
		answer = input('Should shutdown computer at the end ? y/N')
		if answer == "y":
			should_shutdown = True

	# overriding config with arguments from command line
	opts = sys.argv[1:]
	for o in opts:
		if o in ("-f", "--fight"):
			should_fight = True
		elif o in ("-nf", "--no-fight"):
			should_fight = False
		elif o in ("-s", "--sync"):
			should_synchronize = True
		elif o in ("-ns", "--no-sync"):
			should_synchronize = False
		else:
			print("%s/!\\%s Unhandled option: %s%s %s/!\\%s"%(bcolors.FAIL,bcolors.WARNING,bcolors.HEADER,o,bcolors.FAIL,bcolors.ENDC))

	#################################################################
	# Main program
	#################################################################

	# main loop
	for account in Accounts.list:
		api = lwapi(account)
		# connecting to leekwars
		farmer = api.connect()
		
		# welcome & get leeks to realID
		leeks_to_ID = api.display_status()

		# init todolist
		todo = Todolist(account, api)
		
		# syncronize ia
		if should_synchronize:
			todo.trySynchronize()

		# register tournaments if needed
		if account.get('tournaments'):
			todo.registerTournaments()

		# try spending capital once
		if account.get('goals'):
			todo.trySpendCapital()

		# try fighting
		if should_fight:
			for leekid in todo.getGenerator():
				is_farmer = leekid == g.FARMER
				if is_farmer:
					fight_id = api.farmer_fight()
				else:
					fight_id = api.solo_fight(leeks_to_ID[leekid])
				if fight_id is None:
					continue
				# waiting for result
				api.wait_fight_result(fight_id, is_farmer)
				# try spending capital after each fight
				if account.get('goals'):
					todo.trySpendCapital()

		# display status when fights are done
		if should_fight and account.get('behavior') != behavior.NONE:
			api.display_status()

	if should_shutdown:
		os.system('shutdown -s -t 0')


if __name__ == "__main__":
	main()