#!/bin/bash
set -uo pipefail

format_status=0
lint_status=0
typecheck_status=0
test_status=0

echo "=== Running formatter ==="
ruff format . || format_status=$?

echo ""
echo "=== Running linter ==="
ruff check . || lint_status=$?

echo ""
echo "=== Running type checker ==="
mypy . || typecheck_status=$?

echo ""
echo "=== Running tests ==="
pytest || test_status=$?

echo ""
echo "=== Summary ==="
[ $format_status -eq 0 ] && echo "Format:    OK" || echo "Format:    FAILED"
[ $lint_status -eq 0 ] && echo "Lint:      OK" || echo "Lint:      FAILED"
[ $typecheck_status -eq 0 ] && echo "Typecheck: OK" || echo "Typecheck: FAILED"
[ $test_status -eq 0 ] && echo "Tests:     OK" || echo "Tests:     FAILED"

if [ $format_status -ne 0 ] || [ $lint_status -ne 0 ] || [ $typecheck_status -ne 0 ] || [ $test_status -ne 0 ]; then
    exit 1
fi
