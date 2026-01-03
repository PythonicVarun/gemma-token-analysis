# Gemma Token Analysis

This repository explores the internal stochastic nature of Gemma models. By extracting transition scores and logits from the Hugging Face `transformers` generation loop, we can analyze the model's confidence levels and visualize "competing" tokens at each step of the sequence.

## Features

- **Log Probability Analysis**: Extract and analyze the log probabilities of generated tokens to understand model confidence.
- **Top-K Candidates**: View the top alternative tokens considered by the model at each step.
- **Guided Generation**: Steer the model's output by providing a specific starting prefix (e.g., forcing a code block).
- **Data Export**: Save analysis results to JSONL for further processing.

## Repository Structure

- `Logprobs_in_Gemma3.ipynb`: The main Jupyter Notebook containing the analysis code, helper functions, and experiments.

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -U torch transformers pandas accelerate bitsandbytes
```

## Usage

1. Open `Logprobs_in_Gemma3.ipynb` in VS Code or Jupyter Lab.
2. Ensure you have a Hugging Face account and an access token.
3. Run the notebook cells to:
   - Authenticate with Hugging Face.
   - Load the Gemma model (default: `google/gemma-2-2b-it`).
   - Run the log probability analysis experiment.
   - Run the guided generation experiment.

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- Pandas
- Accelerate
- Bitsandbytes
- A GPU is recommended for faster inference.
