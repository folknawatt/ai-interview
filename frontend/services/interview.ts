/**
 * Interview Service
 * Handles all interview-related API calls
 */

import type { Question, AnalysisResponse, SessionSummary } from '@/types'

export const interviewService = {
  /**
   * Fetch a question for a specific role and index
   */
  async getQuestion(roleId: string, index: number): Promise<Question> {
    const { get } = useApi()
    return await get<Question>(`/interview/question/${roleId}/${index}`)
  },

  /**
   * Upload answer video and get evaluation
   */
  async uploadAnswer(formData: FormData): Promise<AnalysisResponse> {
    const { uploadFile } = useApi()
    return await uploadFile<AnalysisResponse>('/interview/upload-answer', formData)
  },

  /**
   * Get interview session summary
   */
  async getSummary(sessionId: string): Promise<SessionSummary> {
    const { get } = useApi()
    return await get<SessionSummary>(`/interview/summary/${sessionId}`)
  },

  /**
   * Complete interview and calculate aggregated scores
   */
  async completeInterview(sessionId: string): Promise<{
    message: string
    session_id: string
    recommendation: string
    total_score: number
  }> {
    const { post } = useApi()
    return await post(`/interview/complete/${sessionId}`)
  }
}
