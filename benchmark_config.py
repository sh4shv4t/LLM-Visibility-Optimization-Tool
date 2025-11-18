"""
Benchmark Configuration for GEO (Generative Engine Optimization) Analysis

This module defines the comprehensive benchmark criteria for evaluating
how well a website is optimized for LLM visibility and promotion.

Based on research in GEO best practices and information retrieval metrics.
"""

# ============================================================================
# GEO EVALUATION DIMENSIONS
# ============================================================================
# These are the key dimensions that determine LLM visibility and ranking

GEO_DIMENSIONS = {
    "relevance": {
        "weight": 0.25,
        "description": "How well the content matches user queries and intent",
        "metrics": ["keyword_coverage", "semantic_similarity", "topic_alignment"]
    },
    "authority": {
        "weight": 0.20,
        "description": "Trustworthiness and credibility signals in the content",
        "metrics": ["source_citations", "expertise_indicators", "factual_accuracy"]
    },
    "comprehensiveness": {
        "weight": 0.20,
        "description": "Breadth and depth of information coverage",
        "metrics": ["topic_coverage", "detail_level", "completeness"]
    },
    "clarity": {
        "weight": 0.15,
        "description": "How easily LLMs can extract and understand information",
        "metrics": ["structure_quality", "conciseness", "terminology_clarity"]
    },
    "recency": {
        "weight": 0.10,
        "description": "Freshness and timeliness of information",
        "metrics": ["date_indicators", "current_events", "update_frequency"]
    },
    "actionability": {
        "weight": 0.10,
        "description": "Presence of clear calls-to-action and next steps",
        "metrics": ["cta_presence", "contact_info", "navigation_clarity"]
    }
}

# ============================================================================
# BENCHMARK QUESTION CATEGORIES
# ============================================================================
# Organized by GEO dimension and query intent type

BENCHMARK_QUESTIONS = {
    "informational": {
        "dimension": "relevance",
        "weight": 0.30,
        "questions": [
            "What is the main topic or purpose of this website?",
            "What are the key products, services, or offerings mentioned?",
            "What problem does this organization solve?",
            "What are the main features or benefits described?",
            "What makes this different from competitors?",
        ]
    },
    
    "navigational": {
        "dimension": "actionability",
        "weight": 0.15,
        "questions": [
            "How can I contact this organization?",
            "Where can I find pricing information?",
            "What are the steps to get started or sign up?",
            "Where is this organization located?",
            "How can I access customer support?",
        ]
    },
    
    "transactional": {
        "dimension": "actionability",
        "weight": 0.15,
        "questions": [
            "What actions does the website encourage visitors to take?",
            "Are there any free trials, demos, or samples available?",
            "What payment methods are accepted?",
            "What is the refund or return policy?",
            "Are there any current promotions or discounts?",
        ]
    },
    
    "comparison": {
        "dimension": "comprehensiveness",
        "weight": 0.15,
        "questions": [
            "What are the different pricing tiers or plans available?",
            "What are the pros and cons mentioned about the products/services?",
            "How does this compare to alternative solutions?",
            "What integrations or compatibility options are available?",
            "What are the system requirements or prerequisites?",
        ]
    },
    
    "authority": {
        "dimension": "authority",
        "weight": 0.15,
        "questions": [
            "What credentials, certifications, or expertise does the organization have?",
            "Are there customer testimonials, reviews, or case studies?",
            "What notable clients or partners are mentioned?",
            "Are there any awards, recognitions, or press mentions?",
            "What is the history or background of the organization?",
        ]
    },
    
    "technical": {
        "dimension": "comprehensiveness",
        "weight": 0.10,
        "questions": [
            "What technical specifications or requirements are provided?",
            "Is there documentation or API information available?",
            "What security or privacy measures are mentioned?",
            "What are the technical limitations or constraints?",
            "Are there any technical support resources?",
        ]
    },
}

# ============================================================================
# SCORING THRESHOLDS
# ============================================================================
# Define what constitutes good, average, and poor performance

SCORING_THRESHOLDS = {
    "excellent": {
        "min_score": 85,
        "color": "green",
        "description": "Highly optimized for LLM visibility"
    },
    "good": {
        "min_score": 70,
        "color": "blue",
        "description": "Well-optimized with room for improvement"
    },
    "average": {
        "min_score": 50,
        "color": "yellow",
        "description": "Basic optimization, significant improvements needed"
    },
    "poor": {
        "min_score": 30,
        "color": "orange",
        "description": "Limited optimization, major improvements required"
    },
    "very_poor": {
        "min_score": 0,
        "color": "red",
        "description": "Minimal LLM visibility, comprehensive overhaul needed"
    }
}

# ============================================================================
# CONFIDENCE SCORING
# ============================================================================
# How to interpret retrieval and LLM confidence scores

CONFIDENCE_INTERPRETATION = {
    "retrieval": {
        "excellent": (90, 100),
        "good": (75, 90),
        "fair": (50, 75),
        "poor": (25, 50),
        "very_poor": (0, 25)
    },
    "llm": {
        "high_confidence": (8, 10),
        "medium_confidence": (5, 8),
        "low_confidence": (3, 5),
        "very_low_confidence": (0, 3)
    }
}

# ============================================================================
# OPTIMIZATION RECOMMENDATIONS
# ============================================================================
# Actionable recommendations based on score ranges

RECOMMENDATIONS = {
    "relevance": {
        "low": [
            "Add clear, descriptive headings that match common search queries",
            "Include relevant keywords naturally throughout the content",
            "Create dedicated pages for each main topic or service",
            "Add FAQ sections addressing common user questions",
            "Use semantic HTML structure (h1, h2, etc.) consistently"
        ],
        "medium": [
            "Expand thin content sections with more detailed information",
            "Add related keywords and synonyms to improve semantic coverage",
            "Create topic clusters linking related content together"
        ],
        "high": [
            "Maintain content freshness with regular updates",
            "Monitor emerging search trends and adjust content accordingly"
        ]
    },
    
    "authority": {
        "low": [
            "Add author bios with credentials and expertise",
            "Include customer testimonials and case studies",
            "Display trust badges, certifications, and partnerships",
            "Add 'About Us' section with company history and mission",
            "Link to reputable external sources for claims"
        ],
        "medium": [
            "Gather and display more customer reviews",
            "Create thought leadership content (blog posts, whitepapers)",
            "Highlight notable achievements and milestones"
        ],
        "high": [
            "Continue building social proof and authority signals",
            "Engage in industry publications and speaking opportunities"
        ]
    },
    
    "comprehensiveness": {
        "low": [
            "Add detailed product/service descriptions",
            "Create comprehensive guides and documentation",
            "Include specifications, features, and use cases",
            "Add comparison tables and decision guides",
            "Provide pricing information and plan details"
        ],
        "medium": [
            "Expand existing content with more details and examples",
            "Add visual content (diagrams, infographics) where helpful",
            "Create advanced guides for power users"
        ],
        "high": [
            "Keep comprehensive content updated and accurate",
            "Add emerging topics and advanced features"
        ]
    },
    
    "clarity": {
        "low": [
            "Simplify complex sentences and jargon",
            "Use bullet points and lists for better scannability",
            "Add a clear value proposition at the top of pages",
            "Improve information hierarchy with better headings",
            "Break long paragraphs into shorter, focused sections"
        ],
        "medium": [
            "Add more examples and analogies for complex concepts",
            "Use consistent terminology throughout the site",
            "Improve navigation and internal linking"
        ],
        "high": [
            "Maintain clarity while adding depth",
            "Regular content audits for readability"
        ]
    },
    
    "recency": {
        "low": [
            "Add publication and last updated dates to content",
            "Create a news or blog section with regular updates",
            "Update statistics and data points to current year",
            "Review and refresh outdated content",
            "Add current events or trend mentions where relevant"
        ],
        "medium": [
            "Establish a regular content update schedule",
            "Add timestamp indicators for time-sensitive information",
            "Create a content calendar for ongoing updates"
        ],
        "high": [
            "Maintain update frequency",
            "Monitor industry changes and update accordingly"
        ]
    },
    
    "actionability": {
        "low": [
            "Add clear call-to-action buttons on every page",
            "Create a prominent contact page with multiple contact methods",
            "Add pricing information and 'Get Started' flows",
            "Include next steps and guidance for visitors",
            "Add newsletter signup or lead capture forms"
        ],
        "medium": [
            "Optimize CTA placement and wording",
            "Add more specific action paths for different user segments",
            "Improve form usability and reduce friction"
        ],
        "high": [
            "A/B test CTAs for better conversion",
            "Personalize actions based on user journey"
        ]
    }
}

# ============================================================================
# REPORT CONFIGURATION
# ============================================================================
# Settings for report generation

REPORT_CONFIG = {
    "show_individual_questions": True,
    "show_recommendations": True,
    "show_confidence_details": True,
    "include_benchmarks": True,
    "format": "detailed",  # Options: "summary", "detailed", "technical"
    "visualization": True,
}

# ============================================================================
# QUALITY METRICS
# ============================================================================
# Additional quality indicators for content analysis

QUALITY_METRICS = {
    "content_density": {
        "min_words": 300,
        "optimal_words": 1500,
        "description": "Amount of meaningful content available"
    },
    "structure_score": {
        "min_headings": 3,
        "optimal_headings": 8,
        "description": "Presence of clear content hierarchy"
    },
    "answer_rate": {
        "min_rate": 0.60,
        "optimal_rate": 0.85,
        "description": "Percentage of questions successfully answered"
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_questions():
    """Returns a flat list of all benchmark questions."""
    all_questions = []
    for category, data in BENCHMARK_QUESTIONS.items():
        all_questions.extend(data["questions"])
    return all_questions


def get_weighted_questions():
    """Returns questions with their category weights."""
    weighted_questions = []
    for category, data in BENCHMARK_QUESTIONS.items():
        for question in data["questions"]:
            weighted_questions.append({
                "question": question,
                "category": category,
                "weight": data["weight"],
                "dimension": data["dimension"]
            })
    return weighted_questions


def get_score_rating(score):
    """Returns the rating category for a given score."""
    for rating, config in SCORING_THRESHOLDS.items():
        if score >= config["min_score"]:
            return rating, config
    return "very_poor", SCORING_THRESHOLDS["very_poor"]


def get_recommendations_for_scores(dimension_scores):
    """
    Returns prioritized recommendations based on dimension scores.
    
    Args:
        dimension_scores: Dict of dimension names to scores (0-100)
    
    Returns:
        Dict with recommendations categorized by priority
    """
    recommendations = {
        "critical": [],  # Score < 50
        "important": [],  # Score 50-70
        "nice_to_have": []  # Score 70-85
    }
    
    for dimension, score in dimension_scores.items():
        if dimension not in RECOMMENDATIONS:
            continue
            
        if score < 50:
            priority = "low"
            recommendations["critical"].extend(RECOMMENDATIONS[dimension][priority])
        elif score < 70:
            priority = "medium"
            recommendations["important"].extend(RECOMMENDATIONS[dimension][priority])
        elif score < 85:
            priority = "high"
            recommendations["nice_to_have"].extend(RECOMMENDATIONS[dimension][priority])
    
    return recommendations


if __name__ == "__main__":
    # Test the configuration
    print("=== GEO Benchmark Configuration ===\n")
    
    print(f"Total dimensions: {len(GEO_DIMENSIONS)}")
    print(f"Total question categories: {len(BENCHMARK_QUESTIONS)}")
    print(f"Total questions: {len(get_all_questions())}")
    
    print("\n=== Sample Weighted Questions ===")
    for i, q in enumerate(get_weighted_questions()[:5], 1):
        print(f"{i}. [{q['category']}] {q['question']}")
        print(f"   Weight: {q['weight']}, Dimension: {q['dimension']}\n")
    
    print("=== Score Rating Test ===")
    for score in [95, 75, 55, 35, 15]:
        rating, config = get_score_rating(score)
        print(f"Score {score}: {rating} - {config['description']}")
