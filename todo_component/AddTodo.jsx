import React, { useState } from 'react';
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