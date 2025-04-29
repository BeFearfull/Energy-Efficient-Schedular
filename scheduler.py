# --- scheduler.py ---
class Task:
    def __init__(self, task_id, arrival_time, burst_time, power_per_unit):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.power_per_unit = power_per_unit
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.energy_consumed = 0

class EnergyEfficientScheduler:
    def __init__(self, tasks):
        self.tasks = [Task(**t) for t in tasks]
        self.completed_tasks = []

    def schedule_tasks(self):
        current_time = 0
        ready_queue = []
        task_list = sorted(self.tasks, key=lambda x: x.arrival_time)

        while task_list or ready_queue:
            while task_list and task_list[0].arrival_time <= current_time:
                ready_queue.append(task_list.pop(0))

            if ready_queue:
                ready_queue.sort(key=lambda x: (x.burst_time, x.power_per_unit))
                current_task = ready_queue.pop(0)

                current_task.start_time = current_time
                current_task.completion_time = current_time + current_task.burst_time
                current_task.turnaround_time = current_task.completion_time - current_task.arrival_time
                current_task.waiting_time = current_task.start_time - current_task.arrival_time
                current_task.energy_consumed = current_task.burst_time * current_task.power_per_unit

                current_time = current_task.completion_time
                self.completed_tasks.append(current_task)
            else:
                if task_list:
                    current_time = task_list[0].arrival_time

        return [
            {
                "task_id": t.task_id,
                "start_time": t.start_time,
                "completion_time": t.completion_time,
                "energy": t.energy_consumed
            }
            for t in self.completed_tasks
        ]

    def summary(self):
        total_energy = sum(t.energy_consumed for t in self.completed_tasks)
        avg_wait = sum(t.waiting_time for t in self.completed_tasks) / len(self.completed_tasks)
        avg_turn = sum(t.turnaround_time for t in self.completed_tasks) / len(self.completed_tasks)
        order = [t.task_id for t in self.completed_tasks]

        return {
            "Execution Order": order,
            "Total Energy (J)": round(total_energy, 2),
            "Average Waiting Time": round(avg_wait, 2),
            "Average Turnaround Time": round(avg_turn, 2)
        }
