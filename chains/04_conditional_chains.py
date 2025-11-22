"""
🔀 Conditional Chains - Dynamic Routing & Branching

This example covers:
- RunnableBranch - Conditional execution paths
- Dynamic routing based on input
- Context-based decisions
- Fallback chains
- Multi-condition branching
- Intent-based routing
- Error fallbacks
- Smart chain selection

Route intelligently based on conditions!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda
from typing import Dict, Any

# Load environment variables
load_dotenv()


def basic_conditional():
    """Example 1: Basic RunnableBranch - Simple if/else"""
    
    print("=" * 70)
    print("🔀 Basic Conditional - RunnableBranch")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define condition functions
    def is_long(x: Dict[str, Any]) -> bool:
        """Check if text is long (>50 chars)"""
        return len(x.get("text", "")) > 50
    
    # Chains for different paths
    summarize_chain = (
        PromptTemplate.from_template("Summarize briefly: {text}")
        | chat
        | StrOutputParser()
    )
    
    expand_chain = (
        PromptTemplate.from_template("Expand this with more details: {text}")
        | chat
        | StrOutputParser()
    )
    
    # Conditional branch
    conditional_chain = RunnableBranch(
        (is_long, summarize_chain),  # If long, summarize
        expand_chain  # Else, expand (default)
    )
    
    # Test with long text
    print("\n1️⃣ Long Text (>50 chars):")
    long_text = "Artificial intelligence is revolutionizing how we interact with technology every day."
    print(f"   Input: {long_text}")
    print(f"   Length: {len(long_text)} chars")
    
    result = conditional_chain.invoke({"text": long_text})
    print(f"   Action: Summarize")
    print(f"   Output: {result[:80]}...")
    
    # Test with short text
    print("\n2️⃣ Short Text (<50 chars):")
    short_text = "AI is cool."
    print(f"   Input: {short_text}")
    print(f"   Length: {len(short_text)} chars")
    
    result = conditional_chain.invoke({"text": short_text})
    print(f"   Action: Expand")
    print(f"   Output: {result[:80]}...")
    
    print("\n💡 RunnableBranch routes to different chains based on conditions!")
    print()


def multi_condition_routing():
    """Example 2: Multiple conditions - Priority-based routing"""
    
    print("=" * 70)
    print("🎯 Multi-Condition Routing")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define multiple conditions
    def is_urgent(x: Dict[str, Any]) -> bool:
        """Check for urgent keywords"""
        text = x.get("text", "").lower()
        urgent_words = ["urgent", "emergency", "critical", "asap", "immediately"]
        return any(word in text for word in urgent_words)
    
    def is_question(x: Dict[str, Any]) -> bool:
        """Check if it's a question"""
        text = x.get("text", "")
        return "?" in text or text.lower().startswith(("what", "how", "why", "when", "where", "who"))
    
    def is_feedback(x: Dict[str, Any]) -> bool:
        """Check if it's feedback"""
        text = x.get("text", "").lower()
        feedback_words = ["love", "hate", "excellent", "terrible", "suggestion", "feedback"]
        return any(word in text for word in feedback_words)
    
    # Different handling chains
    urgent_chain = (
        PromptTemplate.from_template("URGENT - Handle immediately: {text}")
        | chat
        | StrOutputParser()
    )
    
    question_chain = (
        PromptTemplate.from_template("Answer this question thoroughly: {text}")
        | chat
        | StrOutputParser()
    )
    
    feedback_chain = (
        PromptTemplate.from_template("Acknowledge and process feedback: {text}")
        | chat
        | StrOutputParser()
    )
    
    general_chain = (
        PromptTemplate.from_template("Standard response to: {text}")
        | chat
        | StrOutputParser()
    )
    
    # Multi-condition branch (evaluated in order!)
    router = RunnableBranch(
        (is_urgent, urgent_chain),      # Check urgent first
        (is_question, question_chain),   # Then questions
        (is_feedback, feedback_chain),   # Then feedback
        general_chain                    # Default
    )
    
    test_cases = [
        {"text": "URGENT: Server is down!", "expected": "urgent"},
        {"text": "How does AI work?", "expected": "question"},
        {"text": "I love this product!", "expected": "feedback"},
        {"text": "Hello, just checking in.", "expected": "general"}
    ]
    
    print("\n🔄 Routing Test Cases:")
    for i, case in enumerate(test_cases, 1):
        result = router.invoke(case)
        print(f"\n   {i}. Input: {case['text']}")
        print(f"      Expected: {case['expected']}")
        print(f"      Response: {result[:60]}...")
    
    print("\n💡 Conditions evaluated in order - first match wins!")
    print()


def intent_based_routing():
    """Example 3: Intent classification + routing"""
    
    print("=" * 70)
    print("🎯 Intent-Based Routing")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Step 1: Classify intent
    intent_classifier = (
        PromptTemplate.from_template(
            """Classify intent (one word only: support, sales, feedback, general):
            Text: {query}
            Intent:"""
        )
        | chat
        | StrOutputParser()
        | RunnableLambda(lambda x: x.strip().lower())
    )
    
    # Step 2: Different handlers
    support_handler = (
        PromptTemplate.from_template("Support response: {query}")
        | chat
        | StrOutputParser()
    )
    
    sales_handler = (
        PromptTemplate.from_template("Sales response: {query}")
        | chat
        | StrOutputParser()
    )
    
    feedback_handler = (
        PromptTemplate.from_template("Thank customer for feedback: {query}")
        | chat
        | StrOutputParser()
    )
    
    general_handler = (
        PromptTemplate.from_template("General assistance: {query}")
        | chat
        | StrOutputParser()
    )
    
    # Routing based on classified intent
    def route_by_intent(x: Dict[str, Any]) -> Any:
        """Route to appropriate handler based on intent"""
        intent = x.get("intent", "general")
        query = x.get("query", "")
        
        handlers = {
            "support": support_handler,
            "sales": sales_handler,
            "feedback": feedback_handler,
            "general": general_handler
        }
        
        handler = handlers.get(intent, general_handler)
        return handler.invoke({"query": query})
    
    # Complete chain: classify → route → handle
    full_chain = (
        RunnablePassthrough.assign(
            intent=intent_classifier
        )
        | RunnableLambda(route_by_intent)
    )
    
    queries = [
        "I need help with my account login",
        "What's the pricing for enterprise plan?",
        "Your product is amazing!",
        "What are your business hours?"
    ]
    
    print("\n🎯 Intent Classification → Routing:")
    for query in queries:
        print(f"\n   Query: {query}")
        result = full_chain.invoke({"query": query})
        print(f"   Response: {result[:60]}...")
    
    print("\n💡 Two-step: Classify intent → Route to specialist!")
    print()


def fallback_chains():
    """Example 4: Fallback handling with conditional chains"""
    
    print("=" * 70)
    print("🛡️ Fallback Chains - Error Handling")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Primary chain (might fail with complex queries)
    def can_handle_simple(x: Dict[str, Any]) -> bool:
        """Check if query is simple enough"""
        query = x.get("query", "")
        complex_indicators = ["explain quantum", "derive formula", "prove theorem"]
        return not any(indicator in query.lower() for indicator in complex_indicators)
    
    simple_chain = (
        PromptTemplate.from_template("Quick answer: {query}")
        | chat
        | StrOutputParser()
    )
    
    expert_chain = (
        PromptTemplate.from_template(
            """Detailed expert explanation:
            Question: {query}
            
            Provide comprehensive answer with examples."""
        )
        | chat
        | StrOutputParser()
    )
    
    fallback_chain = (
        PromptTemplate.from_template(
            "I'll connect you with an expert for: {query}"
        )
        | chat
        | StrOutputParser()
    )
    
    # Route with fallback
    smart_router = RunnableBranch(
        (can_handle_simple, simple_chain),
        expert_chain  # Default to expert for complex
    )
    
    # Add ultimate fallback using with_fallbacks
    safe_chain = smart_router.with_fallbacks(
        fallbacks=[fallback_chain]
    )
    
    test_queries = [
        "What's 2+2?",
        "Explain quantum entanglement",
        "What's the capital of France?"
    ]
    
    print("\n🛡️ Smart Routing with Fallbacks:")
    for query in test_queries:
        print(f"\n   Query: {query}")
        result = safe_chain.invoke({"query": query})
        print(f"   Response: {result[:60]}...")
    
    print("\n💡 Use with_fallbacks() for robust error handling!")
    print()


def context_based_branching():
    """Example 5: Branch based on accumulated context"""
    
    print("=" * 70)
    print("📦 Context-Based Branching")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Enrichment chain
    def add_metadata(x: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata about the text"""
        text = x.get("text", "")
        return {
            **x,
            "word_count": len(text.split()),
            "has_code": "```" in text or "def " in text or "function" in text,
            "has_data": any(word in text.lower() for word in ["table", "csv", "data", "numbers"])
        }
    
    # Different processors based on content type
    def is_code_heavy(x: Dict[str, Any]) -> bool:
        return x.get("has_code", False)
    
    def is_data_heavy(x: Dict[str, Any]) -> bool:
        return x.get("has_data", False)
    
    code_processor = (
        PromptTemplate.from_template("Explain this code: {text}")
        | chat
        | StrOutputParser()
    )
    
    data_processor = (
        PromptTemplate.from_template("Analyze this data: {text}")
        | chat
        | StrOutputParser()
    )
    
    text_processor = (
        PromptTemplate.from_template("Summarize: {text}")
        | chat
        | StrOutputParser()
    )
    
    # Context-aware routing
    chain = (
        RunnableLambda(add_metadata)
        | RunnableBranch(
            (is_code_heavy, code_processor),
            (is_data_heavy, data_processor),
            text_processor
        )
    )
    
    test_cases = [
        {"text": "Here's a function: def hello(): print('Hi')", "type": "code"},
        {"text": "Sales data shows revenue increased by 20%", "type": "data"},
        {"text": "The quick brown fox jumps over the lazy dog", "type": "text"}
    ]
    
    print("\n📦 Context-Based Routing:")
    for case in test_cases:
        print(f"\n   Type: {case['type']}")
        print(f"   Input: {case['text'][:50]}...")
        result = chain.invoke(case)
        print(f"   Output: {result[:60]}...")
    
    print("\n💡 Enrich context first, then route based on metadata!")
    print()


def dynamic_chain_selection():
    """Example 6: Select chain dynamically at runtime"""
    
    print("=" * 70)
    print("⚙️ Dynamic Chain Selection")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define chain library
    chains = {
        "creative": PromptTemplate.from_template(
            "Write creatively about: {topic}"
        ) | chat | StrOutputParser(),
        
        "technical": PromptTemplate.from_template(
            "Explain technically: {topic}"
        ) | chat | StrOutputParser(),
        
        "simple": PromptTemplate.from_template(
            "Explain simply to a 5-year-old: {topic}"
        ) | chat | StrOutputParser(),
        
        "academic": PromptTemplate.from_template(
            "Academic analysis of: {topic}"
        ) | chat | StrOutputParser()
    }
    
    def select_chain(x: Dict[str, Any]) -> Any:
        """Select chain based on style parameter"""
        style = x.get("style", "simple")
        topic = x.get("topic", "")
        
        selected_chain = chains.get(style, chains["simple"])
        return selected_chain.invoke({"topic": topic})
    
    dynamic_chain = RunnableLambda(select_chain)
    
    topic = "artificial intelligence"
    styles = ["creative", "technical", "simple", "academic"]
    
    print(f"\n📚 Topic: {topic}")
    print("\n⚙️ Different Styles:")
    
    for style in styles:
        result = dynamic_chain.invoke({"topic": topic, "style": style})
        print(f"\n   {style.upper()}:")
        print(f"   {result[:70]}...")
    
    print("\n💡 Store chains in dict, select dynamically!")
    print()


def multi_stage_conditional():
    """Example 7: Multiple conditional stages"""
    
    print("=" * 70)
    print("🔄 Multi-Stage Conditional Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Stage 1: Language detection
    def detect_language(x: Dict[str, Any]) -> Dict[str, Any]:
        text = x.get("text", "")
        if any(word in text.lower() for word in ["código", "función", "clase"]):
            return {**x, "language": "spanish"}
        elif any(word in text.lower() for word in ["code", "function", "class"]):
            return {**x, "language": "english"}
        return {**x, "language": "unknown"}
    
    # Stage 2: Content type detection
    def detect_type(x: Dict[str, Any]) -> Dict[str, Any]:
        text = x.get("text", "")
        if "def " in text or "function" in text:
            return {**x, "content_type": "code"}
        elif "?" in text:
            return {**x, "content_type": "question"}
        return {**x, "content_type": "statement"}
    
    # Conditional processors
    def needs_translation(x: Dict[str, Any]) -> bool:
        return x.get("language") == "spanish"
    
    def is_code_question(x: Dict[str, Any]) -> bool:
        return x.get("content_type") == "code"
    
    translate_chain = (
        PromptTemplate.from_template("Translate to English: {text}")
        | chat
        | StrOutputParser()
    )
    
    code_explain_chain = (
        PromptTemplate.from_template("Explain this code: {text}")
        | chat
        | StrOutputParser()
    )
    
    answer_chain = (
        PromptTemplate.from_template("Answer: {text}")
        | chat
        | StrOutputParser()
    )
    
    # Multi-stage pipeline
    pipeline = (
        # Stage 1: Detect language
        RunnableLambda(detect_language)
        
        # Stage 2: Detect content type
        | RunnableLambda(detect_type)
        
        # Stage 3: Translate if needed
        | RunnableBranch(
            (needs_translation, 
             RunnablePassthrough.assign(translated=translate_chain)),
            RunnablePassthrough()
        )
        
        # Stage 4: Process based on type
        | RunnableBranch(
            (is_code_question, code_explain_chain),
            answer_chain
        )
    )
    
    test_cases = [
        {"text": "def factorial(n): return 1 if n == 0 else n * factorial(n-1)"},
        {"text": "¿Cómo funciona este código?"},
        {"text": "What is machine learning?"}
    ]
    
    print("\n🔄 Multi-Stage Processing:")
    for i, case in enumerate(test_cases, 1):
        print(f"\n   {i}. Input: {case['text'][:50]}...")
        result = pipeline.invoke(case)
        print(f"      Output: {result[:60]}...")
    
    print("\n💡 Chain multiple conditional stages for complex routing!")
    print()


def conditional_with_metadata():
    """Example 8: Preserve routing decisions as metadata"""
    
    print("=" * 70)
    print("📊 Conditional Routing with Metadata")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Classification
    def classify_urgency(x: Dict[str, Any]) -> str:
        text = x.get("text", "").lower()
        if any(word in text for word in ["urgent", "critical", "emergency"]):
            return "high"
        elif any(word in text for word in ["soon", "quickly", "asap"]):
            return "medium"
        return "low"
    
    # Add classification to context
    enriched_chain = (
        RunnablePassthrough.assign(
            urgency=RunnableLambda(classify_urgency)
        )
    )
    
    # Conditional processing
    def is_high_priority(x: Dict[str, Any]) -> bool:
        return x.get("urgency") == "high"
    
    def is_medium_priority(x: Dict[str, Any]) -> bool:
        return x.get("urgency") == "medium"
    
    high_priority_chain = (
        PromptTemplate.from_template("URGENT RESPONSE: {text}")
        | chat
        | StrOutputParser()
    )
    
    medium_priority_chain = (
        PromptTemplate.from_template("Prompt response: {text}")
        | chat
        | StrOutputParser()
    )
    
    standard_chain = (
        PromptTemplate.from_template("Standard response: {text}")
        | chat
        | StrOutputParser()
    )
    
    # Full chain with metadata preservation
    full_chain = (
        enriched_chain
        | RunnablePassthrough.assign(
            response=RunnableBranch(
                (is_high_priority, high_priority_chain),
                (is_medium_priority, medium_priority_chain),
                standard_chain
            )
        )
    )
    
    test_cases = [
        "URGENT: System is down!",
        "Please respond soon about the meeting",
        "Just wanted to say hello"
    ]
    
    print("\n📊 Routing with Metadata:")
    for text in test_cases:
        result = full_chain.invoke({"text": text})
        print(f"\n   Input: {text}")
        print(f"   Urgency: {result['urgency']}")
        print(f"   Response: {result['response'][:50]}...")
    
    print("\n💡 Preserve routing metadata for analytics and debugging!")
    print()


def main():
    """Run all conditional chain examples"""
    
    print("\n" + "🔀" * 35)
    print("Welcome to Conditional Chains - Dynamic Routing!")
    print("🔀" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        basic_conditional()
        input("Press Enter to continue...")
        
        multi_condition_routing()
        input("Press Enter to continue...")
        
        intent_based_routing()
        input("Press Enter to continue...")
        
        fallback_chains()
        input("Press Enter to continue...")
        
        context_based_branching()
        input("Press Enter to continue...")
        
        dynamic_chain_selection()
        input("Press Enter to continue...")
        
        multi_stage_conditional()
        input("Press Enter to continue...")
        
        conditional_with_metadata()
        
        print("=" * 70)
        print("✅ All Conditional Chain examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ RunnableBranch for conditional routing")
        print("  ✓ Conditions evaluated in order (first match)")
        print("  ✓ Two-step: Classify → Route")
        print("  ✓ with_fallbacks() for error handling")
        print("  ✓ Enrich context before routing")
        print("  ✓ Dynamic chain selection from dict")
        print("  ✓ Multi-stage conditional pipelines")
        print("  ✓ Preserve routing metadata")
        print("\n📚 Next: Try 05_practical_chains.py for real-world projects!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
