import Navbar from './Navbar';

// Server component that fetches the current user from the Flask backend
// and passes it to the client Navbar to avoid flash of unauthenticated content.
export default async function ServerNavbar() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
  try {
    const res = await fetch(`${apiUrl}/api/me`, { cache: 'no-store', credentials: 'include' });
    if (!res.ok) {
      return <Navbar />; // render client without initial user
    }
    const data = await res.json();
    const initialUser = data?.user ?? null;
    // Pass initialUser as prop to client Navbar
    // @ts-ignore - this component is a server component passing props to a client component
    return <Navbar initialUser={initialUser} />;
  } catch (e) {
    return <Navbar />;
  }
}
