"""
Evaluation module to measure code improvement.
"""
import time
import ast
import sys
import io
import math
from typing import Dict
from pathlib import Path


class CodeEvaluator:
    """Evaluates code quality and performance."""
    
    def __init__(self):
        self.metrics_history = []
    
    def evaluate(self, code: str, test_cases: list[dict] = None) -> dict:
        """Run all evaluations on the code."""
        metrics = {}
        
        # 1. Syntax check
        metrics["syntax_valid"] = self._check_syntax(code)
        
        # 2. Code quality metrics
        metrics.update(self._code_quality_metrics(code))
        
        # 3. Test execution
        if test_cases:
            test_results = self._run_tests(code, test_cases)
            metrics["test_pass_rate"] = test_results["pass_rate"]
            metrics["test_output"] = test_results["output"]
        else:
            metrics["test_pass_rate"] = 0
            metrics["test_output"] = ""
        
        # 4. Performance (execution time)
        metrics["execution_time"] = self._measure_execution_time(code)
        
        # 5. Overall score
        metrics["overall_score"] = self._calculate_overall_score(metrics)
        
        self.metrics_history.append(metrics)
        return metrics
    
    def _check_syntax(self, code: str) -> bool:
        """Check if code has valid syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    def _code_quality_metrics(self, code: str) -> dict:
        """Calculate code quality metrics."""
        lines = code.splitlines()
        non_empty = [l for l in lines if l.strip()]
        
        # Count functions and classes
        tree = ast.parse(code)
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        # Check for docstrings
        has_docstrings = sum(
            1 for n in functions 
            if n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)
        )
        
        # Check for type hints
        has_type_hints = sum(
            1 for n in functions 
            if n.returns is not None
        )
        
        # Check for comments
        comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
        
        total_lines = len(lines)
        code_lines = len(non_empty)
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / max(code_lines, 1),
            "function_count": len(functions),
            "class_count": len(classes),
            "docstring_coverage": has_docstrings / max(len(functions), 1),
            "type_hint_coverage": has_type_hints / max(len(functions), 1),
        }
    
    def _run_tests(self, code: str, test_cases: list[dict]) -> dict:
        """Execute test cases against the code."""
        passed = 0
        total = len(test_cases)
        outputs = []
        
        for test in test_cases:
            try:
                # Create isolated namespace
                namespace = {"__builtins__": __builtins__, "math": math}
                exec(code, namespace)
                
                # Run test function
                func_name = test.get("function", "")
                args = test.get("args", ())
                expected = test.get("expected")
                
                if func_name in namespace:
                    result = namespace[func_name](*args)
                    if result == expected:
                        passed += 1
                        outputs.append(f"PASS: {func_name}{args} = {result}")
                    else:
                        outputs.append(f"FAIL: {func_name}{args} = {result}, expected {expected}")
                else:
                    outputs.append(f"SKIP: {func_name} not found")
            except Exception as e:
                outputs.append(f"ERROR: {test.get('function', '?')} - {str(e)}")
        
        return {
            "passed": passed,
            "total": total,
            "pass_rate": passed / max(total, 1),
            "output": "\n".join(outputs)
        }
    
    def _measure_execution_time(self, code: str, iterations: int = 3) -> float:
        """Measure code execution time."""
        test_code = f"""
{code}

# Benchmark
if __name__ == "__main__":
    import time
    start = time.time()
    for _ in range({iterations}):
        calculate_stats([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        fibonacci(20)
    end = time.time()
    print(f"BENCHMARK_TIME:{{(end - start) / {iterations}:.6f}}")
"""
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            exec(test_code, {"__builtins__": __builtins__, "math": math})
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            for line in output.splitlines():
                if "BENCHMARK_TIME:" in line:
                    return float(line.split(":")[1])
        except Exception:
            pass
        
        return float('inf')
    
    def _calculate_overall_score(self, metrics: dict) -> float:
        """Calculate overall score from all metrics."""
        score = 0.0
        weights = {
            "syntax_valid": 0.2,
            "test_pass_rate": 0.3,
            "docstring_coverage": 0.1,
            "type_hint_coverage": 0.1,
            "comment_ratio": 0.05,
        }
        
        for key, weight in weights.items():
            if key in metrics:
                value = metrics[key]
                if isinstance(value, bool):
                    value = 1.0 if value else 0.0
                score += value * weight
        
        # Bonus for speed (lower is better)
        exec_time = metrics.get("execution_time", 1.0)
        speed_score = max(0, 1.0 - exec_time * 10)
        score += speed_score * 0.25
        
        return min(1.0, score)
    
    def compare_metrics(self, old: dict, new: dict) -> dict:
        """Compare old and new metrics."""
        comparison = {}
        for key in old:
            if key in new and isinstance(old[key], (int, float)):
                old_val = old[key]
                new_val = new[key]
                if old_val != 0:
                    change_pct = ((new_val - old_val) / old_val) * 100
                else:
                    change_pct = 100 if new_val > 0 else 0
                comparison[key] = {
                    "old": old_val,
                    "new": new_val,
                    "change": change_pct,
                    "improved": new_val > old_val if key != "execution_time" else new_val < old_val
                }
        return comparison
