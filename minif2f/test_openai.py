import os

import openai
print(os.environ)
from minif2f.proofsearch_qwenmax import generate_vllm

prompt='''Tactic state:
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
x y : ℕ
h₀ : 0 < x ∧ 0 < y
h₁ : x ^ y ^ 2 = y ^ x
⊢ (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3)
---
Next tactic:
---
'''

print(generate_vllm(prompt,None,None,[1],10,None))