'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import { CheckCircle, Zap, Shield, ArrowRight, Sparkles } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Auto-redirect if already authenticated
    if (api.isAuthenticated()) {
      router.push('/today');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">TaskFlow</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
              Sign in
            </Link>
            <Link href="/register" className="btn-primary">
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="px-6 pt-16 pb-24">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-8">
              <Sparkles className="w-4 h-4" />
              AI-Powered Task Management
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 tracking-tight">
              Organize your life,
              <span className="block bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                achieve your goals
              </span>
            </h1>

            <p className="mt-8 text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              TaskFlow helps you stay organized with intelligent task management,
              AI assistance, and beautiful design. Get more done with less stress.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/register"
                className="group inline-flex items-center gap-2 bg-gradient-to-r from-primary-600 to-purple-600 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30 transition-all hover:-translate-y-0.5"
              >
                Start for Free
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className="inline-flex items-center gap-2 bg-white text-gray-700 px-8 py-4 rounded-xl text-lg font-semibold border border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-all"
              >
                Sign in to your account
              </Link>
            </div>
          </div>

          {/* Features */}
          <div className="mt-32 grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-lg hover:border-primary-100 transition-all">
              <div className="w-14 h-14 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl flex items-center justify-center mb-6">
                <CheckCircle className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Smart Task Management</h3>
              <p className="text-gray-600 leading-relaxed">
                Organize tasks by priority, due date, and status. Stay on top of your work with intuitive filters and views.
              </p>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-lg hover:border-primary-100 transition-all">
              <div className="w-14 h-14 bg-gradient-to-br from-primary-400 to-purple-500 rounded-xl flex items-center justify-center mb-6">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI-Powered Assistant</h3>
              <p className="text-gray-600 leading-relaxed">
                Chat with our AI to create tasks, get suggestions, and manage your workflow with natural language.
              </p>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-lg hover:border-primary-100 transition-all">
              <div className="w-14 h-14 bg-gradient-to-br from-orange-400 to-rose-500 rounded-xl flex items-center justify-center mb-6">
                <Shield className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Secure & Private</h3>
              <p className="text-gray-600 leading-relaxed">
                Your data is encrypted and secure. We never share your information with third parties.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-6 py-8 border-t border-gray-100">
        <div className="max-w-7xl mx-auto text-center text-gray-500 text-sm">
          <p>&copy; 2024 TaskFlow. Built with Next.js and FastAPI.</p>
        </div>
      </footer>
    </div>
  );
}
