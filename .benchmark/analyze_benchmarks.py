#!/usr/bin/env python3
"""
Docker Build Benchmark Analysis Tool

This script analyzes benchmark results and provides detailed insights,
recommendations, and optimization suggestions for Docker builds.
"""

import json
import os
import sys
import statistics
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import numpy as np

class BenchmarkAnalyzer:
    def __init__(self, results_dir: str = ".benchmark/results"):
        self.results_dir = Path(results_dir)
        self.reports_dir = Path(".benchmark/reports")
        self.charts_dir = self.reports_dir / "charts"
        self.summaries_dir = self.reports_dir / "summaries"

        # Create directories
        for dir_path in [self.reports_dir, self.charts_dir, self.summaries_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def load_benchmark_results(self) -> List[Dict[str, Any]]:
        """Load all benchmark result files."""
        results = []
        if not self.results_dir.exists():
            print(f"Results directory not found: {self.results_dir}")
            return results

        for file_path in self.results_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    data['_file_path'] = file_path
                    results.append(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading {file_path}: {e}")

        return sorted(results, key=lambda x: x.get('benchmark_report', {}).get('generated_at', ''), reverse=True)

    def analyze_build_strategies(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze build strategy performance."""
        strategies_data = []

        for result in results:
            if 'build_strategies' in result:
                for strategy in result['build_strategies']:
                    strategies_data.append({
                        'name': strategy['name'],
                        'duration': strategy['duration_seconds'],
                        'success': strategy['success'],
                        'run_id': result.get('benchmark_report', {}).get('generated_at', 'unknown')
                    })

        if not strategies_data:
            return {}

        # Group by strategy name
        strategy_groups = {}
        for data in strategies_data:
            name = data['name']
            if name not in strategy_groups:
                strategy_groups[name] = []
            strategy_groups[name].append(data['duration'])

        # Calculate statistics for each strategy
        analysis = {}
        for name, durations in strategy_groups.items():
            analysis[name] = {
                'count': len(durations),
                'mean': statistics.mean(durations),
                'median': statistics.median(durations),
                'min': min(durations),
                'max': max(durations),
                'std_dev': statistics.stdev(durations) if len(durations) > 1 else 0,
                'success_rate': len([d for d in durations if d > 0]) / len(durations)
            }

        # Find best strategy
        best_strategy = min(analysis.items(), key=lambda x: x[1]['mean'])
        analysis['_best_strategy'] = best_strategy[0]
        analysis['_performance_gain'] = (max(s['mean'] for s in analysis.values() if isinstance(s, dict)) - best_strategy[1]['mean']) / best_strategy[1]['mean'] * 100

        return analysis

    def analyze_cache_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cache performance across builds."""
        cache_data = []

        for result in results:
            if 'cache_performance' in result:
                for perf in result['cache_performance']:
                    cache_data.append({
                        'name': perf['name'],
                        'duration': perf['duration_seconds'],
                        'run_id': result.get('benchmark_report', {}).get('generated_at', 'unknown')
                    })

        if not cache_data:
            return {}

        # Group by cache type
        cache_groups = {}
        for data in cache_data:
            name = data['name']
            if name not in cache_groups:
                cache_groups[name] = []
            cache_groups[name].append(data['duration'])

        # Calculate cache efficiency
        analysis = {}
        cold_cache_times = cache_groups.get('cold_cache_build', [])
        warm_cache_times = cache_groups.get('warm_cache_build', [])

        if cold_cache_times and warm_cache_times:
            cold_avg = statistics.mean(cold_cache_times)
            warm_avg = statistics.mean(warm_cache_times)
            cache_efficiency = (cold_avg - warm_avg) / cold_avg * 100

            analysis = {
                'cold_cache_avg': cold_avg,
                'warm_cache_avg': warm_avg,
                'cache_efficiency_percent': cache_efficiency,
                'speedup_factor': cold_avg / warm_avg if warm_avg > 0 else 0
            }

        return analysis

    def analyze_system_factors(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze system performance factors."""
        system_data = []

        for result in results:
            system_info = result.get('system_info', {}).get('system', {})
            if system_info:
                system_data.append(system_info)

        if not system_data:
            return {}

        # Analyze Docker versions
        docker_versions = [s.get('docker_version', 'unknown') for s in system_data]
        buildx_versions = [s.get('buildx_version', 'unknown') for s in system_data]

        return {
            'unique_docker_versions': list(set(docker_versions)),
            'unique_buildx_versions': list(set(buildx_versions)),
            'total_runs': len(system_data)
        }

    def generate_recommendations(self, strategy_analysis: Dict, cache_analysis: Dict) -> List[Dict[str, str]]:
        """Generate optimization recommendations."""
        recommendations = []

        # Build strategy recommendations
        if strategy_analysis:
            best_strategy = strategy_analysis.get('_best_strategy')
            performance_gain = strategy_analysis.get('_performance_gain', 0)

            if best_strategy and performance_gain > 10:
                recommendations.append({
                    'category': 'build_strategy',
                    'priority': 'high',
                    'title': f'Use {best_strategy} for optimal performance',
                    'description': f'{best_strategy} is {performance_gain:.1f}% faster than other strategies',
                    'impact': 'high',
                    'effort': 'low'
                })

        # Cache recommendations
        if cache_analysis:
            cache_efficiency = cache_analysis.get('cache_efficiency_percent', 0)
            speedup_factor = cache_analysis.get('speedup_factor', 1)

            if cache_efficiency > 50:
                recommendations.append({
                    'category': 'cache_optimization',
                    'priority': 'high',
                    'title': 'Leverage build cache effectively',
                    'description': f'Cache provides {cache_efficiency:.1f}% performance improvement ({speedup_factor:.1f}x speedup)',
                    'impact': 'high',
                    'effort': 'medium'
                })

        # Layer optimization recommendations
        recommendations.extend([
            {
                'category': 'layer_optimization',
                'priority': 'medium',
                'title': 'Optimize Dockerfile layer structure',
                'description': 'Reorder RUN commands to maximize layer cache hits',
                'impact': 'medium',
                'effort': 'medium'
            },
            {
                'category': 'dependency_management',
                'priority': 'medium',
                'title': 'Use multi-stage builds for dependencies',
                'description': 'Separate build dependencies from runtime to reduce image size',
                'impact': 'medium',
                'effort': 'high'
            },
            {
                'category': 'parallel_builds',
                'priority': 'low',
                'title': 'Implement parallel target building',
                'description': 'Use Docker Bake to build multiple targets simultaneously',
                'impact': 'low',
                'effort': 'low'
            }
        ])

        return recommendations

    def create_performance_chart(self, strategy_analysis: Dict, output_file: str):
        """Create a performance comparison chart."""
        if not strategy_analysis:
            return

        # Filter out metadata keys
        strategies = {k: v for k, v in strategy_analysis.items() if not k.startswith('_')}

        if not strategies:
            return

        names = list(strategies.keys())
        means = [s['mean'] for s in strategies.values()]
        std_devs = [s['std_dev'] for s in strategies.values()]

        x_pos = np.arange(len(names))

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(x_pos, means, yerr=std_devs, capsize=5,
                     color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

        ax.set_ylabel('Build Time (seconds)')
        ax.set_title('Docker Build Strategy Performance Comparison')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(names, rotation=45, ha='right')

        # Add value labels on bars
        for bar, mean in zip(bars, means):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(std_devs) * 0.1,
                   '.1f', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Performance chart saved: {output_file}")

    def create_cache_efficiency_chart(self, cache_analysis: Dict, output_file: str):
        """Create a cache efficiency visualization."""
        if not cache_analysis:
            return

        labels = ['Cold Cache', 'Warm Cache']
        times = [
            cache_analysis.get('cold_cache_avg', 0),
            cache_analysis.get('warm_cache_avg', 0)
        ]

        efficiency = cache_analysis.get('cache_efficiency_percent', 0)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Bar chart
        bars = ax1.bar(labels, times, color=['#ff6b6b', '#4ecdc4'])
        ax1.set_ylabel('Build Time (seconds)')
        ax1.set_title('Cache Performance Comparison')
        ax1.grid(True, alpha=0.3)

        # Add value labels
        for bar, time in zip(bars, times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + max(times) * 0.02,
                    '.1f', ha='center', va='bottom')

        # Efficiency gauge
        ax2.pie([efficiency, 100-efficiency], labels=[f'Efficient\n{efficiency:.1f}%', f'Inefficient\n{100-efficiency:.1f}%'],
               colors=['#4ecdc4', '#ff6b6b'], autopct='%1.1f%%', startangle=90)
        ax2.set_title('Cache Efficiency')
        ax2.axis('equal')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Cache efficiency chart saved: {output_file}")

    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report."""
        print("🔍 Analyzing benchmark results...")

        results = self.load_benchmark_results()
        if not results:
            print("No benchmark results found. Run benchmarks first.")
            return

        print(f"Loaded {len(results)} benchmark results")

        # Perform analyses
        strategy_analysis = self.analyze_build_strategies(results)
        cache_analysis = self.analyze_cache_performance(results)
        system_analysis = self.analyze_system_factors(results)
        recommendations = self.generate_recommendations(strategy_analysis, cache_analysis)

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create charts
        if strategy_analysis:
            chart_file = self.charts_dir / f"build_performance_{timestamp}.png"
            self.create_performance_chart(strategy_analysis, str(chart_file))

        if cache_analysis:
            cache_chart_file = self.charts_dir / f"cache_efficiency_{timestamp}.png"
            self.create_cache_efficiency_chart(cache_analysis, str(cache_chart_file))

        # Generate comprehensive report
        report_file = self.summaries_dir / f"analysis_report_{timestamp}.md"

        with open(report_file, 'w') as f:
            f.write("# Docker Build Performance Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Benchmark Runs:** {len(results)}\n\n")

            # System Information
            f.write("## System Information\n\n")
            if system_analysis:
                f.write(f"- **Docker Versions:** {', '.join(system_analysis['unique_docker_versions'])}\n")
                f.write(f"- **Buildx Versions:** {', '.join(system_analysis['unique_buildx_versions'])}\n")
                f.write(f"- **Total Runs:** {system_analysis['total_runs']}\n")
            f.write("\n")

            # Build Strategy Analysis
            if strategy_analysis:
                f.write("## Build Strategy Analysis\n\n")
                best_strategy = strategy_analysis.get('_best_strategy')
                performance_gain = strategy_analysis.get('_performance_gain', 0)

                if best_strategy:
                    f.write(f"**Recommended Strategy:** {best_strategy} ")
                    f.write(".1f"                    f.write("\n\n")

                f.write("### Strategy Performance\n\n")
                f.write("| Strategy | Mean Time | Median | Min | Max | Std Dev | Success Rate |\n")
                f.write("|----------|-----------|--------|-----|-----|---------|--------------|\n")

                for name, stats in strategy_analysis.items():
                    if not name.startswith('_'):
                        f.write(f"| {name} | {stats['mean']:.2f}s | {stats['median']:.2f}s | ")
                        f.write(f"{stats['min']:.2f}s | {stats['max']:.2f}s | ")
                        f.write(f"{stats['std_dev']:.2f}s | {stats['success_rate']:.1%} |\n")

                f.write("\n")

            # Cache Performance Analysis
            if cache_analysis:
                f.write("## Cache Performance Analysis\n\n")
                efficiency = cache_analysis.get('cache_efficiency_percent', 0)
                speedup = cache_analysis.get('speedup_factor', 1)

                f.write(f"- **Cache Efficiency:** {efficiency:.1f}%\n")
                f.write(f"- **Speedup Factor:** {speedup:.1f}x\n")
                f.write(f"- **Cold Cache Avg:** {cache_analysis.get('cold_cache_avg', 0):.2f}s\n")
                f.write(f"- **Warm Cache Avg:** {cache_analysis.get('warm_cache_avg', 0):.2f}s\n\n")

            # Recommendations
            f.write("## Optimization Recommendations\n\n")
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"### {i}. {rec['title']}\n\n")
                    f.write(f"**Priority:** {rec['priority'].title()}\n")
                    f.write(f"**Impact:** {rec['impact'].title()}\n")
                    f.write(f"**Effort:** {rec['effort'].title()}\n\n")
                    f.write(f"{rec['description']}\n\n")
            else:
                f.write("No specific recommendations available.\n\n")

            # Charts
            if (self.charts_dir / f"build_performance_{timestamp}.png").exists():
                f.write("## Performance Charts\n\n")
                f.write(f"![Build Performance](charts/build_performance_{timestamp}.png)\n\n")

            if (self.charts_dir / f"cache_efficiency_{timestamp}.png").exists():
                f.write(f"![Cache Efficiency](charts/cache_efficiency_{timestamp}.png)\n\n")

        print(f"✅ Comprehensive analysis report generated: {report_file}")

        # Print summary to console
        self.print_summary(strategy_analysis, cache_analysis, recommendations)

    def print_summary(self, strategy_analysis: Dict, cache_analysis: Dict, recommendations: List[Dict]):
        """Print a summary of the analysis to console."""
        print("\n" + "="*60)
        print("📊 BENCHMARK ANALYSIS SUMMARY")
        print("="*60)

        if strategy_analysis:
            best = strategy_analysis.get('_best_strategy')
            gain = strategy_analysis.get('_performance_gain', 0)
            print(f"🏆 Best Build Strategy: {best} ({gain:.1f}% faster)")

        if cache_analysis:
            efficiency = cache_analysis.get('cache_efficiency_percent', 0)
            speedup = cache_analysis.get('speedup_factor', 1)
            print(f"⚡ Cache Efficiency: {efficiency:.1f}% ({speedup:.1f}x speedup)")

        print(f"💡 Top Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec['title']} ({rec['priority']} priority)")

        print("="*60)

def main():
    analyzer = BenchmarkAnalyzer()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "strategies":
            results = analyzer.load_benchmark_results()
            analysis = analyzer.analyze_build_strategies(results)
            print(json.dumps(analysis, indent=2))

        elif command == "cache":
            results = analyzer.load_benchmark_results()
            analysis = analyzer.analyze_cache_performance(results)
            print(json.dumps(analysis, indent=2))

        elif command == "charts":
            results = analyzer.load_benchmark_results()
            strategy_analysis = analyzer.analyze_build_strategies(results)
            cache_analysis = analyzer.analyze_cache_performance(results)

            if strategy_analysis:
                analyzer.create_performance_chart(strategy_analysis, ".benchmark/charts/performance.png")
            if cache_analysis:
                analyzer.create_cache_efficiency_chart(cache_analysis, ".benchmark/charts/cache.png")

        else:
            print(f"Unknown command: {command}")
            print("Available commands: strategies, cache, charts")

    else:
        analyzer.generate_comprehensive_report()

if __name__ == "__main__":
    main()