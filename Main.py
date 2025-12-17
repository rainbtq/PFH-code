


from Scheduler import *




if __name__ == '__main__':

    task_number = 30    #每个任务集中任务的个数
    steps = 400   #每种利用率测试的任务集个数

    # i = 0
    # while i < 3:
    #     Scheduler(task_number, steps, 1)  # If_D_eq_T ==1 表示D=T
    #     i += 1
    #
    # i = 0
    # while i < 3:
    #     Scheduler(task_number, steps, 0)  # If_D_eq_T ==1 表示D=T
    #     i += 1
    #
    #
    #
    # task_number = 30
    #
    # i = 0
    # while i < 3:
    #     Scheduler(task_number, steps, 1)  # If_D_eq_T ==1 表示D=T
    #     i += 1
    #
    # i = 0
    # while i < 3:
    #     Scheduler(task_number, steps, 0)  # If_D_eq_T ==1 表示D=T
    #     i += 1





    Scheduler(task_number,steps,1)   #If_D_eq_T ==1 表示D=T
    Scheduler(task_number,steps,0)  #If_D_eq_T==0 表示D小于等于T

    # steps = 200
    #
    # Scheduler(task_number, steps, 1)  # If_D_eq_T ==1 表示D=T
    # Scheduler(task_number, steps, 0)  # If_D_eq_T==0 表示D小于等于T

    # task_number = 40  # 每个任务集中任务的个数
    #
    # Scheduler(task_number, steps, 1)  # If_D_eq_T ==1 表示D=T
    # Scheduler(task_number, steps, 0)  # If_D_eq_T==0 表示D小于等于T
   # Scheduler(task_number, steps, 1)  # If_D_eq_T ==1 表示D=T
    #tasks1 = [[[1, 1, 200, 200, 0], [2, 294, 800, 800, 0], [3, 422, 800, 800, 1]]]
    #tasks1 = get_Q_table_q_attribute(tasks1)
    #print(Q_table)
    #LAT_edf(tasks1)
    # print("LAT_EDF")
    # PFH1, GG = LAT_edf(tasks1)
    #
    #
    #
    # print("LAT_EDF_no_add")
    # PFH2,GG = LAT_edf_no_add(tasks1)
    #
    #
    #
    # print("q_attribute")
    # PFH3,GG = q_attribute_schedule(tasks1)
    #
    #
    #
    # print("Q_table")
    # PFH4, GG = Q_table_schedule(tasks1)
    # print(PFH1)
    # print(PFH2)
    # print(PFH3)
    # print(PFH4)

    # tasks1 = [[[1, 1, 4, 4, 0], [2, 4, 10, 10, 1], [3, 7, 20, 20, 1]]]
    #
    # print("LAT_EDF")
    # PFH1, GG = LAT_edf(tasks1)
    #
    #
    # print("q_attribute")
    # PFH3,GG = q_attribute_schedule(tasks1)
    #
    # print("Q_table")
    # PFH4, GG = Q_table_schedule(tasks1)
    #
    # print(PFH1)
    # print(PFH3)
    # print(PFH4)
