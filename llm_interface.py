"""
LLM Interface for the self-improving agent.
Supports OpenAI, Anthropic, Ollama (FREE), HuggingFace (FREE), and local fallback.
"""
import json
import os
import requests
from typing import Optional, Dict, Any


class LLMInterface:
    """Interface to interact with LLMs for code generation."""
    
    def __init__(self, provider: str = "local", model: str = "local"):
        self.provider = provider
        self.model = model
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            try:
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    self.client = openai.OpenAI(api_key=api_key)
                else:
                    print("Warning: No OpenAI API key found. Using Ollama (free) instead.")
                    self.provider = "ollama"
                    self.model = "codellama"
            except ImportError:
                print("Warning: openai package not installed. Using Ollama (free) instead.")
                self.provider = "ollama"
                self.model = "codellama"
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    self.client = anthropic.Anthropic(api_key=api_key)
                else:
                    print("Warning: No Anthropic API key found. Using Ollama (free) instead.")
                    self.provider = "ollama"
                    self.model = "codellama"
            except ImportError:
                print("Warning: anthropic package not installed. Using Ollama (free) instead.")
                self.provider = "ollama"
                self.model = "codellama"
        
        elif self.provider == "ollama":
            # Ollama runs locally - no API key needed!
            print(f"Using Ollama (FREE) with model: {self.model}")
            print("Make sure Ollama is running: ollama serve")
    
    def suggest_improvement(self, code: str, metrics: dict, target: str) -> str:
        """Get improvement suggestions from LLM."""
        prompt = self._build_improvement_prompt(code, metrics, target)
        
        if self.provider == "openai" and self.client:
            return self._openai_generate(prompt)
        elif self.provider == "anthropic" and self.client:
            return self._anthropic_generate(prompt)
        elif self.provider == "ollama":
            return self._ollama_generate(prompt)
        elif self.provider == "huggingface":
            return self._huggingface_generate(prompt)
        else:
            return self._local_improvement(code, metrics, target)
    
    def _build_improvement_prompt(self, code: str, metrics: dict, target: str) -> str:
        return f"""You are an AI code improvement agent. Your task is to improve the given code.

Current Code:
```python
{code}
```

Current Metrics:
{json.dumps(metrics, indent=2)}

Improvement Target: {target}

Rules:
1. Maintain the same function signatures and behavior
2. Improve performance, readability, or add new features
3. Keep all existing tests passing
4. Only output the improved code, no explanations
5. Code must be syntactically valid Python

Improved Code:
"""
    
    def _openai_generate(self, prompt: str) -> str:
        """Generate using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            return ""
    
    def _anthropic_generate(self, prompt: str) -> str:
        """Generate using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Anthropic error: {e}")
            return ""
    
    def _ollama_generate(self, prompt: str) -> str:
        """Generate using Ollama (FREE - runs locally)."""
        try:
            # Default Ollama endpoint
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2000
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                print(f"Ollama error: {response.status_code}")
                return ""
        except requests.exceptions.ConnectionError:
            print("Cannot connect to Ollama. Is it running?")
            print("Start it with: ollama serve")
            return ""
        except Exception as e:
            print(f"Ollama error: {e}")
            return ""
    
    def _huggingface_generate(self, prompt: str) -> str:
        """Generate using HuggingFace free inference API."""
        try:
            # Free inference API - no key needed for some models
            API_URL = f"https://api-inference.huggingface.co/models/{self.model}"
            
            response = requests.post(
                API_URL,
                json={"inputs": prompt},
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                return str(result)
            else:
                print(f"HuggingFace error: {response.status_code}")
                return ""
        except Exception as e:
            print(f"HuggingFace error: {e}")
            return ""
    
    def _local_improvement(self, code: str, metrics: dict, target: str) -> str:
        """Local fallback: apply predefined improvements without API."""
        improved = code
        
        # Rule-based improvements
        if "speed" in target.lower() or "performance" in target.lower():
            # Add caching for fibonacci
            if "def fibonacci" in code:
                improved = improved.replace(
                    "def fibonacci(n):",
                    "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fibonacci(n):"
                )
            
            # Optimize prime check
            if "def is_prime" in code:
                improved = improved.replace(
                    "for i in range(3, int(math.sqrt(n)) + 1, 2):",
                    "sqrt_n = int(math.isqrt(n))\n    for i in range(3, sqrt_n + 1, 2):"
                )
        
        if "readability" in target.lower() or "quality" in target.lower():
            # Add type hints
            if "def calculate_stats(numbers):" in code:
                improved = improved.replace(
                    "def calculate_stats(numbers):",
                    "def calculate_stats(numbers: list[float]) -> dict:"
                )
            if "def is_prime(n):" in code:
                improved = improved.replace(
                    "def is_prime(n):",
                    "def is_prime(n: int) -> bool:"
                )
            if "def fibonacci(n):" in code:
                improved = improved.replace(
                    "def fibonacci(n):",
                    "def fibonacci(n: int) -> list[int]:"
                )
            if "def binary_search(arr, target):" in code:
                improved = improved.replace(
                    "def binary_search(arr, target):",
                    "def binary_search(arr: list[int], target: int) -> int:"
                )
        
        if "feature" in target.lower():
            # Add a new function
            if "def calculate_stats" in code and "def percentile" not in code:
                new_func = '''

def percentile(numbers: list[float], p: float) -> float:
    """Calculate the p-th percentile of a list of numbers."""
    sorted_nums = sorted(numbers)
    k = (len(sorted_nums) - 1) * (p / 100)
    f = int(k)
    c = f + 1
    if c >= len(sorted_nums):
        return sorted_nums[f]
    return sorted_nums[f] + (k - f) * (sorted_nums[c] - sorted_nums[f])
'''
                improved = improved.replace(
                    "def is_prime",
                    new_func + "\ndef is_prime"
                )
        
        return improved
