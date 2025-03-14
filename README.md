# SLM Benchmark

This project benchmarks Language Models on CPU, comparing response time and accuracy across different models. Each model runs in a separate container to optimize resource usage.

## Features
- Compare multiple SLMs from Hugging Face
- Measure response time
- Run each model in an isolated container to prevent memory overload
- Supports Hugging Face authentication for gated models

## Directory Structure
```
slm-bench/
│── Dockerfile
│── run.sh
│── run_model.py
│── prompt.json
│── output.csv
│── .env
```

## Setup
### Prerequisites
- Docker or Podman installed

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/hayato-akagi/slm_bench.git
   cd slm-bench
   ```
2. Create a `.env` file with your settings:
   ```sh
    MODEL_PATHS=microsoft/Phi-4-mini-instruct,deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
    PROMPT_FILE=/app/prompt.json
    OUTPUT_FILE=/app/output.csv
    HUGGING_FACE_ACCESS_TOKEN=hf_xxxxxxxxxxxxxx 
    RUNTIME=docker
   ```

## Usage
### Running Benchmarks
```sh
chmod +x run.sh
./run.sh
```
This script:
1. Builds the container
2. Runs each model in a separate container
3. Saves the results to `output.csv`

## Example Output
After running the benchmark, the results are saved in `output.csv` in the following format:

| model_name                          | model_size_b | input_prompt            | response                 | response_time |
|-------------------------------------|-------------|-------------------------|--------------------------|--------------|
| microsoft/Phi-4-mini-instruct       | 3.84        | "What is AI?"           | "AI stands for..."      | 0.532       |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B          | 1.73        | "Explain gravity."      | "Gravity is..."        | 0.678       |

## Customization
### Changing Models
Modify `MODEL_PATHS` in `.env` to test different models:
```sh
MODEL_PATHS=xxx/yyy,zzz/aaa
```
### Modifying Prompts
Edit `prompt.json` to customize the input prompts:
```json
[
    { "content": "What is deep learning?" },
    { "content": "Explain quantum physics." }
]
```

## License
MIT License

