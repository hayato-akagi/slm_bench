import json
import time
import torch
import pandas as pd
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load environment variables
PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.json")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "")
HF_TOKEN = os.getenv("HUGGING_FACE_ACCESS_TOKEN", None)

# Set seed for reproducibility
torch.random.manual_seed(0)

# Load prompts from JSON
with open(PROMPT_FILE, "r") as f:
    prompts = json.load(f)

results = []

# Function to get model parameter size
def get_model_size(model):
    total_params = sum(p.numel() for p in model.parameters())
    return round(total_params / 1e9, 2)  # Convert to billion parameters (B)

# Ensure output.csv exists with headers if not present
if not os.path.exists(OUTPUT_FILE):
    print(f"{OUTPUT_FILE} not found. Creating it...")
    with open(OUTPUT_FILE, "w") as f:
        f.write("model_name,model_size_b,input_prompt,response,response_time\n")  # Add headers

# Loop through each model
print(f"Loading model: {MODEL_PATH}")

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype="auto",
    trust_remote_code=True,
    token=HF_TOKEN  # Ensure authentication with Hugging Face token
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_auth_token=HF_TOKEN)  # Pass the token here as well

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Get model size (number of parameters in billions)
model_size_b = get_model_size(model)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.0,
    "do_sample": False,
}

for prompt in prompts:
    input_text = prompt["content"]
    start_time = time.time()
    output = pipe(input_text, **generation_args)
    end_time = time.time()

    response_time = round(end_time - start_time, 4)
    generated_text = output[0]['generated_text'] if output else ""

    results.append([MODEL_PATH, model_size_b, input_text, generated_text, response_time])

# Write results to CSV
df = pd.DataFrame(results, columns=["model_name", "model_size_b", "input_prompt", "response", "response_time"])
df.to_csv(OUTPUT_FILE, mode='a', header=False, index=False)

print(f"Results saved to {OUTPUT_FILE}")
