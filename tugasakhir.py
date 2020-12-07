from flask import Flask, render_template, request
from datetime import datetime
import random 
import string
import math 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/check', methods=['POST'])
def check():
    text = request.form['tex']
    s = int(request.form['s']) 
    key = request.form['key']
    hasil = ""
    if request.form['action'] == "Dekripsi":
        hasil = decrypt(text,s,key) 
        return render_template("hasil.html" , result = hasil)
    elif request.form['action'] == "Enkripsi":
        hasil = encrypt(text,s,key)
        return render_template("hasil.html" , result = hasil)

def encryptMessage(msg,key): 
    cipher = "" 
  
    # track key indices 
    k_indx = 0
  
    msg_len = float(len(msg)) 
    msg_lst = list(msg) 
    key_lst = sorted(list(key)) 
  
    # calculate column of the matrix 
    col = len(key)  
    row = int(math.ceil(msg_len / col)) 
  
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

#enkripsi shift
def encrypt(text,s,key):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text  
        if (char.isupper()):
            c_idx = ord(char) - ord('A')
            new = (c_idx + s) % 26
            result += chr(new + ord('A'))
    hasil = encryptMessage(result,key)
    return hasil
  
# Encryption columnar

  
# Decryption columnar
def decryptMessage(text,key): 
    msg = "" 
  
    # track key indices 
    k_indx = 0
  
    # track msg indices 
    msg_indx = 0
    msg_len = float(len(text)) 
    msg_lst = list(text) 
  
    # calculate column of the matrix 
    col = len(key) 
      
    # calculate maximum row of the matrix 
    row = int(math.ceil(msg_len / col)) 
    key_lst = sorted(list(key)) 
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
def decrypt(text,s,key):
    # transverse the plain text
    hasildekrip = format(decryptMessage(text,key))
    result = ""
    for i in range(len(hasildekrip)):
        char = hasildekrip[i]
        # Encrypt uppercase characters in plain text  
        if (char.isupper()):
            c_i = ord(char) - ord('A')
            c_post = (c_i - s) % 26 + ord('A')
            result += chr(c_post)
    return result

if __name__ == '__main__':
  app.run(debug=True)