import binascii, codecs, base64

def XORBreak(h):
    en = binascii.unhexlify(h)
    for key in range(256):
        de = ''.join(chr(b ^ key) for b in en)
        if de.isprintable():
            print(de)

def xor_decrypt(cipher_text,key):
    num_list = [ord(char) ^ key for char in cipher_text]
    return ''.join([num.to_bytes((num.bit_length()+7) // 8, 'big').decode() for num in num_list])

file = open('file.txt', 'r')
file = file.readlines()
truc=0
for line in file:
    truc += 1
    if truc == 2:
        exit()

    # for i in range(250):
    try:
        # XORBreak(line)
        base64_hex_code = codecs.encode(codecs.decode(line.strip(), 'hex'), 'base64').decode()
        print(base64_hex_code)
        # xored = xor_decrypt(base64_hex_code, i)
        # print(xored, '\n---------------------------------------------')
        # decoded_base64 = base64.b64decode(line)
        # print(decoded_base64)

    except Exception as e:
        print(e)
        continue