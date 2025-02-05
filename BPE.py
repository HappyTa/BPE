import sys
from collections import Counter


def parser(text: str, sep: str, type=0):
    if not text:
        raise ValueError("No text provided for parser")

    if type == 0:
        # parse text into list
        words = text.rstrip().split(sep)

        word_count = Counter(words)

        corpus = [(list(word) + ["_"], freq) for word, freq in word_count.items()]

        print("Parse corpus successfully!")

        # grab tokens
        tokens = ["_"] + list(set(text.rstrip()))
        tokens.remove(" ")

        return corpus, tokens

    else:
        words = text.rstrip().split(sep)
        words = [list(word) + ["_"] for word in words]
        return words


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


def bpe(corpus, k, vocab):
    """Use BPE to encode corpus and generate vocab"""

    # Perform k merges
    for i in range(k):
        print(f"==Merge {i+1}")

        # Find most frequent pair of tokens
        pair_freq = find_pair_frequencies(corpus)

        # If no more pair exist, we are done
        if not pair_freq:
            break

        most_common_pair = max(pair_freq, key=pair_freq.get)  # type: ignore
        new_token = "".join(most_common_pair)
        vocab.append(new_token)

        # merge the pair and update corpus
        corpus = merge_pair(most_common_pair, corpus)

        print(f"   Merge {i+1} {most_common_pair} -> {''.join(most_common_pair)}")

        print("    Corpus")
        for word, freq in corpus:  # type: ignore
            print(f"     {freq} {' '.join(word)}")

        print(f"   Vocab: {vocab}")

    return corpus, vocab


def tokenization(words, vocab):
    """Tokenizes input text based on the learned BPE tokens"""

    tokenized_text = []

    # Loop through each word and tokenize it
    for word in words:
        i = 0
        while i < len(word):
            best_match = None
            longest_match = 1

            # Find longest match
            # Basically matching i to j character inside word
            # If that subset of word exist in the vocab then update best_match
            for j in range(i + 1, len(word) + 1):
                token = "".join(word[i:j])  # type: ignore
                if token in vocab:
                    best_match = token
                    longest_match = j - i

            # Append best match if exist, else append the current character.
            # Tokenize the character if we don't know what it is
            if best_match:
                tokenized_text.append(best_match)
                i += longest_match
            else:
                tokenized_text.append(word[i])
                i += 1

    return tokenized_text


def main():
    # grab arguments
    sep = sys.argv[1]
    k = int(sys.argv[2])
    test_num = int(sys.argv[3])

    # grab input text
    with open(f"input/test{test_num}.txt") as file:
        text = file.read().rstrip()

    # parse text
    corpus, vocab = parser(text, sep)  # type: ignore

    print("\nInitial Corpus")

    for word, freq in corpus:  # type: ignore
        print(f"{freq} {' '.join(word)}")
    print(f"Initial vocab: {vocab}\n")

    # Encode the corpus
    corpus, vocab = bpe(corpus, k, vocab)

    print("\nFinal Corpus")

    for word, freq in corpus:  # type: ignore
        print(f"{freq} {' '.join(word)}")
    print(f"Final vocab: {vocab}\n")

    # Check if we to demonstrate tokenization
    if len(sys.argv) == 4:
        sys.exit(0)

    # Tokenization example
    with open(f"input/test{test_num}_s.txt") as file:
        text = file.read().rstrip()

    print("=== Tokenization example ===")

    # parse sample text
    sample_words = parser(text, sep, type=1)

    print("\nInitial sample text")

    for word in sample_words:
        print(f"{' '.join(word)}")  # type: ignore

    # tokenize
    tokens = tokenization(sample_words, vocab)

    print(f"\nTokenized output: {tokens}")


if __name__ == "__main__":
    main()
