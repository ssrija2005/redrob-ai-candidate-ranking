import json

candidates = []

with open("C:/Users/srija/Downloads/[PUB] India_runs_data_and_ai_challenge/[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/candidates.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        candidates.append(json.loads(line))


print("Candidates Loaded:", len(candidates))

def score_candidate(candidate):

    score = 0

    years = candidate["profile"]["years_of_experience"]

    # JD prefers 5-9 years
    if 5 <= years <= 9:
        score += 20

    skills = [s["name"].lower() for s in candidate["skills"]]

    important_skills = [
        "nlp",
        "milvus",
        "lora",
        "fine-tuning llms",
        "python"
    ]

    for skill in important_skills:
        if skill in skills:
            score += 10

    return score

def career_score(candidate):

    score = 0

    strong_keywords = [
        "retrieval",
        "ranking",
        "recommendation",
        "vector database",
        "embedding",
        "semantic search",
        "llm",
        "machine learning",
        "nlp"
    ]

    medium_keywords = [
        "python",
        "data pipeline",
        "analytics",
        "api"
    ]

    for job in candidate["career_history"]:
        desc = job.get("description", "").lower()

        for kw in strong_keywords:
            if kw in desc:
                score += 8

        for kw in medium_keywords:
            if kw in desc:
                score += 3

    return min(score, 40)

def title_penalty(candidate):

    title = candidate["profile"]["current_title"].lower()

    bad_titles = [
        "marketing",
        "operations",
        "accountant",
        "customer support",
        "hr",
        "sales",
        "civil engineer",
        "mechanical engineer"
    ]

    penalty = 0

    for bad in bad_titles:
        if bad in title:
            penalty += 15

    return penalty

def signal_score(candidate):

    signals = candidate["redrob_signals"]

    score = 0

    if signals["open_to_work_flag"]:
        score += 10

    if signals["interview_completion_rate"] > 0.7:
        score += 10

    if signals["recruiter_response_rate"] > 0.4:
        score += 10

    if signals["notice_period_days"] <= 30:
        score += 10

    return score

def title_bonus(candidate):

    title = candidate["profile"]["current_title"].lower()

    good_titles = [
        "ai engineer",
        "machine learning",
        "data scientist",
        "data engineer",
        "backend engineer",
        "software engineer",
        "ml engineer"
    ]

    for t in good_titles:
        if t in title:
            return 15

    return 0

def relevance_multiplier(candidate):

    title = candidate["profile"]["current_title"].lower()

    strong = [
        "ai engineer",
        "machine learning",
        "ml engineer",
        "recommendation",
        "data scientist",
        "data engineer",
        "backend engineer",
        "software engineer"
    ]

    medium = [
        "java developer",
        ".net developer",
        "cloud engineer",
        "full stack developer",
        "frontend engineer"
    ]

    for role in strong:
        if role in title:
            return 1.25

    for role in medium:
        if role in title:
            return 1.0

    return 0.5

def ai_bonus(candidate):

    skills = [s["name"].lower() for s in candidate["skills"]]

    bonus = 0

    ai_skills = [
        "nlp",
        "fine-tuning llms",
        "lora",
        "rag",
        "embeddings",
        "milvus",
        "faiss",
        "pinecone",
        "vector databases",
        "recommendation systems"
    ]

    for skill in ai_skills:
        if skill in skills:
            bonus += 3

    return min(bonus, 20)

def retrieval_bonus(candidate):

    skills = [s["name"].lower() for s in candidate["skills"]]

    retrieval_skills = [
        "information retrieval",
        "learning to rank",
        "recommendation systems",
        "bm25",
        "faiss",
        "pinecone",
        "milvus",
        "weaviate",
        "elasticsearch",
        "opensearch"
    ]

    bonus = 0

    for skill in retrieval_skills:
        if skill in skills:
            bonus += 2

    return min(bonus, 15)


for candidate in candidates:

    technical = score_candidate(candidate)
    career = career_score(candidate)
    signal = signal_score(candidate)
    bonus = title_bonus(candidate)
    penalty = title_penalty(candidate)

    score = (
    technical
    + career
    + signal
    + bonus
    + ai_bonus(candidate)
    + retrieval_bonus(candidate)
    - penalty
)

    score *= relevance_multiplier(candidate)

    candidate["score"] = score


# SORT AFTER ALL CANDIDATES ARE SCORED
ranked = sorted(
    candidates,
    key=lambda x: x["score"],
    reverse=True
)

print("\nTOP 20 CANDIDATES\n")

for c in ranked[:20]:
    print(
        c["candidate_id"],
        c["profile"]["current_title"],
        c["score"]
    )

for c in ranked[:5]:
    print("\n")
    print(c["candidate_id"])
    print(c["profile"]["current_title"])
    print(c["profile"]["years_of_experience"])

    print("Skills:")
    print([s["name"] for s in c["skills"][:15]])   

import csv

with open("submission_v2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, c in enumerate(ranked[:100], start=1):
        writer.writerow([
            c["candidate_id"],
            rank,
            round(c["score"], 2),
            "Strong AI/ML experience, relevant career history and behavioral signals"
        ])

print("submission_v2.csv created successfully!")  


from collections import Counter

titles = [
    c["profile"]["current_title"]
    for c in ranked[:100]
]

counter = Counter(titles)

for title, count in counter.most_common(30):
    print(f"{count:3} - {title}")

retrieval_skills = [
    "information retrieval",
    "learning to rank",
    "recommendation systems",
    "bm25",
    "faiss",
    "pinecone",
    "milvus",
    "weaviate",
    "elasticsearch",
    "opensearch",
]

count = 0

for c in ranked[:100]:
    skills = [s["name"].lower() for s in c["skills"]]

    if any(skill in skills for skill in retrieval_skills):
        count += 1

print("Top 100 with retrieval/ranking skills:", count)

for c in ranked[:20]:
    print(
        c["candidate_id"],
        c["profile"]["current_title"],
        c["score"]
    )