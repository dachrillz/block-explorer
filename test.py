hello='01000000'
hej='8a730974ac39042e95f82d719550e224c1a680a8dc9e8df9d007000000000000'

# 00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a

def _from_little_endian(s):
    return ''.join([c[1] + c[0] for c in zip(s[::2], s[1::2])])[::-1]

a = _from_little_endian(hello)
b = _from_little_endian(hej)

print(a)
print(b)


