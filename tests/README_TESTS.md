# Tests for PySTK2 Gymnasium

This folder contains test scripts for our PySTK2 Gymnasium Reinforcement Learning project. The tests are designed to evaluate different aspects of the environment and generate results in the form of CSV files and plots.


### Test Scripts

#### Test 0: Basic Single-Agent Test
- **Script**: `tests0_0.py`
- **Description**: Runs a basic single-agent test using a flattened action space. The agent is AI-controlled and uses random actions sampled from the environment.
- **Outputs**:
  - CSV: `tests_csv/test0_0_results.csv` (step, reward, terminated, truncated).
  - Plot: `tests_csv/test0_0_graph.png` (Reward vs Step).

**To Run**:
```bash
python3 tests0_0.py

