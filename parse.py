import json, csv
from pprint import pprint

# Read Firebase JSON data file
with open('depression-ios-data.json') as data_file:    
    data = json.load(data_file)

# Create new csv file
output = open('output.csv', 'wb')
wr = csv.writer(output, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
# HEADERS = ['id', 'age', 'college', 'ethnicity', 'firstGenerationCollege', 'gender', 'latitude', 'longitude']
HEADERS = ['id', 'age', 'college', 'ethnicity', 'firstGenerationCollege', 'gender', 'latitude', 'longitude', 'themePreference', 'yearInSchool']
wr.writerow(HEADERS)

# test_data = data['tests']
user_data = data['users']

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

	# first generation college student
	# correctly checking if age exists because demographic data is all or none
	if 'firstGenerationCollege' not in user or user['age'] == None:
		user['firstGenerationCollege'] = None

	# Gender
	if 'gender' not in user or user['gender'] == 'n/a':
	    user['gender'] = None

	# Location
	if user['latitude'] == 999:
		user['latitude'] = None
	if user['longitude'] == 999:
		user['longitude'] = None

	# Theme preference
	if 'themePreference' not in user:
	    user['themePreference'] = 'ice'

	# Year in school
	if 'yearInSchool' not in user or user['yearInSchool'] == 'n/a':
	    user['yearInSchool'] = None


	### end filtering invalid data

	user.setdefault('testIDs', None)


	tests_taken = user['testIDs']
	row = [i]
	for column_title in HEADERS[1:]:
		row.append(user[column_title])
		print(user[column_title])
	try:
		wr.writerow(row)
	except KeyError as err:
		print(user)
		print("key error: {0}".format(err))