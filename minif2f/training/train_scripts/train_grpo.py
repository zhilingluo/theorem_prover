
# train_grpo.py
from datasets import load_dataset
from trl import GRPOConfig, GRPOTrainer
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

model_path = 'grpo_outputs/checkpoint-2364/'
data_path = 'grpo.jsonl'
# Define the reward function, which rewards completions that are close to 20 characters
from reward_func import format_reward_func,acc_reward_func
tokenizer = load_tokenizer(model_path)
dataset = load_dataset(data_files=data_path, path='json', split="train")

policy = AutoModelForCausalLM.from_pretrained(model_path)
training_args = GRPOConfig(output_dir="grpo_outputs_continue", logging_steps=10,report_to="wandb")
trainer = GRPOTrainer(
    model=policy,
    reward_funcs=[format_reward_func,acc_reward_func],
    args=training_args,
    train_dataset=dataset,
    #processing_class=tokenizer,
)
trainer.train()
