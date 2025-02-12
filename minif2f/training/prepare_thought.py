from minif2f.training.call_gpt import call_gpt
from minif2f.training.common_utils import read_train_json, save_train_json
from tqdm import tqdm
sys_prompt='阅读下面的lean4 定理证明过程，分析当前要证明的命题，以及已有条件，给出next tactic，注意到提供了一个参考性的next tactic，请不要假设已知这个参考\n'
all=read_train_json('metadata.jsonl')
all=all
prompts=[]
meta_js_all=[]
for i,js in tqdm(enumerate(all)):
    msg = [
        {"role": "system", "content": sys_prompt},
        {'role':'user',
            'content':js['prompt']+'\n'+js['next_tactic']
        }
        ]
    prompts.append({'messages':msg})

    thought=call_gpt(msg)
    rechecked_thought=thought
    if thought:
        js['thought_gpt']=thought
        msg = [
            {"role": "system", "content": "改写下面的解决思路，确保逻辑正确并且与最后的策略对齐"},
            {'role':'user',
                'content':'用户输入:\n'+js['prompt']+'\n'+'解决思路:\n'+thought+'\n```lean\n'+js['next_tactic']+'```'
            }
            ]
        rechecked_thought=call_gpt(msg)
    js['thought_rechecked']=rechecked_thought
    if i % 3==0:
        save_train_json('metadata_w_thoughtgpt.jsonl', all)

save_train_json('metadata_w_thoughtgpt.jsonl',all)
