'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { cn, formatDate, getPriorityColor, isOverdue } from '@/lib/utils';
import type { Task } from '@/types';
import { Calendar, Check, Circle, Trash2 } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  isSelected?: boolean;
  onSelect?: () => void;
  onEdit?: () => void;
}

export function TaskCard({ task, isSelected, onSelect, onEdit }: TaskCardProps) {
  const queryClient = useQueryClient();

  const toggleMutation = useMutation({
    mutationFn: () =>
      task.status === 'done'
        ? api.markTaskPending(task.id)
        : api.markTaskDone(task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => api.deleteTask(task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const isDone = task.status === 'done';
  const overdue = isOverdue(task.due_date) && !isDone;

  return (
    <div
      className={cn(
        'card group cursor-pointer transition-all hover:shadow-md',
        isSelected && 'ring-2 ring-primary-500',
        isDone && 'opacity-60'
      )}
      onClick={onSelect}
      onDoubleClick={onEdit}
    >
      <div className="flex items-start gap-3">
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleMutation.mutate();
          }}
          className={cn(
            'mt-0.5 flex-shrink-0 rounded-full transition-colors',
            isDone
              ? 'text-green-600 hover:text-green-700'
              : 'text-gray-400 hover:text-primary-600'
          )}
        >
          {isDone ? (
            <Check className="w-5 h-5" />
          ) : (
            <Circle className="w-5 h-5" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3
            className={cn(
              'text-sm font-medium text-gray-900',
              isDone && 'line-through text-gray-500'
            )}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="mt-1 text-sm text-gray-500 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="mt-2 flex items-center gap-3">
            {task.due_date && (
              <span
                className={cn(
                  'inline-flex items-center gap-1 text-xs',
                  overdue ? 'text-red-600' : 'text-gray-500'
                )}
              >
                <Calendar className="w-3 h-3" />
                {formatDate(task.due_date)}
              </span>
            )}

            <span
              className={cn(
                'inline-flex px-2 py-0.5 text-xs font-medium rounded-full',
                getPriorityColor(task.priority)
              )}
            >
              {task.priority}
            </span>

            {task.tags.length > 0 && (
              <div className="flex gap-1">
                {task.tags.slice(0, 2).map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
                {task.tags.length > 2 && (
                  <span className="text-xs text-gray-400">
                    +{task.tags.length - 2}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            if (confirm('Delete this task?')) {
              deleteMutation.mutate();
            }
          }}
          className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-600 transition-all"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
