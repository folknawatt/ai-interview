# AI Interview - Frontend

The front-end client for the AI Interview Platform, engineered with Nuxt 4, TypeScript, and TailwindCSS to deliver a modern, fast, and minimalistic user experience.

## 📋 Key Features

- 🎥 **Video Interview Recording:** Browser-native video recording utilizing the MediaRecorder API.
- 🤖 **AI-Powered Feedback:** Real-time AI evaluation results synchronized seamlessly with the Backend.
- 📊 **HR Dashboard & Analytics:** Comprehensive interfaces for managing roles, configuring questions, and reviewing candidate statistics.
- 🔒 **Secure Authentication:** Robust session management and token-based authentication.

## 🏗️ Technology Stack

- **Framework:** Nuxt 4 (Vue 3)
- **Language:** TypeScript
- **State Management:** Pinia
- **Styling:** TailwindCSS
- **Forms & Validation:** VeeValidate + Zod
- **Data Visualization:** Chart.js + vue-chartjs

## 🚀 Installation & Development

```bash
git clone <repository-url>
cd frontend

npm install
cp .env.example .env # Ensure API_BASE_URL aligns with your Backend environment

npm run dev # Launch development server (http://localhost:3000)
```

## 📁 Project Structure Overview

- `components/` - Vue Components partitioned by domain (e.g., charts, common, interview, layout).
- `composables/` - Reusable Vue Composition API hooks (e.g., `useApi`, `useInterview`).
- `pages/` - Application views adhering to Nuxt's file-based routing.
- `services/` - Dedicated API integration modules per feature domain.
- `store/` - Pinia state stores governing application-wide data.

## 📝 Code Standards & Tooling

- **Strict TypeScript:** Strongly typed implementations mandated across the codebase.
- **Composition API:** Consistent use of `<script setup>` syntax.
- **Linting & Formatting:** Enforced via `npm run lint` and `npm run format`.

> **Troubleshooting Note:** If port 3000 is occupied, you can launch the application on an alternate port using: `PORT=3001 npm run dev`
