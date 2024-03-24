from collections import defaultdict


def groupby_unsorted(seq, key=lambda x: x):
    indexes = defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)
