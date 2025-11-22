"""
⚡ Parallel Chains - Concurrent Execution

This example covers:
- RunnableParallel - Run steps concurrently
- Performance optimization with parallelization
- Merging parallel outputs
- Independent task execution
- Multi-perspective analysis
- Concurrent API calls
- Parallel vs Sequential comparison

Speed up your chains with parallelization!
"""

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from typing import Dict, Any

# Load environment variables
load_dotenv()


def basic_parallel():
    """Example 1: Basic parallel execution"""
    
    print("=" * 70)
    print("⚡ Basic Parallel Execution - RunnableParallel")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create independent chains
    chain_a = PromptTemplate.from_template(
        "Pros of {topic}:"
    ) | chat | StrOutputParser()
    
    chain_b = PromptTemplate.from_template(
        "Cons of {topic}:"
    ) | chat | StrOutputParser()
    
    chain_c = PromptTemplate.from_template(
        "Neutral facts about {topic}:"
    ) | chat | StrOutputParser()
    
    # Run in parallel
    parallel_chain = RunnableParallel(
        pros=chain_a,
        cons=chain_b,
        facts=chain_c
    )
    
    topic = "remote work"
    
    print(f"\n📝 Topic: {topic}")
    print("\n⚡ Running 3 chains in parallel:")
    print("   • Chain A: Pros")
    print("   • Chain B: Cons")
    print("   • Chain C: Facts")
    
    start = time.time()
    result = parallel_chain.invoke({"topic": topic})
    elapsed = time.time() - start
    
    print(f"\n✅ Results (completed in {elapsed:.2f}s):")
    print(f"\n   Pros: {result['pros'][:60]}...")
    print(f"\n   Cons: {result['cons'][:60]}...")
    print(f"\n   Facts: {result['facts'][:60]}...")
    
    print("\n💡 All chains executed concurrently!")
    print()


def parallel_vs_sequential():
    """Example 2: Compare parallel vs sequential performance"""
    
    print("=" * 70)
    print("🏎️ Parallel vs Sequential Performance")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define task chains
    task1 = PromptTemplate.from_template("Fact about {topic} #1:") | chat | StrOutputParser()
    task2 = PromptTemplate.from_template("Fact about {topic} #2:") | chat | StrOutputParser()
    task3 = PromptTemplate.from_template("Fact about {topic} #3:") | chat | StrOutputParser()
    
    # Sequential execution
    sequential_chain = (
        RunnablePassthrough.assign(fact1=task1)
        | RunnablePassthrough.assign(fact2=task2)
        | RunnablePassthrough.assign(fact3=task3)
    )
    
    # Parallel execution
    parallel_chain = RunnableParallel(
        fact1=task1,
        fact2=task2,
        fact3=task3
    )
    
    topic = "space exploration"
    
    print(f"\n📝 Topic: {topic}")
    
    # Test sequential
    print("\n🐌 Sequential Execution (one after another):")
    start = time.time()
    seq_result = sequential_chain.invoke({"topic": topic})
    seq_time = time.time() - start
    print(f"   ⏱️  Time: {seq_time:.2f} seconds")
    
    # Test parallel
    print("\n🚀 Parallel Execution (all at once):")
    start = time.time()
    par_result = parallel_chain.invoke({"topic": topic})
    par_time = time.time() - start
    print(f"   ⏱️  Time: {par_time:.2f} seconds")
    
    # Comparison
    speedup = seq_time / par_time if par_time > 0 else 0
    print(f"\n📊 Performance Gain:")
    print(f"   Speedup: {speedup:.2f}x faster")
    print(f"   Time saved: {seq_time - par_time:.2f} seconds")
    
    print("\n💡 Parallel execution is significantly faster for independent tasks!")
    print()


def multi_perspective_analysis():
    """Example 3: Analyze from multiple perspectives simultaneously"""
    
    print("=" * 70)
    print("🔍 Multi-Perspective Analysis")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Different analytical perspectives
    analysis_chain = RunnableParallel(
        technical=PromptTemplate.from_template(
            "Technical analysis of: {product}"
        ) | chat | StrOutputParser(),
        
        business=PromptTemplate.from_template(
            "Business perspective on: {product}"
        ) | chat | StrOutputParser(),
        
        user_experience=PromptTemplate.from_template(
            "User experience analysis of: {product}"
        ) | chat | StrOutputParser(),
        
        competitive=PromptTemplate.from_template(
            "Competitive positioning of: {product}"
        ) | chat | StrOutputParser()
    )
    
    product = "AI-powered code assistant"
    
    print(f"\n📦 Product: {product}")
    print("\n🔄 Analyzing from 4 perspectives in parallel:")
    print("   • Technical")
    print("   • Business")
    print("   • User Experience")
    print("   • Competitive")
    
    result = analysis_chain.invoke({"product": product})
    
    print("\n✅ Multi-Perspective Results:")
    for perspective, analysis in result.items():
        print(f"\n   {perspective.upper()}:")
        print(f"   {analysis[:80]}...")
    
    print("\n💡 Get comprehensive analysis in one parallel execution!")
    print()


def parallel_with_passthrough():
    """Example 4: Parallel chains with preserved input"""
    
    print("=" * 70)
    print("💾 Parallel Chains + Preserved Input")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Parallel processing while keeping original
    chain = RunnableParallel(
        original=RunnablePassthrough(),
        
        analysis=RunnableParallel(
            sentiment=PromptTemplate.from_template(
                "Sentiment (positive/neutral/negative): {text}"
            ) | chat | StrOutputParser(),
            
            keywords=PromptTemplate.from_template(
                "Extract 3 keywords from: {text}"
            ) | chat | StrOutputParser(),
            
            category=PromptTemplate.from_template(
                "Categorize (tech/business/health/other): {text}"
            ) | chat | StrOutputParser()
        )
    )
    
    text = "Revolutionary AI technology is transforming healthcare diagnostics."
    
    print(f"\n📝 Input: {text}")
    print("\n⚡ Parallel Analysis:")
    print("   • Sentiment analysis")
    print("   • Keyword extraction")
    print("   • Categorization")
    print("   (Original text preserved)")
    
    result = chain.invoke({"text": text})
    
    print("\n✅ Results:")
    print(f"   Original: {result['original']['text']}")
    print(f"\n   Analysis:")
    print(f"      Sentiment: {result['analysis']['sentiment']}")
    print(f"      Keywords: {result['analysis']['keywords']}")
    print(f"      Category: {result['analysis']['category']}")
    
    print("\n💡 Nest RunnableParallel + RunnablePassthrough for complex structures!")
    print()


def merge_parallel_outputs():
    """Example 5: Merge outputs from parallel chains"""
    
    print("=" * 70)
    print("🔀 Merging Parallel Outputs")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    def merge_reviews(x: Dict[str, Any]) -> str:
        """Combine parallel reviews into final summary"""
        return f"""
COMPREHENSIVE REVIEW
====================
Technical Score: {x['technical']}
Design Score: {x['design']}
Value Score: {x['value']}

Overall: Excellent product with strong ratings across all dimensions.
"""
    
    # Parallel rating + merge
    chain = (
        RunnableParallel(
            technical=PromptTemplate.from_template(
                "Rate technical quality of {product} (1-10):"
            ) | chat | StrOutputParser(),
            
            design=PromptTemplate.from_template(
                "Rate design quality of {product} (1-10):"
            ) | chat | StrOutputParser(),
            
            value=PromptTemplate.from_template(
                "Rate value/price of {product} (1-10):"
            ) | chat | StrOutputParser()
        )
        | RunnableLambda(merge_reviews)
    )
    
    product = "wireless noise-canceling headphones"
    
    print(f"\n📦 Product: {product}")
    print("\n⚡ Parallel Rating + Merge:")
    print("   Step 1: Rate technical, design, value (parallel)")
    print("   Step 2: Merge into final review")
    
    result = chain.invoke({"product": product})
    
    print("\n✅ Merged Result:")
    print(result)
    
    print("\n💡 Use RunnableLambda after parallel to merge results!")
    print()


def conditional_parallel():
    """Example 6: Conditional parallel execution"""
    
    print("=" * 70)
    print("🎯 Conditional Parallel Execution")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    def create_parallel_chain(analysis_type: str):
        """Create different parallel chains based on type"""
        if analysis_type == "detailed":
            return RunnableParallel(
                summary=PromptTemplate.from_template("Summarize: {text}") | chat | StrOutputParser(),
                keywords=PromptTemplate.from_template("Keywords: {text}") | chat | StrOutputParser(),
                sentiment=PromptTemplate.from_template("Sentiment: {text}") | chat | StrOutputParser(),
                entities=PromptTemplate.from_template("Entities: {text}") | chat | StrOutputParser()
            )
        else:  # quick
            return RunnableParallel(
                summary=PromptTemplate.from_template("Quick summary: {text}") | chat | StrOutputParser(),
                sentiment=PromptTemplate.from_template("Sentiment: {text}") | chat | StrOutputParser()
            )
    
    text = "Apple announces new iPhone with revolutionary camera technology."
    
    # Detailed analysis
    print("\n1️⃣ Detailed Analysis (4 parallel tasks):")
    detailed_chain = create_parallel_chain("detailed")
    result = detailed_chain.invoke({"text": text})
    print(f"   Keys: {list(result.keys())}")
    
    # Quick analysis
    print("\n2️⃣ Quick Analysis (2 parallel tasks):")
    quick_chain = create_parallel_chain("quick")
    result = quick_chain.invoke({"text": text})
    print(f"   Keys: {list(result.keys())}")
    
    print("\n💡 Adjust parallelization based on requirements!")
    print()


def batch_parallel_processing():
    """Example 7: Process multiple items with parallel chains"""
    
    print("=" * 70)
    print("📚 Batch Processing with Parallel Chains")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Parallel analysis per item
    item_processor = RunnableParallel(
        summary=PromptTemplate.from_template(
            "Summarize in 5 words: {text}"
        ) | chat | StrOutputParser(),
        
        category=PromptTemplate.from_template(
            "Category: {text}"
        ) | chat | StrOutputParser()
    )
    
    items = [
        {"text": "AI breakthrough in natural language understanding"},
        {"text": "Stock market volatility impacts tech sector"},
        {"text": "New vaccine shows promising results in trials"}
    ]
    
    print(f"\n📚 Processing {len(items)} items...")
    print("   Each item: 2 parallel analyses")
    
    start = time.time()
    results = item_processor.batch(items)
    elapsed = time.time() - start
    
    print(f"\n✅ Results (completed in {elapsed:.2f}s):")
    for i, (item, result) in enumerate(zip(items, results), 1):
        print(f"\n   Item {i}: {item['text'][:40]}...")
        print(f"      Summary: {result['summary']}")
        print(f"      Category: {result['category']}")
    
    print("\n💡 Combine batch + parallel for maximum efficiency!")
    print()


def main():
    """Run all parallel chain examples"""
    
    print("\n" + "⚡" * 35)
    print("Welcome to Parallel Chains - Concurrent Execution!")
    print("⚡" * 35 + "\n")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        basic_parallel()
        input("Press Enter to continue...")
        
        parallel_vs_sequential()
        input("Press Enter to continue...")
        
        multi_perspective_analysis()
        input("Press Enter to continue...")
        
        parallel_with_passthrough()
        input("Press Enter to continue...")
        
        merge_parallel_outputs()
        input("Press Enter to continue...")
        
        conditional_parallel()
        input("Press Enter to continue...")
        
        batch_parallel_processing()
        
        print("=" * 70)
        print("✅ All Parallel Chain examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ RunnableParallel runs tasks concurrently")
        print("  ✓ Significantly faster than sequential")
        print("  ✓ Perfect for independent operations")
        print("  ✓ Combine with RunnablePassthrough to preserve input")
        print("  ✓ Use RunnableLambda to merge parallel results")
        print("  ✓ Nest parallel chains for complex structures")
        print("  ✓ batch() + parallel = maximum efficiency")
        print("\n📚 Next: Try 04_conditional_chains.py for dynamic routing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
