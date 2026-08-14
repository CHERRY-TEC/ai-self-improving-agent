# 🤖 AI Self-Improving Agent

An autonomous AI agent that modifies and improves its own code through iterative self-enhancement. Inspired by the AIDE² recursive self-improvement system.

## 🎯 What It Does

This agent:
1. **Reads** its own source code
2. **Analyzes** current performance metrics
3. **Suggests** improvements using an LLM
4. **Validates** changes are safe (syntax, security, reasonableness)
5. **Tests** the modified code against test cases
6. **Keeps** improvements that pass all checks
7. **Reverts** changes that don't improve metrics
8. **Repeats** until target score is reached

## Quick Start (100% FREE)

### Option 1: Ollama (RECOMMENDED - Runs locally, no API needed)

```bash
# 1. Install Ollama: https://ollama.com/download
# 2. Download model:
ollama pull codellama

# 3. Run agent:
python main.py --iterations 5
```

### Option 2: Local Rules (No AI, just rules)

```bash
python main.py --iterations 5 --provider local
```

### Option 3: With API (Costs money)

```bash
# OpenAI
export OPENAI_API_KEY="your-key"
python main.py --provider openai --model gpt-4

# Anthropic
export ANTHROPIC_API_KEY="your-key"
python main.py --provider anthropic --model claude-3-opus
```

## 📁 Project Structure

```
ai-self-improving-agent/
├── main.py              # Entry point - run this
├── agent.py             # Core self-improvement engine
├── evaluator.py         # Code quality & performance evaluator
├── safety.py            # Safety checks & validation
├── llm_interface.py     # LLM integration (OpenAI/Anthropic/Local)
├── config.py            # Configuration settings
├── test_cases.py        # Test cases for evaluation
├── agent_code/          # Code the agent improves
│   └── optimizer.py     # Target code file
├── backups/             # Automatic code backups
├── logs/                # Improvement history logs
└── requirements.txt     # Dependencies
```

## 🔧 How It Works

### The Self-Improvement Loop

```
┌─────────────────────────────────────────┐
│  1. Load Current Code                   │
│  2. Evaluate (syntax, tests, speed)     │
│  3. Ask LLM for Improvement             │
│  4. Safety Check                        │
│     - Syntax valid?                     │
│     - No dangerous patterns?            │
│     - Reasonable change size?           │
│  5. Evaluate New Code                   │
│  6. Compare Scores                      │
│     - Better? → Keep & Save             │
│     - Worse? → Revert                   │
│  7. Repeat                              │
└─────────────────────────────────────────┘
```

### Safety Features

- **Syntax Validation**: Catches errors before applying changes
- **Forbidden Patterns**: Blocks dangerous code (`os.system`, `eval`, etc.)
- **File Size Limits**: Prevents excessively large modifications
- **Change Ratio Check**: Rejects changes that are too drastic (>80% diff)
- **Automatic Backups**: Saves code before each modification
- **Rollback Capability**: Reverts to last good version

### Metrics Tracked

| Metric | Description |
|--------|-------------|
| Syntax Valid | Whether code parses without errors |
| Test Pass Rate | Percentage of test cases passing |
| Execution Time | Speed benchmark |
| Docstring Coverage | Functions with docstrings |
| Type Hint Coverage | Functions with type hints |
| Comment Ratio | Comments vs code lines |
| Overall Score | Weighted combination |

## 🎯 Improvement Targets

- `"speed"` - Focus on performance optimization
- `"readability"` - Focus on code clarity and documentation
- `"features"` - Add new functionality
- `"overall improvement"` - Balance all metrics (default)

## 📊 Example Output

```
🤖 AI SELF-IMPROVING AGENT
============================================================
Target file: agent_code/optimizer.py
Max iterations: 5

📊 Evaluating initial code...
   Initial Score: 0.3421
   Syntax Valid: True
   Test Pass Rate: 100.0%
   Execution Time: 0.000123s

🔄 Iteration 1/5
💡 Asking LLM for improvements...
   🔒 Running safety checks...
   ✅ Safety checks passed
📊 Evaluating improved code...
   New Score: 0.4156 (diff: +0.0735)
   🎉 IMPROVEMENT FOUND!

📈 SELF-IMPROVEMENT SUMMARY
Total Iterations: 5
Final Best Score: 0.5234
Successful Improvements: 3/5
```

## Free vs Paid Comparison

| Option | Cost | Quality | Setup |
|--------|------|---------|-------|
| **Ollama** | FREE | High | Install Ollama + download model |
| **HuggingFace** | FREE (limited) | Medium | Sign up for free account |
| **Local Rules** | FREE | Basic | Nothing needed |
| **OpenAI** | ~$0.01-0.10/run | Very High | API key required |
| **Anthropic** | ~$0.01-0.10/run | Very High | API key required |

**Recommendation**: Use **Ollama** for best free experience. See `FREE_SETUP.md` for instructions.

## Test Cases Included

The agent tests against these functions:
- `calculate_stats()` - Statistical calculations
- `is_prime()` - Prime number check
- `fibonacci()` - Fibonacci sequence generation
- `binary_search()` - Binary search algorithm

## ⚙️ Configuration

Edit `config.py` to customize:

```python
MAX_ITERATIONS = 10              # Max improvement attempts
IMPROVEMENT_THRESHOLD = 0.05     # Min score improvement to keep
MAX_FILE_SIZE_KB = 100           # Max code file size
SAFETY_CHECK_ENABLED = True     # Enable safety checks
```

## 🔬 How Self-Improvement Works

### Phase 1: Analysis
The agent parses the code using Python's AST module and measures:
- Code complexity
- Documentation quality
- Execution performance
- Test coverage

### Phase 2: Generation
Using an LLM (or local rules), the agent generates improved versions that:
- Maintain existing functionality
- Add optimizations
- Improve documentation
- Add new features

### Phase 3: Validation
Each proposed change goes through:
1. Syntax checking
2. Security scanning
3. Reasonableness validation
4. Test execution
5. Performance benchmarking

### Phase 4: Selection
The agent keeps changes only if:
- All tests pass
- No safety violations
- Score improves beyond threshold
- Code is syntactically valid

## 🛡️ Safety Guarantees

1. **No destructive operations**: Agent can't delete files or execute system commands
2. **Syntax-first**: Invalid code is rejected immediately
3. **Backup everything**: Every version is saved before modification
4. **Revert on failure**: Bad changes are automatically rolled back
5. **Human oversight**: All changes are logged and reviewable

## 🚧 Limitations

- Local mode uses rule-based improvements (limited creativity)
- API mode requires internet connection and API key
- Complex architectural changes are not supported
- Agent optimizes the target file, not itself (yet!)

## 🔮 Future Improvements

- [ ] Multi-file self-improvement
- [ ] Learning from improvement history
- [ ] A/B testing of multiple suggestions
- [ ] Git integration for version control
- [ ] Web dashboard for monitoring
- [ ] Support for more programming languages

## 📚 References

- [AIDE²: Recursive Self-Improvement](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement)
- [Karpathy's Autoresearch](https://github.com/karpathy/autoresearch)
- [VibeTensor: AI-Generated Deep Learning](https://github.com/NVlabs/vibetensor)

## 📝 License

MIT License - Use freely for learning and research.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

---

**Note**: This is an educational project demonstrating recursive self-improvement concepts. For production use, add more comprehensive safety measures and human oversight.
