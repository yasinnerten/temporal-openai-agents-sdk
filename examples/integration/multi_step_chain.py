"""
Multi-step AI workflow chaining multiple OpenAI operations.

This workflow demonstrates:
1. Generating content with OpenAI
2. Analyzing the generated content
3. Summarizing the analysis
4. Combining results with temporal orchestration
"""

from datetime import timedelta
from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from openai import OpenAI
from typing import TypedDict
import os


class GeneratedContent(TypedDict):
    content: str
    word_count: int


class AnalysisResult(TypedDict):
    content: str
    summary: str
    sentiment: str
    key_points: list[str]


@activity.defn
async def generate_content(topic: str, length: str = "short") -> GeneratedContent:
    """Generate content about a given topic using OpenAI.

    Args:
        topic: The topic to write about
        length: Length of content ("short", "medium", "long")

    Returns:
        GeneratedContent with content and word count
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    token_limits = {"short": 150, "medium": 300, "long": 500}
    max_tokens = token_limits.get(length, 150)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a content writer who creates informative and engaging text.",
            },
            {
                "role": "user",
                "content": f"Write a {length} explanation about {topic}. Focus on key concepts and practical applications.",
            },
        ],
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content or ""
    return {"content": content, "word_count": len(content.split())}


@activity.defn
async def analyze_content(content: str) -> dict[str, str]:
    """Analyze the generated content using OpenAI.

    Args:
        content: Text to analyze

    Returns:
        Dictionary with sentiment, summary, and key insights
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a content analyst. Analyze text and provide insights in JSON format.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following content and provide:
1. Sentiment (positive/neutral/negative)
2. One-sentence summary
3. Key insights (comma-separated)

Content: {content}""",
            },
        ],
        max_tokens=200,
    )

    return {"analysis": response.choices[0].message.content or ""}


@activity.defn
async def summarize_analysis(generated_content: str, analysis: str) -> dict[str, str]:
    """Create a final summary combining content and analysis.

    Args:
        generated_content: Original generated content
        analysis: Analysis of the content

    Returns:
        Dictionary with combined summary and metadata
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a content curator who creates engaging summaries.",
            },
            {
                "role": "user",
                "content": f"""Create a concise, engaging summary that combines:
- The main content
- The key analysis points

Content: {generated_content[:200]}...
Analysis: {analysis}

Provide a summary that highlights the most important aspects in 2-3 sentences.""",
            },
        ],
        max_tokens=150,
    )

    return {
        "final_summary": response.choices[0].message.content or "",
        "original_content_length": str(len(generated_content)),
        "analysis_length": str(len(analysis)),
    }


@activity.defn
async def extract_key_points(combined_text: str) -> list[str]:
    """Extract key bullet points from combined text.

    Args:
        combined_text: Text containing both content and analysis

    Returns:
        List of key points
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract 3-5 key bullet points from the text.",
            },
            {
                "role": "user",
                "content": f"Extract the main takeaways as bullet points:\n\n{combined_text}",
            },
        ],
        max_tokens=200,
    )

    content = response.choices[0].message.content or ""
    return [point.strip("- ").strip() for point in content.split("\n") if point.strip()]


@workflow.defn
class MultiStepAIChainWorkflow:
    """Workflow that chains multiple AI operations."""

    @workflow.run
    async def run(self, topic: str, length: str = "medium") -> dict[str, str]:
        """Run the multi-step AI chain workflow.

        Args:
            topic: Topic to generate content about
            length: Length of content to generate

        Returns:
            Dictionary with all results from the chain
        """
        step1_result = await workflow.execute_activity(
            generate_content,
            topic,
            length,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        step2_result = await workflow.execute_activity(
            analyze_content,
            step1_result["content"],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        step3_result = await workflow.execute_activity(
            summarize_analysis,
            step1_result["content"],
            step2_result["analysis"],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        combined_text = f"{step1_result['content']}\n\n{step2_result['analysis']}\n\n{step3_result['final_summary']}"

        step4_result = await workflow.execute_activity(
            extract_key_points,
            combined_text,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        return {
            "topic": topic,
            "generated_content": step1_result["content"],
            "content_word_count": str(step1_result["word_count"]),
            "analysis": step2_result["analysis"],
            "final_summary": step3_result["final_summary"],
            "key_points": "; ".join(step4_result),
        }
