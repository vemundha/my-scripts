import subprocess
import sys
import json

if len(sys.argv) < 3:
    print("Usage: python kql.py <app_id> <KQL_query> [offset]")
    sys.exit(1)

app_id = sys.argv[1]
kql_query = sys.argv[2]

# Optional offset argument
offset = sys.argv[3] if len(sys.argv) > 3 else "4h"

# Create the command string
#command = f'az monitor app-insights query --apps "{app_id}" --analytics-query "{kql_query}" --offset "{offset}"'
command = f'az monitor app-insights query --apps "{app_id}" --analytics-query "{kql_query}"'


# Run the command
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Check for errors
if result.returncode != 0:
    print("Error executing query:")
    print(result.stderr.decode())
else:
    output_json = json.loads(result.stdout.decode())
    pretty_output = json.dumps(output_json, indent=4)
    print(pretty_output)
    # compact_output = json.dumps(output_json) # or json.dumps(output_json, indent=None)
    # print(compact_output)
