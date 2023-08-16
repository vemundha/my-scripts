import psutil
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python monitor_cpu.py <total_sample_time_in_seconds> <sample_frequency_in_seconds>")
    sys.exit(1)

total_sample_time = int(sys.argv[1])
sample_frequency = int(sys.argv[2])

if sample_frequency <= 0 or total_sample_time <= 0 or sample_frequency > total_sample_time:
    print("Invalid time values provided.")
    sys.exit(1)

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

initial_times = get_process_times()

for i in range(num_samples):
    time.sleep(sample_frequency)
    elapsed_time = (i + 1) * sample_frequency
    print(f"Sampled {elapsed_time} seconds of {total_sample_time} seconds...")

final_times = get_process_times()

delta_records = {name: final_times[name] - initial_times.get(name, 0) for name in final_times}

# Get top 5 processes by delta CPU time
top_processes = sorted(delta_records.items(), key=lambda x: x[1], reverse=True)[:5]

print("\nTop 5 processes by CPU delta time:")
for proc, delta in top_processes:
    print(f"{proc}: {delta:.2f} seconds")
