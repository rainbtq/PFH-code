#
#
# from base import  *
#
# Q_table1 = []
#
# def get_q_attribute(tasks): #计算Q表并给任务加一个q属性
#     deadlines = []
#     max_deadline = 0
#     # Q_table = []
#     for i in tasks:
#         max_deadline = max(max_deadline, i[3])  # 因为在计算Q表时，t不用超过任务的最大截止时间，再大的t用不到，那些job都超时了
#     for i in tasks:
#         deadline1 = i[3]
#         while deadline1 <= max_deadline:
#             deadlines.append(deadline1)
#             deadline1 += i[2]
#
#     deadlines = sorted(set(deadlines))  # 去重并升序排序
#
#     def DBF(tau_i, t):
#
#         C_i = tau_i[1]  # WCET
#         D_i = tau_i[3]  # 截止时间
#         T_i = tau_i[2]  # 周期
#
#         if t < D_i:
#             return 0
#         else:
#             return max(0, ((t - D_i) // T_i + 1) * C_i)
#
#     old_Q_value = 1e6
#     for deadline in deadlines:
#
#         # 计算总DBF
#         dbf = 0
#         for i in tasks:
#             dbf += DBF(i, deadline)
#         #
#         the_Q_value = deadline - dbf
#         if the_Q_value < 0:
#             the_Q_value = 0
#         the_Q_value = min(the_Q_value, old_Q_value)
#         if the_Q_value != old_Q_value:
#             old_Q_value = the_Q_value
#             Q_table1.append((deadline, the_Q_value))
#         if the_Q_value == 0:
#             break
#
#     tasks_with_q = []
#
#     for i in tasks:
#         qtime = query_Q_table(i[3])
#         qtime = min(qtime, i[1])
#         # i.append(qtime)
#         if qtime == -1:
#             qtime = i[1]
#         # 无论task是元组还是列表，都转换为列表并添加q属性
#         new_task = list(i) + [qtime]
#         tasks_with_q.append(new_task)
#     return tasks_with_q  # 从此task的属性为(id,wcet,period,deadline,random_attri 1表示HI而0表示LO,q_attri 静态q属性)
#
#
# # Q表查询函数
# def query_Q_table(t):
#
#
#     # 如果t小于第一个断点
#     if t < Q_table1[0][0]:
#         return -1   #无穷
#
#     for i in range(len(Q_table1)):
#         current_t, current_Q = Q_table1[i]
#
#         # 如果是最后一个断点
#         if i == len(Q_table1) - 1:
#             return current_Q
#
#         next_t, _ = Q_table1[i + 1]
#         if current_t <= t < next_t:
#             return current_Q
#
#
#
#
# def q_attribute_schedule(detailed_tasks):
#
#
#     task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#     num = 0
#     batchNum = 1
#     superPeriod = 1
#
#     all_Instance_Number = 0
#     all_Success_Instance_Number = 0
#     success_Instance_percent = 0.0
#     success_Instance_percent = (str(success_Instance_percent))
#
#     for tasks in detailed_tasks:
#         tasks = get_q_attribute(tasks)
#         # print('加入q属性后：')
#         # print(tasks)
#         # print('Q表：')
#         # print(Q_table)
#         for task in tasks:
#             superPeriod = lcm(superPeriod, task[2])
#         for task in tasks:
#             all_Instance_Number += superPeriod / task[2]
#         num += 1
#         # print('第'+str(num)+'批任务集开始模拟执行：')
#         readyQueue = []
#         currentTime = 0
#         for task in tasks:
#             readyQueue.append([task[0], task[2], 0, task[1], 0, 0 ,task[3] ,task[4] ,task[5]
#                                ,0]  )# readyQueue对象(任务序号，周期，已执行时间，WCET，生命时长，第一次执行标记(为了检测startTime),绝对截止时间,关键性标记_1为HI_0为LOW,q属性,标记这个job是否刚结束非响应模式）
#
#         no_response_flag = 0
#
#         readyQueue.sort(key=lambda x: x[6])
#         while currentTime < superPeriod:
#
#             if readyQueue:
#                 i = 0
#                 while i < len(readyQueue):
#                     if currentTime >= readyQueue[i][6]:
#                         # print('任务集是：')
#                         # print(tasks)
#                         # print('以下任务超时：')
#                         # print(readyQueue[i])
#                         # print('超周期是：')
#                         # print(superPeriod)
#                         # print('当前时间是：')
#                         # print(currentTime)
#                         del readyQueue[i]
#                         # 不增加i，因为删除后后面的元素会前移
#                     else:
#                         i += 1  # 只有不删除时才增加索引
#
#
#             if currentTime != 0:
#
#                 for task in tasks:
#                     if (currentTime % task[2]) == 0:  # 有任务开始周期
#                         # print('此时为第'+str(currentTime)+'ms,任务的周期为：'+str(task[2]))
#                         readyQueue.append \
#                             ([task[0], task[2], 0, task[1], 0, 0, task[3] + currentTime ,task[4] ,task[5] ,0])
#
#
#                 if readyQueue:
#                     if (len(readyQueue ) != 0) & (no_response_flag == 0) & (readyQueue[0][9 ] == 0): # 先看一下有没有发生低抢高
#                         # print('111')
#                         readyQueue2 = readyQueue.copy()
#                         readyQueue2.sort(key=lambda x: x[6] - currentTime)
#                         # print(readyQueue[0][0])
#                         # print(readyQueue2[0][0])
#                         # print(readyQueue[0][7])
#                         # print(readyQueue2[0][7])
#                         if (readyQueue[0][0] != readyQueue2[0][0]) & (readyQueue[0][7] == 1) & \
#                                 (readyQueue2[0][7] == 0) & (readyQueue[0][5] == 1):  # 说明发生了关键性方面的低抢高
#                             # print(readyQueue[0])
#                             # print('here')
#                             # print(currentTime)
#                             no_response_flag = readyQueue[0][8]
#                             no_response_flag = min(no_response_flag, readyQueue[0][3] - readyQueue[0][2])
#                             # print('此时获得静态q属性')
#                             # print(no_response_flag)
#                             # if no_response_flag == -1:
#                             #     no_response_flag = readyQueue[0][3] - readyQueue[0][2]
#                 if no_response_flag == 0:  # 说明没有发生低抢高或不允许LAT运行
#                     readyQueue.sort(key=lambda x: x[6] - currentTime)
#             if readyQueue:
#                 readyQueue[0][2] += 1
#                 # print('在')
#                 # print(currentTime)
#                 # print('到')
#                 # print(currentTime+1)
#                 # print(readyQueue[0])
#                 # print('执行了')
#                 # print('当前非响应时间是：')
#                 # print(no_response_flag)
#                 # print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程执行了1ms')
#                 if (readyQueue[0][5] == 0):  # 修改第一次执行标记
#                     readyQueue[0][5] = 1
#                     startTime[readyQueue[0][0] - 1] = currentTime  # 记录这个job的开始时间，因为任务序号从1开始，所以减1
#                 if (readyQueue[0][2] == readyQueue[0][3]):  # 任务执行完毕
#                     # print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程完成了执行')
#
#                     execution[readyQueue[0][0] - 1] = readyQueue[0][3]
#                     preemptTime[readyQueue[0][0] - 1] = 1 + currentTime - startTime[readyQueue[0][0] - 1] - execution[
#                         readyQueue[0][0] - 1]
#                     inactive1[readyQueue[0][0] - 1] = readyQueue[0][4] + 1 - (
#                                 currentTime + 1 - startTime[readyQueue[0][0] - 1])
#                     taskPerformence[readyQueue[0][0] - 1].append(
#                         [inactive1[readyQueue[0][0] - 1] + inactive2[readyQueue[0][0] - 1],
#                          execution[readyQueue[0][0] - 1],
#                          preemptTime[readyQueue[0][0] - 1], readyQueue[0][1]])
#                     inactive2[readyQueue[0][0] - 1] = readyQueue[0][1] - (
#                                 1 + currentTime - startTime[readyQueue[0][0] - 1]) - inactive1[readyQueue[0][
#                                                                                                    0] - 1]  # 这个inactive2是当前job的，但是用于下一个job的故障概率计算，inactive2=周期-生命时长-inactive1
#                     del readyQueue[0]
#
#                     # 检查是否有已经开始执行的HI关键性任务需要抢占
#                     # hi_task_to_preempt = None
#                     # for i in range(len(readyQueue)):
#                     #     # 检查条件：已经开始执行过的HI关键性任务 (readyQueue[i][2] != 0 且 readyQueue[i][7] == 1)
#                     #     if readyQueue[i][2] != 0 and readyQueue[i][7] == 1:
#                     #         # 检查是否有绝对截止期比这个HI任务更早的任务
#                     #         has_earlier_deadline = False
#                     #         for j in range(len(readyQueue)):
#                     #             if j != i and readyQueue[j][6] < readyQueue[i][6]:
#                     #                 has_earlier_deadline = True
#                     #                 break
#                     #
#                     #         # 如果没有更早截止期的任务，则标记这个HI任务需要被处理
#                     #         if not has_earlier_deadline:
#                     #             hi_task_to_preempt = i
#                     #             break
#                     #
#                     # # 如果找到了符合条件的HI任务，将其移到队列最前面
#                     # if hi_task_to_preempt is not None:  # 在这里，不需要判断此时有无更高优先级job释放，因为在开头那里更新readyQueue后会判断一次并采取措施
#                     #     hi_task = readyQueue.pop(hi_task_to_preempt)
#                     #     readyQueue.insert(0, hi_task)
#
#             currentTime += 1
#             if readyQueue:
#                 if readyQueue[0][9] == 1:
#                     readyQueue[0][9] = 0
#
#             if no_response_flag > 0:
#                 no_response_flag -= 1
#                 if readyQueue:
#                     if (no_response_flag == 0):
#                         readyQueue[0][9] = 1
#             for i in readyQueue:
#                 i[4] += 1
#         number = 1
#         data1 = [None]
#         data2 = [None]
#         for records in taskPerformence:
#             if records:
#                 numbers = 1
#                 Task_Fault_Before_Mean = 0
#                 Task_Fault_After_Mean = 0
#                 for record in records:
#                     # print('第'+str(number)+'个任务的第'+str(numbers)+'个进程实例执行结果为：inactive:'+str(record[0])+' executionTime:'+str(record[1])+' ioTime:'
#                     # +str(record[2])+' preemptTime:'+str(record[3])+' Period:'+str(record[4]))
#                     Task_Fault_Before = Compute_Task_Fault_Before()
#                     Task_Fault_After = Compute_Task_Fault_After(record[2], record[1], record[0], record[3])
#                     task_PFH_list[number - 1] = Decimal(task_PFH_list[number - 1])
#                     task_PFH_list[number - 1] += Task_Fault_After
#                     Task_Fault_Before_Mean += Task_Fault_Before
#                     Task_Fault_After_Mean += Task_Fault_After
#                     numbers += 1
#
#                 all_Success_Instance_Number += (numbers - 1)
#                 Task_Fault_After_Mean = Task_Fault_After_Mean / (numbers - 1)
#                 Task_Fault_Before_Mean = Task_Fault_Before_Mean / (numbers - 1)
#                 data1.append(Task_Fault_Before_Mean)
#                 data2.append(Task_Fault_After_Mean)
#                 task_PFH_list[number - 1] /= (numbers - 1)
#                 number += 1
#
#         for records in taskPerformence:
#             records.clear()
#         for p in inactive2:
#             p = 0
#         numbers = 0
#         for task in tasks:
#             period = task[2]
#             task_PFH_list[numbers] = math.ceil(60 * 60 * 1000 / period) * task_PFH_list[numbers]
#             numbers += 1
#         batchNum += 1
#     sum1 = 0
#     sum1 = Decimal(sum1)
#     for i in task_PFH_list:
#         sum1 += Decimal(str(i))
#
#     success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))
#
#     return sum1 / 20, success_Instance_percent






from base import  *

Q_table = []  #Q表



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
        if qtime == -1:
            qtime = i[1]
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


def q_attribute_schedule(detailed_tasks,task_number):
    taskPerformence = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], [], []]
    faultRateBefore = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], [], []]
    faultRateAfter = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                      [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                      [], [], [], [], [], [], [], [], [], [], [], [], []]

    inactive1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    inactive2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0]
    execution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    preemptTime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    startTime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 非响应模式标记

    task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


    num = 0
    batchNum = 1
    superPeriod = 1

    all_Instance_Number = 0
    all_Success_Instance_Number = 0
    success_Instance_percent = 0.0
    success_Instance_percent = (str(success_Instance_percent))

    HI_task_count= 0

    preemptCount = 0

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
        # print('第'+str(num)+'批任务集开始模拟执行：')
        readyQueue = []
        currentTime = 0
        for task in tasks:
            readyQueue.append([task[0], task[2], 0, task[1], 0, 0 ,task[3] ,task[4] ,task[5]
                               ,0]  )# readyQueue对象(任务序号，周期，已执行时间，WCET，生命时长，第一次执行标记(为了检测startTime),绝对截止时间,关键性标记_1为HI_0为LOW,q属性,标记这个job是否刚结束非响应模式）

        no_response_flag = 0

        last_job=0

        just_finished = 0 #刚刚完成一个job的标记

        readyQueue.sort(key=lambda x: x[6])
        while currentTime < superPeriod:

            # if readyQueue:
            #     readyQueue3 = readyQueue.copy()
            #     readyQueue3.sort(key=lambda x: x[6] - currentTime)
            #     if (readyQueue3[0][0] != readyQueue[0][0]) & (readyQueue[0][2] != readyQueue[0][3]):
            #         preemptCount += 1

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
                        readyQueue.append \
                            ([task[0], task[2], 0, task[1], 0, 0, task[3] + currentTime ,task[4] ,task[5] ,0])

                if readyQueue:
                    if just_finished == 0:
                        if (no_response_flag == 0) & (readyQueue[0][9] == 0):  # 先看一下有没有发生低抢高
                            # print('111')
                            readyQueue2 = readyQueue.copy()
                            readyQueue2.sort(key=lambda x: x[6] - currentTime)
                            # print(readyQueue[0][0])
                            # print(readyQueue2[0][0])
                            # print(readyQueue[0][7])
                            # print(readyQueue2[0][7])
                            if (readyQueue[0][0] != readyQueue2[0][0]) & (readyQueue[0][7] == 1) & \
                                    (readyQueue2[0][7] == 0) & (readyQueue[0][5] == 1):  # 说明发生了关键性方面的低抢高
                                # print(readyQueue[0])
                                # print('here')
                                # print(currentTime)
                                no_response_flag = readyQueue[0][8]
                                no_response_flag = min(no_response_flag, readyQueue[0][3] - readyQueue[0][2])
                                # print('此时获得静态q属性')
                                # print(no_response_flag)
                                # if no_response_flag < (readyQueue[0][3] - readyQueue[0][2]):  # 静态属性不够
                                #     # print('静态q属性不够')
                                #     no_response_flag = query_Q_table(readyQueue[0][6] - currentTime)
                                #     no_response_flag = min(no_response_flag, readyQueue[0][3] - readyQueue[0][2])
                                #     if no_response_flag == -1:
                                #         no_response_flag = readyQueue[0][3] - readyQueue[0][2]
                just_finished = 0

                if no_response_flag == 0:  # 说明没有发生低抢高或不允许LAT运行
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
                # print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程执行了1ms')
                # if last_job != readyQueue[0][0]:
                #     print('在第' + str(currentTime) + 'ms，第' + str(readyQueue[0][0]) + '个任务的实例进程执行了1ms')
                #     last_job = readyQueue[0][0]
                if (readyQueue[0][5] == 0):  # 修改第一次执行标记
                    readyQueue[0][5] = 1
                    startTime[readyQueue[0][0] - 1] = currentTime  # 记录这个job的开始时间，因为任务序号从1开始，所以减1
                if (readyQueue[0][2] == readyQueue[0][3]):  # 任务执行完毕
                    # print('在第'+str(currentTime)+'ms，第'+str(readyQueue[0][0])+'个任务的实例进程完成了执行')

                    execution[readyQueue[0][0] - 1] = readyQueue[0][3]
                    preemptTime[readyQueue[0][0] - 1] = 1 + currentTime - startTime[readyQueue[0][0] - 1] - execution[
                        readyQueue[0][0] - 1]
                    inactive1[readyQueue[0][0] - 1] = readyQueue[0][4] + 1 - (
                                currentTime + 1 - startTime[readyQueue[0][0] - 1])
                    taskPerformence[readyQueue[0][0] - 1].append(
                        [inactive1[readyQueue[0][0] - 1] + inactive2[readyQueue[0][0] - 1],
                         execution[readyQueue[0][0] - 1],
                         preemptTime[readyQueue[0][0] - 1], readyQueue[0][1]])
                    inactive2[readyQueue[0][0] - 1] = readyQueue[0][1] - (
                                1 + currentTime - startTime[readyQueue[0][0] - 1]) - inactive1[readyQueue[0][
                                                                                                   0] - 1]  # 这个inactive2是当前job的，但是用于下一个job的故障概率计算，inactive2=周期-生命时长-inactive1
                    del readyQueue[0]
                    just_finished = 1
                    # # 检查是否有已经开始执行的HI关键性任务需要抢占
                    # hi_task_to_preempt = None
                    # for i in range(len(readyQueue)):
                    #     # 检查条件：已经开始执行过的HI关键性任务 (readyQueue[i][2] != 0 且 readyQueue[i][7] == 1)
                    #     if readyQueue[i][2] != 0 and readyQueue[i][7] == 1:
                    #         # 检查是否有绝对截止期比这个HI任务更早的任务
                    #         has_earlier_deadline = False
                    #         for j in range(len(readyQueue)):
                    #             if j != i and readyQueue[j][6] < readyQueue[i][6]:
                    #                 has_earlier_deadline = True
                    #                 break
                    #
                    #         # 如果没有更早截止期的任务，则标记这个HI任务需要被处理
                    #         if not has_earlier_deadline:
                    #             hi_task_to_preempt = i
                    #             break
                    #
                    # # 如果找到了符合条件的HI任务，将其移到队列最前面
                    # if hi_task_to_preempt is not None:  # 在这里，不需要判断此时有无更高优先级job释放，因为在开头那里更新readyQueue后会判断一次并采取措施
                    #     hi_task = readyQueue.pop(hi_task_to_preempt)
                    #     readyQueue.insert(0, hi_task)

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
                    # print('第'+str(number)+'个任务的第'+str(numbers)+'个进程实例执行结果为：inactive:'+str(record[0])+' executionTime:'+str(record[1])+' ioTime:'
                    # +str(record[2])+' preemptTime:'+str(record[3])+' Period:'+str(record[4]))
                    Task_Fault_Before = Compute_Task_Fault_Before()
                    Task_Fault_After = Compute_Task_Fault_After(record[2], record[1], record[0], record[3])
                    task_PFH_list[number - 1] = Decimal(task_PFH_list[number - 1])
                    task_PFH_list[number - 1] += Task_Fault_After
                    Task_Fault_Before_Mean += Task_Fault_Before
                    Task_Fault_After_Mean += Task_Fault_After
                    numbers += 1

                all_Success_Instance_Number += (numbers - 1)
                Task_Fault_After_Mean = Task_Fault_After_Mean / (numbers - 1)
                Task_Fault_Before_Mean = Task_Fault_Before_Mean / (numbers - 1)
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
            if task[4] == 1:
                period = task[2]
                task_PFH_list[numbers] = math.ceil(60 * 60 * 1000 / period) * task_PFH_list[numbers]
                numbers += 1
                HI_task_count += 1
            else:
                task_PFH_list[numbers] = 0
        batchNum += 1
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in task_PFH_list:
        sum1 += Decimal(str(i))

    success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))

    return sum1 /HI_task_count, success_Instance_percent
