from crewai import Agent, LLM
import logging
import os

logger = logging.getLogger(__name__)



class AgentFactory:
    @staticmethod
    def get_llm():
        """Get OpenRouter LLM instance for CrewAI agents"""
        try:
            return LLM(
                model="openrouter/meta-llama/llama-3.1-8b-instruct",  
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                temperature=0.1,
                max_tokens=1024
            )
        except Exception as e:
            print(f"Failed to initialize LLM: {str(e)}")
            raise


    @staticmethod
    def create_agent(role: str, goal: str, backstory: str, allow_delegation: bool = False) -> Agent:
        """Create a CrewAI agent with specified parameters"""
        try:
            llm = AgentFactory.get_llm()
            
            return Agent(
                role=role,
                goal=goal,
                backstory=backstory,
                verbose=True,
                llm=llm,
                allow_delegation=allow_delegation
            )
        except Exception as e:
            logger.error(f"Failed to create agent {role}: {str(e)}")
            raise