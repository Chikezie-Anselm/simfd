"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post('/register', { email, password, display_name: displayName });
      router.push('/');
      window.location.reload();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Create account</h2>
      {error && <div className="mb-3 text-red-600">{error}</div>}
      <form onSubmit={submit}>
        <div className="mb-3">
          <label htmlFor="email" className="block text-sm font-medium">Email address</label>
          <input id="email" name="email" placeholder="you@example.com" className="w-full border rounded px-3 py-2" value={email} onChange={e => setEmail(e.target.value)} required />
          <p className="text-xs text-gray-500 mt-1">We'll use your email to sign in. This acts as your username.</p>
        </div>
        <div className="mb-3">
          <label htmlFor="display_name" className="block text-sm font-medium">Display name (optional)</label>
          <input id="display_name" name="display_name" placeholder="How your name will appear (e.g. 'Jane')" className="w-full border rounded px-3 py-2" value={displayName} onChange={e => setDisplayName(e.target.value)} />
          <p className="text-xs text-gray-500 mt-1">This will be shown on the site instead of your email.</p>
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="block text-sm font-medium">Password</label>
          <input id="password" name="password" type="password" placeholder="Choose a secure password" className="w-full border rounded px-3 py-2" value={password} onChange={e => setPassword(e.target.value)} required />
          <p className="text-xs text-gray-500 mt-1">Use a strong password (at least 8 characters recommended).</p>
        </div>
        <div className="flex items-center justify-between">
          <button type="submit" className="btn-primary" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
        </div>
      </form>
    </div>
  );
}
