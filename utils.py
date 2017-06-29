import os.path
from collections import namedtuple

from log_conf import get_logger

LOGGER = get_logger(__name__)

LOCATION = namedtuple('LOCATION', 'latitude, longitude')

SOURCE_LOCATION = LOCATION('12.9611159', '77.6362214')

FRIEND_LIST_SOURCES = ('file',)

def is_valid_coordinate_format(coordinate_point=None):

	if not coordinate_point: 
		return False
	coordinate_point = coordinate_point.strip()

	if coordinate_point.count('.') == 1:
		number_before_decimal, number_after_decimal = coordinate_point.split('.')

		if number_before_decimal.startswith('-'): 
			number_before_decimal = number_before_decimal[1:]

		if number_before_decimal.isdigit() and number_after_decimal.isdigit():
			return True
		else:
			return False
	else:
		return False

def is_valid_coordinates_value(latitude=None, longitude=None):

	if not latitude or not longitude:
		return False

	latitude = float(latitude)
	longitude = float(longitude)

	if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
		return False

	return True

def is_valid_location(location=None):

	if not location: 
		return False

	if not isinstance(location, LOCATION):  
		LOGGER.error(
			'Invalid Location type: location should be of type LOCATION, given location is of type : %s ' % str(type(location)))
		return False
	
	latitude = location.latitude
	longitude = location.longitude

	if (not isinstance(latitude, str) and not isinstance(latitude, unicode)) or (not isinstance(longitude, str) and not isinstance(longitude, unicode)):
		LOGGER.error('Invalid Location: latitude and longitude should both be of type str or unicode, given latitude type = %s and longitude type = %s ' % (str(type(latitude)), str(type(longitude))))
		return False
	
	if not is_valid_coordinates_value(latitude, longitude): 
		LOGGER.error(
		    'Invalid coordinate values: Should be -90<=latitude<=90 and -180<=longitude<=180 Given are : %s, %s ' % (latitude, longitude))
		return False

	return True

def is_valid_friends_data(data=None): 

	if not data:
		return False

	if not isinstance(data, dict):
		# logs the error regarding invalid friend data
		LOGGER.error('Bad Data: Data not according to required structure: Data should be in dictionary form')
		return False

	if 'latitude' not in data or 'longitude' not in data or 'name' not in data or 'user_id' not in data:
	    # logs the error regarding invalid inputs keys
	    LOGGER.error(
	        'Invalid Data keys. Data should have all the 4 keys, [longitude], [latitude], [name] and [id]')
	    return False

	if (not isinstance(data['name'], str) and not isinstance(data['name'], unicode)) or not isinstance(data['user_id'], int): 
		# logs the error regarding invalid friend data value types
		LOGGER.error('Bad Data: Data not according to required structure: Name should be of type str or unicode and id of type int.\
			Given data : type(data[name]) : %s and type(data[id]) : %s ' % (str(type(data['name'])), str(type(data['user_id']))))
		return False 

	if (not isinstance(data['latitude'], str) and not isinstance(data['latitude'], unicode)) or (not isinstance(data['longitude'], str) and not isinstance(data['longitude'], unicode)): 
		# logs the error regarding invalid friend data value types
		LOGGER.error('Bad Data: Data not according to required structure: Latitude  and Longitude should be of type str or unicode.\
			Given data : type(data[latitude]) : %s and type(data[longitude]) : %s ' % (str(type(data['latitude'])), str(type(data['longitude']))))
		return False 
	return True

def is_valid_config(config_data=None):

	if not config_data: 
		return False

	if not isinstance(config_data, dict):
		LOGGER.error('Inputs is not valid: Inputs in settings should be a dictionary object')
		return False

	if 'friend_list_source' not in config_data or 'source_path' not in config_data or 'async' not in config_data:
	    LOGGER.error(
	        'Invalid Inputs keys. Settings\' inputs dictionary should have all the 3 keys, [friend_list_source], [source_path] and [async]')
	    return False

	friend_list_source = config_data['friend_list_source']
	source_path = config_data['source_path']
	asynchronous = config_data['async']

	if not isinstance(friend_list_source, str):
	    LOGGER.error('Invalid source type. Source should be of type str.')
	    return False

	if friend_list_source not in FRIEND_LIST_SOURCES:
		LOGGER.error('Invalid source value. Source Value should be from %s ' % str(FRIEND_LIST_SOURCES))

	if (not isinstance(source_path, str) and friend_list_source == 'file') or\
                (source_path is not None and friend_list_source != 'file'):

	    LOGGER.error(
	    	'Invalid Source Path type. Source Path should be of type str when source if file or None if source is not file. ')
	    return False

	if not isinstance(asynchronous, bool):
	    LOGGER.error('Invalid async type. Async should of type bool, i.e, eiher True or False.')
	    return False

	if friend_list_source == 'file' and not os.path.exists(source_path):
	    LOGGER.error('Invalid source path value. source path should a proper directory path')
	    return False

	if not is_valid_location(SOURCE_LOCATION): 
		return False
	return True
