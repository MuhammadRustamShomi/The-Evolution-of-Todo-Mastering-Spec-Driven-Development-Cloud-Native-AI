import Link from 'next/link';
import { LoginForm } from '@/components/auth/login-form';
import { CheckCircle } from 'lucide-react';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-700 to-purple-800 p-12 flex-col justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-12 h-12 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
            <CheckCircle className="w-7 h-7 text-white" />
          </div>
          <span className="text-2xl font-bold text-white">TaskFlow</span>
        </Link>

        <div className="space-y-6">
          <h2 className="text-4xl font-bold text-white leading-tight">
            Welcome back!<br />
            Ready to be productive?
          </h2>
          <p className="text-primary-100 text-lg max-w-md">
            Sign in to access your tasks, track your progress, and achieve your goals.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex -space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-400 to-rose-500 border-2 border-primary-700"></div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500 border-2 border-primary-700"></div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 border-2 border-primary-700"></div>
          </div>
          <p className="text-primary-100 text-sm">
            Join 10,000+ users managing their tasks
          </p>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md space-y-8">
          <div className="lg:hidden flex justify-center mb-8">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">TaskFlow</span>
            </Link>
          </div>

          <div className="text-center lg:text-left">
            <h1 className="text-3xl font-bold text-gray-900">Sign in</h1>
            <p className="mt-2 text-gray-600">
              Enter your credentials to access your account
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <LoginForm />
          </div>

          <p className="text-center text-sm text-gray-500">
            By signing in, you agree to our{' '}
            <a href="#" className="text-primary-600 hover:underline">Terms of Service</a>
            {' '}and{' '}
            <a href="#" className="text-primary-600 hover:underline">Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  );
}
