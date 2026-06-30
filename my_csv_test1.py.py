import json

with open("C:/Users/srija/Downloads/[PUB] India_runs_data_and_ai_challenge/[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/candidates.jsonl", "r", encoding="utf-8") as f:
    first_candidate = json.loads(next(f))

print(first_candidate["candidate_id"])
