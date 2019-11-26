#!/usr/bin/env python3
from settings import Accounts
from todolist import Todolist
from utils import bcolors, g, behavior, state
from lwapi import lwapi
import os

#################################################################
# Main program
#################################################################
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


# main loop
for account in Accounts.list:
	login = account.get('login')
	password = account.get('password')

	api = lwapi(login, password)
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

	# do the fights
	for leekid in todo.getGenerator():
		is_farmer = leekid == g.FARMER
		if is_farmer:
			fight_id = api.farmer_fight()
		else:
			fight_id = api.solo_fight(leeks_to_ID[leekid])
		# waiting for result
		api.wait_fight_result(fight_id, is_farmer)
		# try spending capital after each fight
		if account.get('goals'):
			todo.trySpendCapital()

	# display status when fights are done
	if account.get('behavior') != behavior.NONE:
		api.display_status()


if should_shutdown:
	os.system('shutdown -s -t 0')
