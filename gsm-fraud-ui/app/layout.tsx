import { Inter } from 'next/font/google';
import ServerNavbar from '@/components/ServerNavbar';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'GSM Subscription Fraud Detection System',
  description: 'Advanced AI-powered fraud detection for GSM subscriber registrations',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      </head>
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          {/* Server-side navbar fetches /api/me and passes initialUser to client Navbar */}
          <ServerNavbar />
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="bg-white border-t border-gray-200 mt-16">
            <div className="container mx-auto px-4 py-6 text-center text-gray-600">
              <p>&copy; 2025 GSM Subscription Fraud Detection System. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}