"""
Demo 4: Multi-Agent System (10 min)
Goal: Build a research + writer agent team

Key Teaching Points:
- Creating specialist agents for different tasks
- Converting agents to tools for orchestration
- Coordinating multiple agents with an orchestrator
"""
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands_tools import retrieve
from strands_tools.tavily import tavily_search

# for tavily_search,  signup for an apikey at https://app.tavily.com
# and set the environment variable TAVILY_API_KEY to your api key in the .env file
tavily_search.api_key = os.getenv("TAVILY_API_KEY")

# Load environment variables
load_dotenv()

# Specialist Agent 1: Research Agent
research_agent = Agent(
    tools=[tavily_search, retrieve],
    system_prompt="""You are a research specialist.
    Your job is to find accurate, up-to-date information."""
)

# Specialist Agent 2: Content Writer
writer_agent = Agent(
    system_prompt="""You are a technical writer.
    Create clear, engaging content based on research provided."""
)

# Convert specialist agents to tools
@tool
def research_assistant(query: str) -> str:
    """Research agent that finds information."""
    return research_agent(query)

@tool
def writing_assistant(content: str, style: str = "technical") -> str:
    """Writing agent that creates content."""
    prompt = f"Write in {style} style about: {content}"
    return writer_agent(prompt)

# Orchestrator agent
orchestrator = Agent(
    tools=[research_assistant, writing_assistant],
    system_prompt="""You coordinate research and writing tasks.
    First research, then create content based on findings."""
)

# Demo the multi-agent system
result = orchestrator(
    "Create a technical blog post about the latest advances in RAG systems"
)

print(result)


"""
Sample output:

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_4_multi_agent.py
I'll help you create a technical blog post about the latest advances in RAG (Retrieval-Augmented Generation) systems. Let me first research the current state of RAG technology and recent developments.
Tool #1: research_assistant
I'll search for the latest advances in RAG (Retrieval Augmented Generation) systems in 2024 to provide you with current information on improvements and techniques.
Tool #1: tavily_search
╭───────────────────────────────────────────────────────────────────────── Tavily Search Results ──────────────────────────────────────────────────────────────────────────╮
│ Query: latest advances RAG systems 2024 retrieval augmented generation improvements techniques                                                                           │
│                                                                                                                                                                          │
│ Answer: Retrieval-Augmented Generation (RAG) systems have seen significant advancements in 2024 and 2025, with a focus on improving efficiency, relevance, and           │
│ adaptability. Key developments include the introduction of graph-based approaches like GraphRAG and KRAGEN, which leverage knowledge graphs to enhance query             │
│ decomposition and retrieval. Multi-modal RAG systems have emerged, capable of processing and generating content across text, images, and other data types. Hybrid        │
│ retrieval strategies combining vector search, sparse vector search, and full-text search have shown improved recall and precision. Techniques like CRAG (Corrective      │
│ Retrieval Augmented Generation) and SELF-ROUTE have been implemented to improve robustness and dynamic task routing. The industry has shifted towards building           │
│ production-ready, scalable RAG systems, with increased emphasis on metadata utilization, knowledge graph integration, and adaptive retrieval mechanisms. These           │
│ advancements have collectively enhanced the accuracy, relevance, and real-world applicability of RAG systems across various domains and enterprise applications.         │
│                                                                                                                                                                          │
│ Results: 10 found                                                                                                                                                        │
│ --------------------------------------------------                                                                                                                       │
│                                                                                                                                                                          │
│ [1] Retrieval-Augmented Generation: A Comprehensive ...                                                                                                                  │
│ URL: https://arxiv.org/html/2506.00054v1                                                                                                                                 │
│ Score: 0.8018276                                                                                                                                                         │
│ Content: uses a generative LLM to autoregressively formulate complex multi-hop queries. RAG-Fusion (Rackauckas, 2024) further improves recall by combining results from  │
│ multiple reformulated queries through reciprocal rank fusion (Cormack et al., 2009). Structured approaches have also emerged: KRAGEN (Knowledge Retrieval Augmented      │
│ Generation ENgine) (Matsumoto et al., 2024) introduces graph-of-thoughts prompting to decompose complex queries into subproblems, retrieving relevant subgraphs to guide │
│ [...] In a complementary direction, Doan et al. (Doan et al., 2024) propose a lightweight hybrid retrieval strategy that combines unstructured text embeddings with      │
│ structured knowledge graph embeddings without requiring complex retriever re-training, achieving up to 13.1% improvements in retrieval correctness and ranking precision │
│ in domain-specific RAG deployments.                                                                                                                                      │
│                                                                                                                                                                          │
│ ### 4.2. Enhancing Context Relevance through Filtering [...] low-confidence predictions during sentence generation. SELF-ROUTE (Li et al., 2024) dynamically routes      │
│ tasks between retrieval and generation modules based on model self-assessed difficulty, and AU-RAG (Jang and Li, 2024) leverages agentic decision-making to mediate      │
│ between diverse retrieval sources and procedural knowledge. TA-ARE (Time-Aware Adaptive REtrieval) (Zhang et al., 2024) introduces a retrieval trigger classifier that   │
│ adaptively determines when retrieval is necessary and adjusts the                                                                                                        │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [2] Top 5 Trends in Enterprise RAG                                                                                                                                       │
│ URL: https://www.tonic.ai/guides/enterprise-rag                                                                                                                          │
│ Score: 0.76888984                                                                                                                                                        │
│ Content: With advancements in LLM technology and growing industry adoption, 2024 marks a pivotal year for RAG systems. As businesses and organizations move beyond the   │
│ initial hype and delve into practical applications, the focus shifts towards building reliable and scalable RAGs that can deliver real-world value. This trend           │
│ emphasizes the need for tools and methodologies that bridge the gap between research and deployment, ensuring RAG systems can live up to their transformative potential. │
│ [...] Facebook logo                                                                                                                                                      │
│                                                                                                                                                                          │
│ Large language models (LLM) are revolutionizing numerous industries. However, for LLMs to deliver real-world value, we need robust and adaptable generative systems      │
│ capable of leveraging proprietary information––enter retrieval-augmented generation (RAG) systems. This post explores the top 5 trends that will be crucial for building │
│ successful enterprise RAG systems in 2024, propelling them to the forefront of AI innovation.                                                                            │
│                                                                                                                                                                          │
│ ## 1. Building production-ready RAGs [...] As the complexity of data and user queries grows in 2024, relying solely on basic vector similarity search becomes            │
│ increasingly insufficient. The use of metadata and knowledge graphs provide the crucial context needed for enterprise RAG systems to deliver accurate, relevant, and     │
│ insightful responses. This trend is likely to continue shaping the future of information retrieval powered by AI.                                                        │
│                                                                                                                                                                          │
│ ## 5. Embracing the power of multi-modal RAGs                                                                                                                            │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [3] Advancements in RAG: A Comprehensive Survey of ...                                                                                                                   │
│ URL: https://medium.com/@sahin.samia/advancements-in-rag-a-comprehensive-survey-of-techniques-and-applications-b6160b035199                                              │
│ Score: 0.74251556                                                                                                                                                        │
│ Content: ## Recent Advances in Retrieval Techniques                                                                                                                      │
│                                                                                                                                                                          │
│ Retrieval is the backbone of RAG, and recent techniques focus on enhancing efficiency and relevance:                                                                     │
│                                                                                                                                                                          │
│ ## Recent Advances in Generation Techniques                                                                                                                              │
│                                                                                                                                                                          │
│ Post-retrieval generation has seen significant enhancements to ensure relevance and coherence:                                                                           │
│                                                                                                                                                                          │
│ ## New RAG Paradigms and Architectures                                                                                                                                   │
│                                                                                                                                                                          │
│ RAG has moved beyond sequential retrieve-read to dynamic, modular systems:                                                                                               │
│                                                                                                                                                                          │
│ ## Multimodal and Specialized RAG Techniques [...] The latest and advanced RAG techniques have significantly enhanced the accuracy, relevance, and adaptability of       │
│ AI-generated content. By innovating in retrieval, generation, and system architectures, RAG is poised to play a central role in future AI-assisted information           │
│ processing, particularly in multimodal, domain-specific, and personalized applications. Continued research is essential to address scalability, bias, and                │
│ interpretability challenges, ensuring RAG’s robust deployment across [...] This report provides an in-depth analysis of the latest and advanced techniques in Retrieval  │
│ Augmented Generation (RAG), a pivotal approach in enhancing large language models (LLMs) by integrating external knowledge sources. The following sections detail recent │
│ advancements, categorized by retrieval, generation, new paradigms, and specialized applications, alongside challenges and future directions.                             │
│                                                                                                                                                                          │
│ ## Background and Evolution                                                                                                                                              │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [4] Retrieval Augmented Generation (RAG) for LLMs                                                                                                                        │
│ URL: https://www.promptingguide.ai/research/rag                                                                                                                          │
│ Score: 0.6829338                                                                                                                                                         │
│ Content: | Proposes Corrective Retrieval Augmented Generation (CRAG) to improve the robustness of generation in a RAG system. The core idea is to implement a            │
│ self-correct component for the retriever and improve the utilization of retrieved documents for augmenting generation. The retrieval evaluator helps to assess the       │
│ overall quality of retrieved documents given a query. Using web search and optimized knowledge utilization operations can improve automatic self-correction and          │
│ efficient utilization of [...] Given the increased flexibility in building RAG systems, other important optimization techniques have been proposed to optimize RAG       │
│ pipelines including:                                                                                                                                                     │
│                                                                                                                                                                          │
│ ## RAG Framework                                                                                                                                                         │
│                                                                                                                                                                          │
│ In this section, we summarize the key developments of the components of a RAG system, which include Retrieval, Generation, and Augmentation.                             │
│                                                                                                                                                                          │
│ ### Retrieval                                                                                                                                                            │
│                                                                                                                                                                          │
│ Retrieval is the component of RAG that deals with retrieving highly relevant context from a retriever. A retriever can be enhanced in many ways, including: [...] In     │
│ conclusion, RAG systems have evolved rapidly including the development of more advanced paradigms that enable customization and further the performance and utility of   │
│ RAG across a wide range of domains. There is a huge demand for RAG applications, which has accelerated the development of methods to improve the different components of │
│ a RAG system. From hybrid methodologies to self-retrieval, these are some of the currently explored research areas of modern RAG models. There is also                   │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [5] The Rise and Evolution of RAG in 2024 A Year in Review                                                                                                               │
│ URL: https://ragflow.io/blog/the-rise-and-evolution-of-rag-in-2024-a-year-in-review                                                                                      │
│ Score: 0.66699636                                                                                                                                                        │
│ Content: To achieve this, one approach, as previously mentioned, involves using models to convert multimodal documents into text before indexing for retrieval. Another  │
│ approach, leveraging advancements in VLMs, directly generates vectors, bypassing the complex OCR process. A pioneering example of this is ColPali [Reference 44], which  │
│ emerged in the summer of 2024. ColPali treats an image as 1024 image patches and generates embeddings for each patch, effectively representing a single image as a       │
│ tensor. [...] In April 2024, a technical report titled "BlendedRAG" from IBM Research [Reference 7] demonstrated through experiments that employing multiple recall      │
│ methods can yield better results for RAG. Specifically, combining vector search, sparse vector search, and full-text search achieves optimal recall. This is easy to     │
│ understand, as vectors can represent semantics; a sentence or even an entire article can be encapsulated in a single vector. Essentially, the vector conveys the         │
│ "meaning" of the text, [...] Microsoft's mid-year open-sourcing of GraphRAG was a groundbreaking event. As a library rather than an end-to-end solution, GraphRAG's      │
│ rapid rise in popularity underscores its ability to tackle key issues with Retrieval-Augmented Generation (RAG), particularly the semantic gap. This issue has long been │
│ a challenge for search system developers, as queries and answers often fail to align perfectly. When search systems evolved into RAG models, this problem was amplified: │
│ while traditional search                                                                                                                                                 │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [6] Retrieval-augmented generation                                                                                                                                       │
│ URL: https://en.wikipedia.org/wiki/Retrieval-augmented_generation                                                                                                        │
│ Score: 0.65914243                                                                                                                                                        │
│ Content: 26. ^ Edge, Darren; Trinh, Ha; Cheng, Newman; Bradley, Joshua; Chao, Alex; Mody, Apurva; Truitt, Steven; Metropolitansky, Dasha; Ness, Robert Osazuwa (2024).   │
│ "From Local to Global: A Graph RAG Approach to Query-Focused Summarization". arXiv "ArXiv (identifier)"):2404.16130 . [...] 5. ^ a b Turow Jon, Kiela Douwe (March 26,   │
│ 2025). "RAG Inventor Talks Agents, Grounded AI, and Enterprise Impact". Madrona.                                                                                         │
│ 6. ^ a b c d "Can a technology called RAG keep AI models from making stuff up?". Ars Technica. 6 June 2024. Retrieved 7 March 2025.                                      │
│ 7. ^ "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". ai.meta.com. 2020.                                                                              │
│ 8. ^ a b Xu, Sherlock (January 25, 2024). "Understanding Retrieval-Augmented Generation: Part 1". www.bentoml.com. [...] 9. ^ "Mitigating LLM hallucinations in text     │
│ summarisation". BBC. 20 June 2024. Retrieved 7 March 2025.                                                                                                               │
│ 10. ^ a b "What is RAG? - Retrieval-Augmented Generation AI Explained - AWS". Amazon Web Services, Inc. Retrieved 16 July 2024.                                          │
│ 11. ^ a b Kiela Douwe, Turck Matt (March 6, 2025). "Top AI Researcher on GPT 4.5, DeepSeek and Agentic RAG | Douwe Kiela, CEO, Contextual AI". YouTube.                  │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [7] Challenges and Future Directions in RAG Research                                                                                                                     │
│ URL: https://www.harrisonclarke.com/blog/challenges-and-future-directions-in-rag-research-embracing-data-ai                                                              │
│ Score: 0.6044228                                                                                                                                                         │
│ Content: Approach: Developing more efficient retrieval mechanisms and scalable architectures is crucial. This includes leveraging advances in distributed computing,     │
│ parallel processing, and optimized indexing techniques.                                                                                                                  │
│                                                                                                                                                                          │
│ Techniques:                                                                                                                                                              │
│                                                                                                                                                                          │
│ Example: Implementing a hybrid retrieval system that uses sparse representations for initial filtering and dense representations for fine-grained ranking can enhance    │
│ the scalability and accuracy of RAG systems in large-scale applications. [...] Combining Sparse and Dense Representations                                                │
│                                                                                                                                                                          │
│ ### 2. Improving Adaptability to Diverse Domains                                                                                                                         │
│                                                                                                                                                                          │
│ Approach: Developing domain-adaptation techniques and transfer learning methods can enable RAG systems to perform well across various domains. This involves fine-tuning │
│ pre-trained models on domain-specific data and incorporating domain knowledge into the retrieval and generation processes.                                               │
│                                                                                                                                                                          │
│ Techniques: [...] Retrieval-Augmented Generation (RAG) systems combine the strengths of information retrieval and natural language generation. They fetch relevant       │
│ information from a vast repository and use this data to generate coherent, contextually appropriate responses or documents. This dual capability makes RAG systems       │
│ invaluable for applications such as customer support, content creation, and research synthesis.                                                                          │
│                                                                                                                                                                          │
│ ## Current Challenges in RAG Research                                                                                                                                    │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [8] The Evolution, Advancements, and Industry Landscape of ...                                                                                                           │
│ URL: https://medium.com/@FrankGoortani/the-evolution-advancements-and-industry-landscape-of-retrieval-augmented-generation-rag-dde4cb39940c                              │
│ Score: 0.5780915                                                                                                                                                         │
│ Content: Shift Towards Production-Ready Systems: In 2024, the focus shifted from experimental RAG implementations to scalable, production-ready systems.                 │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [9] A Systematic Review of Key Retrieval-Augmented ...                                                                                                                   │
│ URL: https://arxiv.org/html/2507.18910v1                                                                                                                                 │
│ Score: 0.5524679                                                                                                                                                         │
│ Content: Jul 25, 2025—Retrieval-Augmented Generation (RAG) represents a majoradvancementin natural language processing (NLP), combining large language models            │
│                                                                                                                                                                          │
│                                                                                                                                                                          │
│ [10] What is RAG (Retrieval-Augmented Generation)?                                                                                                                       │
│ URL: https://aws.amazon.com/what-is/retrieval-augmented-generation/                                                                                                      │
│ Score: 0.53225553                                                                                                                                                        │
│ Content: ### Augment the LLM prompt                                                                                                                                      │
│                                                                                                                                                                          │
│ Next, the RAG model augments the user input (or prompts) by adding the relevant retrieved data in context. This step uses prompt engineering techniques to communicate   │
│ effectively with the LLM. The augmented prompt allows the large language models to generate an accurate answer to user queries.                                          │
│                                                                                                                                                                          │
│ ### Update external data [...] Retrieval-Augmented Generation (RAG) is the process of optimizing the output of a large language model, so it references an authoritative │
│ knowledge base outside of its training data sources before generating a response. Large Language Models (LLMs) are trained on vast volumes of data and use billions of   │
│ parameters to generate original output for tasks like answering questions, translating languages, and completing sentences. RAG extends the already powerful             │
│ capabilities of LLMs to specific [...] With RAG, developers can test and improve their chat applications more efficiently. They can control and change the LLM's         │
│ information sources to adapt to changing requirements or cross-functional usage. Developers can also restrict sensitive information retrieval to different authorization │
│ levels and ensure the LLM generates appropriate responses. In addition, they can also troubleshoot and make fixes if the LLM references incorrect information sources    │
│ for specific questions. Organizations can                                                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Based on my search, here are the latest advances in RAG systems for 2024:

## Key Advances in RAG Systems (2024)

### 1. **Graph-Based RAG Approaches**
- **GraphRAG**: Microsoft's open-source GraphRAG gained significant popularity by addressing the semantic gap problem through knowledge graph integration
- **KRAGEN (Knowledge Retrieval Augmented Generation Engine)**: Uses graph-of-thoughts prompting to decompose complex queries into subproblems and retrieve relevant subgraphs
- Knowledge graph embeddings combined with unstructured text embeddings show up to 13.1% improvements in retrieval correctness

### 2. **Hybrid Retrieval Strategies**
- **BlendedRAG** (IBM Research): Demonstrates that combining multiple recall methods yields better results:
  - Vector search for semantic understanding
  - Sparse vector search
  - Full-text search
- This hybrid approach achieves optimal recall by leveraging different strengths of each method

### 3. **Advanced Corrective and Adaptive Techniques**
- **CRAG (Corrective Retrieval Augmented Generation)**: Implements self-correction components for retrievers with quality assessment of retrieved documents
- **SELF-ROUTE**: Dynamically routes tasks between retrieval and generation modules based on model-assessed difficulty
- **AU-RAG**: Uses agentic decision-making to mediate between diverse retrieval sources
- **TA-ARE (Time-Aware Adaptive Retrieval)**: Features a retrieval trigger classifier that adaptively determines when retrieval is necessary

### 4. **Multi-Modal RAG Systems**
- **ColPali**: Treats images as 1024 patches and generates embeddings for each patch, bypassing complex OCR processes
- Multi-modal systems capable of processing text, images, and other data types
- Direct vector generation from visual content using Vision Language Models (VLMs)

### 5. **Production-Ready and Scalable Systems**
- Major shift from experimental implementations to enterprise-ready, scalable RAG systems
- Enhanced metadata utilization for better context understanding
- Improved integration with knowledge graphs
- Focus on reliability and real-world deployment value

### 6. **Query Enhancement Techniques**
- **RAG-Fusion**: Improves recall by combining results from multiple reformulated queries through reciprocal rank fusion
- Complex multi-hop query formulation using generative LLMs
- Advanced query decomposition strategies

### 7. **Architectural Improvements**
- Move beyond sequential retrieve-read to dynamic, modular systems
- Distributed computing and parallel processing integration
- Optimized indexing techniques for better scalability
- Hybrid systems combining sparse and dense representations

### 8. **Domain-Specific Adaptations**
- Transfer learning methods for cross-domain performance
- Fine-tuning pre-trained models on domain-specific data
- Domain knowledge incorporation into retrieval and generation processes

These advances collectively enhance RAG systems' accuracy, relevance, adaptability, and real-world applicability across various enterprise applications. The focus has shifted toward building robust, production-ready systems that can handle complex queries and deliver reliable results at scale.Now let me create a comprehensive technical blog post based on these research findings.
Tool #2: writing_assistant
# The Evolution of RAG: 2024's Most Significant Advances in Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) has rapidly evolved from a promising research concept to a cornerstone technology powering enterprise AI applications. As we progress through 2024, the landscape of RAG systems has transformed dramatically, moving beyond simple vector-based retrieval to sophisticated, multi-modal, and self-correcting architectures.

This comprehensive overview explores the most significant advances in RAG technology this year, providing practical insights for developers and researchers looking to implement state-of-the-art retrieval systems.

## 1. Graph-Based RAG: Bridging the Semantic Gap

### The Knowledge Graph Revolution

Traditional RAG systems often struggle with complex queries requiring multi-hop reasoning or deep contextual understanding. Graph-based RAG approaches have emerged as a powerful solution to this semantic gap problem.

**Microsoft's GraphRAG** has gained significant traction in the open-source community by integrating knowledge graphs directly into the retrieval process. Unlike traditional vector-based approaches that treat documents as isolated entities, GraphRAG creates rich semantic networks that capture relationships between concepts.

```python
# Simplified GraphRAG implementation concept
class GraphRAG:
    def __init__(self, knowledge_graph, text_embeddings):
        self.kg = knowledge_graph
        self.embeddings = text_embeddings
        
    def retrieve(self, query):
        # Extract entities from query
        entities = self.extract_entities(query)
        
        # Retrieve relevant subgraph
        subgraph = self.kg.get_subgraph(entities, max_hops=2)
        
        # Combine graph and text embeddings
        graph_embeddings = self.embed_subgraph(subgraph)
        text_matches = self.semantic_search(query)
        
        return self.fusion_ranking(graph_embeddings, text_matches)
```

**KRAGEN (Knowledge Retrieval Augmented Generation Engine)** takes this further by implementing graph-of-thoughts prompting, which decomposes complex queries into manageable subproblems. This approach has shown remarkable improvements, with knowledge graph embeddings combined with unstructured text embeddings achieving up to **13.1% improvements in retrieval correctness**.

### Implementation Considerations

When implementing graph-based RAG:
- **Entity Linking**: Ensure robust entity extraction and linking to your knowledge graph
- **Subgraph Selection**: Implement efficient algorithms for relevant subgraph retrieval
- **Embedding Fusion**: Develop strategies to effectively combine graph and text embeddings

## 2. Hybrid Retrieval: The Best of All Worlds

### Beyond Single-Method Retrieval

IBM Research's **BlendedRAG** has demonstrated that the future lies not in choosing between retrieval methods, but in intelligently combining them. This hybrid approach leverages:

- **Vector search** for semantic understanding
- **Sparse vector search** for exact term matching
- **Full-text search** for comprehensive coverage

```python
class BlendedRAG:
    def __init__(self):
        self.dense_retriever = DenseVectorRetriever()
        self.sparse_retriever = SparseVectorRetriever()
        self.fulltext_retriever = FullTextRetriever()
        
    def hybrid_retrieve(self, query, k=10):
        # Parallel retrieval from multiple sources
        dense_results = self.dense_retriever.search(query, k)
        sparse_results = self.sparse_retriever.search(query, k)
        fulltext_results = self.fulltext_retriever.search(query, k)
        
        # Weighted fusion with learned parameters
        return self.fuse_results([
            (dense_results, 0.5),
            (sparse_results, 0.3),
            (fulltext_results, 0.2)
        ])
```

This hybrid approach achieves optimal recall by leveraging the unique strengths of each retrieval method, providing more robust and comprehensive results than any single approach.

## 3. Self-Correcting and Adaptive RAG Systems

### Intelligence in Retrieval Decision-Making

The most exciting development in 2024 has been the emergence of RAG systems that can assess their own performance and adapt accordingly.

**CRAG (Corrective Retrieval Augmented Generation)** implements sophisticated self-correction mechanisms:

```python
class CRAG:
    def __init__(self, retriever, generator, quality_assessor):
        self.retriever = retriever
        self.generator = generator
        self.quality_assessor = quality_assessor
        
    def generate_with_correction(self, query):
        # Initial retrieval
        documents = self.retriever.retrieve(query)
        
        # Assess quality of retrieved documents
        quality_scores = self.quality_assessor.evaluate(query, documents)
        
        if self.is_quality_sufficient(quality_scores):
            return self.generator.generate(query, documents)
        else:
            # Corrective retrieval with refined query
            refined_query = self.refine_query(query, documents)
            corrected_docs = self.retriever.retrieve(refined_query)
            return self.generator.generate(query, corrected_docs)
```

**SELF-ROUTE** takes adaptive behavior further by dynamically routing tasks between retrieval and generation modules based on model-assessed difficulty. This intelligent routing prevents unnecessary retrieval operations for queries that can be answered directly.

**TA-ARE (Time-Aware Adaptive Retrieval)** introduces temporal awareness with a retrieval trigger classifier that determines when retrieval is necessary, optimizing both performance and computational resources.

## 4. Multi-Modal RAG: Beyond Text

### Processing the Visual World

The integration of multi-modal capabilities represents a paradigm shift in RAG systems. **ColPali** exemplifies this evolution by treating images as collections of 1024 patches, generating embeddings for each patch without complex OCR preprocessing.

```python
class MultiModalRAG:
    def __init__(self):
        self.text_encoder = TextEncoder()
        self.vision_encoder = VisionEncoder()
        self.colpali_processor = ColPaliProcessor()
        
    def encode_document(self, document):
        if document.type == "text":
            return self.text_encoder.encode(document.content)
        elif document.type == "image":
            # Direct visual embedding without OCR
            patches = self.colpali_processor.patchify(document.image)
            return [self.vision_encoder.encode(patch) for patch in patches]
        elif document.type == "mixed":
            return self.encode_mixed_content(document)
```

This approach bypasses the error-prone OCR pipeline entirely, using Vision Language Models (VLMs) to generate meaningful embeddings directly from visual content.

## 5. Production-Ready Architecture

### From Research to Reality

2024 has witnessed a crucial shift from experimental implementations to enterprise-ready, scalable RAG systems. Key characteristics include:

- **Enhanced metadata utilization** for better context understanding
- **Improved knowledge graph integration** for semantic richness
- **Focus on reliability** and real-world deployment value

```python
class ProductionRAG:
    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.cache_manager = CacheManager()
        self.monitoring = SystemMonitoring()
        
    async def scalable_retrieve(self, query, user_context):
        # Distributed retrieval with caching
        cache_key = self.generate_cache_key(query, user_context)
        
        if cached_result := await self.cache_manager.get(cache_key):
            return cached_result
            
        # Parallel processing across multiple retrieval nodes
        results = await self.load_balancer.distribute_query(
            query, self.available_nodes
        )
        
        # Cache and monitor performance
        await self.cache_manager.set(cache_key, results)
        self.monitoring.log_performance_metrics(query, results)
        
        return results
```

## 6. Advanced Query Enhancement

### RAG-Fusion and Beyond

Query enhancement has become increasingly sophisticated. **RAG-Fusion** improves recall by combining results from multiple reformulated queries through reciprocal rank fusion:

```python
class RAGFusion:
    def __init__(self, query_reformulator, retriever):
        self.reformulator = query_reformulator
        self.retriever = retriever
        
    def enhanced_retrieve(self, original_query, num_variants=3):
        # Generate query variants
        query_variants = self.reformulator.generate_variants(
            original_query, num_variants
        )
        
        # Retrieve for each variant
        all_results = []
        for query in [original_query] + query_variants:
            results = self.retriever.retrieve(query)
            all_results.append(results)
        
        # Reciprocal rank fusion
        return self.reciprocal_rank_fusion(all_results)
    
TRUNCATED for brevity ---
"""