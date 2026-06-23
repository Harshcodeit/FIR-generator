from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = r"E:\AI\models\gemma-4-e4b-it"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

prompt = "What is theft"
chat_prompt = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    tokenize=False,
    add_generation_prompt=True,
)

print("CHAT PROMPT:\n", chat_prompt)
inputs = tokenizer(chat_prompt, return_tensors="pt")
print("INPUT IDs SHAPE:", inputs["input_ids"].shape)
print("INPUT IDS:", inputs["input_ids"][0][:40].tolist())

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

full = tokenizer.decode(outputs[0], skip_special_tokens=True)
new_only = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

print("\nFULL DECODED:\n", full)
print("\nNEW TOKENS ONLY:\n", new_only)
