"""
🔗 LCEL Basics - LangChain Expression Language Fundamentals

This example covers:
- Pipe operator (|) - Chain composition
- invoke() / batch() / stream() - Execution methods
- RunnablePassthrough - Pass data through
- RunnableLambda - Custom functions
- assign() - Add fields to dict
- pick() - Extract specific fields
- Chaining prompts, LLMs, and parsers
- Input/output transformation

Master LCEL - the modern way to build chains!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel
)
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any

# Load environment variables
load_dotenv()


def pipe_operator_basics():
    """Example 1: Pipe Operator - Chain composition with |"""
    
    print("=" * 70)
    print("🔗 Pipe Operator (|) - Modern Chain Composition")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create individual components
    prompt = PromptTemplate(
        template="Write a haiku about {topic}",
        input_variables=["topic"]
    )
    
    parser = StrOutputParser()
    
    # Compose with pipe operator!
    chain = prompt | chat | parser
    
    print("\n📐 Chain Structure:")
    print("   prompt | chat | parser")
    print("   PromptTemplate → ChatModel → StrOutputParser")
    
    print("\n🎯 Execution:")
    topic = "artificial intelligence"
    result = chain.invoke({"topic": topic})
    
    print(f"\n   Topic: {topic}")
    print(f"   Haiku:\n   {result}")
    
    print("\n💡 Pipe operator (|) chains components left to right!")
    print("   Just like Unix pipes: data flows through each step")
    print()


def execution_methods():
    """Example 2: invoke() / batch() / stream() - Different execution modes"""
    
    print("=" * 70)
    print("⚡ Execution Methods - invoke, batch, stream")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = PromptTemplate(
        template="Fun fact about {topic}:",
        input_variables=["topic"]
    )
    
    chain = prompt | chat | StrOutputParser()
    
    # Method 1: invoke() - Single input
    print("\n1️⃣ invoke() - Process single input:")
    result = chain.invoke({"topic": "python"})
    print(f"   {result[:80]}...")
    
    # Method 2: batch() - Multiple inputs
    print("\n2️⃣ batch() - Process multiple inputs:")
    topics = [
        {"topic": "space"},
        {"topic": "ocean"},
        {"topic": "mountains"}
    ]
    results = chain.batch(topics)
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result[:60]}...")
    
    # Method 3: stream() - Streaming output
    print("\n3️⃣ stream() - Stream output token by token:")
    print("   ", end="")
    for chunk in chain.stream({"topic": "AI"}):
        print(chunk, end="", flush=True)
    print()
    
    print("\n💡 Three ways to run chains:")
    print("   • invoke() → Single result")
    print("   • batch() → Multiple results")
    print("   • stream() → Real-time streaming")
    print()


def runnable_passthrough():
    """Example 3: RunnablePassthrough - Preserve original input"""
    
    print("=" * 70)
    print("🔄 RunnablePassthrough - Keep Original Data")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Problem: Chain loses original input!
    simple_chain = (
        PromptTemplate.from_template("Summarize: {text}")
        | chat
        | StrOutputParser()
    )
    
    text = "The quick brown fox jumps over the lazy dog."
    simple_result = simple_chain.invoke({"text": text})
    
    print("\n❌ Without RunnablePassthrough:")
    print(f"   Input: {text}")
    print(f"   Output: {simple_result[:60]}...")
    print("   ⚠️  Original text is lost!")
    
    # Solution: Use RunnablePassthrough to preserve input
    chain_with_passthrough = {
        "original": RunnablePassthrough(),
        "summary": (
            PromptTemplate.from_template("Summarize in 5 words: {text}")
            | chat
            | StrOutputParser()
        )
    }
    
    result = chain_with_passthrough.invoke({"text": text})
    
    print("\n✅ With RunnablePassthrough:")
    print(f"   Original: {result['original']['text']}")
    print(f"   Summary: {result['summary']}")
    print("   ✓ Both preserved!")
    
    print("\n💡 RunnablePassthrough preserves data in the pipeline!")
    print()


def runnable_lambda():
    """Example 4: RunnableLambda - Custom Python functions"""
    
    print("=" * 70)
    print("🎨 RunnableLambda - Custom Function as Chain Step")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define custom processing functions
    def uppercase_processor(x: Dict[str, Any]) -> Dict[str, Any]:
        """Convert input to uppercase"""
        return {"text": x["text"].upper()}
    
    def word_counter(x: str) -> Dict[str, Any]:
        """Count words in text"""
        words = x.split()
        return {
            "text": x,
            "word_count": len(words),
            "char_count": len(x)
        }
    
    # Use RunnableLambda to wrap functions
    chain = (
        RunnableLambda(uppercase_processor)
        | PromptTemplate.from_template("Improve this text: {text}")
        | chat
        | StrOutputParser()
        | RunnableLambda(word_counter)
    )
    
    input_text = "hello world from langchain"
    
    print(f"\n📝 Input: {input_text}")
    print("\n🔄 Chain steps:")
    print("   1. uppercase_processor (custom)")
    print("   2. PromptTemplate")
    print("   3. ChatModel")
    print("   4. StrOutputParser")
    print("   5. word_counter (custom)")
    
    result = chain.invoke({"text": input_text})
    
    print("\n✅ Final Result:")
    print(f"   Text: {result['text'][:60]}...")
    print(f"   Words: {result['word_count']}")
    print(f"   Characters: {result['char_count']}")
    
    print("\n💡 RunnableLambda lets you use ANY Python function in chains!")
    print()


def assign_operator():
    """Example 5: assign() - Add fields to existing dict"""
    
    print("=" * 70)
    print("➕ assign() - Add New Fields Without Replacing")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create processing chains
    summary_chain = (
        PromptTemplate.from_template("Summarize in 10 words: {text}")
        | chat
        | StrOutputParser()
    )
    
    sentiment_chain = (
        PromptTemplate.from_template("Sentiment (positive/negative/neutral): {text}")
        | chat
        | StrOutputParser()
    )
    
    # Use assign() to add fields
    chain = RunnablePassthrough.assign(
        summary=summary_chain,
        sentiment=sentiment_chain
    )
    
    text = "I absolutely love this product! It's amazing and works perfectly."
    
    print(f"\n📝 Original Input:")
    print(f"   text: {text}")
    
    result = chain.invoke({"text": text})
    
    print("\n✅ After assign():")
    print(f"   text: {result['text']}")
    print(f"   summary: {result['summary']}")
    print(f"   sentiment: {result['sentiment']}")
    
    print("\n💡 assign() adds new fields while keeping original!")
    print("   Input: {text}")
    print("   Output: {text, summary, sentiment}")
    print()


def pick_operator():
    """Example 6: pick() - Extract specific fields"""
    
    print("=" * 70)
    print("🎯 pick() - Select Specific Fields")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create a chain that produces multiple fields
    analysis_chain = (
        RunnablePassthrough.assign(
            word_count=RunnableLambda(lambda x: len(x["text"].split())),
            char_count=RunnableLambda(lambda x: len(x["text"])),
            uppercase=RunnableLambda(lambda x: x["text"].upper())
        )
    )
    
    text = "LangChain makes building AI apps easy"
    
    print(f"\n📝 Input: {text}")
    
    # Get all fields
    print("\n1️⃣ Without pick() - All fields:")
    full_result = analysis_chain.invoke({"text": text})
    for key, value in full_result.items():
        print(f"   {key}: {value}")
    
    # Pick only specific field
    print("\n2️⃣ With pick('word_count') - Single field:")
    pick_single = analysis_chain | RunnablePassthrough.pick("word_count")
    result = pick_single.invoke({"text": text})
    print(f"   {result}")
    
    # Pick multiple fields
    print("\n3️⃣ With pick(['text', 'word_count']) - Multiple fields:")
    pick_multiple = analysis_chain | RunnablePassthrough.pick(["text", "word_count"])
    result = pick_multiple.invoke({"text": text})
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    print("\n💡 pick() extracts only what you need!")
    print()


def chaining_with_parsers():
    """Example 7: Chaining with different parsers"""
    
    print("=" * 70)
    print("🔧 Chaining Prompts, LLMs, and Parsers")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Chain 1: String output
    print("\n1️⃣ Chain with StrOutputParser:")
    str_chain = (
        PromptTemplate.from_template("Generate a product name for: {category}")
        | chat
        | StrOutputParser()
    )
    
    result = str_chain.invoke({"category": "eco-friendly water bottle"})
    print(f"   Result type: {type(result)}")
    print(f"   Result: {result}")
    
    # Chain 2: JSON output
    print("\n2️⃣ Chain with JsonOutputParser:")
    
    class Product(BaseModel):
        """Product information"""
        name: str = Field(description="Product name")
        price: float = Field(description="Price in USD")
        category: str = Field(description="Product category")
    
    json_parser = JsonOutputParser(pydantic_object=Product)
    
    json_chain = (
        PromptTemplate(
            template="Generate product info.\n{format_instructions}\nProduct: {desc}",
            input_variables=["desc"],
            partial_variables={"format_instructions": json_parser.get_format_instructions()}
        )
        | chat
        | json_parser
    )
    
    result = json_chain.invoke({"desc": "wireless earbuds"})
    print(f"   Result type: {type(result)}")
    print(f"   Result: {result}")
    
    print("\n💡 Different parsers = different output types!")
    print("   StrOutputParser → str")
    print("   JsonOutputParser → dict")
    print("   PydanticOutputParser → Pydantic object")
    print()


def complex_chain_composition():
    """Example 8: Complex chain with multiple patterns"""
    
    print("=" * 70)
    print("🚀 Complex Chain Composition - All Together")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define custom processors
    def prepare_input(x: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare and validate input"""
        return {
            "topic": x["topic"].strip().lower(),
            "original_topic": x["topic"]
        }
    
    def add_metadata(x: str) -> Dict[str, Any]:
        """Add metadata to result"""
        return {
            "content": x,
            "length": len(x),
            "words": len(x.split())
        }
    
    # Build complex chain
    chain = (
        # Step 1: Prepare input
        RunnableLambda(prepare_input)
        
        # Step 2: Generate content with passthrough
        | RunnablePassthrough.assign(
            description=PromptTemplate.from_template(
                "Write a 2-sentence description of {topic}"
            ) | chat | StrOutputParser()
        )
        
        # Step 3: Pick just the description
        | RunnablePassthrough.pick("description")
        
        # Step 4: Add metadata
        | RunnableLambda(add_metadata)
        
        # Step 5: Add analysis
        | RunnablePassthrough.assign(
            analysis=RunnableLambda(
                lambda x: f"Generated {x['words']} words, {x['length']} characters"
            )
        )
    )
    
    topic = "  Machine Learning  "  # With extra spaces
    
    print(f"\n📝 Input: '{topic}'")
    print("\n🔄 Chain Pipeline:")
    print("   1. prepare_input → Clean & normalize")
    print("   2. assign(description) → Generate content")
    print("   3. pick('description') → Extract field")
    print("   4. add_metadata → Add stats")
    print("   5. assign(analysis) → Add analysis")
    
    result = chain.invoke({"topic": topic})
    
    print("\n✅ Final Result:")
    print(f"   Content: {result['content'][:80]}...")
    print(f"   Length: {result['length']} characters")
    print(f"   Words: {result['words']} words")
    print(f"   Analysis: {result['analysis']}")
    
    print("\n💡 LCEL chains can be arbitrarily complex!")
    print("   Mix: pipes, passthrough, assign, pick, lambdas")
    print()


def main():
    """Run all LCEL basics examples"""
    
    print("\n" + "🔗" * 35)
    print("Welcome to LCEL Basics - Modern LangChain Chains!")
    print("🔗" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        pipe_operator_basics()
        input("Press Enter to continue...")
        
        execution_methods()
        input("Press Enter to continue...")
        
        runnable_passthrough()
        input("Press Enter to continue...")
        
        runnable_lambda()
        input("Press Enter to continue...")
        
        assign_operator()
        input("Press Enter to continue...")
        
        pick_operator()
        input("Press Enter to continue...")
        
        chaining_with_parsers()
        input("Press Enter to continue...")
        
        complex_chain_composition()
        
        print("=" * 70)
        print("✅ All LCEL Basics examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ Pipe operator (|) chains components")
        print("  ✓ invoke() / batch() / stream() for execution")
        print("  ✓ RunnablePassthrough preserves data")
        print("  ✓ RunnableLambda wraps custom functions")
        print("  ✓ assign() adds fields to dict")
        print("  ✓ pick() extracts specific fields")
        print("  ✓ Mix and match for complex pipelines")
        print("\n📚 Next: Try 02_sequential_chains.py for multi-step pipelines!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
