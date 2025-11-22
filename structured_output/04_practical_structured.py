"""
🌟 Practical Structured Output Projects

Real-world projects demonstrating structured output:
1. Resume Parser - Extract structured data from resumes
2. Invoice Processor - Parse invoice details
3. Product Review Analyzer - Structured sentiment analysis
4. Meeting Notes Generator - Extract action items & decisions
5. Form Filler - Auto-fill forms from conversations
6. Data Migration Tool - Transform unstructured to structured

Production-ready examples!
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Load environment variables
load_dotenv()


def resume_parser():
    """Project 1: Resume Parser - Extract structured data"""
    
    print("=" * 70)
    print("📄 Project 1: Resume Parser")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Define resume structure
    class Experience(BaseModel):
        """Work experience"""
        company: str = Field(description="Company name")
        position: str = Field(description="Job title")
        duration: str = Field(description="Time period")
        responsibilities: List[str] = Field(description="Key responsibilities")
    
    class Education(BaseModel):
        """Education details"""
        degree: str = Field(description="Degree name")
        institution: str = Field(description="School/university")
        year: str = Field(description="Graduation year")
    
    class Resume(BaseModel):
        """Complete resume structure"""
        full_name: str = Field(description="Candidate's full name")
        email: str = Field(description="Email address")
        phone: str = Field(description="Phone number")
        summary: str = Field(description="Professional summary")
        skills: List[str] = Field(description="Technical skills")
        experience: List[Experience] = Field(description="Work experience")
        education: List[Education] = Field(description="Education history")
    
    parser = PydanticOutputParser(pydantic_object=Resume)
    
    template = """Extract ALL information from this resume into structured format.

{format_instructions}

RESUME:
{resume_text}

STRUCTURED OUTPUT:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["resume_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    resume_text = """
    JOHN SMITH
    john.smith@email.com | +1-555-0123
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 8 years of experience in full-stack development.
    Expert in Python, JavaScript, and cloud technologies.
    
    SKILLS
    Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL
    
    WORK EXPERIENCE
    
    Senior Software Engineer | Tech Corp | 2020 - Present
    - Led team of 5 developers building microservices architecture
    - Reduced deployment time by 60% using CI/CD automation
    - Mentored junior developers and conducted code reviews
    
    Software Engineer | StartupXYZ | 2016 - 2020
    - Developed RESTful APIs serving 1M+ daily requests
    - Implemented real-time features using WebSockets
    - Optimized database queries improving performance by 40%
    
    EDUCATION
    
    Bachelor of Science in Computer Science
    State University | 2016
    
    Master of Science in Software Engineering
    Tech Institute | 2018
    """
    
    print("\n📄 Parsing resume...")
    print(f"   Input: {len(resume_text)} characters")
    
    result = chain.invoke({"resume_text": resume_text})
    
    print("\n✅ Structured Resume Data:")
    print(f"\n👤 Personal Info:")
    print(f"   Name: {result.full_name}")
    print(f"   Email: {result.email}")
    print(f"   Phone: {result.phone}")
    
    print(f"\n💼 Summary:")
    print(f"   {result.summary[:80]}...")
    
    print(f"\n🛠️  Skills ({len(result.skills)}):")
    print(f"   {', '.join(result.skills[:5])}...")
    
    print(f"\n💼 Experience ({len(result.experience)} positions):")
    for exp in result.experience:
        print(f"   • {exp.position} at {exp.company}")
        print(f"     Duration: {exp.duration}")
        print(f"     Responsibilities: {len(exp.responsibilities)} items")
    
    print(f"\n🎓 Education ({len(result.education)} degrees):")
    for edu in result.education:
        print(f"   • {edu.degree}")
        print(f"     {edu.institution}, {edu.year}")
    
    print("\n💡 Use case: ATS systems, recruitment automation")
    print()


def invoice_processor():
    """Project 2: Invoice Processor - Parse invoice details"""
    
    print("=" * 70)
    print("🧾 Project 2: Invoice Processor")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class LineItem(BaseModel):
        """Invoice line item"""
        description: str
        quantity: int = Field(ge=1)
        unit_price: float = Field(ge=0)
        total: float = Field(ge=0)
    
    class Invoice(BaseModel):
        """Complete invoice"""
        invoice_number: str
        invoice_date: str
        vendor_name: str
        customer_name: str
        items: List[LineItem]
        subtotal: float = Field(ge=0)
        tax: float = Field(ge=0)
        total: float = Field(ge=0)
        payment_terms: str
    
    parser = PydanticOutputParser(pydantic_object=Invoice)
    
    template = """Extract invoice information into structured format.

{format_instructions}

INVOICE TEXT:
{invoice_text}

OUTPUT:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["invoice_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    invoice_text = """
    INVOICE
    
    Invoice #: INV-2024-001
    Date: March 15, 2024
    
    From: TechSupply Inc.
    To: ABC Corporation
    
    Items:
    1. Laptop Computer (x2) - $1,200.00 each = $2,400.00
    2. Wireless Mouse (x5) - $25.00 each = $125.00
    3. USB-C Cable (x10) - $15.00 each = $150.00
    
    Subtotal: $2,675.00
    Tax (8%): $214.00
    Total: $2,889.00
    
    Payment Terms: Net 30 days
    """
    
    print("\n🧾 Processing invoice...")
    
    result = chain.invoke({"invoice_text": invoice_text})
    
    print("\n✅ Structured Invoice Data:")
    print(f"\n📋 Invoice Details:")
    print(f"   Number: {result.invoice_number}")
    print(f"   Date: {result.invoice_date}")
    print(f"   Vendor: {result.vendor_name}")
    print(f"   Customer: {result.customer_name}")
    
    print(f"\n📦 Line Items ({len(result.items)}):")
    for i, item in enumerate(result.items, 1):
        print(f"   {i}. {item.description}")
        print(f"      Qty: {item.quantity} × ${item.unit_price:.2f} = ${item.total:.2f}")
    
    print(f"\n💰 Totals:")
    print(f"   Subtotal: ${result.subtotal:.2f}")
    print(f"   Tax: ${result.tax:.2f}")
    print(f"   Total: ${result.total:.2f}")
    print(f"   Terms: {result.payment_terms}")
    
    print("\n💡 Use case: Accounting automation, expense tracking")
    print()


def review_analyzer():
    """Project 3: Product Review Analyzer - Structured sentiment"""
    
    print("=" * 70)
    print("⭐ Project 3: Product Review Analyzer")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Sentiment(str, Enum):
        """Sentiment types"""
        POSITIVE = "positive"
        NEUTRAL = "neutral"
        NEGATIVE = "negative"
    
    class Aspect(BaseModel):
        """Product aspect rating"""
        aspect: str = Field(description="Feature/aspect name")
        sentiment: Sentiment = Field(description="Sentiment for this aspect")
        comment: str = Field(description="Specific comment about aspect")
    
    class ReviewAnalysis(BaseModel):
        """Complete review analysis"""
        overall_sentiment: Sentiment
        rating_estimate: int = Field(ge=1, le=5, description="Estimated rating 1-5")
        pros: List[str] = Field(description="Positive points")
        cons: List[str] = Field(description="Negative points")
        aspects: List[Aspect] = Field(description="Individual aspect analysis")
        summary: str = Field(description="Brief summary")
        would_recommend: bool = Field(description="Recommendation likelihood")
    
    parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)
    
    template = """Analyze this product review in detail.

{format_instructions}

REVIEW:
{review_text}

ANALYSIS:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["review_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    review_text = """
    I've been using this wireless headphones for 3 months now. The sound quality 
    is absolutely amazing - crystal clear with deep bass. Battery life is impressive,
    lasting about 30 hours on a single charge. The noise cancellation works great
    on flights.
    
    However, the build quality feels a bit cheap for the price. The headband creaks
    sometimes and the ear cups could be more comfortable for long sessions. Also,
    the Bluetooth connection occasionally drops when I'm far from my phone.
    
    Overall, great value for the sound quality, but don't expect premium build.
    I'd recommend for the audio enthusiasts on a budget.
    """
    
    print("\n⭐ Analyzing review...")
    
    result = chain.invoke({"review_text": review_text})
    
    sentiment_emoji = {
        "positive": "😊",
        "neutral": "😐",
        "negative": "😞"
    }
    
    print("\n✅ Structured Analysis:")
    print(f"\n📊 Overall:")
    print(f"   Sentiment: {result.overall_sentiment.value} {sentiment_emoji[result.overall_sentiment.value]}")
    print(f"   Rating: {'⭐' * result.rating_estimate} ({result.rating_estimate}/5)")
    print(f"   Would Recommend: {'✅ Yes' if result.would_recommend else '❌ No'}")
    
    print(f"\n✅ Pros ({len(result.pros)}):")
    for pro in result.pros:
        print(f"   • {pro}")
    
    print(f"\n❌ Cons ({len(result.cons)}):")
    for con in result.cons:
        print(f"   • {con}")
    
    print(f"\n🔍 Aspect Analysis ({len(result.aspects)}):")
    for aspect in result.aspects:
        emoji = sentiment_emoji[aspect.sentiment.value]
        print(f"   • {aspect.aspect}: {aspect.sentiment.value} {emoji}")
        print(f"     \"{aspect.comment}\"")
    
    print(f"\n📝 Summary:")
    print(f"   {result.summary}")
    
    print("\n💡 Use case: E-commerce, product insights, customer feedback")
    print()


def meeting_notes_generator():
    """Project 4: Meeting Notes - Extract action items & decisions"""
    
    print("=" * 70)
    print("📝 Project 4: Meeting Notes Generator")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Priority(str, Enum):
        """Priority levels"""
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
    
    class ActionItem(BaseModel):
        """Action item from meeting"""
        task: str = Field(description="Task description")
        assignee: str = Field(description="Person responsible")
        deadline: Optional[str] = Field(description="Due date if mentioned")
        priority: Priority = Field(description="Task priority")
    
    class Decision(BaseModel):
        """Decision made in meeting"""
        decision: str = Field(description="What was decided")
        rationale: str = Field(description="Why this decision")
    
    class MeetingNotes(BaseModel):
        """Structured meeting notes"""
        meeting_title: str
        date: str
        attendees: List[str]
        key_topics: List[str] = Field(description="Main topics discussed")
        decisions: List[Decision] = Field(description="Decisions made")
        action_items: List[ActionItem] = Field(description="Tasks assigned")
        next_meeting: Optional[str] = Field(description="Next meeting date")
    
    parser = PydanticOutputParser(pydantic_object=MeetingNotes)
    
    template = """Extract structured information from meeting transcript.

{format_instructions}

MEETING TRANSCRIPT:
{transcript}

STRUCTURED NOTES:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["transcript"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    transcript = """
    Product Planning Meeting - March 15, 2024
    
    Attendees: Sarah (PM), John (Dev Lead), Emily (Designer), Mike (QA)
    
    Sarah: Let's discuss the new dashboard feature. We've had user requests.
    
    Emily: I've completed the mockups. Users want dark mode and customizable widgets.
    
    John: Dark mode is straightforward. Custom widgets need 3 weeks development time.
    
    Mike: We should prioritize dark mode first, it's highly requested.
    
    DECISION: Implement dark mode in Sprint 12, defer custom widgets to Sprint 13.
    Rationale: Dark mode has more user demand and faster implementation.
    
    Sarah: John, can you start dark mode implementation next week?
    John: Yes, I'll have it ready by March 30th.
    
    Sarah: Emily, please finalize widget designs by March 25th for Sprint 13.
    Emily: Will do.
    
    Mike: I'll prepare test cases for dark mode this week.
    
    Next meeting: March 22nd to review progress.
    """
    
    print("\n📝 Processing meeting transcript...")
    
    result = chain.invoke({"transcript": transcript})
    
    print("\n✅ Structured Meeting Notes:")
    print(f"\n📅 Meeting Info:")
    print(f"   Title: {result.meeting_title}")
    print(f"   Date: {result.date}")
    print(f"   Attendees: {', '.join(result.attendees)}")
    
    print(f"\n🎯 Key Topics ({len(result.key_topics)}):")
    for topic in result.key_topics:
        print(f"   • {topic}")
    
    print(f"\n✅ Decisions Made ({len(result.decisions)}):")
    for i, decision in enumerate(result.decisions, 1):
        print(f"   {i}. {decision.decision}")
        print(f"      Rationale: {decision.rationale}")
    
    print(f"\n📋 Action Items ({len(result.action_items)}):")
    for item in result.action_items:
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        emoji = priority_emoji[item.priority.value]
        print(f"   {emoji} {item.task}")
        print(f"      Assignee: {item.assignee}")
        if item.deadline:
            print(f"      Deadline: {item.deadline}")
    
    if result.next_meeting:
        print(f"\n📅 Next Meeting: {result.next_meeting}")
    
    print("\n💡 Use case: Meeting automation, team collaboration")
    print()


def form_filler():
    """Project 5: Auto Form Filler - Extract from conversation"""
    
    print("=" * 70)
    print("📋 Project 5: Auto Form Filler")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class FormData(BaseModel):
        """Contact form data"""
        first_name: str
        last_name: str
        email: str
        phone: str
        company: Optional[str]
        job_title: Optional[str]
        interest: str = Field(description="Product/service of interest")
        message: str = Field(description="User's message")
        preferred_contact: str = Field(description="email or phone")
    
    parser = PydanticOutputParser(pydantic_object=FormData)
    
    template = """Extract information from conversation to fill contact form.

{format_instructions}

CONVERSATION:
{conversation}

FORM DATA:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["conversation"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    conversation = """
    Bot: Hi! How can I help you today?
    
    User: I'm interested in your enterprise software solution.
    
    Bot: Great! May I have your name?
    
    User: Sure, I'm Michael Thompson.
    
    Bot: Thanks Michael! And your email address?
    
    User: michael.thompson@techcorp.com
    
    Bot: Perfect. Phone number?
    
    User: +1-555-0199
    
    Bot: Are you currently working with a company?
    
    User: Yes, I'm the CTO at TechCorp Industries.
    
    Bot: Excellent! What specific features are you interested in?
    
    User: We need better team collaboration tools and project management features.
    We have a team of 50 people and struggling with coordination.
    
    Bot: How would you prefer we contact you?
    
    User: Email is best for me.
    """
    
    print("\n📋 Extracting form data from conversation...")
    
    result = chain.invoke({"conversation": conversation})
    
    print("\n✅ Auto-Filled Form:")
    print(f"\n👤 Personal Information:")
    print(f"   First Name: {result.first_name}")
    print(f"   Last Name: {result.last_name}")
    print(f"   Email: {result.email}")
    print(f"   Phone: {result.phone}")
    
    print(f"\n🏢 Professional Information:")
    if result.company:
        print(f"   Company: {result.company}")
    if result.job_title:
        print(f"   Job Title: {result.job_title}")
    
    print(f"\n📝 Inquiry Details:")
    print(f"   Interest: {result.interest}")
    print(f"   Message: {result.message}")
    print(f"   Preferred Contact: {result.preferred_contact}")
    
    print("\n💡 Use case: Lead generation, chatbot integration")
    print()


def data_migration():
    """Project 6: Data Migration - Transform unstructured to structured"""
    
    print("=" * 70)
    print("🔄 Project 6: Data Migration Tool")
    print("=" * 70)
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    class Address(BaseModel):
        """Structured address"""
        street: str
        city: str
        state: str
        zip_code: str
        country: str
    
    class CustomerRecord(BaseModel):
        """New database schema"""
        customer_id: str
        first_name: str
        last_name: str
        email: str
        phone: str
        address: Address
        account_status: str = Field(description="active or inactive")
        join_date: str
        notes: Optional[str]
    
    parser = PydanticOutputParser(pydantic_object=CustomerRecord)
    
    template = """Transform legacy data into new structured format.

{format_instructions}

LEGACY DATA:
{legacy_data}

NEW FORMAT:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["legacy_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | chat | parser
    
    # Simulate legacy unstructured data
    legacy_records = [
        """
        ID: CUST-001
        Name: Jennifer Williams
        Contact: jennifer.w@email.com / 555-0145
        Location: 123 Main St, Springfield, IL 62701, USA
        Status: Active customer since 2022-01-15
        Note: VIP customer, prefers email communication
        """,
        """
        ID: CUST-002
        Name: Robert Chen
        Contact: robert.chen@company.com / 555-0198
        Location: 456 Oak Ave, Chicago, IL 60601, United States
        Status: Account active, joined 2023-03-20
        """
    ]
    
    print("\n🔄 Migrating legacy data...")
    
    migrated_records = []
    
    for i, legacy_data in enumerate(legacy_records, 1):
        print(f"\n   Processing record {i}...")
        
        result = chain.invoke({"legacy_data": legacy_data})
        migrated_records.append(result)
        
        print(f"   ✓ Migrated: {result.first_name} {result.last_name}")
    
    print("\n✅ Migration Complete!")
    print(f"\n📊 Migrated {len(migrated_records)} records:\n")
    
    for record in migrated_records:
        print(f"   Customer: {record.customer_id}")
        print(f"   Name: {record.first_name} {record.last_name}")
        print(f"   Email: {record.email}")
        print(f"   Phone: {record.phone}")
        print(f"   Address: {record.address.street}, {record.address.city}, {record.address.state}")
        print(f"   Status: {record.account_status} (since {record.join_date})")
        if record.notes:
            print(f"   Notes: {record.notes}")
        print()
    
    print("💡 Use case: Database migration, ETL pipelines, data cleanup")
    print()


def main():
    """Run all practical projects"""
    
    print("\n" + "🌟" * 35)
    print("Welcome to Practical Structured Output Projects!")
    print("🌟" * 35 + "\n")
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        return
    
    try:
        resume_parser()
        input("Press Enter to continue...")
        
        invoice_processor()
        input("Press Enter to continue...")
        
        review_analyzer()
        input("Press Enter to continue...")
        
        meeting_notes_generator()
        input("Press Enter to continue...")
        
        form_filler()
        input("Press Enter to continue...")
        
        data_migration()
        
        print("=" * 70)
        print("✅ All Practical Projects completed!")
        print("=" * 70)
        print("\n🎯 Real-World Applications:")
        print("  ✓ Resume Parser → Recruitment automation")
        print("  ✓ Invoice Processor → Accounting systems")
        print("  ✓ Review Analyzer → Product insights")
        print("  ✓ Meeting Notes → Team collaboration")
        print("  ✓ Form Filler → Lead generation")
        print("  ✓ Data Migration → ETL pipelines")
        print("\n💡 These patterns apply to:")
        print("  • Document processing")
        print("  • Data extraction")
        print("  • Business automation")
        print("  • Integration pipelines")
        print("  • Analytics platforms")
        print("\n🎓 You've mastered structured output in LangChain!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
