import json, csv, sys
from pprint import pprint

def buildCSV(output_file_name, platform):
	# Read Firebase JSON data file
	with open('depression-' + platform + '-data.json') as data_file:    
	    data = json.load(data_file)

	# Create new csv file
	output = open(output_file_name + '.csv', 'wb')
	wr = csv.writer(output, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
	HEADERS = ['test_id', 'user_id', 'age', 'college', 'ethnicity', 'firstGenerationCollege', 'gender', 'latitude', 'longitude', 'themePreference', 'yearInSchool']

	test_data = data['tests']
	SCORE_CATEGORIES = ['anhedonia', 'appetite', 'cognition-concentration', 'energy', 'guilt', 'mood', 'psychomotor', 'red-flag', 'sleep-disturbance', 'suicide', 'familyunderstands', 'familysituation', 'culturalbackground', 'appointment', 'fearofstranger', 'adequateresources']
	wr.writerow(HEADERS + ['startTimestamp', 'endTimestamp'] + SCORE_CATEGORIES)

	user_data = data['users']

	TEST_BASE_ID = len(user_data) + 500

	for i, user_id in enumerate(user_data):
		user = user_data[user_id]

		### Filtering invalid data
		# Age
		if 'age' not in user or user['age'] == -1:
			user['age'] = None

		# College
		if 'college' not in user or user['college'] == 'n/a':
		    user['college'] = None
		else:
			user['college'] = user['college'].replace(',', '')

		# Ethnicity
		if 'ethnicity' not in user or user['ethnicity'] == 'n/a':
		    user['ethnicity'] = None
		else:
			user['ethnicity'] = user['ethnicity'].lower()
			if user['ethnicity'] == 'other asian south asian':
				user['ethnicity'] = 'other asian/south asian'

		# first generation college student
		# correctly checking if age exists because demographic data is all or none
		if 'firstGenerationCollege' not in user or user['age'] == None:
			user['firstGenerationCollege'] = None
		else:
			if user['firstGenerationCollege'] == True or user['firstGenerationCollege'] == 'yes' or user['firstGenerationCollege'] == 'Yes':
				user['firstGenerationCollege'] = True
			else:
				user['firstGenerationCollege'] = False

		# Gender
		if 'gender' not in user or user['gender'] == 'n/a':
		    user['gender'] = None
		else:
			user['gender'] = user['gender'].lower()

		# Location
		if 'latitude' not in user or user['latitude'] == 999 or user['latitude'] == 0.0:
			user['latitude'] = None
		if 'longitude' not in user or user['longitude'] == 999 or user['longitude'] == 0.0:
			user['longitude'] = None

		# Theme preference
		if 'themePreference' not in user:
		    user['themePreference'] = 'ice'

		# Year in school
		if 'yearInSchool' not in user or user['yearInSchool'] == 'n/a':
		    user['yearInSchool'] = None
		else:
			user['yearInSchool'] = user['yearInSchool'].encode('utf-8')

		### end filtering invalid data

		# append user demographic info to row
		user_row = []
		for column_title in HEADERS[2:]: # skip test_id and user_id
			user_row.append(user[column_title])

		### users' tests

		user.setdefault('testIDs', None)
		tests_taken = user['testIDs']
		if not tests_taken:
			continue

		test_row = []
		# for each test the user has taken
		for key in tests_taken:
			if tests_taken[key] in test_data:
				test = test_data[tests_taken[key]]
				# timestamps
				test_row = [test['startTimestamp'].replace('\'', ''), test['endTimestamp'].replace('\'', '')]
				# scores
				for category in SCORE_CATEGORIES:
					if category in test['scores']:
						test_row.append(test['scores'][category])
					else:
						test_row.append(None)

				# test_id, user_id, user data, test data
				row = [TEST_BASE_ID, i] + user_row + test_row
				wr.writerow(row)
				TEST_BASE_ID += 1


		### end users' tests


def main(platform):
	buildCSV('output-' + platform, platform)
	print("depression-" + platform + "-data.csv outputed")

if __name__ == "__main__":
	args = sys.argv
	if len(args) != 2:
		print("Needs argument for mobile platform [android|ios]: python parse.py [ios|android]")
		exit()
	main(args[1])