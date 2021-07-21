# Ben Olson 12.2018 
# 
# program to help track donation donors and dates
#  
# single log of donation usage and date.
# program provides a function to export a log 
# file in formatted output summarizing 
# donation dates and $ owed to donor (to be submitted
# to manager)

import datetime
import os
import os.path
from dateutil.parser import parse

donor_list = []
choices =['L','D', 'G','ERASE_LOG','E', 'EXIT',]
curr_dir = os.getcwd()
donor_log_file = os.path.join(curr_dir,'donorLog.txt')

def get_donor():
	donor_choice = input('Please enter donor initials: ')
	length = len(donor_choice) 
	while length == 0:
		donor_choice = input('Must enter value for donor initials : ')
		length = len(donor_choice)
	return donor_choice 

def get_date():
	donation_date = ''
	today_yn = input('Enter Date (T = today) or MM/DD/YYYY: ')

	try:
		if today_yn.upper() == 'T':
			now = datetime.datetime.now()
			return(now.strftime('%m-%d-%Y'))

		donation_date = parse(today_yn, dayfirst = False) #prevent misinterpreation of 25.1.10 -> 1.25.19
		donation_date = donation_date.strftime('%m-%d-%Y')

	except:
		print('EXCEPT BLOCK')
		return get_date()

	return donation_date

def log_donation():
	#write to donor log file
	curr_dir = os.getcwd()
	
	donor = get_donor()
	date = get_date()

	while str(date) == 'None':
		print('Error in date (return \'None\'), please try again. \n')
		date = get_date()
	
	with open(donor_log_file, 'a') as f:
		f.write(donor + '\n')
		f.write(str(date) + '\n')

	print('DONATION LOGGED')

def display_log():
	#print contents to console
	if os.path.exists(donor_log_file):
		print('___________DONOR LOG__________')
		with open(donor_log_file,'r') as f:
			print(f.read())
	else:
		print('Donor log does not exist yet. Log donations to create file\n\n')

def generate_report():

	donor_dict = {}

	#bulk read, create donor/date dictionary
	if os.path.exists(donor_log_file):
		report_dest = os.path.join(curr_dir, 'Donor_Reports')

		if not os.path.exists(report_dest):
			os.makedirs(report_dest)

		with open(donor_log_file,'r') as f:
			line = f.readline()

			while(line):
				if line[0].isalpha():
					donor_ID = line.rstrip() #remove newline and trailing whitespace 
					donation_date = f.readline().rstrip()

					donor_dict.setdefault(donor_ID, [])
					donor_dict[donor_ID].append(donation_date)

				line = f.readline()

		month = input('Generate report for which Month?: ')

		for key in donor_dict.keys():
			report_file = os.path.join(report_dest, key + '.txt')
			count = 0
			donor_name = input('Complete name for donor [' + key + ']: ')

			with open(report_file, 'a+') as output:
				#header
				output.write('\t' + 'Donation Log\n')
				output.write('\t' + month + '\n')
				output.write('\t' + donor_name + '\n')
				output.write('_' * 20 + '\n')

				#bulk write
				for date in donor_dict[key]:
					output.write(date + '\n')
					count += 1
				
				#total (footer)
				output.write('_' * 20 + '\n')
				total = str(50 * count)
				output.write('Total = $' + total)

		print('Reports Generated!')
		print('Files in \'Donor_Reports\' folder\n')

	else:
		print('DonorLog.txt File does not exist. Log donations first. Cannot generate report(s)\n\n')

def erase_log():
	confirm = input('Are you sure you want to erase donor log? (Y/N): ')

	if confirm.upper() == 'Y':
		os.remove(donor_log_file)
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

	elif action == 'E' or action.upper() == 'EXIT':
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
