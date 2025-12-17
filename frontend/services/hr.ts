/**
 * HR Service
 * Handles all HR-related API calls
 */

import type { JDInput, SaveQuestionsRequest, GenerateQuestionsResponse, Role } from '@/types'

export const hrService = {
  /**
   * Generate interview questions using AI
   */
  async generateQuestions(roleTitle: string, jobDescription: string): Promise<GenerateQuestionsResponse> {
    const { post } = useApi()
    const data: JDInput = {
      role_title: roleTitle,
      job_description: jobDescription
    }
    return await post<GenerateQuestionsResponse>('/hr/generate-questions', data)
  },

  /**
   * Save questions to database
   */
  async saveQuestions(roleId: string, roleTitle: string, questions: string[]): Promise<any> {
    const { post } = useApi()
    const data: SaveQuestionsRequest = {
      role_id: roleId,
      role_title: roleTitle,
      questions
    }
    return await post('/hr/save-questions', data)
  },

  /**
   * Get all available roles
   */
  async getRoles(): Promise<Role[]> {
    const { get } = useApi()
    return await get<Role[]>('/hr/roles')
  },

  /**
   * Get detailed information for a specific role
   */
  async getRoleDetails(roleId: string): Promise<any> {
    const { get } = useApi()
    return await get(`/hr/roles/${roleId}`)
  },

  /**
   * Update questions for an existing role
   */
  async updateQuestions(roleId: string, questions: string[]): Promise<any> {
    const { put } = useApi()
    return await put(`/hr/roles/${roleId}/questions`, { questions })
  },

  /**
   * Delete a role
   */
  async deleteRole(roleId: string): Promise<any> {
    const { del } = useApi()
    return await del(`/hr/roles/${roleId}`)
  }
}
