# Backend Unit Tests

This directory contains comprehensive unit tests for the Swarm Wave backend components.

## Test Structure

```
tests/
├── __init__.py           # Test package initialization
├── test_app.py          # Flask application endpoint tests
├── test_aco.py          # ACO algorithm tests  
├── test_pso.py          # PSO algorithm tests
├── test_utilities.py    # Utility function tests
├── run_tests.py         # Test runner script
└── README.md           # This file
```

## Test Coverage

### 1. Flask Application Tests (`test_app.py`)
- Health check endpoint validation
- Response structure verification
- Error handling for missing/invalid parameters
- Algorithm availability checks

### 2. ACO Algorithm Tests (`test_aco.py`)
- Initialization parameters validation
- Dependency parsing and handling
- Sequence generation logic
- Load balancing calculations
- Dependency satisfaction checking

### 3. PSO Algorithm Tests (`test_pso.py`)
- Swarm initialization
- Position-to-sequence conversion
- Dependency-aware sequence generation
- Particle evaluation logic
- Load balance index calculations

### 4. Utility Function Tests (`test_utilities.py`)
- Safe type conversion functions
- Data formatting utilities
- Default agent generation
- Cost function validation

## Running Tests

### Individual Test Files
```bash
# Run specific test file
python -m unittest tests.test_app
python -m unittest tests.test_aco
python -m unittest tests.test_pso
python -m unittest tests.test_utilities
```

### All Tests with Custom Runner
```bash
# Run comprehensive test suite
python tests/run_tests.py
```

### Standard unittest Discovery
```bash
# Run all tests with discovery
python -m unittest discover -s tests -p "test_*.py" -v
```

## Test Features

### Comprehensive Coverage
- **API Endpoints**: All Flask routes tested
- **Algorithm Logic**: Core ACO/PSO functionality validated
- **Error Handling**: Invalid inputs and edge cases covered
- **Dependency System**: Task dependency logic thoroughly tested

### Mock Support
- Uses `unittest.mock` for external dependencies
- Isolated testing environment
- Predictable test outcomes

### Detailed Reporting
- Verbose output with test descriptions
- Success/failure statistics
- Error and failure details
- Custom test runner with summary

## Test Data

### Sample Tasks
```python
tasks = [
    {'id': 'Task_1', 'length': 5, 'cost': 10},
    {'id': 'Task_2', 'length': 3, 'cost': 8},  
    {'id': 'Task_3', 'length': 7, 'cost': 12}
]
```

### Sample Agents
```python
agents = [
    {'id': 'Agent_1'},
    {'id': 'Agent_2'}
]
```

### Dependency Scenarios
- Independent tasks (no dependencies)
- Linear dependencies (Task_2 → Task_1)
- Complex dependencies (Task_3 → Task_1, Task_2)

## Expected Results

When all tests pass, you should see:
```
Tests run: X
Failures: 0
Errors: 0
Success rate: 100.0%
```

## Contributing

When adding new features to the backend:

1. **Add corresponding tests** in the appropriate test file
2. **Update test data** if new parameters are introduced
3. **Run full test suite** before committing
4. **Maintain test coverage** above 80%

## Dependencies

Tests require the same dependencies as the main application:
- `flask`
- `numpy`
- `unittest` (built-in)
- `unittest.mock` (built-in)
