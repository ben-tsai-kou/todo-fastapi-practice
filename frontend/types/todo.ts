export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TodoUpdate {
  id: number;
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface PaginatedTodos {
  items: Todo[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
