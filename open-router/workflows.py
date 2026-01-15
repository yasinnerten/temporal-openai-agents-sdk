"""
Example workflows using OpenRouter models.
These workflows demonstrate different use cases with OpenRouter.
"""
from temporalio import workflow
from temporalio.contrib.openai_agents import OpenAIAgent


# Default free model
DEFAULT_MODEL = "deepseek/deepseek-r1:free"


@workflow.defn
class SimpleAgentWorkflow:
    """Basic workflow using OpenRouter's free DeepSeek model."""
    
    @workflow.run
    async def run(self, query: str) -> str:
        """
        Run a simple AI agent query.
        
        Args:
            query: User question or prompt
            
        Returns:
            AI response
        """
        agent = OpenAIAgent(
            model=DEFAULT_MODEL,
            system="You are a helpful AI assistant powered by DeepSeek R1.",
        )
        
        result = await agent.run(query)
        return result


@workflow.defn
class CodeAssistantWorkflow:
    """Workflow specialized for coding questions."""
    
    @workflow.run
    async def run(self, code_question: str) -> str:
        """
        Answer coding questions.
        
        Args:
            code_question: Programming question
            
        Returns:
            Code example and explanation
        """
        agent = OpenAIAgent(
            model=DEFAULT_MODEL,
            system=(
                "You are an expert programming assistant. "
                "Provide clear code examples with explanations. "
                "Focus on best practices and clean code."
            ),
        )
        
        result = await agent.run(code_question)
        return result


@workflow.defn
class DataAnalysisWorkflow:
    """Workflow for data analysis tasks."""
    
    @workflow.run
    async def run(self, analysis_request: str) -> str:
        """
        Perform data analysis.
        
        Args:
            analysis_request: Description of analysis needed
            
        Returns:
            Analysis results and insights
        """
        agent = OpenAIAgent(
            model=DEFAULT_MODEL,
            system=(
                "You are a data analysis expert. "
                "Provide insights, patterns, and recommendations. "
                "Use clear explanations and suggest visualizations when relevant."
            ),
        )
        
        result = await agent.run(analysis_request)
        return result


def create_custom_workflow(model: str, system_prompt: str):
    """
    Factory function to create custom workflows.
    
    Args:
        model: OpenRouter model ID
        system_prompt: Custom system prompt
        
    Returns:
        Workflow class configured with custom settings
    """
    @workflow.defn
    class CustomWorkflow:
        @workflow.run
        async def run(self, query: str) -> str:
            agent = OpenAIAgent(
                model=model,
                system=system_prompt,
            )
            return await agent.run(query)
    
    return CustomWorkflow