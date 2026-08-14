"""
Safety module to prevent dangerous code modifications.
"""
import re
from config import FORBIDDEN_PATTERNS, MAX_FILE_SIZE_KB, ALLOWED_EXTENSIONS


class SafetyChecker:
    """Validates code changes before applying them."""
    
    def __init__(self):
        self.violations = []
    
    def check_code_safety(self, code: str, filename: str) -> tuple[bool, list[str]]:
        """Check if code is safe to apply."""
        self.violations = []
        
        # Check file extension
        if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            self.violations.append(f"File extension not allowed: {filename}")
        
        # Check file size
        size_kb = len(code.encode('utf-8')) / 1024
        if size_kb > MAX_FILE_SIZE_KB:
            self.violations.append(f"File too large: {size_kb:.1f}KB > {MAX_FILE_SIZE_KB}KB")
        
        # Check for forbidden patterns
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in code:
                self.violations.append(f"Forbidden pattern found: {pattern}")
        
        # Check for potentially dangerous imports
        dangerous_imports = ['subprocess', 'shutil', 'ctypes', 'signal']
        for imp in dangerous_imports:
            if re.search(rf'import\s+{imp}|from\s+{imp}\s+import', code):
                self.violations.append(f"Dangerous import: {imp}")
        
        # Check for infinite loops (basic detection)
        if re.search(r'while\s+True\s*:', code) and 'break' not in code:
            self.violations.append("Potential infinite loop detected")
        
        # Check syntax validity
        try:
            compile(code, filename, 'exec')
        except SyntaxError as e:
            self.violations.append(f"Syntax error: {e}")
        
        is_safe = len(self.violations) == 0
        return is_safe, self.violations
    
    def sanitize_code(self, code: str) -> str:
        """Basic code sanitization."""
        # Remove any null bytes
        code = code.replace('\x00', '')
        # Ensure file ends with newline
        if code and not code.endswith('\n'):
            code += '\n'
        return code


def validate_modification(original: str, modified: str) -> tuple[bool, str]:
    """Validate that a modification is reasonable."""
    # Check if modification is too different (more than 80% changed)
    original_lines = set(original.splitlines())
    modified_lines = set(modified.splitlines())
    
    if original_lines:
        change_ratio = len(original_lines.symmetric_difference(modified_lines)) / len(original_lines)
        if change_ratio > 0.8:
            return False, f"Modification too drastic: {change_ratio:.0%} of code changed"
    
    return True, "Modification looks reasonable"
