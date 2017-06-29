from utils import is_valid_coordinate_format, is_valid_coordinates_value, is_valid_location,\
	is_valid_friends_data, is_valid_config, LOCATION

def setup_module(module):
    print "\nsetup_module module: %s \n\n" % module.__name__

def teardown_module(module):
    print "\n\nteardown_module module: %s " % module.__name__

def test_is_valid_coordinate_format_with_valid_coordinate(): 
	print
	assert is_valid_coordinate_format(' 12.986375') is True  
	assert is_valid_coordinate_format('-152.986375 ') is True 
	assert is_valid_coordinate_format(' -152.986375 ') is True 

def test_is_valid_coordinate_format_with_Invalid_coordinate(): 
	print
	assert is_valid_coordinate_format('a12.986375') is False  
	assert is_valid_coordinate_format('-152986375') is False 
	assert is_valid_coordinate_format('12.986375a') is False  
	assert is_valid_coordinate_format('-1529 86375') is False
	assert is_valid_coordinate_format('15,86375') is False
	assert is_valid_coordinate_format('ab.cdefghi') is False  
	assert is_valid_coordinate_format() is False  

def test_is_valid_coordinates_value_with_valid_coordinates(): 
	print
	assert is_valid_coordinates_value('12.986375', '77.043701') is True  
	assert is_valid_coordinates_value('80.123456', '-175.12345') is True 
	assert is_valid_coordinates_value('-85.654321', '175.654321') is True 

def test_is_valid_coordinates_value_with_Invalid_coordinates(): 
	print
	assert is_valid_coordinates_value('112.986375', '77.043701') is False  
	assert is_valid_coordinates_value('80.1324242', '-181.000000') is False 
	assert is_valid_coordinates_value('-112.134134', '77.123456') is False 
	assert is_valid_coordinates_value('77.123456') is False 
	assert is_valid_coordinates_value() is False 

def test_is_valid_location_with_valid_location(): 
	print
	destination = LOCATION('12.986375', '77.043701')
	assert is_valid_location(destination) is True  
	destination = LOCATION('80.123456', '-175.12345')
	assert is_valid_location(destination) is True  
	destination = LOCATION('-85.654321', '175.654321')
	assert is_valid_location(destination) is True  

def test_is_valid_location_with_Invalid_location(): 
	print
	destination = ('12.986375', '77.043701')
	assert is_valid_location(destination) is False  
	destination = LOCATION('80.1324242', '-181.000000')
	assert is_valid_location(destination) is False  
	destination = LOCATION('12,134134', '77.123456')
	assert is_valid_location(destination) is False 
	destination = LOCATION(12.987654, '77.123456')
	assert is_valid_location(destination) is False  
	destination = LOCATION('12.975310', '77.8ac765')
	assert is_valid_location(destination) is False  
	destination = LOCATION('a12.457984', '77.87654b')
	assert is_valid_location(destination) is False 
	assert is_valid_location() is False 

def test_is_valid_friends_data_with_valid_data(): 
	print 
	data = {"latitude": "12.986375", "user_id": 12, "name": "Chris", "longitude": "77.043701"}
	assert is_valid_friends_data(data) is True 

def test_is_valid_friends_data_with_Invalid_data(): 
	print 
	data = [{"latitud": "12.986375", "user_id": 12, "name": "Chris", "longitude": "77.043701"}]
	assert is_valid_friends_data(data) is False
	data = data[0] 
	assert is_valid_friends_data(data) is False 
	data = {"latitude": 12.986375, "user_id": 12, "name": "Chris", "longitude": "77.043701"} 
	assert is_valid_friends_data(data) is False 
	data = {"latitude": "12.986375", "id": 12, "name": "Chris", "longitude": "77.043701"} 
	assert is_valid_friends_data(data) is False 
	data = {"latitud": "12.986375", "user_id": "12afd3", "name": "Chris", "longitude": "77.043701"}
	assert is_valid_friends_data(data) is False
	data = {"latitud": "12.986375", "user_id": 12, "username": "Chris", "longitude": "77.043701"}
	assert is_valid_friends_data(data) is False 
	data = {"latitude": 12.986375, "user_id": 12, "name": ["Chris", "harris"], "longitude": "77.043701"} 
	assert is_valid_friends_data(data) is False 
	data = {"latitude": "12.986375", "id": 12, "name": "Chris", "lon": "77.043701"} 
	assert is_valid_friends_data(data) is False 
	data = {"latitude": "12.986375", "id": 12, "name": "Chris", "longitude": 77.043701} 
	assert is_valid_friends_data(data) is False 
	assert is_valid_friends_data() is False

def test_is_valid_config_with_good_configurations(): 
	print 
	good_config = {	
					'friend_list_source': 'file', 
					'source_path': 'friends.json',
					'async': True
				}

	assert is_valid_config(good_config) is True

def test_is_valid_config_with_bad_configurations(): 
	print 
	bad_config = [{	
					'source': 'file', 
					'source_path': 'friends.json',
					'async': True
				}]

	assert is_valid_config(bad_config) is False
	bad_config = bad_config[0]
	assert is_valid_config(bad_config) is False
	del bad_config['source']
	bad_config['friend_list_source'] = 1
	assert is_valid_config(bad_config) is False 
	bad_config['friend_list_source'] = 'invalid_source' 
	assert is_valid_config(bad_config) is False 
	bad_config['friend_list_source'] = 'file' 
	bad_config['source_path'] = ('path/to/source')
	assert is_valid_config(bad_config) is False
	del bad_config['source_path']
	assert is_valid_config(bad_config) is False
	bad_config['source_path'] = 'friends.json'
	bad_config['async'] = 1
	assert is_valid_config(bad_config) is False  
	del bad_config['async']
	assert is_valid_config(bad_config) is False
	bad_config['asynchronous'] = True
	assert is_valid_config(bad_config) is False
	assert is_valid_config() is False
