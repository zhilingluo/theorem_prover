#

# from pathlib import Path
# from lean_dojo import LeanGitRepo, trace
# repo = LeanGitRepo.from_path(Path('../lean-dojo-mew'))
# trace(repo,dst_dir="traced_lean4-example")
#repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f")
#trace(repo, dst_dir="traced_lean4-example")

from lean_dojo import *

repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f")
theorem = Theorem(repo, "Lean4Example.lean", "hello_world")

with Dojo(theorem) as (dojo, init_state):
  print(init_state)
  result = dojo.run_tac(init_state, "rw [add_assoc, add_comm b, ←add_assoc]")
  assert isinstance(result, ProofFinished)
  print(result)