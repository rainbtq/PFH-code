import random
import numpy as np
import math
from decimal import Decimal, getcontext

# 设置300位精度
getcontext().prec = 300

# 任务
class Task:
    def __init__(self, task_id, deadline, period, wcet, criticality, pfh, q, active_time, response_time):
        self.Task_id = task_id                                  # 任务的id
        self.Task_deadline = deadline                           # 任务的相对截止期
        self.Task_period = period                               # 任务的周期
        self.Task_wcet = wcet                                   # 任务的执行时间
        self.Task_criticality = criticality                     # 任务的临界性（0表示低关键性，1表示高关键性）
        self.Task_pfh = pfh                                     # 任务的PFH
        self.Task_q = q                                         # 任务的静态属性q
        self.Task_active_time = active_time                     # 任务的激活区间长度
        self.Task_HI_response_time = response_time              # 任务的响应时间

    def __repr__(self):
        return (f"Task(id={self.Task_id}, "
                f"deadline={self.Task_deadline}, "
                f"period={self.Task_period}, "
                f"wcet={self.Task_wcet}, "
                f"criticality={self.Task_criticality}, "
                f"pfh={self.Task_pfh}, "
                f"q={self.Task_q}, "
                f"active_time={self.Task_active_time}, "
                f"HI_response_time={self.Task_HI_response_time})")


# 作业
class Job:
    def __init__(self, task_id, deadline, period, wcet, criticality, pfh, start_execution, end_execution, release_time, real_deadline, index):
        self.Job_id = task_id                                   # 作业的id
        self.Job_deadline = deadline                            # 作业的相对截止期
        self.Job_period = period                                # 作业的周期
        self.Job_wcet = wcet                                    # 作业的执行时间
        self.Job_criticality = criticality                      # 任务的临界性（0表示低关键性，1表示高关键性）
        self.Job_pfh = pfh                                      # 作业的故障概率

        self.Job_start_execution = start_execution              # 作业的开始执行时间
        self.Job_end_execution = end_execution                  # 作业的结束执行时间
        self.Job_release_time = release_time                    # 作业的释放时间
        self.Job_real_deadline = real_deadline                  # 作业的实际截止时间
        self.Job_index = index                                  # 作业的索引

    def __repr__(self):
        return (f"Job(id={self.Job_id}, "
                f"deadline={self.Job_deadline}, "
                f"period={self.Job_period}, "
                f"wcet={self.Job_wcet}, "
                f"criticality={self.Job_criticality}, "
                f"pfh={self.Job_pfh}, "
                f"start_execution={self.Job_start_execution}, "
                f"end_execution={self.Job_end_execution}, "
                f"release_time={self.Job_release_time}, "
                f"real_deadline={self.Job_real_deadline}, "
                f"index={self.Job_index})")

# 计算最小公倍数
def lcm(a,b):
    return abs(a*b) // math.gcd(a,b)


# 截断函数，用于处理浮点精度
def trunc(x, p):
    result = int(int(x * 10 ** p) / float(10 ** p))
    if result == 0:
        return 1
    else:
        return result


# 根据Stafford算法生成任务利用率
def StaffordRandFixedSum(n, u, nsets):
    """
    生成nsets个任务集的任务利用率列表，每个任务集n个任务的利用率之和为u

    Args:
        n: 每个任务集的任务数量
        u: 任务集总利用率
        nsets: 要生成的任务集数量

    Returns:
        任务利用率列表的列表
    """
    if n < u:
        return None

    # 处理n=1的情况
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


# 生成任务集合
def generate_task_set(n=20, total_utilization=0.8, num_sets=1, period_options=None):
    """
    生成任务集合

    Args:
        n: 每个任务集的任务数量
        total_utilization: 任务集总利用率
        num_sets: 要生成的任务集数量
        period_options: 可选的周期列表

    Returns:
        任务对象的列表
    """

    if period_options is None:
        period_options = [400, 600, 800, 1000, 1200]

    # 生成利用率
    utilizations_list = StaffordRandFixedSum(n, total_utilization, num_sets)
    if utilizations_list is None:
        raise ValueError(f"无法生成利用率总和为{total_utilization}的{n}个任务")

    # 生成周期
    periods_list = []
    for _ in range(num_sets):
        periods = random.choices(period_options, k=n)
        periods_list.append(periods)

    task_sets = []

    for utilizations, periods in zip(utilizations_list, periods_list):
        task_set = []
        for i, (ui, pi) in enumerate(zip(utilizations, periods)):
            task_id = i + 1
            deadline = pi  # D = T
            wcet = trunc(ui * pi, 6)
            criticality = random.randint(0, 1)  # 随机生成关键性
            pfh = Decimal('0.0')  # 初始PFH为0
            q = 0  # 初始q属性
            active_time = 0  # 初始激活时间
            response_time = 0  # 初始响应时间

            task = Task(
                task_id=task_id,
                deadline=deadline,
                period=pi,
                wcet=wcet,
                criticality=criticality,
                pfh=pfh,
                q=q,
                active_time=active_time,
                response_time=response_time
            )
            task_set.append(task)

        task_sets.append(task_set)

    return task_sets[0] if num_sets == 1 else task_sets


if __name__ == "__main__":
    print("=== 实时任务调度系统 - 任务集生成测试 ===\n")

    # 测试1: 生成单个任务集
    print("1. 生成单个任务集 (默认参数):")
    tasks1 = generate_task_set()
    print(f"生成任务数量: {len(tasks1)}")
    for task in tasks1:
        print(f"  {task}")
    print()

    # 测试2: 生成指定参数的任务集
    print("2. 生成指定参数的任务集:")
    tasks2 = generate_task_set(
        n=5,
        total_utilization=0.6,
        period_options=[500, 1000, 1500]
    )
    total_util = sum(task.Task_wcet / task.Task_period for task in tasks2)
    print(f"实际总利用率: {total_util:.4f}")
    for task in tasks2:
        utilization = task.Task_wcet / task.Task_period
        print(f"  任务{task.Task_id}: WCET={task.Task_wcet}, Period={task.Task_period}, "
              f"Utilization={utilization:.4f}, Criticality={task.Task_criticality}")
    print()

    # 测试3: 生成多个任务集
    print("3. 生成多个任务集:")
    multiple_sets = generate_task_set(n=3, total_utilization=0.8, num_sets=2)
    for i, task_set in enumerate(multiple_sets):
        total_util = sum(task.Task_wcet / task.Task_period for task in task_set)
        hi_tasks = sum(1 for task in task_set if task.Task_criticality == 1)
        print(f"  任务集 {i + 1}: 任务数={len(task_set)}, 总利用率={total_util:.4f}, "
              f"高关键性任务={hi_tasks}")
        for task in task_set:
            utilization = task.Task_wcet / task.Task_period
            print(f"    Task{task.Task_id}: U={utilization:.4f}, C={task.Task_criticality}")
    print()

    # 测试4: 边界情况测试
    print("4. 边界情况测试:")
    try:
        # 测试高利用率情况
        tasks_high_util = generate_task_set(n=5, total_utilization=0.95)
        high_util = sum(task.Task_wcet / task.Task_period for task in tasks_high_util)
        print(f"  高利用率测试: 目标=0.95, 实际={high_util:.4f}")

        # 测试低利用率情况
        tasks_low_util = generate_task_set(n=8, total_utilization=0.3)
        low_util = sum(task.Task_wcet / task.Task_period for task in tasks_low_util)
        print(f"  低利用率测试: 目标=0.30, 实际={low_util:.4f}")

    except ValueError as e:
        print(f"  错误: {e}")
    print()

    # 测试5: 统计信息
    print("5. 统计信息:")
    all_tasks = generate_task_set(n=50, total_utilization=0.7, num_sets=5)
    total_tasks = sum(len(task_set) for task_set in all_tasks)
    hi_count = sum(1 for task_set in all_tasks for task in task_set if task.Task_criticality == 1)
    lo_count = total_tasks - hi_count

    print(f"  总任务数: {total_tasks}")
    print(f"  高关键性任务: {hi_count} ({hi_count / total_tasks * 100:.1f}%)")
    print(f"  低关键性任务: {lo_count} ({lo_count / total_tasks * 100:.1f}%)")

    # 计算WCET统计
    wcets = [task.Task_wcet for task_set in all_tasks for task in task_set]
    periods = [task.Task_period for task_set in all_tasks for task in task_set]

    print(f"  WCET范围: {min(wcets)} - {max(wcets)}")
    print(f"  周期范围: {min(periods)} - {max(periods)}")
    print(f"  平均WCET: {sum(wcets) / len(wcets):.2f}")
    print(f"  平均周期: {sum(periods) / len(periods):.2f}")

    # 测试6: 验证最小公倍数函数
    print("\n6. 最小公倍数测试:")
    test_cases = [(12, 18), (15, 25), (7, 13)]
    for a, b in test_cases:
        result = lcm(a, b)
        print(f"  lcm({a}, {b}) = {result}")

    # 测试7: 截断函数测试
    print("\n7. 截断函数测试:")
    test_values = [0.123456789, 1.23456789, 0.000123, 12.3456789]
    for val in test_values:
        truncated = trunc(val, 4)
        print(f"  trunc({val}, 4) = {truncated}")

    print("\n=== 测试完成 ===")