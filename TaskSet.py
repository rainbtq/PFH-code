


import random
import numpy as np



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




def generate_task_details(utilizations, periods,If_D_eq_T): #生成任务集,
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
            if If_D_eq_T:    #D = T
                deadline = period
            else:            #D ＜＝ T
                deadline = random.randint(wcet, period)
            random_attr = random.randint(0, 1)  # 随机生成0或1
            if period >= 400:
                random_attr = 1
            else:
                random_attr = 0
            task_group.append([num, wcet, period, deadline,random_attr])
            num += 1
        detailed_tasks.append(task_group)

    return detailed_tasks



