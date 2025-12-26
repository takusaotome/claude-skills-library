#!/usr/bin/env python3
"""
Bug Analysis Script for QA Management
Analyzes bug ticket data to identify quality trends and provide improvement recommendations.
"""

import argparse
import json
import csv
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import statistics


class BugAnalyzer:
    """
    Comprehensive bug analysis engine for quality management.
    Provides statistical analysis, trend identification, and improvement recommendations.
    """

    def __init__(self):
        self.bugs: List[Dict[str, Any]] = []
        self.analysis_results: Dict[str, Any] = {}

    def load_csv(self, file_path: str) -> None:
        """Load bug data from CSV file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.bugs = list(reader)

    def load_json(self, file_path: str) -> None:
        """Load bug data from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both array and object with 'issues' key
            if isinstance(data, list):
                self.bugs = data
            elif isinstance(data, dict) and 'issues' in data:
                self.bugs = data['issues']
            else:
                self.bugs = [data]

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats."""
        if not date_str or date_str.lower() in ['', 'none', 'null', 'n/a']:
            return None

        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None

    def calculate_resolution_days(self, created: str, resolved: str) -> Optional[int]:
        """Calculate days between creation and resolution."""
        created_date = self.parse_date(created)
        resolved_date = self.parse_date(resolved)

        if created_date and resolved_date:
            delta = resolved_date - created_date
            return max(0, delta.days)
        return None

    def analyze_severity_distribution(self) -> Dict[str, Any]:
        """Analyze bug distribution by severity/priority."""
        severity_counts = Counter()
        severity_field = self._find_field(['severity', 'priority', 'importance', 'criticality'])

        for bug in self.bugs:
            severity = bug.get(severity_field, 'Unknown').strip()
            if severity:
                severity_counts[severity] += 1

        total = sum(severity_counts.values())
        distribution = {
            severity: {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0
            }
            for severity, count in severity_counts.most_common()
        }

        return {
            'distribution': distribution,
            'total_bugs': total,
            'unique_severities': len(severity_counts)
        }

    def analyze_category_distribution(self) -> Dict[str, Any]:
        """Analyze bug distribution by category/type."""
        category_counts = Counter()
        category_field = self._find_field(['category', 'type', 'bug_type', 'classification'])

        for bug in self.bugs:
            category = bug.get(category_field, 'Unknown').strip()
            if category:
                category_counts[category] += 1

        total = sum(category_counts.values())
        distribution = {
            category: {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0
            }
            for category, count in category_counts.most_common()
        }

        return {
            'distribution': distribution,
            'total_bugs': total,
            'top_categories': category_counts.most_common(5)
        }

    def analyze_module_distribution(self) -> Dict[str, Any]:
        """Analyze bug distribution by module/feature/component."""
        module_counts = Counter()
        module_field = self._find_field(['module', 'component', 'feature', 'area', 'functionality'])

        for bug in self.bugs:
            module = bug.get(module_field, 'Unknown').strip()
            if module:
                module_counts[module] += 1

        total = sum(module_counts.values())

        # Calculate concentration metrics
        top_3_count = sum(count for _, count in module_counts.most_common(3))
        concentration_ratio = round(top_3_count / total * 100, 2) if total > 0 else 0

        distribution = {
            module: {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0
            }
            for module, count in module_counts.most_common()
        }

        return {
            'distribution': distribution,
            'total_bugs': total,
            'unique_modules': len(module_counts),
            'top_3_modules': module_counts.most_common(3),
            'concentration_ratio': concentration_ratio
        }

    def analyze_resolution_time(self) -> Dict[str, Any]:
        """Analyze bug resolution time metrics."""
        resolution_days = []
        created_field = self._find_field(['created_date', 'created', 'opened_date', 'reported_date'])
        resolved_field = self._find_field(['resolved_date', 'resolved', 'closed_date', 'fixed_date'])

        for bug in self.bugs:
            created = bug.get(created_field, '')
            resolved = bug.get(resolved_field, '')
            days = self.calculate_resolution_days(created, resolved)
            if days is not None:
                resolution_days.append(days)

        if not resolution_days:
            return {
                'total_resolved': 0,
                'message': 'No resolution time data available'
            }

        # Calculate percentiles
        sorted_days = sorted(resolution_days)
        n = len(sorted_days)

        return {
            'total_resolved': len(resolution_days),
            'average_days': round(statistics.mean(resolution_days), 2),
            'median_days': round(statistics.median(resolution_days), 2),
            'min_days': min(resolution_days),
            'max_days': max(resolution_days),
            'std_dev': round(statistics.stdev(resolution_days), 2) if len(resolution_days) > 1 else 0,
            'percentile_50': sorted_days[n // 2],
            'percentile_75': sorted_days[int(n * 0.75)],
            'percentile_90': sorted_days[int(n * 0.90)],
            'distribution': {
                '0-3_days': len([d for d in resolution_days if d <= 3]),
                '4-7_days': len([d for d in resolution_days if 4 <= d <= 7]),
                '8-14_days': len([d for d in resolution_days if 8 <= d <= 14]),
                '15-30_days': len([d for d in resolution_days if 15 <= d <= 30]),
                '30+_days': len([d for d in resolution_days if d > 30]),
            }
        }

    def analyze_status_distribution(self) -> Dict[str, Any]:
        """Analyze bug status distribution."""
        status_counts = Counter()
        status_field = self._find_field(['status', 'state', 'current_status'])

        for bug in self.bugs:
            status = bug.get(status_field, 'Unknown').strip()
            if status:
                status_counts[status] += 1

        total = sum(status_counts.values())

        # Categorize statuses
        open_statuses = ['open', 'new', 'assigned', 'in progress', 'reopened', 'active']
        closed_statuses = ['closed', 'resolved', 'fixed', 'completed', 'done']

        open_count = sum(count for status, count in status_counts.items()
                        if status.lower() in open_statuses)
        closed_count = sum(count for status, count in status_counts.items()
                          if status.lower() in closed_statuses)
        other_count = total - open_count - closed_count

        return {
            'distribution': dict(status_counts.most_common()),
            'total_bugs': total,
            'open_bugs': open_count,
            'closed_bugs': closed_count,
            'other_bugs': other_count,
            'closure_rate': round(closed_count / total * 100, 2) if total > 0 else 0
        }

    def identify_quality_issues(self) -> List[Dict[str, str]]:
        """Identify quality issues and areas of concern."""
        issues = []

        # Check severity distribution
        severity_data = self.analysis_results.get('severity_distribution', {})
        severity_dist = severity_data.get('distribution', {})

        high_severity_keywords = ['critical', 'high', 'blocker', 'severe']
        high_severity_count = sum(
            data['count'] for severity, data in severity_dist.items()
            if any(keyword in severity.lower() for keyword in high_severity_keywords)
        )
        high_severity_pct = (high_severity_count / severity_data.get('total_bugs', 1)) * 100

        if high_severity_pct > 20:
            issues.append({
                'area': 'Severity Distribution',
                'issue': f'High percentage of critical/high severity bugs ({high_severity_pct:.1f}%)',
                'impact': 'Indicates fundamental quality or testing process issues',
                'recommendation': 'Review testing coverage, especially integration and system testing. Consider implementing more rigorous code review processes.'
            })

        # Check module concentration
        module_data = self.analysis_results.get('module_distribution', {})
        concentration = module_data.get('concentration_ratio', 0)

        if concentration > 50:
            top_modules = module_data.get('top_3_modules', [])
            module_names = ', '.join([m[0] for m in top_modules[:3]])
            issues.append({
                'area': 'Module/Feature Distribution',
                'issue': f'Bug concentration in specific modules ({concentration:.1f}% in top 3): {module_names}',
                'impact': 'Suggests code quality issues or insufficient testing in specific areas',
                'recommendation': f'Conduct focused code review and increase test coverage for: {module_names}. Consider refactoring complex modules.'
            })

        # Check resolution time
        resolution_data = self.analysis_results.get('resolution_time', {})
        avg_days = resolution_data.get('average_days', 0)

        if avg_days > 14:
            issues.append({
                'area': 'Resolution Time',
                'issue': f'Average resolution time is {avg_days:.1f} days',
                'impact': 'Extended bug lifecycles may delay releases and impact customer satisfaction',
                'recommendation': 'Implement bug triage process, set SLA targets by severity, and ensure adequate developer resources for bug fixes.'
            })

        # Check open bug ratio
        status_data = self.analysis_results.get('status_distribution', {})
        closure_rate = status_data.get('closure_rate', 0)

        if closure_rate < 70:
            issues.append({
                'area': 'Bug Closure Rate',
                'issue': f'Low bug closure rate ({closure_rate:.1f}%)',
                'impact': 'Accumulating technical debt and increasing maintenance burden',
                'recommendation': 'Allocate dedicated time for bug resolution, prioritize backlog grooming, and consider bug fixing sprints.'
            })

        # Check category distribution
        category_data = self.analysis_results.get('category_distribution', {})
        category_dist = category_data.get('distribution', {})

        ui_keywords = ['ui', 'interface', 'display', 'visual', 'layout']
        ui_count = sum(
            data['count'] for category, data in category_dist.items()
            if any(keyword in category.lower() for keyword in ui_keywords)
        )
        ui_pct = (ui_count / category_data.get('total_bugs', 1)) * 100

        if ui_pct > 30:
            issues.append({
                'area': 'Bug Category',
                'issue': f'High percentage of UI/UX bugs ({ui_pct:.1f}%)',
                'impact': 'User experience issues may affect adoption and satisfaction',
                'recommendation': 'Enhance UI testing (visual regression, cross-browser), involve UX designers earlier, and implement design system.'
            })

        return issues

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate improvement recommendations based on analysis."""
        recommendations = []

        quality_issues = self.identify_quality_issues()

        # Add issue-specific recommendations
        for issue in quality_issues:
            recommendations.append({
                'priority': 'High' if 'critical' in issue['issue'].lower() or 'severe' in issue['issue'].lower() else 'Medium',
                'area': issue['area'],
                'recommendation': issue['recommendation'],
                'expected_impact': issue['impact']
            })

        # Add general best practice recommendations
        total_bugs = len(self.bugs)

        if total_bugs > 100:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Process Improvement',
                'recommendation': 'Implement automated regression testing to catch bugs earlier in the development cycle.',
                'expected_impact': 'Reduce bug count by 20-30% and catch issues before production deployment.'
            })

        recommendations.append({
            'priority': 'Low',
            'area': 'Quality Metrics',
            'recommendation': 'Establish quality gates and KPIs (e.g., defect density, escape rate, mean time to resolution).',
            'expected_impact': 'Enable data-driven quality management and continuous improvement.'
        })

        return recommendations

    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run all analysis modules and compile results."""
        self.analysis_results = {
            'metadata': {
                'total_bugs': len(self.bugs),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            },
            'severity_distribution': self.analyze_severity_distribution(),
            'category_distribution': self.analyze_category_distribution(),
            'module_distribution': self.analyze_module_distribution(),
            'resolution_time': self.analyze_resolution_time(),
            'status_distribution': self.analyze_status_distribution(),
        }

        self.analysis_results['quality_issues'] = self.identify_quality_issues()
        self.analysis_results['recommendations'] = self.generate_recommendations()

        return self.analysis_results

    def _find_field(self, candidates: List[str]) -> str:
        """Find first matching field name from candidates in bug data."""
        if not self.bugs:
            return candidates[0]

        sample_keys = set(self.bugs[0].keys())
        sample_keys_lower = {k.lower(): k for k in sample_keys}

        for candidate in candidates:
            if candidate in sample_keys:
                return candidate
            if candidate.lower() in sample_keys_lower:
                return sample_keys_lower[candidate.lower()]

        return candidates[0]

    def export_json(self, output_path: str) -> None:
        """Export analysis results as JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)

    def get_results(self) -> Dict[str, Any]:
        """Get analysis results."""
        return self.analysis_results


def main():
    parser = argparse.ArgumentParser(
        description='Analyze bug ticket data for quality management insights'
    )
    parser.add_argument(
        'input_file',
        help='Path to bug data file (CSV or JSON)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path for JSON results (optional)',
        default=None
    )
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'json', 'auto'],
        default='auto',
        help='Input file format (default: auto-detect from extension)'
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = BugAnalyzer()

    # Determine format
    input_path = Path(args.input_file)
    if args.format == 'auto':
        file_format = input_path.suffix.lower().lstrip('.')
        if file_format not in ['csv', 'json']:
            print(f"Error: Cannot auto-detect format from extension '{input_path.suffix}'")
            print("Please specify format with --format csv or --format json")
            sys.exit(1)
    else:
        file_format = args.format

    # Load data
    try:
        if file_format == 'csv':
            analyzer.load_csv(str(input_path))
        elif file_format == 'json':
            analyzer.load_json(str(input_path))
        else:
            print(f"Error: Unsupported format '{file_format}'")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    # Run analysis
    print(f"Analyzing {len(analyzer.bugs)} bug tickets...")
    results = analyzer.run_complete_analysis()

    # Export if output specified
    if args.output:
        analyzer.export_json(args.output)
        print(f"Results exported to: {args.output}")

    # Print summary
    print("\n=== Analysis Summary ===")
    print(f"Total Bugs: {results['metadata']['total_bugs']}")
    print(f"Quality Issues Identified: {len(results['quality_issues'])}")
    print(f"Recommendations: {len(results['recommendations'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
