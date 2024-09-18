import torch

from ai_programs.ai import AiClient

def main():
    ai = AiClient()
    print(torch.__version__)

if __name__ == "__main__":
    main()
