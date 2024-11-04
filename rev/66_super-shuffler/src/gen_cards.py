import random
import collections

WORD_LIST = [
    'FndShp',
    '/bin/sh',
]

if __name__ == '__main__':
    max_chars = {}
    for word in WORD_LIST:
        counter = collections.Counter(word)
        for key in counter:
            max_chars[key] = max(max_chars.get(key, 0), counter.get(key))
    charset = []
    for key in max_chars:
        for i in range(max_chars[key]):
            charset.append(key)
    print(f'Charset: {charset}')
    random.shuffle(charset)
    out = ''.join(charset)
    print(out)
    print(len(out))
    