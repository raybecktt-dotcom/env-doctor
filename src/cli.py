import sys
import argparse
from src.checker import EnvDoctor

def main():
    parser = argparse.ArgumentParser(description="🏥 env-doctor: Audit local vs reference environment files.")
    parser.add_argument("-t", "--target", default=".env", help="Path to local .env file")
    parser.add_argument("-e", "--example", default=".env.example", help="Path to .env.example file")
    args = parser.parse_args()

    try:
        doctor = EnvDoctor(target_path=args.target, example_path=args.example)
        report = doctor.diagnose()

        print("\n🏥 Env-Doctor Diagnosis Report\n" + "=" * 35)

        if report["healthy"]:
            print("✅ All required environment variables are present and populated!\n")
            sys.exit(0)

        if report["missing"]:
            print("❌ Missing Keys (in example, missing locally):")
            for k in report["missing"]:
                print(f"   - {k}")

        if report["empty"]:
            print("\n⚠️  Empty Keys (defined locally, but value is blank):")
            for k in report["empty"]:
                print(f"   - {k}")

        if report["extra"]:
            print("\nℹ️  Extra Keys (in local .env, not in example):")
            for k in report["extra"]:
                print(f"   - {k}")

        print("\n")
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
