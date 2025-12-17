# AI Interview - Frontend

> Modern AI-powered interview platform built with Nuxt 3, TypeScript, and TailwindCSS

## 📋 Overview

The AI Interview frontend is a sophisticated web application that enables HR professionals to conduct AI-assisted video interviews. Candidates answer pre-defined questions, and their responses are analyzed in real-time using AI to provide comprehensive feedback and scoring.

### Key Features

- 🎥 **Video Interview Recording** - Browser-based video recording with MediaRecorder API
- 🤖 **AI-Powered Evaluation** - Real-time transcription and evaluation of responses
- 📊 **Comprehensive Analytics** - Detailed reports with charts and insights
- 👔 **HR Dashboard** - Manage roles, questions, and review candidates
- 🎨 **Modern UI** - Clean, minimal design with TailwindCSS
- 🔒 **Secure Authentication** - Token-based auth with refresh mechanism
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🏗️ Tech Stack

| Category             | Technology                                                                        |
| -------------------- | --------------------------------------------------------------------------------- |
| **Framework**        | [Nuxt 3](https://nuxt.com/) (Vue 3)                                               |
| **Language**         | [TypeScript](https://www.typescriptlang.org/)                                     |
| **State Management** | [Pinia](https://pinia.vuejs.org/)                                                 |
| **Styling**          | [TailwindCSS](https://tailwindcss.com/)                                           |
| **HTTP Client**      | Nuxt's built-in `$fetch`                                                          |
| **Charts**           | [Chart.js](https://www.chartjs.org/) + vue-chartjs                                |
| **Forms**            | [@vee-validate/zod](https://vee-validate.logaretm.com/) + [Zod](https://zod.dev/) |
| **Icons**            | [@heroicons/vue](https://heroicons.com/)                                          |
| **Testing**          | [Vitest](https://vitest.dev/) + [@vue/test-utils](https://test-utils.vuejs.org/)  |
| **Linting**          | [ESLint](https://eslint.org/) + [Prettier](https://prettier.io/)                  |

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running (default: `http://localhost:8000`)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Update .env with your API URL
# API_BASE_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# Server runs on http://localhost:3000
```

### Build for Production

```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── assets/              # Global styles and static assets
├── components/
│   ├── charts/          # Chart components (Score visualizations)
│   ├── common/          # Reusable base components
│   ├── interview/       # Interview-specific components
│   └── layout/          # Layout components
├── composables/         # Vue composables (reusable logic)
│   ├── useApi.ts        # API client wrapper
│   ├── useInterview.ts  # Interview state & logic
│   ├── useHR.ts         # HR operations
│   └── ...
├── layouts/             # Page layouts
│   ├── default.vue      # Default layout
│   ├── hr.vue           # HR dashboard layout
│   └── candidate.vue    # Interview layout
├── middleware/          # Route middleware
│   ├── auth.ts          # Authentication guard
│   ├── hr.ts            # HR authorization
│   └── guest.ts         # Guest-only routes
├── pages/               # File-based routing
│   ├── index.vue        # Landing page
│   ├── login.vue        # Login page
│   ├── role-selection.vue
│   ├── question.vue
│   ├── record.vue
│   ├── result.vue
│   └── hr/              # HR dashboard pages
│       ├── dashboard.vue
│       ├── roles.vue
│       ├── generate.vue
│       ├── reports.vue
│       └── reports/[sessionId].vue
├── plugins/             # Nuxt plugins
│   └── axios.ts         # Axios configuration
├── public/              # Static files
├── services/            #API service layer
│   ├── auth.ts          # Authentication services
│   ├── interview.ts     # Interview services
│   ├── hr.ts            # HR services
│   └── report.ts        # Report services
├── store/               # Pinia stores
│   ├── auth.ts          # Auth state
│   ├── interview.ts     # Interview state
│   └── hr.ts            # HR state
├── tests/               # Test files
│   └── unit/            # Unit tests
├── types/               # TypeScript type definitions
│   ├── api.ts           # API types
│   ├── candidate.ts     # Candidate types
│   ├── interview.ts     # Interview types
│   ├── question.ts      # Question types
│   ├── report.ts        # Report types
│   └── index.ts         # Central exports
├── utils/               # Utility functions
│   ├── constants.ts     # App constants
│   ├── date.ts          # Date utilities
│   ├── format.ts        # Formatting utilities
│   ├── validation.ts    # Validation helpers
│   └── index.ts         # Central exports
├── .eslintrc.js         # ESLint configuration
├── .prettierrc          # Prettier configuration
├── nuxt.config.ts       # Nuxt configuration
├── tailwind.config.js   # Tailwind configuration
├── tsconfig.json        # TypeScript configuration
└── vitest.config.ts     # Vitest configuration
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
API_BASE_URL=http://localhost:8000  # Backend API URL
```

### Path Aliases

The project uses path aliases for cleaner imports:

```typescript
import { useInterview } from '@/composables/useInterview'
import type { Question } from '@/types'
import { formatScore } from '@/utils'
import BaseButton from '@/components/common/BaseButton.vue'
```

Available aliases:

- `@` or `~` → Project root
- `@components` → `./components`
- `@composables` → `./composables`
- `@services` → `./services`
- `@types` → `./types`
- `@store` → `./store`

## 🧪 Testing

```bash
# Run unit tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

### Test Structure

Tests are organized by feature:

```
tests/
├── unit/
│   ├── components/
│   ├── composables/
│   ├── services/
│   ├── store/
│   └── utils/
└── tsconfig.json
```

## 📝 Code Style

### Linting & Formatting

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code with Prettier
npm run format

# Type check
npm run type-check
```

### Coding Standards

- **TypeScript**: Strict mode enabled, explicit types preferred
- **Components**: Use `<script setup>` composition API
- **Styling**: TailwindCSS utility classes, avoid custom CSS when possible
- **Naming**:
  - Components: PascalCase (`BaseButton.vue`)
  - Composables: camelCase with `use` prefix (`useInterview.ts`)
  - Services: camelCase with Service suffix (`interviewService`)
  - Types: PascalCase (`InterviewSession`)

## 🔄 Development Workflow

### Feature Development

1. Create a new branch from `main`
2. Make your changes following coding standards
3. Write/update tests
4. Run lint and type check
5. Test locally
6. Create pull request

### Component Development

When creating new components:

1. Use TypeScript with proper prop types
2. Add JSDoc comments for complex logic
3. Use composition API (`<script setup>`)
4. Apply TailwindCSS for styling
5. Make components reusable when possible
6. Write unit tests

Example:

```vue
<template>
  <div class="my-component">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  variant?: 'primary' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
})
</script>
```

## 🚦 API Integration

The app uses a service layer pattern for API calls:

```typescript
// In a composable or component
import { interviewService } from '@/services/interview'

const { data, error } = await interviewService.getQuestion(roleId, index)
```

Services are located in `services/` and use the `useApi()` composable for HTTP requests.

## 🎨 UI/UX Guidelines

- **Color Scheme**: Custom `minimal` palette (defined in `tailwind.config.js`)
- **Accessibility**: WCAG 2.1 AA compliant
- **Responsive**: Mobile-first design
- **Loading States**: Always show loading indicators
- **Error Handling**: User-friendly error messages
- **Animations**: Subtle transitions (max 300ms)

## 📚 Additional Resources

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Documentation](https://vuejs.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Vitest Documentation](https://vitest.dev/)

## 🤝 Contributing

1. Follow the coding standards
2. Write tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PR
5. Keep PRs focused and atomic

## 📄 License

[Add your license information here]

## 🐛 Troubleshooting

### Common Issues

**Port 3000 already in use**

```bash
# Kill the process using port 3000
npx kill-port 3000
# Or use a different port
PORT=3001 npm run dev
```

**Module not found errors**

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**TypeScript errors after pull**

```bash
# Regenerate Nuxt types
npm run postinstall
```

---

Built with ❤️ using Nuxt 3
