import sys
from collections import Counter


def parser(input: str, sep: str, type=0):
    if not input:
        raise ValueError("No input provided for parser")

    # parse input into list
    words = input.rstrip().split(sep)

    word_count = Counter(words)
    corpus = {count: list(word) + ["_"] for word, count in word_count.items()}

    print("Parse corpus successfully!")
    return corpus


def main():
    # grab input
    try:
        sep = sys.argv[1]
        print("Separator recieved...")
    except Exception as e:
        print(f"Error reading stdin: {e}")

    try:
        # Try reading from stdin
        input = sys.stdin.read()
        print("Received input from stdin...")
        print(input)
    except Exception as e:
        print(f"Error reading stdin: {e}")

    # parse input
    corpus = parser(input, sep)  # type: ignore
    print(corpus)


if __name__ == "__main__":
    main()
