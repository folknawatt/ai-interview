/**
 * HR Authorization middleware
 * Protects HR-specific routes
 * Ensures only HR users can access HR dashboard and features
 */
import { useAuth } from '@/store/auth'

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuth()

  // First check if user is authenticated at all
  if (!authStore.isLogin) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }

  // Role-based authorization: only HR and Admin can access
  if (!authStore.hasRole('hr') && !authStore.hasRole('admin')) {
    return navigateTo('/403')
  }
})

