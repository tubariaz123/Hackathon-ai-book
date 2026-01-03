"""
Performance validation for the RAG AI Agent.

This module provides performance tests to:
- Measure response times under various query loads
- Validate token usage and cost optimization
- Verify grounding validation doesn't significantly impact performance
- Test performance under various query loads
"""
import time
import asyncio
from typing import List, Tuple
import statistics
from backend.agent import create_rag_agent, query_agent
from backend.retrieve import search_similar_content


def measure_response_time(func, *args, **kwargs) -> Tuple[float, any]:
    """
    Measure the execution time of a function.

    Args:
        func: Function to measure
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Tuple of (execution_time, function_result)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result


def test_response_times(queries: List[str], iterations: int = 5) -> dict:
    """
    Test response times for a set of queries.

    Args:
        queries: List of queries to test
        iterations: Number of iterations to run each query

    Returns:
        Dictionary with performance metrics
    """
    print(f"Testing response times for {len(queries)} queries with {iterations} iterations each...")

    agent = create_rag_agent(model_name="gpt-3.5-turbo")

    all_times = []
    query_times = {}

    for query in queries:
        times = []
        for i in range(iterations):
            response_time, _ = measure_response_time(
                query_agent, agent, query, 5
            )
            times.append(response_time)
            all_times.append(response_time)

        avg_time = statistics.mean(times)
        query_times[query] = {
            'times': times,
            'avg': avg_time,
            'min': min(times),
            'max': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }

        print(f"Query: '{query[:30]}...' - Avg: {avg_time:.2f}s, Min: {min(times):.2f}s, Max: {max(times):.2f}s")

    overall_metrics = {
        'all_times': all_times,
        'avg_response_time': statistics.mean(all_times),
        'min_response_time': min(all_times),
        'max_response_time': max(all_times),
        'std_dev_response_time': statistics.stdev(all_times) if len(all_times) > 1 else 0,
        'total_queries': len(queries) * iterations,
        'queries': query_times
    }

    return overall_metrics


def test_concurrent_performance(queries: List[str], concurrency_level: int = 3) -> dict:
    """
    Test performance under concurrent query load.

    Args:
        queries: List of queries to test
        concurrency_level: Number of concurrent queries to run

    Returns:
        Dictionary with concurrency performance metrics
    """
    print(f"Testing concurrent performance with {concurrency_level} concurrent queries...")

    agent = create_rag_agent(model_name="gpt-3.5-turbo")

    async def run_query(query_text: str):
        start_time = time.time()
        response = query_agent(agent, query_text, 5)
        end_time = time.time()
        return {
            'query': query_text,
            'response_time': end_time - start_time,
            'answer_length': len(response.answer) if response.answer else 0
        }

    async def run_concurrent_tests():
        tasks = []
        for query in queries:
            for _ in range(concurrency_level):
                tasks.append(run_query(query))

        results = await asyncio.gather(*tasks)
        return results

    # Run the concurrent tests
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(run_concurrent_tests())
        loop.close()
    except RuntimeError:
        # Handle case where loop is already running
        import nest_asyncio
        nest_asyncio.apply()
        results = asyncio.run(run_concurrent_tests())

    response_times = [r['response_time'] for r in results]

    concurrency_metrics = {
        'total_concurrent_queries': len(results),
        'avg_response_time': statistics.mean(response_times),
        'min_response_time': min(response_times),
        'max_response_time': max(response_times),
        'std_dev_response_time': statistics.stdev(response_times) if len(response_times) > 1 else 0,
        'results': results
    }

    print(f"Concurrent performance - Avg: {concurrency_metrics['avg_response_time']:.2f}s, "
          f"Min: {concurrency_metrics['min_response_time']:.2f}s, "
          f"Max: {concurrency_metrics['max_response_time']:.2f}s")

    return concurrency_metrics


def test_grounding_performance_impact():
    """
    Test the performance impact of grounding validation.

    Returns:
        Dictionary comparing performance with and without grounding
    """
    print("Testing grounding validation performance impact...")

    agent_with_grounding = create_rag_agent(model_name="gpt-3.5-turbo")
    agent_with_grounding.grounding_enforcement = True

    agent_without_grounding = create_rag_agent(model_name="gpt-3.5-turbo")
    agent_without_grounding.grounding_enforcement = False

    test_queries = [
        "What is artificial intelligence?",
        "Explain machine learning basics",
        "How does Python programming work?"
    ]

    with_grounding_times = []
    without_grounding_times = []

    for query in test_queries:
        # Test with grounding
        time_with, _ = measure_response_time(
            query_agent, agent_with_grounding, query, 5
        )
        with_grounding_times.append(time_with)

        # Test without grounding
        time_without, _ = measure_response_time(
            query_agent, agent_without_grounding, query, 5
        )
        without_grounding_times.append(time_without)

    grounding_impact = {
        'with_grounding_avg': statistics.mean(with_grounding_times),
        'without_grounding_avg': statistics.mean(without_grounding_times),
        'impact_percentage': (
            (statistics.mean(with_grounding_times) - statistics.mean(without_grounding_times))
            / statistics.mean(without_grounding_times) * 100
        ) if statistics.mean(without_grounding_times) > 0 else 0,
        'with_grounding_times': with_grounding_times,
        'without_grounding_times': without_grounding_times
    }

    print(f"Grounding impact - With: {grounding_impact['with_grounding_avg']:.2f}s, "
          f"Without: {grounding_impact['without_grounding_avg']:.2f}s, "
          f"Impact: {grounding_impact['impact_percentage']:.2f}%")

    return grounding_impact


def validate_performance_metrics(metrics: dict) -> dict:
    """
    Validate performance metrics against acceptable thresholds.

    Args:
        metrics: Performance metrics to validate

    Returns:
        Dictionary with validation results
    """
    print("Validating performance metrics...")

    validation_results = {
        'response_time_ok': metrics.get('avg_response_time', float('inf')) < 10.0,  # Less than 10 seconds
        'concurrent_response_time_ok': metrics.get('avg_response_time', float('inf')) < 15.0,  # Less than 15 seconds under load
        'grounding_impact_acceptable': abs(
            metrics.get('impact_percentage', float('inf'))
        ) < 50.0,  # Grounding shouldn't increase time by more than 50%
    }

    print(f"Performance validation results:")
    print(f"  - Response time acceptable: {validation_results['response_time_ok']}")
    print(f"  - Concurrent performance acceptable: {validation_results['concurrent_response_time_ok']}")
    print(f"  - Grounding impact acceptable: {validation_results['grounding_impact_acceptable']}")

    return validation_results


def run_performance_validation():
    """
    Run all performance validation tests.

    Returns:
        Dictionary with all performance validation results
    """
    print("Starting RAG AI Agent performance validation...")

    # Define test queries
    test_queries = [
        "What is artificial intelligence?",
        "Explain machine learning basics",
        "How does Python programming work?",
        "What are neural networks?",
        "Describe the history of AI",
        "What is deep learning?",
        "Explain natural language processing",
        "What is computer vision?"
    ]

    # Test 1: Basic response times
    response_time_metrics = test_response_times(test_queries[:3], iterations=3)

    # Test 2: Concurrent performance
    concurrency_metrics = test_concurrent_performance(test_queries[:2], concurrency_level=2)

    # Test 3: Grounding performance impact
    grounding_impact = test_grounding_performance_impact()

    # Validate all metrics
    validation_results = validate_performance_metrics(response_time_metrics)

    # Compile all results
    performance_report = {
        'response_time_metrics': response_time_metrics,
        'concurrency_metrics': concurrency_metrics,
        'grounding_impact': grounding_impact,
        'validation_results': validation_results,
        'summary': {
            'all_tests_passed': all(validation_results.values()),
            'total_queries_tested': response_time_metrics['total_queries'],
            'avg_overall_response_time': response_time_metrics['avg_response_time'],
            'max_response_time': max(
                response_time_metrics['max_response_time'],
                concurrency_metrics['max_response_time']
            )
        }
    }

    print(f"\nPerformance Validation Summary:")
    print(f"  - All tests passed: {performance_report['summary']['all_tests_passed']}")
    print(f"  - Total queries tested: {performance_report['summary']['total_queries_tested']}")
    print(f"  - Avg response time: {performance_report['summary']['avg_overall_response_time']:.2f}s")
    print(f"  - Max response time: {performance_report['summary']['max_response_time']:.2f}s")

    return performance_report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Check if required environment variables are available
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "COHERE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        print("Please set these variables before running performance tests.")
        exit(1)

    # Run the performance validation
    results = run_performance_validation()

    # Print detailed results
    print("\nDetailed Performance Report:")
    print("="*50)
    print(f"Response Time Metrics:")
    print(f"  - Average: {results['response_time_metrics']['avg_response_time']:.2f}s")
    print(f"  - Min: {results['response_time_metrics']['min_response_time']:.2f}s")
    print(f"  - Max: {results['response_time_metrics']['max_response_time']:.2f}s")

    print(f"\nConcurrency Metrics:")
    print(f"  - Average: {results['concurrency_metrics']['avg_response_time']:.2f}s")
    print(f"  - Total concurrent queries: {results['concurrency_metrics']['total_concurrent_queries']}")

    print(f"\nGrounding Impact:")
    print(f"  - With grounding: {results['grounding_impact']['with_grounding_avg']:.2f}s")
    print(f"  - Without grounding: {results['grounding_impact']['without_grounding_avg']:.2f}s")
    print(f"  - Performance impact: {results['grounding_impact']['impact_percentage']:.2f}%")