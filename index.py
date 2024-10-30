import json
import os

from ai_programs.ai import AiClient

def main():
    ai = AiClient("v4")
    files = os.listdir("db/jra")
    for f in files:
        loaded = load_data(f"db/jra/{f}")
        data = {
            "title": loaded["title"],
            "course": loaded["course"],
	        "horse": [],
        }
        for horse in loaded["horse"]:
            data["horse"].append({
                "horse": horse["horse"],
                "age": horse["age"],
                "jockey": horse["jockey"],
                "pop": horse["pop"],
                "weight": horse["weight"],
                "h_weight": horse["h_weight"],
                "waku": horse["waku"],
                "umaban": horse["umaban"],
            })
        predictions = {
            "title": loaded["title"],
            "url": loaded["url"],
            "horse": ai.prediction_rank(data)
        }

        write_file(f"db/predictions/{f}", json.dumps(predictions, indent=4, ensure_ascii=False))

def load_data(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as f:
        return json.loads(f.read())
def write_file(file_path: str, content: str):
    with open(file_path, "w", encoding="UTF-8") as f:
        return f.write(content)

if __name__ == "__main__":
    main()
