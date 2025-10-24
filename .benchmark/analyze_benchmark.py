#!/usr/bin/env python3
"""
Docker Build Benchmark Analyzer
Analyzes benchmark results and provides optimization recommendations
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics

# Optional visualization imports
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

@dataclass
class BenchmarkResult:
    name: str
    duration: float
    success: bool
    exit_code: int

@dataclass
class BenchmarkReport:
    timestamp: str
    system_info: Dict[str, Any]
    build_strategies: List[BenchmarkResult]
    cache_performance: List[BenchmarkResult]
    recommendations: List[Dict[str, Any]]

class BenchmarkAnalyzer:
    def __init__(self, report_file: str):
        self.report_file = report_file
        self.data = self.load_report()

    def load_report(self) -> Dict[str, Any]:
        """Load benchmark report from JSON file"""
        try:
            with open(self.report_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Report file not found: {self.report_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in report file: {e}")
            sys.exit(1)

    def parse_results(self, results: List[Dict]) -> List[BenchmarkResult]:
        """Parse raw results into BenchmarkResult objects"""
        return [
            BenchmarkResult(
                name=result.get('name', 'unknown'),
                duration=float(result.get('duration_seconds', 0)),
                success=result.get('success', False),
                exit_code=result.get('exit_code', -1)
            )
            for result in results
        ]

    def analyze_build_strategies(self) -> Dict[str, Any]:
        """Analyze build strategy performance"""
        strategies = self.parse_results(self.data.get('build_strategies', []))

        if not strategies:
            return {"error": "No build strategy data available"}

        successful_strategies = [s for s in strategies if s.success]
        failed_strategies = [s for s in strategies if not s.success]

        if not successful_strategies:
            return {"error": "No successful build strategies"}

        durations = [s.duration for s in successful_strategies]
        fastest = min(successful_strategies, key=lambda x: x.duration)
        slowest = max(successful_strategies, key=lambda x: x.duration)

        return {
            "total_strategies": len(strategies),
            "successful_strategies": len(successful_strategies),
            "failed_strategies": len(failed_strategies),
            "fastest_strategy": {
                "name": fastest.name,
                "duration": fastest.duration
            },
            "slowest_strategy": {
                "name": slowest.name,
                "duration": slowest.duration
            },
            "average_duration": statistics.mean(durations),
            "duration_stddev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "duration_range": max(durations) - min(durations),
            "performance_ratio": slowest.duration / fastest.duration if fastest.duration > 0 else float('inf')
        }

    def analyze_cache_performance(self) -> Dict[str, Any]:
        """Analyze cache performance improvements"""
        cache_results = self.parse_results(self.data.get('cache_performance', []))

        if len(cache_results) < 2:
            return {"error": "Insufficient cache performance data"}

        # Find cold and warm cache builds
        cold_cache = next((r for r in cache_results if 'cold_cache' in r.name), None)
        warm_cache = next((r for r in cache_results if 'warm_cache' in r.name), None)

        if not cold_cache or not warm_cache:
            return {"error": "Missing cold or warm cache data"}

        if not cold_cache.success or not warm_cache.success:
            return {"error": "Cache builds were not successful"}

        improvement_seconds = cold_cache.duration - warm_cache.duration
        improvement_percentage = (improvement_seconds / cold_cache.duration) * 100

        return {
            "cold_cache_duration": cold_cache.duration,
            "warm_cache_duration": warm_cache.duration,
            "improvement_seconds": improvement_seconds,
            "improvement_percentage": improvement_percentage,
            "cache_effectiveness": "excellent" if improvement_percentage > 50 else
                                 "good" if improvement_percentage > 25 else
                                 "moderate" if improvement_percentage > 10 else "poor"
        }

    def generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate specific optimization recommendations"""
        recommendations = []

        # Analyze build strategies
        build_analysis = self.analyze_build_strategies()
        if "error" not in build_analysis:
            fastest = build_analysis["fastest_strategy"]["name"]
            ratio = build_analysis["performance_ratio"]

            if ratio > 2:
                recommendations.append({
                    "priority": "high",
                    "category": "build_strategy",
                    "title": f"Use {fastest} as primary build strategy",
                    "description": f"{fastest} is {ratio:.1f}x faster than the slowest strategy",
                    "estimated_impact": f"{(ratio-1)*100:.0f}% performance improvement",
                    "implementation": f"Set {fastest} as the default build method in CI/CD"
                })

        # Analyze cache performance
        cache_analysis = self.analyze_cache_performance()
        if "error" not in cache_analysis:
            improvement = cache_analysis["improvement_percentage"]
            effectiveness = cache_analysis["cache_effectiveness"]

            if effectiveness in ["poor", "moderate"]:
                recommendations.append({
                    "priority": "high",
                    "category": "caching",
                    "title": "Improve cache effectiveness",
                    "description": f"Cache provides only {improvement:.1f}% improvement ({effectiveness})",
                    "estimated_impact": "20-50% build time reduction",
                    "implementation": "Optimize Dockerfile layer ordering and cache mount points"
                })

        # Layer analysis recommendations
        layer_info = self.data.get('layer_analysis', {})
        total_layers = layer_info.get('total_layers', 0)

        if total_layers > 50:
            recommendations.append({
                "priority": "medium",
                "category": "layer_optimization",
                "title": "Reduce number of layers",
                "description": f"Dockerfile has {total_layers} layers, consider consolidation",
                "estimated_impact": "10-20% build time reduction",
                "implementation": "Combine RUN commands and use multi-stage builds"
            })

        # System-specific recommendations
        system_info = self.data.get('system_info', {})
        docker_version = system_info.get('docker_version', '')

        if 'buildx' not in docker_version.lower():
            recommendations.append({
                "priority": "high",
                "category": "docker_upgrade",
                "title": "Upgrade to Docker with Buildx",
                "description": "Buildx provides advanced caching and build features",
                "estimated_impact": "30-50% performance improvement",
                "implementation": "Install Docker Desktop or Docker CE with Buildx support"
            })

        return recommendations

    def create_visualizations(self, output_dir: str = "visualizations"):
        """Create performance visualizations"""
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries (matplotlib/seaborn) not available, skipping charts")
            return

        os.makedirs(output_dir, exist_ok=True)

        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")

        # Build strategies comparison
        build_data = self.analyze_build_strategies()
        if "error" not in build_data:
            strategies = self.parse_results(self.data.get('build_strategies', []))
            successful = [s for s in strategies if s.success]

            if successful:
                names = [s.name for s in successful]
                durations = [s.duration for s in successful]

                plt.figure(figsize=(10, 6))
                bars = plt.bar(names, durations)
                plt.title('Build Strategy Performance Comparison')
                plt.xlabel('Build Strategy')
                plt.ylabel('Duration (seconds)')
                plt.xticks(rotation=45, ha='right')

                # Add value labels on bars
                for bar, duration in zip(bars, durations):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           f'{duration:.1f}s', ha='center', va='bottom')

                plt.tight_layout()
                plt.savefig(f'{output_dir}/build_strategies.png', dpi=300, bbox_inches='tight')
                plt.close()

        # Cache performance over time
        cache_data = self.analyze_cache_performance()
        if "error" not in cache_data:
            cache_results = self.parse_results(self.data.get('cache_performance', []))
            if len(cache_results) >= 2:
                names = [r.name.replace('_', ' ').title() for r in cache_results]
                durations = [r.duration for r in cache_results]

                plt.figure(figsize=(8, 6))
                plt.plot(names, durations, marker='o', linewidth=2, markersize=8)
                plt.title('Cache Performance Over Time')
                plt.xlabel('Build Run')
                plt.ylabel('Duration (seconds)')
                plt.grid(True, alpha=0.3)

                # Add improvement annotation
                if len(durations) >= 2:
                    improvement = ((durations[0] - durations[1]) / durations[0]) * 100
                    plt.annotate('.1f',
                               xy=(1, durations[1]), xytext=(0.7, durations[1] + max(durations) * 0.1),
                               arrowprops=dict(arrowstyle='->', color='red'),
                               fontsize=10, color='red')

                plt.tight_layout()
                plt.savefig(f'{output_dir}/cache_performance.png', dpi=300, bbox_inches='tight')
                plt.close()

        print(f"Visualizations saved to: {output_dir}/")

    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
# Docker Build Performance Analysis Report

**Generated:** {analysis_time}
**Report File:** {self.report_file}

## System Information

- **Hostname:** {self.data.get('system_info', {}).get('hostname', 'unknown')}
- **Kernel:** {self.data.get('system_info', {}).get('kernel', 'unknown')} {self.data.get('system_info', {}).get('kernel_version', 'unknown')}
- **Architecture:** {self.data.get('system_info', {}).get('architecture', 'unknown')}
- **CPU:** {self.data.get('system_info', {}).get('cpu_info', 'unknown')}
- **Memory:** {self.data.get('system_info', {}).get('memory', 'unknown')}
- **Docker:** {self.data.get('system_info', {}).get('docker_version', 'unknown')}
- **Buildx:** {self.data.get('system_info', {}).get('buildx_version', 'unknown')}

## Build Strategy Analysis

"""

        build_analysis = self.analyze_build_strategies()
        if "error" in build_analysis:
            report += f"❌ Error: {build_analysis['error']}\n\n"
        else:
            report += f"""✅ **{build_analysis['successful_strategies']}/{build_analysis['total_strategies']}** strategies successful

- **Fastest:** {build_analysis['fastest_strategy']['name']} ({build_analysis['fastest_strategy']['duration']:.1f}s)
- **Slowest:** {build_analysis['slowest_strategy']['name']} ({build_analysis['slowest_strategy']['duration']:.1f}s)
- **Average:** {build_analysis['average_duration']:.1f}s
- **Performance Ratio:** {build_analysis['performance_ratio']:.1f}x

"""

        # Cache analysis
        report += "## Cache Performance Analysis\n\n"
        cache_analysis = self.analyze_cache_performance()
        if "error" in cache_analysis:
            report += f"❌ Error: {cache_analysis['error']}\n\n"
        else:
            report += f"""✅ Cache effectiveness: **{cache_analysis['cache_effectiveness'].upper()}**

- **Cold Cache:** {cache_analysis['cold_cache_duration']:.1f}s
- **Warm Cache:** {cache_analysis['warm_cache_duration']:.1f}s
- **Improvement:** {cache_analysis['improvement_percentage']:.1f}% ({cache_analysis['improvement_seconds']:.1f}s faster)

"""

        # Recommendations
        report += "## Optimization Recommendations\n\n"
        recommendations = self.generate_optimization_recommendations()

        if not recommendations:
            report += "✅ No optimization recommendations needed.\n\n"
        else:
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
                report += f"""### {i}. {priority_emoji} {rec['title']} ({rec['priority'].upper()} PRIORITY)

**Description:** {rec['description']}

**Estimated Impact:** {rec['estimated_impact']}

**Implementation:** {rec['implementation']}

"""

        return report

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_benchmark.py <report_file>")
        sys.exit(1)

    report_file = sys.argv[1]

    if not os.path.exists(report_file):
        print(f"Error: Report file not found: {report_file}")
        sys.exit(1)

    analyzer = BenchmarkAnalyzer(report_file)

    # Generate text report
    report = analyzer.generate_report()
    print(report)

    # Create visualizations
    try:
        analyzer.create_visualizations()
    except ImportError:
        print("Warning: matplotlib/seaborn not available, skipping visualizations")
    except Exception as e:
        print(f"Warning: Failed to create visualizations: {e}")

    # Save recommendations to file
    recommendations = analyzer.generate_optimization_recommendations()
    if recommendations:
        rec_file = report_file.replace('.json', '_recommendations.json')
        with open(rec_file, 'w') as f:
            json.dump(recommendations, f, indent=2)
        print(f"\n💡 Recommendations saved to: {rec_file}")

if __name__ == "__main__":
    main()