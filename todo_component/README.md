# React Todo Component

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

