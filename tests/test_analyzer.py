"""
Unit tests for Code2Algo Code Analyzer & Complexity Evaluator
"""

import pytest
from backend.analyzer import CodeAnalyzer
from backend.complexity_analyzer import ComplexityAnalyzer
from backend.algorithm_generator import AlgorithmGenerator

def test_python_ast_analysis():
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
    analyzer = CodeAnalyzer('python', code)
    res = analyzer.analyze()
    assert res['parsed_ast_successfully'] is True
    assert 'factorial' in res['functions']
    assert res['has_recursion'] is True
    assert res['has_if'] is True

def test_java_regex_analysis():
    code = """
public class BubbleSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
"""
    analyzer = CodeAnalyzer('java', code)
    res = analyzer.analyze()
    assert res['language'] == 'java'
    assert res['nested_loop_max'] >= 2
    assert res['loop_count'] >= 2

def test_complexity_estimation_quadratic():
    analysis = {
        'nested_loop_max': 2,
        'has_recursion': False,
        'loop_count': 2,
        'data_structures': ['Arrays / Lists']
    }
    code = "for (int i=0; i<n; i++) { for (int j=0; j<n; j++) { swap(); } }"
    evaluator = ComplexityAnalyzer(analysis, code)
    res = evaluator.evaluate()
    assert res['time_complexity'] == 'O(n²)'
    assert res['space_complexity'] in ['O(1)', 'O(n)']

def test_complexity_estimation_linear():
    analysis = {
        'nested_loop_max': 1,
        'has_recursion': False,
        'loop_count': 1,
        'data_structures': []
    }
    code = "for (let i = 0; i < arr.length; i++) { console.log(arr[i]); }"
    evaluator = ComplexityAnalyzer(analysis, code)
    res = evaluator.evaluate()
    assert res['time_complexity'] == 'O(n)'
    assert res['space_complexity'] == 'O(1)'

def test_detail_modes_generation():
    analysis = {'language': 'python', 'functions': ['compute'], 'variables': ['x'], 'loop_count': 1}
    complexity = {'time_complexity': 'O(n)', 'time_explanation': 'Linear iteration', 'space_complexity': 'O(1)', 'space_explanation': 'Constant space'}
    code = "def compute(x):\n    for i in range(x):\n        print(i)"

    gen_small = AlgorithmGenerator(analysis, complexity, code, 'small').generate()
    gen_medium = AlgorithmGenerator(analysis, complexity, code, 'medium').generate()
    gen_prof = AlgorithmGenerator(analysis, complexity, code, 'professional').generate()

    assert len(gen_small['algorithm']) < len(gen_prof['algorithm'])
    assert '1. Start Program' in gen_prof['algorithm'][0]

def test_flowchart_generation():
    analysis = {'language': 'python', 'functions': ['factorial'], 'variables': ['n'], 'has_recursion': True, 'loop_count': 0}
    complexity = {'time_complexity': 'O(n)', 'time_explanation': 'Linear recursion', 'space_complexity': 'O(n)', 'space_explanation': 'Stack frame'}
    code = "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)"

    res = AlgorithmGenerator(analysis, complexity, code, 'professional').generate()
    assert 'flowchart' in res
    assert 'flowchart TD' in res['flowchart']
    assert 'Start' in res['flowchart']

def test_sample_output_generation():
    analysis = {'language': 'python', 'functions': ['factorial'], 'variables': ['n'], 'has_recursion': True, 'loop_count': 0}
    complexity = {'time_complexity': 'O(n)', 'time_explanation': 'Linear recursion', 'space_complexity': 'O(n)', 'space_explanation': 'Stack frame'}
    code = "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)\nprint(factorial(5))"

    res = AlgorithmGenerator(analysis, complexity, code, 'professional').generate()
    assert 'sample_output' in res
    assert len(res['sample_output']) > 0
    assert '120' in res['sample_output']

def test_go_rust_kotlin_analysis():
    go_code = """package main\nimport "fmt"\nfunc bubbleSort(arr []int) []int {\n    for i := 0; i < len(arr); i++ {\n        for j := 0; j < len(arr)-1; j++ {\n            if arr[j] > arr[j+1] { fmt.Println("swap") }\n        }\n    }\n    return arr\n}"""
    go_res = CodeAnalyzer('go', go_code).analyze()
    assert 'bubbleSort' in go_res['functions']
    assert go_res['nested_loop_max'] >= 2

    rust_code = """fn factorial(n: u64) -> u64 {\n    if n <= 1 { 1 } else { n * factorial(n - 1) }\n}"""
    rust_res = CodeAnalyzer('rust', rust_code).analyze()
    assert 'factorial' in rust_res['functions']
    assert rust_res['has_recursion'] is True

    kotlin_code = """fun isPrime(n: Int): Boolean {\n    if (n <= 1) return false\n    for (i in 2..n) { if (n % i == 0) return false }\n    return true\n}"""
    kt_res = CodeAnalyzer('kotlin', kotlin_code).analyze()
    assert 'isPrime' in kt_res['functions']
    assert kt_res['loop_count'] >= 1

def test_language_auto_detection():
    # Test C program (such as the user's bitwise swap code)
    c_code = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

uint16_t swap_uint16(uint16_t val) {
    return (val << 8) | (val >> 8);
}
"""
    assert CodeAnalyzer.detect_language(c_code) == 'c'

    # Auto analyzer initialization with 'auto'
    analyzer_auto = CodeAnalyzer('auto', c_code)
    assert analyzer_auto.language == 'c'
    res = analyzer_auto.analyze()
    assert 'swap_uint16' in res['functions']

    # Test C++
    cpp_code = "#include <iostream>\nusing namespace std;\nint main() { cout << 42 << endl; return 0; }"
    assert CodeAnalyzer.detect_language(cpp_code) == 'cpp'

    # Test Python
    py_code = "def is_prime(n):\n    if n <= 1:\n        return False\n    return True"
    assert CodeAnalyzer.detect_language(py_code) == 'python'

    # Test TypeScript
    ts_code = "interface User {\n    id: number;\n    name: string;\n}\nconst u: User = { id: 1, name: 'Alice' };"
    assert CodeAnalyzer.detect_language(ts_code) == 'typescript'

    # Test JavaScript
    js_code = "function calculateSum(arr) {\n    return arr.reduce((acc, curr) => acc + curr, 0);\n}\nconsole.log(calculateSum([1, 2, 3]));"
    assert CodeAnalyzer.detect_language(js_code) == 'javascript'

def test_java_serialization_simulation():
    java_code = """
public class SerializationEngine {
    public static void main(String[] args) {
        System.out.println("[KERNEL] Detecting host native architecture...");
        System.out.println("[KERNEL] Native OS Order is: **LITTLE_ENDIAN**");
        System.out.println("==================================================");
        System.out.println("  WIRE STREAM PREVIEW (Enforced Network Big-Endian)");
        System.out.println("==================================================");
        for (int i = 0; i < rawBytes.length; i++) {
            System.out.printf("0x%02X ", rawBytes[i]);
            if ((i + 1) % 4 == 0) System.out.println();
        }
        System.out.println("==================================================");
        System.out.println("  RECONSTRUCTED DESERIALIZED PACKET VALUES");
        System.out.println("==================================================");
        NetworkPacket inboundNode = new NetworkPacket(rxId, rxUser, rxBalance, rxLat);
        System.out.println(inboundNode);
    }
}
"""
    analyzer = CodeAnalyzer('java', java_code)
    analysis = analyzer.analyze()
    assert analysis['has_recursion'] is False
    complexity = ComplexityAnalyzer(analysis, java_code).evaluate()
    assert complexity['time_complexity'] in ['O(n)', 'O(1)']
    
    gen = AlgorithmGenerator(analysis, complexity, java_code, 'professional').generate()
    assert "WIRE STREAM PREVIEW" in gen['sample_output']
    assert "RECONSTRUCTED DESERIALIZED PACKET VALUES" in gen['sample_output']
    assert "0xAF 0xFD 0xAA 0xBB" in gen['sample_output']
    assert "Serialization Engine" in gen['title']





