# train_grpo.py
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    HfArgumentParser,
    BitsAndBytesConfig,
)
#dataset = load_dataset("trl-lib/tldr", split="train")

def load_tokenizer(path):
    tokenizer = AutoTokenizer.from_pretrained(
        path,
        padding_side="left",
        trust_remote_code=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    return tokenizer
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['prompt'])):
        text = f"{example['prompt'][i]}\n{example['completion'][i]}"
        output_texts.append(text)
    return output_texts

model_path = 'qwen1.5b/'
data_path = 'sft.jsonl'
# Define the reward function, which rewards completions that are close to 20 characters
from reward_func import format_reward_func,acc_reward_func
tokenizer = load_tokenizer(model_path)
dataset = load_dataset(data_files=data_path, path='json', split="train")

policy = AutoModelForCausalLM.from_pretrained(model_path)
training_args = SFTConfig(
    max_seq_length=512,
    output_dir="sft_output",
    report_to="wandb",
    num_train_epochs=10
)
trainer = SFTTrainer(
    model=policy,
    args=training_args,
    train_dataset=dataset,
    #formatting_func=formatting_prompts_func
    #processing_class=tokenizer,
)
trainer.train()
