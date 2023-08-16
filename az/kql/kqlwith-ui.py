import subprocess
import json
import tkinter as tk
from tkinter import scrolledtext

def execute_query():
    app_id = app_id_entry.get()
    kql_query = kql_query_entry.get(1.0, tk.END).strip()

    command = f'az monitor app-insights query --apps "{app_id}" --analytics-query "{kql_query}"'
    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        error_msg = "Error executing query:\n" + result.stderr.decode()
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, error_msg)
    else:
        output_json = json.loads(result.stdout.decode())
        pretty_output = json.dumps(output_json, indent=4)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, pretty_output)

        # Write output to the specified file
        output_file = output_file_entry.get()
        if output_file:
            with open(output_file, 'w') as f:
                f.write(pretty_output)

root = tk.Tk()
root.title("KQL Query UI")

# Widgets
app_id_label = tk.Label(root, text="App ID:")
app_id_label.grid(row=0, column=0, sticky='w', pady=5)
app_id_entry = tk.Entry(root, width=50)
app_id_entry.grid(row=0, column=1, pady=5, sticky='ew')

kql_query_label = tk.Label(root, text="KQL Query:")
kql_query_label.grid(row=1, column=0, sticky='w', pady=5)
kql_query_entry = scrolledtext.ScrolledText(root, width=70, height=4)
kql_query_entry.grid(row=1, column=1, pady=5, sticky='ew')

output_file_label = tk.Label(root, text="Output File:")
output_file_label.grid(row=2, column=0, sticky='w', pady=5)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=2, column=1, pady=5, sticky='ew')

execute_button = tk.Button(root, text="Execute Query", command=execute_query)
execute_button.grid(row=3, column=1, pady=15, sticky='e')

output_heading = tk.Label(root, text="Output:")
output_heading.grid(row=4, column=0, sticky='w', pady=5)

output_text = scrolledtext.ScrolledText(root, width=70, wrap=tk.WORD)
output_text.grid(row=5, column=0, columnspan=2, pady=5, sticky='nsew')

# Configuring the rows and columns to adjust according to the window resizing
root.grid_rowconfigure(5, weight=1)   # output_text should expand vertically
root.grid_columnconfigure(1, weight=1)  # Both entry and text widgets should expand horizontally

root.mainloop()
