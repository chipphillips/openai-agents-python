import React from 'react';
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