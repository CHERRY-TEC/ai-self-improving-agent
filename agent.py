"""
Core Self-Improving Agent Engine.
This is the main brain that modifies its own code.
"""
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import (
    AGENT_CODE_DIR, BACKUP_DIR, LOGS_DIR,
    MAX_ITERATIONS, IMPROVEMENT_THRESHOLD
)
from safety import SafetyChecker, validate_modification
from evaluator import CodeEvaluator
from llm_interface import LLMInterface
from test_cases import TEST_CASES


class SelfImprovingAgent:
    """Main agent that improves its own code autonomously."""
    
    def __init__(self, llm_provider: str = "local", llm_model: str = "local"):
        self.safety_checker = SafetyChecker()
        self.evaluator = CodeEvaluator()
        self.llm = LLMInterface(provider=llm_provider, model=llm_model)
        self.iteration = 0
        self.history = []
        self.best_code = None
        self.best_score = 0.0
        self.target_file = AGENT_CODE_DIR / "optimizer.py"
        self.log_file = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def run(self, max_iterations: int = None, target: str = "overall improvement"):
        """Run the self-improvement loop."""
        max_iter = max_iterations or MAX_ITERATIONS
        
        print("=" * 60)
        print("AI SELF-IMPROVING AGENT")
        print("=" * 60)
        print(f"Target file: {self.target_file}")
        print(f"Max iterations: {max_iter}")
        print(f"Improvement threshold: {IMPROVEMENT_THRESHOLD}")
        print("=" * 60)
        
        # Load initial code
        initial_code = self._load_code()
        if not initial_code:
            print(" Error: Could not load target code")
            return
        
        # Evaluate initial state
        print("\n Evaluating initial code...")
        initial_metrics = self.evaluator.evaluate(initial_code, TEST_CASES)
        self.best_code = initial_code
        self.best_score = initial_metrics["overall_score"]
        
        print(f"   Initial Score: {self.best_score:.4f}")
        print(f"   Syntax Valid: {initial_metrics['syntax_valid']}")
        print(f"   Test Pass Rate: {initial_metrics['test_pass_rate']:.1%}")
        print(f"   Execution Time: {initial_metrics['execution_time']:.6f}s")
        
        # Create backup
        self._backup_code(initial_code, "initial")
        
        # Main improvement loop
        for i in range(max_iter):
            self.iteration = i + 1
            print(f"\n{'='*60}")
            print(f"Iteration {self.iteration}/{max_iter}")
            print(f"{'='*60}")
            
            # Get improvement suggestion
            print("Asking LLM for improvements...")
            improved_code = self.llm.suggest_improvement(
                self.best_code,
                self.evaluator.metrics_history[-1] if self.evaluator.metrics_history else {},
                target
            )
            
            if not improved_code:
                print("   [!] No improvement suggestion received. Skipping.")
                continue
            
            # Clean code if wrapped in markdown
            improved_code = self._clean_code_output(improved_code)
            
            # Safety check
            print("Running safety checks...")
            is_safe, violations = self.safety_checker.check_code_safety(
                improved_code, "optimizer.py"
            )
            if not is_safe:
                print(f"   [FAIL] Safety violations: {violations}")
                continue
            
            # Validate modification reasonableness
            is_valid, msg = validate_modification(self.best_code, improved_code)
            if not is_valid:
                print(f"   [FAIL] Modification rejected: {msg}")
                continue
            
            print("   [OK] Safety checks passed")
            
            # Evaluate improved code
            print("Evaluating improved code...")
            new_metrics = self.evaluator.evaluate(improved_code, TEST_CASES)
            new_score = new_metrics["overall_score"]
            
            # Compare with best
            score_diff = new_score - self.best_score
            improved = new_score > self.best_score + IMPROVEMENT_THRESHOLD
            
            print(f"   New Score: {new_score:.4f} (diff: {score_diff:+.4f})")
            print(f"   Test Pass Rate: {new_metrics['test_pass_rate']:.1%}")
            print(f"   Execution Time: {new_metrics['execution_time']:.6f}s")
            
            if improved:
                print(f"   [WIN] IMPROVEMENT FOUND! (+{score_diff:.4f})")
                self.best_code = improved_code
                self.best_score = new_score
                self._save_code(improved_code)
                self._backup_code(improved_code, f"iteration_{self.iteration}")
            else:
                print(f"   [SKIP] No significant improvement. Keeping current best.")
            
            # Log iteration
            self._log_iteration(i + 1, new_metrics, score_diff, improved)
            
            # Check if we've reached a good enough solution
            if self.best_score >= 0.95:
                print("\n[TARGET] Target score reached! Stopping early.")
                break
        
        # Final summary
        self._print_summary()
    
    def _load_code(self) -> Optional[str]:
        """Load the target code file."""
        try:
            return self.target_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error loading code: {e}")
            return None
    
    def _save_code(self, code: str):
        """Save code to target file."""
        self.target_file.write_text(code, encoding='utf-8')
    
    def _clean_code_output(self, output: str) -> str:
        """Clean LLM output to extract just the code."""
        # Remove markdown code blocks
        if "```python" in output:
            output = output.split("```python")[1]
            if "```" in output:
                output = output.split("```")[0]
        elif "```" in output:
            output = output.split("```")[1]
            if "```" in output:
                output = output.split("```")[0]
        
        # Remove leading/trailing whitespace
        output = output.strip()
        
        # Remove any leading comments or explanations
        lines = output.splitlines()
        code_start = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('def ', 'class ', 'import ', 'from ', '@', '#')):
                code_start = i
                break
        
        return "\n".join(lines[code_start:])
    
    def _backup_code(self, code: str, label: str):
        """Create a backup of the current code."""
        backup_file = BACKUP_DIR / f"{label}_{datetime.now().strftime('%H%M%S')}.py"
        backup_file.write_text(code, encoding='utf-8')
    
    def _log_iteration(self, iteration: int, metrics: dict, score_diff: float, improved: bool):
        """Log iteration data."""
        entry = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "score_diff": score_diff,
            "improved": improved,
            "best_score": self.best_score
        }
        self.history.append(entry)
        
        # Save to file
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)
    
    def _print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 60)
        print("SELF-IMPROVEMENT SUMMARY")
        print("=" * 60)
        print(f"Total Iterations: {self.iteration}")
        print(f"Final Best Score: {self.best_score:.4f}")
        
        improvements = sum(1 for h in self.history if h["improved"])
        print(f"Successful Improvements: {improvements}/{self.iteration}")
        
        if self.evaluator.metrics_history:
            initial = self.evaluator.metrics_history[0]
            final = self.evaluator.metrics_history[-1]
            print(f"\nInitial  Final:")
            print(f"  Syntax Valid: {initial['syntax_valid']}  {final['syntax_valid']}")
            print(f"  Test Pass Rate: {initial['test_pass_rate']:.1%}  {final['test_pass_rate']:.1%}")
            print(f"  Execution Time: {initial['execution_time']:.6f}s  {final['execution_time']:.6f}s")
            print(f"  Functions: {initial.get('function_count', 0)}  {final.get('function_count', 0)}")
            print(f"  Type Hints: {initial.get('type_hint_coverage', 0):.0%}  {final.get('type_hint_coverage', 0):.0%}")
        
        print(f"\nLogs saved to: {self.log_file}")
        print(f"Backups saved to: {BACKUP_DIR}")
        print("=" * 60)
