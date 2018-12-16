
from socket import *
import sys

if len(sys.argv) != 2:
    print("Please input: RemoteBet 127.0.0.1\n")
    sys.exit()

ip = sys.argv[1]
ip_port=(ip,9999)

# 封装协议（对象）
s = socket(AF_INET,SOCK_STREAM)

# 向服务端建立连接
s.connect(ip_port)

line = s.recv(1024)
print(line.decode())


while True:
    # 发送消息
    send_data=input('输入你压的值: ').strip()
    if len(send_data) == 0:continue  # 如果发送消息为空，不去执行以下发送
    s.send(bytes(send_data,encoding='utf8'))
    if send_data == 'exit': break  # 如果输入exit，则退出

    t = 0
    while t < 6:
        # 接收对方发送的消息
        recv_data = s.recv(2048)
        print("庄家:" + recv_data.decode('utf8'))
        t = t + 1
    break

# 结束连接
s.close()