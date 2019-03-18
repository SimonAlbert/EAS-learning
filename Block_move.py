import pygame as pg
import time
import numpy as np

s0 = 2
s1 = 4
# s2 = 4


class player:
    def __init__(self):
        # 输入4个数，分别表示当前位置坐标、目标位置坐标
        # 输出4个数，最大的表示移动方向
        # 每次选取离目标最近的（距离最小的，Δx+Δy最小即可）
        # 输入p_x,p_y,t_x,t_y
        self.weight1 = np.random.uniform(-5, 5, [s0, s1])
        # self.weight2 = np.random.uniform(-5, 5, [s1, s2])
        self.bias1 = np.random.uniform(-5, 5, s1)
        # self.bias2 = np.random.uniform(-5, -5, s2)

    def play(self):
        t_x = np.random.randint(0, 15)
        t_y = np.random.randint(0, 11)
        P = player()
        # P = gameplay(self.weight1, self.bias1, self.weight2, self.bias2, t_x, t_y)
        P = gameplay(self.weight1, self.bias1, t_x, t_y)
        self.weight1 = P.weight1
        # self.weight2 = P.weight2
        self.bias1 = P.bias1
        # self.bias2 = P.bias2

    def game(self):
        t_x = np.random.randint(0, 15)
        t_y = np.random.randint(0, 11)
        # game(self.weight1, self.bias1, self.weight2, self.bias2, t_x, t_y)
        game(self.weight1, self.bias1, t_x, t_y)

    def save(self):
        np.save("weight1.npy", self.weight1)
        # np.save("weight2.npy", self.weight2)
        np.save("bias1.npy", self.bias1)
        # np.save("bias2.npy", self.bias2)

    def read(self):
        self.weight1 = np.load("weight1.npy")
        # self.weight2 = np.load("weight2.npy")
        self.bias1 = np.load("bias1.npy")
        # self.bias2 = np.load("bias2.npy")
# 更新方案，更新一次产生十组差异，优胜劣汰


def game(weight1, bias1, t_x, t_y):
# def game(weight1, bias1, weight2, bias2, t_x, t_y):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("贪吃蛇")

    p_x = np.random.randint(0, 15)
    p_y = np.random.randint(0, 11)
    block_szie = [50, 50]
    velocity = [0, 50]
    color = 255, 255, 0
    target_color = 255, 0, 0
    # 生成目标
    step = 0
    while True:
        # 超过26步退出，两个方块接触退出
        if step > 26:
            pg.quit()
            print("无法通过测试")
            return
        if p_x == t_x and p_y == t_y:
            pg.quit()
            return
        step += 1

        # 神经网络决策
        l = abs(p_x - t_x) + abs(p_y - t_y)

        a1 = np.matmul([p_x-t_x, p_y-t_y], weight1) + bias1
        # a2 = np.matmul(a1, weight2) + bias2
        # op = a2.tolist().index(a2.max())
        op = a1.tolist().index(a1.max())
        # 根据最大值决定移动方向
        if op == 0:
            velocity = [0, -1]
        elif op == 1:
            velocity = [0, 1]
        elif op == 2:
            velocity = [-1, 0]
        elif op == 3:
            velocity = [1, 0]
        p_x += velocity[0]
        p_y += velocity[1]

        if p_x >= 800 or p_x < 0:
            p_x -= velocity[0]
        if p_y >= 600 or p_y < 0:
            p_y -= velocity[1]
        pos = [p_x*50, p_y*50] + block_szie
        screen.fill((0, 0, 200))
        pg.draw.rect(screen, color, pos, 0)
        pg.draw.rect(screen, target_color, [t_x * 50, t_y * 50, block_szie[0], block_szie[1]], 0)
        pg.display.update()
        time.sleep(0.2)
        print('p:', p_x, ',', p_y)
        print('t:', t_x, ',', t_y)


def gameplay(weight1, bias1, t_x, t_y):
# def gameplay(weight1, bias1, weight2, bias2, t_x, t_y):

    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("贪吃蛇")

    p_x = np.random.randint(0, 15)
    p_y = np.random.randint(0, 11)
    block_szie = [50, 50]
    velocity = [0, 50]
    color = 255, 255, 0
    # 生成目标
    score = 0
    step = 0
    P = player()

    P.weight1 = weight1
    # P.weight2 = weight2
    P.bias1 = bias1
    # P.bias2 = bias2
    rate = 0.05
    while True:
        # 超过26步退出，两个方块接触退出

        if p_x == t_x and p_y == t_y:
            pg.quit()
            P.weight1 = weight1
            # P.weight2 = weight2
            P.bias1 = bias1
            # P.bias2 = bias2
            pg.quit()
            return P
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         pg.quit()
        #         return P
                # exit()
        step += 1
        # 键盘操作
        # elif event.type == pg.KEYDOWN:
        #     if event.key == pg.K_w:
        #         velocity = [0, -50]
        #     elif event.key == pg.K_s:
        #         velocity = [0, 50]
        #     elif event.key == pg.K_a:
        #         velocity = [-50, 0]
        #     elif event.key == pg.K_d:
        #         velocity = [50, 0]

        # 神经网络决策
        l = abs(p_x-t_x)+abs(p_y-t_y)
        havetry = True
        wm1 = rate * np.random.uniform(-1, 1, [10, s0, s1]) + weight1
        bm1 = rate * np.random.uniform(-1, 1, [10, s1]) + bias1
        # 第二层
        # wm2 = rate * np.random.uniform(-1, 1, [10, s1, s2]) + weight2
        # bm2 = rate * np.random.uniform(-1, 1, [10, s2]) + bias2
        wm1[0] = weight1
        bm1[0] = bias1
        # wm2[0] = weight2
        # bm2[0] = bias2
        ptx = 0
        pty = 0
        r = 0.02
        while havetry:
            wm1 = r*np.random.uniform(-1, 1, [10, s0, s1]) + wm1
            bm1 = r*np.random.uniform(-1, 1, [10, s1]) + bm1
            # 第二层
            # wm2 = r*np.random.uniform(-1, 1, [10, s1, s2]) + wm2
            # bm2 = r*np.random.uniform(-1, 1, [10, s2]) + bm2
            r += 0.005
            a = np.empty(10)
            a1 = np.empty([10, s1])
            # a2 = np.empty([10, s2])
            op = np.empty(10)
            for i in range(10):
                a1[i] = np.matmul([p_x-t_x, p_y-t_y], wm1[i]) + bm1[i]
                # a2[i] = np.matmul(a1[i], wm2[i]) + bm2[i]
                # op[i] = a2[i].tolist().index(a2[i].max())
                op[i] = a1[i].tolist().index(a1[i].max())
            # a1 = np.matmul([p_x, p_y, t_x, t_y], weight1) + bias1
            # a2 = np.matmul(a1, weight2) + bias2
            # op = a2.tolist().index(a2.max())
            # 根据最大值决定移动方向
            ptx = 0
            pty = 0
            for i in range(10):
                ptx = p_x
                pty = p_y
                if op[i] == 0:
                    velocity = [0, -1]
                elif op[i] == 1:
                    velocity = [0, 1]
                elif op[i] == 2:
                    velocity = [-1, 0]
                elif op[i] == 3:
                    velocity = [1, 0]
                ptx += velocity[0]
                pty += velocity[1]
                l2 = abs(ptx-t_x)+abs(pty-t_y)
                if l2 < l:
                    weight1 = wm1[i]
                    # weight2 = wm2[i]
                    bias1 = bm1[i]
                    # bias2 = bm2[i]
                    havetry = False
                    break
        p_x = ptx
        p_y = pty

        if p_x >= 800 or p_x < 0:
            p_x -= velocity[0]
        if p_y >= 600 or p_y < 0:
            p_y -= velocity[1]
        pos = [p_x*50, p_y*50] + block_szie
        screen.fill((0, 0, 200))
        pg.draw.rect(screen, color, pos, 0)
        pg.draw.rect(screen, color, [t_x*50, t_y*50, block_szie[0], block_szie[1]], 0)
        pg.display.update()
        # time.sleep(0.1)
        print('p:', p_x, ',', p_y)
        print('t:', t_x, ',', t_y)
        if step >= 100:
            P.weight1 = weight1
            # P.weight2 = weight2
            P.bias1 = bias1
            # P.bias2 = bias2
            print("本次变异没有产生有价值的后代")
            choice = input("是否进行更激进的变异？Y/N")
            if choice == 'Y' or choice == 'y':
                rate = 5
                step = 0
            elif choice == 'N' or choice == 'n':
                rate = int(input("输入新的rate"))
                step = 0
                # return P
            else:
                print("调皮")


def main():
    P1 = player()
    # P1.read()
    str = ''
    while str != '0':
        str = input("1.evolve\n3.test\n4.save\n5.read\n6.show_net\n7.训练\n8.测试\n0.exit")
        if str == '1':
            P1.play()
        elif str == '3':
            P1.game()
        elif str == '4':
            P1.save()
        elif str == '5':
            P1.read()
        elif str == '6':
            print(P1.weight1)
        elif str == '7':
            t = int(input("训练次数"))
            for i in range(t):
                P1.play()
        elif str == '8':
            t = int(input("测试次数"))
            for i in range(t):
                P1.game()


if __name__ == '__main__':
    main()

