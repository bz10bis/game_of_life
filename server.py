import socket
import sys
import thread

HOST = ''
PORT = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("-- Socket created --")

try:
	server.bind((HOST, PORT))
except socket.error as msg:
	print("!! bind fail. Error Code: " + str(msg[0]))
	sys.exit()

print ("-- Socket bind completed")

server.listen(10)
print("-- Socket is listening")

def client_thread(conn):
	conn.send("Welcome to the server")
	while True:
		data = conn.recv(1024)
		reply = "Ok ..." + data
		if not data:
			break
		conn.sendall(reply)
	conn.close()

while 1:
	conn, addr = server.accept()
	print("Connection with " + addr[0] + ":" + str(addr[1]))
	thread.start_new_thread(client_thread,(conn, ))

server.close()