.PHONY: run test install-hooks clean

# Run Midpoint
run:
	python scripts/run.py $(ARGS)

# Run tests
test:
	python -m pytest tests/ -v

# Run memory-specific tests
test-memory:
	python -m pytest tests/test_memory_*.py -v

# Install git hooks
install-hooks:
	@echo "Installing git pre-commit hook..."
	@cp scripts/hooks/pre-commit-hook.sh .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed successfully!"
	@echo "The hook will run memory tests before each commit."

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# Help command
help:
	@echo "Available commands:"
	@echo "  make run ARGS=\"...\"   - Run Midpoint with optional arguments"
	@echo "  make test               - Run all tests"
	@echo "  make test-memory        - Run memory-specific tests"
	@echo "  make install-hooks      - Install git hooks"
	@echo "  make clean              - Clean temporary files" 