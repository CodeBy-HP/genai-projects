"""
⛓️ Sequential Chains - Multi-Step Pipelines

This example covers:
- Linear pipelines (Step 1 → Step 2 → Step 3)
- Data transformation between steps
- Context passing through pipeline
- Multi-stage processing
- Error handling in sequences
- Preserving intermediate results
- Chain debugging techniques

Real-world sequential workflows!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any

# Load environment variables
load_dotenv()


def simple_sequential():
    """Example 1: Simple sequential chain - 3 steps"""
    
    print("=" * 70)
    print("⛓️ Simple Sequential Chain - Linear Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Step 1: Generate story idea
    step1 = (
        PromptTemplate.from_template("Generate a one-sentence story idea about: {topic}")
        | chat
        | StrOutputParser()
    )
    
    # Step 2: Expand the idea
    step2 = (
        PromptTemplate.from_template("Expand this idea into a 3-sentence plot: {idea}")
        | chat
        | StrOutputParser()
    )
    
    # Step 3: Add a twist
    step3 = (
        PromptTemplate.from_template("Add an unexpected twist to this plot: {plot}")
        | chat
        | StrOutputParser()
    )
    
    # Combine into sequential chain
    sequential_chain = (
        {"idea": step1}
        | {"plot": step2}
        | {"final_story": step3}
    )
    
    topic = "a robot learning to paint"
    
    print(f"\n📝 Input Topic: {topic}")
    print("\n🔄 Pipeline:")
    print("   Step 1: Generate idea")
    print("   Step 2: Expand to plot")
    print("   Step 3: Add twist")
    
    result = sequential_chain.invoke({"topic": topic})
    
    print("\n✅ Final Result:")
    print(f"   {result['final_story']}")
    
    print("\n💡 Each step uses output from previous step!")
    print()


def preserving_intermediate_results():
    """Example 2: Preserve all intermediate results"""
    
    print("=" * 70)
    print("💾 Preserving Intermediate Results")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Processing chain that keeps all steps
    chain = (
        # Step 1: Keep original + generate summary
        RunnablePassthrough.assign(
            summary=PromptTemplate.from_template(
                "Summarize in 1 sentence: {text}"
            ) | chat | StrOutputParser()
        )
        # Step 2: Keep everything + add keywords
        | RunnablePassthrough.assign(
            keywords=PromptTemplate.from_template(
                "Extract 3 keywords from: {summary}"
            ) | chat | StrOutputParser()
        )
        # Step 3: Keep everything + add category
        | RunnablePassthrough.assign(
            category=PromptTemplate.from_template(
                "Categorize this text (tech/business/health/other): {summary}"
            ) | chat | StrOutputParser()
        )
    )
    
    text = """
    Artificial intelligence is transforming healthcare through improved diagnostics,
    personalized treatment plans, and drug discovery. Machine learning models can
    detect diseases earlier than traditional methods.
    """
    
    print(f"\n📝 Original Text: {text.strip()[:80]}...")
    print("\n🔄 Sequential Processing:")
    print("   Step 1: Generate summary (keep original)")
    print("   Step 2: Extract keywords (keep original + summary)")
    print("   Step 3: Categorize (keep all)")
    
    result = chain.invoke({"text": text.strip()})
    
    print("\n✅ All Results Preserved:")
    print(f"   Original length: {len(result['text'])} characters")
    print(f"   Summary: {result['summary']}")
    print(f"   Keywords: {result['keywords']}")
    print(f"   Category: {result['category']}")
    
    print("\n💡 Use assign() to preserve all intermediate results!")
    print()


def data_transformation_pipeline():
    """Example 3: Transform data through multiple stages"""
    
    print("=" * 70)
    print("🔄 Data Transformation Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define transformation functions
    def extract_email_parts(x: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parts from email text"""
        email = x["email_text"]
        lines = email.strip().split('\n')
        
        return {
            "subject": lines[0].replace("Subject:", "").strip() if lines else "",
            "body": '\n'.join(lines[1:]).strip() if len(lines) > 1 else "",
            "original": email
        }
    
    def format_response(x: Dict[str, Any]) -> str:
        """Format final response"""
        return f"""
        EMAIL ANALYSIS REPORT
        =====================
        Subject: {x['subject']}
        
        Sentiment: {x['sentiment']}
        Priority: {x['priority']}
        
        Summary: {x['summary']}
        
        Recommended Action: {x['action']}
        """
    
    # Build transformation pipeline
    chain = (
        # Stage 1: Parse email
        RunnableLambda(extract_email_parts)
        
        # Stage 2: Analyze sentiment
        | RunnablePassthrough.assign(
            sentiment=PromptTemplate.from_template(
                "Sentiment analysis (positive/neutral/negative): {body}"
            ) | chat | StrOutputParser()
        )
        
        # Stage 3: Determine priority
        | RunnablePassthrough.assign(
            priority=PromptTemplate.from_template(
                "Priority level (high/medium/low): {subject} - {body}"
            ) | chat | StrOutputParser()
        )
        
        # Stage 4: Generate summary
        | RunnablePassthrough.assign(
            summary=PromptTemplate.from_template(
                "Summarize in 15 words: {body}"
            ) | chat | StrOutputParser()
        )
        
        # Stage 5: Recommend action
        | RunnablePassthrough.assign(
            action=PromptTemplate.from_template(
                "Recommend action based on priority {priority} and sentiment {sentiment}"
            ) | chat | StrOutputParser()
        )
        
        # Stage 6: Format output
        | RunnableLambda(format_response)
    )
    
    email_text = """Subject: Urgent - Production server down!
    
    Our main production server has been down for 2 hours. Customers are reporting
    errors and we're losing revenue. Need immediate assistance!
    """
    
    print("\n📧 Email Input:")
    print(email_text.strip())
    
    print("\n🔄 Transformation Stages:")
    print("   1. Parse email → Extract subject & body")
    print("   2. Analyze sentiment → Determine tone")
    print("   3. Determine priority → High/Medium/Low")
    print("   4. Generate summary → Brief overview")
    print("   5. Recommend action → What to do")
    print("   6. Format output → Pretty report")
    
    result = chain.invoke({"email_text": email_text})
    
    print("\n✅ Transformed Output:")
    print(result)
    
    print("\n💡 Sequential chains perfect for ETL pipelines!")
    print()


def context_passing():
    """Example 4: Pass context through multiple steps"""
    
    print("=" * 70)
    print("📦 Context Passing Through Pipeline")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Chain that builds context progressively
    chain = (
        # Step 1: Initial context
        RunnablePassthrough.assign(
            character=PromptTemplate.from_template(
                "Create a character name and trait for a {genre} story"
            ) | chat | StrOutputParser()
        )
        
        # Step 2: Add setting (using character context)
        | RunnablePassthrough.assign(
            setting=PromptTemplate.from_template(
                "Create a setting that matches this character: {character}"
            ) | chat | StrOutputParser()
        )
        
        # Step 3: Add conflict (using both character and setting)
        | RunnablePassthrough.assign(
            conflict=PromptTemplate.from_template(
                "Create a conflict for: Character: {character}, Setting: {setting}"
            ) | chat | StrOutputParser()
        )
        
        # Step 4: Write opening (using all context)
        | RunnablePassthrough.assign(
            opening=PromptTemplate.from_template(
                """Write a 2-sentence story opening:
                Character: {character}
                Setting: {setting}
                Conflict: {conflict}
                """
            ) | chat | StrOutputParser()
        )
    )
    
    genre = "sci-fi thriller"
    
    print(f"\n📚 Genre: {genre}")
    print("\n🔄 Context Building:")
    print("   Step 1: Create character")
    print("   Step 2: Create setting (uses character)")
    print("   Step 3: Create conflict (uses character + setting)")
    print("   Step 4: Write opening (uses all context)")
    
    result = chain.invoke({"genre": genre})
    
    print("\n✅ Progressive Context Building:")
    print(f"\n   Character: {result['character']}")
    print(f"\n   Setting: {result['setting']}")
    print(f"\n   Conflict: {result['conflict']}")
    print(f"\n   Opening: {result['opening']}")
    
    print("\n💡 Each step builds on accumulated context!")
    print()


def error_handling_in_sequence():
    """Example 5: Error handling in sequential chains"""
    
    print("=" * 70)
    print("🛡️ Error Handling in Sequential Chains")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define processing steps with validation
    def validate_input(x: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input has required field"""
        if "code" not in x or not x["code"].strip():
            raise ValueError("Input must contain 'code' field")
        return x
    
    def add_error_handling(x: Dict[str, Any]) -> Dict[str, Any]:
        """Add error status"""
        x["has_error"] = False
        x["error_message"] = None
        return x
    
    # Chain with error handling
    safe_chain = (
        RunnableLambda(validate_input)
        | RunnableLambda(add_error_handling)
        | RunnablePassthrough.assign(
            explanation=PromptTemplate.from_template(
                "Explain what this code does in simple terms:\n{code}"
            ) | chat | StrOutputParser()
        )
        | RunnablePassthrough.assign(
            bugs=PromptTemplate.from_template(
                "List potential bugs in:\n{code}"
            ) | chat | StrOutputParser()
        )
    )
    
    # Test with valid input
    print("\n1️⃣ Valid Input:")
    valid_code = """
    def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n-1)
    """
    
    try:
        result = safe_chain.invoke({"code": valid_code})
        print(f"   ✓ Success!")
        print(f"   Explanation: {result['explanation'][:60]}...")
        print(f"   Bugs: {result['bugs'][:60]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test with invalid input
    print("\n2️⃣ Invalid Input (empty code):")
    try:
        result = safe_chain.invoke({"code": ""})
        print(f"   ✓ Success (shouldn't reach here)")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")
    
    # Alternative: Graceful error handling
    def safe_processor(func):
        """Wrapper for safe processing"""
        def wrapper(x):
            try:
                return func(x)
            except Exception as e:
                return {**x, "has_error": True, "error_message": str(e)}
        return wrapper
    
    print("\n3️⃣ With Graceful Handling:")
    graceful_chain = (
        RunnableLambda(safe_processor(validate_input))
        | RunnableLambda(lambda x: x if not x.get("has_error") else x)
    )
    
    result = graceful_chain.invoke({"code": ""})
    if result.get("has_error"):
        print(f"   ✓ Gracefully handled: {result['error_message']}")
    
    print("\n💡 Add validation and error handling to robust chains!")
    print()


def multi_document_pipeline():
    """Example 6: Process multiple items sequentially"""
    
    print("=" * 70)
    print("📚 Multi-Document Sequential Processing")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.4,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Single document processor
    doc_processor = (
        RunnablePassthrough.assign(
            summary=PromptTemplate.from_template(
                "Summarize in 10 words: {text}"
            ) | chat | StrOutputParser()
        )
        | RunnablePassthrough.assign(
            category=PromptTemplate.from_template(
                "Category (tech/business/science/other): {summary}"
            ) | chat | StrOutputParser()
        )
    )
    
    documents = [
        {"text": "AI breakthrough: Neural networks now understand context better than ever."},
        {"text": "Stock market reaches new highs as tech companies report strong earnings."},
        {"text": "Scientists discover new species of deep-sea creatures near volcanic vents."}
    ]
    
    print("\n📚 Processing 3 documents sequentially...")
    
    # Process with batch (sequential internally)
    results = doc_processor.batch(documents)
    
    for i, (doc, result) in enumerate(zip(documents, results), 1):
        print(f"\n   Document {i}:")
        print(f"   Text: {doc['text'][:50]}...")
        print(f"   Summary: {result['summary']}")
        print(f"   Category: {result['category']}")
    
    print("\n💡 batch() processes items sequentially by default!")
    print("   For parallel: Use RunnableParallel (next module)")
    print()


def debugging_sequential_chain():
    """Example 7: Debug sequential chains step by step"""
    
    print("=" * 70)
    print("🔍 Debugging Sequential Chains")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Add logging between steps
    def log_step(step_name: str):
        """Create logging function for a step"""
        def logger(x):
            print(f"\n   🔍 After {step_name}:")
            if isinstance(x, dict):
                for key, value in x.items():
                    if isinstance(value, str):
                        print(f"      {key}: {value[:50]}...")
                    else:
                        print(f"      {key}: {value}")
            else:
                print(f"      {str(x)[:80]}...")
            return x
        return logger
    
    # Chain with logging at each step
    debug_chain = (
        RunnableLambda(log_step("INPUT"))
        
        | RunnablePassthrough.assign(
            step1=PromptTemplate.from_template(
                "Generate a company name for: {industry}"
            ) | chat | StrOutputParser()
        )
        | RunnableLambda(log_step("STEP 1"))
        
        | RunnablePassthrough.assign(
            step2=PromptTemplate.from_template(
                "Create a tagline for company: {step1}"
            ) | chat | StrOutputParser()
        )
        | RunnableLambda(log_step("STEP 2"))
        
        | RunnablePassthrough.assign(
            step3=PromptTemplate.from_template(
                "Suggest product for {step1} with tagline: {step2}"
            ) | chat | StrOutputParser()
        )
        | RunnableLambda(log_step("FINAL"))
    )
    
    print("\n🔍 Debug Mode - Logging Each Step:")
    
    result = debug_chain.invoke({"industry": "eco-friendly tech"})
    
    print("\n✅ Final Output:")
    print(f"   Company: {result['step1']}")
    print(f"   Tagline: {result['step2']}")
    print(f"   Product: {result['step3']}")
    
    print("\n💡 Add logging to debug complex chains!")
    print("   Use RunnableLambda(log_step(...)) between steps")
    print()


def main():
    """Run all sequential chain examples"""
    
    print("\n" + "⛓️" * 35)
    print("Welcome to Sequential Chains - Multi-Step Pipelines!")
    print("⛓️" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        simple_sequential()
        input("Press Enter to continue...")
        
        preserving_intermediate_results()
        input("Press Enter to continue...")
        
        data_transformation_pipeline()
        input("Press Enter to continue...")
        
        context_passing()
        input("Press Enter to continue...")
        
        error_handling_in_sequence()
        input("Press Enter to continue...")
        
        multi_document_pipeline()
        input("Press Enter to continue...")
        
        debugging_sequential_chain()
        
        print("=" * 70)
        print("✅ All Sequential Chain examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ Sequential chains: Step 1 → Step 2 → Step 3")
        print("  ✓ Use assign() to preserve intermediate results")
        print("  ✓ Each step can use outputs from previous steps")
        print("  ✓ Build context progressively through pipeline")
        print("  ✓ Add validation and error handling")
        print("  ✓ Use RunnableLambda for logging/debugging")
        print("  ✓ batch() processes items sequentially")
        print("\n📚 Next: Try 03_parallel_chains.py for concurrent execution!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
