"""
Main orchestrator for the Self-Improving Agent.
Run this file to start the agent.
"""
import argparse
import sys
from agent import SelfImprovingAgent


def main():
    parser = argparse.ArgumentParser(
        description="AI Self-Improving Agent - An agent that improves its own code"
    )
    parser.add_argument(
        "--iterations", "-i",
        type=int,
        default=5,
        help="Number of improvement iterations (default: 5)"
    )
    parser.add_argument(
        "--target", "-t",
        type=str,
        default="overall improvement",
        help="Improvement target: 'speed', 'readability', 'features', 'overall improvement'"
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        default="ollama",
        choices=["local", "openai", "anthropic", "ollama", "huggingface"],
        help="LLM provider (default: ollama - FREE)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="codellama",
        help="LLM model name (default: codellama for ollama)"
    )
    
    args = parser.parse_args()
    
    print("""
    ============================================================
    |           AI SELF-IMPROVING AGENT v1.0                  |
    |                                                         |
    |   An autonomous agent that modifies and improves        |
    |   its own code through iterative self-enhancement.      |
    ============================================================
    """)
    
    print(f"Configuration:")
    print(f"  Iterations: {args.iterations}")
    print(f"  Target: {args.target}")
    print(f"  Provider: {args.provider}")
    print(f"  Model: {args.model}")
    print()
    
    agent = SelfImprovingAgent(
        llm_provider=args.provider,
        llm_model=args.model
    )
    
    try:
        agent.run(
            max_iterations=args.iterations,
            target=args.target
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Agent stopped by user.")
        agent._print_summary()
        sys.exit(0)


if __name__ == "__main__":
    main()
