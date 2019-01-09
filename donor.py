# Ben Olson 12.2018 
# 
# program to help track AR donor samples
#  
# single log of fresh sample usage and date.
# program provides a function to export a log 
# file in formatted output summarizing fresh
# donation dates and $ owed to donor (to be submitted
# to practice manager)

import datetime
import os
import shutil

donor_list = []
choices =['L','D','E', 'EXIT','G','ERASE_LOG']
curr_dir = os.getcwd()

def get_donor():
	donor_choice = input('Please enter donor initials: ') 
	return donor_choice 

def get_date():
	donation_date = ''
	today_yn = input('Donation date? ((T = today) or mm.dd.yyyy: ')

	if len(today_yn) == 0 :
		return ('No Date Entered')

	if today_yn.upper() == 'T':
		now = datetime.datetime.now()
		donation_date = now.strftime('%m-%d-%Y')

	else:
		donation_date = today_yn

	return donation_date

def log_donation():
	#write to donor log file
	donor = get_donor()
	date = get_date()
	print('....writing donor and date to file...')

	with open(os.path.join(curr_dir,'donorLog.txt'), 'a') as f:
		f.write(donor)
		f.write('\n')
		f.write(date)
		f.write('\n')

def display_log():
	#print contents to console
	print('___________DONOR LOG__________')
	with open('donorLog.txt','r') as f:
		print(f.read())

def generate_report():
	print('generating individual reports...')
	print('*\n' * 5)

	report_dest = os.path.join(curr_dir, 'Donor_Reports')

	if not os.path.exists(report_dest):
		os.makedirs(report_dest)

	with open('donorLog.txt','r') as f:
		line = f.readline()

		while(line):
			if line[0].isalpha():
				line = line.rstrip() #remove newline and trailing whitespace 
				report_file = os.path.join(report_dest, line + '.txt')
				with open(report_file, 'a+') as f2:
					line2 = f.readline()
					#print('line2 is: ' + line2)
					f2.write(line2)

				donor_list.append(line)

			line = f.readline()

	print('Reports Generated!')
	print('Files in \'Donor_Reports\' folder\n')

def erase_log():
	confirm = input('Are you sure you want to erase donor logs? (Y/N): ')

	if confirm.upper() == 'Y':
		report_dest = os.path.join(curr_dir, 'Donor_Reports')

		with open('donorLog.txt','w') as f:
			pass 

		shutil.rmtree(report_dest)
		return True

	else:
		return False


def perform_action(action):
	if action == 'L':
		log_donation()

	elif action == 'D':
		display_log()

	elif action == 'G':
		generate_report()

	elif action == 'ERASE_LOG':
		success = erase_log()

		if success:
			print('*****LOG ERASED \n')

		else:
			print('*****No action taken')

	elif action == 'E' or action == 'EXIT':
		print('...Exit...')
		exit()

	else:
		print('Action not defined')

def home_screen():
	print('What would you like to do?\n')
	print('\tLog Donation (L)')
	print('\tDisplay Log (D)')
	print('\tGenerate report (G)')
	print('\tErase log (ERASE_LOG)')
	print('\tExit (E)\n')

	choice = input('****Choice: ')

	while choice.upper() not in choices:
		print('INVALID INPUT, PLEASE TRY AGIAN')
		choice = input('****CHOICE: ')

	print('')

	return choice


#####    MAIN     ######	
choice = ''

while(True):
	choice = home_screen()
	perform_action(choice.upper())

#print('current date: ')
#print(now.strftime('%m-%d-%Y'))

