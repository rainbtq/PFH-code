





# 存放三种调度都需要的代码



from decimal import Decimal, getcontext
import math


getcontext().prec = 300  # 300位精度

# chaoShi = 0
batchNum = 0

CPU_Fault_Rate = 1e-4 # CPU故障率
MEM_Fault_Rate = 1e-4 # 内存故障率
Frequency = 1e6  #系统时钟频率

CPU_Fault_rate = 1-(1-CPU_Fault_Rate)**(1/(3600*Frequency))
CPU_Fault_rate = Decimal(str(CPU_Fault_rate))
MEM_Fault_rate = 1-(1-MEM_Fault_Rate)**(1/(3600*Frequency))
MEM_Fault_rate = Decimal(str(MEM_Fault_rate))
# print(CPU_Fault_rate)

MEM_Size = 1024 # 内存大小MB
Task_Size_inactive = 10 # 任务在两种情况下所占内存MB
Task_Size_active = 30

MEM_Size = Decimal(str(MEM_Size))
Task_Size_inactive = Decimal(str(Task_Size_inactive))
Task_Size_active = Decimal(str(Task_Size_active))

taskPerformence = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
faultRateBefore = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
faultRateAfter = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

inactive1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
inactive2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
execution = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
preemptTime = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
startTime = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]



def lcm(a,b):
    return abs(a*b) // math.gcd(a,b)




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
