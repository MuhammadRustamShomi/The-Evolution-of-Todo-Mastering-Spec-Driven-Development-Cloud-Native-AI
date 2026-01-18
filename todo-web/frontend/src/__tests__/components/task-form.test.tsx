import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TaskForm } from '@/components/task/task-form';

// Mock the API
vi.mock('@/lib/api', () => ({
  api: {
    createTask: vi.fn(),
    updateTask: vi.fn(),
  },
}));

import { api } from '@/lib/api';

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

describe('TaskForm', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders create form when no task provided', () => {
    render(<TaskForm onClose={mockOnClose} />, { wrapper: createWrapper() });

    expect(screen.getByText('New Task')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('What needs to be done?')).toBeInTheDocument();
  });

  it('renders edit form when task provided', () => {
    const task = {
      id: '1',
      user_id: 'user-1',
      title: 'Existing Task',
      description: 'Description',
      status: 'pending' as const,
      priority: 'high' as const,
      due_date: null,
      tags: ['work'],
      created_at: '2025-01-01T00:00:00Z',
      updated_at: '2025-01-01T00:00:00Z',
      completed_at: null,
    };

    render(<TaskForm task={task} onClose={mockOnClose} />, {
      wrapper: createWrapper(),
    });

    expect(screen.getByText('Edit Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing Task')).toBeInTheDocument();
  });

  it('closes on cancel button click', async () => {
    render(<TaskForm onClose={mockOnClose} />, { wrapper: createWrapper() });

    fireEvent.click(screen.getByText('Cancel'));

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('closes on escape key', async () => {
    render(<TaskForm onClose={mockOnClose} />, { wrapper: createWrapper() });

    fireEvent.keyDown(window, { key: 'Escape' });

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('submits new task', async () => {
    const user = userEvent.setup();
    (api.createTask as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: '1',
      title: 'New Task',
    });

    render(<TaskForm onClose={mockOnClose} />, { wrapper: createWrapper() });

    await user.type(
      screen.getByPlaceholderText('What needs to be done?'),
      'New Task'
    );
    await user.click(screen.getByText('Create Task'));

    await waitFor(() => {
      expect(api.createTask).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'New Task',
        })
      );
    });
  });

  it('shows validation error for empty title', async () => {
    const user = userEvent.setup();

    render(<TaskForm onClose={mockOnClose} />, { wrapper: createWrapper() });

    await user.click(screen.getByText('Create Task'));

    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
    });
  });
});
