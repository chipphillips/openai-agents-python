import os
import json
import re
from ai_dev_team import AIDevTeam

def create_todo_component():
    """Generate a React Todo component using the Frontend Developer agent"""
    print("\n=== Starting Todo Component Creation ===\n")
    
    # Initialize the AI development team
    dev_team = AIDevTeam()
    
    # Set the current agent to frontend_dev directly
    dev_team.current_agent = "frontend_dev"
    
    # Create the query for the frontend developer
    query = """
    Create a complete React Todo list component with the following features:
    
    1. Adding new tasks
    2. Marking tasks as complete
    3. Deleting tasks
    4. Clean, modern UI with CSS
    5. Responsive design
    
    Please provide all necessary files with proper file naming. Include:
    1. The main TodoList component (TodoList.jsx)
    2. Any sub-components (TodoItem.jsx, AddTodo.jsx, etc.)
    3. CSS styles (TodoList.css)
    4. A sample App.jsx file showing how to use the component
    
    Start each code block with ```jsx filename.jsx or ```css filename.css to clearly indicate the file name.
    Make sure to include detailed code explanations and comments.
    """
    
    # Process the query
    print("Requesting Todo component implementation from Frontend Developer...")
    response = dev_team.process_query(query)
    
    # Save the full response to a file for examination
    with open("full_response.txt", "w", encoding="utf-8") as f:
        f.write(response)
    print("Full response saved to full_response.txt")
    
    # Extract code blocks from the response
    code_files = {}
    
    # Look for code blocks in markdown format
    lines = response.split('\n')
    in_code_block = False
    current_file = None
    current_code = []
    
    for line in lines:
        # Check for start of code block with file name
        if not in_code_block and line.strip().startswith("```"):
            in_code_block = True
            # Extract the file name from the line
            parts = line.strip().split(None, 1)  # Split by whitespace into max 2 parts
            if len(parts) > 1:
                file_type = parts[0].replace("```", "").strip()
                current_file = parts[1].strip()
                # Add default extension if none provided
                if "." not in current_file:
                    extensions = {
                        "jsx": ".jsx",
                        "js": ".js",
                        "javascript": ".js",
                        "css": ".css",
                        "html": ".html",
                        "tsx": ".tsx",
                        "typescript": ".ts"
                    }
                    ext = extensions.get(file_type.lower(), f".{file_type.lower()}")
                    current_file = current_file + ext
            else:
                # No filename provided, use a default
                file_type = parts[0].replace("```", "").strip()
                if file_type.lower() in ["jsx", "js", "javascript"]:
                    current_file = "TodoComponent.jsx"
                elif file_type.lower() == "css":
                    current_file = "TodoComponent.css"
                elif file_type.lower() in ["html", "tsx", "typescript"]:
                    current_file = f"TodoComponent.{file_type.lower()}"
            
            continue
        
        # Check for end of code block
        elif in_code_block and line.strip() == "```":
            in_code_block = False
            
            # Save the code if we have a file name
            if current_file and current_code:
                code_files[current_file] = "\n".join(current_code)
                print(f"Extracted code for file: {current_file}")
            
            current_file = None
            current_code = []
            continue
        
        # Collect code lines
        if in_code_block:
            current_code.append(line)
    
    # Create README.md from the response
    if "README.md" not in code_files:
        readme_content = "# React Todo Component\n\n"
        readme_content += response.split("```")[0]  # Add the text before the first code block
        code_files["README.md"] = readme_content
    
    # Save files to disk
    output_dir = "todo_component"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save each file
    for filename, content in code_files.items():
        file_path = os.path.join(output_dir, filename)
        
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Saved file: {file_path}")
    
    # If we didn't extract any code files, create a basic implementation
    if len(code_files) <= 1:  # Only README.md
        print("No code files were extracted. Creating basic implementation...")
        create_basic_todo_component(output_dir)
    
    print("\n=== Todo Component Creation Complete ===\n")
    print(f"Files created: {list(code_files.keys())}")
    print(f"Files are located in the '{output_dir}' directory")
    
    return code_files


def create_basic_todo_component(output_dir):
    """Create a basic Todo component implementation"""
    files = {
        "TodoList.jsx": """import React, { useState } from 'react';
import TodoItem from './TodoItem';
import AddTodo from './AddTodo';
import './TodoList.css';

/**
 * TodoList Component - Main component for managing todo items
 */
const TodoList = () => {
  // State to store todo items
  const [todos, setTodos] = useState([]);

  // Add a new todo item
  const addTodo = (text) => {
    if (text.trim() === '') return;
    const newTodo = {
      id: Date.now(),
      text,
      completed: false
    };
    setTodos([...todos, newTodo]);
  };

  // Toggle todo completion status
  const toggleComplete = (id) => {
    setTodos(
      todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  // Delete a todo item
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="todo-list-container">
      <h1>Todo List</h1>
      <AddTodo addTodo={addTodo} />
      <div className="todo-items">
        {todos.length === 0 ? (
          <p className="empty-message">No tasks yet. Add some tasks to get started!</p>
        ) : (
          todos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              toggleComplete={toggleComplete}
              deleteTodo={deleteTodo}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default TodoList;
""",
        "TodoItem.jsx": """import React from 'react';
import './TodoList.css';

/**
 * TodoItem Component - Displays a single todo item
 * @param {Object} props - Component props
 * @param {Object} props.todo - Todo item data
 * @param {Function} props.toggleComplete - Function to toggle completion status
 * @param {Function} props.deleteTodo - Function to delete the todo
 */
const TodoItem = ({ todo, toggleComplete, deleteTodo }) => {
  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleComplete(todo.id)}
        className="todo-checkbox"
      />
      <span className="todo-text">{todo.text}</span>
      <button 
        onClick={() => deleteTodo(todo.id)}
        className="delete-button"
        aria-label="Delete task"
      >
        Delete
      </button>
    </div>
  );
};

export default TodoItem;
""",
        "AddTodo.jsx": """import React, { useState } from 'react';
import './TodoList.css';

/**
 * AddTodo Component - Form for adding new todo items
 * @param {Object} props - Component props
 * @param {Function} props.addTodo - Function to add a new todo
 */
const AddTodo = ({ addTodo }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    addTodo(text);
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="add-todo-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new task..."
        className="todo-input"
      />
      <button type="submit" className="add-button">Add</button>
    </form>
  );
};

export default AddTodo;
""",
        "TodoList.css": """.todo-list-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.add-todo-form {
  display: flex;
  margin-bottom: 20px;
}

.todo-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
}

.add-button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.add-button:hover {
  background-color: #45a049;
}

.todo-items {
  margin-top: 20px;
}

.todo-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.todo-item:hover {
  background-color: #f9f9f9;
}

.todo-checkbox {
  margin-right: 10px;
  transform: scale(1.2);
}

.todo-text {
  flex: 1;
  font-size: 16px;
}

.completed .todo-text {
  text-decoration: line-through;
  color: #888;
}

.delete-button {
  padding: 6px 12px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #d32f2f;
}

.empty-message {
  text-align: center;
  color: #888;
  font-style: italic;
}

/* Responsive styles */
@media (max-width: 600px) {
  .todo-list-container {
    padding: 15px;
    margin: 10px;
  }
  
  .add-todo-form {
    flex-direction: column;
  }
  
  .todo-input {
    border-radius: 4px;
    margin-bottom: 10px;
  }
  
  .add-button {
    border-radius: 4px;
    width: 100%;
  }
}
""",
        "App.jsx": """import React from 'react';
import TodoList from './TodoList';

/**
 * App Component - Root component that includes the TodoList
 */
const App = () => {
  return (
    <div className="app">
      <TodoList />
    </div>
  );
};

export default App;
""",
        "README.md": """# React Todo Component

A clean, modern, and responsive Todo List component built with React.

## Features

- Add new tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Responsive design
- Clean and modern UI

## Installation

1. Copy the component files into your React project:
   - TodoList.jsx
   - TodoItem.jsx
   - AddTodo.jsx
   - TodoList.css

2. Import and use the TodoList component in your app:

```jsx
import React from 'react';
import TodoList from './path/to/TodoList';

function App() {
  return (
    <div className="App">
      <TodoList />
    </div>
  );
}

export default App;
```

## Component Structure

- **TodoList.jsx**: Main component that manages the state and renders the list
- **TodoItem.jsx**: Component for rendering individual todo items
- **AddTodo.jsx**: Component for adding new todo items
- **TodoList.css**: Styling for all todo components

## Customization

You can customize the appearance by modifying the TodoList.css file or by adding your own custom styles.

## Props

### TodoList
No props required. Manages its own state internally.

### TodoItem
- `todo`: Object with `id`, `text`, and `completed` properties
- `toggleComplete`: Function to toggle completion status
- `deleteTodo`: Function to delete the todo

### AddTodo
- `addTodo`: Function to add a new todo

## License

This component is available for use under the MIT License.
"""
    }
    
    # Save each file
    for filename, content in files.items():
        file_path = os.path.join(output_dir, filename)
        
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Created basic file: {file_path}")


if __name__ == "__main__":
    create_todo_component() 