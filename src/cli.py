import sys
import json
import argparse
from src.checker import EnvDoctor

def main():
    parser = argparse.ArgumentParser(description="🏥 env-doctor: Audit local vs reference environment files.")
    parser.add_argument("-t", "--target", default=".env", help="Path to local .env file")
    parser.add_argument("-e", "--example", default=".env.example", help="Path to .env.example file")
    parser.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        doctor = EnvDoctor(target_path=args.target, example_path=args.example)
        report = doctor.diagnose()

        if args.format == "json":
            print(json.dumps(report, indent=2))
            sys.exit(0 if report["healthy"] else 1)

        if args.format == "markdown":
            print("## 🏥 Env-Doctor Diagnosis Report\n")
            if report["healthy"]:
                print("✅ **Status:** All required environment variables are valid!\n")
            else:
                print("❌ **Status:** Configuration issues detected.\n")
                if report["missing"]:
                    print("### Missing Keys\n" + "\n".join(f"- `{k}`" for k in report["missing"]))
                if report["empty"]:
                    print("### Empty Keys\n" + "\n".join(f"- `{k}`" for k in report["empty"]))
                if report["invalid_types"]:
                    print("### Type Mismatches\n" + "\n".join(f"- `{item['key']}` (expected `{item['expected']}`, got `{item['got']}`)" for item in report["invalid_types"]))
                if report["weak_secrets"]:
                    print("### Weak Secrets\n" + "\n".join(f"- `{k}`" for k in report["weak_secrets"]))
            sys.exit(0 if report["healthy"] else 1)

        # Standard text format
        print("\n🏥 Env-Doctor Diagnosis Report\n" + "=" * 35)
        if report["healthy"]:
            print("✅ All required environment variables are present and valid!\n")
            sys.exit(0)

        if report["missing"]:
            print("❌ Missing Keys (in example, missing locally):")
            for k in report["missing"]:
                print(f"   - {k}")

        if report["empty"]:
            print("\n⚠️  Empty Keys (defined locally, but value is blank):")
            for k in report["empty"]:
                print(f"   - {k}")

        if report["invalid_types"]:
            print("\n⚠️  Type Mismatches:")
            for item in report["invalid_types"]:
                print(f"   - {item['key']}: Expected {item['expected']}, got '{item['got']}'")

        if report["weak_secrets"]:
            print("\n🚨 Weak or Hardcoded Secrets Detected:")
            for k in report["weak_secrets"]:
                print(f"   - {k}")

        print("\n")
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
