from flask import Flask, render_template, request
from datetime import datetime
import random 
import string
import math 

app = Flask(__name__)

@app.route('/')
def index():
    key = get_random_string(4)
    s = random.randint(0,26) 
    return render_template("home.html",key=key,s=s)

@app.route('/encrypt', methods=['POST'])
#enkripsi shift
def encrypt():
    text = request.form['tex']
    s = request.form['s'] 
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text  
        if (char.isupper()):
            result = result + chr((ord(char) + (26-s)-65) % 26 + 65)
    return render_template("hasil.html",result=result)
  
# Encryption columnar
def encryptMessage(msg,key): 
    cipher = "" 
  
    # track key indices 
    k_indx = 0
  
    msg_len = float(len(msg)) 
    msg_lst = list(msg) 
    key_lst = sorted(list(key)) 
  
    # calculate column of the matrix 
    col = len(key) 
      
    # calculate maximum row of the matrix 
    row = int(math.ceil(msg_len / col)) 
  
    # add the padding character '_' in empty 
    # the empty cell of the matix  
    fill_null = int((row * col) - msg_len) 
    msg_lst.extend('_' * fill_null) 
  
    # create Matrix and insert message and  
    # padding characters row-wise  
    matrix = [msg_lst[i: i + col]  
              for i in range(0, len(msg_lst), col)] 
  
    # read matrix column-wise using key 
    for _ in range(col): 
        curr_idx = key.index(key_lst[k_indx]) 
        cipher += ''.join([row[curr_idx]  
                          for row in matrix]) 
        k_indx += 1
  
    return cipher 
  
# Decryption columnar
def decryptMessage(cipher,key): 
    msg = "" 
  
    # track key indices 
    k_indx = 0
  
    # track msg indices 
    msg_indx = 0
    msg_len = float(len(cipher)) 
    msg_lst = list(cipher) 
  
    # calculate column of the matrix 
    col = len(key) 
      
    # calculate maximum row of the matrix 
    row = int(math.ceil(msg_len / col)) 
  
    # convert key into list and sort  
    # alphabetically so we can access  
    # each character by its alphabetical position. 
    key_lst = sorted(list(key)) 
  
    # create an empty matrix to  
    # store deciphered message 
    dec_cipher = [] 
    for _ in range(row): 
        dec_cipher += [[None] * col] 
  
    # Arrange the matrix column wise according  
    # to permutation order by adding into new matrix 
    for _ in range(col): 
        curr_idx = key.index(key_lst[k_indx]) 
  
        for j in range(row): 
            dec_cipher[j][curr_idx] = msg_lst[msg_indx] 
            msg_indx += 1
        k_indx += 1
  
    # convert decrypted msg matrix into a string 
    try: 
        msg = ''.join(sum(dec_cipher, [])) 
    except TypeError: 
        raise TypeError("This program cannot", 
                        "handle repeating words.") 
  
    null_count = msg.count('_') 
  
    if null_count > 0: 
        return msg[: -null_count] 
  
    return msg 

#Decrypt shift
def decrypt(text,s):
   result = ""
   # transverse the plain text
   for i in range(len(text)):
      char = text[i]
      # Encrypt uppercase characters in plain text  
      if (char.isupper()):
         result += chr(((ord(char) - (26)-65) % 26 + 65))
      # Encrypt lowercase characters in plain text
    #   else:
    #      result += chr((ord(char) + s - 97) % 26 + 97)
   return result

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str  



# Driver Code 
# msg = "Geeks for Geeks"
  
# cipher = encryptMessage(msg) 
# print("Encrypted Message: {}". 
#                format(cipher)) 
  
# print("Decryped Message: {}". 
#        format(decryptMessage(cipher))) 
  
# text = input("Masukkan Pesan : ")



if __name__ == '__main__':
  app.run(debug=True)