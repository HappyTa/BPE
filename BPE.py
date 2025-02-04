import sys
from collections import Counter


def parser(text: str, sep: str, type=0):
    if not text:
        raise ValueError("No text provided for parser")

    # grab tokens
    tokens = ["_"] + list(set(text.rstrip()))
    tokens.remove(" ")

    # parse text into list
    words = text.rstrip().split(sep)

    word_count = Counter(words)

    corpus = [(list(word) + ["_"], freq) for word, freq in word_count.items()]

    print("Parse corpus successfully!")
    return corpus, tokens


def find_pair_frequencies(corpus):
    """Return all pair of characters and their frequencies in a corpus"""
    frequent_pair = Counter()
    for word, freq in corpus:
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            frequent_pair[pair] += freq

    return frequent_pair


def merge_pair(pair, corpus):
    """Merges the most frequent pair in the corpus."""
    new_corpus = []
    pair_str = "".join(pair)  # Create the new token

    for word, freq in corpus:
        if (
            pair[0] not in word or pair[1] not in word
        ):  # skip word if the pair dont exist
            new_corpus.append((word, freq))
            continue

        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and (word[i], word[i + 1]) == pair:
                new_word.append(pair_str)  # Merge into one token
                i += 2  # Skip merged pair
            else:
                new_word.append(word[i])
                i += 1
        new_corpus.append((new_word, freq))

    return new_corpus


def bpe(corpus, k, tokens: list):
    for _ in range(k):
        pair_freq = find_pair_frequencies(corpus)
        if not pair_freq:
            break

        most_common_pair = max(pair_freq, key=pair_freq.get)  # type: ignore
        new_token = "".join(most_common_pair)
        tokens.append(new_token)
        corpus = merge_pair(most_common_pair, corpus)

        print(f"Merge {most_common_pair} -> {''.join(most_common_pair)}")

    return corpus, tokens


def main():
    # grab text
    if len(sys.argv) != 3:
        raise ValueError("Missing delinimeter and number of merges ")

    sep = sys.argv[1]
    k = int(sys.argv[2])

    # try:
    #     sep = sys.argv[1]
    #     print("Separator recieved...")
    # except Exception as e:
    #     print(f"Error reading stdin: {e}")

    try:
        # Try reading from stdin
        text = sys.stdin.read()
        print("Received text from stdin...")
        print(text)
    except Exception as e:
        print(f"Error reading stdin: {e}")
    # with open("text/test1.txt") as file:
    #     text = file.read().rstrip()

    # parse text
    corpus, tokens = parser(text, sep)  # type: ignore
    print("Initial Corpus")
    for word, freq in corpus:
        print(f"{freq} {' '.join(word)}")
    print(f"Initial tokens: {tokens}\n")

    corpus, tokens = bpe(corpus, k, tokens)

    print("\nFinal Corpus")
    for word, freq in corpus:
        print(f"{freq} {' '.join(word)}")
    print(f"Final tokens: {tokens}\n")

    applyBPE = input("Apply the tokenizer? [Y/n]")
    if applyBPE.upper() == "Y":
        print("apply")
    else:
        print("End")


if __name__ == "__main__":
    main()
