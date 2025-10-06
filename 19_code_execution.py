"""
Demo 18: Code Generation & Execution Agent
Goal: Agent that writes and executes code safely

Key Teaching Points:
- Code generation with LLMs
- Safe code execution in sandbox
- Python code interpreter
- Data analysis automation
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from strands import Agent, tool
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


@tool
def execute_python_code(code: str) -> str:
    """
    Execute Python code in a safe, isolated environment and return the output.
    Only use this for safe, non-destructive code.
    """
    # Security check - block dangerous imports and operations
    dangerous_patterns = [
        'import os',
        'import subprocess',
        'import sys',
        '__import__',
        'eval(',
        'exec(',
        'compile(',
        'open(',
        'file(',
        'input(',
        'raw_input(',
    ]

    code_lower = code.lower()
    for pattern in dangerous_patterns:
        if pattern in code_lower:
            return f"⚠️ Security Error: Code contains potentially dangerous operation: {pattern}"

    try:
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Execute the code with timeout
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5  # 5 second timeout
        )

        # Clean up temp file
        Path(temp_file).unlink()

        # Combine stdout and stderr
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n⚠️ Errors:\n" + result.stderr

        return output if output else "✅ Code executed successfully (no output)"

    except subprocess.TimeoutExpired:
        Path(temp_file).unlink()
        return "⏱️ Execution timeout (> 5 seconds)"
    except Exception as e:
        if 'temp_file' in locals():
            Path(temp_file).unlink()
        return f"❌ Execution error: {str(e)}"


@tool
def analyze_data_with_code(data: str, analysis_request: str) -> str:
    """
    Analyze data by generating and executing Python code.
    Data should be JSON format. Analysis request describes what to do.
    """
    prompt = f"""
You are a data analyst. Given this data:
{data}

Task: {analysis_request}

Write Python code to perform this analysis. Use only standard library (no imports needed for basic operations).
Print the results clearly. Do not use any file I/O or external libraries.
"""

    # In a real implementation, you'd call the agent here to generate code
    # For demo purposes, we'll show how it would work
    return f"To analyze this data: {analysis_request}\n1. Generate appropriate Python code\n2. Execute it safely\n3. Return results"


@tool
def create_visualization(data_description: str, chart_type: str = "bar") -> str:
    """
    Generate code to create a simple ASCII visualization of data.
    chart_type: 'bar', 'line', or 'table'
    """
    return f"""Here's how to create a {chart_type} chart for: {data_description}

Example ASCII bar chart code:
```python
data = {{'A': 10, 'B': 20, 'C': 15}}
max_val = max(data.values())
for label, value in data.items():
    bar = '█' * int((value / max_val) * 20)
    print(f'{{label}}: {{bar}} {{value}}')
```

Use execute_python_code to run this!"""


@tool
def debug_code(code: str, error_message: str) -> str:
    """Help debug code by analyzing the error message."""
    return f"""Debugging assistance:

Code:
{code}

Error:
{error_message}

Common issues to check:
1. Syntax errors (missing colons, parentheses)
2. Indentation problems
3. Undefined variables
4. Type mismatches
5. Logic errors

Suggested fixes will be based on the error type."""


# Create code execution agent
code_agent = Agent(
    tools=[
        execute_python_code,
        analyze_data_with_code,
        create_visualization,
        debug_code
    ],
    system_prompt="""You are a Python code generation and execution assistant.

When users ask you to:
1. Write code - Generate clean, well-commented Python code
2. Execute code - Use execute_python_code tool
3. Analyze data - Write code to process and analyze data
4. Create visualizations - Generate ASCII charts or data displays
5. Debug - Help identify and fix code issues

Safety guidelines:
- Never use file I/O operations
- Avoid external libraries (use standard library only)
- Keep code simple and focused
- Always validate user input
- Explain what the code does

For data analysis:
- Parse data structures carefully
- Show intermediate steps
- Present results clearly
- Handle edge cases
"""
)


def main():
    """Run the code execution demo."""
    print("=" * 70)
    print("💻 Code Generation & Execution Agent Demo")
    print("=" * 70)
    print()

    # Example tasks
    tasks = [
        "Write Python code to calculate the factorial of 5",
        "Create code that finds all prime numbers up to 20",
        "Write a function to reverse a string and test it with 'hello'",
        "Generate a Fibonacci sequence up to 10 numbers",
        "Create a simple ASCII bar chart showing sales: A=10, B=20, C=15",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{'='*70}")
        print(f"📝 Task {i}: {task}")
        print(f"{'='*70}")

        response = code_agent(task)
        print(f"\n{response}\n")

    # Example of direct code execution
    print("\n" + "=" * 70)
    print("🚀 Direct Code Execution Example")
    print("=" * 70)

    sample_code = """
# Calculate factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial of 5 is: {result}")
"""

    print(f"\nExecuting code:\n{sample_code}")
    result = execute_python_code(sample_code)
    print(f"\nOutput:\n{result}")

    # Example of data analysis
    print("\n" + "=" * 70)
    print("📊 Data Analysis Example")
    print("=" * 70)

    analysis_code = """
# Sales data analysis
sales_data = [100, 150, 120, 200, 180]

total = sum(sales_data)
average = total / len(sales_data)
max_sale = max(sales_data)
min_sale = min(sales_data)

print(f"Total Sales: ${total}")
print(f"Average Sale: ${average:.2f}")
print(f"Max Sale: ${max_sale}")
print(f"Min Sale: ${min_sale}")

# Simple bar chart
print("\\nSales Chart:")
for i, sale in enumerate(sales_data, 1):
    bar = '█' * (sale // 10)
    print(f"Day {i}: {bar} ${sale}")
"""

    print(f"\nExecuting analysis:\n{analysis_code}")
    result = execute_python_code(analysis_code)
    print(f"\nResults:\n{result}")

    print("\n" + "=" * 70)
    print("✨ Demo complete!")
    print("\n⚠️ Security Note: This demo uses sandboxing and blocks dangerous operations.")
    print("For production, consider using Docker containers or proper sandboxing solutions.")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add python-dotenv

2. Run the demo:
   python demo_18_code_execution.py

Features Demonstrated:
- Safe Python code execution
- Code generation with LLM
- Data analysis automation
- ASCII visualization creation
- Code debugging assistance
- Security controls

Security Features:
- Blocked dangerous imports (os, subprocess, etc.)
- Execution timeout (5 seconds)
- No file I/O operations
- Isolated temporary file execution
- Input validation

Use Cases:
- Interactive data analysis tools
- Educational coding platforms
- Automation scripting
- Report generation
- Mathematical calculations
- Data processing pipelines

Example Queries:
- "Calculate the sum of squares from 1 to 100"
- "Find all even numbers in a list [1,2,3,4,5,6,7,8,9,10]"
- "Sort these names alphabetically: [Alice, Charlie, Bob]"
- "Create a multiplication table for 7"
- "Calculate compound interest: principal=1000, rate=5%, years=3"

Production Enhancements:
- Use Docker containers for complete isolation
- Implement resource limits (memory, CPU)
- Add support for more languages (JavaScript, SQL)
- Implement code review before execution
- Add persistent workspace/environment
- Support for package installation (in container)
- Implement code versioning
- Add collaborative coding features

Docker Sandbox Example:
```python
import docker
client = docker.from_env()
container = client.containers.run(
    "python:3.11-slim",
    f"python -c '{code}'",
    remove=True,
    mem_limit="128m",
    cpu_quota=50000,
    network_disabled=True
)
```

Safety Recommendations:
1. Always run untrusted code in containers
2. Implement strict resource limits
3. Disable network access for code execution
4. Use read-only file systems
5. Implement audit logging
6. Add rate limiting per user
7. Monitor for malicious patterns
"""


"""Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 17_code_execution.py
======================================================================
💻 Code Generation & Execution Agent Demo
======================================================================


======================================================================
📝 Task 1: Write Python code to calculate the factorial of 5
======================================================================
I'll write Python code to calculate the factorial of 5. Let me create a clear, well-commented solution for you.
Tool #1: execute_python_code
Perfect! The code successfully calculates the factorial of 5. Here's what the code does:

1. **Function Definition**: Creates a `factorial()` function that handles edge cases (negative numbers, 0, and 1)
2. **Main Calculation**: Uses a for loop to multiply all numbers from 2 to n
3. **Result Display**: Shows the result in multiple formats:
   - Simple result: `5! = 120`
   - Mathematical notation: `5 × 4 × 3 × 2 × 1 = 120`
   - Step-by-step breakdown showing how the result builds up

The factorial of 5 is **120**, which is calculated as 5 × 4 × 3 × 2 × 1 = 120.

The code is robust and includes:
- Input validation for negative numbers
- Proper handling of edge cases (0! = 1, 1! = 1)
- Clear documentation and comments
- Multiple output formats for better understanding
Perfect! The code successfully calculates the factorial of 5. Here's what the code does:

1. **Function Definition**: Creates a `factorial()` function that handles edge cases (negative numbers, 0, and 1)
2. **Main Calculation**: Uses a for loop to multiply all numbers from 2 to n
3. **Result Display**: Shows the result in multiple formats:
   - Simple result: `5! = 120`
   - Mathematical notation: `5 × 4 × 3 × 2 × 1 = 120`
   - Step-by-step breakdown showing how the result builds up

The factorial of 5 is **120**, which is calculated as 5 × 4 × 3 × 2 × 1 = 120.

The code is robust and includes:
- Input validation for negative numbers
- Proper handling of edge cases (0! = 1, 1! = 1)
- Clear documentation and comments
- Multiple output formats for better understanding



======================================================================
📝 Task 2: Create code that finds all prime numbers up to 20
======================================================================
I'll create Python code to find all prime numbers up to 20 using the Sieve of Eratosthenes algorithm, which is an efficient method for finding primes.
Tool #2: execute_python_code
Excellent! The code successfully finds all prime numbers up to 20. Here's what the code does:

## **Results:**
The prime numbers up to 20 are: **[2, 3, 5, 7, 11, 13, 17, 19]**
- Total count: **8 prime numbers**

## **Code Features:**

1. **Sieve of Eratosthenes Algorithm**: 
   - Efficient method for finding multiple primes
   - Time complexity: O(n log log n)
   - Works by eliminating multiples of each prime

2. **Detailed Analysis**: 
   - Shows why each number is or isn't prime
   - Identifies the smallest factor for composite numbers

3. **Verification**: 
   - Includes a simple prime-checking function for verification
   - Confirms results match between both methods

4. **Educational Output**:
   - Step-by-step breakdown of each number
   - Clear explanation of what makes a number prime or composite

## **Key Insights:**
- **2** is the only even prime number
- **1** is not considered prime by mathematical definition
- All other even numbers are divisible by 2 (not prime)
- Odd composite numbers have odd factors (like 9 = 3×3, 15 = 3×5)

The algorithm is efficient and could easily be extended to find primes up to much larger numbers!
Excellent! The code successfully finds all prime numbers up to 20. Here's what the code does:

## **Results:**
The prime numbers up to 20 are: **[2, 3, 5, 7, 11, 13, 17, 19]**
- Total count: **8 prime numbers**

## **Code Features:**

1. **Sieve of Eratosthenes Algorithm**: 
   - Efficient method for finding multiple primes
   - Time complexity: O(n log log n)
   - Works by eliminating multiples of each prime

2. **Detailed Analysis**: 
   - Shows why each number is or isn't prime
   - Identifies the smallest factor for composite numbers

3. **Verification**: 
   - Includes a simple prime-checking function for verification
   - Confirms results match between both methods

4. **Educational Output**:
   - Step-by-step breakdown of each number
   - Clear explanation of what makes a number prime or composite

## **Key Insights:**
- **2** is the only even prime number
- **1** is not considered prime by mathematical definition
- All other even numbers are divisible by 2 (not prime)
- Odd composite numbers have odd factors (like 9 = 3×3, 15 = 3×5)

The algorithm is efficient and could easily be extended to find primes up to much larger numbers!



======================================================================
📝 Task 3: Write a function to reverse a string and test it with 'hello'
======================================================================
I'll write a Python function to reverse a string and test it with 'hello'. Let me create a comprehensive solution with multiple approaches.
Tool #3: execute_python_code
Perfect! I've created a comprehensive string reversal solution with multiple approaches. Here's what the code accomplishes:

## **Main Result:**
**'hello' reversed is 'olleh'**

## **Four Different Methods:**

1. **Slicing Method** (`s[::-1]`):
   - Most Pythonic and efficient
   - Uses negative step to reverse

2. **Loop Method**:
   - Manual character-by-character reversal
   - Educational approach showing the process

3. **Built-in Method** (`''.join(reversed(s))`):
   - Uses Python's `reversed()` function
   - Clean and readable

4. **Recursive Method**:
   - Computer science approach
   - Takes last character + recursively reverses the rest

## **Key Features:**

- **Verification**: All methods produce identical results
- **Multiple Test Cases**: Tests various strings including:
  - Regular strings (`hello`, `Python`)
  - Palindromes (`racecar`)
  - Numbers (`12345`)
  - Special characters (`Hello World!`)
  - Edge cases (empty string, single character)

- **Palindrome Detection**: Bonus feature that checks if a string reads the same forwards and backwards

- **Step-by-Step Demo**: Shows exactly how the loop method builds the reversed string

## **Performance Notes:**
- **Slicing method** is fastest and most memory-efficient
- **Loop method** is most educational for understanding the process
- **Recursive method** uses more memory due to function call stack
- **Built-in method** is clean and readable

All methods successfully reverse 'hello' to 'olleh'!
Perfect! I've created a comprehensive string reversal solution with multiple approaches. Here's what the code accomplishes:

## **Main Result:**
**'hello' reversed is 'olleh'**

## **Four Different Methods:**

1. **Slicing Method** (`s[::-1]`):
   - Most Pythonic and efficient
   - Uses negative step to reverse

2. **Loop Method**:
   - Manual character-by-character reversal
   - Educational approach showing the process

3. **Built-in Method** (`''.join(reversed(s))`):
   - Uses Python's `reversed()` function
   - Clean and readable

4. **Recursive Method**:
   - Computer science approach
   - Takes last character + recursively reverses the rest

## **Key Features:**

- **Verification**: All methods produce identical results
- **Multiple Test Cases**: Tests various strings including:
  - Regular strings (`hello`, `Python`)
  - Palindromes (`racecar`)
  - Numbers (`12345`)
  - Special characters (`Hello World!`)
  - Edge cases (empty string, single character)

- **Palindrome Detection**: Bonus feature that checks if a string reads the same forwards and backwards

- **Step-by-Step Demo**: Shows exactly how the loop method builds the reversed string

## **Performance Notes:**
- **Slicing method** is fastest and most memory-efficient
- **Loop method** is most educational for understanding the process
- **Recursive method** uses more memory due to function call stack
- **Built-in method** is clean and readable

All methods successfully reverse 'hello' to 'olleh'!



======================================================================
📝 Task 4: Generate a Fibonacci sequence up to 10 numbers
======================================================================
I'll create Python code to generate a Fibonacci sequence up to 10 numbers. Let me provide multiple approaches and detailed explanations.
Tool #4: execute_python_code
Excellent! I've generated a comprehensive Fibonacci sequence solution. Here are the key results:

## **The First 10 Fibonacci Numbers:**
**[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]**

## **Three Implementation Methods:**

1. **Iterative Method**: Most efficient, builds the sequence step by step
2. **Generator Method**: Memory efficient, yields one number at a time
3. **Recursive Method**: Educational but less efficient for large sequences

## **How Fibonacci Works:**
- **Start**: F(0) = 0, F(1) = 1
- **Rule**: Each number = sum of the two preceding numbers
- **Pattern**: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

## **Key Insights from the Analysis:**

### **Mathematical Properties:**
- **Sum of first 10 terms**: 88
- **Even numbers**: [0, 2, 8, 34] (every 3rd Fibonacci number is even)
- **Odd numbers**: [1, 1, 3, 5, 13, 21]

### **Golden Ratio Connection:**
- Ratios between consecutive terms approach the **Golden Ratio (φ ≈ 1.618034)**
- F(7)/F(6) = 13/8 = 1.625000 (getting close to φ)

### **Step-by-Step Calculation:**
- F(0) = 0, F(1) = 1 (base cases)
- F(2) = 0 + 1 = 1
- F(3) = 1 + 1 = 2
- F(4) = 1 + 2 = 3
- And so on...

## **Extended Sequence:**
For reference, the first 15 Fibonacci numbers are:
**[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]**

The Fibonacci sequence appears frequently in nature (flower petals, spiral shells, tree branches) and has many fascinating mathematical properties!
Excellent! I've generated a comprehensive Fibonacci sequence solution. Here are the key results:

## **The First 10 Fibonacci Numbers:**
**[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]**

## **Three Implementation Methods:**

1. **Iterative Method**: Most efficient, builds the sequence step by step
2. **Generator Method**: Memory efficient, yields one number at a time
3. **Recursive Method**: Educational but less efficient for large sequences

## **How Fibonacci Works:**
- **Start**: F(0) = 0, F(1) = 1
- **Rule**: Each number = sum of the two preceding numbers
- **Pattern**: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

## **Key Insights from the Analysis:**

### **Mathematical Properties:**
- **Sum of first 10 terms**: 88
- **Even numbers**: [0, 2, 8, 34] (every 3rd Fibonacci number is even)
- **Odd numbers**: [1, 1, 3, 5, 13, 21]

### **Golden Ratio Connection:**
- Ratios between consecutive terms approach the **Golden Ratio (φ ≈ 1.618034)**
- F(7)/F(6) = 13/8 = 1.625000 (getting close to φ)

### **Step-by-Step Calculation:**
- F(0) = 0, F(1) = 1 (base cases)
- F(2) = 0 + 1 = 1
- F(3) = 1 + 1 = 2
- F(4) = 1 + 2 = 3
- And so on...

## **Extended Sequence:**
For reference, the first 15 Fibonacci numbers are:
**[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]**

The Fibonacci sequence appears frequently in nature (flower petals, spiral shells, tree branches) and has many fascinating mathematical properties!



======================================================================
📝 Task 5: Create a simple ASCII bar chart showing sales: A=10, B=20, C=15
======================================================================
I'll create a simple ASCII bar chart to visualize the sales data for A=10, B=20, and C=15.
Tool #5: execute_python_code
Perfect! I've created a comprehensive ASCII bar chart visualization for your sales data (A=10, B=20, C=15). Here's what the code provides:

## **Main Horizontal Bar Chart:**
```
A | █████████████████████████ 10
B | ██████████████████████████████████████████████████ 20
C | █████████████████████████████████████ 15
```

## **Key Visualizations:**

1. **Horizontal Bar Chart**: Classic left-to-right bars showing relative sales
2. **Alternative Style**: Same chart with different bar character (▓)
3. **Vertical Bar Chart**: Traditional column chart format
4. **Statistical Summary**: Complete analysis of the data

## **Key Insights from the Analysis:**

### **Sales Performance:**
- **Best Performer**: Product B (20 units) - 44.4% of total sales
- **Average Performer**: Product C (15 units) - exactly at average
- **Needs Improvement**: Product A (10 units) - 22.2% of total sales

### **Summary Statistics:**
- **Total Sales**: 45 units
- **Average Sales**: 15.0 units
- **Range**: 10 units (from 10 to 20)

### **Performance vs Average:**
- **Product A**: 5.0 units below average
- **Product B**: 5.0 units above average  
- **Product C**: Exactly at average

## **Chart Features:**
- **Auto-scaling**: Bars automatically scale to fit the display
- **Clear labeling**: Shows both visual bars and exact values
- **Multiple formats**: Horizontal and vertical options
- **Professional formatting**: Aligned text and clear legends

The visualization clearly shows that Product B is the top performer with twice the sales of Product A, while Product C sits comfortably in the middle!
Perfect! I've created a comprehensive ASCII bar chart visualization for your sales data (A=10, B=20, C=15). Here's what the code provides:

## **Main Horizontal Bar Chart:**
```
A | █████████████████████████ 10
B | ██████████████████████████████████████████████████ 20
C | █████████████████████████████████████ 15
```

## **Key Visualizations:**

1. **Horizontal Bar Chart**: Classic left-to-right bars showing relative sales
2. **Alternative Style**: Same chart with different bar character (▓)
3. **Vertical Bar Chart**: Traditional column chart format
4. **Statistical Summary**: Complete analysis of the data

## **Key Insights from the Analysis:**

### **Sales Performance:**
- **Best Performer**: Product B (20 units) - 44.4% of total sales
- **Average Performer**: Product C (15 units) - exactly at average
- **Needs Improvement**: Product A (10 units) - 22.2% of total sales

### **Summary Statistics:**
- **Total Sales**: 45 units
- **Average Sales**: 15.0 units
- **Range**: 10 units (from 10 to 20)

### **Performance vs Average:**
- **Product A**: 5.0 units below average
- **Product B**: 5.0 units above average  
- **Product C**: Exactly at average

## **Chart Features:**
- **Auto-scaling**: Bars automatically scale to fit the display
- **Clear labeling**: Shows both visual bars and exact values
- **Multiple formats**: Horizontal and vertical options
- **Professional formatting**: Aligned text and clear legends

The visualization clearly shows that Product B is the top performer with twice the sales of Product A, while Product C sits comfortably in the middle!



======================================================================
🚀 Direct Code Execution Example
======================================================================

Executing code:

# Calculate factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial of 5 is: {result}")


Output:
Factorial of 5 is: 120


======================================================================
📊 Data Analysis Example
======================================================================

Executing analysis:

# Sales data analysis
sales_data = [100, 150, 120, 200, 180]

total = sum(sales_data)
average = total / len(sales_data)
max_sale = max(sales_data)
min_sale = min(sales_data)

print(f"Total Sales: ${total}")
print(f"Average Sale: ${average:.2f}")
print(f"Max Sale: ${max_sale}")
print(f"Min Sale: ${min_sale}")

# Simple bar chart
print("\nSales Chart:")
for i, sale in enumerate(sales_data, 1):
    bar = '█' * (sale // 10)
    print(f"Day {i}: {bar} ${sale}")


Results:
Total Sales: $750
Average Sale: $150.00
Max Sale: $200
Min Sale: $100

Sales Chart:
Day 1: ██████████ $100
Day 2: ███████████████ $150
Day 3: ████████████ $120
Day 4: ████████████████████ $200
Day 5: ██████████████████ $180


======================================================================
✨ Demo complete!

⚠️ Security Note: This demo uses sandboxing and blocks dangerous operations.
For production, consider using Docker containers or proper sandboxing solutions.
======================================================================
"""