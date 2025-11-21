"""
💬 Chat Model Example - Conversational AI with Gemini

This example shows how Chat Models differ from LLMs.
Chat Models understand context and can have multi-turn conversations!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()


def basic_chat_example():
    """Simple example: Single message to chat model"""
    
    print("=" * 60)
    print("💬 Basic Chat Model Example")
    print("=" * 60)
    
    # Initialize Gemini Chat Model
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Chat models work with messages, not just strings
    messages = [
        HumanMessage(content="Hi! What's the capital of Japan?")
    ]
    
    print("\n👤 You: Hi! What's the capital of Japan?")
    
    response = chat.invoke(messages)
    print(f"🤖 AI: {response.content}\n")


def conversation_with_context():
    """Example: Multi-turn conversation with context"""
    
    print("=" * 60)
    print("🔄 Multi-Turn Conversation (This is where Chat Models shine!)")
    print("=" * 60)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Start a conversation with context
    messages = [
        HumanMessage(content="I'm learning Python. What are the best resources?")
    ]
    
    print("\n👤 You: I'm learning Python. What are the best resources?")
    
    response = chat.invoke(messages)
    print(f"🤖 AI: {response.content}\n")
    
    # Add the AI's response to our conversation history
    messages.append(AIMessage(content=response.content))
    
    # Continue the conversation - notice we don't mention Python again!
    messages.append(
        HumanMessage(content="Which one would you recommend for beginners?")
    )
    
    print("👤 You: Which one would you recommend for beginners?")
    
    response = chat.invoke(messages)
    print(f"🤖 AI: {response.content}\n")
    
    print("✨ Notice: The AI understood 'which one' refers to Python resources!")
    print("   This is the power of Chat Models - they maintain context!\n")


def system_message_example():
    """Example: Using system messages to set behavior"""
    
    print("=" * 60)
    print("🎭 System Messages - Control AI's Personality")
    print("=" * 60)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.9,  # More creative!
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # System message sets the AI's role and behavior
    messages = [
        SystemMessage(content="""You are a friendly coding mentor who loves using emojis 
        and encouraging students. You explain things simply and always end with 
        a motivational statement."""),
        HumanMessage(content="What is a variable in programming?")
    ]
    
    print("\n🎯 System Role: Friendly coding mentor with emojis")
    print("👤 You: What is a variable in programming?")
    
    response = chat.invoke(messages)
    print(f"🤖 AI: {response.content}\n")


def streaming_chat_example():
    """Example: Stream chat responses for better UX"""
    
    print("=" * 60)
    print("🌊 Streaming Chat (Modern & Responsive!)")
    print("=" * 60)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    messages = [
        SystemMessage(content="You are a helpful programming assistant."),
        HumanMessage(content="Explain the difference between == and === in JavaScript briefly.")
    ]
    
    print("\n👤 You: Explain the difference between == and === in JavaScript briefly.")
    print("🤖 AI: ", end="", flush=True)
    
    # Stream the response
    for chunk in chat.stream(messages):
        print(chunk.content, end="", flush=True)
    
    print("\n")


def interactive_chat_session():
    """Example: Build a simple interactive chatbot"""
    
    print("=" * 60)
    print("🎮 Interactive Chat Session")
    print("=" * 60)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Set up the chatbot personality
    conversation_history = [
        SystemMessage(content="""You are TechBuddy, a friendly AI assistant specializing in 
        technology and programming. You're enthusiastic, helpful, and give concise answers. 
        You remember the conversation context.""")
    ]
    
    print("\n🤖 TechBuddy: Hello! I'm TechBuddy, your friendly tech assistant!")
    print("               Ask me anything about technology or programming.")
    print("               (Type 'quit' to exit)\n")
    
    # Predefined conversation for demo (you can make it truly interactive)
    demo_questions = [
        "What is LangChain?",
        "How is it different from using OpenAI API directly?",
        "quit"
    ]
    
    for question in demo_questions:
        print(f"👤 You: {question}")
        
        if question.lower() == 'quit':
            print("🤖 TechBuddy: Goodbye! Happy coding! 🚀\n")
            break
        
        # Add user message to history
        conversation_history.append(HumanMessage(content=question))
        
        # Get AI response
        response = chat.invoke(conversation_history)
        
        # Add AI response to history
        conversation_history.append(AIMessage(content=response.content))
        
        print(f"🤖 TechBuddy: {response.content}\n")
    
    print(f"📊 Conversation had {len(conversation_history)} messages in total!")


def compare_llm_vs_chat():
    """Example: Side-by-side comparison of LLM vs Chat Model"""
    
    print("=" * 60)
    print("⚖️  LLM vs Chat Model Comparison")
    print("=" * 60)
    
    from langchain_google_genai import GoogleGenerativeAI
    
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = "What is your favorite programming language?"
    
    print("\n📝 Same prompt to both models:")
    print(f"   '{prompt}'\n")
    
    print("🤖 LLM Response:")
    llm_response = llm.invoke(prompt)
    print(f"   {llm_response[:200]}...\n")
    
    print("💬 Chat Model Response:")
    chat_response = chat.invoke([HumanMessage(content=prompt)])
    print(f"   {chat_response.content[:200]}...\n")
    
    print("💡 Key Insight:")
    print("   Both work, but Chat Models are more natural for conversations")
    print("   and better at understanding context in multi-turn dialogues!\n")


def main():
    """Run all chat model examples"""
    
    print("\n" + "💬" * 30)
    print("Welcome to LangChain Chat Model Examples with Gemini!")
    print("💬" * 30 + "\n")
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables!")
        print("Make sure you have a .env file with your API key.")
        return
    
    try:
        # Run all examples
        basic_chat_example()
        input("Press Enter to continue...")
        
        conversation_with_context()
        input("Press Enter to continue...")
        
        system_message_example()
        input("Press Enter to continue...")
        
        streaming_chat_example()
        input("Press Enter to continue...")
        
        interactive_chat_session()
        input("Press Enter to continue...")
        
        compare_llm_vs_chat()
        
        print("=" * 60)
        print("✅ All Chat Model examples completed!")
        print("=" * 60)
        print("\n💡 Key Takeaways:")
        print("  ✓ Chat Models maintain conversation context")
        print("  ✓ Use HumanMessage, AIMessage, SystemMessage")
        print("  ✓ SystemMessage sets AI's personality/role")
        print("  ✓ Perfect for building chatbots and assistants")
        print("  ✓ Streaming makes the experience more interactive")
        print("\n📚 Next: Try 03_embeddings_example.py for semantic search!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your GOOGLE_API_KEY is valid!")


if __name__ == "__main__":
    main()
