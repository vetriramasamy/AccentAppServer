from gpt4all import GPT4All

# Load model once
model = GPT4All(
    model_name="Llama-3.2-1B-Instruct-Q5_K_M.gguf",
    model_path="./models",
    allow_download=False,
    n_threads=8   # adjust to CPU cores
)

def rewrite_to_american_english(text: str) -> str:
    prompt = llama32_prompt(
    system="You are an expert in English",
    user=f"fix the grammar and return the corrected text.: {text}"
    )
    response = model.generate(prompt, max_tokens=80, temp=0.3)
    return response

def llama32_prompt(system, user):
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{user}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""
