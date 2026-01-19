'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  Calendar,
  CalendarDays,
  CheckSquare,
  LogOut,
  MessageSquare,
  CheckCircle,
  Plus,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useRouter } from 'next/navigation';

const navigation = [
  { name: 'Today', href: '/today', icon: Calendar, color: 'text-orange-500' },
  { name: 'Upcoming', href: '/upcoming', icon: CalendarDays, color: 'text-purple-500' },
  { name: 'All Tasks', href: '/tasks', icon: CheckSquare, color: 'text-blue-500' },
  { name: 'AI Chat', href: '/chat', icon: MessageSquare, color: 'text-green-500' },
];

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await api.logout();
    router.push('/login');
  };

  return (
    <aside className="w-72 bg-gradient-to-b from-gray-50 to-white border-r border-gray-200 min-h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-100">
        <Link href="/today" className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
            <CheckCircle className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
            TaskFlow
          </span>
        </Link>
      </div>

      {/* Quick Add Button */}
      <div className="px-4 py-4">
        <button className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-primary-600 to-purple-600 text-white px-4 py-3 rounded-xl font-medium shadow-lg shadow-primary-500/20 hover:shadow-xl hover:shadow-primary-500/30 transition-all hover:-translate-y-0.5">
          <Plus className="w-5 h-5" />
          Add New Task
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-1">
        <p className="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          Menu
        </p>
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all',
                isActive
                  ? 'bg-white text-gray-900 shadow-sm border border-gray-100'
                  : 'text-gray-600 hover:bg-white hover:shadow-sm hover:text-gray-900'
              )}
            >
              <item.icon className={cn('w-5 h-5', isActive ? item.color : 'text-gray-400')} />
              {item.name}
              {isActive && (
                <div className="ml-auto w-2 h-2 rounded-full bg-gradient-to-r from-primary-500 to-purple-500"></div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* User section */}
      <div className="p-4 border-t border-gray-100">
        <div className="bg-gray-50 rounded-xl p-3">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
              U
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">User</p>
              <p className="text-xs text-gray-500 truncate">Free Plan</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center justify-center gap-2 w-full px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Sign out
          </button>
        </div>
      </div>
    </aside>
  );
}
