
import subprocess
import sys

# Run the tool
process = subprocess.Popen([
    'python', 'tools/breach_checker.py'
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Send input
input_data = "yes\n+17314150198\n"
stdout, stderr = process.communicate(input=input_data)

print("=== Breach Checker Results ===")
print(stdout)
if stderr:
    print("Errors:", stderr)
