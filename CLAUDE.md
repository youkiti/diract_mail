# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository analyzes the relationship between direct mail (DMS) distribution and voting outcomes for Team Mirai (チームみらい) across Kyoto's administrative districts, incorporating demographic factors.

## Quick Start

```bash
# Activate virtual environment and run complete analysis
source venv/bin/activate
python run_analysis.py
```

This single command processes raw data, performs statistical analysis, and generates all visualizations.

## Files Structure

### Input Files (Required)
- `dms.csv`: DMS distribution data (Shift-JIS encoded)
- `kyoto_demographic_team_mirai_votes.csv`: Demographic and voting data

### Core Scripts
- `run_analysis.py`: Main script that runs the entire pipeline
- `process_dms_final.py`: Processes raw DMS data and merges with demographics
- `analyze_dms_votes.py`: Performs regression analysis and creates visualizations

### Output Files (Generated)
- `merged_demographic_dms.csv`: Final integrated dataset
- `dms_aggregated.csv`: DMS counts by district
- `regression_analysis_results.txt`: Statistical analysis results
- `dms_vote_scatter.png`: Scatter plot with regression line
- `correlation_matrix.png`: Correlation matrix heatmap

## Data Pipeline

1. Convert DMS data from Shift-JIS to UTF-8
2. Parse and aggregate DMS counts by district and type (機関誌/確認団体ビラ)
3. Merge with demographic data
4. Perform simple and multiple regression analysis
5. Generate visualizations with Japanese font support

## Dependencies

The virtual environment includes: pandas, numpy, matplotlib, seaborn, scipy, statsmodels, japanize-matplotlib, setuptools

## Analysis Context

Data manually collected from https://action.team-mir.ai/map/posting. Sample limited to 11 Kyoto districts. Statistical significance limited due to small sample size.