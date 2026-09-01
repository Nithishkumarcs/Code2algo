"""
Code Analysis Module for Code2Algo

Performs multi-language static code analysis to detect program constructs,
execution flow, control structures, data structures, and algorithmic patterns.
"""

import re
import ast

class CodeAnalyzer:
    """Analyzes source code written in Python, Java, C, C++, JavaScript, C#, or PHP."""

    SUPPORTED_LANGUAGES = [
        'python', 'java', 'c', 'cpp', 'javascript', 'typescript',
        'csharp', 'php', 'go', 'rust', 'kotlin', 'swift',
        'ruby', 'dart', 'scala', 'r', 'sql'
    ]

    def __init__(self, language: str, code: str):
        self.language = language.lower().strip() if language else 'auto'
        if self.language == 'auto' or self.language not in self.SUPPORTED_LANGUAGES:
            self.language = self.detect_language(code)
        self.code = code
        self.lines = [line.strip() for line in code.splitlines() if line.strip()]

    @classmethod
    def detect_language(cls, code: str) -> str:
        """Heuristically detects the programming language of a code snippet."""
        if not code or not code.strip():
            return 'python'

        text = code.strip()
        scores = {lang: 0 for lang in cls.SUPPORTED_LANGUAGES}

        # 1. C & C++
        if re.search(r'#include\s*<(?:stdio|stdlib|string|stdint|stdbool|math|unistd|fcntl|sys/|errno|ctype|time|assert)\.h>', text, re.IGNORECASE):
            scores['c'] += 25
        if re.search(r'#include\s*<(?:iostream|vector|string|algorithm|map|set|queue|stack|deque|memory|cmath|cstdio|cstdlib|bits/stdc\+\+\.h)>', text, re.IGNORECASE):
            scores['cpp'] += 30
        if re.search(r'#include\s*[<"][a-zA-Z0-9_./\\]+[>"]', text):
            scores['c'] += 8
            scores['cpp'] += 8
        if re.search(r'\b(?:std::|cout\s*<<|cin\s*>>|endl\b|nullptr\b|template\s*<|constexpr\b|class\s+\w+\s*:\s*(?:public|private|protected))', text):
            scores['cpp'] += 20
        if re.search(r'\b(?:printf|scanf|fprintf|sprintf|snprintf|malloc|calloc|realloc|free|memcpy|memset)\s*\(', text):
            scores['c'] += 15
            scores['cpp'] += 6
        if re.search(r'\b(?:uint8_t|uint16_t|uint32_t|uint64_t|int8_t|int16_t|int32_t|int64_t|size_t|ssize_t|intptr_t|uintptr_t)\b', text):
            scores['c'] += 15
            scores['cpp'] += 10
        if re.search(r'\btypedef\s+struct\b|\bstruct\s+\w+\s*\{', text):
            scores['c'] += 10
            scores['cpp'] += 8

        # 2. Python
        if re.search(r'\bdef\s+[a-zA-Z_]\w*\s*\([^)]*\)\s*:', text):
            scores['python'] += 20
        if re.search(r'\b(?:elif|pass|None|True|False|self\.)\b', text):
            scores['python'] += 12
        if re.search(r'^\s*(?:import\s+[a-zA-Z_]\w*|from\s+[a-zA-Z_]\w*\s+import)', text, re.MULTILINE):
            scores['python'] += 15
        if re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', text):
            scores['python'] += 25
        if re.search(r'\bprint\s*\([^)]*\)', text) and not re.search(r'[;{}]', text):
            scores['python'] += 10
        if re.search(r'\bin\s+range\s*\(', text):
            scores['python'] += 15

        # 3. PHP
        if re.search(r'<\?php|<\?=', text, re.IGNORECASE):
            scores['php'] += 35
        if re.search(r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', text):
            scores['php'] += 10
        if re.search(r'\b(?:echo\s+[^;]+;|var_dump\s*\(|print_r\s*\()', text):
            scores['php'] += 15

        # 4. Java
        if re.search(r'public\s+class\s+\w+|public\s+static\s+void\s+main\s*\(\s*String\s*(?:\[\s*\]\s*\w+|\w+\s*\[\s*\])\s*\)', text):
            scores['java'] += 30
        if re.search(r'System\.(?:out|err)\.(?:println|print|printf)\s*\(', text):
            scores['java'] += 25
        if re.search(r'import\s+java\.[a-zA-Z0-9_.*]+;', text):
            scores['java'] += 25
        if re.search(r'@Override\b', text):
            scores['java'] += 15

        # 5. C#
        if re.search(r'using\s+System(?:\.[a-zA-Z0-9_]+)*\s*;', text):
            scores['csharp'] += 25
        if re.search(r'Console\.(?:WriteLine|Write|ReadLine)\s*\(', text):
            scores['csharp'] += 25
        if re.search(r'namespace\s+[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*\s*\{', text):
            scores['csharp'] += 15

        # 6. TypeScript vs JavaScript
        if re.search(r':\s*(?:string|number|boolean|any|void|never|unknown|object|symbol|bigint)\b|interface\s+[A-Z]\w*\s*\{|type\s+[A-Z]\w*\s*=\s*|as\s+const\b|<[A-Z]\w*>\s*\(|:\s*[A-Z]\w*(?:\[\])?\s*(?:=|;|,|\))', text):
            scores['typescript'] += 20
        if re.search(r'\b(?:const|let|var)\s+[a-zA-Z_$]\w*\s*=', text):
            scores['javascript'] += 8
            scores['typescript'] += 8
        if re.search(r'console\.(?:log|warn|error|info|debug)\s*\(', text):
            scores['javascript'] += 10
            scores['typescript'] += 10
        if re.search(r'function\s+[a-zA-Z_$]\w*\s*\([^)]*\)\s*\{', text):
            scores['javascript'] += 8
            scores['typescript'] += 8
        if re.search(r'=>\s*\{|document\.getElementById|window\.addEventListener|export\s+default\b', text):
            scores['javascript'] += 8
            scores['typescript'] += 8

        # 7. Go
        if re.search(r'package\s+main\b', text):
            scores['go'] += 25
        if re.search(r'import\s*\(\s*["\']fmt["\']|import\s+["\']fmt["\']', text):
            scores['go'] += 20
        if re.search(r'func\s+(?:main|\([a-zA-Z0-9_* ]+\)\s*\w+|\w+)\s*\([^)]*\)', text):
            scores['go'] += 15
        if re.search(r'fmt\.(?:Println|Printf|Sprintf|Print)\s*\(', text):
            scores['go'] += 20
        if ':=' in text:
            scores['go'] += 10

        # 8. Rust
        if re.search(r'fn\s+(?:main|[a-zA-Z_]\w*)\s*\([^)]*\)\s*(?:->\s*[^{]+)?\s*\{', text):
            scores['rust'] += 18
        if re.search(r'(?:println!|eprintln!|format!)\s*\(', text):
            scores['rust'] += 25
        if re.search(r'\b(?:let\s+mut\b|pub\s+fn\b|impl\b|match\s+\w+\s*\{)', text):
            scores['rust'] += 15

        # 9. Kotlin
        if re.search(r'fun\s+(?:main|[a-zA-Z_]\w*)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{', text):
            scores['kotlin'] += 20

        # 10. Swift
        if re.search(r'import\s+(?:UIKit|Foundation|SwiftUI)', text):
            scores['swift'] += 30
        if re.search(r'guard\s+let\b|if\s+let\b', text):
            scores['swift'] += 15

        # 11. Ruby
        if re.search(r'\bputs\s+[^;]+|\bdef\s+[a-zA-Z_]\w*\s*(?:\([^)]*\))?\s*[\r\n]+[\s\S]*?\bend\b', text) and not re.search(r'[;{}]', text):
            scores['ruby'] += 15

        # 12. SQL
        if re.search(r'^\s*(?:SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE)\b', text, re.MULTILINE | re.IGNORECASE):
            scores['sql'] += 30

        # 13. Dart
        if re.search(r'void\s+main\s*\(\s*\)\s*\{|import\s+[\'"]package:flutter', text):
            scores['dart'] += 25

        # 14. R
        if re.search(r'<-|library\s*\([a-zA-Z_]\w*\)|ggplot\s*\(', text):
            scores['r'] += 20

        # 15. Scala
        if re.search(r'object\s+[A-Z]\w*(?:\s+extends\s+App)?\s*\{|def\s+main\s*\(', text):
            scores['scala'] += 25

        best_lang = max(scores, key=scores.get)
        if scores[best_lang] > 0:
            return best_lang

        return 'python'

    def analyze(self) -> dict:
        """Main analysis entrypoint. Returns structured breakdown of the program."""
        if not self.code.strip():
            return {
                "error": "Empty code provided",
                "valid": False
            }

        # Specialized analysis for Python if valid AST, otherwise regex/heuristics for all languages
        if self.language == 'python':
            ast_res = self._analyze_python_ast()
            if ast_res.get('parsed_ast_successfully'):
                return ast_res

        return self._analyze_generic_regex()

    def _analyze_python_ast(self) -> dict:
        """Use Python's built-in AST module for precise Python analysis."""
        try:
            tree = ast.parse(self.code)
        except Exception:
            # Fall back to regex parsing if AST fails due to syntax error or snippet fragment
            return {'parsed_ast_successfully': False}

        functions = []
        variables = set()
        loop_count = 0
        nested_loop_max = 0
        has_if = False
        has_recursion = False
        has_input = False
        has_output = False
        data_structures = set()
        concepts = set()

        class ASTVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_func = None
                self.current_loop_depth = 0
                self.max_loop_depth = 0
                self.func_names = set()

            def visit_FunctionDef(self, node):
                self.func_names.add(node.name)
                functions.append(node.name)
                prev_func = self.current_func
                self.current_func = node.name
                self.generic_visit(node)
                self.current_func = prev_func

            def visit_AsyncFunctionDef(self, node):
                self.visit_FunctionDef(node)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    variables.add(node.id)
                self.generic_visit(node)

            def visit_For(self, node):
                nonlocal loop_count
                loop_count += 1
                self.current_loop_depth += 1
                if self.current_loop_depth > self.max_loop_depth:
                    self.max_loop_depth = self.current_loop_depth
                self.generic_visit(node)
                self.current_loop_depth -= 1

            def visit_While(self, node):
                nonlocal loop_count
                loop_count += 1
                self.current_loop_depth += 1
                if self.current_loop_depth > self.max_loop_depth:
                    self.max_loop_depth = self.current_loop_depth
                self.generic_visit(node)
                self.current_loop_depth -= 1

            def visit_If(self, node):
                nonlocal has_if
                has_if = True
                self.generic_visit(node)

            def visit_Call(self, node):
                nonlocal has_input, has_output, has_recursion
                # Detect function call
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name == self.current_func and self.current_func is not None:
                        has_recursion = True
                    if func_name in ('input', 'read', 'sys.stdin.read'):
                        has_input = True
                    if func_name in ('print', 'display'):
                        has_output = True
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in ('append', 'extend', 'insert', 'pop'):
                        data_structures.add('List / Array')
                    elif node.func.attr in ('keys', 'values', 'items', 'get'):
                        data_structures.add('Dictionary / Hash Map')
                    elif node.func.attr in ('add', 'remove', 'union', 'intersection'):
                        data_structures.add('Set')

                self.generic_visit(node)

            def visit_List(self, node):
                data_structures.add('List / Array')
                self.generic_visit(node)

            def visit_Dict(self, node):
                data_structures.add('Dictionary / Hash Map')
                self.generic_visit(node)

            def visit_Set(self, node):
                data_structures.add('Set')
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                data_structures.add('Classes / OOP Objects')
                concepts.add('Object-Oriented Programming')
                self.generic_visit(node)

        visitor = ASTVisitor()
        visitor.visit(tree)

        nested_loop_max = visitor.max_loop_depth

        # Infer algorithmic patterns
        code_str = self.code.lower()
        if 'sort' in code_str or ('swap' in code_str and nested_loop_max >= 2):
            concepts.add('Sorting Algorithm')
        if ('mid' in code_str or 'left' in code_str and 'right' in code_str) and ('// 2' in code_str or '/ 2' in code_str):
            concepts.add('Binary Search / Divide & Conquer')
        if has_recursion:
            concepts.add('Recursion')
        if loop_count > 0:
            concepts.add('Iterative Control Flow')
        if has_if:
            concepts.add('Conditional Logic')

        return {
            'parsed_ast_successfully': True,
            'language': 'python',
            'functions': functions,
            'variables': list(variables),
            'loop_count': loop_count,
            'nested_loop_max': nested_loop_max,
            'has_if': has_if,
            'has_recursion': has_recursion,
            'has_input': has_input,
            'has_output': has_output,
            'data_structures': sorted(list(data_structures)),
            'concepts': sorted(list(concepts)),
            'line_count': len(self.lines)
        }

    def _analyze_generic_regex(self) -> dict:
        """Regex and heuristic analysis for any supported language."""
        code = self.code
        code_lower = code.lower()

        # Detect functions
        functions = []
        if self.language in ['c', 'cpp', 'java', 'csharp', 'dart']:
            func_pattern = r'(?:public|private|protected|static|inline|void|int|float|double|char|bool|boolean|string|long|short|unsigned|signed|auto|var|uint8_t|uint16_t|uint32_t|uint64_t|int8_t|int16_t|int32_t|int64_t|size_t|ssize_t)\s+(?:[*&]\s*)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)'
            for match in re.finditer(func_pattern, code):
                name = match.group(1)
                if name not in ('if', 'while', 'for', 'switch', 'catch', 'main'):
                    functions.append(name)
        elif self.language in ['javascript', 'typescript', 'php']:
            func_pattern = r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            for match in re.finditer(func_pattern, code):
                functions.append(match.group(1))
            # ES6 / TS arrow functions
            arrow_pattern = r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\([^)]*\)\s*=>'
            for match in re.finditer(arrow_pattern, code):
                functions.append(match.group(1))
        elif self.language in ['python', 'ruby']:
            py_func = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            functions = re.findall(py_func, code)
        elif self.language in ['go', 'swift']:
            go_func = r'func\s+(?:\([^)]*\)\s*)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(go_func, code)
        elif self.language == 'rust':
            rust_func = r'fn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(rust_func, code)
        elif self.language == 'kotlin':
            kt_func = r'fun\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(kt_func, code)
        elif self.language == 'scala':
            scala_func = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(scala_func, code)
        elif self.language == 'r':
            r_func = r'([a-zA-Z_][a-zA-Z0-9_\.]*)\s*<-\s*function'
            functions = re.findall(r_func, code)
        elif self.language == 'sql':
            sql_func = r'CREATE\s+(?:PROCEDURE|FUNCTION)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            functions = re.findall(sql_func, code, re.IGNORECASE)

        # Detect recursion (accurate check inside function body, excluding main/entrypoints)
        has_recursion = False
        for fn in functions:
            if fn.lower() in ('main', 'init', 'setup', 'run', 'start', 'tostring', 'equals', 'hashcode'):
                continue
            # Match function signature opening (supports optional return type like -> u64 or : Int)
            fn_match = re.search(r'\b' + re.escape(fn) + r'\s*\([^)]*\)[^{:]*\{', code)
            if fn_match:
                start_idx = fn_match.end() - 1
                brace_depth = 0
                body = ""
                for char in code[start_idx:]:
                    if char == '{':
                        brace_depth += 1
                    elif char == '}':
                        brace_depth -= 1
                        if brace_depth == 0:
                            break
                    body += char
                # Check if function name is invoked recursively inside its own body
                if re.search(r'\b' + re.escape(fn) + r'\s*\(', body[1:]):
                    has_recursion = True
                    break

        # Count loops & compute nesting depth
        loop_tokens = r'\b(for|while|do|loop)\b'
        loop_matches = list(re.finditer(loop_tokens, code_lower))
        loop_count = len(loop_matches)

        nested_loop_max = self._calculate_nesting_depth()

        # Conditional checks
        has_if = bool(re.search(r'\b(if|else if|elif|switch|match|when|unless)\b', code_lower))

        # Input / Output detection
        input_keywords = ['input', 'cin', 'scanner', 'readline', 'fgets', 'scanf', 'prompt', '$_post', '$_get', 'bufio', 'read_line', 'readln', 'gets', 'stdin', 'scan', 'from']
        output_keywords = ['print', 'printf', 'println', 'cout', 'system.out.println', 'console.log', 'console.writeline', 'echo', 'fmt.println', 'fmt.printf', 'println!', 'print!', 'puts', 'cat', 'select']

        has_input = any(kw in code_lower for kw in input_keywords)
        has_output = any(kw in code_lower for kw in output_keywords)

        # Data structures
        data_structures = set()
        if re.search(r'\[.*\]|\bList\b|\bArrayList\b|\bvector\b|\bArray\b', code):
            data_structures.add('Arrays / Lists')
        if re.search(r'\bMap\b|\bHashMap\b|\bDictionary\b|\bstd::map\b|\bdict\b|\{.*:.*\}', code):
            data_structures.add('Maps / Dictionaries')
        if re.search(r'\bSet\b|\bHashSet\b|\bstd::set\b', code):
            data_structures.add('Sets')
        if re.search(r'\bStack\b|\bstd::stack\b|\.push\(|\.pop\(', code):
            data_structures.add('Stacks / Queues')
        if re.search(r'\bclass\b|\bstruct\b|\binterface\b', code):
            data_structures.add('Classes / Objects')

        # Algorithmic Concepts
        concepts = set()
        if loop_count > 0:
            concepts.add('Iterative Control Flow')
        if nested_loop_max >= 2:
            concepts.add('Nested Loop Processing')
        if has_if:
            concepts.add('Branching Logic / Decision Making')
        if has_recursion:
            concepts.add('Recursion')

        if any(term in code_lower for term in ['sort', 'swap', 'temp']) and nested_loop_max >= 1:
            concepts.add('Sorting Mechanism')
        if any(term in code_lower for term in ['binary', 'mid', 'middle', 'pivot']):
            concepts.add('Divide and Conquer / Binary Search')
        if any(term in code_lower for term in ['prime', 'factorial', 'fibonacci', 'gcd', 'lcm', 'pow', 'sqrt', '%']):
            concepts.add('Mathematical Computation')
        if 'class' in code_lower or 'this.' in code_lower or 'self.' in code_lower:
            concepts.add('Object-Oriented Design')

        # Variables extraction (rough heuristic)
        var_pattern = r'\b(?:int|float|double|char|var|let|const|auto)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        vars_found = set(re.findall(var_pattern, code))
        if self.language == 'python':
            vars_found.update(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code))

        return {
            'parsed_ast_successfully': False,
            'language': self.language,
            'functions': list(set(functions)),
            'variables': sorted(list(vars_found))[:10],  # Limit top 10
            'loop_count': loop_count,
            'nested_loop_max': nested_loop_max,
            'has_if': has_if,
            'has_recursion': has_recursion,
            'has_input': has_input,
            'has_output': has_output,
            'data_structures': sorted(list(data_structures)),
            'concepts': sorted(list(concepts)),
            'line_count': len(self.lines)
        }

    def _calculate_nesting_depth(self) -> int:
        """Estimate loop nesting depth based on brace levels and indentation."""
        max_depth = 0
        current_depth = 0

        # Scan line by line for loop keywords and brace tracking
        in_loop_stack = []

        for line in self.lines:
            line_clean = line.split('//')[0].split('#')[0]  # ignore comments
            # Check if line opens a loop
            is_loop = bool(re.search(r'\b(for|while|do)\b', line_clean))

            open_braces = line_clean.count('{')
            close_braces = line_clean.count('}')

            if is_loop:
                current_depth += 1
                in_loop_stack.append(current_depth)
                if current_depth > max_depth:
                    max_depth = current_depth

            if close_braces > 0 and in_loop_stack:
                for _ in range(min(close_braces, len(in_loop_stack))):
                    in_loop_stack.pop()
                    current_depth = max(0, current_depth - 1)

        # Fallback for Python whitespace indentation loop nesting
        if self.language == 'python' and max_depth == 0:
            indent_levels = []
            for line in self.code.splitlines():
                if line.strip() and not line.strip().startswith('#'):
                    indent = len(line) - len(line.lstrip())
                    if re.match(r'^\s*(for|while)\b', line):
                        indent_levels.append(indent)

            # Check distinct strictly increasing indentation levels of loops
            if indent_levels:
                unique_indents = sorted(list(set(indent_levels)))
                max_depth = max(1, len(unique_indents))

        return max_depth
