import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='testuser',
                             password='password',
                             db='testdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def update_message_queue(users,shares,msg_id):
	for i in range(0,len(users)):
		with connection.cursor() as cursor:
			sql = "INSERT INTO `message_queue` (`msg_id`, `user_id`, `subkey`, `status`) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (int(msg_id), int(users[i]), shares[i], int(0)))
		connection.commit()

def new_message(location, thres_num_users, sender_id):
	with connection.cursor() as cursor:
		sql = "INSERT INTO `message` (`location`, `is_encrypted`, `thres_num_users`, `sender_id`) VALUES (%s, %s, %s, %s)"
		cursor.execute(sql, (location, int(1), int(thres_num_users), int(sender_id)))
		msg_id = cursor.lastrowid
	connection.commit()
	return msg_id

def connection_close():
	connection.close()

def mark_key_sent(msg_id, user_id):
	with connection.cursor() as cursor:
		sql = "UPDATE `message_queue` SET `subkey`=-1, `status`=1 WHERE `msg_id`=%s and `user_id`=%s"
		cursor.execute(sql, (int(msg_id), int(user_id)))
	connection.commit()

def mark_key_received(msg_id, user_id, subkey):
	with connection.cursor() as cursor:
		sql = "UPDATE `message_queue` SET `subkey`=%s, `status`=2 WHERE `msg_id`=%s and `user_id`=%s"
		cursor.execute(sql, (subkey, int(msg_id), int(user_id)))
	connection.commit()

def count_thres_num_users(msg_id):
	with connection.cursor() as cursor:
		sql = "SELECT * FROM `message_queue` WHERE `msg_id`=%s and `status`=2"
		result = cursor.execute(sql, (int(msg_id)))
	return result

def remove_from_message_queue(msg_id, user_id):
	with connection.cursor() as cursor:
		sql = "DELETE FROM `message_queue` WHERE `msg_id`=%s and `user_id`=%s"
		cursor.execute(sql, (int(msg_id), int(user_id)))
	connection.commit()

def count_num_users(msg_id):
	with connection.cursor() as cursor:
		sql = "SELECT * FROM `message_queue` WHERE `msg_id`=%s"
		result = cursor.execute(sql, (int(msg_id)))
	return result

