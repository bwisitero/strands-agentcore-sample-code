"""
Demo 14: Document Processing Pipeline
Goal: Upload PDFs/documents, extract information, and answer questions

Key Teaching Points:
- Document parsing and text extraction
- Building a document knowledge base
- Question answering over documents
- Practical use cases: contract analysis, research assistants, document QA
"""

import os
from pathlib import Path
from typing import List, Dict
from strands import Agent, tool
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Global document store (in production, use a database)
DOCUMENT_STORE = []


class DocumentProcessor:
    """Handles document processing and knowledge base creation."""

    def __init__(self, docs_folder: str = "documents"):
        self.docs_folder = docs_folder
        self.documents = []
        Path(docs_folder).mkdir(exist_ok=True)

    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error extracting TXT: {str(e)}"

    def process_document(self, file_path: str) -> Dict:
        """Process a document and extract its content."""
        file_ext = Path(file_path).suffix.lower()
        file_name = Path(file_path).name

        if file_ext == '.txt':
            content = self.extract_text_from_txt(file_path)
        else:
            content = f"Unsupported file type: {file_ext}. Only .txt files are supported in this demo."

        return {
            "content": content,
            "metadata": {
                "filename": file_name,
                "file_type": file_ext,
                "file_path": file_path
            }
        }

    def process_all_documents(self) -> List[Dict]:
        """Process all documents in the documents folder."""
        global DOCUMENT_STORE
        documents = []

        for file_path in Path(self.docs_folder).glob('*.txt'):
            if file_path.is_file():
                doc = self.process_document(str(file_path))
                documents.append(doc)
                print(f"✅ Processed: {file_path.name}")

        self.documents = documents
        DOCUMENT_STORE = documents
        return documents


# Create sample documents for demo
def create_sample_documents():
    """Create sample documents for demonstration."""
    docs_folder = Path("documents")
    docs_folder.mkdir(exist_ok=True)

    # Sample 1: Employment Contract
    contract = """
EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on October 1, 2025,
between TechCorp Inc. ("Company") and John Smith ("Employee").

1. POSITION AND DUTIES
Employee shall serve as Senior Software Engineer, reporting to the CTO.

2. COMPENSATION
Base Salary: $150,000 per year, paid bi-weekly
Annual Bonus: Up to 20% of base salary based on performance
Stock Options: 10,000 shares vesting over 4 years

3. BENEFITS
- Health Insurance: Company covers 100% of employee premium
- Vacation: 20 days paid time off per year
- 401(k): Company matches up to 6% of salary

4. WORK SCHEDULE
Employee will work remotely with core hours 10 AM - 3 PM EST.
Occasional travel may be required (< 10% of time).

5. TERMINATION
Either party may terminate this agreement with 30 days written notice.

6. CONFIDENTIALITY
Employee agrees to maintain confidentiality of all proprietary information.

Signed: October 1, 2025
    """

    # Sample 2: Product Requirements Document
    prd = """
PRODUCT REQUIREMENTS DOCUMENT

Product: AI-Powered Customer Support Chatbot
Version: 1.0
Date: October 5, 2025

1. OVERVIEW
Build an AI chatbot to handle tier-1 customer support queries, reducing
response time by 80% and support costs by 50%.

2. TARGET USERS
- Customers seeking product information
- Users with billing questions
- Technical support inquiries (basic level)

3. KEY FEATURES
a) Natural Language Understanding
   - Support for English, Spanish, French
   - Intent classification accuracy > 95%

b) Knowledge Base Integration
   - Connect to product documentation
   - Real-time inventory checks
   - Order status tracking

c) Escalation System
   - Auto-escalate complex issues to human agents
   - Smart routing based on issue type

d) Analytics Dashboard
   - Response time metrics
   - Customer satisfaction scores
   - Cost savings analysis

4. TECHNICAL REQUIREMENTS
- Response time: < 2 seconds
- Uptime: 99.9% SLA
- Concurrent users: Support 1000+ simultaneous conversations
- Security: SOC 2 compliant

5. SUCCESS METRICS
- 80% of tier-1 queries resolved without human intervention
- Customer satisfaction score > 4.5/5
- Average resolution time < 3 minutes

6. TIMELINE
Phase 1 (MVP): 8 weeks
Phase 2 (Full features): 16 weeks
    """

    # Sample 3: Research Paper Abstract
    research = """
RESEARCH PAPER: Advances in Retrieval-Augmented Generation

Abstract

Retrieval-Augmented Generation (RAG) has emerged as a powerful technique for
enhancing large language models with external knowledge. This paper presents
a comprehensive analysis of RAG architectures and their applications.

Introduction

Traditional language models are limited by their training data cutoff and
inability to access real-time information. RAG addresses these limitations
by combining retrieval systems with generative models.

Methodology

We evaluated 5 different RAG architectures across 3 benchmark datasets:
1. Naive RAG: Simple retrieval + generation
2. Advanced RAG: With query rewriting and re-ranking
3. Modular RAG: Specialized retrievers for different content types
4. Agentic RAG: Autonomous decision-making for retrieval
5. Self-RAG: Self-reflection and critique mechanisms

Results

Our experiments show that Agentic RAG achieves:
- 23% improvement in answer accuracy over naive RAG
- 35% reduction in hallucination rate
- 2.1x faster response time with caching

Key findings:
- Query rewriting improves retrieval precision by 18%
- Hybrid search (dense + sparse) outperforms single method by 15%
- Self-reflection reduces factual errors by 40%

Conclusion

Agentic RAG represents the next evolution in knowledge-augmented AI systems,
providing more accurate, reliable, and contextually relevant responses.

Keywords: RAG, LLM, Information Retrieval, Natural Language Processing
    """

    # Write sample documents
    (docs_folder / "employment_contract.txt").write_text(contract)
    (docs_folder / "product_requirements.txt").write_text(prd)
    (docs_folder / "research_paper.txt").write_text(research)

    print("📄 Created sample documents in 'documents/' folder")


# Tools for document management
@tool
def list_documents() -> str:
    """List all available documents in the knowledge base."""
    processor = DocumentProcessor()
    docs_folder = Path(processor.docs_folder)

    if not docs_folder.exists():
        return "No documents folder found."

    files = list(docs_folder.glob('*'))
    if not files:
        return "No documents found."

    file_list = []
    for file in files:
        if file.is_file():
            file_list.append(f"- {file.name} ({file.suffix})")

    return "Available documents:\n" + "\n".join(file_list)


@tool
def get_document_summary(filename: str) -> str:
    """Get a summary of a specific document by filename."""
    processor = DocumentProcessor()
    file_path = Path(processor.docs_folder) / filename

    if not file_path.exists():
        return f"Document '{filename}' not found."

    doc = processor.process_document(str(file_path))
    content = doc['content']

    # Return first 500 characters as summary
    summary = content[:500] + "..." if len(content) > 500 else content
    return f"Document: {filename}\n\n{summary}"


@tool
def search_documents(query: str) -> str:
    """Search through all documents for information relevant to the query."""
    global DOCUMENT_STORE

    if not DOCUMENT_STORE:
        return "No documents have been loaded yet."

    query_lower = query.lower()
    results = []

    for doc in DOCUMENT_STORE:
        content = doc['content'].lower()
        filename = doc['metadata']['filename']

        # Simple keyword search
        if any(word in content for word in query_lower.split()):
            # Find relevant excerpt
            lines = doc['content'].split('\n')
            relevant_lines = []
            for line in lines:
                if any(word in line.lower() for word in query_lower.split()):
                    relevant_lines.append(line)

            if relevant_lines:
                excerpt = '\n'.join(relevant_lines[:5])  # First 5 matching lines
                results.append(f"From {filename}:\n{excerpt}\n")

    if not results:
        return f"No relevant information found for: {query}"

    return "\n---\n".join(results)


def main():
    """Run the document processing pipeline demo."""
    print("=" * 70)
    print("📚 Document Processing Pipeline Demo")
    print("=" * 70)
    print()

    # Create sample documents
    create_sample_documents()
    print()

    # Process documents
    processor = DocumentProcessor()
    documents = processor.process_all_documents()
    print(f"\n✅ Processed {len(documents)} documents\n")

    # Create document QA agent with tools
    doc_agent = Agent(
        tools=[list_documents, get_document_summary, search_documents],
        system_prompt="""You are a document analysis assistant. You help users extract
        information from documents and answer questions based on their content.

        When answering questions:
        1. Use search_documents to find relevant information from the documents
        2. Use get_document_summary to get details about specific documents
        3. Cite specific documents when providing answers
        4. If information spans multiple documents, synthesize the information
        5. Be specific and quote relevant sections when helpful
        """
    )

    # Example queries
    queries = [
        "What documents are available?",
        "What is John Smith's base salary according to the employment contract?",
        "What are the key features of the AI chatbot product?",
        "What is the main finding of the RAG research paper?",
        "Compare the vacation policy with the product timeline",
        "What are the success metrics for the chatbot project?",
    ]

    print("🤖 Document Q&A Agent Ready!\n")
    print("=" * 70)

    for i, query in enumerate(queries, 1):
        print(f"\n❓ Question {i}: {query}")
        print("-" * 70)
        response = doc_agent(query)
        print(f"💡 Answer: {response}\n")

    print("=" * 70)
    print("✨ Demo complete!")
    print("\nTry your own questions by running:")
    print("  python -c \"from demo_14_document_processing import doc_agent;")
    print("  print(doc_agent('Your question here'))\"")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add python-dotenv

2. Run the demo:
   python demo_14_document_processing.py

3. The demo will:
   - Create sample documents (contract, PRD, research paper)
   - Process and extract text from all TXT documents
   - Build a searchable document store
   - Answer questions about the documents

4. Add your own documents:
   - Place TXT files in the 'documents/' folder
   - Re-run the script to process them

Features Demonstrated:
- Text file document parsing
- Document search using tools
- Natural language Q&A over documents
- Document citation and reference
- Cross-document information synthesis
- Simple RAG pattern implementation

Use Cases:
- Contract analysis and review
- Research paper Q&A
- Product documentation search
- Legal document review
- Academic research assistant
- Technical documentation helper

Example Questions:
- "What are the compensation details in the employment contract?"
- "Summarize the key technical requirements for the chatbot"
- "What methodology was used in the research paper?"
- "What are the termination conditions?"
- "Compare timeline and success metrics"

Production Enhancements:
- Add support for more formats (PDF, DOCX, PPTX with proper libraries)
- Implement semantic search with embeddings
- Add metadata extraction (dates, entities, key terms)
- Build document comparison and diff tools
- Add support for structured data extraction
- Implement document classification
- Add version control for documents
- Create export functionality (summaries, reports)

Note: This demo uses a simple keyword-based search. For production,
consider using vector embeddings for semantic search.
"""


"""Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_14_document_processing.py
======================================================================
📚 Document Processing Pipeline Demo
======================================================================

📄 Created sample documents in 'documents/' folder

✅ Processed: research_paper.txt
✅ Processed: product_requirements.txt
✅ Processed: employment_contract.txt

✅ Processed 3 documents

🤖 Document Q&A Agent Ready!

======================================================================

❓ Question 1: What documents are available?
----------------------------------------------------------------------
I'll check what documents are available in the knowledge base for you.
Tool #1: list_documents
There are 3 documents available in the knowledge base:

1. **research_paper.txt** - A text document
2. **product_requirements.txt** - A text document  
3. **employment_contract.txt** - A text document

Would you like me to get a summary of any of these documents or search for specific information within them?💡 Answer: There are 3 documents available in the knowledge base:

1. **research_paper.txt** - A text document
2. **product_requirements.txt** - A text document  
3. **employment_contract.txt** - A text document

Would you like me to get a summary of any of these documents or search for specific information within them?



❓ Question 2: What is John Smith's base salary according to the employment contract?
----------------------------------------------------------------------
I'll search for John Smith's base salary information in the employment contract document.
Tool #2: search_documents
According to the employment contract document, **John Smith's base salary is $150,000 per year**, paid bi-weekly.

The contract also mentions that he is eligible for an annual bonus of up to 20% of his base salary based on performance, which would be up to $30,000 additional per year.💡 Answer: According to the employment contract document, **John Smith's base salary is $150,000 per year**, paid bi-weekly.

The contract also mentions that he is eligible for an annual bonus of up to 20% of his base salary based on performance, which would be up to $30,000 additional per year.



❓ Question 3: What are the key features of the AI chatbot product?
----------------------------------------------------------------------
I'll search for information about the AI chatbot product features in the documents.
Tool #3: search_documents
Let me get more specific information about the key features by searching more directly for the features section.
Tool #4: search_documents
Let me get the full document summary for the product requirements to see all the key features.
Tool #5: get_document_summary
Let me search for more specific details about the key features.
Tool #6: search_documents
Let me search for more complete feature information.
Tool #7: search_documents
Based on the product requirements document, here are the **key features of the AI chatbot product**:

## Key Features

**a) Natural Language Understanding**
- Support for multiple languages: English, Spanish, and French
- Intent classification with >95% accuracy

**b) Knowledge Base Integration** 
- Smart routing based on issue type

## Product Goals
The AI-powered customer support chatbot is designed to:
- Handle tier-1 customer support queries
- Reduce response time by 80%
- Reduce support costs by 50%

## Target Users
- Customers seeking product information
- Users with billing questions  
- Technical support inquiries (basic level)

The document appears to contain additional features, but the search results show partial information. The chatbot is specifically focused on automating basic customer support interactions with high accuracy natural language processing capabilities.💡 Answer: Based on the product requirements document, here are the **key features of the AI chatbot product**:

## Key Features

**a) Natural Language Understanding**
- Support for multiple languages: English, Spanish, and French
- Intent classification with >95% accuracy

**b) Knowledge Base Integration** 
- Smart routing based on issue type

## Product Goals
The AI-powered customer support chatbot is designed to:
- Handle tier-1 customer support queries
- Reduce response time by 80%
- Reduce support costs by 50%

## Target Users
- Customers seeking product information
- Users with billing questions  
- Technical support inquiries (basic level)

The document appears to contain additional features, but the search results show partial information. The chatbot is specifically focused on automating basic customer support interactions with high accuracy natural language processing capabilities.



❓ Question 4: What is the main finding of the RAG research paper?
----------------------------------------------------------------------
I'll search for the main findings of the RAG research paper.
Tool #8: search_documents
Let me search more specifically for the key findings and results.
Tool #9: search_documents
Let me get the full summary of the research paper to see the complete findings.
Tool #10: get_document_summary
Let me search for specific performance improvements and results.
Tool #11: search_documents
Let me search for the evaluation results and performance metrics.
Tool #12: search_documents
Let me try a different search to find the specific results and conclusions.
Tool #13: search_documents
Based on the research paper about "Advances in Retrieval-Augmented Generation," here are the **main findings**:

## Key Research Focus
The paper presents **a comprehensive analysis of RAG architectures and their applications**, focusing on how Retrieval-Augmented Generation enhances large language models with external knowledge.

## Problem Addressed
The research tackles the fundamental limitations of traditional language models:
- Limited by their training data cutoff
- Inability to access real-time information

## Methodology 
The researchers **evaluated 5 different RAG architectures across 3 benchmark datasets**, including:
1. **Naive RAG**: Simple retrieval + generation approach

## Main Finding
The paper shows that **RAG addresses the limitations** of traditional language models by combining retrieval systems with generation capabilities, representing **"the next evolution in knowledge-augmented AI systems."**

The research demonstrates significant improvements, with mentions of enhanced answer accuracy compared to baseline approaches, particularly showing the evolution from basic naive RAG to more sophisticated agentic RAG systems.

The paper appears to be focused on advancing the field of Natural Language Processing and Information Retrieval through improved RAG architectures.💡 Answer: Based on the research paper about "Advances in Retrieval-Augmented Generation," here are the **main findings**:

## Key Research Focus
The paper presents **a comprehensive analysis of RAG architectures and their applications**, focusing on how Retrieval-Augmented Generation enhances large language models with external knowledge.

## Problem Addressed
The research tackles the fundamental limitations of traditional language models:
- Limited by their training data cutoff
- Inability to access real-time information

## Methodology 
The researchers **evaluated 5 different RAG architectures across 3 benchmark datasets**, including:
1. **Naive RAG**: Simple retrieval + generation approach

## Main Finding
The paper shows that **RAG addresses the limitations** of traditional language models by combining retrieval systems with generation capabilities, representing **"the next evolution in knowledge-augmented AI systems."**

The research demonstrates significant improvements, with mentions of enhanced answer accuracy compared to baseline approaches, particularly showing the evolution from basic naive RAG to more sophisticated agentic RAG systems.

The paper appears to be focused on advancing the field of Natural Language Processing and Information Retrieval through improved RAG architectures.



❓ Question 5: Compare the vacation policy with the product timeline
----------------------------------------------------------------------
I'll search for information about the vacation policy and product timeline to compare them.
Tool #14: search_documents
Now let me search for product timeline information.
Tool #15: search_documents
Let me get more specific details about the timeline and work schedule.
Tool #16: search_documents
Let me search for more detailed timeline information from the product requirements.
Tool #17: search_documents
Let me try to get the full timeline section from the product requirements document.
Tool #18: search_documents
Based on my searches, I can compare the information I found about the vacation policy and what's available about timing/schedule:

## Vacation Policy vs Product Timeline Comparison

### Vacation Policy (from Employment Contract)
- **20 days paid time off per year** for John Smith
- This provides approximately 4 weeks of vacation annually

### Product Schedule Information
From the available information, I found:
- **Product Requirements Document dated**: October 5, 2025
- **Employment Contract dated**: October 1, 2025
- **Work Schedule**: Employee works remotely with core hours 10 AM - 3 PM EST

However, I was unable to find detailed information about the specific product development timeline phases in the search results. The document references show there is a "6. TIMELINE" section in the product requirements, but the detailed timeline phases and dates aren't appearing in my searches.

**To provide a complete comparison**, I would need to access more specific details about the product timeline phases, development milestones, and launch dates. Could you help me search for more specific timeline information, or would you like me to try a different search approach to find the product development schedule details?💡 Answer: Based on my searches, I can compare the information I found about the vacation policy and what's available about timing/schedule:

## Vacation Policy vs Product Timeline Comparison

### Vacation Policy (from Employment Contract)
- **20 days paid time off per year** for John Smith
- This provides approximately 4 weeks of vacation annually

### Product Schedule Information
From the available information, I found:
- **Product Requirements Document dated**: October 5, 2025
- **Employment Contract dated**: October 1, 2025
- **Work Schedule**: Employee works remotely with core hours 10 AM - 3 PM EST

However, I was unable to find detailed information about the specific product development timeline phases in the search results. The document references show there is a "6. TIMELINE" section in the product requirements, but the detailed timeline phases and dates aren't appearing in my searches.

**To provide a complete comparison**, I would need to access more specific details about the product timeline phases, development milestones, and launch dates. Could you help me search for more specific timeline information, or would you like me to try a different search approach to find the product development schedule details?



❓ Question 6: What are the success metrics for the chatbot project?
----------------------------------------------------------------------
I'll search for the success metrics and performance indicators for the chatbot project.
Tool #19: search_documents
Let me search for more specific details about the success metrics section.
Tool #20: search_documents
Let me search for more comprehensive metrics including uptime and other KPIs.
Tool #21: search_documents
Let me search for customer satisfaction and other business metrics.
Tool #22: search_documents
Based on the product requirements document, here are the **success metrics for the chatbot project**:

## Primary Success Metrics

### Performance Targets
- **Response Time**: < 2 seconds per query
- **Average Resolution Time**: < 3 minutes
- **System Uptime**: 99.9% SLA (Service Level Agreement)

### Business Impact Goals
- **Response Time Improvement**: 80% reduction in response time
- **Cost Reduction**: 50% reduction in support costs

### Technical Performance Metrics
- **Intent Classification Accuracy**: > 95%
- **Real-time Inventory Checks**: Available for product inquiries

### Measurement Areas
- **Response Time Metrics**: Tracking query response speed
- **Customer Satisfaction Scores**: Measuring user experience
- **Cost Savings Analysis**: Monitoring operational cost reductions

## Overall Project Objective
The chatbot is designed to **handle tier-1 customer support queries** effectively, focusing on:
- Product information requests
- Basic billing questions  
- Basic technical support inquiries

These metrics collectively aim to demonstrate the chatbot's effectiveness in automating customer support while maintaining high quality service standards and achieving significant operational improvements.💡 Answer: Based on the product requirements document, here are the **success metrics for the chatbot project**:

## Primary Success Metrics

### Performance Targets
- **Response Time**: < 2 seconds per query
- **Average Resolution Time**: < 3 minutes
- **System Uptime**: 99.9% SLA (Service Level Agreement)

### Business Impact Goals
- **Response Time Improvement**: 80% reduction in response time
- **Cost Reduction**: 50% reduction in support costs

### Technical Performance Metrics
- **Intent Classification Accuracy**: > 95%
- **Real-time Inventory Checks**: Available for product inquiries

### Measurement Areas
- **Response Time Metrics**: Tracking query response speed
- **Customer Satisfaction Scores**: Measuring user experience
- **Cost Savings Analysis**: Monitoring operational cost reductions

## Overall Project Objective
The chatbot is designed to **handle tier-1 customer support queries** effectively, focusing on:
- Product information requests
- Basic billing questions  
- Basic technical support inquiries

These metrics collectively aim to demonstrate the chatbot's effectiveness in automating customer support while maintaining high quality service standards and achieving significant operational improvements.


======================================================================
✨ Demo complete!

Try your own questions by running:
  python -c "from demo_14_document_processing import doc_agent;
  print(doc_agent('Your question here'))"
======================================================================

"""