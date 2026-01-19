import Link from 'next/link';
import { RegisterForm } from '@/components/auth/register-form';
import { CheckCircle, Star, TrendingUp, Clock } from 'lucide-react';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-600 via-primary-700 to-primary-800 p-12 flex-col justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-12 h-12 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
            <CheckCircle className="w-7 h-7 text-white" />
          </div>
          <span className="text-2xl font-bold text-white">TaskFlow</span>
        </Link>

        <div className="space-y-6">
          <h2 className="text-4xl font-bold text-white leading-tight">
            Start your journey<br />
            to productivity
          </h2>
          <p className="text-purple-100 text-lg max-w-md">
            Join thousands of users who have transformed how they work with TaskFlow.
          </p>

          {/* Benefits */}
          <div className="space-y-4 pt-4">
            <div className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center">
                <Star className="w-5 h-5" />
              </div>
              <span>Free forever for personal use</span>
            </div>
            <div className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5" />
              </div>
              <span>Track progress with analytics</span>
            </div>
            <div className="flex items-center gap-3 text-white">
              <div className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center">
                <Clock className="w-5 h-5" />
              </div>
              <span>Set up in under 2 minutes</span>
            </div>
          </div>
        </div>

        <p className="text-purple-200 text-sm">
          No credit card required. Cancel anytime.
        </p>
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
            <h1 className="text-3xl font-bold text-gray-900">Create account</h1>
            <p className="mt-2 text-gray-600">
              Get started with your free account today
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <RegisterForm />
          </div>

          <p className="text-center text-sm text-gray-500">
            By signing up, you agree to our{' '}
            <a href="#" className="text-primary-600 hover:underline">Terms of Service</a>
            {' '}and{' '}
            <a href="#" className="text-primary-600 hover:underline">Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  );
}
