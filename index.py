import json

from ai_programs.ai import AiClient


def main():
    ai = AiClient("v4")
    predictions = ai.prediction_rank({
        "title": "サウジアラビアロイヤルカップ",
        "course": {
            "distance": 1600,
            "surface": "芝",
            "direction": "右",
            "position": "外"
        },
        "url": "https://www.jra.go.jp/datafile/seiseki/g1/afs/result/afs2023.html",
        "horse": [
            {
                "waku": "枠1白",
                "umaban": 1,
                "horse": "アルテヴェローチェ",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "佐々木 大輔",
                "h_weight": 448,
                "pop": "1"
            },
            {
                "waku": "枠2黒",
                "umaban": 2,
                "horse": "ニシルノアルノーヴァ",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "永野 猛蔵",
                "h_weight": 470,
                "pop": "5"
            },
            {
                "waku": "枠3赤",
                "umaban": 3,
                "horse": "アルレッキーノ",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "C.ルメール",
                "h_weight": 462,
                "pop": "1"
            },
            {
                "waku": "枠4青",
                "umaban": 4,
                "horse": "マイネルチケット",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "戸崎 圭太",
                "h_weight": 454,
                "pop": "2"
            },
            {
                "waku": "枠5黄",
                "umaban": 5,
                "horse": "タイセイカレント",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "横山 武史",
                "h_weight": 486,
                "pop": "5"
            },
            {
                "waku": "枠6緑",
                "umaban": 6,
                "horse": "シンフォーエバー",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "菅原 明良",
                "h_weight": 496,
                "pop": "2"
            },
            {
                "waku": "枠7橙",
                "umaban": 7,
                "horse": "フードマン",
                "age": "牡2",
                "weight": "56.0",
                "jockey": "松山 弘平",
                "h_weight": 462,
                "pop": "1"
            },
        ]
    })

    for horse in predictions:
        name = horse["name"]
        rank = horse["rank"]
        print(f"{name}: {rank}")

if __name__ == "__main__":
    main()
