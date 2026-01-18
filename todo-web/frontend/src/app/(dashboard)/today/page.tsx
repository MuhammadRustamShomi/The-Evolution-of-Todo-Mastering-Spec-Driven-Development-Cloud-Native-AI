'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/header';
import { TaskList } from '@/components/task/task-list';
import { TaskForm } from '@/components/task/task-form';
import type { Task } from '@/types';

export default function TodayPage() {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | undefined>();

  // Get today's date in YYYY-MM-DD format
  const today = new Date().toISOString().split('T')[0];

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
        title="Today"
        onNewTask={() => setShowTaskForm(true)}
      />

      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-3xl mx-auto">
          <p className="text-gray-500 mb-6">
            Tasks due today and overdue tasks
          </p>
          <TaskList
            dueBefore={today}
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
