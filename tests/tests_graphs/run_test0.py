import os
import csv
import subprocess
import matplotlib.pyplot as plt

# Define paths
test_script = os.path.join("tests", "tests0_0.py")
csv_file = os.path.join("tests", "tests_csv", "test0_0_results.csv")

# Run the test script
subprocess.run(["python3", test_script])

# Read CSV data
steps = []
rewards = []

with open(csv_file, "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip the header row
    for row in reader:
        steps.append(int(row[0]))  # Step
        rewards.append(float(row[1]))  # Reward

# Plot the graph
plt.figure()
plt.plot(steps, rewards, label="Reward")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.title("Test 0: Reward vs Step")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join("tests", "tests_graphs", "test0_0_graph.png"))
plt.show()
