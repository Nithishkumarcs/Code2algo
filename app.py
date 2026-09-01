"""
Code2Algo — Intelligent Code-to-Algorithm Generator
Flask REST API and Web Application Server
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from backend.ai_service import AIService

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Limit max request body size to 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

ai_service = AIService()

# Built-in code examples for the UI loader
CODE_EXAMPLES = {
    "python_factorial": {
        "title": "Factorial (Python)",
        "language": "python",
        "code": """def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nnum = 5\nresult = factorial(num)\nprint(f"Factorial of {num} is {result}")"""
    },
    "python_prime": {
        "title": "Prime Number Checker (Python)",
        "language": "python",
        "code": """def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nnumber = 29\nif is_prime(number):\n    print(f"{number} is a prime number")\nelse:\n    print(f"{number} is not a prime number")"""
    },
    "java_bubblesort": {
        "title": "Bubble Sort (Java)",
        "language": "java",
        "code": """public class BubbleSort {\n    public static void sort(int[] arr) {\n        int n = arr.length;\n        for (int i = 0; i < n - 1; i++) {\n            for (int j = 0; j < n - i - 1; j++) {\n                if (arr[j] > arr[j + 1]) {\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                }\n            }\n        }\n    }\n}"""
    },
    "cpp_binarysearch": {
        "title": "Binary Search (C++)",
        "language": "cpp",
        "code": """#include <iostream>\nusing namespace std;\n\nint binarySearch(int arr[], int size, int target) {\n    int left = 0, right = size - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target)\n            return mid;\n        if (arr[mid] < target)\n            left = mid + 1;\n        else\n            right = mid - 1;\n    }\n    return -1;\n}"""
    },
    "javascript_fibonacci": {
        "title": "Fibonacci Sequence (JavaScript)",
        "language": "javascript",
        "code": """function generateFibonacci(n) {\n    const fib = [0, 1];\n    for (let i = 2; i < n; i++) {\n        fib[i] = fib[i - 1] + fib[i - 2];\n    }\n    return fib;\n}\n\nconst terms = 10;\nconsole.log(generateFibonacci(terms));"""
    },
    "csharp_grades": {
        "title": "Student Grade Evaluator (C#)",
        "language": "csharp",
        "code": """using System;\n\nclass Program {\n    static void Main() {\n        int score = 85;\n        char grade;\n        if (score >= 90) grade = 'A';\n        else if (score >= 80) grade = 'B';\n        else if (score >= 70) grade = 'C';\n        else if (score >= 60) grade = 'D';\n        else grade = 'F';\n        Console.WriteLine("Grade: " + grade);\n    }\n}"""
    },
    "php_calculator": {
        "title": "Simple Calculator (PHP)",
        "language": "php",
        "code": """<?php\nfunction calculate($num1, $num2, $operator) {\n    switch ($operator) {\n        case '+': return $num1 + $num2;\n        case '-': return $num1 - $num2;\n        case '*': return $num1 * $num2;\n        case '/': return $num2 != 0 ? $num1 / $num2 : "Cannot divide by zero";\n        default: return "Invalid operator";\n    }\n}\necho calculate(10, 5, '+');\n?>"""
    },
    "typescript_search": {
        "title": "Linear Search (TypeScript)",
        "language": "typescript",
        "code": """function findElement<T>(arr: T[], target: T): number {\n    for (let i: number = 0; i < arr.length; i++) {\n        if (arr[i] === target) {\n            return i;\n        }\n    }\n    return -1;\n}\n\nconst numbers: number[] = [10, 20, 30, 40, 50];\nconsole.log(findElement(numbers, 30));"""
    },
    "go_quicksort": {
        "title": "Bubble Sort (Go / Golang)",
        "language": "go",
        "code": """package main\nimport "fmt"\n\nfunc bubbleSort(arr []int) []int {\n    n := len(arr)\n    for i := 0; i < n-1; i++ {\n        for j := 0; j < n-i-1; j++ {\n            if arr[j] > arr[j+1] {\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n            }\n        }\n    }\n    return arr\n}\n\nfunc main() {\n    nums := []int{64, 34, 25, 12, 22}\n    fmt.Println(bubbleSort(nums))\n}"""
    },
    "rust_factorial": {
        "title": "Recursive Factorial (Rust)",
        "language": "rust",
        "code": """fn factorial(n: u64) -> u64 {\n    if n <= 1 {\n        1\n    } else {\n        n * factorial(n - 1)\n    }\n}\n\nfn main() {\n    let result = factorial(5);\n    println!("Factorial: {}", result);\n}"""
    },
    "kotlin_prime": {
        "title": "Prime Checker (Kotlin)",
        "language": "kotlin",
        "code": """fun isPrime(n: Int): Boolean {\n    if (n <= 1) return false\n    for (i in 2..Math.sqrt(n.toDouble()).toInt()) {\n        if (n % i == 0) return false\n    }\n    return true\n}\n\nfun main() {\n    println(isPrime(29))\n}"""
    },
    "swift_fibonacci": {
        "title": "Fibonacci Generator (Swift)",
        "language": "swift",
        "code": """func generateFibonacci(_ n: Int) -> [Int] {\n    var fib = [0, 1]\n    for i in 2..<n {\n        fib.append(fib[i-1] + fib[i-2])\n    }\n    return fib\n}\n\nprint(generateFibonacci(10))"""
    },
    "ruby_calculator": {
        "title": "Calculator (Ruby)",
        "language": "ruby",
        "code": """def calculate(a, b, op)\n  case op\n  when '+' then a + b\n  when '-' then a - b\n  when '*' then a * b\n  when '/' then b != 0 ? a / b : "Error"\n  else "Invalid"\n  end\nend\n\nputs calculate(10, 5, '+')"""
    },
    "dart_grade": {
        "title": "Student Grade (Dart)",
        "language": "dart",
        "code": r"""String getGrade(int score) {\n  if (score >= 90) return 'A';\n  if (score >= 80) return 'B';\n  if (score >= 70) return 'C';\n  if (score >= 60) return 'D';\n  return 'F';\n}\n\nvoid main() {\n  print('Grade: ${getGrade(85)}');\n}"""
    },
    "sql_query": {
        "title": "Aggregation & Filter (SQL)",
        "language": "sql",
        "code": """SELECT department_id, COUNT(employee_id) AS total_employees, AVG(salary) AS avg_salary\nFROM employees\nWHERE status = 'Active'\nGROUP BY department_id\nHAVING COUNT(employee_id) > 5\nORDER BY avg_salary DESC;"""
    }
}


@app.route('/')
def serve_index():
    """Serve main frontend SPA."""
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static frontend assets (css, js, images)."""
    return send_from_directory('frontend', path)


@app.route('/api/generate', methods=['POST'])
def generate_algorithm():
    """
    POST /api/generate
    Receives JSON: { "language": "python", "code": "...", "detail_level": "professional" }
    Returns structured analysis, algorithm steps, pseudocode, and complexities.
    """
    try:
        data = request.get_json(force=True, silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({
                "success": False,
                "error": "Invalid request payload. Please provide a valid JSON body."
            }), 400

        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower().strip()
        detail_level = data.get('detail_level', 'professional').lower().strip()

        # Input validations
        if not code:
            return jsonify({
                "success": False,
                "error": "Code input is empty. Please enter or paste source code."
            }), 400

        if len(code) > 50000:
            return jsonify({
                "success": False,
                "error": "Submitted code exceeds maximum limit of 50,000 characters."
            }), 400

        # Execute generation pipeline via AI service or rule-based fallback
        result = ai_service.generate_algorithm(language, code, detail_level)

        return jsonify({
            "success": True,
            **result
        }), 200

    except Exception as err:
        # Secure error response without stack traces
        return jsonify({
            "success": False,
            "error": "An internal server error occurred while analyzing code.",
            "details": str(err)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return pre-populated code examples for testing."""
    return jsonify({
        "success": True,
        "examples": CODE_EXAMPLES
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "app": "Code2Algo",
        "ai_provider": ai_service.provider
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
