"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { api, authLogout } from '@/lib/api';

type User = { id?: number; email?: string; display_name?: string };

export default function Navbar({ initialUser }: { initialUser?: User | null } = {}): JSX.Element {
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(initialUser ?? null);

  useEffect(() => {
    // If we already have an initial user from server, avoid refetch to prevent flicker.
    if (initialUser) return;
    let mounted = true;
    api.get('/api/me')
      .then(res => { if (!mounted) return; setCurrentUser(res.data?.user ?? null); })
      .catch(() => { if (!mounted) return; setCurrentUser(null); });
    return () => { mounted = false; };
  }, [initialUser]);

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Upload', href: '/upload' },
    { name: 'Results', href: '/results' },
    { name: 'About', href: '/about' },
    { name: 'Saved Uploads', href: '/uploads' },
  ];

  return (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0">
              <h1 className="text-xl font-bold text-primary-600">GSM Fraud Detection</h1>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navigation.map(item => (
              <Link key={item.name} href={item.href} className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${pathname === item.href ? 'text-primary-600 bg-primary-50' : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50'}`}>
                {item.name}
              </Link>
            ))}

            {currentUser ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">{currentUser.display_name || currentUser.email}</span>
                <button onClick={() => { authLogout(); setCurrentUser(null); window.location.href = '/'; }} className="text-sm text-gray-600 hover:text-primary-600">Sign out</button>
              </div>
            ) : (
              <>
                <Link href="/login" className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-primary-600 hover:bg-gray-50">Sign in</Link>
                <Link href="/register" className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-primary-600 hover:bg-gray-50">Register</Link>
              </>
            )}
          </div>

          <div className="md:hidden flex items-center">
            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="text-gray-600 hover:text-primary-600 focus:outline-none focus:text-primary-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'} />
              </svg>
            </button>
          </div>
        </div>

        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigation.map(item => (
                <Link key={item.name} href={item.href} className={`block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${pathname === item.href ? 'text-primary-600 bg-primary-50' : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50'}`} onClick={() => setIsMenuOpen(false)}>
                  {item.name}
                </Link>
              ))}
              <div className="mt-2 border-t pt-2">
                {currentUser ? (
                  <div className="flex items-center justify-between">
                    <span className="text-sm">{currentUser.display_name || currentUser.email}</span>
                    <button onClick={() => { authLogout(); setCurrentUser(null); window.location.href = '/'; }} className="text-sm text-gray-600">Sign out</button>
                  </div>
                ) : (
                  <div className="space-y-1">
                    <Link href="/login" className="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-primary-600">Sign in</Link>
                    <Link href="/register" className="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-primary-600">Register</Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}