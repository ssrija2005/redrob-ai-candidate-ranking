import pandas as pd

print("Starting...")

df = pd.read_csv(r"D:\redrobai\submission_v2.csv")

print("CSV Loaded")

df.to_excel(r"D:\redrobai\submission_v2.xlsx", index=False)

print("XLSX Created")