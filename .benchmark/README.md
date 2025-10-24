# Docker Build Benchmarking Suite

A comprehensive benchmarking and performance analysis system for Docker builds, designed to measure, analyze, and optimize container build performance.

## Overview

This benchmarking suite provides detailed performance measurements for Docker builds using Buildx and Bake, with automated analysis and optimization recommendations.

## Features

- **Multi-strategy Comparison**: Compare Docker Bake, legacy builds, and Buildx performance
- **Cache Analysis**: Measure cache efficiency and optimization opportunities
- **Layer Analysis**: Examine Dockerfile layer structure and optimization
- **System Profiling**: Hardware and software environment analysis
- **Automated CI/CD**: GitHub Actions integration with performance regression detection
- **Visual Reports**: Charts and graphs for performance visualization
- **Optimization Recommendations**: AI-powered suggestions for performance improvements

## Quick Start

### Run Complete Benchmark Suite

```bash
# Run all benchmarks
./.benchmark/run_benchmark.sh all

# Run specific benchmark types
./.benchmark/run_benchmark.sh build    # Build strategies only
./.benchmark/run_benchmark.sh cache    # Cache performance only
./.benchmark/run_benchmark.sh layers   # Layer analysis only
./.benchmark/run_benchmark.sh disk     # Disk I/O performance
```

### Analyze Results

```bash
# Generate comprehensive analysis report
python .benchmark/analyze_benchmarks.py

# Analyze specific aspects
python .benchmark/analyze_benchmarks.py strategies  # Build strategies
python .benchmark/analyze_benchmarks.py cache       # Cache performance
python .benchmark/analyze_benchmarks.py charts      # Generate charts only
```

### View Results

```bash
# List all benchmark results
./.benchmark/run_benchmark.sh list

# View latest results
cat .benchmark/results/$(ls -t .benchmark/results/ | head -1)

# View analysis reports
cat .benchmark/reports/summaries/$(ls -t .benchmark/reports/summaries/ | head -1)
```

## Directory Structure

```
.benchmark/
├── run_benchmark.sh          # Main benchmark runner script
├── analyze_benchmarks.py     # Analysis and reporting tool
├── benchmark_config.yml      # Configuration file
├── results/                  # Benchmark result files
│   ├── stages/              # Individual stage measurements
│   └── comparisons/         # Benchmark comparisons
├── reports/                 # Analysis reports and summaries
│   ├── charts/             # Performance visualization charts
│   └── summaries/          # Markdown summary reports
└── README.md               # This documentation
```

## Benchmark Types

### 1. Build Strategies (`build`)
Compares different Docker build approaches:
- **Docker Bake** (recommended): Modern build orchestration
- **Docker Bake All**: Multi-target parallel builds
- **Legacy Build**: Traditional `docker build` command
- **Buildx No Cache**: Buildx without cache optimization

### 2. Cache Performance (`cache`)
Measures cache efficiency:
- **Cold Cache**: First build with empty cache
- **Warm Cache**: Subsequent builds with populated cache
- **Hot Cache**: Multiple iterations with full cache

### 3. Layer Analysis (`layers`)
Analyzes Dockerfile structure:
- Layer count and ordering
- Image size analysis
- Build context optimization

### 4. Disk Performance (`disk`)
System I/O benchmarking:
- Read/write speed measurements
- Storage performance impact
- I/O bottleneck identification

## Configuration

The `benchmark_config.yml` file controls benchmarking parameters:

```yaml
benchmark:
  parameters:
    iterations: 3          # Number of test iterations
    timeout: 1800         # Maximum test time (seconds)
    cleanup: true         # Clean resources between tests

thresholds:
  max_build_time:
    dev: 300             # Maximum build time (seconds)
  min_cache_efficiency: 50  # Minimum cache efficiency (%)
```

## CI/CD Integration

### GitHub Actions

The benchmark suite integrates with GitHub Actions for automated performance monitoring:

- **Scheduled Runs**: Weekly performance benchmarks
- **PR Integration**: Automatic benchmarking on pull requests
- **Regression Detection**: Alerts for performance degradation
- **Artifact Storage**: Results and reports stored as artifacts

### Manual Workflow Triggers

```yaml
# Trigger benchmark workflow
gh workflow run benchmark.yml -f benchmark_type=all -f iterations=5
```

## Performance Metrics

### Key Metrics Tracked

- **Build Duration**: Total time for complete build process
- **Cache Hit Ratio**: Percentage of cache-effective operations
- **Layer Efficiency**: Optimization of Dockerfile layer structure
- **Resource Usage**: CPU, memory, and disk utilization
- **Success Rate**: Percentage of successful build operations

### Performance Thresholds

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Build Time | < 120s | 120-300s | > 300s |
| Cache Efficiency | > 50% | 25-50% | < 25% |
| Success Rate | > 95% | 80-95% | < 80% |

## Analysis and Reporting

### Automated Analysis

The analysis tool provides:

1. **Performance Comparison**: Side-by-side strategy comparison
2. **Trend Analysis**: Performance changes over time
3. **Bottleneck Identification**: Slowest stages and optimization opportunities
4. **Recommendations**: Specific improvement suggestions

### Visual Reports

Generated charts include:
- Build strategy performance comparison
- Cache efficiency visualization
- Layer analysis diagrams
- Trend analysis graphs

### Sample Report Output

```
📊 BENCHMARK ANALYSIS SUMMARY
==================================================
🏆 Best Build Strategy: bake_dev (34.2% faster)
⚡ Cache Efficiency: 67.3% (2.1x speedup)
💡 Top Recommendations:
   1. Use bake_dev as the primary build strategy (high priority)
   2. Leverage build cache effectively (high priority)
   3. Focus on layer optimization and cache persistence (medium priority)
==================================================
```

## Optimization Recommendations

### Build Strategy Optimization

1. **Use Docker Bake**: Significantly faster than legacy builds
2. **Enable BuildKit**: Modern build system with advanced caching
3. **Parallel Builds**: Use Bake for multi-target parallel execution

### Cache Optimization

1. **Persistent Volumes**: Use named volumes for cache persistence
2. **Multi-layer Cache**: Cache at different stages (dependencies, compilation, etc.)
3. **Registry Cache**: Leverage remote cache for distributed builds

### Dockerfile Optimization

1. **Layer Ordering**: Place frequently changing instructions later
2. **Multi-stage Builds**: Separate build and runtime stages
3. **Cache Mounts**: Use `--mount=type=cache` for package managers

### System Optimization

1. **Resource Allocation**: Ensure adequate CPU and memory
2. **Storage Performance**: Use fast storage for build cache
3. **Network Optimization**: Optimize registry connectivity

## Troubleshooting

### Common Issues

**Build Timeouts**
```bash
# Increase timeout in configuration
timeout: 3600  # 1 hour
```

**Cache Inefficiency**
```bash
# Check cache mount configuration
docker buildx inspect
```

**Analysis Failures**
```bash
# Install required Python packages
pip install matplotlib numpy
```

### Debug Mode

Enable verbose logging:
```bash
export BUILDKIT_PROGRESS=plain
./.benchmark/run_benchmark.sh all
```

## Contributing

### Adding New Benchmarks

1. Add benchmark logic to `run_benchmark.sh`
2. Update analysis in `analyze_benchmarks.py`
3. Add configuration options to `benchmark_config.yml`
4. Update documentation

### Extending Analysis

1. Add new metrics to the analysis pipeline
2. Create additional visualization types
3. Implement custom recommendation algorithms

## Requirements

- **Docker**: Version 20.10+ with Buildx
- **Python**: Version 3.8+ for analysis
- **Git**: For repository operations
- **Make**: For build orchestration (optional)

### Python Dependencies

```bash
pip install matplotlib numpy PyYAML
```

## License

See repository license file.