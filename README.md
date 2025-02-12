# 🔐 Salsa20/12 Encryption Algorithm Implementation  

## 📖 Overview  

This project implements the **Salsa20/12 encryption algorithm**, a lightweight and secure stream cipher used for encrypting data. The algorithm is a variant of **Salsa20**, designed for fast and efficient encryption while maintaining strong security properties.  

The provided **Python script (`salsa2012.py`)** contains the implementation of **quarter rounds, row rounds, and column rounds**, which form the core of the Salsa20/12 encryption function.  

---

## 🛠 Technologies Used  

- **Python** – Core implementation language.  
- **NumPy** – Optimized numerical computations for encryption operations.  
- **Struct & Bitwise Operations** – Used for efficient data transformations.  

---

## 📌 Features  

✅ **Implements Salsa20/12 Encryption Algorithm**  
✅ **Fast and Secure Stream Cipher**  
✅ **Lightweight & Efficient for Data Encryption**  
✅ **Python-Based Implementation**  
✅ **Supports 128-bit and 256-bit Encryption Keys**  

---

## 📂 Project Structure  

```
📁 Salsa20-Encryption/
│── salsa2012.py     # Python script implementing Salsa20/12 encryption
│── README.md        # Project documentation
```

---

## 🚀 How It Works  

1️⃣ **Initialize the Salsa20/12 state**  
2️⃣ **Perform quarter-round transformations**  
3️⃣ **Apply row and column rounds for mixing data**  
4️⃣ **Generate keystream for encrypting plaintext**  
5️⃣ **Encrypt or decrypt data using XOR with keystream**  

---

## 🏃 Running the Encryption Script  

### **Encrypting Data**  
```sh
python salsa2012.py --encrypt --input plaintext.txt --output encrypted.bin --key "your-secret-key"
```

### **Decrypting Data**  
```sh
python salsa2012.py --decrypt --input encrypted.bin --output decrypted.txt --key "your-secret-key"
```

This will securely encrypt and decrypt data using Salsa20/12.

---

## 🔐 Security Considerations  

- **Salsa20/12 is resistant to known cryptanalysis attacks.**  
- **The 12-round variant is a trade-off between speed and security.**  
- **Always use a unique nonce to prevent repetition in encryption.**  

---

## 🔮 Future Enhancements  

🔹 **Expand to Full Salsa20 Implementation (20 Rounds)**  
🔹 **Integrate ChaCha20 Encryption**  
🔹 **Support for File Encryption & Secure Key Management**  
🔹 **Performance Optimizations for Large Data Sets**  

---

## 📜 References  

- [Salsa20 Research Paper](https://cr.yp.to/snuffle.html)  
- [NumPy Documentation](https://numpy.org/doc/)  
- [Cryptography in Python](https://cryptography.io/)  

---

## 📧 Contact  

**Author:** Siddartha Reddy Boreddy  
📍 **SUNY Binghamton**  
✉️ **Email:** sboreddy@binghamton.edu 

---

### ⭐ If you find this project helpful, feel free to star the repository! 🚀  
