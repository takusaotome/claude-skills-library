#!/usr/bin/env python3
"""
Salesforce Flow Deployment Script

Automated deployment via sf CLI with pre-deployment validation and error handling.

Usage:
    python3 deploy_flow.py --source-dir <flow_directory> --target-org <org_alias> [options]

Example:
    python3 deploy_flow.py --source-dir flows/ --target-org my-sandbox --validate-only
    python3 deploy_flow.py --source-dir flows/ --target-org production --test-level RunLocalTests
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class FlowDeployer:
    """Automated Flow deployment via sf CLI"""

    def __init__(
        self,
        source_dir: str,
        target_org: str,
        validate_only: bool = False,
        test_level: str = "NoTestRun",
        rollback_on_error: bool = False,
    ):
        """
        Initialize Flow deployer

        Args:
            source_dir: Directory containing Flow files
            target_org: Target org alias
            validate_only: If True, only validate without deploying
            test_level: Test level (NoTestRun, RunLocalTests, RunAllTestsInOrg)
            rollback_on_error: Auto-rollback if deployment fails
        """
        self.source_dir = Path(source_dir)
        self.target_org = target_org
        self.validate_only = validate_only
        self.test_level = test_level
        self.rollback_on_error = rollback_on_error

        # Validate inputs
        self._validate_inputs()

    def _validate_inputs(self):
        """Validate input parameters"""
        if not self.source_dir.exists():
            print(f"ERROR: Source directory not found: {self.source_dir}")
            sys.exit(1)

        if not self.source_dir.is_dir():
            print(f"ERROR: Source path is not a directory: {self.source_dir}")
            sys.exit(1)

    def _run_command(self, cmd: List[str], description: str) -> Tuple[int, str, str]:
        """
        Run shell command and capture output

        Args:
            cmd: Command as list of strings
            description: Description for logging

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        print(f"🔄 {description}...")
        print(f"   Command: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        return result.returncode, result.stdout, result.stderr

    def validate_org_connection(self) -> bool:
        """
        Validate sf CLI connection to target org

        Returns:
            True if connection is valid
        """
        print(f"🔍 Validating connection to org: {self.target_org}")

        # Check sf CLI installed
        returncode, stdout, stderr = self._run_command(["sf", "--version"], "Checking sf CLI installation")

        if returncode != 0:
            print("❌ ERROR: sf CLI not installed or not in PATH")
            print("   Install: https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/")
            return False

        print(f"✅ sf CLI version: {stdout.strip()}")

        # Check org connection
        returncode, stdout, stderr = self._run_command(
            ["sf", "org", "display", "--target-org", self.target_org, "--json"],
            f"Checking connection to {self.target_org}",
        )

        if returncode != 0:
            print(f"❌ ERROR: Cannot connect to org '{self.target_org}'")
            print(f"   {stderr}")
            print("\nTroubleshooting:")
            print("  1. List available orgs: sf org list")
            print("  2. Authenticate: sf org login web --alias <org-alias>")
            return False

        # Parse org info
        try:
            org_info = json.loads(stdout)
            result = org_info.get("result", {})
            print("✅ Connected to org:")
            print(f"   Username: {result.get('username')}")
            print(f"   Org ID: {result.get('id')}")
            print(f"   Instance: {result.get('instanceUrl')}")
            return True
        except json.JSONDecodeError:
            print("⚠️  Warning: Could not parse org info, but connection appears valid")
            return True

    def run_pre_deployment_checks(self) -> bool:
        """
        Run pre-deployment validation on Flow files

        Returns:
            True if all validations pass
        """
        print("\n🔍 Running pre-deployment validation...")

        # Find all Flow metadata files
        flow_files = list(self.source_dir.glob("**/*.flow-meta.xml"))

        if not flow_files:
            print(f"⚠️  Warning: No Flow metadata files found in {self.source_dir}")
            print("   Looking for: *.flow-meta.xml")
            return True  # Not an error, just no Flows to validate

        print(f"   Found {len(flow_files)} Flow file(s)")

        # Validate each Flow
        all_passed = True
        for flow_file in flow_files:
            print(f"\n   Validating: {flow_file.name}")

            # Check if validate_flow.py exists
            validator_script = Path(__file__).parent / "validate_flow.py"

            if not validator_script.exists():
                print("   ⚠️  Warning: validate_flow.py not found, skipping validation")
                continue

            # Run validator
            returncode, stdout, stderr = self._run_command(
                ["python3", str(validator_script), str(flow_file), "--format", "text"], f"Validating {flow_file.name}"
            )

            if returncode != 0:
                print(f"   ❌ Validation FAILED for {flow_file.name}")
                print(stdout)
                all_passed = False
            else:
                print(f"   ✅ Validation passed for {flow_file.name}")

        return all_passed

    def deploy_flows(self) -> bool:
        """
        Deploy Flows to target org

        Returns:
            True if deployment successful
        """
        mode = "Validating" if self.validate_only else "Deploying"
        print(f"\n🚀 {mode} Flows to {self.target_org}...")

        # Build sf deploy command
        cmd = [
            "sf",
            "project",
            "deploy",
            "start",
            "--source-dir",
            str(self.source_dir),
            "--target-org",
            self.target_org,
            "--test-level",
            self.test_level,
        ]

        if self.validate_only:
            cmd.extend(["--dry-run"])

        # Execute deployment
        returncode, stdout, stderr = self._run_command(cmd, f"{mode} Flows")

        # Parse results
        if returncode == 0:
            print(f"\n✅ {mode} successful!")
            print(stdout)
            return True
        else:
            print(f"\n❌ {mode} FAILED")
            print(stderr)

            # Parse error details
            self._parse_deployment_errors(stderr)

            return False

    def _parse_deployment_errors(self, error_output: str):
        """
        Parse and explain deployment errors

        Args:
            error_output: Error output from sf CLI
        """
        print("\n📋 Error Analysis:")

        # Common error patterns
        error_patterns = {
            "INVALID_TYPE_ON_FIELD_IN_RECORD": {
                "description": "Variable type doesn't match field type",
                "fix": "Check variable dataType matches target object field type",
            },
            "INVALID_FIELD_OR_REFERENCE": {
                "description": "Field or variable not found",
                "fix": "Run validate_flow.py to find undeclared references",
            },
            "FLOW_ACTIVE_VERSION_NOT_FOUND": {
                "description": "No active Flow version",
                "fix": "Activate Flow after deployment: Setup → Flows → [Flow] → Activate",
            },
            "REQUIRED_FIELD_MISSING": {
                "description": "Required field not populated",
                "fix": "Ensure all required fields are set in Create/Update elements",
            },
            "CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY": {
                "description": "Insufficient permissions",
                "fix": "Check user has object/field permissions and FLS access",
            },
            "FIELD_CUSTOM_VALIDATION_EXCEPTION": {
                "description": "Validation rule failure",
                "fix": "Review validation rules on target object",
            },
        }

        # Find matching error patterns
        found_errors = []
        for error_code, error_info in error_patterns.items():
            if error_code in error_output:
                found_errors.append((error_code, error_info))

        if found_errors:
            for error_code, error_info in found_errors:
                print(f"\n   ⚠️  {error_code}")
                print(f"      Description: {error_info['description']}")
                print(f"      Fix: {error_info['fix']}")
        else:
            print("   No known error patterns detected. Review full error output above.")

        print("\n💡 Troubleshooting Tips:")
        print("   1. Run validation: python3 scripts/validate_flow.py <flow_file>")
        print("   2. Check Debug Logs: Setup → Debug Logs → New → Run Flow → View Log")
        print("   3. Review error reference: assets/error_reference_table.md")

    def rollback_deployment(self) -> bool:
        """
        Rollback failed deployment (if backup exists)

        Returns:
            True if rollback successful
        """
        print("\n🔄 Attempting rollback...")

        backup_dir = self.source_dir.parent / "backups" / f"{self.source_dir.name}_backup"

        if not backup_dir.exists():
            print(f"❌ No backup found at {backup_dir}")
            print("   Cannot rollback. Manual intervention required.")
            return False

        print(f"   Restoring from: {backup_dir}")

        returncode, stdout, stderr = self._run_command(
            ["sf", "project", "deploy", "start", "--source-dir", str(backup_dir), "--target-org", self.target_org],
            "Rolling back deployment",
        )

        if returncode == 0:
            print("✅ Rollback successful")
            return True
        else:
            print("❌ Rollback FAILED")
            print(stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Deploy Salesforce Flows via sf CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate deployment (dry run)
  python3 deploy_flow.py --source-dir flows/ --target-org sandbox --validate-only

  # Deploy to sandbox
  python3 deploy_flow.py --source-dir flows/ --target-org sandbox

  # Deploy to production with tests
  python3 deploy_flow.py --source-dir flows/ --target-org production --test-level RunLocalTests

  # Deploy with auto-rollback on error
  python3 deploy_flow.py --source-dir flows/ --target-org sandbox --rollback-on-error
        """,
    )

    parser.add_argument("--source-dir", required=True, help="Directory containing Flow files")
    parser.add_argument("--target-org", required=True, help="Target org alias (from sf org list)")
    parser.add_argument("--validate-only", action="store_true", help="Validate deployment without deploying (dry run)")
    parser.add_argument(
        "--test-level",
        default="NoTestRun",
        choices=["NoTestRun", "RunLocalTests", "RunAllTestsInOrg"],
        help="Test level for deployment (default: NoTestRun)",
    )
    parser.add_argument(
        "--rollback-on-error", action="store_true", help="Auto-rollback if deployment fails (requires backup)"
    )

    args = parser.parse_args()

    # Create deployer
    deployer = FlowDeployer(
        source_dir=args.source_dir,
        target_org=args.target_org,
        validate_only=args.validate_only,
        test_level=args.test_level,
        rollback_on_error=args.rollback_on_error,
    )

    # Step 1: Validate org connection
    if not deployer.validate_org_connection():
        sys.exit(1)

    # Step 2: Run pre-deployment validation
    if not deployer.run_pre_deployment_checks():
        print("\n❌ Pre-deployment validation failed")
        print("   Fix validation errors before deployment")
        sys.exit(1)

    # Step 3: Deploy
    success = deployer.deploy_flows()

    if not success and args.rollback_on_error:
        # Attempt rollback
        deployer.rollback_deployment()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
