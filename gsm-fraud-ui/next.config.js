/** @type {import('next').NextConfig} */
const nextConfig = {
  //experimental: {
    //appDir: true,
  //},
  async rewrites() {
    return [
      {
        source: '/api/upload',
        destination: 'http://localhost:5000/upload',
      },
    ];
  },
};

module.exports = nextConfig;