import socket
import multiprocessing

"""
4.0 使用面向对象开发
"""

HOST = ''
PORT = 9999
ADDR = (HOST, PORT)
BUFFSIZE = 4096


class HTTPServer(object):
    def __init__(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(ADDR)
        server_socket.listen(128)

        self.server_socket = server_socket

    def request_handler(self, client_socket):
        """
        为每个客户服务
        :param client_socket:
        :return:
        """
        recv_data = client_socket.recv(BUFFSIZE)
        if not recv_data:
            print("客户端已经断开连接")
            client_socket.close()
            return
        recv_str_data = recv_data.decode()
        data_list = recv_str_data.split("\r\n")
        request_line = data_list[0]
        print(data_list)
        # 请求行的第一个数据就是用户的资源请求路径
        path_info = request_line.split(' ')[1]
        print("用户请求路径是%s" % path_info)
        if path_info == '/':
            path_info = '/grand.html'
        try:
            # ./static  + /index.html
            file = open("./static" + path_info, "rb")
            file_data = file.read()  # 如果文件过大 容易崩溃
            file.close()
        except Exception as e:
            # 用户请求路径是失败了
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

            # 响应行
            response_line = "HTTP/1.1 200 OK\r\n"

            # 响应头
            response_header = "Server: PythonWebServer1.0\r\n"

            # 响应体
            response_body = file_data

            # 拼接报文
            response_data = (response_line + response_header + "\r\n").encode() + response_body

            # 发送
            client_socket.send(response_data)
        finally:
            # 关闭套接字
            client_socket.close()

    def start(self):
        while True:
            # 从队列中取出一个客户套接字
            client_socket, client_addr = self.server_socket.accept()
            pro=multiprocessing.Process(target=self.request_handler,args=(client_socket,))
            pro.start()
            client_socket.close()

if __name__ == '__main__':
    http_server = HTTPServer()
    http_server.start()
