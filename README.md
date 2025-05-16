🌐 Common Local URLs

🖼️ Frontend UI
-> React / Vue / Next.js (Vite, Webpack, etc.):
    http://localhost:3000
    http://localhost:5173 (if using Vite)
-> Port is defined in your docker-compose.yml under ports: of the frontend service.

⚙️ Backend API (Django)
-> Django (interactive Swagger UI):
    http://localhost:8000/swagger      ← Swagger UI
    http://localhost:8000/redoc     ← ReDoc alternative
    http://localhost:8000           ← Raw API root

-> Django (admin panel):
    http://localhost:8000/admin


🗄️ Database Admin (if you're running one via Docker)
-> pgAdmin (PostgreSQL):
    http://localhost:5050



# Frontend:
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


...

1. Add ".env.local" file and add following line in the file: "VITE_API_URL=https://31bb-39-51-104-189.ngrok-free.app/api/"
2. Install node on your system if not installed.
3. git clone the repository
4. run "npm i" to install all modules.
5. run "npm run dev" command to start the project.