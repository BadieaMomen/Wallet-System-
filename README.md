#   Wallet System API  
A secure and scalable electronic wallet system built using **Django**, **Django REST Framework**, and **PostgreSQL**, supporting multi–currency wallets, deposits, withdrawals, balance transfers, and complete transaction tracking.  

This project demonstrates real–world financial operations with strong authentication, authorization, and data validation strategies.

---

##  Table of Contents

1. [Project Overview](#project-overview)  
2. [Core Features](#core-features)  
3. [System Architecture](#system-architecture)  
4. [Entities](#entities)  
5. [Use Cases](#use-cases)  
6. [API Operations](#api-operations)  
7. [Security Strategies](#security-strategies)  
8. [Authentication Flow (JWT)](#authentication-flow-jwt)  
9. [Installation & Setup](#installation--setup)  
10. [Postman Collection](#postman-collection)  
11. [Database Schema / Wallet Logic](#database-schema--wallet-logic)  
12. [Project Structure](#project-structure)  

---

#  Project Overview

This system is an **electronic multi–currency wallet**, allowing users to:

- Create an account  
- Automatically receive a default wallet  
- Deposit money  
- Withdraw money  
- Transfer between wallets  
- Transfer to another user  
- Check full wallet details (balance + currency + owner info)  
- View all related transactions (sent, received, deposits, withdrawals)

The project is built with:

- **Python + Django + DRF** (backend)
- **PostgreSQL** (database)
- **JWT Authentication** (secure login)
- **Postman** (API testing)

---

#  The Features

###  Users Module
- Register using **username**, **phone**, **password**
- Phone number must be **unique**
- Password stored securely
- Login using phone + password
- Receive **Access** and **Refresh** JWT tokens

###  Wallet Module
- Each user automatically gets a wallet when signing up
- Default currency: **YEM**
- Default balance: **0.00**
- Wallet linked to user using One-To-One or ForeignKey

###  Financial Operations
✔ Deposit  
✔ Withdraw  
✔ Transfer to another wallet  
✔ Transfer between your own wallets  
✔ Full validation to prevent misuse  
✔ Full transaction logging  

---

#  System Architecture


|
| One-To-One
v
Wallet
|
| One-To-Many
v
Transaction (Log every action)

# YAML-like flow:
- User registers → Wallet automatically created  
- User logs in → receives JWT tokens  
- Operations validated → Transaction created every time  

---

#  Entities 

### 1 User
- username  
- phone  
- password  
- created_at  
- JWT tokens  

### 2 Wallet
- owner (User)  
- currency (YEM)  
- balance 
- created_at  

### 3 Transaction
- type (DEPOSIT, WITHDRAW, TRANSFER)  
- amount  
- from_wallet  
- to_wallet 
- reference 
- timestamp  
- status (success / failed)

---

#  Use Cases

### ✔ User  
1. Create account  
2. Login  / delete / update 
3. View all wallets  
4. View all transactions  
5. Update or delete account  

### ✔ Wallet  
6. Deposit money  
7. Withdraw money  
8. Transfer money to another wallet    
9. Fetch wallet details  
10. Audit logs & history  

---

#  API Operations (Details)

## 1 User Registration  
- Username required  
- Phone required (unique)  
- Strong password required  
- After creation, system automatically generates a wallet with:
  - Balance = 0.00  
  - Currency = YEM  
  - Status = Active  
  - Linked to the user  

---

## 2 Login (JWT)
User logs in with:

- phone  
- password  

Server returns:

- access token  
- refresh token  

These tokens are required for all protected endpoints.

---

## 3 Deposit

### Requirements:
- Amount  
- Phone number of target wallet  
- Authorization token  

### Server checks:
1. Token valid  
2. Fields exist  
3. Amount is positive  
4. Wallet exists  
5. User owns the wallet  
6. Add to balance  
7. Create transaction record  

---

## 4 Withdraw

Similar to deposit but subtracts amount.

Validation checks include:

- Is amount positive?
- Does wallet have enough balance?
- Is the user the owner?

---

## 5 Transfer  
Transfer money from one wallet to another (your wallet or another user).

### Server performs:

1. Check if user is authenticated  
2. Validate wallets  
3. Check balance  
4. Subtract from sender  
5. Add to receiver  
6. Create transaction record  

---

# 6 Security Strategies

This project implements multiple levels of security:

### 1. **JWT Authentication**
- Access Token: short life  
- Refresh Token: long life  
- Automatic token rotation  
- Strict validation for every request  

### 2. **Authorization Rules**
- Only the owner can:
  - Deposit into his own wallet  
  - Withdraw from his wallet  
  - View wallet details  
  - View his transactions  
- User cannot manipulate another wallet  

### 3. **Input Validation**
- Amount must be positive  
- Wallet must exist  
- Prevent negative deposits  
- Prevent overdraft on withdrawal  
- Phone number must be unique  

### 4. **Database Integrity**
- Foreign key constraints  
- Transactions always logged  
- No operation done without a record  

### 5. **Error Handling**
- Clear error messages  
- Protected endpoints only  
- Only authorized users see financial data  

### 6. **Secure User Model**
- Custom AbstractUser  
- Phone is login field  
- Password hashed by Django  

#  Installation & Setup

### 1 Clone the repository:

git clone https://github.com/BadieaMomen/Wallet-System-.git
cd Wallet-System-


### 2 Install virtual environment:
python -m venv env
env\Scripts\activate

### 3 Install dependencies:
pip install -r requirements.txt


### 4 config pyadmin
config pyadmin that installed from requirements
 with port and username and password thet put ins sitting.py
## 5 migrate
python manage.py makemigrations
python manage.py migrate

### Run server 
python manage.py runserver

#  Postman Collection

A full Postman collection is included inside:  
/postman/wallet-api.postman_collection.json


## the projects 
project/
│
├── accounts/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── urls.py
│
├── wallet/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── urls.py
│
├── postman/
│ └── wallet-api.postman_collection.json
│
├── manage.py
└── requirements.txt




### future improvements may include :
- malti currency exchange 
- use more secure authentications 
- varifide email 
- transfer between the accounts in same users wallet

### ------------------------------ANNND Thank U -----------------------------
