import pandas as pd

df = pd.read_parquet("hf://datasets/internlm/Lean-Workbook/wkbk_1009.parquet")
print(df)