## 🚀 Live Demo

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://code2algo-1.onrender.com/)

Experience Code2Algo live:
**https://code2algo-1.onrender.com/**



Code2Algo — Intelligent Code-to-Algorithm Generator
License: MIT Python 3.9+ Flask REST API GitHub Ready

Code2Algo is a professional, full-stack web application designed to automatically analyze source code across 17 programming languages and transform it into structured step-by-step algorithms, standard pseudocode, conceptual explanations, time/space complexity estimations, and input/output specifications.

🌟 Features
Multi-Language Support (17 Languages): Python, JavaScript, TypeScript, Java, C++, C, C#, Go (Golang), Rust, Kotlin, Swift, PHP, Ruby, Dart, Scala, R, and SQL.
Selectable Detail Levels: Customize algorithm granularity across Small, Medium, and Professional modes.
Algorithmic Step Extraction: Generates dynamic 1...N logical execution steps (including academic sub-steps).
Standard Pseudocode Generator: Outputs clean UPPERCASE pseudocode reflecting control flow.
Interactive Program Flowcharts: Automatically synthesizes and renders vector Mermaid.js flowcharts visualizing decision logic, loops, and termination paths.
Big-O Complexity Evaluation: Estimates Time Complexity (
O
(
1
)
, 
O
(
log
⁡
n
)
, 
O
(
n
)
, 
O
(
n
log
⁡
n
)
, 
O
(
n
2
)
, $O(2^n)$) and Space Complexity with mathematical rationales.
Code Construct & Pattern Detection: Identifies functions, variables, loop nesting depth, recursion, branching logic, arrays, hash maps, and sorting/searching routines.
Hybrid Dual-Engine Architecture:
Built-in Rule-Based Engine: 100% offline static AST/regex analyzer and algorithm synthesizer.
Optional LLM AI Engine: Seamless integration with Google Gemini API / OpenAI API via .env.
Export & Report Utilities: Copy full reports or individual cards, download formatted .txt files, or generate printable reports via @media print.
📐 Algorithm Detail Levels
Mode	Target Audience	Description
Small	Quick Overview	Concise, high-level summary steps highlighting input, core loop/math, and output.
Medium	Standard Reference	Structured step-by-step breakdown explaining control flow and variable initialization.
Professional	Academic & Portfolio	Comprehensive academic-style breakdown with sub-steps, state allocation, boundary checks, pseudocode, and Big-O rationales.
🛠️ Technology Stack
Frontend: HTML5, Vanilla CSS3 (Glassmorphism Dark Theme, Modern Variables, @media print), JavaScript (ES6 Async/Fetch, Clipboard API, Dynamic Line Counter).
Backend: Python 3, Flask, Flask-CORS, python-dotenv, AST parser, Regex heuristic analyzers.
Testing & Verification: Pytest suite for unit and API integration testing.
📁 Project Architecture
Code2Algo/
│
├── app.py                      # Flask REST API server and static web host
├── requirements.txt            # Python package dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Git exclusions for Python & virtual environments
├── README.md                   # Comprehensive GitHub documentation
│
├── backend/
│   ├── __init__.py
│   ├── analyzer.py             # Multi-language static code construct detector
│   ├── algorithm_generator.py  # Dynamic algorithm step & pseudocode synthesizer
│   ├── complexity_analyzer.py  # Big-O time and space complexity evaluator
│   └── ai_service.py           # LLM adapter with offline engine fallback
│
├── frontend/
│   ├── index.html              # Developer dashboard UI
│   ├── css/
│   │   └── style.css           # Glassmorphism dark theme & responsive layout
│   └── js/
│       └── script.js           # Interactive UI logic, API connector, copy/download/print handlers
│
├── tests/
│   ├── test_analyzer.py        # Unit tests for code parsing & Big-O evaluation
│   └── test_api.py             # Integration tests for REST endpoints
│
└── examples/                   # Standalone code examples across 7 languages
    ├── python_factorial.py
    ├── python_prime.py
    ├── java_bubblesort.java
    ├── cpp_binarysearch.cpp
    ├── javascript_fibonacci.js
    ├── csharp_grades.cs
    └── php_calculator.php
🚀 Quick Start & Installation
Prerequisites
Python 3.9 or higher
Git
Step-by-Step Setup
Clone the Repository

git clone https://github.com/your-username/Code2Algo.git
cd Code2Algo
Create and Activate Virtual Environment

Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
Linux / macOS:
python3 -m venv venv
source venv/bin/activate
Install Dependencies

pip install -r requirements.txt
Configure Environment Variables (Optional) Copy .env.example to .env:

cp .env.example .env
To enable LLM support, set your Gemini or OpenAI API key in .env. If left empty, Code2Algo runs using its built-in offline engine.

Run the Application

python app.py
Open your browser and navigate to http://localhost:5000.

🧪 Running Automated Tests
Run the full pytest suite to verify code analysis and API endpoints:

python -m pytest
📡 API Documentation
1. POST /api/generate
Analyzes source code and produces an algorithm report.

Request Payload:

{
  "language": "python",
  "code": "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)",
  "detail_level": "professional"
}
Response Payload (200 OK):

{
  "success": true,
  "title": "Factorial Computation Algorithm",
  "detail_level": "professional",
  "algorithm": [
    "1. Start Program",
    "2. Read & Validate Input Parameters...",
    "3. State Variable Allocation...",
    "4. Recursive Execution Strategy...",
    "5. Conditional Decision Evaluation...",
    "6. Result Return...",
    "7. Stop Program Execution"
  ],
  "pseudocode": "START\n  FUNCTION FACTORIAL()\n  ...\nSTOP",
  "explanation": "This program is written in Python. It defines 1 function(s): factorial...",
  "input": "Non-negative integer n.",
  "output": "Factorial value n! computed as n × (n-1) × ... × 1.",
  "time_complexity": "O(n)",
  "time_explanation": "The single linear recursion reduces the input parameter by a constant amount each step...",
  "space_complexity": "O(n)",
  "space_explanation": "Each recursive invocation pushes a call frame onto the call stack...",
  "concepts": ["Iterative Control Flow", "Mathematical Computation", "Recursion"],
  "engine": "Rule-Based Analyzer Engine (Offline)"
}
2. GET /api/examples
Returns pre-populated code examples across all supported languages.

3. GET /api/health
Health check endpoint returning server status and active engine type.

📸 Screenshots
(Place screenshot images here: docs/screenshots/dashboard.png and docs/screenshots/report.png)

🔮 Future Enhancements
 Image / OCR Code Input: Upload code screenshots for automatic OCR code extraction.
 Interactive Flowchart Generator: Render visual SVG flowcharts representing control flow.
 PDF Report Export: Export styled PDF documents with embedded vector diagrams.
 More Languages: Support for Rust, Go, Swift, Kotlin, and TypeScript.
 Algorithm Execution Visualization: Step-by-step debugger playback.
📄 License
Distributed under the MIT License. See LICENSE for more information.
