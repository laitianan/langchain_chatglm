# -*- coding: utf-8 -*-
import tiktoken

# simple test
enc = tiktoken.get_encoding("cl100k_base")
print(enc.encode("hello world") == [15339, 1917])
print(enc.decode([15339, 1917]) == "hello world")
print(enc.encode("hello <|endoftext|>", allowed_special="all") == [15339, 220, 100257])

# encode
tokens = enc.encode("tiktoken is great!")
print(tokens)
print(len(tokens))

# decode
print(enc.decode([83, 1609, 5963, 374, 2294, 0]))

# chinese encode
tokens = enc.encode("大模型是什么？")
print(tokens)
print(len(tokens))

# chinese decode
print(enc.decode([2028, 374, 264, 1296, 3319, 13]))
