# Todo App Frontend

Next.js + TypeScript + Tailwind CSS frontend for the Todo App.

## Features

- Create, Read, Update, Delete todos
- Pagination support
- Clean and responsive UI
- Type-safe API client
- Encapsulated fetch API

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```bash
cp .env.example .env.local
```

3. Update the API URL in `.env.local` if needed:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Routes

The app expects the following API endpoints:

- `GET /todo` - Get all todos
- `POST /todo` - Create a new todo
- `PUT /todo` - Update a todo
- `DELETE /todo?id={id}` - Delete a todo
- `GET /todo/{page}?page_size={size}` - Get paginated todos

## Project Structure

```
.
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── AddTodoForm.tsx
│   ├── Pagination.tsx
│   ├── TodoItem.tsx
│   └── TodoList.tsx
├── lib/
│   ├── api.ts          # Generic API client
│   └── todoApi.ts      # Todo-specific API methods
└── types/
    └── todo.ts         # TypeScript types
```

## API Client Usage

The API client is encapsulated in `lib/api.ts` and provides:

- `get<T>(endpoint)` - GET request
- `post<T>(endpoint, data)` - POST request
- `put<T>(endpoint, data)` - PUT request
- `delete<T>(endpoint)` - DELETE request

Example:
```typescript
import { apiClient } from '@/lib/api';

const data = await apiClient.get<Todo[]>('/todo');
```
