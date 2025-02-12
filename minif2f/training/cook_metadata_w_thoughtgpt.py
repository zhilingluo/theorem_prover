from minif2f.training.common_utils import read_train_json,save_train_json
from minif2f.training.prompt import system_prompts

raw=read_train_json('metadata_w_thoughtgpt.jsonl')
cooked=[]
sft_cooked=[]
for line in raw:
    prompt =[
        {
            'role':'system',
            'content':system_prompts
        },
        {
            "role":"user",
            "content":line['prompt']
        }

    ]
    # '[{"role":"system", "content":"请简洁回答"},{"role":"user","content":"'+line['prompt']+'"}]'
    gt=line['next_tactic'].strip()
    thought=line.get('thought_gpt','')
    complete=[
        {
            'role':'assistant',
            'content':'<think>'+thought+'</think>```lean\n'+gt+'\n```'
        }
    ]
    #'[{"role":"assistant","content": "<think>'+thought+'</think><answer>\n```lean\n'+gt+'\n```</answer>"}]'
    cooked_line = {
        'prompt':prompt,
        'completion':complete,
        'ground_truth':gt
    }
    sft_line={
        'messages':prompt+complete
    }
    if len(str(sft_line))>10000:
        print(sft_line)
    else:

        cooked.append(cooked_line)
        sft_cooked.append(sft_line)
print(cooked_line)
save_train_json('train_scripts/grpo_ds.jsonl',cooked)
save_train_json('train_scripts/sft_ds.jsonl',sft_cooked)