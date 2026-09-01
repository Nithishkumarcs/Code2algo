# 🚀 Code2Algo – Intelligent Code-to-Algorithm Generator

<p align="center">
  <b>Transform Source Code into Clear, Structured Algorithms Automatically</b>
</p>

<p align="center">
  <a href="https://code2algo-1.onrender.com/" target="_blank">
    🌐 <b>Live Demo</b>
  </a>
</p>

---

## 📌 Overview

**Code2Algo** is a web-based developer and learning tool that automatically analyzes source code and converts it into a clear, structured, step-by-step algorithm.

The system accepts source code as input, analyzes its logic and control flow, and generates an easy-to-understand algorithm representation along with complexity information.

It is designed to help:

- 👨‍💻 Developers understand unfamiliar code
- 🎓 Students learn algorithms and programming logic
- 📚 Educators explain program execution
- 🔍 Beginners convert code into algorithmic steps
- ⚡ Developers analyze code structure quickly

---

## ✨ Key Features

### 🧠 Code-to-Algorithm Conversion
Automatically converts source code into structured, human-readable algorithm steps.

### 🌍 Multi-Language Code Support
Designed to work with multiple programming languages and source-code formats.

### 📊 Complexity Analysis
Provides algorithmic complexity information such as:

- Time Complexity
- Space Complexity
- Big-O representation

### 🔍 Code Analysis
Analyzes source-code structure including:

- Variables
- Conditions
- Loops
- Functions
- Control flow
- Logical operations

### 🎯 Example Programs
The project includes sample programs for testing and demonstration.

Supported examples include:

- Python
- Java
- JavaScript
- C++
- C#
- PHP

### 🌐 Web-Based Interface
Users can enter source code through a simple browser-based interface and receive generated algorithm results.

### 🔌 REST API
The backend exposes API endpoints for code analysis and algorithm generation.

### 🧪 Testing
Automated tests are included to validate API and analyzer functionality.

### 🚀 Cloud Deployment
The application is deployed online and can be accessed through the live demo.

---

## 🌐 Live Demo

👉 **Try Code2Algo Online:**

https://code2algo-1.onrender.com/

> Note: The application is deployed using Render. If the service is inactive, the first request may take a few seconds to start.

---

## 🏗️ Project Architecture

```text
Code2Algo/
│
├── backend/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── algorithm_generator.py
│   ├── analyzer.py
│   └── complexity_analyzer.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── examples/
│   ├── cpp_binarysearch.cpp
│   ├── csharp_grades.cs
│   ├── java_bubblesort.java
│   ├── javascript_fibonacci.js
│   ├── php_calculator.php
│   ├── python_factorial.py
│   └── python_prime.py
│
├── tests/
│   ├── test_analyzer.py
│   └── test_api.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
