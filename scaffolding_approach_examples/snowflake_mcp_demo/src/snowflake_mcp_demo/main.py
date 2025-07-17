#!/usr/bin/env python
"""
3-Agent Regulatory Risk Monitoring System

This system provides comprehensive regulatory monitoring for asset managers using:
- Regulatory Intelligence Agent: Analyzes new regulations from web sources
- Portfolio SEC Analyst: Historical SEC filing analysis 
- Market News Analyst: Current market reactions and analyst opinions

Usage:
    python main.py  # Interactive mode
    crewai run      # CrewAI CLI mode

Requirements:
    - SERPER_API_KEY: For web search capabilities
    - SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PAT: For SEC filing data
"""

import sys
import warnings

from datetime import datetime

from snowflake_mcp_demo.crew import SnowflakeMcpDemo

# Suppress various deprecation warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="snowflake.connector.vendored.urllib3")
warnings.filterwarnings("ignore", message=".*PydanticDeprecatedSince20.*")
warnings.filterwarnings("ignore", message=".*Attempting to mutate a Context after a Connection was created.*")


def run():
    """
    Run the 3-agent regulatory monitoring crew.
    """
    print("🔍 3-Agent Regulatory Risk Monitoring System")
    print("=" * 50)
    
    # Show examples
    print("\n📋 Example URLs:")
    print("• FDA: https://www.fda.gov/news-events/press-announcements/...")
    print("• SEC: https://www.sec.gov/news/press-release/...")
    print("• Federal Reserve: https://www.federalreserve.gov/newsevents/...")
    print()
    
    # Get regulation URL (required)
    regulation_url = input("Enter regulation URL: ").strip()
    
    if not regulation_url:
        print("❌ Error: Regulation URL is required!")
        return
    
    # Get optional portfolio focus
    print("\n🎯 Portfolio Focus Examples:")
    print("• Healthcare companies, medical device manufacturers")
    print("• Regional banks, fintech companies")
    print("• Technology companies, cybersecurity firms")
    print("• Leave blank for general regulatory monitoring")
    print()
    
    portfolio_focus = input("Portfolio focus (optional - sectors/companies): ").strip()
    
    # Format input for the regulatory intelligence agent
    if portfolio_focus:
        user_input = f"Regulation URL: {regulation_url}\nPortfolio Focus: {portfolio_focus}"
    else:
        user_input = f"Regulation URL: {regulation_url}\nPortfolio Focus: General regulatory monitoring"
    
    inputs = {
        'user_input': user_input
    }
 
    print(f"📋 Regulation: {regulation_url}")
    if portfolio_focus:
        print(f"🎯 Portfolio Focus: {portfolio_focus}")
    print("\n" + "=" * 50)
    
    try:
        result = SnowflakeMcpDemo().crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 50)
        print("✅ Regulatory monitoring analysis complete!")
        print("=" * 50)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise Exception(f"An error occurred while running the regulatory monitoring crew: {e}")


def train():
    """
    Train the regulatory monitoring crew for a given number of iterations.
    """
    # Sample regulatory monitoring training data
    training_input = "Regulation URL: https://www.sec.gov/news/press-release/2024-31\nPortfolio Focus: Public companies with high environmental impact"
    
    inputs = {
        "user_input": training_input
    }
    try:
        SnowflakeMcpDemo().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the regulatory monitoring crew: {e}")

def replay():
    """
    Replay the regulatory monitoring crew execution from a specific task.
    """
    try:
        SnowflakeMcpDemo().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the regulatory monitoring crew: {e}")

def test():
    """
    Test the regulatory monitoring crew execution with sample data.
    """
    # Sample regulatory monitoring test data
    test_input = "Regulation URL: https://www.fda.gov/news-events/press-announcements/fda-announces-new-medical-device-cybersecurity-requirements\nPortfolio Focus: Healthcare technology companies, medical device manufacturers"
    
    inputs = {
        "user_input": test_input
    }
    
    try:
        SnowflakeMcpDemo().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the regulatory monitoring crew: {e}")
