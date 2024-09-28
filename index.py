import json

from ai_programs.ai import AiClient


def main():
    ai = AiClient("v1")
    ai.createModel()

if __name__ == "__main__":
    main()
