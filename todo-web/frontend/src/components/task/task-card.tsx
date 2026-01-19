'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { cn, formatDate, getPriorityColor, isOverdue } from '@/lib/utils';
import type { Task } from '@/types';
import { Calendar, Check, Circle, Trash2, Flag, MoreHorizontal } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  isSelected?: boolean;
  onSelect?: () => void;
  onEdit?: () => void;
}

const priorityConfig = {
  high: { color: 'text-red-500', bg: 'bg-red-50', border: 'border-red-200' },
  medium: { color: 'text-orange-500', bg: 'bg-orange-50', border: 'border-orange-200' },
  low: { color: 'text-blue-500', bg: 'bg-blue-50', border: 'border-blue-200' },
};

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
  const priority = priorityConfig[task.priority as keyof typeof priorityConfig] || priorityConfig.medium;

  return (
    <div
      className={cn(
        'group relative bg-white rounded-2xl border transition-all duration-200 hover:shadow-lg hover:border-primary-200 hover:-translate-y-0.5',
        isSelected ? 'ring-2 ring-primary-500 border-primary-300' : 'border-gray-100',
        isDone && 'opacity-60 bg-gray-50'
      )}
      onClick={onSelect}
      onDoubleClick={onEdit}
    >
      {/* Priority indicator */}
      <div className={cn('absolute left-0 top-0 bottom-0 w-1 rounded-l-2xl', priority.bg.replace('bg-', 'bg-').replace('50', '400'))} />

      <div className="p-5 pl-6">
        <div className="flex items-start gap-4">
          {/* Checkbox */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleMutation.mutate();
            }}
            className={cn(
              'mt-0.5 flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all',
              isDone
                ? 'bg-gradient-to-br from-green-400 to-emerald-500 border-green-400 text-white'
                : 'border-gray-300 hover:border-primary-500 hover:bg-primary-50'
            )}
          >
            {isDone && <Check className="w-4 h-4" />}
          </button>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h3
              className={cn(
                'text-base font-semibold text-gray-900',
                isDone && 'line-through text-gray-400'
              )}
            >
              {task.title}
            </h3>

            {task.description && (
              <p className="mt-1.5 text-sm text-gray-500 line-clamp-2 leading-relaxed">
                {task.description}
              </p>
            )}

            {/* Meta info */}
            <div className="mt-3 flex flex-wrap items-center gap-2">
              {task.due_date && (
                <span
                  className={cn(
                    'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium',
                    overdue
                      ? 'bg-red-50 text-red-600 border border-red-200'
                      : 'bg-gray-100 text-gray-600'
                  )}
                >
                  <Calendar className="w-3.5 h-3.5" />
                  {formatDate(task.due_date)}
                </span>
              )}

              <span
                className={cn(
                  'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium border',
                  priority.bg,
                  priority.color,
                  priority.border
                )}
              >
                <Flag className="w-3.5 h-3.5" />
                {task.priority}
              </span>

              {task.tags.length > 0 && (
                <div className="flex gap-1.5">
                  {task.tags.slice(0, 2).map((tag) => (
                    <span
                      key={tag}
                      className="inline-flex px-2.5 py-1 text-xs font-medium bg-primary-50 text-primary-700 rounded-lg"
                    >
                      #{tag}
                    </span>
                  ))}
                  {task.tags.length > 2 && (
                    <span className="inline-flex px-2 py-1 text-xs text-gray-400">
                      +{task.tags.length - 2}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (confirm('Delete this task?')) {
                  deleteMutation.mutate();
                }
              }}
              className="p-2 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            >
              <Trash2 className="w-4 h-4" />
            </button>
            <button className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
              <MoreHorizontal className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
