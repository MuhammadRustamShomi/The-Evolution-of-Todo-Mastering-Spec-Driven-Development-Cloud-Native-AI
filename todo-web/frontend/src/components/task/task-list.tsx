'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { TaskCard } from './task-card';
import { TaskListSkeleton } from './task-list-skeleton';
import type { Task, TaskStatus } from '@/types';

interface TaskListProps {
  status?: TaskStatus;
  dueBefore?: string;
  dueAfter?: string;
  onEditTask?: (task: Task) => void;
}

export function TaskList({
  status,
  dueBefore,
  dueAfter,
  onEditTask,
}: TaskListProps) {
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const queryClient = useQueryClient();

  const markDoneMutation = useMutation({
    mutationFn: (taskId: string) => api.markTaskDone(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const markPendingMutation = useMutation({
    mutationFn: (taskId: string) => api.markTaskPending(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', { status, dueBefore, dueAfter }],
    queryFn: () =>
      api.getTasks({
        status,
        due_before: dueBefore,
        due_after: dueAfter,
      }),
  });

  // Keyboard navigation
  useEffect(() => {
    const handleNavNext = () => {
      if (tasks) {
        setSelectedIndex((prev) => Math.min(prev + 1, tasks.length - 1));
      }
    };

    const handleNavPrev = () => {
      setSelectedIndex((prev) => Math.max(prev - 1, 0));
    };

    const handleToggle = () => {
      if (tasks && selectedIndex >= 0 && selectedIndex < tasks.length) {
        const task = tasks[selectedIndex];
        if (task.status === 'done') {
          markPendingMutation.mutate(task.id);
        } else {
          markDoneMutation.mutate(task.id);
        }
      }
    };

    window.addEventListener('nav-next', handleNavNext);
    window.addEventListener('nav-prev', handleNavPrev);
    window.addEventListener('toggle-task', handleToggle);

    return () => {
      window.removeEventListener('nav-next', handleNavNext);
      window.removeEventListener('nav-prev', handleNavPrev);
      window.removeEventListener('toggle-task', handleToggle);
    };
  }, [tasks, selectedIndex]);

  if (isLoading) {
    return <TaskListSkeleton />;
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 text-lg">No tasks found</div>
        <p className="text-gray-500 text-sm mt-2">
          Press <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">n</kbd>{' '}
          to create a new task
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task, index) => (
        <TaskCard
          key={task.id}
          task={task}
          isSelected={index === selectedIndex}
          onSelect={() => setSelectedIndex(index)}
          onEdit={() => onEditTask?.(task)}
        />
      ))}
    </div>
  );
}
