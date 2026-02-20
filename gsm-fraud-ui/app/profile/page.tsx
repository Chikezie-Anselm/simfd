"use client";

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function ProfilePage() {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    api.get('/api/me')
      .then(res => { if (!mounted) return; setUser(res.data?.user ?? null); })
      .catch(() => { if (!mounted) return; setUser(null); })
      .finally(() => { if (!mounted) return; setLoading(false); });
    return () => { mounted = false; };
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;
  if (!user) return <div className="p-6">Not signed in. <a className="text-primary-600" href="/login">Sign in</a></div>;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Profile</h2>
      <div className="bg-white border rounded p-4">
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Display name:</strong> {user.display_name || '(not set)'}</p>
      </div>
      <div className="mt-4">
        <a className="text-primary-600" href="/api/uploads">Saved uploads (server)</a>
      </div>
    </div>
  );
}
