'use client';

import { useState, useEffect } from 'react';
import { todoApi } from '@/lib/todoApi';
import type { Todo, TodoCreate, PaginatedTodos } from '@/types/todo';
import TodoList from '@/components/TodoList';
import AddTodoForm from '@/components/AddTodoForm';
import Pagination from '@/components/Pagination';

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize] = useState(10);

  const fetchTodos = async (page: number = currentPage) => {
    setLoading(true);
    setError(null);
    try {
      const data: PaginatedTodos = await todoApi.getPaginated(page, pageSize);
      setTodos(data.items);
      setTotalPages(data.total_pages);
      setCurrentPage(data.page);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos(1);
  }, []);

  const handleAddTodo = async (newTodo: TodoCreate) => {
    try {
      await todoApi.create(newTodo);
      await fetchTodos(1);
    } catch (err) {
      setError('Failed to create todo');
      console.error(err);
    }
  };

  const handleUpdateTodo = async (id: number, updates: Partial<Todo>) => {
    try {
      await todoApi.update({ id, ...updates });
      await fetchTodos();
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await todoApi.delete(id);
      await fetchTodos();
    } catch (err) {
      setError('Failed to delete todo');
      console.error(err);
    }
  };

  const handlePageChange = (page: number) => {
    fetchTodos(page);
  };

  return (
    <main className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Todo App
        </h1>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <AddTodoForm onAdd={handleAddTodo} />

        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          </div>
        ) : (
          <>
            <TodoList
              todos={todos}
              onUpdate={handleUpdateTodo}
              onDelete={handleDeleteTodo}
            />

            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            )}
          </>
        )}
      </div>
    </main>
  );
}
