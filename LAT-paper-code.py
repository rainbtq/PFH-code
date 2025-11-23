from decimal import Decimal, getcontext
import numpy as np
import random
import math
# 设置更高的精度
getcontext().prec = 300  # 100位精度

# 超时计数器
chaoShi = 0
# 批次计数器
batchNum = 0

CPU_Fault_Rate = 1e-6   # CPU故障率
MEM_Fault_Rate = 1e-6   # 内存故障率
Frequency = 1e6         #系统时钟频率

# 计算CPU故障概率
CPU_Fault_rate = 1-(1-CPU_Fault_Rate)**(1/(3600*Frequency))
CPU_Fault_rate = Decimal(str(CPU_Fault_rate))
# 计算MEM故障概率
MEM_Fault_rate = 1-(1-MEM_Fault_Rate)**(1/(3600*Frequency))
MEM_Fault_rate = Decimal(str(MEM_Fault_rate))

MEM_Size = 1024         # 内存大小MB
Task_Size_inactive = 10 # 任务在非激活情况下占用内存 10MB
Task_Size_active = 30   # 任务在激活情况下占用内存 30MB

MEM_Size = Decimal(str(MEM_Size))
Task_Size_inactive = Decimal(str(Task_Size_inactive))
Task_Size_active = Decimal(str(Task_Size_active))

# 性能记录数组（21个空列表，对应最多21个任务）
taskPerformence = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
faultRateBefore = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
faultRateAfter = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# 任务状态记录数组
inactive1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]                   # 第一个非活跃时间段
inactive2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   # 第二个非活跃时间段
execution = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]               # 执行时间
preemptTime = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]                 # 抢占时间
startTime = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   # 开始时间

Q_table = []  # Q表，用于LAT-EDF算法

# 计算最小公倍数
def lcm(a,b):
    return abs(a*b) // math.gcd(a,b)


# 生成nsets个任务集的任务利用率列表，每个任务集n个任务的利用率之和为u
def StaffordRandFixedSum(n, u, nsets):
    if n < u:
        return None

    #deal with n=1 case
    if n == 1:
        return np.tile(np.array([u]), [nsets, 1])

    k = min(int(u), n - 1)
    s = u
    s1 = s - np.arange(k, k - n, -1.)
    s2 = np.arange(k + n, k, -1.) - s

    tiny = np.finfo(float).tiny
    huge = np.finfo(float).max

    w = np.zeros((n, n + 1))
    w[0, 1] = huge
    t = np.zeros((n - 1, n))

    for i in np.arange(2, n + 1):
        tmp1 = w[i - 2, np.arange(1, i + 1)] * s1[np.arange(0, i)] / float(i)
        tmp2 = w[i - 2, np.arange(0, i)] * s2[np.arange(n - i, n)] / float(i)
        w[i - 1, np.arange(1, i + 1)] = tmp1 + tmp2
        tmp3 = w[i - 1, np.arange(1, i + 1)] + tiny
        tmp4 = s2[np.arange(n - i, n)] > s1[np.arange(0, i)]
        t[i - 2, np.arange(0, i)] = (tmp2 / tmp3) * tmp4 + \
            (1 - tmp1 / tmp3) * (np.logical_not(tmp4))

    x = np.zeros((n, nsets))
    rt = np.random.uniform(size=(n - 1, nsets))  # rand simplex type
    rs = np.random.uniform(size=(n - 1, nsets))  # rand position in simplex
    s = np.repeat(s, nsets)
    j = np.repeat(k + 1, nsets)
    sm = np.repeat(0, nsets)
    pr = np.repeat(1, nsets)

    for i in np.arange(n - 1, 0, -1):  # iterate through dimensions
        # decide which direction to move in this dimension (1 or 0):
        e = rt[(n - i) - 1, ...] <= t[i - 1, j - 1]
        sx = rs[(n - i) - 1, ...] ** (1.0 / i)  # next simplex coord
        sm = sm + (1.0 - sx) * pr * s / (i + 1)
        pr = sx * pr
        x[(n - i) - 1, ...] = sm + pr * e
        s = s - e
        j = j - e  # change transition table column if required

    x[n - 1, ...] = sm + pr * s

    for i in range(0, nsets):
        x[..., i] = x[np.random.permutation(n), i]

    return x.T.tolist()


# 生成nsets个任务集的任务利用率列表，每个任务集n个任务的利用率之和为u
def UUniFastDiscard(n, u, nsets):
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)

        # If no task utilization exceeds 1:
        if all(ut <= 1 for ut in utilizations):
            sets.append(utilizations)

    return sets


# 生成未知个任务集的任务利用率列表，每个任务集n个任务的利用率之和为u
def gen_kato_utilizations(nsets, umin, umax, target_util):
    """
    Kato et al. tasksets generator.

    A task set Γ is generated as follows. A new periodic task is appended
    to Γ as long as U(Γ) ≤ Utot is satisfied. For each task τi, its
    utilization Ui is computed based on a uniform distribution within the
    range of [Umin, Umax]. Only the utilization of the task generated at the
    very end is adjusted so that U(Γ) becomes equal to Utot (thus the Umin
    constraint might not be satisfied for this task).

    Args:
        - `nsets`: Number of tasksets to generate.
        - `umin`: Minimum task utilization.
        - `umax`: Maximum task utilization.
        - `target_util`:
    """
    sets = []
    for i in range(nsets):
        task_set = []
        total_util = 0.0
        while total_util < target_util:
            u = random.uniform(umin, umax)
            if u + total_util > target_util:
                u = target_util - total_util
            total_util += u
            task_set.append(u)
        sets.append(task_set)
    return sets


# 从给定的周期列表中随机选择一组周期
def gen_periods_discrete(n, nsets, periods):
    """
    Generate a matrix of (nsets x n) random periods chosen randomly in the
    list of periods.

    Args:
        - `n`: The number of tasks in a task set.
        - `nsets`: Number of sets to generate.
        - `periods`: A list of available periods.
    """
    try:
        return np.random.choice(periods, size=(nsets, n)).tolist()
    except AttributeError:
        # Numpy < 1.7:
        p = np.array(periods)
        return p[np.random.randint(len(p), size=(nsets, n))].tolist()


def edf_no_preempt(detailed_tasks):
    task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    num = 0
    batchNum = 1
    superPeriod = 1

    all_Instance_Number = 0
    all_Success_Instance_Number = 0
    success_Instance_percent = 0.0
    success_Instance_percent = (str(success_Instance_percent))

    for tasks in detailed_tasks:

        for task in tasks:
            superPeriod = lcm(superPeriod, task[2])
        for task in tasks:
            all_Instance_Number += superPeriod / task[2]
        num += 1
        #print('第'+str(num)+'批任务集开始模拟执行：')
        readyQueue = []
        currentTime = 0
        for task in tasks:
            readyQueue.append([task[0], task[2], 0, task[1], 0, 0,task[3]])#readyQueue对象(任务序号，周期，已执行时间，WCET，生命时长(从job进入就绪队列开始算)，第一次执行标记,绝对截止时间
        # print('一批结束')
        readyQueue.sort(key=lambda x: x[6])
        while currentTime < superPeriod:

            if readyQueue:
                i = 0
                while i < len(readyQueue):
                    if currentTime >= readyQueue[i][6]:
                        print('该任务超时')
                        del readyQueue[i]
                        # 不增加i，因为删除后后面的元素会前移
                    else:
                        i += 1  # 只有不删除时才增加索引

            if currentTime != 0:
                for task in tasks:
                    if (currentTime % task[2]) == 0: #有任务开始周期
                        #print('此时为第'+str(currentTime)+'ms,任务的周期为：'+str(task[2]))
                        readyQueue.append([task[0],task[2],0,task[1],0,0,task[3]+currentTime])
                # readyQueue.sort(key=lambda x: x[1]) #不抢占，所以不排序

            if readyQueue:
                readyQueue[0][2] += 1
                # print('在')
                # print(currentTime)
                # print('到')
                # print(currentTime+1)
                # print(readyQueue[0])
                # print('执行了')
                #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程执行了1ms')
                if(readyQueue[0][5] == 0):  #修改第一次执行标记
                    readyQueue[0][5] = 1
                    startTime[readyQueue[0][0]-1] = currentTime  #记录这个job的开始时间，因为任务序号从1开始，所以减1
                if (readyQueue[0][2] == readyQueue[0][3]):  # 任务执行完毕
                    #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程完成了执行')
                    execution[readyQueue[0][0]-1] = readyQueue[0][3]
                    preemptTime[readyQueue[0][0]-1] = 0
                    inactive1[readyQueue[0][0]-1] = readyQueue[0][4] + 1 - (currentTime + 1 - startTime[readyQueue[0][0]-1])
                    taskPerformence[readyQueue[0][0]-1].append([inactive1[readyQueue[0][0]-1]+inactive2[readyQueue[0][0]-1],  #本job需要用上一个job的inactive2
                                                                execution[readyQueue[0][0]-1],
                                                                preemptTime[readyQueue[0][0]-1], readyQueue[0][1]])
                    inactive2[readyQueue[0][0]-1] = readyQueue[0][1] - (1 + currentTime - startTime[readyQueue[0][0]-1]) - inactive1[readyQueue[0][0]-1] #这个inactive2是当前job的，但是用于下一个job的故障概率计算，inactive2=周期-生命时长-inactive1
                    del readyQueue[0]
                    readyQueue.sort(key=lambda x: x[6] - currentTime)   #根据相对截止时间排序

            currentTime += 1
            for i in readyQueue:   #就绪队列所有job的生命时长+1
                i[4] += 1

        number = 1
        data1 = [None]
        data2 = [None]
        for records in taskPerformence:   #records是一个任务的所有job的记录
            if records:
                numbers = 1
                Task_Fault_Before_Mean = 0
                Task_Fault_After_Mean = 0
                for record in records:    #record是某个job的记录

                    #print('第'+str(number)+'个任务的第'+str(numbers)+'个进程实例执行结果为：inactive:'+str(record[0])+' executionTime:'+str(record[1])+' ioTime:'
                          #+str(record[2])+' preemptTime:'+str(record[3])+' Period:'+str(record[4]))
                    Task_Fault_Before = Compute_Task_Fault_Before()
                    Task_Fault_After = Compute_Task_Fault_After(record[2],record[1],record[0],record[3])
                    task_PFH_list[number - 1] = Decimal(task_PFH_list[number - 1])
                    task_PFH_list[number - 1] += Task_Fault_After
                    #print('粗略硬件故障率为：'+str(Task_Fault_Before))
                    #print('精细硬件故障率为：'+str(Task_Fault_After))
                    Task_Fault_Before_Mean += Task_Fault_Before
                    Task_Fault_After_Mean += Task_Fault_After
                    # faultRateBefore[number].append(Task_Fault_Before)
                    # faultRateAfter[number].append(Task_Fault_After)


                    numbers += 1

                all_Success_Instance_Number += (numbers - 1)
                Task_Fault_After_Mean = Task_Fault_After_Mean/(numbers-1)
                Task_Fault_Before_Mean = Task_Fault_Before_Mean/(numbers-1)
                data1.append(Task_Fault_Before_Mean)
                data2.append(Task_Fault_After_Mean)
                task_PFH_list[number - 1] /= (numbers - 1)
                number += 1


        for records in taskPerformence:
            records.clear()
        for p in inactive2:
            p = 0
        numbers = 0
        for task in tasks:
            period = task[2]
            # print('前')
            # print(task_PFH_list[numbers])
            task_PFH_list[numbers] = math.ceil(60 * 60 * 1000 / period) * task_PFH_list[numbers]
            # print('后')
            # print(task_PFH_list[numbers])
            numbers += 1
        batchNum += 1
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in task_PFH_list:
        sum1 += Decimal(str(i))

    success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))

    return sum1 / 20,success_Instance_percent


def edf_preempt(detailed_tasks):
    task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    num = 0
    batchNum = 1
    superPeriod = 1

    all_Instance_Number = 0
    all_Success_Instance_Number = 0
    success_Instance_percent = 0.0
    success_Instance_percent = (str(success_Instance_percent))

    for tasks in detailed_tasks:

        for task in tasks:
            superPeriod = lcm(superPeriod, task[2])
        for task in tasks:
            all_Instance_Number += superPeriod / task[2]
        num += 1
        #print('第'+str(num)+'批任务集开始模拟执行：')
        readyQueue = []
        currentTime = 0
        for task in tasks:
            # print(task[0])
            readyQueue.append([task[0], task[2], 0, task[1], 0, 0,task[3]])#readyQueue对象(任务序号，周期，已执行时间，WCET，生命时长，第一次执行标记(为了检测startTime),绝对截止时间

        # print('一批结束')
        readyQueue.sort(key=lambda x: x[6])
        while currentTime < superPeriod:

            if readyQueue:
                i = 0
                while i < len(readyQueue):
                    if currentTime >= readyQueue[i][6]:
                        # print('该任务超时')
                        del readyQueue[i]
                        # 不增加i，因为删除后后面的元素会前移
                    else:
                        i += 1  # 只有不删除时才增加索引


            if currentTime != 0:
                for task in tasks:
                    if (currentTime % task[2]) == 0:  # 有任务开始周期
                        # print('此时为第'+str(currentTime)+'ms,任务的周期为：'+str(task[2]))
                        readyQueue.append([task[0], task[2], 0, task[1], 0, 0, task[3] + currentTime])

                readyQueue.sort(key=lambda x: x[6] - currentTime)
            if readyQueue:
                readyQueue[0][2] += 1
                #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程执行了1ms')
                if (readyQueue[0][5] == 0):  # 修改第一次执行标记
                    readyQueue[0][5] = 1
                    startTime[readyQueue[0][0] - 1] = currentTime  # 记录这个job的开始时间，因为任务序号从1开始，所以减1
                if (readyQueue[0][2] == readyQueue[0][3]):  # 任务执行完毕
                    #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程完成了执行')

                    execution[readyQueue[0][0]-1] = readyQueue[0][3]
                    preemptTime[readyQueue[0][0]-1] = 1 + currentTime - startTime[readyQueue[0][0]-1] - execution[readyQueue[0][0]-1]
                    inactive1[readyQueue[0][0]-1] = readyQueue[0][4] + 1 - (currentTime + 1 - startTime[readyQueue[0][0]-1])
                    taskPerformence[readyQueue[0][0]-1].append([inactive1[readyQueue[0][0]-1]+inactive2[readyQueue[0][0]-1],
                                                                execution[readyQueue[0][0]-1],
                                                                preemptTime[readyQueue[0][0]-1], readyQueue[0][1]])
                    inactive2[readyQueue[0][0]-1] = readyQueue[0][1] - (1 + currentTime - startTime[readyQueue[0][0]-1]) - inactive1[readyQueue[0][0]-1] #这个inactive2是当前job的，但是用于下一个job的故障概率计算，inactive2=周期-生命时长-inactive1
                    del readyQueue[0]
            currentTime += 1
            for i in readyQueue:
                i[4] += 1
        number = 1
        data1 = [None]
        data2 = [None]
        for records in taskPerformence:
            if records:
                numbers = 1
                Task_Fault_Before_Mean = 0
                Task_Fault_After_Mean = 0
                for record in records:
                    #print('第'+str(number)+'个任务的第'+str(numbers)+'个进程实例执行结果为：inactive:'+str(record[0])+' executionTime:'+str(record[1])+' ioTime:'
                          #+str(record[2])+' preemptTime:'+str(record[3])+' Period:'+str(record[4]))
                    Task_Fault_Before = Compute_Task_Fault_Before()
                    Task_Fault_After = Compute_Task_Fault_After(record[2],record[1],record[0],record[3])
                    task_PFH_list[number - 1] = Decimal(task_PFH_list[number - 1])
                    task_PFH_list[number - 1] += Task_Fault_After
                    Task_Fault_Before_Mean += Task_Fault_Before
                    Task_Fault_After_Mean += Task_Fault_After
                    numbers += 1

                all_Success_Instance_Number += (numbers - 1)
                Task_Fault_After_Mean = Task_Fault_After_Mean/(numbers-1)
                Task_Fault_Before_Mean = Task_Fault_Before_Mean/(numbers-1)
                data1.append(Task_Fault_Before_Mean)
                data2.append(Task_Fault_After_Mean)
                task_PFH_list[number - 1] /= (numbers - 1)
                number += 1


        for records in taskPerformence:
            records.clear()
        for p in inactive2:
            p = 0
        numbers = 0
        for task in tasks:
            period = task[2]
            task_PFH_list[numbers] = math.ceil(60 * 60 * 1000 / period) * task_PFH_list[numbers]
            numbers += 1
        batchNum += 1
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in task_PFH_list:
        sum1 += Decimal(str(i))

    success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))

    return sum1 / 20,success_Instance_percent


def LAT_edf(detailed_tasks):

     #非响应模式标记

    task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    num = 0
    batchNum = 1
    superPeriod = 1

    all_Instance_Number = 0
    all_Success_Instance_Number = 0
    success_Instance_percent = 0.0
    success_Instance_percent = (str(success_Instance_percent))

    for tasks in detailed_tasks:
        Q_table.clear()
        tasks = get_Q_table_q_attribute(tasks)
        # print('加入q属性后：')
        # print(tasks)
        # print('Q表：')
        # print(Q_table)
        for task in tasks:
            superPeriod = lcm(superPeriod, task[2])
        for task in tasks:
            all_Instance_Number += superPeriod / task[2]
        num += 1
        #print('第'+str(num)+'批任务集开始模拟执行：')
        readyQueue = []
        currentTime = 0
        for task in tasks:
            readyQueue.append([task[0], task[2], 0, task[1], 0, 0,task[3],task[4],task[5],0])#readyQueue对象(任务序号，周期，已执行时间，WCET，生命时长，第一次执行标记(为了检测startTime),绝对截止时间,关键性标记_1为HI_0为LOW,q属性,标记这个job是否刚结束非响应模式）

        no_response_flag = 0

        readyQueue.sort(key=lambda x: x[6])
        while currentTime < superPeriod:

            if readyQueue:
                i = 0
                while i < len(readyQueue):
                    if currentTime >= readyQueue[i][6]:
                        # print('任务集是：')
                        # print(tasks)
                        # print('以下任务超时：')
                        # print(readyQueue[i])
                        # print('超周期是：')
                        # print(superPeriod)
                        # print('当前时间是：')
                        # print(currentTime)
                        del readyQueue[i]
                        # 不增加i，因为删除后后面的元素会前移
                    else:
                        i += 1  # 只有不删除时才增加索引


            if currentTime != 0:

                for task in tasks:
                    if (currentTime % task[2]) == 0:  # 有任务开始周期
                        # print('此时为第'+str(currentTime)+'ms,任务的周期为：'+str(task[2]))
                        readyQueue.append([task[0], task[2], 0, task[1], 0, 0, task[3] + currentTime,task[4],task[5],0])


                if readyQueue:
                    if (len(readyQueue)!=0) & (no_response_flag == 0) & (readyQueue[0][9]==0): #先看一下有没有发生低抢高
                        # print('111')
                        readyQueue2 = readyQueue.copy()
                        readyQueue2.sort(key=lambda x: x[6] - currentTime)
                        # print(readyQueue[0][0])
                        # print(readyQueue2[0][0])
                        # print(readyQueue[0][7])
                        # print(readyQueue2[0][7])
                        if (readyQueue[0][0] != readyQueue2[0][0]) & (readyQueue[0][7] == 1) & (readyQueue2[0][7] == 0) & (readyQueue[0][5] == 1):  #说明发生了关键性方面的低抢高
                            # print(readyQueue[0])
                            # print('here')
                            # print(currentTime)
                            no_response_flag = readyQueue[0][8]
                            no_response_flag = min(no_response_flag, readyQueue[0][3] - readyQueue[0][2])
                            # print('此时获得静态q属性')
                            # print(no_response_flag)
                            if no_response_flag < (readyQueue[0][3] - readyQueue[0][2]): #静态属性不够
                                # print('静态q属性不够')
                                no_response_flag = query_Q_table(readyQueue[0][6] - currentTime)
                                no_response_flag = min(no_response_flag, readyQueue[0][3] - readyQueue[0][2])
                                if no_response_flag == -1:
                                    no_response_flag = readyQueue[0][3] - readyQueue[0][2]

                if no_response_flag == 0: #说明没有发生低抢高
                    readyQueue.sort(key=lambda x: x[6] - currentTime)
            if readyQueue:
                readyQueue[0][2] += 1
                # print('在')
                # print(currentTime)
                # print('到')
                # print(currentTime+1)
                # print(readyQueue[0])
                # print('执行了')
                # print('当前非响应时间是：')
                # print(no_response_flag)
                #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程执行了1ms')
                if (readyQueue[0][5] == 0):  # 修改第一次执行标记
                    readyQueue[0][5] = 1
                    startTime[readyQueue[0][0] - 1] = currentTime  # 记录这个job的开始时间，因为任务序号从1开始，所以减1
                if (readyQueue[0][2] == readyQueue[0][3]):  # 任务执行完毕
                    #print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程完成了执行')

                    execution[readyQueue[0][0]-1] = readyQueue[0][3]
                    preemptTime[readyQueue[0][0]-1] = 1 + currentTime - startTime[readyQueue[0][0]-1] - execution[readyQueue[0][0]-1]
                    inactive1[readyQueue[0][0]-1] = readyQueue[0][4] + 1 - (currentTime + 1 - startTime[readyQueue[0][0]-1])
                    taskPerformence[readyQueue[0][0]-1].append([inactive1[readyQueue[0][0]-1]+inactive2[readyQueue[0][0]-1],
                                                                execution[readyQueue[0][0]-1],
                                                                preemptTime[readyQueue[0][0]-1], readyQueue[0][1]])
                    inactive2[readyQueue[0][0]-1] = readyQueue[0][1] - (1 + currentTime - startTime[readyQueue[0][0]-1]) - inactive1[readyQueue[0][0]-1] #这个inactive2是当前job的，但是用于下一个job的故障概率计算，inactive2=周期-生命时长-inactive1
                    del readyQueue[0]

                    # 检查是否有已经开始执行的HI关键性任务需要抢占
                    hi_task_to_preempt = None
                    for i in range(len(readyQueue)):
                        # 检查条件：已经开始执行过的HI关键性任务 (readyQueue[i][2] != 0 且 readyQueue[i][7] == 1)
                        if readyQueue[i][2] != 0 and readyQueue[i][7] == 1:
                            # 检查是否有绝对截止期比这个HI任务更早的任务
                            has_earlier_deadline = False
                            for j in range(len(readyQueue)):
                                if j != i and readyQueue[j][6] < readyQueue[i][6]:
                                    has_earlier_deadline = True
                                    break

                            # 如果没有更早截止期的任务，则标记这个HI任务需要被处理
                            if not has_earlier_deadline:
                                hi_task_to_preempt = i
                                break

                    # 如果找到了符合条件的HI任务，将其移到队列最前面
                    if hi_task_to_preempt is not None:             #在这里，不需要判断此时有无更高优先级job释放，因为在开头那里更新readyQueue后会判断一次并采取措施
                        hi_task = readyQueue.pop(hi_task_to_preempt)
                        readyQueue.insert(0, hi_task)

            currentTime += 1
            if readyQueue:
                if readyQueue[0][9] == 1:
                    readyQueue[0][9] = 0

            if no_response_flag > 0:
                no_response_flag -= 1
                if readyQueue:
                    if (no_response_flag == 0):
                        readyQueue[0][9] = 1
            for i in readyQueue:
                i[4] += 1
        number = 1
        data1 = [None]
        data2 = [None]
        for records in taskPerformence:
            if records:
                numbers = 1
                Task_Fault_Before_Mean = 0
                Task_Fault_After_Mean = 0
                for record in records:
                    #print('第'+str(number)+'个任务的第'+str(numbers)+'个进程实例执行结果为：inactive:'+str(record[0])+' executionTime:'+str(record[1])+' ioTime:'
                          #+str(record[2])+' preemptTime:'+str(record[3])+' Period:'+str(record[4]))
                    Task_Fault_Before = Compute_Task_Fault_Before()
                    Task_Fault_After = Compute_Task_Fault_After(record[2],record[1],record[0],record[3])
                    task_PFH_list[number - 1] = Decimal(task_PFH_list[number - 1])
                    task_PFH_list[number - 1] += Task_Fault_After
                    Task_Fault_Before_Mean += Task_Fault_Before
                    Task_Fault_After_Mean += Task_Fault_After
                    numbers += 1

                all_Success_Instance_Number += (numbers - 1)
                Task_Fault_After_Mean = Task_Fault_After_Mean/(numbers-1)
                Task_Fault_Before_Mean = Task_Fault_Before_Mean/(numbers-1)
                data1.append(Task_Fault_Before_Mean)
                data2.append(Task_Fault_After_Mean)
                task_PFH_list[number - 1] /= (numbers - 1)
                number += 1


        for records in taskPerformence:
            records.clear()
        for p in inactive2:
            p = 0
        numbers = 0
        for task in tasks:
            period = task[2]
            task_PFH_list[numbers] = math.ceil(60 * 60 * 1000 / period) * task_PFH_list[numbers]
            numbers += 1
        batchNum += 1
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in task_PFH_list:
        sum1 += Decimal(str(i))

    success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))

    return sum1 / 20,success_Instance_percent


def get_Q_table_q_attribute(tasks): #计算Q表并给任务加一个q属性
    deadlines = []
    max_deadline = 0
    # Q_table = []
    for i in tasks:
        max_deadline = max(max_deadline, i[3])  #因为在计算Q表时，t不用超过任务的最大截止时间，再大的t用不到，那些job都超时了
    for i in tasks:
        deadline1 = i[3]
        while deadline1 <= max_deadline:
            deadlines.append(deadline1)
            deadline1 += i[2]

    deadlines = sorted(set(deadlines))  # 去重并升序排序

    def DBF(tau_i, t):

        C_i = tau_i[1]  # WCET
        D_i = tau_i[3]  # 截止时间
        T_i = tau_i[2]  # 周期

        if t < D_i:
            return 0
        else:
            return max(0, ((t - D_i) // T_i + 1) * C_i)
    old_Q_value = 1e6
    for deadline in deadlines:

        #计算总DBF
        dbf=0
        for i in tasks:
            dbf += DBF(i,deadline)
        #
        the_Q_value = deadline - dbf
        if the_Q_value < 0:
            the_Q_value = 0
        the_Q_value = min(the_Q_value,old_Q_value)
        if the_Q_value != old_Q_value:
            old_Q_value = the_Q_value
            Q_table.append((deadline,the_Q_value))
        if the_Q_value == 0:
            break

    tasks_with_q = []

    for i in tasks:
        qtime = query_Q_table(i[3])
        qtime = min(qtime,i[1])
        # i.append(qtime)

        # 无论task是元组还是列表，都转换为列表并添加q属性
        new_task = list(i) + [qtime]
        tasks_with_q.append(new_task)
    return tasks_with_q    #从此task的属性为(id,wcet,period,deadline,random_attri 1表示HI而0表示LO,q_attri 静态q属性)


# Q表查询函数
def query_Q_table(t):
    # 如果t小于第一个断点
    if t < Q_table[0][0]:
        return -1   #无穷

    for i in range(len(Q_table)):
        current_t, current_Q = Q_table[i]

        # 如果是最后一个断点
        if i == len(Q_table) - 1:
            return current_Q

        next_t, _ = Q_table[i + 1]
        if current_t <= t < next_t:
            return current_Q


def generate_task_details(utilizations, periods): #生成D=T的任务集,所以代码直接deadline = period
    """
    将利用率列表和周期列表组合成任务集，并添加任务ID

    :param utilizations: 任务利用率列表，格式为 [[u1, u2, ...], ...]
    :param periods: 任务周期列表，格式为 [[p1, p2, ...], ...]
    :return: 返回详细任务信息，格式为 [[(id, wcet, period,deadline,random_attr), ...], ...]
    """

    def trunc(x, p):
        """截断函数，用于处理浮点精度"""
        resul = int(int(x * 10 ** p) / float(10 ** p))
        if resul == 0:
            return 1
        else:
            return resul

    detailed_tasks = []

    for us, ps in zip(utilizations, periods):
        task_group = []
        num = 1
        for ui, pi in zip(us, ps):
            wcet = int(trunc(ui * pi, 6))
            period = trunc(pi, 6)
            # 将结果添加到任务组中
            deadline = period
            random_attr = random.randint(0, 1)  # 随机生成0或1
            task_group.append([num, wcet, period, deadline,random_attr])
            num += 1
        detailed_tasks.append(task_group)

    return detailed_tasks


def Compute_Task_Fault_Before():

    Task_Fault_Before = 1 - (1 - CPU_Fault_rate) * (1 - MEM_Fault_rate)
    return Task_Fault_Before


def Compute_Task_Fault_After(preTime,exeTime,inacTime,period):

    preTime = Decimal(str(preTime))
    exeTime = Decimal(str(exeTime))
    inacTime = Decimal(str(inacTime))
    period = Decimal(str(period))

    inacFaultRate = 1 - (1-Task_Size_inactive/MEM_Size*MEM_Fault_rate)**(inacTime/period)
    exePreeFaultRate = 1 - ((1-CPU_Fault_rate)*(1-Task_Size_active/MEM_Size*MEM_Fault_rate))**((preTime + exeTime)/period)
    Task_Fault_After = 1-(1-inacFaultRate)*(1-exePreeFaultRate)
    return Task_Fault_After


if __name__ == '__main__':
     data1 = [None]     #edf_no_preempt_PFH
     data2 = [None]     #edf_preempt_PFH
     data3 = [None]     #LAT__PFH
     data4 = [None]     #upper_bound_failurePFH
     data5 = [None]     #failureMaxPFH


     success_Instance_percent_edf_preempt = 0
     success_Instance_percent_edf_preempt = Decimal(str(success_Instance_percent_edf_preempt))

     success_Instance_percent_edf_no_preempt = 0
     success_Instance_percent_edf_no_preempt = Decimal(str(success_Instance_percent_edf_no_preempt))

     success_Instance_percent_LAT = 0
     success_Instance_percent_LAT = Decimal(str(success_Instance_percent_LAT))


     mean_Edf_preempt_PFH = 0
     mean_Edf_preempt_PFH = Decimal(str(mean_Edf_preempt_PFH))

     mean_Edf_no_preempt_PFH = 0
     mean_Edf_no_preempt_PFH = Decimal(str(mean_Edf_no_preempt_PFH))

     mean_LAT_PFH = 0
     mean_LAT_PFH = Decimal(str(mean_LAT_PFH))


     uti=0.05
     while uti <= 1.0 :
         count1=1

         edf_preempt_PFH = 0
         edf_no_preempt_PFH = 0
         LAT_PFH = 0


         upper_bound_failurePFH1 = 0 #公式的理论最大值
         oldfailureMaxPFH1 = 0  #未使用时间分配函数前的值


         edf_preempt_PFH = Decimal(str(edf_preempt_PFH))
         edf_no_preempt_PFH = Decimal(str(edf_no_preempt_PFH))
         LAT_PFH = Decimal(str(LAT_PFH))

         upper_bound_failurePFH1 = Decimal(str(upper_bound_failurePFH1))
         oldfailureMaxPFH1 = Decimal(str(oldfailureMaxPFH1))

         oldfailureMaxPFH = 0
         inacFaultRate = 0
         exePreeFaultRate = 0
         upper_bound_failurePFH= 0

         oldfailureMaxPFH = Decimal(str(oldfailureMaxPFH))
         inacFaultRate = Decimal(str(inacFaultRate))
         exePreeFaultRate = Decimal(str(exePreeFaultRate))
         upper_bound_failurePFH = Decimal(str(upper_bound_failurePFH))


         success_Instance_percent_edf_preempt1 = 0
         success_Instance_percent_edf_preempt1 = Decimal(str(success_Instance_percent_edf_preempt1))

         success_Instance_percent_edf_no_preempt1 = 0
         success_Instance_percent_edf_no_preempt1 = Decimal(str(success_Instance_percent_edf_no_preempt1))


         success_Instance_percent_LAT1 = 0
         success_Instance_percent_LAT1 = Decimal(str(success_Instance_percent_LAT1))


         while count1 <= 10:
             detailed_tasks = generate_task_details(
                 StaffordRandFixedSum(20, uti, 1), gen_periods_discrete(20, 1, [400,600,800,1000,1200]))

             for i in detailed_tasks: # 计算一下理论上限和旧方法计算值
                for j in i:
                    preTime1 = j[2] - j[1]
                    exeTime1 = j[1]
                    inacTime1 = j[2] - j[1]
                    period1 = j[2]

                    preTime1 = Decimal(str(preTime1))
                    exeTime1 = Decimal(str(exeTime1))
                    inacTime1 = Decimal(str(inacTime1))
                    period1 = Decimal(str(period1))


                    oldfailureMaxPFH11 = 1 - (1 - CPU_Fault_rate) * (1 - Task_Size_inactive/MEM_Size*MEM_Fault_rate)
                    oldfailureMaxPFH += math.ceil(60 * 60 * 1000 / period1) * oldfailureMaxPFH11
                    inacFaultRate = 1 - (1 - Task_Size_inactive / MEM_Size * MEM_Fault_rate) ** (inacTime1 / period1)
                    exePreeFaultRate = 1 - ((1 - CPU_Fault_rate) * (1 - Task_Size_active / MEM_Size * MEM_Fault_rate)) ** ((exeTime1 + preTime1) / period1)
                    upper_bound_failurePFH11 = 1 - (1 - inacFaultRate) * (1 - exePreeFaultRate)
                    upper_bound_failurePFH += math.ceil(60 * 60 * 1000 / period1) * upper_bound_failurePFH11

                oldfailureMaxPFH /= 20 #因为任务集里有20个任务
                upper_bound_failurePFH /= 20

                oldfailureMaxPFH1 += oldfailureMaxPFH
                upper_bound_failurePFH1 += upper_bound_failurePFH

             backNum = 0.0
             backNum = Decimal(str(backNum))

             backNum1 = 0.0
             backNum1 = Decimal(str(backNum1))


             backNum, backNum1 = edf_preempt(detailed_tasks)
             edf_preempt_PFH += backNum
             success_Instance_percent_edf_preempt1 += backNum1


             backNum, backNum1 = edf_no_preempt(detailed_tasks)
             edf_no_preempt_PFH += backNum
             success_Instance_percent_edf_no_preempt1 += backNum1

             backNum, backNum1 = LAT_edf(detailed_tasks)
             LAT_PFH += backNum
             success_Instance_percent_LAT1 += backNum1


             print(count1)
             count1 += 1
             print('轮次：')

             print('uti:')
             print(uti)

         edf_preempt_PFH /= 10   #除以任务集的个数
         edf_no_preempt_PFH /= 10
         LAT_PFH /= 10
         upper_bound_failurePFH1 /= 10
         oldfailureMaxPFH1 /= 10


         data1.append(edf_no_preempt_PFH)
         data2.append(edf_preempt_PFH)
         data3.append(LAT_PFH)
         data4.append(upper_bound_failurePFH1)
         data5.append(oldfailureMaxPFH1)


         success_Instance_percent_edf_preempt1 /= 10  #除以任务集的个数
         success_Instance_percent_edf_no_preempt1 /= 10
         success_Instance_percent_LAT1 /= 10


         success_Instance_percent_edf_preempt += success_Instance_percent_edf_preempt1
         success_Instance_percent_edf_no_preempt += success_Instance_percent_edf_no_preempt1
         success_Instance_percent_LAT += success_Instance_percent_LAT1


         mean_Edf_preempt_PFH += edf_preempt_PFH
         mean_Edf_no_preempt_PFH += edf_no_preempt_PFH
         mean_LAT_PFH += LAT_PFH


         print('uti:')
         print(uti)
         uti = round(uti + 0.05, 2)

        #利用率共20种

     success_Instance_percent_edf_preempt /= 20
     success_Instance_percent_edf_no_preempt /= 20
     success_Instance_percent_LAT /= 20


     # print(success_Instance_percent_edf_preempt)
     # print(success_Instance_percent_edf_no_preempt)
     # print(success_Instance_percent_LAT)


     mean_Edf_preempt_PFH /= 20
     mean_Edf_no_preempt_PFH /= 20
     mean_LAT_PFH /= 20


     # print(mean_Edf_preempt_PFH)
     # print(mean_Edf_no_preempt_PFH)
     # print(mean_LAT_PFH)


     print('三种平均完成率：')

     print('success_Instance_percent_edf_preempt:')
     print(success_Instance_percent_edf_preempt)
     print('success_Instance_percent_edf_no_preempt:')
     print(success_Instance_percent_edf_no_preempt)
     print('success_Instance_percent_LAT:')
     print(success_Instance_percent_LAT)

     print('三种平均故障率：')
     print('mean_Edf_preempt_PFH:')
     print(mean_Edf_preempt_PFH)
     print('mean_Edf_no_preempt_PFH:')
     print(mean_Edf_no_preempt_PFH)
     print('mean_LAT_PFH:')
     print(mean_LAT_PFH)