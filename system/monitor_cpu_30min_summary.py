import psutil
import time
import sys
import datetime

# Check if the log directory exists
import os
if not os.path.exists("C:\\temp"):
    print("Directory C:\\temp does not exist. Please create it or change the log path.")
    sys.exit(1)

sample_frequency = int(sys.argv[1])

if sample_frequency <= 0:
    print("Invalid sample frequency provided.")
    sys.exit(1)

total_sample_time = 600 # 10 minutes
num_samples = total_sample_time // sample_frequency

def get_process_times():
    excluded_names = ['Idle', 'System', 'System Idle Process', 'System Interrupts', 'System', 
                      'sfcservice64.exe', 'sfc.exe', 'dwm.exe', 'conhost.exe', 'svchost.exe', 'csrss.exe', 
                      'wininit.exe', 'winlogon.exe', 'services.exe', 'lsass.exe', 'svchost.exe', 'Taskmgr.exe']
    process_times = {}
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_times']):
        if proc.info['name'] not in excluded_names:
            cpu_time = proc.info['cpu_times'].user + proc.info['cpu_times'].system
            process_times[proc.info['name']] = cpu_time
    
    return process_times

while True:
    from_time = datetime.datetime.now()
    initial_times = get_process_times()

    for i in range(num_samples):
        time.sleep(sample_frequency)
        elapsed_time = (i + 1) * sample_frequency
        print(f"Sampled {elapsed_time} seconds of {total_sample_time} seconds...")

    final_times = get_process_times()
    to_time = datetime.datetime.now()

    delta_records = {name: final_times[name] - initial_times.get(name, 0) for name in final_times}

    # Get top 5 processes by delta CPU time
    top_processes = sorted(delta_records.items(), key=lambda x: x[1], reverse=True)[:5]

    duration_minutes = (to_time - from_time).seconds / 60.0

    with open("C:\\temp\\monitor-cpu.log", "a") as file:
        file.write(f"\nSummary from {from_time.strftime('%Y-%m-%d %H:%M:%S')} to {to_time.strftime('%Y-%m-%d %H:%M:%S')} ({duration_minutes:.2f} minutes):\n")
        for proc, delta in top_processes:
            file.write(f"{proc}: {delta:.2f} seconds\n")
