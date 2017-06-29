import pytest
import random
import json
import time

from invite_friends import calculate_distance, process_friends_data_worker, read_friend_list,\
    print_bad_inputs, print_invitation_list, invite_friends
from utils import LOCATION

def setup_module(module):
    print "\nsetup_module module: %s \n\n" % module.__name__
    try:
        create_large_input_file('friends_large.json', 1000000)
    except:
        print 'unable to create large input file'

def teardown_module(module):
    print "\n\nteardown_module module: %s " % module.__name__

def test_calculate_distance_with_valid_inputs():
    destination = LOCATION('12.986375', '77.043701')
    print
    assert calculate_distance(destination) == 64.26480291995638
    destination = LOCATION('80.123456', '-175.12345')
    assert calculate_distance(destination) == 8909.980105033259
    destination = LOCATION('-85.654321', '175.654321')
    assert calculate_distance(destination) == 11511.948749243722

def test_calculate_distance_with_invalid_inputs():
    print
    with pytest.raises(Exception):
        destination = LOCATION('112.986375', '77.043701')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION('80.1324242', '-181.000000')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION('12,134134', '77.123456')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION(12.987654, '77.123456')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION('12.975310', '77.8ac765')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION('a12.457984', '77.87654b')
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        destination = LOCATION(('12.986375', '77.043701'))
        assert calculate_distance(destination)
    with pytest.raises(Exception):
        assert calculate_distance()

def create_large_input_file(filename, num_of_entries):
    def _lat():
        return "{:.6f}".format(random.uniform(-90, 90))

    def _lon():
        return "{:.6f}".format(random.uniform(-180, 180))

    def _user_name():
        return ''.join([random.choice('abcdefgjhijklmnopqrstuvwzyz') for _ in xrange(random.randrange(5, 15))]) +\
            ''.join([random.choice('abcdefgjhijklmnopqrstuvwzyz')
                     for _ in xrange(random.randrange(5, 15))])

    def _create_item(user_id):
        return {'latitude': _lat(), 'user_id': user_id, 'name': _user_name(), 'longitude': _lon()}

    with open(filename, 'w') as output_file:
        for i in xrange(num_of_entries):
            json.dump(_create_item(i), output_file)
            output_file.write('\n')

def test_read_friend_list_with_valid_source_path():
    print
    s = time.time()
    assert read_friend_list(source_path='friends.json', asynchronous=False, testing=True) is True
    print 'Done'
    print 'Reading took : %s seconds' % str(time.time() - s)
    s = time.time()
    assert read_friend_list(source_path='friends.json', asynchronous=True, testing=True) is True
    print 'Done'
    print 'Reading took : %s seconds' % str(time.time() - s)
    s = time.time()
    assert read_friend_list(source_path='friends_large.json',
                            asynchronous=False, testing=True) is True 
    print 'Done'
    print 'Reading took : %s seconds' % str(time.time() - s)
    s = time.time()
    assert read_friend_list(source_path='friends_large.json',
                            asynchronous=True, testing=True) is None
    print 'Done' 
    print 'Reading took : %s seconds' % str(time.time() - s)

def test_read_friend_list_with_invalid_source_path():
    print
    with pytest.raises(Exception):
        assert read_friend_list(source_path='friens.json', asynchronous=False, testing=True)
    with pytest.raises(Exception):
        assert read_friend_list(source_path='/usr/local/etc/friends.json',
                                asynchronous=True, testing=True)

def test_process_friends_data_worker_with_valid_data(): 
    print 
    with open('friends.json', 'rb') as input_file:
            data = input_file.readlines(8192) 
            assert process_friends_data_worker(data, testing=True) is True
            
def test_print_bad_inputs(): 
    inputs = [
                {"latitude": "12.240382", "user_id": "10", "name": "Georgina", "longitude": "77.972413"},
                {"latitude": "12.240382", "user_id": 10, "name": "Georgina", "longitude": 77.972413}
            ]
    print
    assert print_bad_inputs(inputs) is None

def test_print_invitation_list(): 
    print
    invitation_list = [ 
                        {"latitude": "12.240382", "user_id": 10, "name": "Georgina", "longitude": "77.972413"},
                        {"latitude": "13.2411022", "user_id": 4, "name": "Ian", "longitude": "77.238335"},
                        {"latitude": "13.1302756", "user_id": 5, "name": "Nora", "longitude": "77.2397222"}
                    ] 

    assert print_invitation_list(invitation_list) is None

def test_invite_friends_with_source_as_file(): 
    print
    assert invite_friends(friend_list_source='file', source_path='friends.json', asynchronous=False) is None 

def test_invite_friends_with_source_not_as_file(): 
    print
    with pytest.raises(NotImplementedError):
        assert invite_friends(friend_list_source='mongodb', source_path=None, asynchronous=False)
