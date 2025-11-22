"""
📄 Basic Prompts - Foundation of Prompt Engineering

This example covers:
- Static prompts (hardcoded)
- Dynamic prompts (with variables)
- PromptTemplate basics
- Partial variables
- Template validation

Master these fundamentals before moving to advanced topics!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Load environment variables
load_dotenv()


def static_prompt_example():
    """Example 1: Static prompts - simple but inflexible"""
    
    print("=" * 70)
    print("📄 Static Prompts - The Basic Approach")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Static prompt - hardcoded, never changes
    static_prompt = "Explain what machine learning is in simple terms."
    
    print(f"\n📝 Static Prompt: {static_prompt}")
    print("\n🤖 Response:")
    
    response = chat.invoke(static_prompt)
    print(response.content)
    
    print("\n💡 Problem: What if we want to explain different topics?")
    print("   We'd need to write a new prompt each time! 😓")
    print()


def dynamic_prompt_example():
    """Example 2: Dynamic prompts using f-strings"""
    
    print("=" * 70)
    print("🔄 Dynamic Prompts - Adding Flexibility")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Function to create dynamic prompts
    def create_explanation_prompt(topic: str, audience: str) -> str:
        return f"Explain {topic} in simple terms for {audience}."
    
    # Use the same pattern for different topics!
    topics = [
        ("quantum computing", "high school students"),
        ("blockchain", "business executives"),
    ]
    
    for topic, audience in topics:
        prompt = create_explanation_prompt(topic, audience)
        
        print(f"\n📝 Dynamic Prompt: {prompt}")
        print(f"   Topic: {topic}")
        print(f"   Audience: {audience}")
        print("\n🤖 Response:")
        
        response = chat.invoke(prompt)
        print(response.content[:200] + "...\n")
    
    print("💡 Better! But we can do even better with PromptTemplate! 🚀")
    print()


def prompt_template_basics():
    """Example 3: PromptTemplate - The LangChain way"""
    
    print("=" * 70)
    print("📋 PromptTemplate - Professional Approach")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create a reusable template
    template = PromptTemplate(
        input_variables=["topic", "audience"],
        template="Explain {topic} in simple terms for {audience}. Keep it under 100 words."
    )
    
    print("\n📋 Template Created:")
    print(f"   Variables: {template.input_variables}")
    print(f"   Template: {template.template}")
    
    # Use the template multiple times
    test_cases = [
        {"topic": "neural networks", "audience": "beginners"},
        {"topic": "APIs", "audience": "non-technical managers"},
    ]
    
    for case in test_cases:
        # Format the template with values
        prompt = template.format(**case)
        
        print(f"\n📝 Formatted Prompt for '{case['topic']}':")
        print(f"   {prompt}")
        print("\n🤖 Response:")
        
        response = chat.invoke(prompt)
        print(response.content)
        print()
    
    print("✨ Benefits of PromptTemplate:")
    print("   ✓ Reusable across your app")
    print("   ✓ Variables are validated")
    print("   ✓ Easy to maintain and update")
    print("   ✓ Can be saved and version controlled")
    print()


def prompt_template_with_formatting():
    """Example 4: Advanced template formatting"""
    
    print("=" * 70)
    print("🎨 Advanced PromptTemplate Formatting")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Template with multiple variables and structure
    template = PromptTemplate(
        input_variables=["role", "task", "context", "constraints"],
        template="""You are a {role}.

Task: {task}

Context:
{context}

Constraints:
{constraints}

Provide your response:"""
    )
    
    # Fill the template
    prompt = template.format(
        role="Python programming tutor",
        task="Explain list comprehensions",
        context="The student knows basic for loops but not list comprehensions",
        constraints="- Use simple examples\n- Limit to 150 words\n- Include one code example"
    )
    
    print("\n📋 Structured Template:")
    print(prompt)
    print("\n🤖 Response:")
    
    response = chat.invoke(prompt)
    print(response.content)
    
    print("\n💡 Notice: Well-structured prompts get better responses!")
    print()


def partial_variables_example():
    """Example 5: Partial variables - Pre-fill some values"""
    
    print("=" * 70)
    print("🎯 Partial Variables - Pre-configured Templates")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create a template with some pre-filled values
    base_template = PromptTemplate(
        input_variables=["question"],
        template="""You are a helpful coding assistant.
You always:
- Provide working code examples
- Explain your reasoning
- Use Python 3.10+ syntax

Question: {question}

Answer:"""
    )
    
    print("\n📋 Template with Pre-configured Personality:")
    print("   The system behavior is baked into the template!")
    
    questions = [
        "How do I read a JSON file?",
        "What's the difference between a list and a tuple?"
    ]
    
    for question in questions:
        prompt = base_template.format(question=question)
        
        print(f"\n❓ Question: {question}")
        print("\n🤖 Response:")
        
        response = chat.invoke(prompt)
        print(response.content[:300] + "...")
        print()
    
    print("💡 Use partial templates to maintain consistency!")
    print()


def template_from_string():
    """Example 6: Quick template creation from string"""
    
    print("=" * 70)
    print("⚡ Quick Template Creation")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Shorthand: Create template directly from string
    template = PromptTemplate.from_template(
        "Translate the following to {language}: {text}"
    )
    
    # LangChain auto-detects the variables!
    print(f"\n✨ Auto-detected variables: {template.input_variables}")
    
    translations = [
        {"language": "Spanish", "text": "Hello, how are you?"},
        {"language": "French", "text": "Good morning!"},
        {"language": "German", "text": "Thank you very much!"}
    ]
    
    for trans in translations:
        prompt = template.format(**trans)
        
        print(f"\n🌍 Translating to {trans['language']}: {trans['text']}")
        print("🤖 Translation:")
        
        response = chat.invoke(prompt)
        print(response.content)
    
    print("\n💡 from_template() is quick for simple templates!")
    print()


def template_validation():
    """Example 7: Template validation catches errors"""
    
    print("=" * 70)
    print("🛡️ Template Validation - Catch Errors Early")
    print("=" * 70)
    
    template = PromptTemplate(
        input_variables=["name", "age", "city"],
        template="Hello {name}, you are {age} years old and live in {city}."
    )
    
    print("\n📋 Template requires: name, age, city")
    
    # Correct usage
    print("\n✅ Correct usage (all variables provided):")
    try:
        prompt = template.format(name="Alice", age=25, city="NYC")
        print(f"   {prompt}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Missing variable
    print("\n❌ Missing variable (forgot 'city'):")
    try:
        prompt = template.format(name="Bob", age=30)
        print(f"   {prompt}")
    except KeyError as e:
        print(f"   ⚠️  Error caught: Missing variable {e}")
        print("   This helps catch bugs before sending to AI!")
    
    # Extra variable (this is OK)
    print("\n⚠️  Extra variable (added 'country'):")
    try:
        prompt = template.format(name="Charlie", age=28, city="London", country="UK")
        print(f"   {prompt}")
        print("   ✓ Extra variables are ignored (no error)")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n💡 Validation helps prevent runtime errors!")
    print()


def comparing_approaches():
    """Example 8: Side-by-side comparison"""
    
    print("=" * 70)
    print("⚖️  Comparing All Approaches")
    print("=" * 70)
    
    topic = "artificial intelligence"
    
    # Approach 1: Static
    static = "Explain artificial intelligence in one sentence."
    
    # Approach 2: F-string
    dynamic = f"Explain {topic} in one sentence."
    
    # Approach 3: PromptTemplate
    template = PromptTemplate.from_template(
        "Explain {topic} in one sentence."
    )
    templated = template.format(topic=topic)
    
    print("\n1️⃣  Static Prompt:")
    print(f"    {static}")
    print("    ❌ Hardcoded - can't reuse")
    
    print("\n2️⃣  F-string Prompt:")
    print(f"    {dynamic}")
    print("    ⚠️  Flexible but no validation")
    
    print("\n3️⃣  PromptTemplate:")
    print(f"    {templated}")
    print("    ✅ Flexible + Validated + Reusable")
    
    print("\n🏆 Winner: PromptTemplate for production apps!")
    print()


def main():
    """Run all basic prompt examples"""
    
    print("\n" + "📄" * 35)
    print("Welcome to Basic Prompts - LangChain Fundamentals!")
    print("📄" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        static_prompt_example()
        input("Press Enter to continue...")
        
        dynamic_prompt_example()
        input("Press Enter to continue...")
        
        prompt_template_basics()
        input("Press Enter to continue...")
        
        prompt_template_with_formatting()
        input("Press Enter to continue...")
        
        partial_variables_example()
        input("Press Enter to continue...")
        
        template_from_string()
        input("Press Enter to continue...")
        
        template_validation()
        input("Press Enter to continue...")
        
        comparing_approaches()
        
        print("=" * 70)
        print("✅ All Basic Prompt examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ Static prompts are simple but inflexible")
        print("  ✓ Dynamic prompts add variables")
        print("  ✓ PromptTemplate is the professional way")
        print("  ✓ Templates are reusable and validated")
        print("  ✓ Use from_template() for quick creation")
        print("  ✓ Validation catches errors early")
        print("\n📚 Next: Try 02_chat_prompts.py for conversation prompts!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
