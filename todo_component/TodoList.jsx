import React, { useState } from 'react';
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