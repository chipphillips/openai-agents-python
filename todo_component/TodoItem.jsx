import React from 'react';
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