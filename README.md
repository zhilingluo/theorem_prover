# theorem_prover
Contributing to formal theorem proving in GitHub repos

## Goal
- Contributing theorem proving to [Lean-Matrix-Cookbook](https://github.com/eric-wieser/lean-matrix-cookbook) 
- Contributing theorem proving in [PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd)

## Roadmap
1) Basic architecture: 
   2) Lean-dojo + searching + enhanced LLM for lean theorem proving, verify it on simple benchmarks: minif2f
   3) a solution to translate informal theorem into formal one (in Lean 4)


## Process

I proposed a reinforcement learning framework to iteratively optimize the pretrained LLM by rolling out next tactics and comparing them with the expected ones. The experiment results show that it helps to achieve a higher accuracy compared with directly fine-tuned LLM.

My model proved 13 theorems of 30 in minif2f. 👏🏻

| |#Positive sample on MiniF2F | Acc on MiniF2F | Acc on Trainset |
|-----|-----------|---------|-----|
|Lean-qwen0.5B-sft | 11 | 36% |  49% |
|Lean-qwen0.5B-rl | 13 | 43\% | 61% |


[tech report](https://arxiv.org/abs/2502.08908)


## Models

[Lean-qwen0.5b-sft](https://www.modelscope.cn/models/mengxin1942/lean-qwen0.5b-sft/)

[Lean-qwen0.5b-rl](https://www.modelscope.cn/models/mengxin1942/lean-qwen0.5b-rl/)

## Citation
```bibtex
@article{lean-reinforced-llm,
      title={Reinforced Large Language Model is a formal theorem prover}, 
      author={Zhiling Luo},
      year={2025},
      journal={arXiv preprint arXiv:2502.08908},
      url={https://arxiv.org/abs/2502.08908},
      primaryClass={cs.AI}
}
```

## Ref

[Ref](/ref.md)

