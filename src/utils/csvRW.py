import os
import csv

def setup_output(csv_filename, output_directory=None):
    """Creates the output CSV file in the specified directory."""
    if output_directory is None:
        output_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.abspath(os.path.join(output_directory, "..", "..", "tests"))  

    os.makedirs(output_directory, exist_ok=True)  
    return os.path.join(output_directory, csv_filename)

def write_csv_header(csv_file, *headers):
    """Writes a flexible header row to a CSV file, allowing dynamic column names."""
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)

def write_to_csv(csv_file, *data):
    """Writes a row of data to a CSV file, supporting variable-length arguments."""
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(data)

def read_csv_data(csv_file, is_multi_agent=False):
    """Reads CSV data and dynamically adjusts based on available headers.
    
    - `is_multi_agent=True`: Returns a dictionary where keys are agent IDs.
    """
    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)  # Read header row dynamically

        if is_multi_agent:
            data_dict = {header: {} for header in headers[1:]}  # Skip the "Agent" column
        else:
            data_dict = {header: [] for header in headers}

        for row in reader:
            if is_multi_agent:
                agent_id = int(row[0])  # The first column should be the agent number
                for i, header in enumerate(headers[1:], start=1):
                    if agent_id not in data_dict[header]:
                        data_dict[header][agent_id] = []
                    try:
                        data_dict[header][agent_id].append(float(row[i]) if row[i].replace('.', '', 1).isdigit() else row[i])
                    except ValueError:
                        data_dict[header][agent_id].append(row[i])
            else:
                for i, header in enumerate(headers):
                    try:
                        data_dict[header].append(float(row[i]) if row[i].replace('.', '', 1).isdigit() else row[i])
                    except IndexError:
                        data_dict[header].append(None)  # Handle missing values

    return data_dict  # Return structured data dictionary
