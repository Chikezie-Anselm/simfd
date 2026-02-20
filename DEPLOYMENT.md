Deployment with Docker Compose

This repository contains both the Flask backend and Next.js frontend. The following instructions show how to deploy both using Docker and docker-compose locally or on a server.

Prerequisites
- Docker and docker-compose installed on the host.

Quick start (development-like with live code mounts)
1. From the repository root run:

   docker-compose up --build

2. Services:
   - Backend: http://localhost:5000
   - Frontend: http://localhost:3000

Production notes
- The backend image uses gunicorn to serve the Flask app. Set a secure SECRET_KEY and configure CORS origins as needed via environment variables.
- The frontend builds a production Next.js app and serves it using `npm run start`. For production, consider using a more robust static hosting or Vercel for serverless Next.js.
- If you need a single host/port, add an Nginx reverse proxy and route `/api` to the backend and other paths to the frontend.

Environment
- You can pass environment variables to the docker-compose file or use a `.env` file to set values like `SECRET_KEY` and `NEXT_PUBLIC_API_URL`.

Security
- Do not store secrets in the compose or Dockerfiles for production. Use environment or secret stores.

*** End of file
