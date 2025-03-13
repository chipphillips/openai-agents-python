import os
import json
from ai_dev_team import AIDevTeam

class TodoComponentCreator:
    """Class for creating a Todo component using the AI development team"""
    
    def __init__(self):
        self.dev_team = AIDevTeam()
        self.code_files = {}
        self.project_name = "Todo Component"
    
    def initialize_project(self):
        """Initialize the project by setting up the context"""
        self.dev_team.project_context["name"] = "React Todo Component"
        self.dev_team.project_context["requirements"] = [
            "Create a React Todo list component",
            "Component should allow adding new tasks",
            "Component should allow marking tasks as complete",
            "Component should allow deleting tasks",
            "Component should have a clean, modern UI",
            "Component should be responsive"
        ]
        self.dev_team.project_context["status"] = {
            "requirements_complete": True,
            "architecture_complete": False,
            "frontend_progress": 0,
            "backend_progress": 0,
            "testing_progress": 0
        }
    
    def design_component(self):
        """Work with the architect to design the component"""
        # Request architecture from the architect
        design_query = """
        Design the architecture for our React Todo component. 
        We need to determine:
        1. Component structure
        2. State management approach
        3. Data flow between components
        4. UI/UX considerations
        
        Please provide a comprehensive design that covers these aspects.
        """
        
        # Process the query and get the response
        response = self.dev_team.process_query(design_query)
        print("\n--- Component Design ---")
        print(response)
        
        # Update project context with architecture 
        self.dev_team.project_context["architecture"] = {
            "design_complete": True,
            "description": "React Todo Component Architecture"
        }
        self.dev_team.project_context["status"]["architecture_complete"] = True
        
        return response
    
    def implement_component(self):
        """Work with the frontend developer to implement the component"""
        # Request implementation from the frontend developer
        implementation_query = """
        Create a complete React Todo component based on our design.
        
        Requirements:
        1. Component should allow adding new tasks
        2. Component should allow marking tasks as complete
        3. Component should allow deleting tasks
        4. Component should have a clean, modern UI with CSS
        5. Component should be responsive
        
        Please provide the complete implementation with all necessary files.
        """
        
        # Process the query and get the response
        response = self.dev_team.process_query(implementation_query)
        print("\n--- Component Implementation ---")
        print(response)
        
        # Extract code from the response
        self._extract_code_from_response(response)
        
        # Update project context
        self.dev_team.project_context["status"]["frontend_progress"] = 100
        
        return response
    
    def test_component(self):
        """Work with the QA tester to test the component"""
        # Request testing from the QA tester
        testing_query = """
        Review our Todo component implementation and identify any potential issues or improvements.
        
        Focus on:
        1. Functionality testing
        2. Edge cases
        3. User experience
        4. Accessibility
        5. Performance considerations
        
        Please provide a comprehensive test report.
        """
        
        # Process the query and get the response
        response = self.dev_team.process_query(testing_query)
        print("\n--- Component Testing ---")
        print(response)
        
        # Update project context
        self.dev_team.project_context["status"]["testing_progress"] = 100
        
        return response
    
    def create_documentation(self):
        """Work with the technical writer to create documentation"""
        # Request documentation from the technical writer
        documentation_query = """
        Create comprehensive documentation for our React Todo component.
        
        Include:
        1. Overview of the component
        2. Installation instructions
        3. Usage examples
        4. Props/API documentation
        5. Customization options
        
        Please provide complete documentation that would be helpful for developers using this component.
        """
        
        # Process the query and get the response
        response = self.dev_team.process_query(documentation_query)
        print("\n--- Component Documentation ---")
        print(response)
        
        # Extract README from the response
        self._extract_readme_from_response(response)
        
        return response
    
    def _extract_code_from_response(self, response):
        """Extract code blocks from the response and save them to files"""
        # Look for code blocks in markdown format - ```jsx or ```javascript or ```css
        lines = response.split('\n')
        in_code_block = False
        current_file = None
        current_code = []
        
        for line in lines:
            # Check for start of code block with file name
            if not in_code_block and (line.startswith("```jsx") or line.startswith("```javascript") or 
                                    line.startswith("```js") or line.startswith("```css") or 
                                    line.startswith("```html") or line.startswith("```tsx")):
                in_code_block = True
                
                # Try to extract file name
                if ":" in line:
                    parts = line.split(":", 1)
                    current_file = parts[1].strip()
                    file_type = parts[0].replace("```", "").strip()
                    if not current_file.endswith(f".{file_type}") and not "." in current_file:
                        current_file = f"{current_file}.{file_type}"
                continue
                
            # Check for end of code block
            elif in_code_block and line.startswith("```"):
                in_code_block = False
                
                # Save the code if we have a file name
                if current_file:
                    self.code_files[current_file] = "\n".join(current_code)
                    print(f"Extracted code for file: {current_file}")
                
                current_file = None
                current_code = []
                continue
                
            # Collect code lines
            if in_code_block:
                current_code.append(line)
    
    def _extract_readme_from_response(self, response):
        """Extract README from the response"""
        # Save the entire response as README.md
        self.code_files["README.md"] = response
    
    def save_files(self, output_dir="todo_component"):
        """Save all extracted files to disk"""
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save each file
        for filename, content in self.code_files.items():
            file_path = os.path.join(output_dir, filename)
            
            # Create subdirectories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Saved file: {file_path}")
    
    def create_todo_component(self):
        """Run the complete process to create a Todo component"""
        print("\n=== Starting Todo Component Creation ===\n")
        
        # Step 1: Initialize the project
        self.initialize_project()
        print("Project initialized")
        
        # Step 2: Design the component
        self.design_component()
        
        # Step 3: Implement the component
        self.implement_component()
        
        # Step 4: Test the component
        self.test_component()
        
        # Step 5: Create documentation
        self.create_documentation()
        
        # Step 6: Save all files
        self.save_files()
        
        print("\n=== Todo Component Creation Complete ===\n")
        print(f"Files created: {list(self.code_files.keys())}")


def main():
    creator = TodoComponentCreator()
    creator.create_todo_component()


if __name__ == "__main__":
    main() 