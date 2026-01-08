# Gemma Token Analysis

| Notebook | Link |
| :--- | :--- |
| **Logprobs Generation** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonicVarun/gemma-token-analysis/blob/master/Logprobs_in_Gemma.ipynb) |
| **Token Tree Analysis** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PythonicVarun/gemma-token-analysis/blob/master/Token_Tree_Analysis.ipynb) |

This repository explores the internal stochastic nature of Gemma models. By extracting transition scores and logits from the Hugging Face `transformers` generation loop, we can analyze the model's confidence levels and visualize "competing" tokens at each step of the sequence.

## Features

- **Log Probability Analysis**: Extract and analyze the log probabilities of generated tokens to understand model confidence.
- **Top-K Candidates**: View the top alternative tokens considered by the model at each step.
- **Guided Generation**: Steer the model's output by providing a specific starting prefix (e.g., forcing a code block).
- **Token Tree Exploration**: Construct and visualize decision trees of token generation paths based on probability thresholds.
- **Data Export**: Save analysis results to JSONL or JSON for further processing.

## Dynamic Thresholding Logic

The dynamic thresholding logic in `Token_Tree_Analysis.ipynb` adapts how "picky" the model is about branching based on how busy the search queue currently is.

$$
T_{current} = T_{min} + \min\left(1.0, \frac{|Q|}{Q_{limit}}\right) \times (T_{max} - T_{min})
$$

Where:
* $T_{current}$ is the calculated probability threshold for the current step.
* $T_{min}$ is the `min_branch_threshold` (e.g., 0.1).
* $T_{max}$ is the `max_branch_threshold` (e.g., 0.5).
* $|Q|$ is the current length of the queue (number of active paths).
* $Q_{limit}$ is the `soft_queue_limit` (target number of active paths).

**Note:** The saturation ratio is capped at **1.0**.

### How it works behaviorally:

1. **Empty Queue:** When the queue is small, the threshold is close to $T_{min}$. This encourages the model to branch out and explore even low-probability alternatives.
2. **Full Queue:** As the queue fills up (approaching `soft_queue_limit`), the threshold rises toward $T_{max}$. This forces the model to be very selective, only branching on highly probable tokens to prevent the search from exploding exponentially.

## Repository Structure

- `Logprobs_in_Gemma.ipynb`: The main Jupyter Notebook containing the log probability analysis code, helper functions, and experiments.
- `Token_Tree_Analysis.ipynb`: Notebook for generating and analyzing token trees.
- `token_tree_analysis/`: Contains the visualizer and sample outputs for the token tree analysis.

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -U torch transformers pandas accelerate numpy huggingface-hub
```

## Usage

1. Open `Logprobs_in_Gemma.ipynb` in VS Code or Jupyter Lab.
2. Ensure you have a Hugging Face account and an access token.
3. Run the notebook cells to:
   - Authenticate with Hugging Face.
   - Load the Gemma model (default: `google/gemma-2-2b-it`).
   - Run the log probability analysis experiment.
   - Run the guided generation experiment.
4. Open `Token_Tree_Analysis.ipynb` to generate and analyze token decision trees.

## Visualization

- You can visualize the generated JSONL data using the [Gemma Token Analysis Visualizer](https://pythonicvarun.github.io/gemma-token-analysis/logprobs-visualizer/).

- For analyzing token generation trees, use the [Token Tree Visualizer](https://pythonicvarun.github.io/gemma-token-analysis/token_tree_analysis/).
  - **Response Visualizer**: Click any token to see alternatives and regenerate sequences
  - **Tree Visualizer**: Interactive D3.js visualization of token generation paths

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- Pandas
- Accelerate
- Bitsandbytes
- A GPU is recommended for faster inference.
