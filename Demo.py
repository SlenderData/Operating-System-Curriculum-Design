# 参考学长的C++程序重新造的轮子，并不完善，有很多问题
# 可参考，但不建议使用

import math
import os
import platform
import time

mainflag = None  # 用于控制主菜单的循环
cpuflag = None  # 用于控制进程调度算法的选择
memoryflag = None  # 用于控制页面调度算法的选择
timeSlice = None  # 时间片长度
pageLength = None  # 单页面大小
pageFrameAmount = None  # 页面数
TIME = None  # 单位时间
process = None  # 进程对象列表
pageFrame = None  # 页面列表
avgTurnAroundTime = None  # 平均周转时间
avgWeightTurnAroundTime = None  # 平均带权周转时间


class pcb:
    def __init__(self, name, arraiveTime, priority, serveTime, serveTimeLeft, finishTime,
                 turnAroundTime, weightTunAroundTime, fc, runInfo):
        self.name = name  # 进程名
        self.arraiveTime = arraiveTime  # 创建时间
        self.priority = priority  # 优先级
        self.serveTime = serveTime  # 服务时间
        self.serveTimeLeft = serveTimeLeft  # 剩余所需服务时间
        self.finishTime = finishTime  # 完成时间
        self.turnAroundTime = turnAroundTime  # 周转时间
        self.weightTunAroundTime = weightTunAroundTime  # 带权周转时间
        self.fc = fc
        self.runInfo = runInfo

    class function:
        def __init__(self, name, lenth, abAddr):
            self.name = name  # 文件名
            self.lenth = lenth  # 大小
            self.abAddr = abAddr  # 绝对地址

    class run:
        def __init__(self, timeNode, operation, operationNode):
            self.timeNode = timeNode  # 时间节点
            self.operation = operation  # 操作名称
            self.operationNode = operationNode  # 操作节点


def create():
    global process, pageFrame, pageFrameAmount

    pageFrame = [None] * pageFrameAmount  # 初始化页面列表

    # 直接将三个txt文件的内容按格式硬编码为list对象
    process = []
    process.append(pcb('A进程', 0, 5, 100, 100, None, None, None, None, None))
    process.append(pcb('B进程', 1, 4, 31, 31, None, None, None, None, None))
    process.append(pcb('C进程', 3, 7, 37, 37, None, None, None, None, None))
    process.append(pcb('D进程', 6, 5, 34, 34, None, None, None, None, None))
    process.append(pcb('E进程', 8, 6, 39, 39, None, None, None, None, None))

    process[0].fc = []
    process[0].fc.append(pcb.function('main', 0.6, None))
    process[0].fc.append(pcb.function('A1', 1.2, None))
    process[0].fc.append(pcb.function('A2', 1.2, None))
    process[0].fc.append(pcb.function('A3', 1.5, None))
    process[0].fc.append(pcb.function('A4', 0.8, None))

    process[1].fc = []
    process[1].fc.append(pcb.function('main', 1.6, None))
    process[1].fc.append(pcb.function('B1', 2.2, None))
    process[1].fc.append(pcb.function('B2', 0.2, None))
    process[1].fc.append(pcb.function('B3', 0.5, None))
    process[1].fc.append(pcb.function('B4', 1.8, None))
    process[1].fc.append(pcb.function('B5', 0.9, None))

    process[2].fc = []
    process[2].fc.append(pcb.function('main', 0.3, None))
    process[2].fc.append(pcb.function('C1', 0.1, None))
    process[2].fc.append(pcb.function('C2', 0.3, None))
    process[2].fc.append(pcb.function('C3', 0.5, None))

    process[3].fc = []
    process[3].fc.append(pcb.function('main', 0.9, None))
    process[3].fc.append(pcb.function('D1', 1.6, None))
    process[3].fc.append(pcb.function('D2', 1.8, None))
    process[3].fc.append(pcb.function('D3', 2.0, None))
    process[3].fc.append(pcb.function('D4', 0.9, None))

    process[4].fc = []
    process[4].fc.append(pcb.function('main', 0.7, None))
    process[4].fc.append(pcb.function('E1', 0.3, None))
    process[4].fc.append(pcb.function('E2', 0.5, None))
    process[4].fc.append(pcb.function('E3', 0.9, None))
    process[4].fc.append(pcb.function('E4', 0.3, None))

    process[0].runInfo = []
    process[0].runInfo.append(pcb.run(5, '跳转', 1021))
    process[0].runInfo.append(pcb.run(10, '跳转', 2021))
    process[0].runInfo.append(pcb.run(20, '读写磁盘', 10))
    process[0].runInfo.append(pcb.run(30, '跳转', 2031))
    process[0].runInfo.append(pcb.run(70, '跳转', 4050))
    process[0].runInfo.append(pcb.run(100, '结束', 0))

    process[1].runInfo = []
    process[1].runInfo.append(pcb.run(3, '跳转', 2508))
    process[1].runInfo.append(pcb.run(10, '跳转', 6007))
    process[1].runInfo.append(pcb.run(15, '读写磁盘', 20))
    process[1].runInfo.append(pcb.run(22, '跳转', 5737))
    process[1].runInfo.append(pcb.run(27, '跳转', 2245))
    process[1].runInfo.append(pcb.run(31, '结束', 6311))

    process[2].runInfo = []
    process[2].runInfo.append(pcb.run(3, '跳转', 1074))
    process[2].runInfo.append(pcb.run(9, '跳转', 94))
    process[2].runInfo.append(pcb.run(15, '读写磁盘', 10))
    process[2].runInfo.append(pcb.run(22, '跳转', 70))
    process[2].runInfo.append(pcb.run(30, '跳转', 516))
    process[2].runInfo.append(pcb.run(37, '结束', 50))

    process[3].runInfo = []
    process[3].runInfo.append(pcb.run(3, '跳转', 1037))
    process[3].runInfo.append(pcb.run(10, '跳转', 782))
    process[3].runInfo.append(pcb.run(15, '读写磁盘', 4))
    process[3].runInfo.append(pcb.run(22, '跳转', 1168))
    process[3].runInfo.append(pcb.run(28, '跳转', 79))
    process[3].runInfo.append(pcb.run(34, '结束', 431))

    process[4].runInfo = []
    process[4].runInfo.append(pcb.run(3, '跳转', 1414))
    process[4].runInfo.append(pcb.run(11, '跳转', 1074))
    process[4].runInfo.append(pcb.run(16, '读写磁盘', 30))
    process[4].runInfo.append(pcb.run(24, '跳转', 149))
    process[4].runInfo.append(pcb.run(32, '跳转', 1273))
    process[4].runInfo.append(pcb.run(39, '结束', 2053))


# 显示进程信息
def showProcess():
    print("")
    if cpuflag == '1':
        print("先来先服务算法: ")
    elif cpuflag == '2':
        print("时间片轮转算法: ")
    print("进程名\t到达时间\t服务时间\t剩余所需服务时间\t完成时间\t周转时间\t带权周转时间")
    for p in process:
        print(p.name, '\t', p.arraiveTime, '\t', p.serveTime, '\t', p.serveTimeLeft, '\t', p.finishTime, '\t',
              p.turnAroundTime, '\t', p.weightTunAroundTime)


# 分页，计算每个文件的绝对地址
def pageDevide():
    global process
    for p in process:
        total = 0
        for f in p.fc:
            f.lenth = math.ceil(f.lenth * 1024)  # 将 KB 转换为 Byte，对不满 1B 的部分使用 math.ceil() 向上取整
            f.abAddr = total
            total += f.lenth


# 页面置换
def replacePage(n):
    global pageFrame
    # 将页面向后移动，为新页面腾出位置
    for i in range(pageFrameAmount - 1, 0, -1):
        pageFrame[i] = pageFrame[i - 1]
    # 将新页面放置在页面列表的首位
    pageFrame[0] = n


# 请求页面
def requirePage(addr):
    global pageFrame, memoryflag
    a = 0
    n = math.floor(addr / pageLength)  # 计算请求的页面号

    for i in range(pageFrameAmount):
        if pageFrame[i] == n:
            if memoryflag == '2':  # 如果使用LRU算法
                for j in range(i, 0, -1):
                    pageFrame[j] = pageFrame[j - 1]
                pageFrame[0] = n
            return n
        else:
            a += 1

    if a == pageFrameAmount:
        replacePage(n)
    return n


def fcfs():
    global TIME, process, avgTurnAroundTime, avgWeightTurnAroundTime
    create()
    TIME = 0
    pageDevide()
    process.sort(key=lambda p: p.arraiveTime)  # 按到达时间升序排列

    showProcess()
    for p in process:
        if TIME < p.arraiveTime:
            TIME = p.arraiveTime

        for j in range(len(p.fc)):
            k = 0
            while p.serveTimeLeft >= 0 and k < len(p.fc):
                if p.runInfo[k].timeNode == p.serveTime - p.serveTimeLeft:
                    requirePage(p.fc[k].abAddr)
                    showProcess()
                    print(
                        f"占用cpu的进程: {p.name} \t函数名: {p.fc[k].name} \t操作类型: {p.runInfo[k].operation} \t跳转目的地或I/O操作时间: {p.runInfo[k].operationNode}")
                    k += 1
                    time.sleep(1)  # 暂停1秒以帮助观察输出

                if p.serveTimeLeft == 0:
                    p.finishTime = TIME
                    p.turnAroundTime = p.finishTime - p.arraiveTime
                    p.weightTunAroundTime = p.turnAroundTime / p.serveTime
                    showProcess()
                    break

                p.serveTimeLeft -= 1
                TIME += 1

    avgTurnAroundTime = sum(p.turnAroundTime for p in process) / len(process)
    avgWeightTurnAroundTime = sum(p.weightTunAroundTime for p in process) / len(process)
    print("")
    print("平均周转时间：", avgTurnAroundTime, "\t平均带权周转时间：", avgWeightTurnAroundTime)


def rr():
    global TIME, process, timeSlice, avgTurnAroundTime, avgWeightTurnAroundTime
    create()
    TIME = 0
    pageDevide()
    process.sort(key=lambda p: p.arraiveTime)  # 按到达时间升序排列

    showProcess()
    process_queue = [p for p in process]  # 创建就绪队列
    while process_queue:
        p = process_queue.pop(0)  # 取出队列首部的进程
        if TIME < p.arraiveTime:
            TIME = p.arraiveTime

        time_allocated = min(p.serveTimeLeft, timeSlice)  # 分配的时间是剩余服务时间和时间片长度的最小值
        for _ in range(time_allocated):
            for k in range(len(p.fc)):
                if p.runInfo[k].timeNode == p.serveTime - p.serveTimeLeft:
                    requirePage(p.fc[k].abAddr)
                    showProcess()
                    print(
                        f"占用cpu的进程: {p.name} \t函数名: {p.fc[k].name} \t操作类型: {p.runInfo[k].operation} \t跳转目的地或I/O操作时间: {p.runInfo[k].operationNode}")
                    time.sleep(1)  # 暂停1秒以帮助观察输出

            p.serveTimeLeft -= 1
            TIME += 1

            if p.serveTimeLeft == 0:
                p.finishTime = TIME
                p.turnAroundTime = p.finishTime - p.arraiveTime
                p.weightTunAroundTime = p.turnAroundTime / p.serveTime
                showProcess()
                break

        if p.serveTimeLeft > 0:
            process_queue.append(p)  # 如果进程未完成，重新加入队列末尾

    avgTurnAroundTime = sum(p.turnAroundTime for p in process) / len(process)
    avgWeightTurnAroundTime = sum(p.weightTunAroundTime for p in process) / len(process)
    print("")
    print("平均周转时间：", avgTurnAroundTime, "\t平均带权周转时间：", avgWeightTurnAroundTime)


def writeResult():
    global process, avgTurnAroundTime, avgWeightTurnAroundTime
    # 检查文件是否存在且非空
    file_exists = os.path.isfile('result.txt') and os.path.getsize('result.txt') > 0

    with open('result.txt', 'a', encoding='utf-8') as file:
        # 如果文件已存在且非空，则在新内容前添加换行符
        if file_exists:
            file.write("\n")
            file.write("************************************************************\n")
            file.write("\n")

        # 假设每个中文字符占两个英文字符宽度
        header_format = "{:<6} {:<7} {:<7} {:<7} {:<7} {:<9}\n"
        data_format = "{:<7} {:<11} {:<11} {:<11} {:<11} {:<15}\n"

        header = header_format.format("进程名", "运行时间", "开始时间", "完成时间", "周转时间", "带权周转时间")
        file.write(header)

        for p in process:
            line = data_format.format(
                p.name, p.serveTime, p.arraiveTime, p.finishTime, p.turnAroundTime, p.weightTunAroundTime)
            file.write(line)

        file.write("\n平均周转时间: {:.5f}\n".format(avgTurnAroundTime))
        file.write("平均带权周转时间: {:.5f}\n".format(avgWeightTurnAroundTime))


def init():
    global cpuflag, timeSlice, memoryflag, pageLength, pageFrameAmount
    print("")
    print("**** 选择进程调度算法 ****")
    print("1: FCFS  先来先服务")
    print("2: RR    时间片轮转")
    cpuflag = input("请输入你的选择: ")

    if cpuflag == '2':
        print("")
        timeSlice = int(input("请输入时间片长度(单位ms): "))

    print("")
    print("**** 选择页面调度算法 ****")
    print("1: FIFO  先进先出")
    print("2: LRU   最近最少使用")
    memoryflag = input("请输入你的选择: ")

    print("")
    pageLength = input("请输入页面大小(单位KB): ")
    pageLength = math.ceil(float(pageLength) * 1024)  # 将 KB 转换为 Byte，对不满 1B 的部分使用 math.ceil() 向上取整

    print("")
    pageFrameAmount = int(input("请输入最大页框数: "))

    if cpuflag == '1':
        fcfs()
        writeResult()
    elif cpuflag == '2':
        rr()
        writeResult()


def main():
    global mainflag
    print("")
    print("")
    print("**************************************************************")
    print("*                 CPU & 内存调度管理原型系统                 *")
    print("*    CPU & Memory Scheduling Management Prototype System     *")
    print("**************************************************************")
    print("*                       **** Menu ****                       *")
    print("*                        1: 设置参数                         *")
    print("*                        0: 退出                             *")
    print("**************************************************************")
    mainflag = input("请输入你的选择: ")

    if mainflag == '1':
        init()
        main()
    elif mainflag == '0':
        if platform.system() == 'Windows':
            os.system("cls")  # 如果是 Windows 系统，使用 cls 清屏
        else:
            os.system("clear")  # 如果是 Linux/macOS 系统，使用 clear 清屏
        print("感谢使用！")
        print("")
        if platform.system() == 'Windows':
            # 如果是 Windows 系统，使用 type 命令显示文件内容
            # Windows 默认终端不支持 UTF-8 编码，如遇乱码请查找相关资料或换用其它终端解决
            os.system("type result.txt")
            print("")
        else:
            # 如果是 Linux/macOS 系统，使用 cat 命令显示文件内容
            os.system("cat result.txt")
            print("")


if __name__ == '__main__':
    main()
