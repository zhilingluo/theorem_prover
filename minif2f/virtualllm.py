from minif2f.constant import QWEN_SYSTEM_PROMPT
from minif2f.ft_model_call import call_ft_v0, call_ft_v1
from minif2f.qwenmax import call_qwen
import math
from concurrent.futures import ThreadPoolExecutor


DEFAULT_SCORE=0.1
def call_qwen_llm(prompt,temperatures,num_samples):
    # it calls qwen_turbo
    texts, scores = [], []
    for sample in range(num_samples):
        for temperature in temperatures:
            text = call_qwen(user_prompt_fewshot(prompt), temperature, system_prompt=QWEN_SYSTEM_PROMPT)
            text = post_process_on_general_llm(text)
            score = DEFAULT_SCORE
            texts.append(text)
            scores.append(score)
    return texts, scores

def call_qwen_ft0_raw(prompt,temperatures,num_samples):
    # it calls my fined qwen_ft
    texts, scores = [], []
    for sample in range(num_samples):
        for temperature in temperatures:
            text = call_ft_v0(user_prompt_0shot(prompt), temperature).strip()
            score = DEFAULT_SCORE
            texts.append(text)
            scores.append(score)
    return texts, scores


def call_qwen_ft0(prompt, temperatures, num_samples):
    texts, scores = [], []

    def generate_text(sample, temperature):
        text = call_ft_v0(user_prompt_0shot(prompt), temperature).strip()
        score = DEFAULT_SCORE
        return text, score

    with ThreadPoolExecutor() as executor:
        futures = []
        for sample in range(num_samples):
            for temperature in temperatures:
                futures.append(executor.submit(generate_text, sample, temperature))

        for future in futures:
            text, score = future.result()
            texts.append(text)
            scores.append(score)

    return texts, scores
def call_qwen_ft1_raw(prompt,temperatures,num_samples):
    # it calls my fined qwen_ft
    texts, scores = [], []
    for sample in range(num_samples):
        for temperature in temperatures:
            text = call_ft_v1(user_prompt_0shot(prompt), temperature).strip()
            score = DEFAULT_SCORE
            texts.append(text)
            scores.append(score)
    return texts, scores

def call_qwen_ft1(prompt, temperatures, num_samples):
    texts, scores = [], []

    def generate_text(sample, temperature):
        text = call_ft_v1(user_prompt_0shot(prompt), temperature).strip()
        score = DEFAULT_SCORE
        return text, score

    with ThreadPoolExecutor() as executor:
        futures = []
        for sample in range(num_samples):
            for temperature in temperatures:
                futures.append(executor.submit(generate_text, sample, temperature))

        for future in futures:
            text, score = future.result()
            texts.append(text)
            scores.append(score)

    return texts, scores
def call_deepseek(prompt,temperatures,num_samples):
    pass


def user_prompt_0shot(ts):
    prompt = """Tactic state:
---
%s
---
Next tactic:
---\n""" % (ts)
    return prompt
def user_prompt_fewshot(ts):
    prompt = """Tactic state:
---
α : Type u_1
r : α → α → Prop
inst✝¹ : DecidableEq α
inst✝ : IsIrrefl α r
⊢ CutExpand r ≤ InvImage (Finsupp.Lex (rᶜ ⊓ fun x x_1 => x ≠ x_1) fun x x_1 => x < x_1) ↑toFinsupp
---
Next tactic:
---
rintro s t ⟨u, a, hr, he⟩
---

Tactic state:
---
ι : Type u_1
I✝ J✝ : Box ι
x y : ι → ℝ
I J : WithBot (Box ι)
⊢ ↑I = ↑J ↔ I = J
---
Next tactic:
---
simp only [Subset.antisymm_iff, ← le_antisymm_iff, withBotCoe_subset_iff]
---

Tactic state:
---
m n : ℕ
h : Nat.coprime m n
⊢ Nat.gcd m n = 1
---
Next tactic:
---
rw [← h.gcd_eq_one]
---

Tactic state:
---
%s
---
Next tactic:
---\n""" % (ts)
    return prompt
def post_process_on_general_llm(text):
    if '```lean' in text:
        text = text.split("```lean")[1].split("```")[0].strip()
    for line in text.split("\n"):
        if line.startswith('-- '):
            continue
        else:
            text = line
    return text


def deduplicate_and_sync(texts, scores, llm_labels):
    unique_texts = {}

    for text, score, llm_label in zip(texts, scores, llm_labels):
        if text not in unique_texts:
            unique_texts[text] = {
                'score': score,
                'llm_label': llm_label
            }

    # 提取去重后的结果
    deduplicated_texts = list(unique_texts.keys())
    deduplicated_scores = [unique_texts[text]['score'] for text in deduplicated_texts]
    deduplicated_llm_labels = [unique_texts[text]['llm_label'] for text in deduplicated_texts]

    return deduplicated_texts, deduplicated_scores, deduplicated_llm_labels


def generate_by_virtual_LLM(prompt,temperatures,num_samples):
    # this is the virtual llm

    # i prepare a hand-craft strategy here
    texts, scores,llm_labels = [], [],[]
    llm_list = ['qwen_llm']
    llm_list = ['qwen_ft0','qwen_ft1']
    num_samples_per_llm = math.floor(num_samples/len(llm_list))
    residence = num_samples-num_samples_per_llm*len(llm_list)
    num_samples_list = []
    for i,llm_name in enumerate(llm_list):
        num_sample_i = num_samples_per_llm
        if i==0:
            num_sample_i+=residence
        texts_i,scores_i = globals()['call_'+llm_name](prompt,temperatures,num_sample_i)

        texts+=texts_i
        scores+=scores_i
        llm_labels+=[llm_name for j in range(num_sample_i)]
    texts,scores,llm_labels=deduplicate_and_sync(texts,scores,llm_labels)
    return texts,scores,llm_labels

