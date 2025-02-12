from minif2f.training.call_gpt import call_gpt
from minif2f.training.common_utils import read_train_json, save_list, save_train_json
all=read_train_json('merged.jsonl')
#all=all[:3]
prompts=[]
meta_js_all=[]
for js in all:

    meta_js_all.append(
        {
            "tactic_state":js['messages'][1]['content'].split('\n---\n')[1],
            "next_tactic":js['messages'][2]['content'],
            "prompt":js['messages'][1]['content'],
         }
    )

save_train_json('metadata.jsonl',meta_js_all)
