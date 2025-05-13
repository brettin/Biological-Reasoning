import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
model_id = "google/txgemma-2b-predict"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    #quantization_config=quantization_config,
    device_map={"":0},
    torch_dtype="auto",
    attn_implementation="eager",
)

# wget -nc https://storage.googleapis.com/healthai-us/txgemma/datasets/trialbench_adverse-event-rate-prediction_train.jsonl
from datasets import load_dataset
data = load_dataset(
    "json",
    data_files="trialbench_adverse-event-rate-prediction_train.jsonl",
    split="train",
)

# Display dataset details
def formatting_func(example):
    text = f"{example['input_text']} {example['output_text']}"
    return text

# Display formatted training data example
print(formatting_func(data[100]))

from peft import LoraConfig

lora_config = LoraConfig(
    r=8,
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "o_proj",
        "k_proj",
        "v_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
)

from peft import prepare_model_for_kbit_training, get_peft_model
model = prepare_model_for_kbit_training(model)

import transformers
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model=model,
    train_dataset=data,
    args=SFTConfig(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=2,
        max_steps=50,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=5,
        max_seq_length=512,
        output_dir="./content/outputs",
        optim="paged_adamw_8bit",
        report_to="none",
    ),
    peft_config=lora_config,
    formatting_func=formatting_func,
)

trainer.train()

