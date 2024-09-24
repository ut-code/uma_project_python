import json

from ai_programs.ai import AiClient


def main():
    ai = AiClient()
    ai.predict_rank("beta1", json.dumps({
        "horse": [
            {
                "umaban": "1",
                "horse": "Horse A",
                "age": "3",
                "weight": "500",
                "jockey": "Jockey A",
                "time": "1:30",
                "h_weight": "500",
                "f_time": "1:32",
                "pop": "5"
            },
            {
                "umaban": "2",
                "horse": "Horse B",
                "age": "4",
                "weight": "480",
                "jockey": "Jockey B",
                "time": "1:31",
                "h_weight": "480",
                "f_time": "1:33",
                "pop": "3"
            }
        ]
    }))
#    ai.createModel("beta1")


if __name__ == "__main__":
    main()
