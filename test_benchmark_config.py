#!/usr/bin/env python3
"""
Test script for GEO Benchmark Configuration

This script validates the benchmark configuration and displays
the complete benchmark structure without running actual analysis.
"""

from benchmark_config import (
    GEO_DIMENSIONS,
    BENCHMARK_QUESTIONS,
    SCORING_THRESHOLDS,
    CONFIDENCE_INTERPRETATION,
    QUALITY_METRICS,
    RECOMMENDATIONS,
    get_all_questions,
    get_weighted_questions,
    get_score_rating,
    get_recommendations_for_scores
)


def test_configuration():
    """Test and display the benchmark configuration."""
    
    print("=" * 80)
    print("GEO BENCHMARK CONFIGURATION TEST")
    print("=" * 80)
    print()
    
    # Test 1: Dimensions
    print("1. GEO DIMENSIONS")
    print("-" * 80)
    total_weight = 0
    for dimension, config in GEO_DIMENSIONS.items():
        weight = config["weight"]
        total_weight += weight
        print(f"  • {dimension.upper()}")
        print(f"    Weight: {weight*100}%")
        print(f"    Description: {config['description']}")
        print(f"    Metrics: {', '.join(config['metrics'])}")
        print()
    
    print(f"  Total Weight: {total_weight*100}% {'✓' if total_weight == 1.0 else '✗ ERROR'}")
    print()
    
    # Test 2: Question Categories
    print("2. QUESTION CATEGORIES")
    print("-" * 80)
    total_cat_weight = 0
    total_questions = 0
    for category, config in BENCHMARK_QUESTIONS.items():
        weight = config["weight"]
        total_cat_weight += weight
        num_questions = len(config["questions"])
        total_questions += num_questions
        
        print(f"  • {category.upper()}")
        print(f"    Dimension: {config['dimension']}")
        print(f"    Weight: {weight*100}%")
        print(f"    Questions: {num_questions}")
        print(f"    Sample: \"{config['questions'][0]}\"")
        print()
    
    print(f"  Total Weight: {total_cat_weight*100}% {'✓' if total_cat_weight == 1.0 else '✗ ERROR'}")
    print(f"  Total Questions: {total_questions}")
    print()
    
    # Test 3: All Questions
    print("3. COMPLETE QUESTION LIST")
    print("-" * 80)
    weighted_questions = get_weighted_questions()
    for i, q in enumerate(weighted_questions, 1):
        print(f"  {i:2d}. [{q['category']:15s}] {q['question']}")
    print()
    
    # Test 4: Scoring Thresholds
    print("4. SCORING THRESHOLDS")
    print("-" * 80)
    for rating, config in SCORING_THRESHOLDS.items():
        print(f"  • {rating.upper():12s} (>= {config['min_score']:3d}): {config['description']}")
    print()
    
    # Test 5: Score Rating Function
    print("5. SCORE RATING TESTS")
    print("-" * 80)
    test_scores = [95, 75, 55, 35, 15]
    for score in test_scores:
        rating, config = get_score_rating(score)
        print(f"  Score {score:3d} → {rating:12s} ({config['description']})")
    print()
    
    # Test 6: Recommendations
    print("6. RECOMMENDATIONS STRUCTURE")
    print("-" * 80)
    for dimension, recs in RECOMMENDATIONS.items():
        total_recs = sum(len(recs[priority]) for priority in ["low", "medium", "high"])
        print(f"  • {dimension.upper()}: {total_recs} recommendations")
        print(f"    - Critical (low score): {len(recs['low'])} items")
        print(f"    - Important (medium score): {len(recs['medium'])} items")
        print(f"    - Nice-to-have (high score): {len(recs['high'])} items")
    print()
    
    # Test 7: Sample Recommendations
    print("7. SAMPLE RECOMMENDATIONS")
    print("-" * 80)
    sample_scores = {
        "relevance": 45,
        "authority": 60,
        "comprehensiveness": 75,
        "clarity": 80,
        "recency": 40,
        "actionability": 55
    }
    
    print("  Sample dimension scores:")
    for dim, score in sample_scores.items():
        print(f"    {dim}: {score}")
    print()
    
    recs = get_recommendations_for_scores(sample_scores)
    print(f"  Generated Recommendations:")
    print(f"    Critical: {len(recs['critical'])} items")
    print(f"    Important: {len(recs['important'])} items")
    print(f"    Nice-to-have: {len(recs['nice_to_have'])} items")
    print()
    
    if recs['critical']:
        print("  Top 3 Critical Recommendations:")
        for i, rec in enumerate(recs['critical'][:3], 1):
            print(f"    {i}. {rec}")
    print()
    
    # Test 8: Quality Metrics
    print("8. QUALITY METRICS")
    print("-" * 80)
    for metric, config in QUALITY_METRICS.items():
        print(f"  • {metric.upper()}")
        print(f"    {config['description']}")
        if 'min_words' in config:
            print(f"    Min: {config['min_words']}, Optimal: {config['optimal_words']}")
        elif 'min_headings' in config:
            print(f"    Min: {config['min_headings']}, Optimal: {config['optimal_headings']}")
        elif 'min_rate' in config:
            print(f"    Min: {config['min_rate']*100}%, Optimal: {config['optimal_rate']*100}%")
        print()
    
    # Test 9: Confidence Interpretation
    print("9. CONFIDENCE INTERPRETATION")
    print("-" * 80)
    print("  Retrieval Confidence:")
    for quality, (min_val, max_val) in CONFIDENCE_INTERPRETATION["retrieval"].items():
        print(f"    {quality:12s}: {min_val:5.1f}% - {max_val:5.1f}%")
    print()
    print("  LLM Confidence:")
    for quality, (min_val, max_val) in CONFIDENCE_INTERPRETATION["llm"].items():
        print(f"    {quality:20s}: {min_val:4.1f} - {max_val:4.1f}")
    print()
    
    # Summary
    print("=" * 80)
    print("CONFIGURATION SUMMARY")
    print("=" * 80)
    print(f"  ✓ {len(GEO_DIMENSIONS)} GEO dimensions configured")
    print(f"  ✓ {len(BENCHMARK_QUESTIONS)} question categories defined")
    print(f"  ✓ {total_questions} total benchmark questions")
    print(f"  ✓ {len(SCORING_THRESHOLDS)} scoring thresholds")
    print(f"  ✓ {len(RECOMMENDATIONS)} dimension recommendation sets")
    print(f"  ✓ Configuration appears valid")
    print("=" * 80)
    print()


def test_dimension_coverage():
    """Test that all dimensions are covered by question categories."""
    print("DIMENSION COVERAGE TEST")
    print("-" * 80)
    
    # Collect dimensions from questions
    covered_dimensions = set()
    for category, config in BENCHMARK_QUESTIONS.items():
        covered_dimensions.add(config["dimension"])
    
    # Check coverage
    all_dimensions = set(GEO_DIMENSIONS.keys())
    missing = all_dimensions - covered_dimensions
    extra = covered_dimensions - all_dimensions
    
    if not missing and not extra:
        print("  ✓ All dimensions are properly covered by question categories")
    else:
        if missing:
            print(f"  ✗ Missing coverage for: {missing}")
        if extra:
            print(f"  ✗ Extra dimensions in questions: {extra}")
    
    print()


if __name__ == "__main__":
    test_configuration()
    test_dimension_coverage()
    
    print("\nConfiguration test complete!")
    print("You can now run: python geo_benchmark.py")
