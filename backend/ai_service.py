"""
AI Service Integration Module for Code2Algo

Provides optional LLM integration (Gemini / OpenAI API compatible) for advanced code understanding.
If AI_API_KEY is not configured or an API call fails, seamlessly falls back to rule-based engine.
"""

import os
import json
import requests
from backend.analyzer import CodeAnalyzer
from backend.complexity_analyzer import ComplexityAnalyzer
from backend.algorithm_generator import AlgorithmGenerator

class AIService:
    """Handles AI-assisted algorithm generation with automatic rule-based fallback."""

    def __init__(self):
        self.provider = os.getenv('AI_PROVIDER', 'none').lower().strip()
        self.api_key = os.getenv('AI_API_KEY', '').strip()

    def generate_algorithm(self, language: str, code: str, detail_level: str) -> dict:
        """Attempts AI generation if configured; otherwise uses rule-based engine."""
        if not language or language.lower().strip() == 'auto':
            language = CodeAnalyzer.detect_language(code)
        if self.api_key and self.provider in ['gemini', 'openai']:
            try:
                if self.provider == 'gemini':
                    res = self._call_gemini(language, code, detail_level)
                    if res:
                        return res
                elif self.provider == 'openai':
                    res = self._call_openai(language, code, detail_level)
                    if res:
                        return res
            except Exception as err:
                print(f"[AIService Warning] LLM call failed ({err}). Falling back to rule-based engine.")

        # Fallback to local rule-based analysis
        return self.generate_fallback(language, code, detail_level)

    def generate_fallback(self, language: str, code: str, detail_level: str) -> dict:
        """Executes built-in offline analysis engine."""
        analyzer = CodeAnalyzer(language, code)
        analysis_data = analyzer.analyze()

        complexity_eval = ComplexityAnalyzer(analysis_data, code)
        complexity_data = complexity_eval.evaluate()

        generator = AlgorithmGenerator(analysis_data, complexity_data, code, detail_level)
        result = generator.generate()
        result["engine"] = "Rule-Based Analyzer Engine (Offline)"
        return result

    def _call_gemini(self, language: str, code: str, detail_level: str) -> dict:
        """Call Google Gemini REST API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

        prompt = self._build_prompt(language, code, detail_level)

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            text_content = data['candidates'][0]['content']['parts'][0]['text']
            parsed = json.loads(text_content)
            parsed["engine"] = "Google Gemini AI Engine"
            return parsed
        return None

    def _call_openai(self, language: str, code: str, detail_level: str) -> dict:
        """Call OpenAI REST API."""
        url = "https://api.openai.com/v1/chat/completions"

        prompt = self._build_prompt(language, code, detail_level)

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are Code2Algo AI, an expert algorithm analyst."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            text_content = data['choices'][0]['message']['content']
            parsed = json.loads(text_content)
            parsed["engine"] = "OpenAI AI Engine"
            return parsed
        return None

    def _build_prompt(self, language: str, code: str, detail_level: str) -> str:
        """Construct JSON prompt for LLM API."""
        return f"""
Analyze the following {language} code and generate an algorithm analysis in JSON format.
Detail Level Mode: {detail_level.upper()}

Return JSON matching this schema:
{{
  "title": "Algorithm Title",
  "detail_level": "{detail_level}",
  "algorithm": ["Step 1", "Step 2", ...],
  "pseudocode": "UPPERCASE Pseudocode text",
  "flowchart": "flowchart TD\\n  Start([Start]) --> Stop([Stop])",
  "sample_output": ">> Program Execution Output...\\nResult: 120\\n[Process Finished with Code 0]",
  "explanation": "Detailed explanation of code logic",
  "input": "Description of inputs",
  "output": "Description of outputs",
  "time_complexity": "O(...)",
  "time_explanation": "Rationale for time complexity",
  "space_complexity": "O(...)",
  "space_explanation": "Rationale for space complexity",
  "concepts": ["Concept 1", "Concept 2"],
  "detected_info": {{
    "language": "{language}",
    "functions": ["func1"],
    "variables": ["var1"],
    "loop_count": 1,
    "max_nesting_depth": 1,
    "data_structures": ["Array"],
    "has_recursion": false
  }}
}}

Source Code:
```{language}
{code}
```
"""
