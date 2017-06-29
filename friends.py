from concurrent.futures import ProcessPoolExecutor
from functools import partial
from operator import itemgetter
import json
import os.path
import math
import time
import invite_friends_config as config 
from utils import is_valid_location, is_valid_friends_data, is_valid_config, LOCATION, SOURCE_LOCATION
from log_conf import get_logger

LOGGER = get_logger(__name__)

RADIUS = 6371 											

SMALL_FILE_SIZE = 8

FILE_INPUT_BUFFER_SIZE = SMALL_FILE_SIZE * 1024 * 1024

SHOULD_VALIDATE_INDIVIDUAL_DATA = True

DISTANCE_RANGE = 100

GLOBAL_RESULT = []

bad_inputs = []

def calculate_distance(location_destination, location_source=SOURCE_LOCATION):

	if location_source != SOURCE_LOCATION and not is_valid_location(location_source):
		raise Exception 

	if not is_valid_location(location_destination):
		raise Exception	

	latitude_source = float(location_source.latitude)
	longitude_source = float(location_source.longitude)
	latitude_destination = float(location_destination.latitude)
	longitude_destination = float(location_destination.longitude)  

	phi_1 = math.radians(latitude_source)
	phi_2 = math.radians(latitude_destination)
	delta_lambda = math.radians(longitude_destination - longitude_source)
	delta_sigma = math.acos((math.sin(phi_1) * math.sin(phi_2)) +
	                        (math.cos(phi_1) * math.cos(phi_2) * math.cos(delta_lambda)))
	result = RADIUS * delta_sigma

	return result

def process_friends_data_worker(data, testing=False):
	
	if testing:
		bad_data_testing = list()
		good_result_testing = list()
		good_data_testing = list()
		test_data_length = len(data)
 
	distance = 100.0
	
	for friend_item in data: 
		json_decoded_friends_data = json.loads(friend_item)  

		LOGGER.debug('CHECK BUG LINE 1 : json_decoded_friends_data : type= %s and\nValue : %s ' % (str(type(json_decoded_friends_data)), json_decoded_friends_data)) 

		if SHOULD_VALIDATE_INDIVIDUAL_DATA and not is_valid_friends_data(json_decoded_friends_data): 

			LOGGER.debug('Not Valid Friends Data : data = %s ' % json_decoded_friends_data) 
			if not testing:

				LOGGER.debug('bad_inputs data  appending : %s ' % json_decoded_friends_data) 
				bad_inputs.append(json_decoded_friends_data) 
				LOGGER.debug('bad_inputs lenthg : %d ' % len(bad_inputs)) 
			else: 

				LOGGER.debug('bad_testing_data appending : %s ' % json_decoded_friends_data)   
				bad_data_testing.append(json_decoded_friends_data)
				LOGGER.debug('bad_testing_data  lenthg : %d ' % len(bad_data_testing))

			LOGGER.debug('continue with rest of loop') 
			continue

			LOGGER.debug('THIS LINE SHOULD NOT BE ADDED - IF ADDED THEN SOMETHING WRONG WITH CODE') 
		
		friends_location_coordinates = LOCATION(json_decoded_friends_data['latitude'], json_decoded_friends_data['longitude'])
		
		try: 
			distance = calculate_distance(location_destination=friends_location_coordinates) 
		 
		except:  
			if not testing:

				LOGGER.debug('bad_inputs data  appending : %s ' % json_decoded_friends_data) 
				bad_inputs.append(json_decoded_friends_data) 
				LOGGER.debug('bad_inputs lenthg : %d ' % len(bad_inputs)) 
			else:

				LOGGER.debug('bad_testing_data appending : %s ' % json_decoded_friends_data)   
				bad_data_testing.append(json_decoded_friends_data)
				LOGGER.debug('bad_testing_data  lenthg : %d ' % len(bad_data_testing)) 

			LOGGER.debug('Continue Statement since bad_data') 
			continue
			LOGGER.debug('THIS LINE SHOULD NOT BE PRINTED, IF IT DOES, THEN SOMETHIN IS WRONG IN CODE')

		if distance < DISTANCE_RANGE:

			LOGGER.debug('json_decoded_friends_data : type= %s and\nValue : %s ' % (str(type(json_decoded_friends_data)), json_decoded_friends_data)) 
			LOGGER.debug('distance qualified : %f ' % distance)
			if not testing:

				LOGGER.debug('Adding Good Resuly appending : %s ' % json_decoded_friends_data) 
				GLOBAL_RESULT.append(json_decoded_friends_data) 
				LOGGER.debug('GLOBAL_RESULT lenthg : %d ' % len(GLOBAL_RESULT))
			else: 

				LOGGER.debug('Adding Testing Good Result appending : %s ' % json_decoded_friends_data) 
				good_result_testing.append(json_decoded_friends_data)
				LOGGER.debug('good_result_testing lenthg : %d ' % len(good_result_testing))
			LOGGER.debug('CHECK BUG LINE 2')
		else:
			if testing: 
				good_data_testing.append(json_decoded_friends_data)

	LOGGER.debug('GOOD_RESULT TILL NOW length : %d ' % len(GLOBAL_RESULT))
	LOGGER.debug('bad_inputs  TIll Now length : %d ' % len(bad_inputs))

	if testing: 
		if len(bad_data_testing) + len(good_result_testing) + len(good_data_testing) != test_data_length:
			return False
		return True

def _dummy_process_data_worker_function(data):
	
	if data is not None and len(data) > 0: 
		return True 
	raise Exception

def read_friend_list(source_path, asynchronous, testing=False): 
	
	file_size = None
	executor_futures_result = None 

	try:
		file_size = os.path.getsize(source_path) / float(1024 * 1024)

	except OSError:
		LOGGER.error('File does not exist or permission is denied at path: %s ' % source_path)
		raise

	friends_data = list()

	if file_size <= SMALL_FILE_SIZE: 
		LOGGER.info('Input Friend List file size is small : size in MB = %d ' % file_size)
		
		with open(source_path, 'rb') as input_file:
			friends_data = input_file.readlines()
			if not testing:
				process_friends_data_worker(friends_data) 
			else: 
				LOGGER.info('Testing read_friend_list functionality, hence not passing the opened file for processing') 

	else:
		LOGGER.info('Input Friend List file size is large : size in MB = %s ' % str(file_size))
	
		with open(source_path, 'rb') as input_file:
			LOGGER.debug('Input File Opened as input_file') 
			if asynchronous is True:
				LOGGER.debug('asynchronous is True') 
				with ProcessPoolExecutor() as executor: 
					partial_readlines = partial(input_file.readlines, FILE_INPUT_BUFFER_SIZE) 
					iterator_for_executor_map = iter(partial_readlines, [])
					if not testing:
						try:
							executor.map(process_friends_data_worker, iterator_for_executor_map, chunksize=1)
						except: 
							return
					else: 
						try: 
							executor.map(_dummy_process_data_worker_function, iterator_for_executor_map, chunksize=1) 
						except: 
							return 
				return executor_futures_result
			
			else:
				LOGGER.debug('asynchronous is False') 
				while True:
					LOGGER.debug('Starting While Loop') 
					friends_data = input_file.readlines(FILE_INPUT_BUFFER_SIZE)
					if not friends_data:
						LOGGER.debug('Friend data is None')
						LOGGER.debug('Breaking from Loop Now') 
						break
						LOGGER.debug('THIS LINE SHOULD NOT BE PRINTED _ ELSE SOMETHING WRONG WITH CODE')
					else:
						LOGGER.debug('Friend data is not None - calling process_friends_data_worker') 
						if not testing:
							LOGGER.debug('Testing = False --> Friend data is not None - calling process_friends_data_worker')
							process_friends_data_worker(friends_data)

	if testing:
		LOGGER.debug('Testing is True, now return True') 
		return True 

def print_bad_inputs(inputs=None):

	if inputs is None: 
		inputs = bad_inputs
	
	count = len(inputs) 

	if count < 0: 
		LOGGER.error('Found %d bad_inputs ' % count) 
		print 'Bad Inputs : \n'
		for i in xrange(count): 
			print str(i + 1) + '.  ', inputs[i] 

	else: 
		print ''

def print_invitation_list(invitation_list=None):

	if invitation_list is None: 
		invitation_list = GLOBAL_RESULT 

	if invitation_list == []: 
		LOGGER.info('Found 0 friends nearby to send invitations')
		print 'Found 0 friends nearby to send invitations' 

	else: 
		invitation_list.sort(key=itemgetter('user_id')) 
		
		count = len(invitation_list)
		
		LOGGER.info('Found %d qualified friends ' % count)

		print 'The names and user Id\'s of matching friends, sorted by user Id within range\n'
		for i in xrange(count): 
			print str(i + 1) + '.  ' + 'Id: ', invitation_list[i]['user_id'], ' Name: ' + invitation_list[i]['name'] 

def invite_friends(friend_list_source, source_path=None, asynchronous=False):

	if friend_list_source == 'file':
		try:
			start_time = time.time()
			LOGGER.debug('Call read_friend_list()')
			read_friend_list(source_path, asynchronous)
			LOGGER.debug('Returned from read_friend_list()')
			LOGGER.debug('GOOD_RESULT FINAL length : %d ' % len(GLOBAL_RESULT))
			LOGGER.debug('bad_inputs  FINAL length : %d ' % len(bad_inputs))
			reading_time = time.time() - start_time
			LOGGER.info('Invitatoin Generation Time: %f seconds ' % reading_time)
		except:
			return 

		print_bad_inputs()
		print_invitation_list()

	else:
		print '\nThese advanced features will be implemented soon\nKeep following\n\n'
		raise NotImplementedError

def main():
	config_data = config.inputs
	
	if not is_valid_config(config_data):
	    return

	friend_list_source = config_data['friend_list_source']
	source_path = config_data['source_path']
	asynchronous = config_data['async']

	invite_friends(friend_list_source, source_path, asynchronous) 

if __name__ == "__main__":
    main()
