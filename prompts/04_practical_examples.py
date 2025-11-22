"""
🚀 Practical Examples - Real-World Applications

This example showcases:
- Smart FAQ bot with few-shot learning
- Code generator with structured output
- Data extraction system
- Multi-step reasoning chatbot
- Content personalizer

Apply your prompt engineering skills to real projects!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
    MessagesPlaceholder
)
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field

# Load environment variables
load_dotenv()


def smart_faq_bot():
    """Project 1: Smart FAQ Bot with Few-Shot Learning"""
    
    print("=" * 70)
    print("🤖 Project 1: Smart FAQ Bot")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define FAQ examples to teach the pattern
    faq_examples = [
        {
            "question": "How do I reset my password?",
            "answer": "Go to Settings > Security > Reset Password. You'll receive an email with a reset link valid for 24 hours."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept Visa, Mastercard, American Express, PayPal, and bank transfers. All transactions are encrypted and secure."
        },
        {
            "question": "How long does shipping take?",
            "answer": "Standard shipping: 5-7 business days. Express shipping: 2-3 business days. International: 10-14 business days."
        }
    ]
    
    # Template for each example
    example_template = PromptTemplate(
        input_variables=["question", "answer"],
        template="Q: {question}\nA: {answer}"
    )
    
    # Create few-shot template
    faq_template = FewShotPromptTemplate(
        examples=faq_examples,
        example_prompt=example_template,
        prefix="""You are a customer service bot. Answer questions based on the pattern below.
Be helpful, specific, and include relevant details.

Examples:""",
        suffix="\nQ: {user_question}\nA:",
        input_variables=["user_question"]
    )
    
    print("\n🎓 Bot trained on example FAQs:")
    for i, ex in enumerate(faq_examples, 1):
        print(f"   {i}. {ex['question'][:50]}...")
    
    # Test questions
    test_questions = [
        "Can I get a refund?",
        "Do you ship internationally?",
        "How do I track my order?"
    ]
    
    for question in test_questions:
        prompt = faq_template.format(user_question=question)
        
        print(f"\n👤 User: {question}")
        print("🤖 Bot:")
        
        response = chat.invoke(prompt)
        print(response.content)
    
    print("\n✅ FAQ Bot learns response patterns from examples!")
    print()


def code_generator():
    """Project 2: Code Generator with Structured Output"""
    
    print("=" * 70)
    print("💻 Project 2: Code Generator")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define output schema
    class CodeOutput(BaseModel):
        language: str = Field(description="Programming language")
        code: str = Field(description="The generated code")
        explanation: str = Field(description="Brief explanation of how it works")
        usage_example: str = Field(description="How to use the code")
    
    parser = JsonOutputParser(pydantic_object=CodeOutput)
    
    template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert programmer. Generate clean, well-documented code.
Always follow best practices and include helpful comments."""),
        ("human", """{request}

{format_instructions}""")
    ])
    
    print("\n🎯 Code Generator - Structured Output")
    
    # Code requests
    requests = [
        "Create a Python function to check if a string is a palindrome",
        "Write a JavaScript function to debounce user input"
    ]
    
    for request in requests:
        prompt = template.format_messages(
            request=request,
            format_instructions=parser.get_format_instructions()
        )
        
        print(f"\n{'='*70}")
        print(f"📝 Request: {request}")
        print(f"{'='*70}")
        
        response = chat.invoke(prompt)
        
        try:
            parsed = parser.parse(response.content)
            
            print(f"\n🔹 Language: {parsed['language']}")
            print(f"\n🔹 Code:\n{parsed['code']}")
            print(f"\n🔹 Explanation:\n{parsed['explanation']}")
            print(f"\n🔹 Usage:\n{parsed['usage_example']}")
            
        except Exception as e:
            print(f"⚠️  Parsing error: {e}")
            print(f"Raw response:\n{response.content}")
    
    print("\n✅ Structured output makes code generation predictable!")
    print()


def data_extraction_system():
    """Project 3: Data Extraction from Unstructured Text"""
    
    print("=" * 70)
    print("📊 Project 3: Data Extraction System")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,  # Low temperature for accuracy
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define extraction schema
    class ExtractedData(BaseModel):
        person_name: str = Field(description="Full name of the person")
        email: str = Field(description="Email address")
        phone: str = Field(description="Phone number if available, else 'N/A'")
        company: str = Field(description="Company name if mentioned, else 'N/A'")
        role: str = Field(description="Job role/title if mentioned, else 'N/A'")
        interests: list[str] = Field(description="List of mentioned interests or topics")
    
    parser = JsonOutputParser(pydantic_object=ExtractedData)
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a data extraction specialist. Extract structured information accurately."),
        ("human", """Extract information from this text:

{text}

{format_instructions}""")
    ])
    
    # Sample texts
    texts = [
        """Hi, I'm Sarah Johnson (sarah.j@techcorp.com). I work as a Senior Data Scientist 
        at TechCorp Inc. You can reach me at +1-555-0123. I'm passionate about machine 
        learning, natural language processing, and building scalable AI systems.""",
        
        """Contact: Mike Chen, email mike.chen@startup.io. Currently leading the engineering 
        team at StartupXYZ. Interested in cloud architecture and DevOps practices."""
    ]
    
    print("\n🎯 Extracting structured data from unstructured text:\n")
    
    for i, text in enumerate(texts, 1):
        print(f"{'='*70}")
        print(f"📄 Text Sample {i}:")
        print(f"{'='*70}")
        print(text[:100] + "...")
        
        prompt = template.format_messages(
            text=text,
            format_instructions=parser.get_format_instructions()
        )
        
        response = chat.invoke(prompt)
        
        try:
            data = parser.parse(response.content)
            
            print("\n✅ Extracted Data:")
            print(f"   Name: {data['person_name']}")
            print(f"   Email: {data['email']}")
            print(f"   Phone: {data['phone']}")
            print(f"   Company: {data['company']}")
            print(f"   Role: {data['role']}")
            print(f"   Interests: {', '.join(data['interests'])}")
            print()
            
        except Exception as e:
            print(f"\n⚠️  Extraction failed: {e}\n")
    
    print("✅ Data extraction turns messy text into clean data!")
    print()


def multi_step_reasoning_bot():
    """Project 4: Multi-Step Reasoning Chatbot"""
    
    print("=" * 70)
    print("🧠 Project 4: Multi-Step Reasoning Bot")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Template for step-by-step reasoning
    template = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that breaks down complex problems.

When answering:
1. Understand: Restate the question
2. Break down: Identify sub-problems
3. Solve: Address each step
4. Conclude: Provide final answer

Always show your reasoning process."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])
    
    print("\n🧠 Reasoning Bot - Breaks down complex problems")
    print("   (Simulated conversation)\n")
    
    # Conversation
    history = []
    
    questions = [
        "I want to learn web development. I have 3 months. Create a study plan.",
        "What if I only have 2 hours per day?",
        "Should I focus on frontend or backend first?"
    ]
    
    for question in questions:
        print(f"👤 You: {question}")
        
        messages = template.format_messages(
            history=history,
            question=question
        )
        
        response = chat.invoke(messages)
        print(f"\n🤖 Bot:\n{response.content}\n")
        print("-" * 70 + "\n")
        
        # Update history
        history.append(HumanMessage(content=question))
        history.append(AIMessage(content=response.content))
    
    print("✅ Multi-step reasoning provides thorough, thoughtful answers!")
    print()


def content_personalizer():
    """Project 5: Content Personalizer"""
    
    print("=" * 70)
    print("🎨 Project 5: Content Personalizer")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.8,  # More creative
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Template with user preferences
    template = PromptTemplate.from_template(
        """Create personalized content based on this user profile:

User Profile:
- Name: {name}
- Age Group: {age_group}
- Interests: {interests}
- Tone Preference: {tone}
- Content Type: {content_type}

Task: {task}

Make it engaging and perfectly suited to this user!"""
    )
    
    print("\n🎨 Personalizing content for different users:\n")
    
    # Different user profiles
    users = [
        {
            "name": "Alex",
            "age_group": "teenager (13-17)",
            "interests": "gaming, technology, anime",
            "tone": "casual and fun",
            "content_type": "social media post",
            "task": "Announce a new Python coding workshop"
        },
        {
            "name": "Dr. Smith",
            "age_group": "professional (40+)",
            "interests": "business, leadership, innovation",
            "tone": "professional and insightful",
            "content_type": "LinkedIn article",
            "task": "Announce a new Python coding workshop"
        }
    ]
    
    for user in users:
        print(f"{'='*70}")
        print(f"👤 User: {user['name']} ({user['age_group']})")
        print(f"{'='*70}")
        
        prompt = template.format(**user)
        
        response = chat.invoke(prompt)
        print(f"\n📝 Personalized Content:\n{response.content}\n")
    
    print("✅ Personalization creates content that resonates!")
    print()


def practical_prompt_patterns():
    """Bonus: Demonstrate common prompt patterns"""
    
    print("=" * 70)
    print("📚 Bonus: Common Prompt Patterns")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    patterns = {
        "Chain of Thought": """Let's solve this step by step:

Problem: {problem}

Think through this carefully, showing each step of your reasoning.""",
        
        "Role Playing": """You are {role}.

Respond to this situation: {situation}

Stay in character and provide authentic advice.""",
        
        "Constrained Output": """Answer this question: {question}

Constraints:
- Maximum {max_words} words
- Use {format} format
- Include {required_element}""",
    }
    
    print("\n📖 Common Prompt Engineering Patterns:\n")
    
    for pattern_name, pattern_template in patterns.items():
        print(f"🔹 {pattern_name}")
        print(f"   Template: {pattern_template[:80]}...")
        print()
    
    # Example: Chain of Thought
    cot_template = PromptTemplate.from_template(patterns["Chain of Thought"])
    prompt = cot_template.format(
        problem="If a train travels 120 km in 2 hours, what's its average speed in meters per second?"
    )
    
    print("🎯 Example: Chain of Thought")
    print(f"📝 Problem: Train speed calculation")
    print("\n🤖 Response:")
    
    response = chat.invoke(prompt)
    print(response.content)
    
    print("\n💡 These patterns work across all AI models!")
    print()


def main():
    """Run all practical examples"""
    
    print("\n" + "🚀" * 35)
    print("Welcome to Practical Examples - Real-World Projects!")
    print("🚀" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        smart_faq_bot()
        input("Press Enter to continue...")
        
        code_generator()
        input("Press Enter to continue...")
        
        data_extraction_system()
        input("Press Enter to continue...")
        
        multi_step_reasoning_bot()
        input("Press Enter to continue...")
        
        content_personalizer()
        input("Press Enter to continue...")
        
        practical_prompt_patterns()
        
        print("=" * 70)
        print("✅ All Practical Examples completed!")
        print("=" * 70)
        print("\n🎉 Congratulations! You've mastered LangChain Prompts!")
        print("\n💡 What You've Learned:")
        print("  ✓ Building intelligent FAQ bots")
        print("  ✓ Generating code with structured output")
        print("  ✓ Extracting data from unstructured text")
        print("  ✓ Multi-step reasoning and problem solving")
        print("  ✓ Personalizing content for different audiences")
        print("  ✓ Common prompt engineering patterns")
        print("\n🚀 You're now ready to:")
        print("  • Build production-ready prompt systems")
        print("  • Design complex conversational flows")
        print("  • Extract and structure information")
        print("  • Create adaptive, context-aware applications")
        print("\n📚 Next Steps:")
        print("  → Explore LangChain Chains (combine prompts + models)")
        print("  → Learn Memory (persistent conversations)")
        print("  → Build Agents (autonomous AI)")
        print("  → Create RAG systems (knowledge retrieval)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
