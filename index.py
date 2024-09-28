import json

from ai_programs.ai import AiClient


def main():
    ai = AiClient("beta2")
    ai.createModel()

if __name__ == "__main__":
    main()
