import socket

# 创建一个套接字
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接web服务
tcp_socket.connect(('127.0.0.1', 80))

# 模拟浏览器发送http请求报文
request_data = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
tcp_socket.send(request_data.encode())

# 接收HTTP响应报文
recv_data = tcp_socket.recv(4096)

recv_str_data = recv_data.decode()
index = recv_str_data.find("\r\n\r\n")
print(recv_str_data[index + 4:])

tcp_socket.close()
