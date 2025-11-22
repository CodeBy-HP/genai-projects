"""
🎓 Advanced Prompts - Professional Techniques

This example covers:
- Few-shot prompting (learning from examples)
- Output parsers (structured data)
- Prompt composition (combining prompts)
- Conditional prompting
- Prompt pipelines

Master these for production-ready applications!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
    PipelinePromptTemplate
)
from langchain_core.output_parsers import (
    JsonOutputParser,
    CommaSeparatedListOutputParser,
    StrOutputParser
)
from langchain_core.pydantic_v1 import BaseModel, Field

# Load environment variables
load_dotenv()


def few_shot_prompting():
    """Example 1: Few-shot prompting - Learn from examples"""
    
    print("=" * 70)
    print("🎓 Few-Shot Prompting - Teaching Through Examples")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,  # Lower for consistency
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define examples to teach the AI a pattern
    examples = [
        {
            "input": "happy",
            "output": "sad"
        },
        {
            "input": "tall",
            "output": "short"
        },
        {
            "input": "hot",
            "output": "cold"
        }
    ]
    
    # Template for each example
    example_template = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    )
    
    # Create few-shot prompt
    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_template,
        prefix="Give the antonym (opposite) of each word:",
        suffix="Input: {word}\nOutput:",
        input_variables=["word"]
    )
    
    print("\n📚 Teaching the AI with examples:")
    for ex in examples:
        print(f"   {ex['input']} → {ex['output']}")
    
    # Test with new words
    test_words = ["light", "fast", "loud"]
    
    for word in test_words:
        prompt = few_shot_template.format(word=word)
        
        print(f"\n📝 Prompt for '{word}':")
        print(prompt)
        print("\n🤖 Response:")
        
        response = chat.invoke(prompt)
        print(response.content)
    
    print("\n💡 Few-shot learning: Show examples, AI learns the pattern!")
    print()


def json_output_parser():
    """Example 2: Parse JSON output - Structured data"""
    
    print("=" * 70)
    print("📦 JSON Output Parser - Structured Responses")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define expected output structure
    class Recipe(BaseModel):
        name: str = Field(description="Name of the dish")
        ingredients: list[str] = Field(description="List of ingredients")
        cook_time: int = Field(description="Cooking time in minutes")
        difficulty: str = Field(description="Easy, Medium, or Hard")
    
    # Create parser
    parser = JsonOutputParser(pydantic_object=Recipe)
    
    # Create prompt with format instructions
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful cooking assistant. Always respond in valid JSON format."),
        ("human", "{query}\n\n{format_instructions}")
    ])
    
    # Format the prompt
    prompt = template.format_messages(
        query="Give me a simple pasta recipe",
        format_instructions=parser.get_format_instructions()
    )
    
    print("\n📋 Format Instructions sent to AI:")
    print(parser.get_format_instructions()[:200] + "...")
    
    print("\n👤 Query: Give me a simple pasta recipe")
    print("🤖 Response:")
    
    response = chat.invoke(prompt)
    print(response.content)
    
    # Parse the JSON
    try:
        parsed = parser.parse(response.content)
        print("\n✅ Parsed JSON:")
        print(f"   Name: {parsed['name']}")
        print(f"   Ingredients: {len(parsed['ingredients'])} items")
        print(f"   Cook Time: {parsed['cook_time']} minutes")
        print(f"   Difficulty: {parsed['difficulty']}")
    except Exception as e:
        print(f"\n⚠️  Parsing failed: {e}")
    
    print("\n💡 Output parsers convert text to structured data!")
    print()


def list_output_parser():
    """Example 3: Parse list output"""
    
    print("=" * 70)
    print("📝 List Output Parser - Comma-Separated Values")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create list parser
    parser = CommaSeparatedListOutputParser()
    
    # Create prompt with format instructions
    template = PromptTemplate(
        template="""List {count} {category}.

{format_instructions}

Your response:""",
        input_variables=["count", "category"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    queries = [
        {"count": "5", "category": "programming languages"},
        {"count": "3", "category": "data science tools"},
    ]
    
    for query in queries:
        prompt = template.format(**query)
        
        print(f"\n👤 Query: List {query['count']} {query['category']}")
        print("🤖 Response:")
        
        response = chat.invoke(prompt)
        print(response.content)
        
        # Parse the list
        try:
            parsed_list = parser.parse(response.content)
            print("\n✅ Parsed List:")
            for i, item in enumerate(parsed_list, 1):
                print(f"   {i}. {item.strip()}")
        except Exception as e:
            print(f"\n⚠️  Parsing failed: {e}")
    
    print("\n💡 List parsers extract clean arrays from text!")
    print()


def prompt_composition():
    """Example 4: Compose prompts from multiple pieces"""
    
    print("=" * 70)
    print("🔗 Prompt Composition - Building Modular Prompts")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define reusable prompt components
    tone_template = PromptTemplate.from_template(
        "Tone: {tone}"
    )
    
    audience_template = PromptTemplate.from_template(
        "Audience: {audience}"
    )
    
    task_template = PromptTemplate.from_template(
        """Task: {task}

Guidelines:
- Be {tone}
- Target audience: {audience}
- Keep it under {word_limit} words"""
    )
    
    # Combine them
    full_prompt = PromptTemplate.from_template(
        """{tone_section}
{audience_section}

{task_section}

Your response:"""
    )
    
    print("\n🏗️  Composing prompt from 3 components:")
    print("   1. Tone template")
    print("   2. Audience template")
    print("   3. Task template")
    
    # Format each component
    tone_text = tone_template.format(tone="professional and informative")
    audience_text = audience_template.format(audience="business executives")
    task_text = task_template.format(
        task="Explain the benefits of cloud computing",
        tone="professional and informative",
        audience="business executives",
        word_limit=150
    )
    
    # Combine into final prompt
    final_prompt = full_prompt.format(
        tone_section=tone_text,
        audience_section=audience_text,
        task_section=task_text
    )
    
    print("\n📝 Final Composed Prompt:")
    print(final_prompt)
    
    print("\n🤖 Response:")
    response = chat.invoke(final_prompt)
    print(response.content)
    
    print("\n💡 Composition allows reusable, modular prompts!")
    print("   Change one component without rewriting everything!")
    print()


def conditional_prompting():
    """Example 5: Conditional prompts based on context"""
    
    print("=" * 70)
    print("🔀 Conditional Prompting - Dynamic Behavior")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    def create_explanation_prompt(topic: str, user_level: str) -> str:
        """Create different prompts based on user level"""
        
        base_template = PromptTemplate.from_template(
            """You are a {role}.

Explain {topic}.

{additional_instructions}"""
        )
        
        # Conditional logic
        if user_level == "beginner":
            return base_template.format(
                role="patient teacher for absolute beginners",
                topic=topic,
                additional_instructions="Use simple words, everyday analogies, and avoid jargon. Keep it under 100 words."
            )
        elif user_level == "intermediate":
            return base_template.format(
                role="knowledgeable instructor",
                topic=topic,
                additional_instructions="Use technical terms but explain them. Include practical examples. 150 words max."
            )
        else:  # advanced
            return base_template.format(
                role="expert in the field",
                topic=topic,
                additional_instructions="Use advanced terminology, discuss edge cases and best practices. 200 words max."
            )
    
    topic = "recursion in programming"
    levels = ["beginner", "intermediate", "advanced"]
    
    print(f"\n📚 Topic: {topic}")
    print("🔀 Generating different explanations for each level:\n")
    
    for level in levels:
        prompt = create_explanation_prompt(topic, level)
        
        print(f"{'='*70}")
        print(f"👤 Level: {level.upper()}")
        print(f"{'='*70}")
        
        response = chat.invoke(prompt)
        print(f"🤖 Response:\n{response.content}\n")
    
    print("💡 Conditional prompts adapt to user context!")
    print()


def pipeline_prompts():
    """Example 6: Pipeline prompts - Sequential processing"""
    
    print("=" * 70)
    print("⚡ Pipeline Prompts - Sequential Processing")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Step 1: Extract key info
    extraction_template = PromptTemplate.from_template(
        """Extract the key information from this text:
        
Text: {input_text}

Extract:
- Main topic
- Key points (3 max)

Format as: Topic: X | Points: A, B, C"""
    )
    
    # Step 2: Create summary from extraction
    summary_template = PromptTemplate.from_template(
        """Based on this extracted information:
{extracted_info}

Write a one-sentence summary."""
    )
    
    print("\n📊 Two-Step Pipeline:")
    print("   Step 1: Extract key information")
    print("   Step 2: Create summary from extraction")
    
    input_text = """
    Machine learning is a subset of artificial intelligence that focuses on 
    building systems that learn from data. It includes supervised learning, 
    unsupervised learning, and reinforcement learning. Applications include 
    image recognition, natural language processing, and recommendation systems.
    """
    
    # Step 1: Extract
    print("\n🔹 Step 1: Extraction")
    extraction_prompt = extraction_template.format(input_text=input_text)
    extraction_response = chat.invoke(extraction_prompt)
    print(f"Result: {extraction_response.content}")
    
    # Step 2: Summarize
    print("\n🔹 Step 2: Summary")
    summary_prompt = summary_template.format(extracted_info=extraction_response.content)
    summary_response = chat.invoke(summary_prompt)
    print(f"Result: {summary_response.content}")
    
    print("\n💡 Pipelines break complex tasks into manageable steps!")
    print()


def advanced_output_parsing():
    """Example 7: Advanced output parsing with validation"""
    
    print("=" * 70)
    print("🎯 Advanced Output Parsing - With Validation")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define strict output schema
    class CodeReview(BaseModel):
        code_quality: int = Field(description="Quality score from 1-10", ge=1, le=10)
        issues: list[str] = Field(description="List of issues found")
        suggestions: list[str] = Field(description="List of improvement suggestions")
        overall_verdict: str = Field(description="Overall verdict: Excellent, Good, Fair, or Poor")
    
    parser = JsonOutputParser(pydantic_object=CodeReview)
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a code reviewer. Provide structured feedback in JSON format."),
        ("human", """Review this Python code:

```python
{code}
```

{format_instructions}""")
    ])
    
    code_to_review = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)
"""
    
    prompt = template.format_messages(
        code=code_to_review,
        format_instructions=parser.get_format_instructions()
    )
    
    print("\n👤 Reviewing code:")
    print(code_to_review)
    
    print("\n🤖 Structured Review:")
    
    response = chat.invoke(prompt)
    print(response.content)
    
    try:
        parsed = parser.parse(response.content)
        print("\n✅ Validation Passed! Parsed data:")
        print(f"   Quality Score: {parsed['code_quality']}/10")
        print(f"   Issues Found: {len(parsed['issues'])}")
        print(f"   Suggestions: {len(parsed['suggestions'])}")
        print(f"   Verdict: {parsed['overall_verdict']}")
    except Exception as e:
        print(f"\n⚠️  Validation failed: {e}")
    
    print("\n💡 Pydantic validation ensures data quality!")
    print()


def main():
    """Run all advanced prompt examples"""
    
    print("\n" + "🎓" * 35)
    print("Welcome to Advanced Prompts - Professional Techniques!")
    print("🎓" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        few_shot_prompting()
        input("Press Enter to continue...")
        
        json_output_parser()
        input("Press Enter to continue...")
        
        list_output_parser()
        input("Press Enter to continue...")
        
        prompt_composition()
        input("Press Enter to continue...")
        
        conditional_prompting()
        input("Press Enter to continue...")
        
        pipeline_prompts()
        input("Press Enter to continue...")
        
        advanced_output_parsing()
        
        print("=" * 70)
        print("✅ All Advanced Prompt examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ Few-shot prompting teaches patterns through examples")
        print("  ✓ Output parsers extract structured data")
        print("  ✓ Prompt composition enables modular design")
        print("  ✓ Conditional prompts adapt to context")
        print("  ✓ Pipelines break complex tasks into steps")
        print("  ✓ Pydantic validation ensures data quality")
        print("\n📚 Next: Try 04_practical_examples.py for real-world projects!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
