#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_context7_mcp.crew import CrewaiContext7Mcp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")


def run():
    """
    Run the crew.
    """
    inputs = {
        'library_name': '/crewaiinc/crewai',
        'topic': input('Enter a question: '),
    }
    
    try:
        CrewaiContext7Mcp().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "CrewAI Flows",
    }
    try:
        CrewaiContext7Mcp().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiContext7Mcp().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "CrewAI Flows",
    }
    
    try:
        CrewaiContext7Mcp().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
