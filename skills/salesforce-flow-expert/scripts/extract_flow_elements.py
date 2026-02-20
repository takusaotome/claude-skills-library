#!/usr/bin/env python3
"""
Flow Elements Extractor

Parse Flow XML to extract and analyze structure: variables, elements, connections.
Useful for documentation, analysis, and debugging.

Usage:
    python3 extract_flow_elements.py <flow_file.flow-meta.xml> [--output-format json|yaml|markdown]

Example:
    python3 extract_flow_elements.py MyFlow.flow-meta.xml --output-format markdown > flow_structure.md
"""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List


class FlowExtractor:
    """Extract and analyze Flow structure"""

    def __init__(self, flow_file: str):
        """Initialize extractor"""
        self.flow_file = Path(flow_file)
        self.tree = ET.parse(self.flow_file)
        self.root = self.tree.getroot()

    def extract_variables(self) -> List[Dict]:
        """Extract all variables"""
        variables = []
        for var in self.root.findall(".//variables"):
            name_elem = var.find("name")
            if name_elem is None:
                continue

            var_info = {
                "name": name_elem.text,
                "dataType": self._get_elem_text(var, "dataType", "String"),
                "isInput": self._get_elem_text(var, "isInput", "false") == "true",
                "isOutput": self._get_elem_text(var, "isOutput", "false") == "true",
                "isCollection": self._get_elem_text(var, "isCollection", "false") == "true",
            }

            if var_info["dataType"] == "SObject":
                var_info["objectType"] = self._get_elem_text(var, "objectType", "")

            variables.append(var_info)

        return variables

    def extract_elements(self) -> Dict[str, List[str]]:
        """Extract all Flow elements by type"""
        element_types = {
            "screens": [],
            "assignments": [],
            "decisions": [],
            "recordCreates": [],
            "recordUpdates": [],
            "recordDeletes": [],
            "recordLookups": [],
            "loops": [],
            "subflows": [],
            "actionCalls": [],
        }

        for elem_type in element_types.keys():
            for elem in self.root.findall(f".//{elem_type}"):
                name_elem = elem.find("name")
                if name_elem is not None and name_elem.text:
                    element_types[elem_type].append(name_elem.text)

        return element_types

    def extract_connections(self) -> List[Dict]:
        """Extract connections between elements"""
        connections = []

        for elem in self.root.findall(".//*"):
            elem_name = self._get_elem_text(elem, "name")
            if not elem_name:
                continue

            # Find connectors
            for connector in elem.findall(".//connector"):
                target = self._get_elem_text(connector, "targetReference")
                if target:
                    connections.append({"from": elem_name, "to": target})

            # Find targetReference (in choices, etc.)
            for target_ref in elem.findall(".//targetReference"):
                if target_ref.text and target_ref.text.strip():
                    connections.append({"from": elem_name, "to": target_ref.text})

        return connections

    def _get_elem_text(self, parent: ET.Element, tag: str, default: str = "") -> str:
        """Get text from child element"""
        elem = parent.find(tag)
        return elem.text if elem is not None and elem.text else default

    def export(self, format: str = "json") -> str:
        """Export Flow structure in specified format"""
        variables = self.extract_variables()
        elements = self.extract_elements()
        connections = self.extract_connections()

        data = {
            "flowFile": str(self.flow_file.name),
            "variables": variables,
            "elements": elements,
            "connections": connections,
            "summary": {
                "totalVariables": len(variables),
                "totalElements": sum(len(elems) for elems in elements.values()),
                "totalConnections": len(connections),
            },
        }

        if format == "json":
            return json.dumps(data, indent=2)

        elif format == "yaml":
            # Simple YAML-like format
            lines = []
            lines.append(f"flowFile: {data['flowFile']}")
            lines.append("")
            lines.append("variables:")
            for var in variables:
                lines.append(f"  - name: {var['name']}")
                lines.append(f"    dataType: {var['dataType']}")
                lines.append(f"    isCollection: {var['isCollection']}")
            lines.append("")
            lines.append("elements:")
            for elem_type, elem_list in elements.items():
                if elem_list:
                    lines.append(f"  {elem_type}:")
                    for elem_name in elem_list:
                        lines.append(f"    - {elem_name}")
            lines.append("")
            lines.append("summary:")
            lines.append(f"  totalVariables: {data['summary']['totalVariables']}")
            lines.append(f"  totalElements: {data['summary']['totalElements']}")
            lines.append(f"  totalConnections: {data['summary']['totalConnections']}")
            return "\n".join(lines)

        elif format == "markdown":
            lines = []
            lines.append(f"# Flow Structure: {data['flowFile']}")
            lines.append("")

            # Summary
            lines.append("## Summary")
            lines.append("")
            lines.append(f"- **Variables**: {data['summary']['totalVariables']}")
            lines.append(f"- **Elements**: {data['summary']['totalElements']}")
            lines.append(f"- **Connections**: {data['summary']['totalConnections']}")
            lines.append("")

            # Variables
            if variables:
                lines.append("## Variables")
                lines.append("")
                lines.append("| Name | Type | Collection | Input | Output |")
                lines.append("|------|------|------------|-------|--------|")
                for var in variables:
                    lines.append(
                        f"| {var['name']} | {var['dataType']} | {var['isCollection']} | {var['isInput']} | {var['isOutput']} |"
                    )
                lines.append("")

            # Elements
            lines.append("## Elements")
            lines.append("")
            for elem_type, elem_list in elements.items():
                if elem_list:
                    lines.append(f"### {elem_type} ({len(elem_list)})")
                    lines.append("")
                    for elem_name in elem_list:
                        lines.append(f"- {elem_name}")
                    lines.append("")

            # Connections
            if connections:
                lines.append("## Connections")
                lines.append("")
                lines.append("| From | To |")
                lines.append("|------|------|")
                for conn in connections[:50]:  # Limit to first 50
                    lines.append(f"| {conn['from']} | {conn['to']} |")
                if len(connections) > 50:
                    lines.append("| ... | ... |")
                    lines.append(f"| *({len(connections) - 50} more connections)* | |")
                lines.append("")

            return "\n".join(lines)

        else:
            return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and analyze Flow structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract to JSON
  python3 extract_flow_elements.py MyFlow.flow-meta.xml

  # Extract to Markdown
  python3 extract_flow_elements.py MyFlow.flow-meta.xml --output-format markdown

  # Save to file
  python3 extract_flow_elements.py MyFlow.flow-meta.xml --output-format markdown > flow_doc.md
        """,
    )

    parser.add_argument("flow_file", help="Path to Flow XML file")
    parser.add_argument(
        "--output-format", choices=["json", "yaml", "markdown"], default="json", help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Extract Flow structure
    extractor = FlowExtractor(args.flow_file)
    output = extractor.export(format=args.output_format)

    print(output)


if __name__ == "__main__":
    main()
