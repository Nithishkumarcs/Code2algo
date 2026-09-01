"""
Complexity Analyzer Module for Code2Algo

Estimates time and space complexity based on program structure, loop nesting,
divide-and-conquer recursion patterns, memory allocations, and data structures.
"""

import re

class ComplexityAnalyzer:
    """Computes time and space complexity estimations and explanations."""

    def __init__(self, analysis: dict, code: str):
        self.analysis = analysis
        self.code = code
        self.code_lower = code.lower()

    def evaluate(self) -> dict:
        """Determines time and space complexity details."""
        nested_depth = self.analysis.get('nested_loop_max', 0)
        has_recursion = self.analysis.get('has_recursion', False)
        loop_count = self.analysis.get('loop_count', 0)
        data_structures = self.analysis.get('data_structures', [])

        # Time Complexity evaluation
        time_comp, time_expl = self._estimate_time_complexity(nested_depth, has_recursion, loop_count)

        # Space Complexity evaluation
        space_comp, space_expl = self._estimate_space_complexity(has_recursion, data_structures)

        return {
            "time_complexity": time_comp,
            "time_explanation": time_expl,
            "space_complexity": space_comp,
            "space_explanation": space_expl
        }

    def _estimate_time_complexity(self, nested_depth: int, has_recursion: bool, loop_count: int) -> tuple:
        """Derive Big-O Time Complexity."""

        # Binary search / Divide & conquer heuristics
        if ('mid' in self.code_lower or 'middle' in self.code_lower or 'pivot' in self.code_lower) and \
           ('/ 2' in self.code_lower or '// 2' in self.code_lower or '>> 1' in self.code_lower):
            if nested_depth <= 1 and not ('for' in self.code_lower and nested_depth == 2):
                if loop_count > 0 or has_recursion:
                    return (
                        "O(log n)",
                        "The program repeatedly halves the problem size (divide-and-conquer strategy or binary reduction), yielding logarithmic time complexity O(log n)."
                    )
            elif nested_depth >= 2 or (loop_count >= 2 and 'sort' in self.code_lower):
                return (
                    "O(n log n)",
                    "The algorithm combines linear iterations with logarithmic partitioning (typical of efficient comparison sorts like Merge Sort or Quick Sort), resulting in O(n log n) time complexity."
                )

        # Exponential recursion (e.g., naive fibonacci f(n-1) + f(n-2))
        if has_recursion:
            func_calls_in_body = len(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*[-+]', self.code))
            if func_calls_in_body >= 2 or ('- 1' in self.code and '- 2' in self.code):
                return (
                    "O(2ⁿ)",
                    "The function invokes multiple recursive calls for each step without memoization, generating a binary decision tree of operations and O(2ⁿ) exponential time complexity."
                )
            elif nested_depth == 0:
                return (
                    "O(n)",
                    "The single linear recursion reduces the input parameter by a constant amount each step, making T(n) = T(n-1) + O(1), which evaluates to O(n) linear time complexity."
                )

        # Nested loops evaluation
        if nested_depth >= 3:
            return (
                f"O(n^{nested_depth})",
                f"The code contains {nested_depth} nested loops iterating over n elements, producing O(n^{nested_depth}) polynomial time complexity."
            )
        elif nested_depth == 2:
            return (
                "O(n²)",
                "Two nested loops iterate through the input dataset, causing the inner operations to execute n × n times, resulting in O(n²) quadratic time complexity."
            )
        elif nested_depth == 1:
            return (
                "O(n)",
                "The program features a single loop that traverses the input elements once, executing in linear O(n) time complexity."
            )

        # Sequential loops without nesting
        if loop_count > 0 and nested_depth <= 1:
            return (
                "O(n)",
                "The program executes sequential loops over n items, keeping overall time complexity linear at O(n)."
            )

        # Constant time fallback
        return (
            "O(1)",
            "The program executes a fixed sequence of statements, conditional branches, or basic operations without dynamic looping over input sizes, operating in O(1) constant time complexity."
        )

    def _estimate_space_complexity(self, has_recursion: bool, data_structures: list) -> tuple:
        """Derive Big-O Auxiliary Space Complexity."""
        code_lower = self.code_lower

        # Dynamic memory / multi-dimensional arrays / matrix
        if 'grid' in code_lower or 'matrix' in code_lower or ('[[' in self.code and ']]' in self.code):
            return (
                "O(n²)",
                "The algorithm instantiates a two-dimensional grid or matrix buffer storing n × n elements, requiring quadratic O(n²) auxiliary space."
            )

        # Recursion stack space
        if has_recursion:
            return (
                "O(n)",
                "Each recursive invocation pushes a call frame onto the call stack, utilizing O(n) space proportional to the maximum call stack depth."
            )

        # Linear auxiliary data structures (Arrays, Maps, Vectors, Sets)
        if any(ds in ['Arrays / Lists', 'Maps / Dictionaries', 'Sets', 'Stacks / Queues'] for ds in data_structures) or \
           re.search(r'\b(new|append|push|vector|ArrayList|malloc)\b', self.code):
            return (
                "O(n)",
                "The program creates additional dynamic data structures (lists, arrays, or maps) scaling linearly with input size n, leading to O(n) auxiliary space complexity."
            )

        # Constant space fallback
        return (
            "O(1)",
            "The algorithm uses only a small, fixed number of primitive variables and control flags. Auxiliary memory usage remains constant O(1) regardless of input size."
        )
