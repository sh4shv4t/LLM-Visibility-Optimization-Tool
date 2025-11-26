# GEO Benchmark System Documentation

## Overview

The GEO (Generative Engine Optimization) Benchmark System is a comprehensive tool for analyzing how well your website is optimized for visibility in LLM-generated responses. This system evaluates multiple dimensions of content quality and provides actionable recommendations.

## What is GEO?

Generative Engine Optimization (GEO) is the practice of optimizing content to increase its likelihood of being featured and recommended by Large Language Models (LLMs) like ChatGPT, Claude, Gemini, etc. As users increasingly rely on AI assistants for information, GEO becomes crucial for digital visibility.

## System Architecture

### Components

1. **benchmark_config.py** - Configuration and criteria for evaluation
   - Defines 6 key GEO dimensions
   - Contains 30+ benchmark questions across 6 categories
   - Includes scoring thresholds and recommendations

2. **geo_benchmark.py** - Main benchmark analysis engine
   - Runs comprehensive analysis
   - Generates detailed reports with scores and recommendations
   - Handles LLM queries with retry logic

## GEO Dimensions Explained

### 1. Relevance (25% weight)
**What it measures:** How well your content matches user queries and intent.

**Why it matters:** LLMs prioritize content that directly answers user questions with relevant keywords and semantic alignment.

**Key factors:**
- Keyword coverage
- Semantic similarity to common queries
- Topic alignment with user intent

### 2. Authority (20% weight)
**What it measures:** Trustworthiness and credibility signals in your content.

**Why it matters:** LLMs prefer citing authoritative sources with proven expertise.

**Key factors:**
- Source citations and references
- Expertise indicators (credentials, certifications)
- Social proof (testimonials, case studies)

### 3. Comprehensiveness (20% weight)
**What it measures:** Breadth and depth of information coverage.

**Why it matters:** LLMs favor comprehensive resources that thoroughly cover topics.

**Key factors:**
- Topic coverage breadth
- Detail level and depth
- Completeness of information

### 4. Clarity (15% weight)
**What it measures:** How easily LLMs can extract and understand information.

**Why it matters:** Well-structured, clear content is easier for LLMs to parse and summarize.

**Key factors:**
- Content structure quality
- Conciseness and readability
- Terminology clarity

### 5. Recency (10% weight)
**What it measures:** Freshness and timeliness of information.

**Why it matters:** LLMs prefer recent, up-to-date information for time-sensitive topics.

**Key factors:**
- Date indicators
- Current events and trends
- Update frequency

### 6. Actionability (10% weight)
**What it measures:** Presence of clear calls-to-action and next steps.

**Why it matters:** LLMs often recommend sites that provide clear guidance on next actions.

**Key factors:**
- CTA presence and clarity
- Contact information availability
- Navigation clarity

## Question Categories

### 1. Informational (30% weight)
Questions about core content, products, services, and value propositions.
- *Example:* "What is the main topic or purpose of this website?"

### 2. Navigational (15% weight)
Questions about finding specific information or contact details.
- *Example:* "How can I contact this organization?"

### 3. Transactional (15% weight)
Questions about taking action, purchasing, or engaging.
- *Example:* "What actions does the website encourage visitors to take?"

### 4. Comparison (15% weight)
Questions about options, alternatives, and feature comparisons.
- *Example:* "What are the different pricing tiers available?"

### 5. Authority (15% weight)
Questions about credibility, expertise, and social proof.
- *Example:* "What credentials does the organization have?"

### 6. Technical (10% weight)
Questions about specifications, requirements, and technical details.
- *Example:* "What technical specifications are provided?"

## Scoring System

### Overall GEO Score (0-100)
Calculated as a weighted average of dimension scores:
```
GEO Score = Σ(Dimension Score × Dimension Weight)
```

### Score Ratings

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 85-100 | Excellent | Highly optimized for LLM visibility |
| 70-84 | Good | Well-optimized with room for improvement |
| 50-69 | Average | Basic optimization, significant improvements needed |
| 30-49 | Poor | Limited optimization, major improvements required |
| 0-29 | Very Poor | Minimal LLM visibility, comprehensive overhaul needed |

### Confidence Scores

**Retrieval Confidence (0-100%):**
- Measures how well the vector database retrieves relevant content
- Based on similarity scores from the embedding model
- Higher = better content organization and relevance

**LLM Confidence (0-10):**
- Self-reported by the LLM for each answer
- Indicates how certain the model is based on available context
- Higher = clearer, more complete information

## Using the Benchmark System

### Quick Start

1. **Install dependencies:**
```bash
pip install -U langchain-chroma langchain-ollama
```

2. **Ensure Ollama is running:**
```bash
ollama serve
# In another terminal:
ollama pull gpt-oss:20b  # or your preferred model
```

3. **Run benchmark analysis:**
```bash
python geo_benchmark.py
```

### Via Web Interface

1. Start the Flask app:
```bash
python app.py
```

2. Navigate to `http://localhost:5000`

3. Steps:
   - Enter a website URL
   - Click "Scrape and Index"
   - Click "Analyze Quality"
   - Review the comprehensive GEO report

### Standalone Usage

```python
from geo_benchmark import GEOBenchmarkAnalyzer, generate_report_text

# Initialize analyzer
analyzer = GEOBenchmarkAnalyzer()
if analyzer.initialize():
    # Run analysis
    report = analyzer.analyze_by_category()
    
    # Print human-readable report
    print(generate_report_text(report))
    
    # Access specific data
    geo_score = report['overall_geo_score']
    recommendations = report['recommendations']
```

## Interpreting Results

### Report Structure

```json
{
  "overall_geo_score": 75.5,
  "rating": "good",
  "rating_description": "Well-optimized with room for improvement",
  "dimension_scores": {
    "relevance": 80.2,
    "authority": 65.5,
    "comprehensiveness": 78.0,
    "clarity": 82.1,
    "recency": 60.0,
    "actionability": 71.3
  },
  "statistics": {
    "total_questions": 30,
    "answered_questions": 25,
    "answer_rate": 0.833,
    "avg_retrieval_confidence": 72.5,
    "avg_llm_confidence": 7.2
  },
  "recommendations": {
    "critical": [],
    "important": [...],
    "nice_to_have": [...]
  }
}
```

### Understanding Recommendations

**Critical (Score < 50):**
- Must-fix issues significantly impacting LLM visibility
- Address these first for maximum impact

**Important (Score 50-70):**
- Notable improvements that will boost visibility
- Address after critical issues

**Nice-to-have (Score 70-85):**
- Refinements for optimization excellence
- Address for competitive edge

## Optimization Workflow

### 1. Initial Analysis
Run the benchmark to establish baseline scores.

### 2. Prioritize Improvements
Focus on:
- Critical recommendations first
- Dimensions with lowest scores
- High-weight dimensions (relevance, authority, comprehensiveness)

### 3. Implement Changes
Follow recommendations for each dimension:
- Add missing content
- Improve structure
- Enhance credibility signals
- Update outdated information

### 4. Re-analyze
Run benchmark again to measure improvement.

### 5. Iterate
Continue optimizing until target score achieved.

## Best Practices

### Content Optimization
1. **Use clear, descriptive headings** - LLMs rely heavily on document structure
2. **Include FAQs** - Direct Q&A format is ideal for LLM extraction
3. **Add structured data** - Lists, tables, and sections help parsing
4. **Cite sources** - Build authority with references
5. **Keep content fresh** - Regular updates improve recency scores

### Technical Optimization
1. **Semantic HTML** - Use proper heading hierarchy (h1, h2, h3)
2. **Meta information** - Include dates, authors, categories
3. **Internal linking** - Connect related content
4. **Clean formatting** - Avoid cluttered layouts
5. **Mobile-friendly** - Ensure content is accessible

### Testing Strategy
1. **Regular benchmarking** - Run analysis monthly
2. **A/B testing** - Test changes on staging before production
3. **Monitor trends** - Track score changes over time
4. **Competitor analysis** - Compare with industry leaders
5. **User feedback** - Validate with real user questions

## Troubleshooting

### Common Issues

**"No data received from Ollama stream"**
- Ensure Ollama is running: `ollama serve`
- Check model is available: `ollama list`
- Verify model name in config matches installed model

**"Invalid JSON response"**
- LLM may not support JSON format parameter
- Try using a different model (llama3, mistral, etc.)
- Increase timeout in OllamaLLM initialization

**Low retrieval confidence**
- Content may not be properly indexed
- Re-run scraping and indexing
- Check vector database exists

**Low answer rate**
- Content may be too sparse
- Add more comprehensive information
- Ensure scraper captured all relevant content

## Customization

### Adding Custom Questions

Edit `benchmark_config.py`:

```python
BENCHMARK_QUESTIONS["custom_category"] = {
    "dimension": "relevance",
    "weight": 0.10,
    "questions": [
        "Your custom question here?",
        "Another question?",
    ]
}
```

### Adjusting Dimension Weights

Modify `GEO_DIMENSIONS` in `benchmark_config.py`:

```python
GEO_DIMENSIONS["relevance"]["weight"] = 0.30  # Increase from 0.25
```

### Custom Recommendations

Add to `RECOMMENDATIONS` in `benchmark_config.py`:

```python
RECOMMENDATIONS["custom_dimension"] = {
    "low": ["Recommendation for low scores"],
    "medium": ["Recommendation for medium scores"],
    "high": ["Recommendation for high scores"]
}
```

## Performance Considerations

- **Analysis time:** ~2-5 minutes for 30 questions
- **Model requirements:** 8GB+ RAM for 20B parameter models
- **Retry logic:** Handles temporary LLM failures
- **Timeout:** 60 seconds per question by default

## Future Enhancements

Planned features:
- [ ] Historical tracking and trend analysis
- [ ] Competitor comparison reports
- [ ] Visual dashboards with charts
- [ ] Export to PDF/HTML reports
- [ ] API endpoint for programmatic access
- [ ] Multi-language support
- [ ] Custom scoring formulas

## References

- [Generative Engine Optimization Principles](https://arxiv.org)
- [LangChain Documentation](https://python.langchain.com)
- [Ollama Documentation](https://ollama.ai)
- [ChromaDB Documentation](https://docs.trychroma.com)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in console output
3. Verify all dependencies are installed
4. Ensure Ollama model is compatible

## License

This tool is part of the LLM-Visibility-Optimization-Tool project.
