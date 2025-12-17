




from base import  *








def edf_preempt(detailed_tasks,task_number):
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

    task_PFH_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    task_activeTime_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0,
                            0.0, 0.0]

    num = 0
    batchNum = 1
    superPeriod = 1

    all_Instance_Number = 0
    all_Success_Instance_Number = 0
    success_Instance_percent = 0.0
    success_Instance_percent = (str(success_Instance_percent))

    HI_task_count = 0

    preemptCount = 0

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

                if readyQueue:
                    readyQueue3 = readyQueue.copy()
                    readyQueue3.sort(key=lambda x: x[6] - currentTime)
                    if (readyQueue3[0][0] != readyQueue[0][0]) & (readyQueue[0][2] != readyQueue[0][3]):
                        preemptCount += 1

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

                    task_activeTime_list[number - 1] = task_activeTime_list[number - 1]
                    task_activeTime_list[number - 1] += record[2] + record[1]

                    Task_Fault_Before_Mean += Task_Fault_Before
                    Task_Fault_After_Mean += Task_Fault_After
                    numbers += 1

                all_Success_Instance_Number += (numbers - 1)
                Task_Fault_After_Mean = Task_Fault_After_Mean/(numbers-1)
                Task_Fault_Before_Mean = Task_Fault_Before_Mean/(numbers-1)
                data1.append(Task_Fault_Before_Mean)
                data2.append(Task_Fault_After_Mean)
                task_PFH_list[number - 1] /= (numbers - 1)
                task_activeTime_list[number - 1] /= (numbers - 1)
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
                task_activeTime_list[numbers] = 0
    batchNum += 1
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in task_PFH_list:
        sum1 += Decimal(str(i))

    sum2 = 0
    sum2 = Decimal(sum2)
    for i in task_activeTime_list:
        sum2 += Decimal(str(i))

    success_Instance_percent = Decimal(str(all_Success_Instance_Number / all_Instance_Number))

    return sum1 / HI_task_count,success_Instance_percent,sum2 / HI_task_count, preemptCount
