#!/bin/bash

# Test runner script for different test types

set -e

echo "🧪 Test Suite Runner"
echo "====================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "No virtual environment detected. Activating if exists..."
    if [[ -d "venv" ]]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "No virtual environment found. Please create one first."
        exit 1
    fi
fi

# Install test dependencies if not already installed
print_status "Installing test dependencies..."
pip install -r requirements-test.txt

# Function to run specific test types
run_contract_tests() {
    print_status "Running Contract Tests (60%)..."
    echo "Testing external API contracts..."
    pytest -m contract --tb=short -v
    print_success "Contract tests completed!"
}

run_integration_tests() {
    print_status "Running Integration Tests (30%)..."
    echo "Testing component interactions..."
    pytest -m integration --tb=short -v
    print_success "Integration tests completed!"
}

run_unit_tests() {
    print_status "Running Unit Tests (10%)..."
    echo "Testing business logic..."
    pytest -m unit --tb=short -v
    print_success "Unit tests completed!"
}

run_performance_tests() {
    print_status "Running Performance Tests..."
    echo "Testing performance characteristics..."
    pytest -m slow --tb=short -v
    print_success "Performance tests completed!"
}

run_all_tests() {
    print_status "Running All Tests with Coverage..."
    pytest --cov=src --cov-report=html --cov-report=term-missing --tb=short -v
    print_success "All tests completed!"
    print_status "Coverage report generated in htmlcov/"
}

run_parallel_tests() {
    print_status "Running Tests in Parallel..."
    pytest -n auto --cov=src --cov-report=term-missing --tb=short -v
    print_success "Parallel tests completed!"
}

# Menu for test selection
show_menu() {
    echo ""
    echo "Select test type to run:"
    echo "1) Contract Tests (API contracts)"
    echo "2) Integration Tests (Component interaction)"
    echo "3) Unit Tests (Business logic)"
    echo "4) Performance Tests (Slow tests)"
    echo "5) All Tests (with coverage)"
    echo "6) All Tests (parallel execution)"
    echo "7) Quick Tests (Unit + Contract only)"
    echo "8) Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice
}

# Main execution
main() {
    if [[ $# -eq 0 ]]; then
        show_menu
        case $choice in
            1)
                run_contract_tests
                ;;
            2)
                run_integration_tests
                ;;
            3)
                run_unit_tests
                ;;
            4)
                run_performance_tests
                ;;
            5)
                run_all_tests
                ;;
            6)
                run_parallel_tests
                ;;
            7)
                print_status "Running Quick Tests (Unit + Contract)..."
                pytest -m "unit or contract" --tb=short -v
                print_success "Quick tests completed!"
                ;;
            8)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please select 1-8."
                main
                ;;
        esac
    else
        # Command line arguments
        case $1 in
            "contract")
                run_contract_tests
                ;;
            "integration")
                run_integration_tests
                ;;
            "unit")
                run_unit_tests
                ;;
            "performance")
                run_performance_tests
                ;;
            "all")
                run_all_tests
                ;;
            "parallel")
                run_parallel_tests
                ;;
            "quick")
                pytest -m "unit or contract" --tb=short -v
                ;;
            *)
                print_error "Unknown test type: $1"
                echo "Available: contract, integration, unit, performance, all, parallel, quick"
                exit 1
                ;;
        esac
    fi
}

# Check if tests directory exists
if [[ ! -d "tests" ]]; then
    print_error "Tests directory not found. Please run from project root."
    exit 1
fi

# Run main function
main "$@"