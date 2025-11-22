"""
💬 Chat Prompts - Conversational Prompt Engineering

This example covers:
- ChatPromptTemplate basics
- System, Human, AI messages
- MessagesPlaceholder for history
- Conversation memory handling
- Multi-turn dialogues

Perfect for building chatbots and conversational AI!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()


def chat_prompt_template_basics():
    """Example 1: ChatPromptTemplate fundamentals"""
    
    print("=" * 70)
    print("💬 ChatPromptTemplate Basics")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create a chat prompt template
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant named {assistant_name}."),
        ("human", "{user_input}")
    ])
    
    print("\n📋 Chat Template Structure:")
    print("   1. System message (sets behavior)")
    print("   2. Human message (user input)")
    
    # Format and use the template
    messages = template.format_messages(
        assistant_name="TechBot",
        user_input="What is Python?"
    )
    
    print(f"\n📝 Formatted Messages:")
    for msg in messages:
        print(f"   {msg.__class__.__name__}: {msg.content}")
    
    print("\n🤖 Response:")
    response = chat.invoke(messages)
    print(response.content)
    
    print("\n💡 ChatPromptTemplate creates structured conversations!")
    print()


def system_message_personality():
    """Example 2: Using system messages to set personality"""
    
    print("=" * 70)
    print("🎭 System Messages - Control AI Personality")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.9,  # More creative!
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Different personalities
    personalities = [
        {
            "name": "Formal Professor",
            "system": "You are a formal academic professor. Use sophisticated language and cite sources."
        },
        {
            "name": "Friendly Tutor",
            "system": "You are a friendly, encouraging tutor. Use simple language, emojis, and be supportive!"
        },
        {
            "name": "Pirate Captain",
            "system": "You are a pirate captain who knows programming! Speak like a pirate while teaching code. Arrr!"
        }
    ]
    
    question = "What is a variable in programming?"
    
    for personality in personalities:
        template = ChatPromptTemplate.from_messages([
            ("system", personality["system"]),
            ("human", "{question}")
        ])
        
        messages = template.format_messages(question=question)
        
        print(f"\n🎭 {personality['name']}:")
        print(f"   System: {personality['system'][:60]}...")
        print(f"\n🤖 Response:")
        
        response = chat.invoke(messages)
        print(response.content[:250] + "...")
        print()
    
    print("💡 System messages dramatically change AI behavior!")
    print()


def multi_turn_conversation():
    """Example 3: Multi-turn conversations with context"""
    
    print("=" * 70)
    print("🔄 Multi-Turn Conversations")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Template with system message
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful programming tutor. Remember the conversation context."),
        ("human", "{message}")
    ])
    
    # Simulated conversation
    conversation = [
        "I want to learn web development. Where should I start?",
        "Should I learn HTML first or JavaScript?",
        "How long does it typically take to learn it?"  # "it" refers to HTML from context
    ]
    
    # Store conversation history
    history = []
    
    for user_message in conversation:
        print(f"\n👤 User: {user_message}")
        
        # Create messages with full history
        messages = [
            SystemMessage(content="You are a helpful programming tutor. Remember the conversation context.")
        ]
        
        # Add history
        messages.extend(history)
        
        # Add new user message
        messages.append(HumanMessage(content=user_message))
        
        # Get response
        response = chat.invoke(messages)
        print(f"🤖 AI: {response.content}\n")
        
        # Save to history
        history.append(HumanMessage(content=user_message))
        history.append(AIMessage(content=response.content))
    
    print("💡 The AI remembers context! Notice how 'it' in the last")
    print("   question correctly refers to HTML from earlier.")
    print()


def messages_placeholder_example():
    """Example 4: MessagesPlaceholder for dynamic history"""
    
    print("=" * 70)
    print("🗨️  MessagesPlaceholder - Dynamic History Injection")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Template with placeholder for chat history
    template = ChatPromptTemplate.from_messages([
        ("system", "You are {bot_name}, a {bot_role}."),
        MessagesPlaceholder(variable_name="chat_history"),  # Dynamic history!
        ("human", "{user_input}")
    ])
    
    print("\n📋 Template with MessagesPlaceholder:")
    print("   The 'chat_history' can be any number of messages!")
    
    # Initial conversation
    history = []
    
    # Turn 1
    messages = template.format_messages(
        bot_name="CodeHelper",
        bot_role="Python programming assistant",
        chat_history=history,
        user_input="What's a for loop?"
    )
    
    print("\n👤 Turn 1: What's a for loop?")
    response = chat.invoke(messages)
    print(f"🤖 {response.content[:200]}...")
    
    # Add to history
    history.append(HumanMessage(content="What's a for loop?"))
    history.append(AIMessage(content=response.content))
    
    # Turn 2 - reference previous context
    messages = template.format_messages(
        bot_name="CodeHelper",
        bot_role="Python programming assistant",
        chat_history=history,
        user_input="Can you show me an example?"
    )
    
    print("\n👤 Turn 2: Can you show me an example?")
    response = chat.invoke(messages)
    print(f"🤖 {response.content[:200]}...")
    
    print(f"\n💡 MessagesPlaceholder injected {len(history)} messages of history!")
    print("   This is how production chatbots maintain context!")
    print()


def conversation_with_context_window():
    """Example 5: Managing conversation history (context window)"""
    
    print("=" * 70)
    print("📊 Managing Context Window - Keep Relevant History")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Full conversation history
    full_history = [
        HumanMessage(content="My name is Alice"),
        AIMessage(content="Nice to meet you, Alice!"),
        HumanMessage(content="I like Python programming"),
        AIMessage(content="Python is a great language!"),
        HumanMessage(content="What's the weather like?"),
        AIMessage(content="I don't have access to weather data."),
    ]
    
    print(f"\n📚 Full History: {len(full_history)} messages")
    for i, msg in enumerate(full_history):
        msg_type = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"   {msg_type} {msg.content[:50]}")
    
    # Keep only last 4 messages (most recent context)
    recent_history = full_history[-4:]
    
    print(f"\n✂️  Keeping only last {len(recent_history)} messages (to save tokens)")
    
    # New question
    messages = template.format_messages(
        history=recent_history,
        input="What's my name?"
    )
    
    print("\n👤 User: What's my name?")
    print("🤖 Response:")
    
    response = chat.invoke(messages)
    print(response.content)
    
    print("\n💡 Context window management:")
    print("   ✓ Keeps recent context relevant")
    print("   ✓ Prevents token limit issues")
    print("   ✓ Reduces API costs")
    print("   ⚠️  May lose older context (like the name 'Alice')")
    print()


def structured_chat_template():
    """Example 6: Structured chat templates with roles"""
    
    print("=" * 70)
    print("🏗️  Structured Chat Templates")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Detailed structured template
    template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """You are {assistant_name}, an AI assistant specialized in {specialty}.
            
Your personality traits:
- {trait_1}
- {trait_2}
- {trait_3}

Always follow these rules:
{rules}"""
        ),
        MessagesPlaceholder(variable_name="conversation_history", optional=True),
        HumanMessagePromptTemplate.from_template("{user_question}")
    ])
    
    print("\n📋 Highly Structured Template:")
    print("   - Named assistant with specialty")
    print("   - Personality traits")
    print("   - Rules to follow")
    print("   - Optional conversation history")
    print("   - User question")
    
    # Configure the assistant
    messages = template.format_messages(
        assistant_name="DataBot",
        specialty="data science and machine learning",
        trait_1="Patient and thorough",
        trait_2="Uses real-world examples",
        trait_3="Explains complex concepts simply",
        rules="1. Always explain technical terms\n2. Provide code examples when relevant\n3. Keep answers under 200 words",
        conversation_history=[],  # Empty for first message
        user_question="What is overfitting in machine learning?"
    )
    
    print("\n👤 User: What is overfitting in machine learning?")
    print("🤖 Response:")
    
    response = chat.invoke(messages)
    print(response.content)
    
    print("\n💡 Structured templates ensure consistent AI behavior!")
    print()


def chatbot_with_memory():
    """Example 7: Complete chatbot with conversation memory"""
    
    print("=" * 70)
    print("🤖 Complete Chatbot with Memory")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define chatbot template
    template = ChatPromptTemplate.from_messages([
        ("system", """You are TravelBot, a friendly travel advisor.
        
You help users plan trips by:
- Suggesting destinations
- Providing travel tips
- Recommending activities
- Remembering their preferences

Be enthusiastic and helpful!"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_message}")
    ])
    
    print("\n🤖 TravelBot: Hello! I'm TravelBot, your travel advisor!")
    print("              Ask me about travel destinations!")
    print("              (Simulated conversation below)\n")
    
    # Conversation history
    history = []
    
    # Simulated conversation
    user_messages = [
        "I want to plan a vacation. I love beaches and warm weather.",
        "That sounds great! What activities are there?",
        "Perfect! What should I pack?",
        "Thanks! By the way, what was my preference again?"  # Tests memory
    ]
    
    for user_msg in user_messages:
        print(f"👤 You: {user_msg}")
        
        # Format with history
        messages = template.format_messages(
            chat_history=history,
            user_message=user_msg
        )
        
        # Get response
        response = chat.invoke(messages)
        print(f"🤖 TravelBot: {response.content}\n")
        
        # Update history
        history.append(HumanMessage(content=user_msg))
        history.append(AIMessage(content=response.content))
    
    print(f"📊 Conversation Summary:")
    print(f"   Total messages: {len(history)}")
    print(f"   User messages: {len([m for m in history if isinstance(m, HumanMessage)])}")
    print(f"   Bot messages: {len([m for m in history if isinstance(m, AIMessage)])}")
    
    print("\n💡 The bot remembered preferences throughout the conversation!")
    print()


def main():
    """Run all chat prompt examples"""
    
    print("\n" + "💬" * 35)
    print("Welcome to Chat Prompts - Conversational AI!")
    print("💬" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        chat_prompt_template_basics()
        input("Press Enter to continue...")
        
        system_message_personality()
        input("Press Enter to continue...")
        
        multi_turn_conversation()
        input("Press Enter to continue...")
        
        messages_placeholder_example()
        input("Press Enter to continue...")
        
        conversation_with_context_window()
        input("Press Enter to continue...")
        
        structured_chat_template()
        input("Press Enter to continue...")
        
        chatbot_with_memory()
        
        print("=" * 70)
        print("✅ All Chat Prompt examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ ChatPromptTemplate structures conversations")
        print("  ✓ System messages control personality")
        print("  ✓ MessagesPlaceholder handles dynamic history")
        print("  ✓ Context window management prevents token overflow")
        print("  ✓ Structured templates ensure consistency")
        print("  ✓ Chat history enables multi-turn conversations")
        print("\n📚 Next: Try 03_advanced_prompts.py for advanced techniques!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
