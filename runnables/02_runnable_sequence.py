"""
🔗 RunnableSequence - Sequential Composition

Deep dive into sequential pipelines:
1. Pipe Operator Basics - Creating sequences with |
2. Manual RunnableSequence - Explicit creation
3. Automatic Coercion - Strings, dicts, functions
4. Streaming Behavior - How streams flow through
5. Error Propagation - Handling failures in sequences
6. Nested Sequences - Complex hierarchical chains
7. Intermediate Access - Getting step-by-step results
8. Performance Optimization - Efficient sequencing

Master sequential composition!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnableSequence,
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel
)
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any, List
import time

# Load environment variables
load_dotenv()


def pipe_operator_basics():
    """Example 1: Pipe operator fundamentals"""
    
    print("=" * 70)
    print("🔗 Example 1: Pipe Operator Basics")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n📌 The pipe operator (|) creates RunnableSequence")
    
    # Method 1: Simple pipe
    print("\n1️⃣ Simple pipe:")
    prompt = PromptTemplate.from_template("Write a tagline for {product}")
    parser = StrOutputParser()
    
    chain1 = prompt | chat | parser
    
    print(f"   Type: {type(chain1).__name__}")
    print(f"   Steps: prompt → model → parser")
    
    result = chain1.invoke({"product": "eco-friendly water bottle"})
    print(f"   Result: {result}")
    
    # Method 2: Multi-step pipe
    print("\n2️⃣ Multi-step pipe:")
    
    def add_emoji(text: str) -> str:
        return f"✨ {text} ✨"
    
    chain2 = (
        prompt
        | chat
        | parser
        | RunnableLambda(add_emoji)
        | RunnableLambda(lambda x: x.upper())
    )
    
    result = chain2.invoke({"product": "smart watch"})
    print(f"   Result: {result}")
    
    # Method 3: Branching and merging
    print("\n3️⃣ Pipe with passthrough:")
    
    chain3 = (
        RunnablePassthrough.assign(
            tagline=prompt | chat | parser
        )
        | RunnableLambda(lambda x: f"Product: {x['product']}\nTagline: {x['tagline']}")
    )
    
    result = chain3.invoke({"product": "solar charger"})
    print(f"   Result:\n{result}")
    
    print("\n💡 Pipe operator is:")
    print("   • Clean and readable")
    print("   • Type-safe composition")
    print("   • Automatically optimized")
    print()


def manual_sequence_creation():
    """Example 2: Manually creating RunnableSequence"""
    
    print("=" * 70)
    print("🏗️ Example 2: Manual RunnableSequence")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🛠️ Creating RunnableSequence explicitly")
    
    # Components
    prompt = PromptTemplate.from_template("Summarize: {text}")
    parser = StrOutputParser()
    
    # Method 1: Using pipe (recommended)
    chain_pipe = prompt | chat | parser
    
    # Method 2: Explicit RunnableSequence
    chain_explicit = RunnableSequence(
        first=prompt,
        middle=[chat],
        last=parser
    )
    
    print("\n1️⃣ Pipe operator (recommended):")
    result1 = chain_pipe.invoke({"text": "AI is transforming industries"})
    print(f"   Result: {result1}")
    
    print("\n2️⃣ Explicit RunnableSequence:")
    result2 = chain_explicit.invoke({"text": "AI is transforming industries"})
    print(f"   Result: {result2}")
    
    print("\n3️⃣ Both are equivalent:")
    print(f"   Pipe type: {type(chain_pipe).__name__}")
    print(f"   Explicit type: {type(chain_explicit).__name__}")
    
    print("\n💡 Use pipe operator:")
    print("   • More readable")
    print("   • Less verbose")
    print("   • Industry standard")
    print()


def automatic_coercion():
    """Example 3: Automatic type coercion"""
    
    print("=" * 70)
    print("🎨 Example 3: Automatic Coercion")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n✨ LangChain automatically converts common types")
    
    # Coercion 1: String → PromptTemplate
    print("\n1️⃣ String → PromptTemplate:")
    
    chain1 = "Tell me about {topic}" | chat | StrOutputParser()
    
    result = chain1.invoke({"topic": "quantum physics"})
    print(f"   String automatically becomes PromptTemplate")
    print(f"   Result: {result[:60]}...")
    
    # Coercion 2: Dict → RunnableParallel
    print("\n2️⃣ Dict → RunnableParallel:")
    
    analysis = {
        "length": RunnableLambda(lambda x: len(x["text"])),
        "words": RunnableLambda(lambda x: len(x["text"].split())),
        "uppercase": RunnableLambda(lambda x: sum(1 for c in x["text"] if c.isupper()))
    }
    
    chain2 = analysis | RunnableLambda(lambda x: f"Stats: {x}")
    
    result = chain2.invoke({"text": "Hello World! This is AI."})
    print(f"   Dict automatically becomes RunnableParallel")
    print(f"   Result: {result}")
    
    # Coercion 3: Function → RunnableLambda
    print("\n3️⃣ Function → RunnableLambda:")
    
    def process(x: str) -> str:
        return x.upper()
    
    # Function automatically wrapped
    chain3 = "Say hello" | chat | StrOutputParser() | process
    
    result = chain3.invoke({})
    print(f"   Function automatically becomes RunnableLambda")
    print(f"   Result: {result}")
    
    print("\n💡 Automatic coercion makes code:")
    print("   • More concise")
    print("   • Less boilerplate")
    print("   • Easier to read")
    print()


def streaming_behavior():
    """Example 4: Streaming through sequences"""
    
    print("=" * 70)
    print("🌊 Example 4: Streaming Behavior")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n📡 Streams flow through the entire sequence")
    
    # Create streaming chain
    chain = (
        PromptTemplate.from_template("Write a short story about {topic}")
        | chat
        | StrOutputParser()
    )
    
    print("\n1️⃣ Non-streaming (invoke):")
    start = time.time()
    result = chain.invoke({"topic": "a robot"})
    duration = time.time() - start
    
    print(f"   Time: {duration:.2f}s")
    print(f"   Result: {result[:60]}...")
    
    print("\n2️⃣ Streaming (stream):")
    print("   Output: ", end="", flush=True)
    
    start = time.time()
    chunk_count = 0
    for chunk in chain.stream({"topic": "a robot"}):
        print(chunk, end="", flush=True)
        chunk_count += 1
    
    duration = time.time() - start
    print(f"\n   Time: {duration:.2f}s")
    print(f"   Chunks: {chunk_count}")
    
    # Streaming with transformation
    print("\n3️⃣ Streaming with transformations:")
    
    def add_prefix(text: str) -> str:
        return f"[STORY] {text}"
    
    chain_with_transform = chain | add_prefix
    
    print("   Output: ", end="", flush=True)
    for chunk in chain_with_transform.stream({"topic": "a dragon"}):
        print(chunk, end="", flush=True)
    print()
    
    print("\n💡 Streaming benefits:")
    print("   • Better UX (show progress)")
    print("   • Lower perceived latency")
    print("   • Handles long outputs")
    print()


def error_propagation():
    """Example 5: Error handling in sequences"""
    
    print("=" * 70)
    print("❌ Example 5: Error Propagation")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🚨 Errors propagate through sequences")
    
    # Chain with potential failure
    def validate_input(x: Dict[str, Any]) -> Dict[str, Any]:
        if "text" not in x:
            raise ValueError("Missing 'text' field")
        if len(x["text"]) < 5:
            raise ValueError("Text too short (minimum 5 characters)")
        return x
    
    def safe_uppercase(x: str) -> str:
        if not isinstance(x, str):
            raise TypeError(f"Expected string, got {type(x)}")
        return x.upper()
    
    chain = (
        RunnableLambda(validate_input)
        | PromptTemplate.from_template("Summarize: {text}")
        | chat
        | StrOutputParser()
        | RunnableLambda(safe_uppercase)
    )
    
    # Test 1: Valid input
    print("\n1️⃣ Valid input:")
    try:
        result = chain.invoke({"text": "Artificial intelligence is amazing"})
        print(f"   ✓ Success: {result[:40]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Missing field
    print("\n2️⃣ Missing field:")
    try:
        result = chain.invoke({"wrong_key": "value"})
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ✗ Error caught: {e}")
    
    # Test 3: Too short
    print("\n3️⃣ Text too short:")
    try:
        result = chain.invoke({"text": "AI"})
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ✗ Error caught: {e}")
    
    # Using with_fallbacks for safety
    print("\n4️⃣ With fallback protection:")
    
    fallback_chain = (
        RunnableLambda(lambda x: {"text": "Default text for processing"})
        | PromptTemplate.from_template("Summarize: {text}")
        | chat
        | StrOutputParser()
    )
    
    safe_chain = chain.with_fallbacks([fallback_chain])
    
    try:
        result = safe_chain.invoke({"wrong_key": "value"})
        print(f"   ✓ Fallback used: {result[:40]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n💡 Error handling strategies:")
    print("   • Validate early in the sequence")
    print("   • Use with_fallbacks() for robustness")
    print("   • Use with_retry() for transient errors")
    print()


def nested_sequences():
    """Example 6: Nested RunnableSequences"""
    
    print("=" * 70)
    print("🏗️ Example 6: Nested Sequences")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🔄 Sequences can be nested arbitrarily deep")
    
    # Sub-chain 1: Preprocessing
    preprocess = (
        RunnableLambda(lambda x: x["text"].strip().lower())
        | RunnableLambda(lambda x: {"processed": x})
    )
    
    # Sub-chain 2: Analysis
    analyze = (
        PromptTemplate.from_template("Analyze tone: {processed}")
        | chat
        | StrOutputParser()
        | RunnableLambda(lambda x: {"tone": x})
    )
    
    # Sub-chain 3: Generation
    generate = (
        PromptTemplate.from_template("Write response with {tone} tone")
        | chat
        | StrOutputParser()
    )
    
    # Combine into master chain
    print("\n1️⃣ Building nested chain:")
    print("   Preprocess → Analyze → Generate")
    
    master_chain = (
        preprocess
        | analyze
        | generate
    )
    
    result = master_chain.invoke({"text": "  HELLO WORLD!  "})
    print(f"   Result: {result}")
    
    # Even more nesting
    print("\n2️⃣ Deeply nested chain:")
    
    step1 = RunnableLambda(lambda x: f"Step1: {x}")
    step2 = RunnableLambda(lambda x: f"Step2: {x}")
    step3 = RunnableLambda(lambda x: f"Step3: {x}")
    
    sub_chain_a = step1 | step2
    sub_chain_b = step3 | RunnableLambda(lambda x: f"Final: {x}")
    
    deep_chain = sub_chain_a | sub_chain_b
    
    result = deep_chain.invoke("input")
    print(f"   Result: {result}")
    
    print("\n💡 Nested sequences enable:")
    print("   • Modular design")
    print("   • Reusable sub-chains")
    print("   • Clear separation of concerns")
    print()


def intermediate_access():
    """Example 7: Accessing intermediate results"""
    
    print("=" * 70)
    print("🔍 Example 7: Intermediate Access")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n📊 Capture results from each step")
    
    # Method 1: Using RunnablePassthrough.assign()
    print("\n1️⃣ Using assign() to preserve intermediate steps:")
    
    chain1 = (
        RunnablePassthrough.assign(
            step1=RunnableLambda(lambda x: f"Processed: {x['input']}")
        )
        | RunnablePassthrough.assign(
            step2=PromptTemplate.from_template("Analyze: {step1}") | chat | StrOutputParser()
        )
        | RunnablePassthrough.assign(
            step3=RunnableLambda(lambda x: f"Final: {x['step2'][:20]}")
        )
    )
    
    result = chain1.invoke({"input": "machine learning"})
    
    print(f"   Original: {result['input']}")
    print(f"   Step 1: {result['step1']}")
    print(f"   Step 2: {result['step2'][:50]}...")
    print(f"   Step 3: {result['step3']}")
    
    # Method 2: Manual logging
    print("\n2️⃣ Manual logging at each step:")
    
    def log_and_pass(label: str):
        def _log(x):
            print(f"   [{label}] {str(x)[:40]}...")
            return x
        return _log
    
    chain2 = (
        RunnableLambda(log_and_pass("INPUT"))
        | PromptTemplate.from_template("Topic: {topic}")
        | RunnableLambda(log_and_pass("PROMPT"))
        | chat
        | RunnableLambda(log_and_pass("MODEL"))
        | StrOutputParser()
        | RunnableLambda(log_and_pass("PARSED"))
    )
    
    result = chain2.invoke({"topic": "AI"})
    
    print("\n💡 Intermediate access helps with:")
    print("   • Debugging complex chains")
    print("   • Monitoring pipeline stages")
    print("   • Building composite outputs")
    print()


def performance_optimization():
    """Example 8: Optimizing sequences"""
    
    print("=" * 70)
    print("⚡ Example 8: Performance Optimization")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("\n🚀 Optimizing sequential pipelines")
    
    # Inefficient: Multiple sequential calls
    print("\n1️⃣ Inefficient approach (sequential calls):")
    
    chain_slow = (
        PromptTemplate.from_template("Summarize: {text}")
        | chat
        | StrOutputParser()
    )
    
    texts = [
        "AI is transforming technology",
        "Machine learning enables predictions",
        "Deep learning uses neural networks"
    ]
    
    start = time.time()
    results_slow = []
    for text in texts:
        results_slow.append(chain_slow.invoke({"text": text}))
    duration_slow = time.time() - start
    
    print(f"   Time: {duration_slow:.2f}s")
    print(f"   Results: {len(results_slow)}")
    
    # Efficient: Batch processing
    print("\n2️⃣ Efficient approach (batch):")
    
    start = time.time()
    results_fast = chain_slow.batch([{"text": t} for t in texts])
    duration_fast = time.time() - start
    
    print(f"   Time: {duration_fast:.2f}s")
    print(f"   Results: {len(results_fast)}")
    print(f"   Speedup: {duration_slow/duration_fast:.1f}x faster")
    
    # Optimization 3: Parallel independent steps
    print("\n3️⃣ Parallelize independent operations:")
    
    # Instead of sequential analysis
    chain_sequential = (
        RunnablePassthrough.assign(
            summary=PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser()
        )
        | RunnablePassthrough.assign(
            keywords=PromptTemplate.from_template("Keywords: {text}") | chat | StrOutputParser()
        )
    )
    
    # Use parallel
    chain_parallel = RunnablePassthrough.assign(
        **RunnableParallel(
            summary=PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser(),
            keywords=PromptTemplate.from_template("Keywords: {text}") | chat | StrOutputParser()
        )
    )
    
    text = "Artificial intelligence is revolutionizing industries worldwide"
    
    print("   Sequential analysis:")
    start = time.time()
    result_seq = chain_sequential.invoke({"text": text})
    duration_seq = time.time() - start
    print(f"   Time: {duration_seq:.2f}s")
    
    print("   Parallel analysis:")
    start = time.time()
    result_par = chain_parallel.invoke({"text": text})
    duration_par = time.time() - start
    print(f"   Time: {duration_par:.2f}s")
    print(f"   Speedup: {duration_seq/duration_par:.1f}x faster")
    
    print("\n💡 Performance tips:")
    print("   • Use batch() for multiple inputs")
    print("   • Parallelize independent operations")
    print("   • Stream for better UX")
    print("   • Cache expensive operations")
    print()


def main():
    """Run all RunnableSequence examples"""
    
    print("\n" + "🔗" * 35)
    print("Welcome to RunnableSequence - Sequential Composition!")
    print("🔗" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        pipe_operator_basics()
        input("Press Enter to continue...")
        
        manual_sequence_creation()
        input("Press Enter to continue...")
        
        automatic_coercion()
        input("Press Enter to continue...")
        
        streaming_behavior()
        input("Press Enter to continue...")
        
        error_propagation()
        input("Press Enter to continue...")
        
        nested_sequences()
        input("Press Enter to continue...")
        
        intermediate_access()
        input("Press Enter to continue...")
        
        performance_optimization()
        
        print("=" * 70)
        print("✅ RunnableSequence examples completed!")
        print("=" * 70)
        print("\n🎯 Key Takeaways:")
        print("  ✓ Pipe operator (|) creates sequences")
        print("  ✓ Automatic type coercion (strings, dicts, functions)")
        print("  ✓ Streaming flows through entire sequence")
        print("  ✓ Errors propagate unless handled")
        print("  ✓ Sequences can be nested arbitrarily")
        print("  ✓ Preserve intermediate results with assign()")
        print("  ✓ Optimize with batch() and parallel")
        print("\n💡 Next: RunnableParallel for concurrent execution!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
