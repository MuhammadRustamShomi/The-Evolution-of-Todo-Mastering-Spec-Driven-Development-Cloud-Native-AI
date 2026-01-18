'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/header';
import { TaskList } from '@/components/task/task-list';
import { TaskForm } from '@/components/task/task-form';
import type { Task, TaskStatus } from '@/types';

export default function AllTasksPage() {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | undefined>();
  const [statusFilter, setStatusFilter] = useState<TaskStatus | undefined>();

  // Listen for new-task keyboard shortcut
  useEffect(() => {
    const handleNewTask = () => setShowTaskForm(true);
    window.addEventListener('new-task', handleNewTask);
    return () => window.removeEventListener('new-task', handleNewTask);
  }, []);

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCloseForm = () => {
    setShowTaskForm(false);
    setEditingTask(undefined);
  };

  return (
    <div className="flex flex-col h-screen">
      <Header
        title="All Tasks"
        onNewTask={() => setShowTaskForm(true)}
      />

      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center gap-4 mb-6">
            <span className="text-gray-500">Filter:</span>
            <div className="flex gap-2">
              <button
                onClick={() => setStatusFilter(undefined)}
                className={`px-3 py-1 rounded-full text-sm ${
                  !statusFilter
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setStatusFilter('pending')}
                className={`px-3 py-1 rounded-full text-sm ${
                  statusFilter === 'pending'
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                Pending
              </button>
              <button
                onClick={() => setStatusFilter('in_progress')}
                className={`px-3 py-1 rounded-full text-sm ${
                  statusFilter === 'in_progress'
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                In Progress
              </button>
              <button
                onClick={() => setStatusFilter('done')}
                className={`px-3 py-1 rounded-full text-sm ${
                  statusFilter === 'done'
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                Done
              </button>
            </div>
          </div>

          <TaskList
            status={statusFilter}
            onEditTask={handleEditTask}
          />
        </div>
      </div>

      {showTaskForm && (
        <TaskForm task={editingTask} onClose={handleCloseForm} />
      )}
    </div>
  );
}
