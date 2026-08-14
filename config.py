"""
Configuration for the Self-Improving Agent
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
AGENT_CODE_DIR = BASE_DIR / "agent_code"
BACKUP_DIR = BASE_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"
TESTS_DIR = BASE_DIR / "tests"

# Create directories
BACKUP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# LLM Configuration (supports multiple providers)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, local
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Agent Settings
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
IMPROVEMENT_THRESHOLD = float(os.getenv("IMPROVEMENT_THRESHOLD", "0.05"))
SAFETY_CHECK_ENABLED = True
MAX_FILE_SIZE_KB = 100
ALLOWED_EXTENSIONS = [".py", ".md", ".json"]
FORBIDDEN_PATTERNS = [
    "os.system", "subprocess", "shutil.rmtree",
    "eval(", "exec(", "__import__", "open('/etc"
]

# Evaluation Settings
METRICS = ["accuracy", "speed", "code_quality", "test_pass_rate"]
