/**
 * HR Authorization middleware
 * Protects HR-specific routes
 * Ensures only HR users can access HR dashboard and features
 */
import { useAuth } from '@/store/auth'

export default defineNuxtRouteMiddleware(to => {
  const authStore = useAuth()

  // Skip middleware checks while auth is loading to prevent race conditions
  if (authStore.loading) {
    return
  }

  // First check if user is authenticated at all
  if (!authStore.isLogin) {
    return navigateTo({
      path: '/hr/login',
      query: { redirect: to.fullPath },
    })
  }

  // Role-based authorization: only HR and Admin can access
  if (!authStore.hasRole('hr') && !authStore.hasRole('admin')) {
    return navigateTo('/403')
  }
})
