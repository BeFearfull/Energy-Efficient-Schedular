# --- main.py ---
import tkinter as tk
from tkinter import messagebox
from scheduler import EnergyEfficientScheduler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Energy Efficient Task Scheduler")
root.geometry("1000x600")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Inputs
entries = {}
tasks = []

fields = ["Task ID", "Arrival Time", "Burst Time", "Power Per Unit"]
for field in fields:
    label = tk.Label(left_frame, text=field)
    label.pack()
    entry = tk.Entry(left_frame)
    entry.pack()
    entries[field] = entry

def add_task():
    try:
        task = {
            "task_id": entries["Task ID"].get(),
            "arrival_time": int(entries["Arrival Time"].get()),
            "burst_time": int(entries["Burst Time"].get()),
            "power_per_unit": float(entries["Power Per Unit"].get())
        }
        tasks.append(task)
        update_display()
        for e in entries.values():
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

add_button = tk.Button(left_frame, text="Add Task", command=add_task)
add_button.pack(pady=10)

text_output = tk.Text(left_frame, height=20, width=40)
text_output.pack()

# Charts
chart_frame = tk.Frame(right_frame)
chart_frame.pack(fill=tk.BOTH, expand=True)

# Update output
def update_display():
    text_output.delete(1.0, tk.END)
    for task in tasks:
        text_output.insert(tk.END, f"{task['task_id']} | Arrival: {task['arrival_time']} | Burst: {task['burst_time']} | Power: {task['power_per_unit']}\n")

def show_results():
    for widget in chart_frame.winfo_children():
        widget.destroy()

    scheduler = EnergyEfficientScheduler(tasks)
    execution = scheduler.schedule_tasks()
    summary = scheduler.summary()

    text_output.insert(tk.END, f"\nExecution Order: {summary['Execution Order']}\n")
    text_output.insert(tk.END, f"Total Energy: {summary['Total Energy (J)']} J\n")
    text_output.insert(tk.END, f"Average Waiting Time: {summary['Average Waiting Time']}\n")
    text_output.insert(tk.END, f"Average Turnaround Time: {summary['Average Turnaround Time']}\n")

    fig, (gantt, energy) = plt.subplots(2, 1, figsize=(8, 6))  # Increased height to avoid overlap

    # Gantt Chart
    for task in execution:
        gantt.barh(task["task_id"], task["completion_time"] - task["start_time"], left=task["start_time"])
    gantt.set_title("Gantt Chart")
    gantt.set_xlabel("Time")

    # Energy Chart
    ids = [task["task_id"] for task in execution]
    energies = [task["energy"] for task in execution]
    energy.bar(ids, energies)
    energy.set_title("Energy Consumption")
    energy.set_ylabel("Energy (J)")

    fig.tight_layout(pad=4.0)  # Added padding to prevent overlap

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

process_button = tk.Button(left_frame, text="Run Scheduler", command=show_results)
process_button.pack(pady=5)

root.mainloop()
