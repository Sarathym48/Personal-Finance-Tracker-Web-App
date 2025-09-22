# Personal Finance Tracker Web App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-success)
![MySQL](https://img.shields.io/badge/database-MySQL-lightgrey)

## Overview

This project is a **personal finance management web application** that allows users to **track, categorize, and manage their financial transactions** securely. It demonstrates **full-stack development** with a Flask backend, MySQL database, and responsive HTML/CSS frontend.

Key functionalities include:
- **CRUD operations** for transactions (Add, Edit, Delete, View)  
- **Categorized transaction tracking**  
- **User authentication** for secure access  
- **RESTful API endpoints** for backend integration  

---

## Features

- **Add, Edit, Delete, and View Transactions**  
- **Categorized Transactions** for better financial insight  
- **User Authentication & Secure Login**  
- **SQL-based Data Management (MySQL)**  
- **RESTful API Endpoints** for frontend-backend interaction  
- **Responsive HTML/CSS Frontend**  
- **Version Control with Git/GitHub**  

---

## Tools & Technologies

- **Python 3.10+**  
- **Flask**  
- **MySQL**  
- **HTML & CSS**  
- **Git/GitHub**  

---

## Screenshots

**Login Page**  
![Login Page](1(1).png)  

**Dashboard / Transactions Overview**  
![Dashboard](1(2).png)  

**Add Transaction Form**  
![Add Transaction](1(3).png)  

> *Create a folder named `screenshots` in the root of your repo and upload your images there. Replace the placeholders with actual screenshots.*

---

## System Architecture

```mermaid
flowchart TD
    UI[UI - HTML/CSS] --> FLASK[Flask Backend]
    FLASK --> AUTH[User Auth Module]
    FLASK --> CRUD[Transaction CRUD Module]
    FLASK --> API[REST API Endpoints]
    AUTH --> DB_USERS[MySQL Users Table]
    CRUD --> DB_TRANSACTIONS[MySQL Transactions Table]
    API --> DB[MySQL Database]
    DB --> FLASK
    FLASK --> UI
