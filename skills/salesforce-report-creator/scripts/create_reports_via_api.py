#!/usr/bin/env python3
"""
Create Salesforce Reports via Analytics REST API

This script creates reports using the Analytics Reports REST API instead of
Metadata API, as the Metadata API has issues with custom report type field references.

Usage:
    python scripts/sf_deploy/create_reports_via_api.py --org full
"""

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Optional


def get_org_info(org: str) -> tuple[str, str]:
    """Get access token and instance URL for the org."""
    result = subprocess.run(["sf", "org", "display", "--target-org", org, "--json"], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error getting org info: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(result.stdout)
    return data["result"]["accessToken"], data["result"]["instanceUrl"]


def get_report_type_columns(instance_url: str, access_token: str, report_type: str) -> list[str]:
    """Get all available column names for a report type."""
    url = f"{instance_url}/services/data/v62.0/analytics/reportTypes/{report_type}"

    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())

        # Extract column keys from categories
        columns = []
        categories = data.get("reportTypeMetadata", {}).get("categories", [])
        for category in categories:
            columns.extend(category.get("columns", {}).keys())

        return columns
    except urllib.error.HTTPError as e:
        print(f"Error getting report type columns: {e.code}", file=sys.stderr)
        print(e.read().decode(), file=sys.stderr)
        return []


def create_report(
    instance_url: str,
    access_token: str,
    name: str,
    report_type: str,
    columns: list[str],
    date_column: str,
    description: str = "",
) -> Optional[str]:
    """Create a report via Analytics REST API."""

    url = f"{instance_url}/services/data/v62.0/analytics/reports"

    body = {
        "reportMetadata": {
            "name": name,
            "description": description,
            "reportFormat": "TABULAR",
            "reportType": {"type": report_type},
            "detailColumns": columns,
            "standardDateFilter": {"column": date_column, "durationValue": "CUSTOM"},
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            report_id = data.get("reportMetadata", {}).get("id")
            print(f"  ✓ Created report: {name}")
            print(f"    ID: {report_id}")
            print(f"    Columns: {len(columns)}")
            return report_id
    except urllib.error.HTTPError as e:
        print(f"  ✗ Error creating report {name}: {e.code}", file=sys.stderr)
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            print(f"    {error_data}", file=sys.stderr)
        except:
            print(f"    {error_body}", file=sys.stderr)
        return None


def move_report_to_folder(instance_url: str, access_token: str, report_id: str, folder_id: str) -> bool:
    """Move a report to a specific folder."""
    url = f"{instance_url}/services/data/v62.0/analytics/reports/{report_id}"

    body = {"reportMetadata": {"folderId": folder_id}}

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        method="PATCH",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"    Moved to folder: {folder_id}")
            return True
    except urllib.error.HTTPError as e:
        print(f"    Warning: Could not move to folder: {e.code}", file=sys.stderr)
        return False


def get_folder_id(instance_url: str, access_token: str, folder_name: str) -> Optional[str]:
    """Get folder ID by name."""
    # Query for the folder
    query = f"SELECT Id, DeveloperName FROM Folder WHERE DeveloperName = '{folder_name}' AND Type = 'Report'"

    result = subprocess.run(
        ["sf", "data", "query", "--query", query, "--target-org", "full", "--json"], capture_output=True, text=True
    )

    if result.returncode == 0:
        data = json.loads(result.stdout)
        records = data.get("result", {}).get("records", [])
        if records:
            return records[0]["Id"]

    return None


# Key fields for Account (under 100 columns)
# Note: Lookup fields use .Name suffix (e.g., Account.Owner.Name)
ACCOUNT_KEY_FIELDS = [
    # Standard fields
    "Account.Id",
    "Account.Name",
    "Account.RecordType",
    "Account.Owner.Name",
    "Account.Type",
    "Account.Industry",
    "Account.Phone",
    "Account.Fax",
    "Account.Website",
    "Account.BillingStreet",
    "Account.BillingCity",
    "Account.BillingState",
    "Account.BillingPostalCode",
    "Account.BillingCountry",
    "Account.ShippingStreet",
    "Account.ShippingCity",
    "Account.ShippingState",
    "Account.ShippingPostalCode",
    "Account.ShippingCountry",
    "Account.CreatedDate",
    "Account.CreatedBy.Name",
    "Account.LastModifiedDate",
    "Account.LastModifiedBy.Name",
    "Account.Parent.Name",
    "Account.AccountNumber",
    "Account.AccountSource",
    # Custom fields for migration (redac_* fields)
    "Account.redac_Connection_Redac__c",
    "Account.redac_benchmarkcompany__c",
    "Account.redac_cm__c",
    "Account.redac_cmownedproperty2__c",
    "Account.redac_cmpropertytype__c",
    "Account.redac_commercialleasemanagement2__c",
    "Account.emailaddress1__c",
    "Account.importsequencenumber__c",
    "Account.advantage_corporate_contract__c",
    "Account.jan_corporate_contract__c",
    "Account.core_target__c",
    "Account.decision_maker__c.Name",
    "Account.primarycontactid__c.Name",
]

# Key fields for Contact (under 100 columns)
# Note: Lookup fields use .Name suffix (e.g., Contact.Account.Name)
CONTACT_KEY_FIELDS = [
    # Standard fields
    "Contact.Id",
    "Contact.Name",
    "Contact.FirstName",
    "Contact.LastName",
    "Contact.RecordType",
    "Contact.Owner.Name",
    "Contact.Account.Name",
    "Contact.Email",
    "Contact.Phone",
    "Contact.MobilePhone",
    "Contact.HomePhone",
    "Contact.Fax",
    "Contact.Title",
    "Contact.Department",
    "Contact.MailingStreet",
    "Contact.MailingCity",
    "Contact.MailingState",
    "Contact.MailingPostalCode",
    "Contact.MailingCountry",
    "Contact.OtherStreet",
    "Contact.OtherCity",
    "Contact.OtherState",
    "Contact.OtherPostalCode",
    "Contact.OtherCountry",
    "Contact.OtherPhone",
    "Contact.CreatedDate",
    "Contact.CreatedBy.Name",
    "Contact.LastModifiedDate",
    "Contact.LastModifiedBy.Name",
    "Contact.ReportsTo.Name",
    "Contact.Birthdate",
    "Contact.LeadSource",
    # Custom fields for migration (redac_* fields)
    "Contact.emailaddress2__c",
    "Contact.emailaddress3__c",
    "Contact.redac_Japanesespeakinglevel__c",
    "Contact.redac_age_of_children__c",
    "Contact.redac_arriveddate__c",
    "Contact.redac_assetsize__c",
    "Contact.redac_bulkmailsend__c",
    "Contact.redac_capitalgain__c",
    "Contact.redac_commissionrate__c",
    "Contact.redac_cont_blacklist__c",
    "Contact.redac_cont_businessphoneext__c",
    "Contact.redac_cont_character__c",
]

# Report configurations
REPORT_CONFIGS = {
    "Account": {
        "name": "Account All Fields - Migration",
        "report_type": "Account_All_Fields__c",
        "date_column": "Account.CreatedDate",
        "description": "Account All Fields Report for Migration Data Verification (max 99 columns)",
        "max_columns": 99,  # REST API limit is 100
        "key_fields": None,  # Use all available fields (up to max_columns)
        "field_filters": {"exclude_suffixes": [], "transform": {}},
    },
    "Contact": {
        "name": "Contact All Fields - Migration",
        "report_type": "Contact_Key_Fields__c",
        "date_column": "Contact.CreatedDate",
        "description": "Contact All Fields Report for Migration Data Verification (max 99 columns)",
        "max_columns": 99,
        "key_fields": None,  # Use all available fields (up to max_columns)
        "field_filters": {"exclude_suffixes": [], "transform": {}},
    },
    "Property__c": {
        "name": "Property All Fields - Migration",
        "report_type": "Property_All_Fields__c",
        "date_column": "Property__c.CreatedDate",
        "description": "Property All Fields Report for Migration Data Verification",
        "max_columns": 99,
        "key_fields": None,  # Use all fields (under 100)
        "field_filters": {"exclude_suffixes": [], "transform": {}},
    },
}


def filter_columns(columns: list[str], config: dict) -> list[str]:
    """Filter and transform columns based on config."""
    filters = config.get("field_filters", {})
    exclude_suffixes = filters.get("exclude_suffixes", [])
    transforms = filters.get("transform", {})
    key_fields = config.get("key_fields")
    max_columns = config.get("max_columns", 99)

    # If key_fields specified, filter to only those that exist in available columns
    if key_fields:
        available_set = set(columns)
        result = [f for f in key_fields if f in available_set]
        print(f"  Key fields matched: {len(result)} of {len(key_fields)}")
        return result[:max_columns]

    result = []
    for col in columns:
        # Skip if matches exclude suffix
        if any(col.endswith(suffix) for suffix in exclude_suffixes):
            continue

        # Apply transform if exists
        if col in transforms:
            result.append(transforms[col])
        else:
            result.append(col)

    return result[:max_columns]


def main():
    parser = argparse.ArgumentParser(description="Create Salesforce Reports via Analytics REST API")
    parser.add_argument("--org", required=True, help="Salesforce org alias (e.g., 'full')")
    parser.add_argument("--report", choices=list(REPORT_CONFIGS.keys()), help="Create specific report only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without creating")

    args = parser.parse_args()

    print(f"Target org: {args.org}")
    print("-" * 50)

    # Get org credentials
    access_token, instance_url = get_org_info(args.org)
    print(f"Instance URL: {instance_url}")

    # Get folder ID for Migration_Data_Reports
    folder_id = get_folder_id(instance_url, access_token, "Migration_Data_Reports")
    if folder_id:
        print(f"Target folder ID: {folder_id}")
    else:
        print("Warning: Migration_Data_Reports folder not found")

    print("-" * 50)

    # Process each report
    reports_to_create = [args.report] if args.report else list(REPORT_CONFIGS.keys())

    created_reports = []

    for obj_name in reports_to_create:
        config = REPORT_CONFIGS[obj_name]
        print(f"\nProcessing {obj_name}...")

        # Get available columns for this report type
        columns = get_report_type_columns(instance_url, access_token, config["report_type"])

        if not columns:
            print(f"  Warning: No columns found for {config['report_type']}")
            continue

        print(f"  Available columns: {len(columns)}")

        # Filter columns
        filtered_columns = filter_columns(columns, config)
        print(f"  Filtered columns: {len(filtered_columns)}")

        # Limit to 200 columns (Salesforce limit)
        if len(filtered_columns) > 200:
            filtered_columns = filtered_columns[:200]
            print("  Limited to 200 columns (Salesforce max)")

        if args.dry_run:
            print(f"  [DRY RUN] Would create report: {config['name']}")
            print(f"  Columns (first 10): {filtered_columns[:10]}")
            continue

        # Create report
        report_id = create_report(
            instance_url,
            access_token,
            config["name"],
            config["report_type"],
            filtered_columns,
            config["date_column"],
            config["description"],
        )

        if report_id:
            created_reports.append(report_id)

            # Move to folder if available
            if folder_id:
                move_report_to_folder(instance_url, access_token, report_id, folder_id)

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Created {len(created_reports)} reports")

    if created_reports:
        print("\nView reports at:")
        for report_id in created_reports:
            print(f"  {instance_url}/lightning/r/Report/{report_id}/view")


if __name__ == "__main__":
    main()
