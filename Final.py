# 本代码有是在 Demo.py 的基础上进行修改得到的大屎山，有很多不够精简的地方，冗余的代码也很多
# 但是由于临近 DDL，无法进行重构，故将其作为最终版本提交

import math
import os
import platform
import time

mainflag = None  # 用于控制主菜单的循环
cpuflag = None  # 用于控制进程调度算法的选择
memoryflag = None  # 用于控制页面调度算法的选择
timeSlice = None  # 时间片长度
pageLength = None  # 单页面大小
TIME = None  # 单位时间
process = None  # 进程对象列表
pageFrameAmount = None  # 页面数
ioQueue = None  # I/O请求队列
readyQueue = None  # 就绪队列
avgTurnAroundTime = None  # 平均周转时间
avgWeightTurnAroundTime = None  # 平均带权周转时间
running_process = None  # 当前运行的进程


class pcb:
    def __init__(self, name, status, arraiveTime, priority, pageFrame, pageFaultCount, serveTime, serveTimeLeft,
                 finishTime, turnAroundTime, weightTunAroundTime, fc, runInfo, iostart, iofinish, currentAddr):
        self.name = name  # 进程名
        self.status = status  # 进程状态
        self.arraiveTime = arraiveTime  # 创建时间
        self.priority = priority  # 优先级
        self.pageFrame = pageFrame  # 页面列表
        self.pageFaultCount = pageFaultCount  # 缺页次数
        self.serveTime = serveTime  # 服务时间
        self.serveTimeLeft = serveTimeLeft  # 剩余所需服务时间
        self.finishTime = finishTime  # 完成时间
        self.turnAroundTime = turnAroundTime  # 周转时间
        self.weightTunAroundTime = weightTunAroundTime  # 带权周转时间
        self.fc = fc
        self.runInfo = runInfo
        self.iostart = iostart  # I/O开始时间
        self.iofinish = iofinish  # I/O结束时间
        self.currentAddr = currentAddr  # 当前操作地址

    class function:
        def __init__(self, name, lenth, rtAddr):
            self.name = name  # 文件名
            self.lenth = lenth  # 大小
            self.rtAddr = rtAddr  # 相对地址

    class run:
        def __init__(self, timeNode, operation, operateAddr, ioTime, finishflag):
            self.timeNode = timeNode  # 时间节点
            self.operation = operation  # 操作名称
            self.operateAddr = operateAddr  # 操作地址
            self.ioTime = ioTime  # I/O操作时间
            self.finishflag = finishflag  # 结束标志


def create():
    global process, pageFrameAmount

    # 直接将三个txt文件的内容按格式硬编码为list对象
    process = []
    process.append(pcb('A进程', '就绪', 0, 5, None, 0, 100, 100, None, None, None, None, None, None, None, 0))
    process.append(pcb('B进程', '就绪', 1, 4, None, 0, 31, 31, None, None, None, None, None, None, None, 0))
    process.append(pcb('C进程', '就绪', 3, 7, None, 0, 37, 37, None, None, None, None, None, None, None, 0))
    process.append(pcb('D进程', '就绪', 6, 5, None, 0, 34, 34, None, None, None, None, None, None, None, 0))
    process.append(pcb('E进程', '就绪', 8, 6, None, 0, 39, 39, None, None, None, None, None, None, None, 0))

    for p in process:
        p.pageFrame = []
        for i in range(pageFrameAmount[process.index(p)]):
            p.pageFrame.append(None)

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

    for p in process:
        total = 0
        for f in p.fc:
            f.lenth = math.ceil(f.lenth * 1024)  # 将 KB 转换为 Byte，对不满 1B 的部分使用 math.ceil() 向上取整
            f.rtAddr = total
            total += f.lenth
        p.totalsize = total

    process[0].runInfo = []
    process[0].runInfo.append(pcb.run(5, '跳转', 1021, None, False))
    process[0].runInfo.append(pcb.run(10, '跳转', 2021, None, False))
    process[0].runInfo.append(pcb.run(20, '读写磁盘', None, 10, False))
    process[0].runInfo.append(pcb.run(30, '跳转', 2031, None, False))
    process[0].runInfo.append(pcb.run(70, '跳转', 4050, None, False))
    process[0].runInfo.append(pcb.run(100, '结束', None, None, False))

    process[1].runInfo = []
    process[1].runInfo.append(pcb.run(3, '跳转', 2508, None, False))
    process[1].runInfo.append(pcb.run(10, '跳转', 6007, None, False))
    process[1].runInfo.append(pcb.run(15, '读写磁盘', None, 20, False))
    process[1].runInfo.append(pcb.run(22, '跳转', 5737, None, False))
    process[1].runInfo.append(pcb.run(27, '跳转', 2245, None, False))
    process[1].runInfo.append(pcb.run(31, '结束', 6311, None, False))

    process[2].runInfo = []
    process[2].runInfo.append(pcb.run(3, '跳转', 1074, None, False))
    process[2].runInfo.append(pcb.run(9, '跳转', 94, None, False))
    process[2].runInfo.append(pcb.run(15, '读写磁盘', None, 10, False))
    process[2].runInfo.append(pcb.run(22, '跳转', 70, None, False))
    process[2].runInfo.append(pcb.run(30, '跳转', 516, None, False))
    process[2].runInfo.append(pcb.run(37, '结束', 50, None, False))

    process[3].runInfo = []
    process[3].runInfo.append(pcb.run(3, '跳转', 1037, None, False))
    process[3].runInfo.append(pcb.run(10, '跳转', 782, None, False))
    process[3].runInfo.append(pcb.run(15, '读写磁盘', None, 4, False))
    process[3].runInfo.append(pcb.run(22, '跳转', 1168, None, False))
    process[3].runInfo.append(pcb.run(28, '跳转', 79, None, False))
    process[3].runInfo.append(pcb.run(34, '结束', 431, None, False))

    process[4].runInfo = []
    process[4].runInfo.append(pcb.run(3, '跳转', 1414, None, False))
    process[4].runInfo.append(pcb.run(11, '跳转', 1074, None, False))
    process[4].runInfo.append(pcb.run(16, '读写磁盘', None, 30, False))
    process[4].runInfo.append(pcb.run(24, '跳转', 149, None, False))
    process[4].runInfo.append(pcb.run(32, '跳转', 1273, None, False))
    process[4].runInfo.append(pcb.run(39, '结束', 2053, None, False))

    readyList = []


# 显示进程信息
def showProcess():
    print("***************************************************************************")
    print("进程名\t进程状态\t到达时间\t服务时间\t剩余所需服务时间\t完成时间\t周转时间\t带权周转时间")
    for p in process:
        print(p.name, '\t', p.status, '\t', p.arraiveTime, '\t', p.serveTime, '\t', p.serveTimeLeft, '\t', p.finishTime,
              '\t',
              p.turnAroundTime, '\t', p.weightTunAroundTime)
    print("当前各进程页面分配情况: ")
    for p in process:
        print(p.name, ":", p.pageFrame)
    print("***************************************************************************")


# 显示当前就绪队列
def showReadyQueue(readyQueue):
    show = []
    for p in readyQueue:
        show.append(p.name)
    print("当前就绪进程队列: ", show)


# 页面置换
def replacePage(n, index):
    global process
    print("将页面向后移动，为新页面腾出位置")
    if process[index].pageFrame[pageFrameAmount[index] - 1] is not None:
        print("页面列表已满，将页面 ", process[index].pageFrame[pageFrameAmount[index] - 1], " 移出内存")
    # 将页面向后移动，为新页面腾出位置
    for i in range(pageFrameAmount[index] - 1, 0, -1):
        process[index].pageFrame[i] = process[index].pageFrame[i - 1]
    # 将新页面放置在页面列表的首位
    process[index].pageFrame[0] = n


# 请求页面
def requirePage(addr, index):
    global process, memoryflag
    a = 0  # 帮助检查请求页面是否已在页面列表中的计数器
    n = math.floor(addr / pageLength)  # 计算请求的页面号
    print(process[index].name, " 请求了页面: ", n)

    for i in range(pageFrameAmount[index]):
        if process[index].pageFrame[i] == n:
            print("页面已在页面列表中")
            if memoryflag == '2':  # 如果使用LRU算法
                print("正在使用 LRU 算法，其余页面向后移动，将请求的页面置于页面列表的首位")
                # 将页面向后移动，将请求的页面置于页面列表的首位
                for j in range(i, 0, -1):
                    process[index].pageFrame[j] = process[index].pageFrame[j - 1]
                process[index].pageFrame[0] = n
            return n
        else:
            a += 1

    if a == pageFrameAmount[index]:
        process[index].pageFaultCount += 1
        print("页面不在列表中，", process[index].name, "发生了第", process[index].pageFaultCount, "次缺页中断")
        replacePage(n, index)

    return n


def fcfs():
    global process, TIME, ioQueue, readyQueue, avgTurnAroundTime, avgWeightTurnAroundTime, running_process

    create()  # 初始化进程
    print("初始化进程完成")
    showProcess()

    TIME = 0
    print("")
    print("* ", "当前时间: ", TIME, " *")
    time.sleep(0.1)
    ioQueue = []
    readyQueue = [p for p in process if p.arraiveTime <= TIME]
    print("进程 ", readyQueue[0].name, " 到达，变为就绪态")
    showReadyQueue(readyQueue)

    running_process = None  # 添加一个变量来追踪当前运行的进程

    while readyQueue or ioQueue or running_process:
        if running_process and running_process.serveTimeLeft == 0:
            # 如果当前运行的进程已经完成
            finish_process(running_process)
            running_process = None

            # 如果所有进程都已经完成
            if not (readyQueue or ioQueue):
                # 计算平均周转时间和带权周转时间
                calculate_averages()
                break

        check_io_queue()  # 检查IO队列中是否有完成IO的进程

        if not running_process and readyQueue:
            # 如果没有进程在运行，并且就绪队列不为空
            running_process = readyQueue.pop(0)
            start_process(running_process)
            showReadyQueue(readyQueue)

        # 运行当前进程一个时间单位
        TIME += 1
        if running_process:
            running_process.serveTimeLeft -= 1
        print("\n* ", "当前时间: ", TIME, " *")
        time.sleep(0.1)

        check_arriving_processes()  # 检查新到达的进程

        if running_process:
            if running_process.serveTimeLeft > 0:
                check_page_jump(running_process)  # 检查页面跳转
                if check_io_request(running_process):
                    # 如果有 IO 请求发生
                    running_process = None  # 暂停当前进程


def check_page_jump(proc):
    for r in proc.runInfo:
        if r.timeNode == proc.serveTime - proc.serveTimeLeft:
            if r.operation == '跳转':
                # 处理页面跳转
                requirePage(r.operateAddr, process.index(proc))
                showProcess()
                # 遍历proc.fc，找到当前地址对应的函数名
                for f in proc.fc:
                    if f.rtAddr > proc.currentAddr:
                        break
                    currentFunctionName = f.name
                # 遍历proc.fc，找到目标地址对应的函数名
                for f in proc.fc:
                    if f.rtAddr > r.operateAddr:
                        break
                    targetFunctionName = f.name
                # 更新进程的当前地址
                proc.currentAddr = r.operateAddr
                print("占用cpu的进程: ", proc.name, "\t函数名: ", currentFunctionName,
                      "\t操作类型: ", r.operation, "\t操作地址: ", r.operateAddr, "\t目标函数名: ",
                      targetFunctionName)


def finish_process(proc):
    proc.status = '完成'
    print(f"进程 {proc.name} 完成")
    proc.finishTime = TIME
    proc.turnAroundTime = TIME - proc.arraiveTime
    proc.weightTunAroundTime = proc.turnAroundTime / proc.serveTime
    showProcess()


def check_io_queue():
    global TIME, running_process
    for p in list(ioQueue):
        if p.iofinish == TIME:
            print(f"进程 {p.name} I/O 完成，变为就绪态，放入就绪队列首部")
            p.status = '就绪'
            readyQueue.insert(0, p)
            showReadyQueue(readyQueue)
            ioQueue.remove(p)

            if running_process:
                # 如果当前有进程在运行，将其移回就绪队列
                print(f"暂停当前运行的进程 {running_process.name}，将其放在绪队列刚完成 I/O 的进程后面")
                running_process.status = '就绪'
                readyQueue.insert(1, running_process)
                showReadyQueue(readyQueue)

            running_process = readyQueue.pop(0)  # 将刚完成 I/O 的进程移出就绪队列
            print("刚完成 I/O 的进程 ", p.name, " 开始运行，进入CPU，移出就绪队列")
            showReadyQueue(readyQueue)
            return True
            break
    return False


def start_process(proc):
    print(f"进程 {proc.name} 开始运行，进入CPU，移出就绪队列")
    proc.status = '运行'


def check_arriving_processes():
    for p in list(filter(lambda x: x.arraiveTime == TIME, process)):
        if p not in readyQueue and p not in ioQueue:
            p.status = '就绪'
            readyQueue.append(p)
            print("进程 ", p.name, " 到达，变为就绪态")
            showReadyQueue(readyQueue)


def check_io_request(proc):
    for r in proc.runInfo:
        if r.timeNode == proc.serveTime - proc.serveTimeLeft:
            if r.operation == '读写磁盘':
                # 处理 I/O 请求
                # 遍历proc.fc，找到当前地址对应的函数名
                for f in proc.fc:
                    if f.rtAddr > proc.currentAddr:
                        break
                    currentFunctionName = f.name
                proc.status = '等待'
                print("占用cpu的进程: ", proc.name, "\t函数名: ", currentFunctionName,
                      "\t操作类型: ", r.operation, "\tI/O操作时间: ", r.ioTime)
                showProcess()
                proc.iostart = TIME
                proc.iofinish = TIME + r.ioTime
                ioQueue.append(proc)
                return True
    return False


def calculate_averages():
    global avgTurnAroundTime, avgWeightTurnAroundTime
    avgTurnAroundTime = sum(p.turnAroundTime for p in process if p.status == '完成') / len(process)
    avgWeightTurnAroundTime = sum(p.weightTunAroundTime for p in process if p.status == '完成') / len(process)
    print("\n平均周转时间：", avgTurnAroundTime, "\t平均带权周转时间：", avgWeightTurnAroundTime)


def rr():
    global process, TIME, ioQueue, readyQueue, avgTurnAroundTime, avgWeightTurnAroundTime, timeSlice

    create()  # 初始化进程
    print("初始化进程完成")
    showProcess()

    # 初始化时间和队列
    TIME = 0
    print("")
    print("* ", "当前时间: ", TIME, " *")
    time.sleep(0.1)
    ioQueue = []
    readyQueue = [p for p in process if p.arraiveTime <= TIME]  # 将到达时间小于等于当前时间的进程加入就绪队列
    print("进程 ", readyQueue[0].name, " 到达，变为就绪态")
    showReadyQueue(readyQueue)

    while readyQueue or ioQueue:
        # 处理就绪队列
        if readyQueue:
            current_process = readyQueue.pop(0)
            print(f"进程 {current_process.name} 开始运行，进入CPU，移出就绪队列")
            showReadyQueue(readyQueue)
            current_process.status = '运行'
            time_spent = 0

            # 执行时间片
            while time_spent < timeSlice and current_process.serveTimeLeft > 0:
                TIME += 1
                time_spent += 1
                current_process.serveTimeLeft -= 1
                print("")
                print("* ", "当前时间: ", TIME, " *")
                time.sleep(0.1)

                # 将新到达的进程添加到就绪队列
                for p in list(filter(lambda x: x.arraiveTime == TIME, process)):
                    if p not in readyQueue and p not in ioQueue:
                        p.status = '就绪'
                        readyQueue.append(p)
                        print("进程 ", p.name, " 到达，变为就绪态")
                        showReadyQueue(readyQueue)

                # 检查并处理I/O请求
                for r in current_process.runInfo:
                    if r.timeNode == current_process.serveTime - current_process.serveTimeLeft:
                        # 处理跳转和I/O请求
                        if r.operation == '跳转':
                            requirePage(r.operateAddr, process.index(current_process))
                            showProcess()
                            # 遍历current_process.fc，找到当前地址对应的函数名
                            for f in current_process.fc:
                                if f.rtAddr > current_process.currentAddr:
                                    break
                                currentFunctionName = f.name
                            # 遍历current_process.fc，找到目标地址对应的函数名
                            for f in current_process.fc:
                                if f.rtAddr > r.operateAddr:
                                    break
                                targetFunctionName = f.name
                            current_process.currentAddr = r.operateAddr
                            print("占用cpu的进程: ", current_process.name, "\t函数名: ", currentFunctionName,
                                  "\t操作类型: ", r.operation, "\t操作地址: ", r.operateAddr, "\t目标函数名: ",
                                  targetFunctionName)
                        elif r.operation == '读写磁盘':
                            # 遍历current_process.fc，找到当前地址对应的函数名
                            for f in current_process.fc:
                                if f.rtAddr > current_process.currentAddr:
                                    break
                                currentFunctionName = f.name
                            current_process.status = '等待'
                            print("占用cpu的进程: ", current_process.name, "\t函数名: ", currentFunctionName,
                                  "\t操作类型: ", r.operation, "\tI/O操作时间: ", r.ioTime)
                            print("进程 ", current_process.name, " 开始 I/O 请求，变为等待态")
                            showProcess()
                            current_process.iostart = TIME
                            current_process.iofinish = TIME + r.ioTime
                            ioQueue.append(current_process)
                            break
                if current_process.status == '等待':
                    break

            # 如果进程完成
            if current_process.serveTimeLeft == 0:
                current_process.status = '完成'
                print(f"进程 {current_process.name} 完成")
                current_process.finishTime = TIME
                current_process.turnAroundTime = TIME - current_process.arraiveTime
                current_process.weightTunAroundTime = current_process.turnAroundTime / current_process.serveTime
                showProcess()
            elif current_process.status != '等待':
                # 如果进程未完成且不需要I/O，放回队列末尾
                current_process.status = '就绪'
                readyQueue.append(current_process)
                print(f"进程 {current_process.name} 时间片内未完成，放回就绪队列末尾")
                showReadyQueue(readyQueue)

        # 检查IO队列中是否有完成IO的进程
        for p in list(ioQueue):
            if len(readyQueue) == 0:
                while p.iofinish > TIME:
                    TIME += 1
                    print("")
                    print("* ", "当前时间: ", TIME, " *")
                    time.sleep(0.1)
            if p.iofinish <= TIME:
                print(f"进程 {p.name} I/O 完成，变为就绪态，放回就绪队列末尾")
                p.status = '就绪'
                readyQueue.append(p)
                ioQueue.remove(p)
                showReadyQueue(readyQueue)

        # 将新到达的进程添加到就绪队列
        for p in list(filter(lambda x: x.arraiveTime == TIME, process)):
            if p not in readyQueue and p not in ioQueue:
                p.status = '就绪'
                readyQueue.append(p)
                showReadyQueue(readyQueue)

    # 计算平均周转时间和带权周转时间
    calculate_averages()


# 尝试对过于冗长的原rr()函数进行重构精简，但是由于时间关系未能完成，总是出现各种各样的错误，故弃用
# def rr():
#     global process, TIME, ioQueue, readyQueue, avgTurnAroundTime, avgWeightTurnAroundTime, running_process, timeSlice
#
#     create()  # 初始化进程
#     print("初始化进程完成")
#     showProcess()
#
#     TIME = 0
#     print("")
#     print("* ", "当前时间: ", TIME, " *")
#     time.sleep(0.1)
#     ioQueue = []
#     readyQueue = [p for p in process if p.arraiveTime <= TIME]
#     print("进程 ", readyQueue[0].name, " 到达，变为就绪态")
#     showReadyQueue(readyQueue)
#
#     running_process = None
#     remaining_time_slice = 0  # 剩余时间片
#
#     while readyQueue or ioQueue or running_process:
#         if running_process and running_process.serveTimeLeft == 0:
#             # 如果当前运行的进程已经完成
#             finish_process(running_process)
#             running_process = None
#             remaining_time_slice = 0
#             # 如果所有进程都已经完成
#             if not (readyQueue or ioQueue):
#                 # 计算平均周转时间和带权周转时间
#                 calculate_averages()
#                 break
#
#         if check_io_queue() and not(ioQueue):
#             remaining_time_slice = 0
#
#         if not running_process and readyQueue:
#             # 如果没有进程在运行，并且就绪队列不为空
#             running_process = readyQueue.pop(0)
#             start_process(running_process)
#             showReadyQueue(readyQueue)
#             remaining_time_slice = timeSlice  # 重置时间片长度
#
#         TIME += 1
#         if running_process:
#             running_process.serveTimeLeft -= 1
#         remaining_time_slice -= 1
#         print("\n* ", "当前时间: ", TIME, " *")
#         time.sleep(0.1)
#
#         check_arriving_processes()  # 检查新到达的进程
#
#         if running_process:
#             if running_process.serveTimeLeft > 0:
#                 check_page_jump(running_process)  # 检查页面跳转
#                 if check_io_request(running_process):
#                     # 如果有 IO 请求发生
#                     running_process = None  # 暂停当前进程
#                     remaining_time_slice = 0
#                     continue
#
#             if remaining_time_slice == 0 and running_process.serveTimeLeft > 0:
#                 # 如果时间片用完且进程未完成
#                 print(f"时间片用完，进程 {running_process.name} 回到就绪队列末尾")
#                 running_process.status = '就绪'
#                 readyQueue.append(running_process)
#                 running_process = None


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
    pageFrameAmount = list(map(int, input("请输入为五个进程各自分配的页面数（用空格分开）: ").split()))

    # 确保输入的页面数与进程数匹配
    while len(pageFrameAmount) != 5:
        print("输入的页面数与进程数不匹配，请重新输入。")
        pageFrameAmount = list(map(int, input("请输入五个进程各自分配的页面数（用空格分开）: ").split()))

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
