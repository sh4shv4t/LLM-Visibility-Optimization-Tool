# GEO Benchmark System - Quick Start

## What's New

Your LLM Visibility Optimization Tool now includes a comprehensive **GEO (Generative Engine Optimization) Benchmark System** that evaluates how well your website is optimized for LLM visibility across 6 key dimensions with 30+ benchmark questions.

## Quick Start

### 1. Install Updated Dependencies

```bash
pip install -U langchain-chroma langchain-ollama
```

### 2. Test the Configuration

```bash
python test_benchmark_config.py
```

This will display:
- 6 GEO dimensions (Relevance, Authority, Comprehensiveness, Clarity, Recency, Actionability)
- 30+ benchmark questions across 6 categories
- Scoring thresholds and recommendation structure
- Complete configuration validation

### 3. Run Comprehensive Analysis

```bash
# Make sure Ollama is running
ollama serve

# In another terminal, run the benchmark
python geo_benchmark.py
```

This will:
- Analyze your scraped content across all dimensions
- Generate detailed scores for each dimension
- Provide prioritized recommendations
- Save a detailed JSON report

### 4. Use via Web Interface

```bash
python app.py
```

Then visit `http://localhost:5000` and use the updated "Analyze Quality" button.

## New Files Created

1. **benchmark_config.py** - Complete GEO configuration
   - 6 evaluation dimensions with weights
   - 30+ benchmark questions in 6 categories
   - Scoring system and recommendation engine

2. **geo_benchmark.py** - Main analysis engine
   - Comprehensive benchmark analyzer
   - Retry logic for LLM queries
   - Detailed report generation

3. **GEO_BENCHMARK_GUIDE.md** - Complete documentation
   - Detailed explanation of all dimensions
   - How to interpret results
   - Optimization workflow and best practices

4. **test_benchmark_config.py** - Configuration validator
   - Tests configuration integrity
   - Displays all questions and settings
   - Validates dimension coverage

## Key Improvements

✅ **Fixed Deprecation Warnings**
- Updated to `langchain-chroma` and `langchain-ollama`
- Compatible with latest LangChain versions

✅ **Better Error Handling**
- Retry logic for LLM failures
- JSON parsing improvements
- Graceful error recovery

✅ **Comprehensive Analysis**
- 30+ questions vs 7 in old system
- Weighted scoring by importance
- Category-based organization

✅ **Actionable Recommendations**
- Prioritized by impact (Critical, Important, Nice-to-have)
- Specific to each GEO dimension
- Based on actual scores

## Example Output

```
Overall GEO Score: 75.5/100 (GOOD)
Rating: Well-optimized with room for improvement

Dimension Scores:
  - Relevance: 80.2/100 (weight: 25%)
  - Authority: 65.5/100 (weight: 20%)
  - Comprehensiveness: 78.0/100 (weight: 20%)
  - Clarity: 82.1/100 (weight: 15%)
  - Recency: 60.0/100 (weight: 10%)
  - Actionability: 71.3/100 (weight: 10%)

Statistics:
  - Answer Rate: 83.3%
  - Avg Retrieval Confidence: 72.5%
  - Avg LLM Confidence: 7.2/10

CRITICAL Recommendations:
  • Add publication and last updated dates to content
  • Display trust badges, certifications, and partnerships
  
IMPORTANT Recommendations:
  • Expand existing content with more details and examples
  • Establish a regular content update schedule
```

## Understanding Your Score

- **85-100 (Excellent):** Highly optimized for LLM visibility
- **70-84 (Good):** Well-optimized with room for improvement
- **50-69 (Average):** Basic optimization, significant improvements needed
- **30-49 (Poor):** Limited optimization, major improvements required
- **0-29 (Very Poor):** Minimal LLM visibility, comprehensive overhaul needed

## Next Steps

1. **Read the Guide:** Check `GEO_BENCHMARK_GUIDE.md` for detailed documentation
2. **Run Analysis:** Test with your scraped content
3. **Review Scores:** Focus on dimensions with lowest scores
4. **Implement Recommendations:** Start with critical items
5. **Re-analyze:** Measure improvement

## Troubleshooting

**Issue:** "No data received from Ollama stream"
- **Solution:** Ensure Ollama is running with `ollama serve`

**Issue:** "Invalid JSON response"
- **Solution:** Try a different model or increase timeout

**Issue:** Low scores across all dimensions
- **Solution:** Ensure content was properly scraped and indexed

## Support

For detailed information, see:
- `GEO_BENCHMARK_GUIDE.md` - Complete documentation
- `benchmark_config.py` - Configuration details
- `geo_benchmark.py` - Implementation code

## Performance Notes

The comprehensive GEO benchmark analysis typically takes 2-5 minutes to complete, depending on the complexity of your content and the LLM being used.
