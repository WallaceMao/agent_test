import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex(("127.0.0.1", 8080))
print(result)