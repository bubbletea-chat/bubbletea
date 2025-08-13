#!/usr/bin/env python3
"""
Validate that all test files have been converted to pytest format
"""

import ast
import os
import sys


def validate_test_file(filepath):
    """Validate that a test file uses pytest patterns"""
    print(f"Validating {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Parse the AST to check structure
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"  ❌ Syntax error: {e}")
        return False
    
    # Check for pytest patterns
    has_pytest_import = 'import pytest' in content
    has_test_functions = any(
        isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
        for node in ast.walk(tree)
    )
    
    # Check for old unittest patterns (should not be present)
    has_unittest_classes = any(
        isinstance(node, ast.ClassDef) and node.name.startswith('Test')
        for node in ast.walk(tree)
    )
    
    # Modern pytest patterns
    has_fixtures = '@pytest.fixture' in content
    has_async_tests = '@pytest.mark.asyncio' in content or 'async def test_' in content
    
    print(f"  ✅ Syntax valid")
    print(f"  {'✅' if has_pytest_import else '⚠️'} pytest import: {has_pytest_import}")
    print(f"  {'✅' if has_test_functions else '❌'} test_ functions: {has_test_functions}")
    print(f"  {'✅' if not has_unittest_classes else '⚠️'} No unittest classes: {not has_unittest_classes}")
    
    if has_fixtures:
        print(f"  ✅ Uses pytest fixtures")
    if has_async_tests:
        print(f"  ✅ Has async test support")
    
    return has_test_functions and not has_unittest_classes


def main():
    """Validate all test files"""
    print("🧪 BubbleTea Pytest Conversion Validator")
    print("=" * 50)
    
    test_dir = "tests"
    test_files = [
        "test_bot.py",
        "test_config_decorator.py", 
        "test_config_simple.py",
        "test_config_integration.py",
        "test_image_features.py"
    ]
    
    valid_count = 0
    total_files = len(test_files)
    
    for test_file in test_files:
        filepath = os.path.join(test_dir, test_file)
        
        if not os.path.exists(filepath):
            print(f"❌ Missing: {filepath}")
            continue
            
        if validate_test_file(filepath):
            valid_count += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"📊 Validation Summary: {valid_count}/{total_files} files valid")
    
    if valid_count == total_files:
        print("\n🎉 All test files successfully converted to pytest format!")
        print("\nTo run tests (once pytest environment is fixed):")
        print("  python -m pytest tests/ -v")
        return 0
    else:
        print(f"\n⚠️  {total_files - valid_count} test file(s) need fixes")
        return 1


if __name__ == "__main__":
    sys.exit(main())