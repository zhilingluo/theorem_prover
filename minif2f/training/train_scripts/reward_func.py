import re
def format_reward_func(completions, **kwargs):
    """Reward function that checks if the completion has a specific format."""
    pattern = r"^<think>.*?</think>.*?$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content,re.DOTALL) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]


def acc_reward_func(completions, **kwargs):
    # Regular expression to capture content inside \boxed{}
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.search(r".*?</think>.*?```lean.*?\n(.*?)\n```.*?",completion_content,re.DOTALL) for completion_content in completion_contents]
    #matches = [re.search(r"```lean\n(.*?)\n```", completion) for completion in completion_contents]
    contents = [match.groups()[-1] if match else "" for match in matches]
    extracted=[]
    for content in contents:
        lines = content.split("\n")
        next_tactic = lines[0]
        next_tactic_list = []
        if len(lines) > 1:
            next_tactic_list=[]
            for line in lines:
                if '--' in line or 'theorem' in line:# this is a comment line
                    continue
                else:
                    next_tactic_list.append(line)
            next_tactic="\n".join(next_tactic_list)
        extracted.append(next_tactic)
    # for c, gt in zip(extracted,kwargs['ground_truth']):
    #     if c!=gt:
    #         print('----')
    #         print(c)
    #         print(gt)
    # Reward 1 if the content is the same as the ground truth, 0 otherwise
    return [1.0 if c == gt else 0.0 for c, gt in zip(extracted,kwargs['ground_truth'])]
