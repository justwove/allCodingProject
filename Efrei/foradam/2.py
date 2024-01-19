import base64
from nltk.corpus import words
word_list = words.words()

def xor_decrypt(cipher_text,key):
    num_list = [ord(char) ^ key for char in cipher_text]
    return ''.join([num.to_bytes((num.bit_length()+7) // 8, 'big').decode() for num in num_list])


file = open('file.txt', 'r')
file = file.readlines()
truc = 0
char = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']

for line in file:
    truc += 1
    try:
        for n in char:
            decrypt_word = xor_decrypt(line,n)
            print(truc, decrypt_word)
            print('------------------------------------------------------------------------------------')
            print('\n')
            print(n)
            print(decrypt_word)
            print('\n')

    except Exception as e:
        print(e)
        continue