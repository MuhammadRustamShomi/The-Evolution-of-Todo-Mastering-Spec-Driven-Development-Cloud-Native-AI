import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TaskList } from '@/components/task/task-list';

// Mock the API
vi.mock('@/lib/api', () => ({
  api: {
    getTasks: vi.fn(),
    markTaskDone: vi.fn(),
    markTaskPending: vi.fn(),
  },
}));

import { api } from '@/lib/api';

const mockTasks = [
  {
    id: '1',
    user_id: 'user-1',
    title: 'Test Task 1',
    description: 'Description 1',
    status: 'pending' as const,
    priority: 'medium' as const,
    due_date: null,
    tags: [],
    created_at: '2025-01-01T00:00:00Z',
    updated_at: '2025-01-01T00:00:00Z',
    completed_at: null,
  },
  {
    id: '2',
    user_id: 'user-1',
    title: 'Test Task 2',
    description: null,
    status: 'done' as const,
    priority: 'high' as const,
    due_date: '2025-01-15',
    tags: ['work'],
    created_at: '2025-01-01T00:00:00Z',
    updated_at: '2025-01-01T00:00:00Z',
    completed_at: '2025-01-10T00:00:00Z',
  },
];

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('TaskList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading skeleton initially', () => {
    (api.getTasks as ReturnType<typeof vi.fn>).mockReturnValue(
      new Promise(() => {})
    );

    render(<TaskList />, { wrapper: createWrapper() });

    expect(screen.getByRole('generic')).toBeInTheDocument();
  });

  it('renders tasks when loaded', async () => {
    (api.getTasks as ReturnType<typeof vi.fn>).mockResolvedValue(mockTasks);

    render(<TaskList />, { wrapper: createWrapper() });

    expect(await screen.findByText('Test Task 1')).toBeInTheDocument();
    expect(await screen.findByText('Test Task 2')).toBeInTheDocument();
  });

  it('shows empty state when no tasks', async () => {
    (api.getTasks as ReturnType<typeof vi.fn>).mockResolvedValue([]);

    render(<TaskList />, { wrapper: createWrapper() });

    expect(await screen.findByText('No tasks found')).toBeInTheDocument();
  });

  it('passes filters to API', async () => {
    (api.getTasks as ReturnType<typeof vi.fn>).mockResolvedValue([]);

    render(
      <TaskList status="pending" dueBefore="2025-01-15" />,
      { wrapper: createWrapper() }
    );

    await screen.findByText('No tasks found');

    expect(api.getTasks).toHaveBeenCalledWith({
      status: 'pending',
      due_before: '2025-01-15',
      due_after: undefined,
    });
  });
});
