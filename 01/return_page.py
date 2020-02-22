import socket

"""
1.0 当用户访问服务器，不管用户访问的是什么页面，都返回Helloworld

"""


def request_handler(client_socket):
    """
    为每个用户进行服务
    :param client_socket:
    :return:
    """
    recv_data = client_socket.recv(4096)
    if not recv_data:
        print("客户连接已经断开")
        client_socket.close()
        return
    print(recv_data)
    # 给客户端回复HTTP响应报文：响应行+响应头+空行+响应体

    # 响应行
    response_line = 'HTTP/1.1 200 OK\r\n'
    # 响应头
    response_header = "Server:PythonWebServer1.0\r\n"
    # 响应体
    response_body = "Hello World!!!"
    # 拼接报文
    response_data = response_line + response_header + "\r\n" + response_body
    # 发送
    client_socket.send(response_data.encode())
    # 关闭套接字
    client_socket.close()


if __name__ == '__main__':
    # 个服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定
    server_socket.bind(('', 9999))
    # 监听 被动套接字，设置已完成的三次握手队列的长度
    server_socket.listen(128)

    while True:
        # 从队列中取出一个客户套接字用以服务
        client_socket, client_addr = server_socket.accept()
        request_handler(client_socket)
