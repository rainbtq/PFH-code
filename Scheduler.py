

from EDF_no_preempt import  *
from EDF_preempt import  *
from LAT_EDF import *
from TaskSet import *
from q_attribute import *
from Q_table import *
from LAT_EDF_no_add import *

import matplotlib.pyplot as plt

import os

import datetime

def Scheduler(task_number,steps,If_D_eq_T): # If_D_eq_T ==1 表示D=T If_D_eq_T==0 表示D小于等于T

    data1 = [None]  # EDF_no_preempt_PFH
    data2 = [None]  # EDF_preempt_PFH
    data3 = [None]  # LAT__PFH

    data4 = [None]  # upper_bound_failurePFH
    data5 = [None]  # failureMaxPFH

    data6 = [None]  # q_attribute_schedule_PFH
    data7 = [None]  # Q_table_schedule_PFH
    data8 = [None]  # LAT__PFH_no_add_PFH
    max_PFH = 0


    active_Time_EDF_preempt = [None]
    active_Time_EDF_no_preempt = [None]
    active_Time_LAT = [None]
    max_Active_Time = 0


    run_Time_q = [None]
    run_Time_Q = [None]
    run_Time_LAT = [None]
    max_Run_Time = 0

    preempt_Count_LAT = [None]
    preempt_Count_EDF = [None]
    preempt_Count_nopreEDF = [None]
    max_preempt_Count = 0


    success_Instance_percent_edf_preempt = 0
    success_Instance_percent_edf_preempt = Decimal(str(success_Instance_percent_edf_preempt))

    success_Instance_percent_edf_no_preempt = 0
    success_Instance_percent_edf_no_preempt = Decimal(str(success_Instance_percent_edf_no_preempt))

    success_Instance_percent_LAT = 0
    success_Instance_percent_LAT = Decimal(str(success_Instance_percent_LAT))

    success_Instance_percent_LAT_no_add = 0
    success_Instance_percent_LAT_no_add = Decimal(str(success_Instance_percent_LAT_no_add))

    success_Instance_percent_q_attribute_schedule = 0
    success_Instance_percent_q_attribute_schedule = Decimal(str(success_Instance_percent_q_attribute_schedule))

    success_Instance_percent_Q_table_schedule = 0
    success_Instance_percent_Q_table_schedule = Decimal(str(success_Instance_percent_Q_table_schedule))



    mean_Edf_preempt_PFH = 0
    mean_Edf_preempt_PFH = Decimal(str(mean_Edf_preempt_PFH))

    mean_Edf_no_preempt_PFH = 0
    mean_Edf_no_preempt_PFH = Decimal(str(mean_Edf_no_preempt_PFH))

    mean_LAT_PFH = 0
    mean_LAT_PFH = Decimal(str(mean_LAT_PFH))

    mean_LAT_PFH_no_add = 0
    mean_LAT_PFH_no_add = Decimal(str(mean_LAT_PFH_no_add))

    mean_q_attribute_PFH = 0
    mean_q_attribute_PFH = Decimal(str(mean_q_attribute_PFH))

    mean_Q_table_PFH = 0
    mean_Q_table_PFH = Decimal(str(mean_Q_table_PFH))

    mean_active_time_Edf_no_preempt = 0
    mean_active_time_Edf_no_preempt = Decimal(str(mean_active_time_Edf_no_preempt))

    mean_active_time_Edf_preempt = 0
    mean_active_time_Edf_preempt = Decimal(str(mean_active_time_Edf_preempt))

    mean_active_time_LAT = 0
    mean_active_time_LAT = Decimal(str(mean_active_time_LAT))


    # detailed_tasks = generate_task_details(
    #                  StaffordRandFixedSum(20, 0.5, 1), gen_periods_discrete(20, 1, [400,600,800,1000,1200]))


    #总的运行时间
    q_attribute_time = 0
    Q_table_time = 0
    LAT_EDF_time = 0
    LAT_EDF_no_add_time = 0

    uti = 0.10
    while uti <= 1.0:
        count1 = 1

        edf_preempt_PFH = 0
        edf_no_preempt_PFH = 0
        LAT_PFH = 0
        LAT_PFH_no_add = 0

        q_attribute_PFH = 0
        Q_table_PFH = 0

        upper_bound_failurePFH1 = 0  # 公式的理论最大值
        oldfailureMaxPFH1 = 0  # 未使用时间分配函数前的值

        edf_preempt_PFH = Decimal(str(edf_preempt_PFH))
        edf_no_preempt_PFH = Decimal(str(edf_no_preempt_PFH))
        LAT_PFH = Decimal(str(LAT_PFH))
        LAT_PFH_no_add = Decimal(str(LAT_PFH_no_add))

        q_attribute_PFH = Decimal(str(q_attribute_PFH))
        Q_table_PFH = Decimal(str(Q_table_PFH))

        upper_bound_failurePFH1 = Decimal(str(upper_bound_failurePFH1))
        oldfailureMaxPFH1 = Decimal(str(oldfailureMaxPFH1))

        oldfailureMaxPFH = 0
        inacFaultRate = 0
        exePreeFaultRate = 0
        upper_bound_failurePFH = 0

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

        success_Instance_percent_LAT1_no_add = 0
        success_Instance_percent_LAT1_no_add = Decimal(str(success_Instance_percent_LAT1_no_add))


        success_Instance_percent_q_attribute_schedule1 = 0
        success_Instance_percent_q_attribute_schedule1 = Decimal(str(success_Instance_percent_q_attribute_schedule1))

        success_Instance_percent_Q_table_schedule1 = 0
        success_Instance_percent_Q_table_schedule1 = Decimal(str(success_Instance_percent_Q_table_schedule1))

        mean_active_time_Edf_no_preempt1 = 0
        mean_active_time_Edf_no_preempt1 = Decimal(str(mean_active_time_Edf_no_preempt1))

        mean_active_time_Edf_preempt1 = 0
        mean_active_time_Edf_preempt1 = Decimal(str(mean_active_time_Edf_preempt1))

        mean_active_time_LAT1 = 0
        mean_active_time_LAT1 = Decimal(str(mean_active_time_LAT1))


        mean_preempt_Count_LAT1 = 0
        mean_preempt_Count_LAT1= Decimal(str(mean_preempt_Count_LAT1))
        mean_preempt_Count_EDF1 = 0
        mean_preempt_Count_EDF1 = Decimal(str(mean_preempt_Count_EDF1))
        mean_preempt_Count_nopreEDF1 = 0
        mean_preempt_Count_nopreEDF1 = Decimal(str(mean_preempt_Count_nopreEDF1))


        #单个利用率下的平均运行时间(us)
        q_attribute_time1 = 0
        Q_table_time1 = 0
        LAT_EDF_time1 = 0






        while count1 <= steps:
            checkk = 0
            detailed_tasks = []
            while checkk == 0:
                detailed_tasks = generate_task_details(
                    UUniFastDiscard(task_number, uti, 1),
                    gen_periods_discrete(task_number, 1, [50, 100, 200, 400, 800, 1000, 2000, 4000]),If_D_eq_T)
                for j in detailed_tasks:
                    utii = 0.0
                    for i in j:
                        utii += i[1]/i[2]
                    # if (abs(utii-uti) < 0.01) & (utii < uti):
                    print(utii)
                    if (abs(utii-uti) < 0.1) & (utii < uti):
                        # print("ok")
                        checkk = 1
            # [180,192,200,216,225,240]
            # [375,400,432,450,480,500]
            # [50, 80, 100, 200, 400, 800, 1000]
            # [400, 420, 440, 460, 480, 500]
            # while checkk == 0:
            #     detailed_tasks = generate_task_details(
            #         StaffordRandFixedSum(task_number, uti, 1),
            #         gen_periods_discrete(task_number, 1, [10, 20, 40, 50, 80, 100, 200, 400, 800,4000]),If_D_eq_T)
            #     for j in detailed_tasks:
            #         utii = 0.0
            #         for i in j:
            #             utii += i[1]/i[2]
            #         if (abs(utii-uti) < 0.001) & (utii < uti):
            #             checkk = 1
            # print("任务集是：")
            # print(detailed_tasks)

            for i in detailed_tasks:  # 计算一下理论上限和旧方法计算值

                for j in i:
                    preTime1 = j[2] - j[1]
                    exeTime1 = j[1]
                    inacTime1 = j[2] - j[1]
                    period1 = j[2]

                    preTime1 = Decimal(str(preTime1))
                    exeTime1 = Decimal(str(exeTime1))
                    inacTime1 = Decimal(str(inacTime1))
                    period1 = Decimal(str(period1))

                    oldfailureMaxPFH11 = 1 - (1 - CPU_Fault_rate) * (1 - Task_Size_inactive / MEM_Size * MEM_Fault_rate)
                    oldfailureMaxPFH += math.ceil(60 * 60 * 1000 / period1) * oldfailureMaxPFH11
                    inacFaultRate = 1 - (1 - Task_Size_inactive / MEM_Size * MEM_Fault_rate) ** (inacTime1 / period1)
                    exePreeFaultRate = 1 - (
                                (1 - CPU_Fault_rate) * (1 - Task_Size_active / MEM_Size * MEM_Fault_rate)) ** \
                                       ((exeTime1 + preTime1) / period1)
                    upper_bound_failurePFH11 = 1 - (1 - inacFaultRate) * (1 - exePreeFaultRate)
                    upper_bound_failurePFH += math.ceil(60 * 60 * 1000 / period1) * upper_bound_failurePFH11

                oldfailureMaxPFH /= task_number  # 因为任务集里有task_number个任务
                upper_bound_failurePFH /= task_number

                oldfailureMaxPFH1 += oldfailureMaxPFH
                upper_bound_failurePFH1 += upper_bound_failurePFH

            backNum = 0.0
            backNum = Decimal(str(backNum))

            backNum1 = 0.0
            backNum1 = Decimal(str(backNum1))

            mean_active_time_Edf_no_preempt1 = 0

            mean_active_time_Edf_preempt1 = 0

            mean_active_time_LAT1 = 0

            mean_preempt_Count_LAT1 = 0

            mean_preempt_Count_EDF1 = 0

            mean_preempt_Count_nopreEDF1 = 0



            backNum, backNum1, time1, count2 = edf_preempt(detailed_tasks,task_number)
            edf_preempt_PFH += backNum
            success_Instance_percent_edf_preempt1 += backNum1
            mean_active_time_Edf_preempt1 += time1
            mean_preempt_Count_EDF1 += count2


            backNum, backNum1 , time1, count2= edf_no_preempt(detailed_tasks,task_number)
            edf_no_preempt_PFH += backNum
            success_Instance_percent_edf_no_preempt1 += backNum1
            mean_active_time_Edf_no_preempt1 += time1
            mean_preempt_Count_nopreEDF1 += count2



            starttime = datetime.datetime.now()
            backNum, backNum1 , time1, count2= LAT_edf(detailed_tasks,task_number)
            LAT_PFH += backNum
            success_Instance_percent_LAT1 += backNum1
            endtime = datetime.datetime.now()
            LAT_EDF_time1 += (endtime - starttime).microseconds
            LAT_EDF_time += (endtime - starttime).microseconds
            mean_active_time_LAT1 += time1
            mean_preempt_Count_LAT1 += count2


            # starttime = datetime.datetime.now()
            # backNum, backNum1 = LAT_edf_no_add(detailed_tasks,task_number)
            # LAT_PFH_no_add += backNum
            # success_Instance_percent_LAT1_no_add += backNum1
            # endtime = datetime.datetime.now()
            # LAT_EDF_no_add_time += (endtime - starttime).microseconds







            starttime = datetime.datetime.now()
            backNum, backNum1 = q_attribute_schedule(detailed_tasks,task_number)
            q_attribute_PFH += backNum
            success_Instance_percent_q_attribute_schedule1 += backNum1
            endtime = datetime.datetime.now()
            q_attribute_time1 += (endtime - starttime).microseconds
            q_attribute_time += (endtime - starttime).microseconds




            starttime = datetime.datetime.now()
            backNum, backNum1 = Q_table_schedule(detailed_tasks,task_number)
            Q_table_PFH += backNum
            success_Instance_percent_Q_table_schedule1 += backNum1
            endtime = datetime.datetime.now()
            Q_table_time1 += (endtime - starttime).microseconds
            Q_table_time += (endtime - starttime).microseconds





            str22 = '轮次：'
            #print('轮次：')
           # print(count1)
            str22 = f"{str22}{count1}"
            #str22 += str(count1)
            str22 += '/'
            str22 = f"{str22}{steps}"
            #str22 += str(steps)
            print(str22)

            count1 += 1
            # print('uti:')
            # print(uti)



        edf_preempt_PFH /= steps  # 除以任务集的个数
        edf_no_preempt_PFH /= steps
        LAT_PFH /= steps
        LAT_PFH_no_add /= steps

        q_attribute_PFH /= steps
        Q_table_PFH /= steps
        upper_bound_failurePFH1 /= steps
        oldfailureMaxPFH1 /= steps

        data1.append(edf_no_preempt_PFH)
        data2.append(edf_preempt_PFH)
        data3.append(LAT_PFH)
        data4.append(upper_bound_failurePFH1)
        data5.append(oldfailureMaxPFH1)

        data6.append(q_attribute_PFH)
        data7.append(Q_table_PFH)

        data8.append(LAT_PFH_no_add)

        max_PFH = max(edf_no_preempt_PFH,max_PFH)
        max_PFH = max(edf_preempt_PFH, max_PFH)
        max_PFH = max(LAT_PFH, max_PFH)
        max_PFH = max(q_attribute_PFH, max_PFH)
        max_PFH = max(Q_table_PFH, max_PFH)


        success_Instance_percent_edf_preempt1 /= steps  # 除以任务集的个数
        success_Instance_percent_edf_no_preempt1 /= steps
        success_Instance_percent_LAT1 /= steps
        success_Instance_percent_LAT1_no_add /= steps

        success_Instance_percent_q_attribute_schedule1 /= steps
        success_Instance_percent_Q_table_schedule1 /= steps


        mean_active_time_Edf_no_preempt1 /= steps
        mean_active_time_Edf_preempt1 /= steps
        mean_active_time_LAT1 /= steps

        # mean_preempt_Count_LAT1 /= steps
        #
        # mean_preempt_Count_EDF1 /= steps
        #
        # mean_preempt_Count_nopreEDF1 /= steps


        active_Time_EDF_preempt.append(mean_active_time_Edf_preempt1)
        active_Time_EDF_no_preempt.append(mean_active_time_Edf_no_preempt1)
        active_Time_LAT.append(mean_active_time_LAT1)

        preempt_Count_LAT.append(mean_preempt_Count_LAT1)
        preempt_Count_EDF.append(mean_preempt_Count_EDF1)
        preempt_Count_nopreEDF.append(mean_preempt_Count_nopreEDF1)

        max_preempt_Count = max(max_preempt_Count, mean_preempt_Count_LAT1)
        max_preempt_Count = max(max_preempt_Count, mean_preempt_Count_EDF1)
        max_preempt_Count = max(max_preempt_Count, mean_preempt_Count_nopreEDF1)


        max_Active_Time = max(max_Active_Time,mean_active_time_Edf_no_preempt1)
        max_Active_Time = max(max_Active_Time, mean_active_time_Edf_preempt1)
        max_Active_Time = max(max_Active_Time, mean_active_time_LAT1)



        q_attribute_time1 /= steps
        Q_table_time1 /= steps
        LAT_EDF_time1 /= steps

        max_Run_Time = max(max_Run_Time,q_attribute_time1)
        max_Run_Time = max(max_Run_Time, Q_table_time1)
        max_Run_Time = max(max_Run_Time, LAT_EDF_time1)


        run_Time_q.append(q_attribute_time1)
        run_Time_Q.append(Q_table_time1)
        run_Time_LAT.append(LAT_EDF_time1)


        success_Instance_percent_edf_preempt += success_Instance_percent_edf_preempt1
        success_Instance_percent_edf_no_preempt += success_Instance_percent_edf_no_preempt1
        success_Instance_percent_LAT += success_Instance_percent_LAT1
        success_Instance_percent_LAT_no_add += success_Instance_percent_LAT1_no_add

        success_Instance_percent_q_attribute_schedule += success_Instance_percent_q_attribute_schedule1
        success_Instance_percent_Q_table_schedule += success_Instance_percent_Q_table_schedule1

        mean_active_time_Edf_no_preempt += mean_active_time_Edf_no_preempt1
        mean_active_time_Edf_preempt += mean_active_time_Edf_preempt1
        mean_active_time_LAT += mean_active_time_LAT1



        mean_Edf_preempt_PFH += edf_preempt_PFH
        mean_Edf_no_preempt_PFH += edf_no_preempt_PFH
        mean_LAT_PFH += LAT_PFH
        mean_LAT_PFH_no_add += LAT_PFH_no_add

        mean_q_attribute_PFH += q_attribute_PFH
        mean_Q_table_PFH += Q_table_PFH




        print('uti:')
        print(uti)
        uti = round(uti + 0.10, 2)

    # 利用率共10种

    success_Instance_percent_edf_preempt /= 10
    success_Instance_percent_edf_no_preempt /= 10
    success_Instance_percent_LAT /= 10
    success_Instance_percent_LAT_no_add /= 10

    success_Instance_percent_q_attribute_schedule /= 10
    success_Instance_percent_Q_table_schedule /= 10

    mean_active_time_Edf_no_preempt /=  10  #activeTime加到这里
    mean_active_time_Edf_preempt /=  10
    mean_active_time_LAT /=  10

    # print(success_Instance_percent_edf_preempt)
    # print(success_Instance_percent_edf_no_preempt)
    # print(success_Instance_percent_LAT)

    mean_Edf_preempt_PFH /= 10
    mean_Edf_no_preempt_PFH /= 10
    mean_LAT_PFH /= 10
    mean_LAT_PFH_no_add /= 10

    mean_q_attribute_PFH /= 10
    mean_Q_table_PFH /= 10


    # print(mean_Edf_preempt_PFH)
    # print(mean_Edf_no_preempt_PFH)
    # print(mean_LAT_PFH)

    # print('六种平均完成率：')
    #
    # print('success_Instance_percent_edf_preempt:')
    # print(success_Instance_percent_edf_preempt)
    # print('success_Instance_percent_edf_no_preempt:')
    # print(success_Instance_percent_edf_no_preempt)
    # print('success_Instance_percent_LAT:')
    # print(success_Instance_percent_LAT)
    # print('success_Instance_percent_LAT_no_add:')
    # print(success_Instance_percent_LAT_no_add)
    #
    # print('success_Instance_percent_q_attribute_schedule:')
    # print(success_Instance_percent_q_attribute_schedule)
    # print('success_Instance_percent_Q_table_schedule:')
    # print(success_Instance_percent_Q_table_schedule)
    #
    #
    #
    #
    # print('六种平均故障率：')
    # print('mean_Edf_preempt_PFH:')
    # print(mean_Edf_preempt_PFH)
    # print('mean_Edf_no_preempt_PFH:')
    # print(mean_Edf_no_preempt_PFH)
    # print('mean_LAT_PFH:')
    # print(mean_LAT_PFH)
    # print('mean_LAT_PFH_no_add:')
    # print(mean_LAT_PFH_no_add)
    #
    # print('mean_q_attribute_PFH:')
    # print(mean_q_attribute_PFH)
    # print('mean_Q_table_PFH:')
    # print(mean_Q_table_PFH)
    #
    #
    #
    # print("四种算法运行时间：")
    # print('q_attribute_time:')
    # print(q_attribute_time / 1000)
    # print('Q_table_time:')
    # print(Q_table_time / 1000)
    # print('LAT_EDF_time:')
    # print(LAT_EDF_time / 1000)
    # print('LAT_EDF_no_add_time:')
    # print(LAT_EDF_no_add_time / 1000)
    #
    #
    #
    # print("三种平均activeTime:")
    # print("mean_active_time_Edf_no_preempt:")
    # print(mean_active_time_Edf_no_preempt)
    # print("mean_active_time_Edf_preempt:")
    # print(mean_active_time_Edf_preempt)
    # print("mean_active_time_LAT:")
    # print(mean_active_time_LAT)
    #
    #
    # print('10种利用率下的LAT_PFH:')
    # print(data3)
    #
    # print('10种利用率下的LAT_PFH_no_add:')
    # print(data8)
    #
    # print('10种利用率下的q_attribute_PFH:')
    # print(data6)
    #
    # print('10种利用率下的Q_table_PFH:')
    # print(data7)







    # 接下来显示利用率从0.1到1的各种调度策略PFH
    plt.figure(figsize=(20, 15))

    x_ticks = [i * 0.10 for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]  # 10 个点

    x_data = x_ticks[0:11]

    # 增大坐标轴标签和刻度字体

    #plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

    plt.xlabel("Utilizations", fontsize=30)  # 横坐标轴标签（如果未设置，可以去掉）
    plt.ylabel("PFH", fontsize=30)  # 纵坐标轴标签（如果未设置，可以去掉）


    plt.plot(x_data, data1[0:11], label='EDF_no_preempt_PFH', marker='.', color='r')  # 只取前 11 个点
    plt.plot(x_data, data2[0:11], label='EDF_preempt_PFH', marker='.', color='b')
    plt.plot(x_data, data3[0:11], label='LAT-EDF_PFH', marker='.', color='g')
    #plt.plot(x_data, data4[0:11], label='upper_bound_PFH', marker='.', color='c')
    #plt.plot(x_data, data5[0:11], label='failureMaxPFH', marker='.', color='m')
    plt.plot(x_data, data6[0:11], label='q_attribute_PFH', marker='*', color='y', markersize=15)
    plt.plot(x_data, data7[0:11], label='Q_table_PFH', marker='+', color='k', markersize=15)
    #plt.plot(x_data, data8[0:11], label='LAT-EDF_PFH_no_add', marker='+', color='orange', markersize=15)

    plt.xticks(x_ticks, [f"{x:.2f}" for x in x_ticks], fontsize=30, rotation=45)
    plt.yticks(fontsize=40)  # 纵坐标刻度字体大小
    # x_ticks = [i * 0.05 for i in range(1, 21)]
    plt.xlim([0, 1.05])
    plt.ylim([0, float(max_PFH)*1.25])
    plt.grid(True, linestyle='--')

    # plt.legend(loc=9, fontsize=40)  # fontsize 控制图例字体大小
    plt.legend(fontsize=26, loc='upper right', ncol=2)  # 调整字体大小和位置

    # 创建结果文件夹
    current_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(current_dir, 'PFH_Result')
    if If_D_eq_T:
        result_dir = os.path.join(current_dir, 'PFH_Result1')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # 生成带时间戳的文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"PFH_comparison_{timestamp}.png"
    save_path = os.path.join(result_dir, filename)

    # 保存图片
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()




    # 文件名（固定，每次运行都会追加）
    filename = "PFH_Result/experiment_results.txt"
    if If_D_eq_T:
        filename = "PFH_Result1/experiment_results.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # 打开文件，以追加模式写入
    with open(filepath, 'a', encoding='utf-8') as f:

        # 写入10种利用率下的数据
        f.write(timestamp+'\n')
        f.write('\n')

        f.write("【10种利用率下的EDF_no_preempt_PFH】\n")
        f.write("-" * 40 + "\n")
        if hasattr(data1, '__len__'):
            for i, value in enumerate(data1):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{data1}\n")


        f.write("【10种利用率下的EDF_preempt_PFH】\n")
        f.write("-" * 40 + "\n")
        if hasattr(data2, '__len__'):
            for i, value in enumerate(data2):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{data2}\n")
        f.write("\n")

        f.write("【10种利用率下的LAT-EDF_PFH】\n")
        f.write("-" * 40 + "\n")
        # 假设data3是列表或数组，格式化输出
        if hasattr(data3, '__len__'):
            for i, value in enumerate(data3):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{data3}\n")
        f.write("\n")


        f.write("【10种利用率下的q_attribute_PFH】\n")
        f.write("-" * 40 + "\n")
        if hasattr(data6, '__len__'):
            for i, value in enumerate(data6):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{data6}\n")
        f.write("\n")

        f.write("【10种利用率下的Q_table_PFH】\n")
        f.write("-" * 40 + "\n")
        if hasattr(data7, '__len__'):
            for i, value in enumerate(data7):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{data7}\n")


        # 写入空行分隔
        f.write("\n\n")




    # plt.clf()
    #
    #
    #
    # # 接下来显示利用率从0.1到1的三种调度策略activeTime
    # plt.figure(figsize=(20, 15))
    #
    # x_ticks = [i * 0.10 for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]  # 10 个点
    #
    # x_data = x_ticks[0:11]
    #
    # # 增大坐标轴标签和刻度字体
    #
    # #plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    # plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
    #
    # plt.xlabel("Utilizations", fontsize=30)  # 横坐标轴标签（如果未设置，可以去掉）
    # plt.ylabel("active_Time", fontsize=30)  # 纵坐标轴标签（如果未设置，可以去掉）
    #
    # plt.plot(x_data, active_Time_EDF_no_preempt[0:11], label='EDF_no_preempt', marker='.', color='r')  # 只取前 11 个点
    # plt.plot(x_data, active_Time_EDF_preempt[0:11], label='EDF_preempt', marker='.', color='b')
    # plt.plot(x_data, active_Time_LAT[0:11], label='LAT_EDF', marker='.', color='g')
    #
    #
    # plt.xticks(x_ticks, [f"{x:.2f}" for x in x_ticks], fontsize=30, rotation=45)
    # plt.yticks(fontsize=40)  # 纵坐标刻度字体大小
    # # x_ticks = [i * 0.05 for i in range(1, 21)]
    # plt.xlim([0, 1.05])
    # plt.ylim([0, float(max_Active_Time)*1.25])
    # plt.grid(True, linestyle='--')
    #
    # # plt.legend(loc=9, fontsize=40)  # fontsize 控制图例字体大小
    # plt.legend(fontsize=26, loc='upper right', ncol=2)  # 调整字体大小和位置
    #
    # # 创建结果文件夹
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # result_dir = os.path.join(current_dir, 'active_Time_Result')
    # if If_D_eq_T:
    #     result_dir = os.path.join(current_dir, 'active_Time_Result1')
    #
    # if not os.path.exists(result_dir):
    #     os.makedirs(result_dir)
    #
    # # 生成带时间戳的文件名
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"PFH_comparison_{timestamp}.png"
    # save_path = os.path.join(result_dir, filename)
    #
    # # 保存图片
    # plt.savefig(save_path, dpi=300, bbox_inches='tight')
    # plt.close()
    #
    #
    #
    # # 文件名（固定，每次运行都会追加）
    # filename = "active_Time_Result/experiment_results.txt"
    # if If_D_eq_T:
    #     filename = "active_Time_Result1/experiment_results.txt"
    # filepath = os.path.join(os.path.dirname(__file__), filename)
    #
    # # 打开文件，以追加模式写入
    # with open(filepath, 'a', encoding='utf-8') as f:
    #
    #     # 写入10种利用率下的数据
    #     f.write(timestamp + '\n')
    #     f.write('\n')
    #
    #     f.write("【10种利用率下的EDF_no_preempt_active_time】\n")
    #     f.write("-" * 40 + "\n")
    #     if hasattr(active_Time_EDF_no_preempt, '__len__'):
    #         for i, value in enumerate(active_Time_EDF_no_preempt):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{active_Time_EDF_no_preempt}\n")
    #
    #     f.write("【10种利用率下的EDF_preempt_active_time】\n")
    #     f.write("-" * 40 + "\n")
    #     if hasattr(active_Time_EDF_preempt, '__len__'):
    #         for i, value in enumerate(active_Time_EDF_preempt):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{active_Time_EDF_preempt}\n")
    #     f.write("\n")
    #
    #     f.write("【10种利用率下的LAT-EDF_active_time】\n")
    #     f.write("-" * 40 + "\n")
    #     # 假设data3是列表或数组，格式化输出
    #     if hasattr(active_Time_LAT, '__len__'):
    #         for i, value in enumerate(active_Time_LAT):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{active_Time_LAT}\n")
    #     f.write("\n")
    #
    #     # 写入空行分隔
    #     f.write("\n\n")
    #
    #
    #

    # plt.clf()
    #
    #
    #
    #
    # # 接下来显示利用率从0.1到1的三种调度策略的runtime
    # plt.figure(figsize=(20, 15))
    #
    # x_ticks = [i * 0.10 for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]  # 10 个点
    #
    # x_data = x_ticks[0:11]
    #
    # # 增大坐标轴标签和刻度字体
    #
    # #plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    # plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    # plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
    #
    # plt.xlabel("Utilizations", fontsize=30)  # 横坐标轴标签（如果未设置，可以去掉）
    # plt.ylabel("runtime(ms)", fontsize=30)  # 纵坐标轴标签（如果未设置，可以去掉）
    #
    # plt.plot(x_data, run_Time_q[0:11], label='q_attribute', marker='.', color='r')  # 只取前 11 个点
    # plt.plot(x_data, run_Time_Q[0:11], label='Q_table', marker='.', color='b')
    # plt.plot(x_data, run_Time_LAT[0:11], label='LAT', marker='.', color='g')
    #
    # plt.xticks(x_ticks, [f"{x:.2f}" for x in x_ticks], fontsize=30, rotation=45)
    # plt.yticks(fontsize=40)  # 纵坐标刻度字体大小
    # # x_ticks = [i * 0.05 for i in range(1, 21)]
    # plt.xlim([0, 1.05])
    # plt.ylim([0, max_Run_Time*1.25])
    # plt.grid(True, linestyle='--')
    #
    # # plt.legend(loc=9, fontsize=40)  # fontsize 控制图例字体大小
    # plt.legend(fontsize=26, loc='upper right', ncol=2)  # 调整字体大小和位置
    #
    # # 创建结果文件夹
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # result_dir = os.path.join(current_dir, 'run_Time_Result')
    #
    # if If_D_eq_T:
    #     result_dir = os.path.join(current_dir, 'run_Time_Result1')
    #
    # if not os.path.exists(result_dir):
    #     os.makedirs(result_dir)
    #
    # # 生成带时间戳的文件名
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"PFH_comparison_{timestamp}.png"
    # save_path = os.path.join(result_dir, filename)
    #
    # # 保存图片
    # plt.savefig(save_path, dpi=300, bbox_inches='tight')
    # plt.close()
    # # 文件名（固定，每次运行都会追加）
    # filename = "run_Time_Result/experiment_results.txt"
    # if If_D_eq_T:
    #     filename = "run_Time_Result1/experiment_results.txt"
    # filepath = os.path.join(os.path.dirname(__file__), filename)
    #
    # # 打开文件，以追加模式写入
    # with open(filepath, 'a', encoding='utf-8') as f:
    #
    #     # 写入10种利用率下的数据
    #     f.write(timestamp + '\n')
    #     f.write('\n')
    #
    #     f.write("【10种利用率下的run_Time_q】\n")
    #     f.write("-" * 40 + "\n")
    #     if hasattr(run_Time_q, '__len__'):
    #         for i, value in enumerate(run_Time_q):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{run_Time_q}\n")
    #
    #     f.write("【10种利用率下的run_Time_Q】\n")
    #     f.write("-" * 40 + "\n")
    #     if hasattr(run_Time_Q, '__len__'):
    #         for i, value in enumerate(run_Time_Q):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{run_Time_Q}\n")
    #     f.write("\n")
    #
    #     f.write("【10种利用率下的run_Time_LAT】\n")
    #     f.write("-" * 40 + "\n")
    #     # 假设data3是列表或数组，格式化输出
    #     if hasattr(run_Time_LAT, '__len__'):
    #         for i, value in enumerate(run_Time_LAT):
    #             f.write(f"  利用率{i + 1}: {value}\n")
    #     else:
    #         f.write(f"{run_Time_LAT}\n")
    #     f.write("\n")
    #
    #     # 写入空行分隔
    #     f.write("\n\n")
    #

    plt.clf()


    # 接下来显示利用率从0.1到1的两种调度策略的抢占次数
    plt.figure(figsize=(20, 15))

    x_ticks = [i * 0.10 for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]  # 10 个点

    x_data = x_ticks[0:11]

    # 增大坐标轴标签和刻度字体

    #plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

    plt.xlabel("Utilizations", fontsize=30)  # 横坐标轴标签（如果未设置，可以去掉）
    plt.ylabel("preempt_count", fontsize=30)  # 纵坐标轴标签（如果未设置，可以去掉）

    # plt.plot(x_data, preempt_Count_nopreEDF[0:11], label='EDF_no_preempt', marker='.', color='r')  # 只取前 11 个点
    plt.plot(x_data, preempt_Count_EDF[0:11], label='EDF_preempt', marker='.', color='b')
    plt.plot(x_data, preempt_Count_LAT[0:11], label='LAT_EDF', marker='.', color='g')



    plt.xticks(x_ticks, [f"{x:.2f}" for x in x_ticks], fontsize=30, rotation=45)
    plt.yticks(fontsize=40)  # 纵坐标刻度字体大小
    # x_ticks = [i * 0.05 for i in range(1, 21)]
    plt.xlim([0, 1.05])
    plt.ylim([0, float(max_preempt_Count)*1.25])
    plt.grid(True, linestyle='--')

    # plt.legend(loc=9, fontsize=40)  # fontsize 控制图例字体大小
    plt.legend(fontsize=26, loc='upper right', ncol=2)  # 调整字体大小和位置

    # 创建结果文件夹
    current_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(current_dir, 'preempt_Count')
    if If_D_eq_T:
        result_dir = os.path.join(current_dir, 'preempt_Count1')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # 生成带时间戳的文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"preempt_Count_comparison_{timestamp}.png"
    save_path = os.path.join(result_dir, filename)

    # 保存图片
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()



    # 文件名（固定，每次运行都会追加）
    filename = "preempt_Count/experiment_results.txt"
    if If_D_eq_T:
        filename = "preempt_Count1/experiment_results.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # 打开文件，以追加模式写入
    with open(filepath, 'a', encoding='utf-8') as f:

        # 写入10种利用率下的数据
        f.write(timestamp + '\n')
        f.write('\n')

        # f.write("【10种利用率下的preempt_Count_nopreEDF】\n")
        # f.write("-" * 40 + "\n")
        # if hasattr(preempt_Count_nopreEDF, '__len__'):
        #     for i, value in enumerate(preempt_Count_nopreEDF):
        #         f.write(f"  利用率{i + 1}: {value}\n")
        # else:
        #     f.write(f"{preempt_Count_nopreEDF}\n")

        f.write("【10种利用率下的preempt_Count_EDF】\n")
        f.write("-" * 40 + "\n")
        if hasattr(preempt_Count_EDF, '__len__'):
            for i, value in enumerate(preempt_Count_EDF):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{preempt_Count_EDF}\n")
        f.write("\n")

        f.write("【10种利用率下的preempt_Count_LAT】\n")
        f.write("-" * 40 + "\n")
        # 假设data3是列表或数组，格式化输出
        if hasattr(preempt_Count_LAT, '__len__'):
            for i, value in enumerate(preempt_Count_LAT):
                f.write(f"  利用率{i + 1}: {value}\n")
        else:
            f.write(f"{preempt_Count_LAT}\n")
        f.write("\n")

        # 写入空行分隔
        f.write("\n\n")





    # print(run_Time_q)
    # print(run_Time_Q)
    # print(run_Time_LAT)
    #print(f"图片已保存到: {save_path}")
    #str1 = 'E:/Research/毕设/resultPicture2/单像图1e-6.png'
    # plt.title('各种调度策略在不同利用率下的故障率及上限', fontsize=35, fontweight='bold')
    #plt.savefig(str1)

    # print(len(data7))
    # data1.append(edf_no_preempt_PFH)
    # data2.append(edf_preempt_PFH)
    # data3.append(LAT_PFH)
    # data4.append(upper_bound_failurePFH1)
    # data5.append(oldfailureMaxPFH1)
    #
    # data6.append(q_attribute_PFH)
    # data7.append(Q_table_PFH)
