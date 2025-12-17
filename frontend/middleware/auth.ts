/**
 * Authentication middleware
 * Protects routes that require user authentication
 * Redirects to login page if not authenticated
 */
import { useAuth } from '@/store/auth'

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuth()

  // Check if user is authenticated
  if (!authStore.isLogin) {
    // Save the intended destination for redirect after login
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }
})
