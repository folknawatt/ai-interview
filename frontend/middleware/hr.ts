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

  // TODO: Add role-based authorization when user roles are implemented
  // For now, all authenticated users can access HR routes
  // In production, check if user has 'hr' or 'admin' role:
  // if (!authStore.hasRole('hr') && !authStore.hasRole('admin')) {
  //   return navigateTo('/403')
  // }
})
