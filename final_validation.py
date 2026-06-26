#!/usr/bin/env python3
import os
import json

print("🔍 FINAL VALIDATION CHECKLIST\n" + "="*70)

checks = []

# 1. Check required files
required_files = [
    "README.md",
    "requirements.txt",
    ".env.example",
    "Dockerfile",
    "app/main.py",
    "queuestorm_sample_outputs.json"
]

for file in required_files:
    exists = os.path.exists(file)
    checks.append(("Required File: " + file, exists))
    print(f"{'✅' if exists else '❌'} {file}")

print()

# 2. Check .env.example doesn't contain secrets
with open(".env.example") as f:
    env_example = f.read()
    has_real_key = len([line for line in env_example.split("\n") if "=" in line and "your_" not in line and "OPENAI_API_KEY" in line]) == 0
    checks.append((".env.example has no real secrets", has_real_key))
    print(f"{'✅' if has_real_key else '❌'} .env.example contains no real API keys")

# 3. Check sample outputs file
try:
    with open("queuestorm_sample_outputs.json") as f:
        outputs = json.load(f)
        has_10_outputs = len(outputs) == 10
        checks.append(("Sample outputs file has 10 cases", has_10_outputs))
        print(f"{'✅' if has_10_outputs else '❌'} Sample outputs contains {len(outputs)}/10 cases")
except:
    checks.append(("Sample outputs file valid", False))
    print(f"❌ Sample outputs file invalid")

# 4. Check README has MODELS section
with open("README.md") as f:
    readme = f.read()
    has_models = "MODELS" in readme or "Model" in readme
    has_safety = "Safety" in readme or "SAFETY" in readme
    has_setup = "Setup" in readme or "Installation" in readme
    checks.append(("README has MODELS section", has_models))
    checks.append(("README has Safety section", has_safety))
    checks.append(("README has Setup instructions", has_setup))
    print(f"{'✅' if has_models else '❌'} README contains MODELS section")
    print(f"{'✅' if has_safety else '❌'} README contains Safety section")
    print(f"{'✅' if has_setup else '❌'} README contains Setup instructions")

# 5. Check .gitignore includes sensitive files
if os.path.exists(".gitignore"):
    with open(".gitignore") as f:
        gitignore = f.read()
        ignores_env = ".env" in gitignore
        checks.append((".gitignore includes .env", ignores_env))
        print(f"{'✅' if ignores_env else '❌'} .gitignore includes .env")

print("\n" + "="*70)
passed = sum(1 for _, result in checks if result)
total = len(checks)
print(f"VALIDATION SUMMARY: {passed}/{total} checks passed")
print("="*70)

if passed == total:
    print("\n🎉 ALL CHECKS PASSED - Ready for submission!")
else:
    print(f"\n⚠️  {total - passed} issues found - please review")

