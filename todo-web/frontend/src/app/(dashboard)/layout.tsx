'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Sidebar } from '@/components/layout/sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!api.isAuthenticated()) {
      router.push('/login');
    } else {
      setIsLoading(false);
    }
  }, [router]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Only handle if not in an input/textarea
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      ) {
        return;
      }

      switch (e.key) {
        case 'n':
          // Trigger new task (handled by page)
          window.dispatchEvent(new CustomEvent('new-task'));
          break;
        case '/':
          e.preventDefault();
          // Focus search
          const searchInput = document.querySelector(
            'input[placeholder*="Search"]'
          ) as HTMLInputElement;
          searchInput?.focus();
          break;
        case 'j':
          // Next task
          window.dispatchEvent(new CustomEvent('nav-next'));
          break;
        case 'k':
          // Previous task
          window.dispatchEvent(new CustomEvent('nav-prev'));
          break;
        case 'Enter':
          // Toggle selected task
          window.dispatchEvent(new CustomEvent('toggle-task'));
          break;
        case '?':
          // Show help
          window.dispatchEvent(new CustomEvent('show-help'));
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  );
}
