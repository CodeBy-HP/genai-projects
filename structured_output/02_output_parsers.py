"""
🔧 Output Parsers - Universal Structured Output

This example covers:
- PydanticOutputParser (Pydantic models)
- JsonOutputParser (JSON/dict)
- StructuredOutputParser (ResponseSchema)
- StrOutputParser (clean strings)
- CommaSeparatedListOutputParser (lists)
- DatetimeOutputParser (dates/times)
- EnumOutputParser (enum values)
- BooleanOutputParser (true/false)

Use when models DON'T support with_structured_output!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import (
    JsonOutputParser,
    StrOutputParser,
    CommaSeparatedListOutputParser,
    PydanticOutputParser
)
from langchain.output_parsers import (
    StructuredOutputParser,
    ResponseSchema,
    DatetimeOutputParser,
    EnumOutputParser,
    BooleanOutputParser
)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime
from enum import Enum

# Load environment variables
load_dotenv()


def pydantic_output_parser():
    """Example 1: PydanticOutputParser - Parse into Pydantic models"""
    
    print("=" * 70)
    print("🔧 PydanticOutputParser - Parse into Pydantic Models")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define Pydantic model
    class Article(BaseModel):
        """News article"""
        title: str = Field(description="Article title")
        author: str = Field(description="Author name")
        summary: str = Field(description="Brief summary")
        category: str = Field(description="Article category")
        word_count: int = Field(description="Approximate word count")
    
    # Create parser
    parser = PydanticOutputParser(pydantic_object=Article)
    
    # Get format instructions
    format_instructions = parser.get_format_instructions()
    
    print("\n📋 Format Instructions (sent to AI):")
    print(format_instructions[:200] + "...")
    
    # Create prompt with instructions
    template = """Extract article information.

{format_instructions}

Article text: {text}

Your response:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )
    
    # Create chain
    chain = prompt | chat | parser
    
    article_text = """
    The Future of AI in Healthcare by Dr. Jane Smith
    
    Artificial intelligence is revolutionizing healthcare through improved diagnostics,
    personalized treatment plans, and drug discovery. Machine learning models can now
    detect diseases earlier and more accurately than traditional methods.
    This breakthrough technology promises to save millions of lives.
    """
    
    print(f"\n👤 Input: Article text ({len(article_text.split())} words)")
    print("\n🤖 Parsed Output:")
    
    result = chain.invoke({"text": article_text})
    
    # Result is Article object!
    print(f"   Type: {type(result)}")
    print(f"   Title: {result.title}")
    print(f"   Author: {result.author}")
    print(f"   Category: {result.category}")
    print(f"   Summary: {result.summary}")
    print(f"   Word Count: {result.word_count}")
    
    print("\n✨ Parser + format instructions = structured output!")
    print()


def json_output_parser():
    """Example 2: JsonOutputParser - Parse into JSON/dict"""
    
    print("=" * 70)
    print("📦 JsonOutputParser - Parse into JSON/Dict")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Optional: Define schema with Pydantic
    class Company(BaseModel):
        """Company information"""
        name: str = Field(description="Company name")
        industry: str = Field(description="Industry sector")
        founded: int = Field(description="Year founded")
        employees: int = Field(description="Number of employees")
        headquarters: str = Field(description="HQ location")
    
    # Create JSON parser (can work with or without schema)
    parser = JsonOutputParser(pydantic_object=Company)
    
    template = ChatPromptTemplate.from_messages([
        ("system", "Extract company information as JSON."),
        ("human", "{text}\n\n{format_instructions}")
    ])
    
    chain = template | chat | parser
    
    text = """
    Tesla Inc. is an American automotive and clean energy company.
    Founded in 2003, Tesla is headquartered in Austin, Texas.
    The company employs approximately 127,000 people worldwide
    and operates in the electric vehicle and renewable energy industries.
    """
    
    print(f"\n👤 Input: Company description")
    print("\n🤖 Parsed Output:")
    
    result = chain.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    
    # Result is dict!
    print(f"   Type: {type(result)}")
    print(f"   Data: {result}")
    print(f"\n   Name: {result['name']}")
    print(f"   Industry: {result['industry']}")
    print(f"   Founded: {result['founded']}")
    print(f"   Employees: {result['employees']:,}")
    print(f"   HQ: {result['headquarters']}")
    
    print("\n💡 JsonOutputParser returns dict, not objects!")
    print()


def structured_output_parser():
    """Example 3: StructuredOutputParser - Simple field extraction"""
    
    print("=" * 70)
    print("📋 StructuredOutputParser - ResponseSchema")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define response schemas
    response_schemas = [
        ResponseSchema(
            name="customer_name",
            description="The customer's full name"
        ),
        ResponseSchema(
            name="email",
            description="The customer's email address"
        ),
        ResponseSchema(
            name="issue_type",
            description="Type of issue: technical, billing, or general"
        ),
        ResponseSchema(
            name="priority",
            description="Priority level: low, medium, or high"
        ),
        ResponseSchema(
            name="summary",
            description="Brief summary of the issue"
        )
    ]
    
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    template = PromptTemplate(
        template="""Extract customer support ticket information.

{format_instructions}

Support ticket: {ticket}

Output:""",
        input_variables=["ticket"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    ticket = """
    From: john.doe@email.com
    Name: John Doe
    
    My billing shows duplicate charges for the last two months.
    This is urgent as it's affecting my budget. Please resolve ASAP.
    """
    
    print(f"\n👤 Input: Support ticket")
    print("\n🤖 Parsed Output:")
    
    result = chain.invoke({"ticket": ticket})
    
    print(f"   Customer: {result['customer_name']}")
    print(f"   Email: {result['email']}")
    print(f"   Issue Type: {result['issue_type']}")
    print(f"   Priority: {result['priority']}")
    print(f"   Summary: {result['summary']}")
    
    print("\n💡 StructuredOutputParser: Simple & effective!")
    print()


def string_output_parser():
    """Example 4: StrOutputParser - Clean string output"""
    
    print("=" * 70)
    print("📝 StrOutputParser - Clean Text Output")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # StrOutputParser just returns clean string
    parser = StrOutputParser()
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful writing assistant."),
        ("human", "Write a tagline for: {product}")
    ])
    
    chain = template | chat | parser
    
    products = [
        "eco-friendly water bottle",
        "smart home security system",
        "online coding bootcamp"
    ]
    
    print("\n🎯 Generating clean text outputs:")
    
    for product in products:
        result = chain.invoke({"product": product})
        
        print(f"\n   Product: {product}")
        print(f"   Tagline: {result}")
        print(f"   Type: {type(result)}")  # str
    
    print("\n💡 StrOutputParser: For simple text output!")
    print()


def list_output_parser():
    """Example 5: CommaSeparatedListOutputParser - Lists"""
    
    print("=" * 70)
    print("📝 CommaSeparatedListOutputParser - List Extraction")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    parser = CommaSeparatedListOutputParser()
    
    template = PromptTemplate(
        template="""List {count} {category}.

{format_instructions}

Output:""",
        input_variables=["count", "category"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    queries = [
        {"count": "5", "category": "popular programming languages"},
        {"count": "3", "category": "cloud computing platforms"},
        {"count": "4", "category": "machine learning frameworks"}
    ]
    
    print("\n📝 Extracting lists:")
    
    for query in queries:
        result = chain.invoke(query)
        
        print(f"\n   Query: {query['count']} {query['category']}")
        print(f"   Result type: {type(result)}")  # list
        print(f"   Items:")
        for i, item in enumerate(result, 1):
            print(f"      {i}. {item.strip()}")
    
    print("\n💡 Perfect for extracting lists from text!")
    print()


def datetime_output_parser():
    """Example 6: DatetimeOutputParser - Parse dates/times"""
    
    print("=" * 70)
    print("📅 DatetimeOutputParser - Date/Time Extraction")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    parser = DatetimeOutputParser()
    
    template = PromptTemplate(
        template="""Extract the date from this text and format it.

{format_instructions}

Text: {text}

Date:""",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    texts = [
        "The meeting is scheduled for March 15, 2024",
        "Project deadline: 2024-06-30",
        "Event on 01/01/2025"
    ]
    
    print("\n📅 Parsing dates:")
    
    for text in texts:
        result = chain.invoke({"text": text})
        
        print(f"\n   Input: {text}")
        print(f"   Parsed: {result}")
        print(f"   Type: {type(result)}")  # datetime
        print(f"   Formatted: {result.strftime('%B %d, %Y')}")
    
    print("\n💡 Returns proper datetime objects!")
    print()


def boolean_output_parser():
    """Example 7: BooleanOutputParser - True/False"""
    
    print("=" * 70)
    print("✓ BooleanOutputParser - True/False Extraction")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    parser = BooleanOutputParser()
    
    template = PromptTemplate(
        template="""Answer with yes or no.

{format_instructions}

Question: {question}

Answer:""",
        input_variables=["question"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    questions = [
        "Is Python a programming language?",
        "Is the Earth flat?",
        "Can AI help with data analysis?",
        "Is 2+2 equal to 5?"
    ]
    
    print("\n✓ Boolean questions:")
    
    for question in questions:
        result = chain.invoke({"question": question})
        
        symbol = "✅" if result else "❌"
        print(f"\n   Q: {question}")
        print(f"   A: {result} {symbol}")
        print(f"   Type: {type(result)}")  # bool
    
    print("\n💡 Clean boolean values!")
    print()


def enum_output_parser():
    """Example 8: EnumOutputParser - Enum values"""
    
    print("=" * 70)
    print("🎨 EnumOutputParser - Enum Value Extraction")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define enum
    class Sentiment(str, Enum):
        POSITIVE = "positive"
        NEUTRAL = "neutral"
        NEGATIVE = "negative"
    
    parser = EnumOutputParser(enum=Sentiment)
    
    template = PromptTemplate(
        template="""Analyze the sentiment of this text.

{format_instructions}

Text: {text}

Sentiment:""",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = template | chat | parser
    
    texts = [
        "This product is amazing! Best purchase ever!",
        "It's okay, nothing special.",
        "Terrible experience. Very disappointed."
    ]
    
    print("\n🎨 Sentiment analysis:")
    
    for text in texts:
        result = chain.invoke({"text": text})
        
        emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}
        
        print(f"\n   Text: {text[:50]}...")
        print(f"   Sentiment: {result.value} {emoji[result.value]}")
        print(f"   Type: {type(result)}")  # Sentiment enum
    
    print("\n💡 Ensures only valid enum values!")
    print()


def comparing_parsers():
    """Example 9: Comparing different parsers"""
    
    print("=" * 70)
    print("⚖️  Comparing All Parsers")
    print("=" * 70)
    
    text = "John Smith, age 30, lives in NYC, email: john@email.com"
    
    print(f"\n📝 Input text: {text}")
    print("\n🔍 Different parsers for different needs:\n")
    
    parsers = {
        "StrOutputParser": "Clean text output",
        "JsonOutputParser": "Dict/JSON output",
        "PydanticOutputParser": "Validated Pydantic object",
        "StructuredOutputParser": "Simple field extraction",
        "CommaSeparatedListOutputParser": "List extraction"
    }
    
    for parser_name, description in parsers.items():
        print(f"   {parser_name}")
        print(f"   └─ Use case: {description}")
        print()
    
    print("💡 Choose based on your needs:")
    print("   • Need validation? → PydanticOutputParser")
    print("   • Simple JSON? → JsonOutputParser")
    print("   • Just text? → StrOutputParser")
    print("   • Simple fields? → StructuredOutputParser")
    print("   • Lists? → CommaSeparatedListOutputParser")
    print()


def main():
    """Run all output parser examples"""
    
    print("\n" + "🔧" * 35)
    print("Welcome to Output Parsers - Universal Structured Output!")
    print("🔧" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        pydantic_output_parser()
        input("Press Enter to continue...")
        
        json_output_parser()
        input("Press Enter to continue...")
        
        structured_output_parser()
        input("Press Enter to continue...")
        
        string_output_parser()
        input("Press Enter to continue...")
        
        list_output_parser()
        input("Press Enter to continue...")
        
        datetime_output_parser()
        input("Press Enter to continue...")
        
        boolean_output_parser()
        input("Press Enter to continue...")
        
        enum_output_parser()
        input("Press Enter to continue...")
        
        comparing_parsers()
        
        print("=" * 70)
        print("✅ All Output Parser examples completed!")
        print("=" * 70)
        print("\n💡 Key Takeaways:")
        print("  ✓ Output parsers work with ANY model")
        print("  ✓ Inject format instructions into prompts")
        print("  ✓ PydanticOutputParser: Best for validation")
        print("  ✓ JsonOutputParser: Simple dict output")
        print("  ✓ StructuredOutputParser: Quick field extraction")
        print("  ✓ StrOutputParser: Clean text")
        print("  ✓ Specialized parsers: List, DateTime, Boolean, Enum")
        print("  ✓ Use chain pattern: prompt | llm | parser")
        print("\n📚 Next: Try 03_advanced_structured.py for advanced techniques!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
