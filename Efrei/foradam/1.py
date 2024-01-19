import base64, codecs

hex_code = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

base64_hex_code = codecs.encode(codecs.decode(hex_code, 'hex'), 'base64').decode()
print(base64_hex_code)

def xor_decrypt(cipher_text,key):
    num_list = [ord(char) ^ key for char in cipher_text]
    return ''.join([num.to_bytes((num.bit_length()+7) // 8, 'big').decode() for num in num_list])

