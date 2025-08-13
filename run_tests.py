#!/usr/bin/env python3
"""
Test runner for BubbleTea package using pytest
"""

import subprocess
import sys
import os


def main():
    """Run all tests using pytest"""
    print("🧪 BubbleTea Pytest Test Runner")
    print("=" * 50)
    
    # Change to package directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if pytest is available
    try:
        import pytest
        print(f"✅ pytest {pytest.__version__} available")
    except ImportError:
        print("❌ pytest not installed. Please install with:")
        print("   pip install pytest pytest-asyncio")
        sys.exit(1)
    
    # Run tests
    test_commands = [
        "Basic functionality tests",
        "Config decorator tests", 
        "Integration tests",
        "Image feature tests",
        "Simple config tests"
    ]
    
    test_files = [
        "tests/test_bot.py",
        "tests/test_config_decorator.py",
        "tests/test_config_integration.py", 
        "tests/test_image_features.py",
        "tests/test_config_simple.py"
    ]
    
    passed = 0
    total = len(test_files)
    
    for i, (description, test_file) in enumerate(zip(test_commands, test_files)):
        print(f"\n[{i+1}/{total}] Running {description}...")
        
        try:
            # Use subprocess to avoid pytest plugin conflicts
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, "-v", "--tb=short"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ {description} - PASSED")
                passed += 1
            else:
                print(f"❌ {description} - FAILED")
                print("STDERR:", result.stderr[:500])
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {description} - TIMEOUT")
        except Exception as e:
            print(f"💥 {description} - ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All test suites completed successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) had issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())