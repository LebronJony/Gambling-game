

from socket import *
from random import *
import time
import sys


ip_port = ('127.0.0.1',9999)

# 封装协议（对象)
s = socket(AF_INET, SOCK_STREAM)

# 绑定ip，端口
s.bind(ip_port)

# 启动监听
s.listen(5)  # 挂起连接数，  允许最多处理5个请求

point = [
    "│   │\n"
    "│ ● │\n"
    "│   │",
    "│ ● │\n"
    "│   │\n"
    "│ ● │",
    "│●  │\n"
    "│ ● │\n"
    "│  ●│",
    "│● ●│\n"
    "│   │\n"
    "│● ●│",
    "│● ●│\n"
    "│ ● │\n"
    "│● ●│",
    "│● ●│\n"
    "│● ●│\n"
    "│● ●│"
]

def touzi(i):
    return("┌───┐\n" + point[i-1]+'\n'+ "└───┘\n")

gamble = {
    "tc":"头彩",
    "dc":"大彩",
    "qx":"七星",
    "dd":"单对",
    "sx":"散星",
    "kp":"空盘"
}
stake = {
    1:"一",
    2:"二",
    3:"三",
    4:"四",
    5:"五",
    6:"六",
    7:"七",
    8:"八",
    9:"九",
    10:"十",
    11:"十一点",
    12:"十二点"
}
gamble2 = {
    "tc":35,
    "dc":17,
    "qx":5,
    "dd":3,
    "sx":2,
    "kp":5
}
money = {
    "coin":"铜币",
    "silver":"银币",
    "gold":"金币"
}

while True:
    # 等待连接
    conn, addr = s.accept()  # accept方法等待客户端连接，直到有客户端连接后，会返回连接线（conn）、连接地址（addr）

    print("玩家:", addr, "进入游戏\n")

    conn.send('''规则如下：
    ya tc <数量> <coin|silver|gold> 押头彩(两数顺序及点数均正确)       一赔三十五
    ya dc <数量> <coin|silver|gold> 押大彩(两数点数正确)               一赔十七
    ya kp <数量> <coin|silver|gold> 押空盘(两数不同且均为偶数)         一赔五
    ya qx <数量> <coin|silver|gold> 押七星(两数之和为七)               一赔五
    ya dd <数量> <coin|silver|gold> 押单对(两数均为奇数)               一赔三
    ya sx <数量> <coin|silver|gold> 押散星(两数之和为三、五、九、十一)   一赔二
    每盘按从上到下的顺序只出现一种点型(头彩和大彩可同时出现)，其他情况都算庄家赢。
    输入exit退出。
    	'''.encode())


    while True:

        q1 = randint(1,6)
        q2 = randint(1,6)
        touzi1 = str(touzi(q1))
        touzi2 = str(touzi(q2))
        total = touzi1 + touzi2
        data = "庄家唱道:新开盘！预叫头彩\n" + "庄家将两枚玉骰往银盘中一撒\n" + touzi1 + touzi2
        conn.sendall(data.encode('utf8'))
        time.sleep(2)

        # 接收消息
        recv_data=conn.recv(1024)  # 接收conn连接线路，并指定缓存该线路的1024
        if len(recv_data)  > 0:
            r = recv_data.decode('utf8')
        x = r.split(' ')
        mes1 = x[1]  # 押什么
        mes2 = x[2]  # 押多少枚
        mes3 = x[3]  # 什么币
        if not recv_data:
            break

        print("你押" + gamble[mes1] + mes2 + '枚' + money[mes3])
        send_data = "您押"+gamble[mes1]+mes2+'枚'+money[mes3]+'\n'
        conn.sendall(send_data.encode('utf8'))

        t1 = randint(1,6)
        t2 = randint(1,6)

        Sum = t1 + t2
        data1 = "将左手的金盅倒扣在银盘上，玉骰滚了出来\n" + str(touzi(t1))
        send_data = data1.encode('utf8')
        conn.sendall(send_data)

        data2 = "将右手的金盅倒扣在银盘上，玉骰滚了出来\n" + str(touzi(t2))
        send_data = data2.encode('utf8')
        conn.sendall(send_data)

        time.sleep(2)
        data3 = "庄家唱道:"+str(stake[t1])+'、'+str(stake[t2])+"······"+str(stake[Sum])
        send_data = data3.encode('utf8')
        conn.sendall(send_data)

        if (mes1 == "tc"):
            if t1 == q1 and t2 == q2:
                print("你赢到" + gamble["tc"] + '得' + str(int(mes2) * 35) + '枚' + mes3)
                pr = "你赢到" + gamble["tc"] + '得' + str(int(mes2) * 35) + '枚' + str(money[mes3])

            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"


        elif mes1 == "dc":
            if ((t1 == q1 and q2 == t2) or (q1 == t2 and q2 == t1)):
                print("你赢到" + gamble["dc"] + '得' + str(int(mes2) * 17) + '枚' + str(money[mes3]))
                pr = "你赢到" + gamble["dc"] + '得' + str(int(mes2) * 17) + '枚' + str(money[mes3])
            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"


        elif mes1 == "kp":
            if ((t1 != t2) and (t1 % 2 == 0) and (t2 % 2 == 0)):
                print("你赢到" + gamble["qx"] + '得' + str(int(mes2) * 5) + '枚' + str(money[mes3]))
                pr = "你赢到" + gamble["qx"] + '得' + str(int(mes2) * 5) + '枚' + str(money[mes3])

            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"

        elif (mes1 == "qx"):
            if (t1 + t2 == 7):
                print("你赢到" + gamble["qx"] + '得' + str(int(mes2) * 5) + '枚' + str(money[mes3]))
                pr = "你赢到" + gamble["qx"] + '得' + str(int(mes2) * 5) + '枚' + str(money[mes3])

            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"

        elif (mes1 == "dd"):
            if ((t1 % 2 != 0) and (t2 % 2 != 0)):
                print("你赢到" + gamble["dd"] + '得' + str(int(mes2) * 3) + '枚' + str(money[mes3]))
                pr = "你赢到" + gamble["qx"] + '得' + str(int(mes2) * 3) + '枚' + str(money[mes3])

            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"

        elif (mes1 == "sx"):
            if (Sum == 3 or Sum == 5 or Sum == 9 or Sum == 11):
                print("你赢到" + gamble["sx"] + '得' + str(int(mes2) * 2) + '枚' + str(money[mes3]))
                pr = "你赢到" + gamble["sx"] + '得' + str(int(mes2) * 2) + '枚' + str(money[mes3])

            else:
                print("本次赚" + mes2 + '枚' + str(money[mes3]) + '\n')
                pr = "庄家赢!"

        send_data = pr.encode('utf8')
        conn.sendall(send_data)
        pr = "GAME OVER!"
        send_data = pr.encode('utf8')
        conn.sendall(send_data)
        break

    conn.close()