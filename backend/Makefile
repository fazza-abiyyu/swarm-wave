# Backend Test Commands
# Simple Makefile for running various test configurations

.PHONY: test test-verbose test-app test-aco test-pso test-utils test-coverage clean

# Run all tests (default)
test:
	@echo "Running all backend unit tests..."
	@python tests/run_tests.py

# Run tests with verbose output
test-verbose:
	@echo "Running all tests with verbose output..."
	@python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test modules
test-app:
	@echo "Running Flask application tests..."
	@python -m unittest tests.test_app -v

test-aco:
	@echo "Running ACO algorithm tests..."
	@python -m unittest tests.test_aco -v

test-pso:
	@echo "Running PSO algorithm tests..."
	@python -m unittest tests.test_pso -v

test-utils:
	@echo "Running utility function tests..."
	@python -m unittest tests.test_utilities -v

# Interactive test runner
test-interactive:
	@echo "Starting interactive test runner..."
	@python tests/interactive_runner.py

# Test coverage (requires coverage.py: pip install coverage)
test-coverage:
	@echo "Running tests with coverage analysis..."
	@coverage run --source=. -m unittest discover -s tests -p "test_*.py"
	@coverage report -m
	@coverage html
	@echo "Coverage report generated in htmlcov/"

# Clean test artifacts
clean:
	@echo "Cleaning test artifacts..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/
	@rm -f .coverage

# Help
help:
	@echo "Available test commands:"
	@echo "  make test              - Run all tests (default)"
	@echo "  make test-verbose      - Run tests with verbose output"
	@echo "  make test-app          - Run Flask application tests only"
	@echo "  make test-aco          - Run ACO algorithm tests only"
	@echo "  make test-pso          - Run PSO algorithm tests only"
	@echo "  make test-utils        - Run utility function tests only"
	@echo "  make test-interactive  - Interactive test runner"
	@echo "  make test-coverage     - Run tests with coverage analysis"
	@echo "  make clean             - Clean test artifacts"
	@echo "  make help              - Show this help message"
