'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Plus, Search } from 'lucide-react';

interface HeaderProps {
  title: string;
  onNewTask?: () => void;
}

export function Header({ title, onNewTask }: HeaderProps) {
  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: () => api.getMe(),
  });

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search tasks... (Press /)"
              className="input pl-9 w-64"
            />
          </div>

          {onNewTask && (
            <button onClick={onNewTask} className="btn-primary">
              <Plus className="w-4 h-4 mr-2" />
              New Task
            </button>
          )}

          {user && (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                <span className="text-sm font-medium text-primary-700">
                  {user.name?.[0] || user.email[0].toUpperCase()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
