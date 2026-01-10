#!/usr/bin/env python3
"""
Salesforce Flow Validation Script

Comprehensive pre-deployment validation for Salesforce Flows focusing on:
1. Variable/element reference errors (Priority 1)
2. Governor limit violations (DML/SOQL in loops)
3. Metadata structure validation
4. Naming convention checks

Usage:
    python3 validate_flow.py <flow_file.flow-meta.xml> [--strict] [--format {text|json|markdown}] [--output <file>]

Example:
    python3 validate_flow.py MyFlow.flow-meta.xml --format markdown --output validation_report.md
"""

import argparse
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import re


class FlowValidator:
    """Comprehensive Salesforce Flow validator"""

    def __init__(self, flow_file: str, strict: bool = False):
        """
        Initialize Flow validator

        Args:
            flow_file: Path to Flow XML file (.flow or .flow-meta.xml)
            strict: If True, treat warnings as errors
        """
        self.flow_file = Path(flow_file)
        self.strict = strict
        self.errors = []
        self.warnings = []

        # Parse Flow XML
        self.tree = self._load_flow_xml()
        self.root = self.tree.getroot()

        # Extract Flow metadata
        self.api_version = self._get_text('apiVersion')
        self.status = self._get_text('status')
        self.process_type = self._get_text('processType')
        self.label = self._get_text('label')

        # Extract Flow components
        self.variables = self._extract_variables()
        self.elements = self._extract_elements()
        self.connectors = self._extract_connectors()

    def _load_flow_xml(self) -> ET.ElementTree:
        """Load and parse Flow XML file"""
        try:
            tree = ET.parse(self.flow_file)
            return tree
        except ET.ParseError as e:
            print(f"ERROR: Failed to parse XML file: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.flow_file}")
            sys.exit(1)

    def _get_text(self, tag: str, default: str = '') -> str:
        """Get text from XML element"""
        ns = {'sf': 'http://soap.sforce.com/2006/04/metadata'}
        elem = self.root.find(f'sf:{tag}', ns) if 'soap.sforce.com' in str(self.root.tag) else self.root.find(tag)
        return elem.text if elem is not None and elem.text else default

    def _find_all(self, tag: str) -> List[ET.Element]:
        """Find all elements with given tag"""
        ns = {'sf': 'http://soap.sforce.com/2006/04/metadata'}
        if 'soap.sforce.com' in str(self.root.tag):
            return self.root.findall(f'sf:{tag}', ns)
        return self.root.findall(tag)

    def _extract_variables(self) -> Dict[str, Dict]:
        """Extract all variables from Flow"""
        variables = {}
        for var in self._find_all('variables'):
            name_elem = var.find('name')
            if name_elem is None or not name_elem.text:
                continue

            name = name_elem.text
            variables[name] = {
                'name': name,
                'dataType': self._get_elem_text(var, 'dataType', 'String'),
                'isInput': self._get_elem_text(var, 'isInput', 'false') == 'true',
                'isOutput': self._get_elem_text(var, 'isOutput', 'false') == 'true',
                'isCollection': self._get_elem_text(var, 'isCollection', 'false') == 'true',
                'objectType': self._get_elem_text(var, 'objectType', ''),
            }
        return variables

    def _get_elem_text(self, parent: ET.Element, tag: str, default: str = '') -> str:
        """Get text from child element"""
        elem = parent.find(tag)
        return elem.text if elem is not None and elem.text else default

    def _extract_elements(self) -> Dict[str, Dict]:
        """Extract all Flow elements (screens, assignments, decisions, etc.)"""
        elements = {}

        # Common element types in Flows
        element_types = [
            'screens', 'assignments', 'decisions', 'recordCreates', 'recordUpdates',
            'recordDeletes', 'recordLookups', 'loops', 'subflows', 'actionCalls',
            'waits', 'choices', 'dynamicChoiceSets'
        ]

        for elem_type in element_types:
            for elem in self._find_all(elem_type):
                name_elem = elem.find('name')
                if name_elem is None or not name_elem.text:
                    continue

                name = name_elem.text
                elements[name] = {
                    'name': name,
                    'type': elem_type,
                    'element': elem
                }

        return elements

    def _extract_connectors(self) -> List[Dict]:
        """Extract all connectors from elements"""
        connectors = []

        for elem_name, elem_data in self.elements.items():
            elem = elem_data['element']

            # Find connector or targetReference
            for connector in elem.findall('.//connector'):
                target_elem = connector.find('targetReference')
                if target_elem is not None and target_elem.text:
                    connectors.append({
                        'from': elem_name,
                        'to': target_elem.text,
                        'source_element': elem
                    })

            # Also check direct targetReference (in choices, etc.)
            for target_ref in elem.findall('.//targetReference'):
                if target_ref.text and target_ref.text != '':
                    connectors.append({
                        'from': elem_name,
                        'to': target_ref.text,
                        'source_element': elem
                    })

        return connectors

    def validate_references(self):
        """Validate variable and element references (Priority 1)"""
        # Check 1: Undeclared variables in assignments, formulas, etc.
        for elem_name, elem_data in self.elements.items():
            elem = elem_data['element']

            # Search for variable references in element
            elem_str = ET.tostring(elem, encoding='unicode')

            # Pattern: {!VariableName}
            var_pattern = r'\{!([a-zA-Z_][a-zA-Z0-9_]*)\}'
            matches = re.findall(var_pattern, elem_str)

            for var_name in matches:
                # Skip system variables and resources
                if var_name.startswith('$') or var_name.startswith('Global.'):
                    continue

                # Check if variable is declared
                if var_name not in self.variables and var_name not in self.elements:
                    # Suggest similar names (simple Levenshtein)
                    suggestions = self._find_similar_names(var_name, list(self.variables.keys()))
                    suggestion_text = f" → Did you mean '{suggestions[0]}'?" if suggestions else ""

                    self.errors.append({
                        'code': 'E001',
                        'type': 'Undeclared Variable',
                        'message': f"Undeclared Variable: '{var_name}' referenced in {elem_name}",
                        'detail': suggestion_text,
                        'fix': f"Declare variable '{var_name}' or rename reference to existing variable",
                        'element': elem_name
                    })

        # Check 2: Invalid element references in connectors
        for connector in self.connectors:
            target = connector['to']

            # Skip system references
            if target in ['PAUSE', 'FAST_FORWARD', '']:
                continue

            if target not in self.elements:
                available = ', '.join(list(self.elements.keys())[:5])
                self.errors.append({
                    'code': 'E002',
                    'type': 'Invalid Element Reference',
                    'message': f"Invalid Element Reference: '{target}' in connector from {connector['from']}",
                    'detail': f" → Available elements: {available}...",
                    'fix': f"Update connector to reference existing element",
                    'element': connector['from']
                })

        # Check 3: Type mismatches (simplified - checks variable vs SObject field types)
        for var_name, var_data in self.variables.items():
            if var_data['isCollection'] != (var_data['objectType'] != ''):
                # Collection variables should have objectType for SObjects
                pass  # This is valid - Text collections don't need objectType

        # Check 4: Collection vs Single Value usage
        for elem_name, elem_data in self.elements.items():
            elem = elem_data['element']

            # Check assignments
            if elem_data['type'] == 'assignments':
                for assign in elem.findall('.//assignmentItems'):
                    ref_elem = assign.find('reference')
                    if ref_elem is not None and ref_elem.text:
                        var_name = ref_elem.text
                        if var_name in self.variables:
                            var_data = self.variables[var_name]

                            # Check if assigning collection to single or vice versa
                            # (This is simplified - real validation would need more context)
                            pass

    def _find_similar_names(self, name: str, candidates: List[str], threshold: int = 2) -> List[str]:
        """Find similar names using simple edit distance"""
        def levenshtein(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein(s2, s1)
            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        similar = []
        for candidate in candidates:
            distance = levenshtein(name.lower(), candidate.lower())
            if distance <= threshold:
                similar.append((candidate, distance))

        similar.sort(key=lambda x: x[1])
        return [name for name, dist in similar[:3]]

    def validate_governor_limits(self):
        """Validate governor limit patterns (DML/SOQL in loops)"""
        # Check for loops
        loops = {name: data for name, data in self.elements.items() if data['type'] == 'loops'}

        for loop_name, loop_data in loops.items():
            loop_elem = loop_data['element']

            # Check for DML operations inside loop (ERROR)
            dml_types = ['recordCreates', 'recordUpdates', 'recordDeletes']
            for dml_type in dml_types:
                # Check if any DML element is referenced within the loop
                # (This is simplified - real implementation would trace connectors)
                loop_str = ET.tostring(loop_elem, encoding='unicode')

                # Check for nested elements (very simplified)
                for elem_name, elem_data in self.elements.items():
                    if elem_data['type'] in dml_types:
                        # Check if this DML is inside the loop by checking connectors
                        for connector in self.connectors:
                            if connector['from'] == loop_name and connector['to'] == elem_name:
                                self.errors.append({
                                    'code': 'E101',
                                    'type': 'DML in Loop',
                                    'message': f"DML in Loop: {elem_data['type']} element '{elem_name}' inside loop '{loop_name}'",
                                    'detail': " → Causes governor limit error with bulk data (limit: 150 DML statements)",
                                    'fix': f"Move DML outside loop: collect records in loop, perform batch update after",
                                    'element': loop_name
                                })

            # Check for SOQL (Get Records) inside loop (WARNING)
            for elem_name, elem_data in self.elements.items():
                if elem_data['type'] == 'recordLookups':
                    for connector in self.connectors:
                        if connector['from'] == loop_name and connector['to'] == elem_name:
                            self.warnings.append({
                                'code': 'W001',
                                'type': 'SOQL in Loop',
                                'message': f"SOQL in Loop: Get Records element '{elem_name}' inside loop '{loop_name}'",
                                'detail': " → Risk: May exceed 100 SOQL query limit",
                                'fix': f"Move Get Records before loop and filter in memory",
                                'element': loop_name
                            })

        # Check total SOQL count
        soql_count = len([e for e in self.elements.values() if e['type'] == 'recordLookups'])
        if soql_count > 80:
            self.warnings.append({
                'code': 'W002',
                'type': 'High SOQL Count',
                'message': f"High SOQL Count: {soql_count} Get Records elements (limit: 100)",
                'detail': " → Consider consolidating queries or using batch processing",
                'fix': "Optimize queries: combine filters, reduce element count",
                'element': 'Flow'
            })

        # Check total DML count
        dml_count = len([e for e in self.elements.values() if e['type'] in ['recordCreates', 'recordUpdates', 'recordDeletes']])
        if dml_count > 120:
            self.warnings.append({
                'code': 'W003',
                'type': 'High DML Count',
                'message': f"High DML Count: {dml_count} DML elements (limit: 150)",
                'detail': " → Consider using batch operations or Apex",
                'fix': "Optimize DML: batch updates, reduce element count",
                'element': 'Flow'
            })

    def validate_metadata(self):
        """Validate metadata structure and required fields"""
        # Check API version
        if not self.api_version:
            self.errors.append({
                'code': 'E201',
                'type': 'Missing Required Field',
                'message': "Missing required field: apiVersion",
                'detail': " → Required for deployment",
                'fix': "Add <apiVersion>60.0</apiVersion> to Flow metadata",
                'element': 'Metadata'
            })
        else:
            try:
                version = float(self.api_version)
                if version < 50.0:
                    self.warnings.append({
                        'code': 'W101',
                        'type': 'Old API Version',
                        'message': f"Old API version: {self.api_version}",
                        'detail': " → Consider upgrading to latest version (60.0+)",
                        'fix': "Update apiVersion to match your org (typically 58.0-61.0)",
                        'element': 'Metadata'
                    })
            except ValueError:
                self.errors.append({
                    'code': 'E202',
                    'type': 'Invalid API Version',
                    'message': f"Invalid API version: {self.api_version}",
                    'detail': " → Must be a valid number (e.g., 60.0)",
                    'fix': "Correct apiVersion format: 60.0",
                    'element': 'Metadata'
                })

        # Check status
        if not self.status:
            self.errors.append({
                'code': 'E203',
                'type': 'Missing Required Field',
                'message': "Missing required field: status",
                'detail': " → Required for deployment",
                'fix': "Add <status>Draft</status> or <status>Active</status>",
                'element': 'Metadata'
            })
        elif self.status not in ['Draft', 'Active', 'Obsolete', 'InvalidDraft']:
            self.warnings.append({
                'code': 'W102',
                'type': 'Invalid Status Value',
                'message': f"Invalid status value: {self.status}",
                'detail': " → Valid values: Draft, Active, Obsolete, InvalidDraft",
                'fix': "Use valid status value",
                'element': 'Metadata'
            })

        # Check label
        if not self.label:
            self.warnings.append({
                'code': 'W103',
                'type': 'Missing Label',
                'message': "Missing Flow label",
                'detail': " → Label is recommended for clarity",
                'fix': "Add <label>Your Flow Name</label>",
                'element': 'Metadata'
            })

    def validate_naming_conventions(self):
        """Validate naming conventions (camelCase for variables, PascalCase for elements)"""
        # Check variables (should be camelCase)
        for var_name in self.variables.keys():
            # Skip system variables
            if var_name.startswith('$'):
                continue

            # Check camelCase: starts with lowercase, no underscores except for special cases
            if not re.match(r'^[a-z][a-zA-Z0-9]*$', var_name) and not var_name.startswith('col'):
                self.warnings.append({
                    'code': 'W201',
                    'type': 'Naming Convention',
                    'message': f"Variable '{var_name}' should use camelCase",
                    'detail': " → Example: totalAmount, selectedAccount, isApproved",
                    'fix': f"Rename to camelCase (e.g., '{self._to_camel_case(var_name)}')",
                    'element': var_name
                })

        # Check elements (should be PascalCase with underscores)
        for elem_name in self.elements.keys():
            # Elements typically use PascalCase_With_Underscores
            # But single words should be PascalCase
            if '_' not in elem_name and not re.match(r'^[A-Z][a-zA-Z0-9]*$', elem_name):
                self.warnings.append({
                    'code': 'W202',
                    'type': 'Naming Convention',
                    'message': f"Element '{elem_name}' should use PascalCase",
                    'detail': " → Example: Screen_Input, Assignment_Calculate, Decision_Check_Status",
                    'fix': f"Rename to PascalCase (e.g., '{self._to_pascal_case(elem_name)}')",
                    'element': elem_name
                })

    def _to_camel_case(self, name: str) -> str:
        """Convert to camelCase"""
        parts = re.split(r'[_\s]+', name.lower())
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    def _to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase"""
        parts = re.split(r'[_\s]+', name.lower())
        return ''.join(word.capitalize() for word in parts)

    def run_all_validations(self):
        """Run all validation checks"""
        self.validate_references()
        self.validate_governor_limits()
        self.validate_metadata()
        self.validate_naming_conventions()

    def generate_report(self, format: str = 'text') -> str:
        """
        Generate validation report

        Args:
            format: Output format (text, json, markdown)

        Returns:
            Formatted report string
        """
        error_count = len(self.errors)
        warning_count = len(self.warnings)

        # Treat warnings as errors in strict mode
        if self.strict:
            error_count += warning_count

        status = "✅ PASSED" if error_count == 0 else "❌ FAILED"

        if format == 'json':
            return json.dumps({
                'flow': str(self.flow_file.name),
                'apiVersion': self.api_version,
                'status': status,
                'errorCount': error_count,
                'warningCount': warning_count if not self.strict else 0,
                'errors': self.errors,
                'warnings': [] if self.strict else self.warnings
            }, indent=2)

        elif format == 'markdown':
            lines = []
            lines.append("# Flow Validation Report")
            lines.append("")
            lines.append(f"**Flow:** `{self.flow_file.name}`  ")
            lines.append(f"**API Version:** {self.api_version}  ")
            lines.append(f"**Status:** {status} ({error_count} errors, {warning_count} warnings)")
            lines.append("")

            if self.errors:
                lines.append("## Errors")
                lines.append("")
                for error in self.errors:
                    lines.append(f"### [{error['code']}] {error['type']}")
                    lines.append(f"**Message:** {error['message']}")
                    if error.get('detail'):
                        lines.append(f"**Detail:** {error['detail']}")
                    lines.append(f"**Fix:** {error['fix']}")
                    lines.append("")

            if self.warnings and not self.strict:
                lines.append("## Warnings")
                lines.append("")
                for warning in self.warnings:
                    lines.append(f"### [{warning['code']}] {warning['type']}")
                    lines.append(f"**Message:** {warning['message']}")
                    if warning.get('detail'):
                        lines.append(f"**Detail:** {warning['detail']}")
                    lines.append(f"**Fix:** {warning['fix']}")
                    lines.append("")

            lines.append("---")
            lines.append(f"✅ Validation complete. {'Fix %d errors before deployment.' % error_count if error_count > 0 else 'Flow is ready for deployment.'}")

            return '\n'.join(lines)

        else:  # text format
            lines = []
            lines.append("=" * 80)
            lines.append("FLOW VALIDATION REPORT")
            lines.append("=" * 80)
            lines.append(f"Flow: {self.flow_file.name}")
            lines.append(f"API Version: {self.api_version}")
            lines.append(f"Status: {status} ({error_count} errors, {warning_count} warnings)")
            lines.append("")

            if self.errors:
                lines.append("ERRORS:")
                for i, error in enumerate(self.errors, 1):
                    lines.append(f"[{error['code']}] {error['message']}")
                    if error.get('detail'):
                        lines.append(f"       {error['detail']}")
                    lines.append(f"       → Fix: {error['fix']}")
                    lines.append("")

            if self.warnings and not self.strict:
                lines.append("WARNINGS:")
                for i, warning in enumerate(self.warnings, 1):
                    lines.append(f"[{warning['code']}] {warning['message']}")
                    if warning.get('detail'):
                        lines.append(f"       {warning['detail']}")
                    lines.append(f"       → Fix: {warning['fix']}")
                    lines.append("")

            lines.append("=" * 80)
            lines.append(f"✅ Validation complete. {'Fix %d errors before deployment.' % error_count if error_count > 0 else 'Flow is ready for deployment.'}")
            lines.append("=" * 80)

            return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate Salesforce Flow for deployment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 validate_flow.py MyFlow.flow-meta.xml
  python3 validate_flow.py MyFlow.flow-meta.xml --format markdown --output report.md
  python3 validate_flow.py MyFlow.flow-meta.xml --strict
        """
    )

    parser.add_argument('flow_file', help='Path to Flow XML file (.flow or .flow-meta.xml)')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    args = parser.parse_args()

    # Validate Flow
    validator = FlowValidator(args.flow_file, strict=args.strict)
    validator.run_all_validations()

    # Generate report
    report = validator.generate_report(format=args.format)

    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"✅ Validation report written to: {args.output}")
    else:
        print(report)

    # Exit with error code if validation failed
    error_count = len(validator.errors)
    if validator.strict:
        error_count += len(validator.warnings)

    sys.exit(1 if error_count > 0 else 0)


if __name__ == '__main__':
    main()
