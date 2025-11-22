"""
🔧 Runnable Interface - Core Fundamentals

Complete exploration of the Runnable protocol:
1. Core Methods - invoke(), batch(), stream() fundamentals
2. Async Execution - ainvoke(), abatch(), astream()
3. Configuration - Runtime config, metadata, tags
4. Input/Output Schemas - Type introspection
5. Method Chaining - Composing runnables
6. Custom Runnable - Building from scratch
7. Runnable Inspection - Debugging and introspection
8. Config Propagation - Passing config through chains

Master the foundation of LangChain!
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableConfig
from langchain_core.pydantic_v1 import BaseModel
from typing import Dict, Any, List, Iterator
import time

# Load environment variables
load_dotenv()


def core_methods_example():
    """Example 1: Core Runnable methods - invoke, batch, stream"""
    
    print("=" * 70)
    print("🔧 Example 1: Core Runnable Methods")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = PromptTemplate.from_template("Write a haiku about {topic}")
    parser = StrOutputParser()
    
    # Create a simple chain
    chain = prompt | chat | parser
    
    print("\n📌 All LangChain components are Runnables!")
    print("   Models, prompts, chains, parsers - same interface")
    
    # Method 1: invoke() - Single input
    print("\n1️⃣ invoke() - Process single input:")
    result = chain.invoke({"topic": "mountains"})
    print(f"   Input: {{'topic': 'mountains'}}")
    print(f"   Output: {result}")
    
    # Method 2: batch() - Multiple inputs
    print("\n2️⃣ batch() - Process multiple inputs efficiently:")
    results = chain.batch([
        {"topic": "ocean"},
        {"topic": "forest"},
        {"topic": "desert"}
    ])
    
    print("   Inputs: ocean, forest, desert")
    for i, result in enumerate(results, 1):
        print(f"   Result {i}: {result[:40]}...")
    
    # Method 3: stream() - Streaming output
    print("\n3️⃣ stream() - Real-time streaming:")
    print("   Streaming haiku about 'sunset': ", end="", flush=True)
    for chunk in chain.stream({"topic": "sunset"}):
        print(chunk, end="", flush=True)
    print()
    
    print("\n💡 Key insight: Same interface (invoke/batch/stream) works")
    print("   for ALL runnables - models, chains, custom functions!")
    print()


def async_execution_example():
    """Example 2: Async execution methods"""
    
    print("=" * 70)
    print("⚡ Example 2: Async Execution")
    print("=" * 70)
    
    async def async_demo():
        chat = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        prompt = PromptTemplate.from_template("Translate to {language}: {text}")
        chain = prompt | chat | StrOutputParser()
        
        print("\n🚀 Async methods for non-blocking I/O")
        
        # 1. ainvoke()
        print("\n1️⃣ ainvoke() - Async single execution:")
        result = await chain.ainvoke({
            "language": "Spanish",
            "text": "Hello, how are you?"
        })
        print(f"   Result: {result}")
        
        # 2. abatch()
        print("\n2️⃣ abatch() - Async batch processing:")
        start = time.time()
        results = await chain.abatch([
            {"language": "French", "text": "Good morning"},
            {"language": "German", "text": "Good night"},
            {"language": "Italian", "text": "Thank you"}
        ])
        duration = time.time() - start
        
        print(f"   Processed 3 translations in {duration:.2f}s")
        for i, result in enumerate(results, 1):
            print(f"   Translation {i}: {result}")
        
        # 3. astream()
        print("\n3️⃣ astream() - Async streaming:")
        print("   Streaming: ", end="", flush=True)
        async for chunk in chain.astream({
            "language": "Japanese",
            "text": "Beautiful day"
        }):
            print(chunk, end="", flush=True)
        print()
        
        print("\n💡 Async is essential for:")
        print("   • FastAPI / async web frameworks")
        print("   • Concurrent request handling")
        print("   • Better performance under load")
    
    # Run async function
    asyncio.run(async_demo())
    print()


def configuration_example():
    """Example 3: Runtime configuration"""
    
    print("=" * 70)
    print("⚙️ Example 3: Runtime Configuration")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = PromptTemplate.from_template("Explain {concept} in one sentence")
    chain = prompt | chat | StrOutputParser()
    
    print("\n📋 Config allows runtime customization and metadata")
    
    # Config with metadata
    config = {
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        },
        "tags": ["explanation", "educational"],
        "run_name": "concept_explainer"
    }
    
    print("\n1️⃣ Invoke with config:")
    print(f"   Config: {config}")
    
    result = chain.invoke(
        {"concept": "quantum computing"},
        config=config
    )
    
    print(f"   Result: {result}")
    
    print("\n💡 Config is useful for:")
    print("   • User tracking and analytics")
    print("   • A/B testing different prompts")
    print("   • Environment-specific behavior")
    print("   • Custom callbacks and monitoring")
    print()


def schema_introspection_example():
    """Example 4: Input/Output schema inspection"""
    
    print("=" * 70)
    print("🔍 Example 4: Schema Introspection")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = PromptTemplate(
        template="Summarize: {text}",
        input_variables=["text"]
    )
    
    chain = prompt | chat | StrOutputParser()
    
    print("\n📊 Every Runnable has input/output schemas")
    
    # Get schemas
    print("\n1️⃣ Input Schema:")
    input_schema = chain.input_schema.schema()
    print(f"   Type: {input_schema.get('type')}")
    print(f"   Properties: {list(input_schema.get('properties', {}).keys())}")
    
    print("\n2️⃣ Output Schema:")
    output_schema = chain.output_schema.schema()
    print(f"   Type: {output_schema.get('type')}")
    
    print("\n3️⃣ Individual component schemas:")
    print(f"   Prompt input: {prompt.input_schema.schema()['type']}")
    print(f"   Model output type: {type(chat.invoke('test')).__name__}")
    print(f"   Parser output: {parser.output_schema.schema()['type']}")
    
    print("\n💡 Schema introspection helps with:")
    print("   • Type validation")
    print("   • API documentation")
    print("   • IDE autocomplete")
    print("   • Runtime type checking")
    print()


def method_chaining_example():
    """Example 5: Method chaining and composition"""
    
    print("=" * 70)
    print("🔗 Example 5: Method Chaining")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🎯 Runnables can be chained in multiple ways")
    
    # Way 1: Pipe operator
    print("\n1️⃣ Pipe operator (recommended):")
    chain1 = (
        PromptTemplate.from_template("Topic: {topic}")
        | chat
        | StrOutputParser()
        | RunnableLambda(lambda x: x.upper())
    )
    
    result1 = chain1.invoke({"topic": "AI"})
    print(f"   Result: {result1[:50]}...")
    
    # Way 2: with_ methods
    print("\n2️⃣ with_ methods for configuration:")
    
    # with_fallbacks
    backup_chain = PromptTemplate.from_template("Simple answer: {topic}") | chat
    chain_with_fallback = chain1.with_fallbacks([backup_chain])
    
    print("   ✓ Added fallback chain")
    
    # with_retry
    chain_with_retry = chain1.with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True
    )
    
    print("   ✓ Added retry logic (3 attempts)")
    
    # with_config
    chain_with_config = chain1.with_config(
        tags=["production"],
        metadata={"version": "1.0"}
    )
    
    print("   ✓ Bound default config")
    
    print("\n💡 Method chaining enables:")
    print("   • Clean, readable code")
    print("   • Composable error handling")
    print("   • Reusable configurations")
    print()


def custom_runnable_example():
    """Example 6: Creating custom Runnables"""
    
    print("=" * 70)
    print("🎨 Example 6: Custom Runnable")
    print("=" * 70)
    
    class TextAnalyzer(Runnable):
        """Custom Runnable that analyzes text"""
        
        def invoke(self, input: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
            """Analyze text and return statistics"""
            text = input.get("text", "")
            
            return {
                "original": text,
                "word_count": len(text.split()),
                "char_count": len(text),
                "uppercase_count": sum(1 for c in text if c.isupper()),
                "sentence_count": text.count('.') + text.count('!') + text.count('?')
            }
        
        def batch(self, inputs: List[Dict[str, Any]], config: RunnableConfig = None) -> List[Dict[str, Any]]:
            """Batch analysis"""
            return [self.invoke(input, config) for input in inputs]
        
        def stream(self, input: Dict[str, Any], config: RunnableConfig = None) -> Iterator[Dict[str, Any]]:
            """Stream analysis results"""
            result = self.invoke(input, config)
            for key, value in result.items():
                yield {key: value}
    
    print("\n🛠️ Custom Runnable: TextAnalyzer")
    
    analyzer = TextAnalyzer()
    
    # Test invoke
    print("\n1️⃣ invoke():")
    result = analyzer.invoke({
        "text": "Hello World! This is a test. How are you?"
    })
    
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Test batch
    print("\n2️⃣ batch():")
    results = analyzer.batch([
        {"text": "Short text."},
        {"text": "A longer piece of text with more words."}
    ])
    
    for i, result in enumerate(results, 1):
        print(f"   Text {i}: {result['word_count']} words")
    
    # Test stream
    print("\n3️⃣ stream():")
    print("   Streaming analysis:")
    for chunk in analyzer.stream({"text": "Custom runnable test!"}):
        print(f"   {chunk}")
    
    # Compose with other runnables
    print("\n4️⃣ Composable with other runnables:")
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Analyze → Generate summary
    combined = (
        analyzer
        | RunnableLambda(lambda x: {
            "analysis": f"Text has {x['word_count']} words and {x['char_count']} characters"
        })
        | PromptTemplate.from_template("Create a title for text with: {analysis}")
        | chat
        | StrOutputParser()
    )
    
    title = combined.invoke({"text": "Artificial intelligence is transforming technology."})
    print(f"   Generated title: {title}")
    
    print("\n💡 Custom Runnables allow:")
    print("   • Domain-specific logic")
    print("   • Reusable components")
    print("   • Full composition support")
    print()


def inspection_debugging_example():
    """Example 7: Runnable inspection and debugging"""
    
    print("=" * 70)
    print("🐛 Example 7: Inspection & Debugging")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Build a chain
    chain = (
        PromptTemplate.from_template("Explain {topic}")
        | chat
        | StrOutputParser()
        | RunnableLambda(lambda x: x.upper())
    )
    
    print("\n🔍 Inspecting chain structure")
    
    # 1. String representation
    print("\n1️⃣ Chain structure:")
    print(f"   {chain}")
    
    # 2. Get steps
    print("\n2️⃣ Pipeline steps:")
    print(f"   Type: {type(chain).__name__}")
    
    # 3. Add debug logging
    print("\n3️⃣ Adding debug logging:")
    
    def debug_log(x):
        print(f"   [DEBUG] Intermediate: {str(x)[:50]}...")
        return x
    
    debug_chain = (
        PromptTemplate.from_template("What is {topic}?")
        | RunnableLambda(debug_log)
        | chat
        | RunnableLambda(debug_log)
        | StrOutputParser()
        | RunnableLambda(debug_log)
    )
    
    print("   Running with debug logging:")
    result = debug_chain.invoke({"topic": "LCEL"})
    
    print("\n💡 Debugging techniques:")
    print("   • Insert RunnableLambda for logging")
    print("   • Inspect input/output schemas")
    print("   • Use callbacks for detailed tracing")
    print("   • Test components individually")
    print()


def config_propagation_example():
    """Example 8: Config propagation through chains"""
    
    print("=" * 70)
    print("📡 Example 8: Config Propagation")
    print("=" * 70)
    
    print("\n🔄 Config automatically propagates through chains")
    
    # Custom runnable that uses config
    class ConfigAwareRunnable(Runnable):
        """Runnable that accesses config"""
        
        def invoke(self, input: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
            # Access config metadata
            metadata = config.get("metadata", {}) if config else {}
            user_id = metadata.get("user_id", "anonymous")
            
            return {
                **input,
                "processed_by": user_id,
                "timestamp": time.time()
            }
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Chain with config-aware component
    chain = (
        ConfigAwareRunnable()
        | RunnableLambda(lambda x: {
            "user": x["processed_by"],
            "text": f"User {x['processed_by']} asks: {x.get('question', '')}"
        })
        | PromptTemplate.from_template("Answer: {text}")
        | chat
        | StrOutputParser()
    )
    
    print("\n1️⃣ Without config:")
    result1 = chain.invoke({"question": "What is AI?"})
    print(f"   User: anonymous")
    print(f"   Result: {result1[:60]}...")
    
    print("\n2️⃣ With config:")
    config = {
        "metadata": {
            "user_id": "alice_123",
            "session": "prod_session"
        }
    }
    
    result2 = chain.invoke({"question": "What is ML?"}, config=config)
    print(f"   User: alice_123")
    print(f"   Result: {result2[:60]}...")
    
    print("\n💡 Config propagation enables:")
    print("   • User-specific behavior")
    print("   • Request tracing")
    print("   • A/B testing")
    print("   • Analytics and monitoring")
    print()


def main():
    """Run all Runnable interface examples"""
    
    print("\n" + "🔧" * 35)
    print("Welcome to Runnable Interface - Core Fundamentals!")
    print("🔧" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        core_methods_example()
        input("Press Enter to continue...")
        
        async_execution_example()
        input("Press Enter to continue...")
        
        configuration_example()
        input("Press Enter to continue...")
        
        schema_introspection_example()
        input("Press Enter to continue...")
        
        method_chaining_example()
        input("Press Enter to continue...")
        
        custom_runnable_example()
        input("Press Enter to continue...")
        
        inspection_debugging_example()
        input("Press Enter to continue...")
        
        config_propagation_example()
        
        print("=" * 70)
        print("✅ Runnable Interface examples completed!")
        print("=" * 70)
        print("\n🎯 Key Takeaways:")
        print("  ✓ invoke/batch/stream - Core execution methods")
        print("  ✓ Async versions for non-blocking I/O")
        print("  ✓ Config for metadata and customization")
        print("  ✓ Schemas for type introspection")
        print("  ✓ Method chaining for composition")
        print("  ✓ Custom runnables for domain logic")
        print("  ✓ Debugging with logging and inspection")
        print("  ✓ Config propagation for context")
        print("\n💡 Next: RunnableSequence for sequential composition!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
