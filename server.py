import aes
import os, random, string
import database
from secretsharing import SecretSharer

def process_image(filename,k,n,users,sender_id):
	# AES Key 
	key = 'a'*32

	# Encrypting Image and Deleting the file
	aes.encrypt_file(key,filename)
	#os.remove(filename)

	# Splitting AES Key into N parts
	shares = SecretSharer.split_secret(key,k,n)

	# Creating a New Message
	msg_id = database.new_message(filename + '.enc', k, sender_id)
	users.insert(0,sender_id)
	
	# Updating message queue
	database.update_message_queue(users,shares,msg_id)

def mark_key_sent(msg_id, user_id):
	database.mark_key_sent(msg_id, user_id)

def mark_key_received(msg_id, user_id, subkey):
	database.mark_key_received(msg_id, user_id, subkey)
	
def send_decrpyted_image(filename,shares,k):
	key = SecretSharer.recover_secret(shares[0:k]) 
	aes.decrypt_file(key,filename)

def count_thres_num_users(msg_id):
	return database.count_thres_num_users(msg_id)

def remove_from_message_queue(msg_id, user_id):
	database.remove_from_message_queue(msg_id, user_id)

def count_num_users(msg_id):
	return database.count_num_users(msg_id)

#process_image('img.jpg',2,3,[3,4],2)
#mark_key_sent(12,2)
remove_from_message_queue(12,4)
print count_num_users(12)

database.connection_close()
