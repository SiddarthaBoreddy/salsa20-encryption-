import numpy 
import struct
import sys

def rotate_left(val, shift):
    return ((val << shift) & 0xFFFFFFFF) | ((val & 0xFFFFFFFF) >> (32 - shift))


def quarter_round(var0, var1, var2, var3):
    result_array = numpy.zeros(4, dtype=numpy.int32)
    result_array[1] = var1 ^ rotate_left((numpy.array(var0).astype(numpy.int32) + numpy.array(var3).astype(numpy.int32)), 7)
    result_array[2] = var2 ^ rotate_left((result_array[1] + numpy.array(var0).astype(numpy.int32)), 9)
    result_array[3] = var3 ^ rotate_left((result_array[2] + result_array[1]), 13)
    result_array[0] = var0 ^ rotate_left((result_array[3] + result_array[2]), 18)
    #print(result_array)
    return result_array
    

def row_round(input_array):
    result_array = [0] * 16
    
   
    quarter_round_0 = quarter_round(input_array[0], input_array[1], input_array[2], input_array[3])
    result_array[0], result_array[1], result_array[2], result_array[3] = quarter_round_0
    
    quarter_round_1 = quarter_round(input_array[5], input_array[6], input_array[7], input_array[4])
    result_array[5], result_array[6], result_array[7], result_array[4] = quarter_round_1
    
    quarter_round_2 = quarter_round(input_array[10], input_array[11], input_array[8], input_array[9])
    result_array[10], result_array[11], result_array[8], result_array[9] = quarter_round_2
    
    quarter_round_3 = quarter_round(input_array[15], input_array[12], input_array[13], input_array[14])
    result_array[15], result_array[12], result_array[13], result_array[14] = quarter_round_3
    
    return result_array



def column_round(state):
    result_array = [0] * 16
    
    # Call quarter_round function for each column
    quarter_round_0 = quarter_round(state[0], state[4], state[8], state[12])
    result_array[0], result_array[4], result_array[8], result_array[12] = quarter_round_0
    
    quarter_round_1 = quarter_round(state[5], state[9], state[13], state[1])
    result_array[5], result_array[9], result_array[13], result_array[1] = quarter_round_1
    
    quarter_round_2 = quarter_round(state[10], state[14], state[2], state[6])
    result_array[10], result_array[14], result_array[2], result_array[6] = quarter_round_2
    
    quarter_round_3 = quarter_round(state[15], state[3], state[7], state[11])
    result_array[15], result_array[3], result_array[7], result_array[11] = quarter_round_3
    
    return result_array


def doubleround(state):

    return row_round(column_round(state))

def littleendian(b):
    signed_int = struct.unpack('<i', bytes(b))[0]
    
    #print(signed_int)
    return signed_int
   


def littleendian_inverse(word):

    b0 = word & 0xFF
    b1 = (word >> 8) & 0xFF
    b2 = (word >> 16) & 0xFF
    b3 = (word >> 24) & 0xFF
    #print(b0, b1, b2, b3)
    return b0, b1, b2, b3

def doubleround10(x):
   
    for _ in range(6):
        x = doubleround(x)
    return x

def salsa20_hash(x):
   
    result = []
    
    words = [littleendian(x[i:i+4]) for i in range(0, len(x), 4)]

    result_words = words
    
    result_words = doubleround10(words)
    for i in range (len(words)):
        inv_words = littleendian_inverse(result_words[i]+words[i])

        result.extend(inv_words)
    #print(result)
    return (result)




def expansion_8_byte(k, n):
    
    alpha0 = (101, 120, 112, 97)
    alpha1 = (110, 100, 32, 48)
    alpha2 = (56, 45, 98, 121)
    alpha3 = (116, 101, 32, 107)

    n = n[:16]
   
    padding_length = 16 - len(n)
    
    n += bytes([0] * padding_length)
    result =  alpha0 + tuple(k) +tuple(k)+ alpha1 + tuple(n) + alpha2 + tuple(k) + tuple(k) + alpha3    
    #print(result)
    return salsa20_hash(result)

def expansion_16_byte(k, n):

    tau0 = (101, 120, 112, 97)
    tau1 = (110, 100, 32, 49)
    tau2 = (54, 45, 98, 121)
    tau3 = (116, 101, 32, 107)
 
    
    n = n[:16]
   
    padding_length = 16 - len(n)
    
    n += bytes([0] * padding_length)
    result =  tau0 + tuple(k) + tau1 + tuple(n) + tau2 + tuple(k) + tau3
    #print(result)
    return salsa20_hash(result)

def expansion_32_byte(k, n):
    """
    Performs the Salsa20 expansion function for 32-byte key.
    """
    sigma0 = (101, 120, 112, 97)
    sigma1 = (110, 100, 32, 51)
    sigma2 = (50, 45, 98, 121)
    sigma3 = (116, 101, 32, 107)

    n = n[:16]
   
    padding_length = 16 - len(n)
    
    n += bytes([0] * padding_length)
    result =  sigma0 + tuple(k[:16]) + sigma1 + tuple(n) + sigma2 + tuple(k[16:]) + sigma3
    #print(result)
    return salsa20_hash(result)

 
def salsa20_encryption(keylen, key, nonce, message):
    stream_index = 0
    n = nonce[:]
    encrypted = message[:]

   

    for i in range(len(message)):
        if (stream_index + i) % 64 == 0:
            if keylen == 8:
                keystream = expansion_8_byte(key, n)
            elif keylen == 16:
                keystream = expansion_16_byte(key, n)
            elif keylen == 32:
                keystream = expansion_32_byte(key, n)
        #print(keystream)

        encrypted[i] ^= keystream[(stream_index + i) % 64]
        

    #print("salsa20Encryption -->", encrypted)
    return encrypted



def main():
    # Input
    #keylen = 256
    keylen = int(sys.argv[1])
    key_length_bytes = keylen // 8
    #print(key_length_bytes)
    #hexadecimal_key = "fb423b4a0be74f7d1e5091158b5b2a510d1e5161dc7ab8dfd495d19949adf3a3"
    hexadecimal_key = sys.argv[2]
    
    int_key = [int(hexadecimal_key[i:i+2], 16) for i in range(0, len(hexadecimal_key), 2)]
    #print(int_key)
    #nonce = "11d4d7e4e368c8e9"
    hexadecimal_nonce = sys.argv[3]
    int_nonce = [int(hexadecimal_nonce[i:i+2], 16) for i in range(0, len(hexadecimal_nonce), 2)]
    #print(int_nonce)
    #hexadecimal_message = "54686973697364656372797074656474657874"
    hexadecimal_message = sys.argv[4]

    int_msg = [int(hexadecimal_message[i:i+2], 16) for i in range(0, len(hexadecimal_message), 2)]
    #print(int_msg)

    

    

    # Encryption
    encrypted_output = salsa20_encryption(key_length_bytes, int_key, int_nonce, int_msg)

    #print(hexadecimal_message)
    #print("Encrypted Output:", encrypted_output)

# Convert the list of integers to a hexadecimal string
    hexadecimal_output = ''.join([hex(x)[2:].zfill(2) for x in encrypted_output])

    print("Encryption(Cipher Text):", hexadecimal_output)


    # Decryption
    decrypted_output = salsa20_encryption(key_length_bytes, int_key, int_nonce, encrypted_output)
    hexadecimal_Dec_output = ''.join([hex(x)[2:].zfill(2) for x in decrypted_output])

    #print("Decryption(Plain Text):", hexadecimal_Dec_output)
    #print("Encrypted Output:", encrypted_output)

    # Check if decryption is correct
    #original_message = bytes.fromhex(hexadecimal_message).decode('utf-8')
    #print("Decryption matches original message:", decrypted_output == original_message)

if __name__ == "__main__":
    main()
