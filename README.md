# Byte Pair Encoding Learning Project

This repo was made to store my implementation of *Byte Pair Encoding* (BPE).

**Byte Pair Encoding**: A corpus based tokenizer that focus on the *Morphemes* of the word.

Properties of BPE:

- Uses the training data to define how to tokenize.
- Tend to only pick frequent words, and frequent subwords (i.e. Morphemes).

## TODO

- [x] Implement BPE
- [x] Implement tokenizer

## How to run

```
python3 -O BPE.py [Seperator] [K-count] [Test File Number]
```

- *Seperator*: The seperator used by the test file
- *K-count*: The number of merges BPE will do
- *Test File Number*: the number of the test file
- (optional) ```-O```: Tell the script to not run in debug mode (less verbose)
