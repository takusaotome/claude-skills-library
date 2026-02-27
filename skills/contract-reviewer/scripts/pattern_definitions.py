"""
Pattern definitions for contract analysis.

This module contains regex patterns and metadata for:
- Red flag detection
- Contract type classification
- Standard clause identification
"""

# Red flag patterns with regex and metadata
RED_FLAG_PATTERNS = [
    {
        "id": "RF001",
        "title": "Unlimited Liability",
        "pattern": r"(unlimited\s+liabilit|no\s+limit\s+on\s+liabilit|liable\s+for\s+all\s+damages)",
        "severity": "Critical",
        "category": "Financial",
        "description": "Contract contains unlimited liability exposure",
        "recommendation": "Negotiate liability cap (typically 12-24 months of fees)",
    },
    {
        "id": "RF002",
        "title": "One-Sided Indemnification",
        "detection_mode": "absence",
        "prerequisite_pattern": r"(customer|licensee|buyer)\s+shall\s+indemnif",
        "pattern": r"(vendor|provider|licensor|seller)\s+shall\s+indemnif|each\s+party\s+shall\s+indemnif|mutual\s+indemnif",
        "severity": "Critical",
        "category": "Financial",
        "description": "Customer indemnification is present but mutual/vendor indemnification is not found",
        "recommendation": "Request mutual indemnification clause",
    },
    {
        "id": "RF003",
        "title": "Automatic Renewal - Long Notice",
        "pattern": r"(automatically\s+renew|auto[\-\s]?renew).{0,200}(notice|prior).{0,50}(9[1-9]|1[0-9]{2}|[2-9][0-9]{2})\s*days?",
        "severity": "High",
        "category": "Operational",
        "description": "Auto-renewal with notice period exceeding 90 days",
        "recommendation": "Negotiate notice period to 30-60 days",
    },
    {
        "id": "RF004",
        "title": "Unilateral Amendment Rights",
        "pattern": r"(provider|vendor|company)\s+(may|reserves?\s+the\s+right\s+to)\s+(modify|change|amend|update).{0,50}(terms?|agreement|conditions?).{0,50}(at\s+any\s+time|without\s+consent|by\s+posting)",
        "severity": "Critical",
        "category": "Legal",
        "description": "Other party can change terms without consent",
        "recommendation": "Require mutual written consent for amendments",
    },
    {
        "id": "RF005",
        "title": "No Consequential Damages Exclusion",
        "detection_mode": "absence",
        "prerequisite_pattern": r"consequential\s+damages?",
        "pattern": r"consequential\s+damages?.{0,50}(excluded?|waive[sd]?|shall\s+not)|(exclud|waiv|no\s+(?:liability|claim)\s+for).{0,50}consequential\s+damages?",
        "severity": "High",
        "category": "Financial",
        "description": "Consequential damages are mentioned but no exclusion or waiver is found",
        "recommendation": "Add mutual exclusion of consequential damages",
    },
    {
        "id": "RF006",
        "title": "Broad IP Assignment",
        "pattern": r"(assign|transfer|convey).{0,50}(all|any|every).{0,50}(intellectual\s+property|ip|patent|copyright|invention)",
        "severity": "Critical",
        "category": "Strategic",
        "description": "Broad assignment of intellectual property rights",
        "recommendation": "Limit IP assignment to specific deliverables",
    },
    {
        "id": "RF007",
        "title": "No Termination for Convenience",
        "detection_mode": "absence",
        "prerequisite_pattern": r"terminat",
        "pattern": r"terminat.{0,50}(for\s+convenience|without\s+cause|at\s+will)",
        "severity": "High",
        "category": "Operational",
        "description": "Termination is mentioned but no termination for convenience right is found",
        "recommendation": "Add termination for convenience with reasonable notice",
    },
    {
        "id": "RF008",
        "title": "Excessive Termination Penalty",
        "pattern": r"(terminat|early).{0,30}(fee|penalty|charge).{0,30}(100%|all\s+remaining|entire\s+balance)",
        "severity": "High",
        "category": "Financial",
        "description": "Termination penalty appears to be 100% of remaining fees",
        "recommendation": "Negotiate declining penalty structure",
    },
    {
        "id": "RF009",
        "title": "Residual Knowledge Clause",
        "pattern": r"(residual|unaided\s+memory|retained\s+in\s+memory).{0,100}(use|free|unrestricted)",
        "severity": "Critical",
        "category": "Strategic",
        "description": "Residual knowledge exception can negate confidentiality",
        "recommendation": "Remove or significantly limit this clause",
    },
    {
        "id": "RF010",
        "title": "Sole and Exclusive Remedy",
        "pattern": r"(sole\s+and\s+exclusive|only)\s+remed.{0,50}(credit|service\s+level)",
        "severity": "High",
        "category": "Operational",
        "description": "SLA credits may be exclusive remedy with no termination right",
        "recommendation": "Add termination right after repeated SLA failures",
    },
]

# Contract type detection patterns
CONTRACT_TYPE_PATTERNS = {
    "NDA": [
        r"non[\-\s]?disclosure\s+agreement",
        r"confidentiality\s+agreement",
        r"mutual\s+nda",
        r"unilateral\s+nda",
    ],
    "MSA": [
        r"master\s+service[s]?\s+agreement",
        r"master\s+agreement",
        r"framework\s+agreement",
    ],
    "SOW": [
        r"statement\s+of\s+work",
        r"scope\u0020of\s+work",
        r"service\s+agreement",
        r"professional\s+services\s+agreement",
    ],
    "SLA": [
        r"service\s+level\s+agreement",
        r"service\s+levels?",
        r"uptime\s+guarantee",
        r"availability\s+commitment",
    ],
    "License": [
        r"software\s+license\s+agreement",
        r"license\s+agreement",
        r"end[\-\s]?user\s+license",
        r"subscription\s+agreement",
    ],
}

# Clause detection patterns
CLAUSE_PATTERNS = {
    "Definitions": r"(definition[s]?|defined\s+term[s]?)",
    "Term": r"(term\s+of|effective\s+date|duration|period\s+of\s+agreement)",
    "Termination": r"(terminat|cancellation|expir)",
    "Liability": r"(limitation\s+of\s+liability|limit\s+of\s+liability|cap\s+on\s+liability)",
    "Indemnification": r"(indemnif|hold\s+harmless)",
    "Confidentiality": r"(confidential|non[\-\s]?disclosure|proprietary\s+information)",
    "IP Rights": r"(intellectual\s+property|ip\s+rights|ownership|work\s+product)",
    "Data Protection": r"(data\s+protection|privacy|gdpr|personal\s+data|pii)",
    "Governing Law": r"(governing\s+law|jurisdiction|applicable\s+law|choice\s+of\s+law)",
    "Force Majeure": r"(force\s+majeure|act[s]?\s+of\s+god|unforeseeable)",
    "Assignment": r"(assignment|transfer\s+of\s+rights|successors\s+and\s+assigns)",
    "Amendment": r"(amendment|modification|change[s]?\s+to\s+agreement)",
}
