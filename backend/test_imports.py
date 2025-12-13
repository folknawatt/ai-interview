#!/usr/bin/env python
"""Test imports for domain models."""
import sys
import traceback

try:
    print("Testing domain models import...")
    from app.domain.models import Evaluation, AggregatedScore
    print("✓ Domain models imported successfully")
except Exception as e:
    print(f"✗ Domain models import failed:")
    traceback.print_exc()

try:
    print("\nTesting evaluator import...")
    from app.domain.scoring.evaluator import evaluate_candidate
    print("✓ Evaluator imported successfully")
except Exception as e:
    print(f"✗ Evaluator import failed:")
    traceback.print_exc()

try:
    print("\nTesting aggregator import...")
    from app.domain.scoring.aggregator import calculate_aggregated_score
    print("✓ Aggregator imported successfully")
except Exception as e:
    print(f"✗ Aggregator import failed:")
    traceback.print_exc()

try:
    print("\nTesting service import...")
    from app.services.interview_service import InterviewService
    print("✓ Service imported successfully")
except Exception as e:
    print(f"✗ Service import failed:")
    traceback.print_exc()

print("\nAll tests completed!")
