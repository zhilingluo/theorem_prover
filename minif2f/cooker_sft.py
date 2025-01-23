import json

from minif2f.constant import QWEN_SYSTEM_PROMPT
def read_collect_file(filename):
    collect_file = 'collects/report_2025-01-15_20-11-30.txt'
    with open(collect_file, 'r') as f:
        js_raw = json.load(f)

    return js_raw
js_raw=[]
file_list =['collects/report_2025-01-15_20-11-30.txt','collects/report_2025-01-15_17-04-54.txt']
file_list=['collects/report_2025-01-22_11-49-48.txt','collects/report_2025-01-15_20-11-30.txt','collects/report_2025-01-15_17-04-54.txt','report_2025-01-22_17-09-27.txt']
for filename  in file_list:
    js_raw+=read_collect_file(filename)
def unique(js_raw):
    unique_list = []

    for item in js_raw:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list
js_raw=unique(js_raw)
def message_builder(chosen_js):
    js={
        "messages":[{'role':"system","content":QWEN_SYSTEM_PROMPT},
                  {'role':"user","content":chosen_js['state_before']},
                    {'role':"assistant","content":chosen_js['tactic']}]
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
    for js in js_raw:
        if js['state_before']==state_before and js['is_correct']==True and js['state_after']==state_after:
            chosen_js.append(js)


    for chosen in chosen_js:

        messages.append(message_builder(chosen))
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
save_train_json('cooked_data/sft.jsonl',messages)