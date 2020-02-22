import socket

"""
2.0 版本，当用户访问服务器，返回指定页面，当页面不存在返回404
"""

BUFFSIZR = 4096


def request_handler(client_socket):
    """
    为每个用户进行服务
    :param client_socket:
    :return:
    """
    # 接收用户请求报文
    recv_data = client_socket.recv(BUFFSIZR)
    if not recv_data:
        print("客户连接已经断开")
        client_socket.close()
        return

    # 对请求报文进行切割
    request_str_data = recv_data.decode()
    data_list = request_str_data.split("\r\n")
    # 请求行在第0个元素
    request_line = data_list[0]
    print("请求行：", request_line)
    # 请求行中的第一个数据就是用户资源请求路径
    path_info = request_line.split(' ')[1]
    print("用户请求路径是%s" % path_info)

    if path_info == '/':
        path_info = '/grand.html'
    try:
        # 路径拼接
        file = open('./static' + path_info, 'rb')
        file_data = file.read()
        file.close()
    except Exception as e:
        # 用户请求路径失败了
        # 响应行
        response_line = "HTTP/1.1 404 Not Found\r\n"
        # 响应头
        response_header = "Server: PythonWebServer2.0\r\n"
        # 响应体
        response_body = "ERROR!!!!!"
        # 拼接报文
        response_data = response_line + response_header + "\r\n" + response_body
        # 发送
        client_socket.send(response_data.encode())
    else:
        # 给客户端回复HTTP响应报文：响应行 + 响应头 +空行 + 响应体
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_header = "Server: PythonWebServer1.0\r\n"
        # 响应体
        response_body = file_data
        # 拼接报文
        response_data = (response_line + response_header + "\r\n").encode() + response_body
        client_socket.send(response_data)
    finally:
        client_socket.close()


if __name__ == '__main__':
    # 创建一个服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 9999))
    server_socket.listen(128)
    while True:
        client_socket, client_addr = server_socket.accept()
        # 调用函数 对客户端进行服务
        request_handler(client_socket)
