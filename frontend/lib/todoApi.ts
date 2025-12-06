import { apiClient } from './api';
import type { Todo, TodoCreate, TodoUpdate, PaginatedTodos } from '@/types/todo';

export const todoApi = {
  getAll: async (): Promise<Todo[]> => {
    return apiClient.get<Todo[]>('/todo');
  },

  getPaginated: async (page: number = 1, pageSize: number = 10): Promise<PaginatedTodos> => {
    return apiClient.get<PaginatedTodos>(`/todo/${page}?page_size=${pageSize}`);
  },

  create: async (todo: TodoCreate): Promise<Todo> => {
    return apiClient.post<Todo>('/todo', todo);
  },

  update: async (todo: TodoUpdate): Promise<Todo> => {
    return apiClient.put<Todo>('/todo', todo);
  },

  delete: async (id: number): Promise<void> => {
    return apiClient.delete<void>(`/todo?id=${id}`);
  },
};
