import os
import matplotlib.pyplot as plt

def plt_plot(x_data, y_data, x_label, y_label, title, filename, color="blue"):
    """Generates and saves a single-line Matplotlib plot."""
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, label=y_label, color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plt_multi_agent_plot(agent_data, x_label, y_label, title, filename):
    """Generates and saves a Matplotlib plot for multi-agent data."""
    plt.figure(figsize=(10, 6))

    for agent, (x_data, y_data) in agent_data.items():
        plt.plot(x_data, y_data, label=f"Agent {agent}")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
