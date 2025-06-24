from langchain.tools import tool
from pydantic import BaseModel, Field
import re
import math

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression or calculation to evaluate (e.g., '100 * 50', '2500 + 1000', 'sqrt(16)')")

class CalculatorTools():
    @tool("calculate", args_schema=CalculatorInput, return_direct=False)
    @staticmethod
    def calculate(expression: str) -> str:
        """Calculate mathematical expressions safely. Supports basic arithmetic, percentages, and common mathematical functions."""
        
        # Debug logging
        print(f"DEBUG: CalculatorTools received expression type: {type(expression)}")
        print(f"DEBUG: CalculatorTools received expression value: {repr(expression)}")
        
        # Handle empty or invalid input
        if not expression or not isinstance(expression, str) or not expression.strip():
            return "Error: Please provide a valid mathematical expression as a string."
        
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Replace common mathematical functions and constants
            expression = expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('pow', 'math.pow')
            expression = expression.replace('pi', 'math.pi')
            expression = expression.replace('e', 'math.e')
            expression = expression.replace('sin', 'math.sin')
            expression = expression.replace('cos', 'math.cos')
            expression = expression.replace('tan', 'math.tan')
            expression = expression.replace('log', 'math.log')
            expression = expression.replace('abs', 'abs')
            
            # Handle percentage calculations
            if '%' in expression:
                # Simple percentage handling (e.g., "20% of 100" or "100 + 20%")
                if ' of ' in expression:
                    parts = expression.split(' of ')
                    if len(parts) == 2:
                        percent = float(parts[0].replace('%', '')) / 100
                        value = float(parts[1])
                        result = percent * value
                        return f"Result: {result}"
                elif '+' in expression and '%' in expression:
                    # Handle cases like "100 + 20%"
                    parts = expression.split('+')
                    if len(parts) == 2 and '%' in parts[1]:
                        base = float(parts[0].strip())
                        percent = float(parts[1].strip().replace('%', '')) / 100
                        result = base + (base * percent)
                        return f"Result: {result}"
            
            # Create a safe evaluation environment
            safe_dict = {
                "__builtins__": {},
                "math": math,
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow
            }
            
            # Validate expression contains only safe characters
            if not re.match(r'^[0-9+\-*/.() \t\n,mathsqrtpowlogsincotan]+$', expression.replace('math.', '')):
                return "Error: Expression contains invalid characters. Only numbers, basic operators (+, -, *, /, **), parentheses, and math functions are allowed."
            
            # Evaluate the expression
            result = eval(expression, safe_dict)
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 2)
            
            return f"Result: {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except ValueError as e:
            return f"Error: Invalid mathematical expression - {str(e)}"
        except SyntaxError:
            return "Error: Invalid syntax in mathematical expression."
        except Exception as e:
            return f"Error: Unable to calculate expression - {str(e)}"