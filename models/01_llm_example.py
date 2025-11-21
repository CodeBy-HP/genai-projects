"""
🤖 LLM Example - Simple Text Completion with Gemini

This example shows how to use Google's Gemini as an LLM for simple text completions.
LLMs are straightforward: text in → text out!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

def basic_llm_example():
    """Simple example: Ask the LLM to complete a prompt"""
    
    print("=" * 60)
    print("🎯 Basic LLM Example - Text Completion")
    print("=" * 60)
    
    # Initialize the Gemini LLM
    # temperature: 0.7 means creative but not too random (0=focused, 1=very creative)
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Simple text completion
    prompt = "Explain what artificial intelligence is in one sentence:"
    
    print(f"\n📝 Prompt: {prompt}")
    print("\n🤖 Response:")
    
    response = llm.invoke(prompt)
    print(response)
    print()


def creative_writing_example():
    """Example: Using LLM for creative content generation"""
    
    print("=" * 60)
    print("✨ Creative Writing with LLM")
    print("=" * 60)
    
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.9,  # Higher temperature for more creativity!
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = """Write a haiku about learning to code with AI.
    
Haiku format:
- First line: 5 syllables
- Second line: 7 syllables
- Third line: 5 syllables"""
    
    print(f"\n📝 Prompt: {prompt[:50]}...")
    print("\n🤖 Response:")
    
    response = llm.invoke(prompt)
    print(response)
    print()


def batch_processing_example():
    """Example: Process multiple prompts efficiently"""
    
    print("=" * 60)
    print("⚡ Batch Processing Multiple Prompts")
    print("=" * 60)
    
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompts = [
        "What is Python in one sentence?",
        "What is JavaScript in one sentence?",
        "What is LangChain in one sentence?"
    ]
    
    print("\n📝 Processing multiple prompts...\n")
    
    # batch() is efficient for multiple prompts
    responses = llm.batch(prompts)
    
    for i, (prompt, response) in enumerate(zip(prompts, responses), 1):
        print(f"{i}. Q: {prompt}")
        print(f"   A: {response}\n")


def streaming_example():
    """Example: Stream responses as they're generated (better UX!)"""
    
    print("=" * 60)
    print("🌊 Streaming Response (Modern Approach!)")
    print("=" * 60)
    
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = "Write a short motivational quote about learning new technologies."
    
    print(f"\n📝 Prompt: {prompt}")
    print("\n🤖 Streaming Response:")
    print("-" * 60)
    
    # Stream the response token by token
    for chunk in llm.stream(prompt):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 60)
    print()


def main():
    """Run all LLM examples"""
    
    print("\n" + "🚀" * 30)
    print("Welcome to LangChain LLM Examples with Gemini!")
    print("🚀" * 30 + "\n")
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables!")
        print("Make sure you have a .env file with your API key.")
        return
    
    try:
        # Run all examples
        basic_llm_example()
        input("Press Enter to continue to next example...")
        
        creative_writing_example()
        input("Press Enter to continue to next example...")
        
        batch_processing_example()
        input("Press Enter to continue to next example...")
        
        streaming_example()
        
        print("=" * 60)
        print("✅ All LLM examples completed!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  - LLMs are simple: prompt → completion")
        print("  - Temperature controls creativity (0-1)")
        print("  - Use batch() for multiple prompts")
        print("  - Use stream() for better user experience")
        print("\n📚 Next: Try 02_chat_model_example.py for conversations!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your GOOGLE_API_KEY is valid!")


if __name__ == "__main__":
    main()
