import os
import csv
import matplotlib.pyplot as plt
import subprocess

# Define paths (Following run_test3.py style)
test_script = os.path.join("tests", "test_stayInMddleOnly_csvBeta.py")
csv_folder = os.path.join("tests", "tests_csv")
graph_folder = os.path.join("tests", "tests_graphs")
os.makedirs(graph_folder, exist_ok=True)

# Define file paths
angle_csv_file = os.path.join(csv_folder, "angle_beta_results.csv")
angle_png_file = os.path.join(graph_folder, "angle_beta_graph.png")

# Run the test script to generate the CSVs
subprocess.run(["python3", test_script])
# Read CSV data
steps = []
angles = []

with open(angle_csv_file, "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip the header row
    for row in reader:
        steps.append(int(row[0]))          # Step number
        angles.append(float(row[1]))       # Beta angle

# Plot angle beta vs step
plt.figure(figsize=(10, 6))
plt.plot(steps, angles, label="Beta Angle", color="blue", marker="o", linestyle="-")
plt.xlabel("Steps")
plt.ylabel("Beta Angle (degrees)")
plt.title("Angle Beta Over Steps")
plt.legend()
plt.grid(True)

# Save the figure in the structured folder
plt.savefig(angle_png_file)

