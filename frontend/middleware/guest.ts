/**
 * Guest middleware
 * Redirects authenticated users away from guest-only pages (like login)
 * Prevents logged-in users from accessing login page
 */
import { useAuth } from '@/store/auth'

export default defineNuxtRouteMiddleware(() => {
  const authStore = useAuth()

  // If user is already logged in, redirect to appropriate page
  if (authStore.isLogin) {
    // Redirect to HR dashboard for authenticated users
    // In production, could redirect based on user role
    return navigateTo('/hr/dashboard')
  }
})
