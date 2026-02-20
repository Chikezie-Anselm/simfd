"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post('/login', { email, password });
      // On success, navigate home (the Navbar will refresh current user on mount)
      router.push('/');
      window.location.reload();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Sign in failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Sign in</h2>
      {error && <div className="mb-3 text-red-600">{error}</div>}
      <form onSubmit={submit}>
        <div className="mb-3">
          <label htmlFor="email" className="block text-sm font-medium">Email address</label>
          <input id="email" name="email" placeholder="you@example.com" className="w-full border rounded px-3 py-2" value={email} onChange={e => setEmail(e.target.value)} required />
          <p className="text-xs text-gray-500 mt-1">Sign in with the email you registered with.</p>
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="block text-sm font-medium">Password</label>
          <input id="password" name="password" type="password" placeholder="Your password" className="w-full border rounded px-3 py-2" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <div className="flex items-center justify-between">
          <button type="submit" className="btn-primary" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
        </div>
      </form>
    </div>
  );
}
