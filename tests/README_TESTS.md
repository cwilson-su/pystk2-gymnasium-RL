# Tests

This folder contains test scripts for our PySTK2 Gymnasium Reinforcement Learning project. The tests are designed to evaluate different aspects of the environment and generate results in the form of CSV files and plots.

#### <i>---To me continuously modified as the tests are modified.---</i>

#### Test Scripts
1. **`tests0_0.py`**:
   - A simple test script that runs a single-agent simulation with an AI-controlled agent using a flattened action space.
   - **Output**: Overwrites or creates `tests_csv/test0_0_results.csv`.

2. **`tests0_1.py`**:
   - A single-agent simulation with custom manual actions.
   - **Output**: Overwrites or creates `tests_csv/test0_1_results.csv`.

3. **`tests0_2.py`**:
   - A multi-agent simulation with five agents, including AI-controlled and manually controlled agents. Outputs detailed information for each agent.
   - **Output**: Overwrites or creates `tests_csv/test0_2_results.csv`.

---

#### CSV Storage (`tests_csv` Folder)
- CSV files store the results of each test:
  - `test0_0_results.csv`: Contains columns `Step`, `Reward`, `Terminated`, and `Truncated`.
  - `test0_1_results.csv`: Contains columns `Step`, `Reward`, `Terminated`, and `Truncated`.
  - `test0_2_results.csv`: Contains columns `Agent`, `Reward`, `Terminated`, `Position`, and `Distance`.

Running the test scripts directly (`tests0_0.py`, `tests0_1.py`, `tests0_2.py`) will generate or overwrite these files.

---

#### Graph Generation (`tests_graphs` Folder)
The scripts in the `tests_graphs` folder automate running the tests, reading the CSV files, and generating plots:
1. **`run_test0.py`**:
   - Runs `tests0_0.py` and reads the generated `tests_csv/test0_0_results.csv`.
   - Creates a plot of `Step` vs `Reward`.
   - Saves the graph in the `tests_graphs` folder as `test0_0_graph.png`.

2. **`run_test1.py`**:
   - Runs `tests0_1.py` and reads the generated `tests_csv/test0_1_results.csv`.
   - Creates a plot of `Step` vs `Reward`.
   - Saves the graph in the `tests_graphs` folder as `test0_1_graph.png`.

3. **`run_test2.py`**:
   - Runs `tests0_2.py` and reads the generated `tests_csv/test0_2_results.csv`.
   - Creates three plots:
     - **`Step` vs `Reward`**: Shows reward progression for all agents.
     - **`Step` vs `Position`**: Shows position changes for all agents.
     - **`Step` vs `Distance`**: Shows the distance covered by all agents.
   - Saves the graphs in the `tests_graphs` folder as:
     - `test0_2_reward_graph.png`
     - `test0_2_position_graph.png`
     - `test0_2_distance_graph.png`

---

### How to Use

1. **Run Simple Test Scripts**:
   - To run the basic tests and generate or overwrite CSV files, execute:
     ```bash
     python3 tests0_0.py
     python3 tests0_1.py
     python3 tests0_2.py
     ```

2. **Generate Graphs with `tests_graphs` Scripts**:
   - To run tests and generate plots, execute:
     ```bash
     python3 tests_graphs/run_test0.py
     python3 tests_graphs/run_test1.py
     python3 tests_graphs/run_test2.py
     ```
   - These scripts will run the corresponding test scripts, read the resulting CSV files, and create graphs.

3. **Outputs**:
   - **CSV Files**: Stored in `tests_csv/`.
   - **Graphs**: Stored in `tests_graphs/`.

---

### Requirements
Ensure the following Python libraries are installed:
- `gymnasium`
- `matplotlib`
- `numpy`

Install them using:
```bash
pip install gymnasium matplotlib numpy
```

