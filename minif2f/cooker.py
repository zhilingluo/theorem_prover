import json

from minif2f.constant import QWEN_SYSTEM_PROMPT

collect_file='collects/report_2025-01-15_20-11-30.txt'
with open(collect_file,'r') as f:
    js_raw=json.load(f)

def message_builder(chosen_js,rejected_js):
    js={
        "prompt":[{'role':"system","content":QWEN_SYSTEM_PROMPT},
                  {'role':"user","content":chosen_js['state_before']}],
        "chosen":[{'role':"assistant","content":chosen_js['tactic']}],
        "rejected":[{'role':"assistant","content":rejected_js['tactic']}]
    }
    return js

def search_node(state_after,js_raw):
    messages=[]
    for js in js_raw:
        if js['state_after']==state_after and js['is_correct']==True:
            messages+=search(js['state_before'],js['state_after'], js_raw)
            messages+=search_node(js['state_before'],js_raw)
    return messages
def search(state_before,state_after,js_raw):
    messages=[]

    chosen_js=[]
    rejected_js=[]
    # search pos
    for js in js_raw:
        if js['state_before']==state_before and js['is_correct']==True and js['state_after']==state_after:
            chosen_js.append(js)

    for js in js_raw:
        if js['state_before']==state_before and js['is_correct']==False:
            rejected_js.append(js)

    for chosen in chosen_js:
        for rejected in rejected_js:
            messages.append(message_builder(chosen,rejected))
    return messages

messages=[]
for js in js_raw:
    if js['is_finish']==True:# it reaches the solved

        messages+=search(js['state_before'],js['state_after'],js_raw)
        messages+=search_node(js['state_before'],js_raw)
# prepare js_all
# js={
#     "prompt":[],
#     "chosen":[],
#     "rejected":[]
# }



def save_train_json(target_file,js):
    with open(target_file,'w',encoding='utf-8') as f:
        for js_single in js:
            strs= json.dumps(js_single,ensure_ascii=False)
            f.write(strs+'\n')

# save it
save_train_json('cooked_data/dpo.jsonl',messages)