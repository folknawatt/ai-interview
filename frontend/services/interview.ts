/**
 * Interview Service
 * Handles all interview-related API calls
 */

import type { Question, AnalysisResponse, SessionSummary } from '@/types'

export const interviewService = {
  /**
   * Fetch a question for a specific session and index (Snapshot Pattern)
   * @param skipTts - If true, skip TTS audio generation (for checking next question)
   */
  async getSessionQuestion(sessionId: string, index: number, skipTts: boolean = false): Promise<Question> {
    const { get } = useApi()
    const params = skipTts ? '?skip_tts=true' : ''
    return await get<Question>(`/interview/session/${sessionId}/question/${index}${params}`)
  },

  /**
   * Upload resume PDF and generate questions
   */
  async uploadResume(formData: FormData): Promise<{
    session_id: string
    role_id: string
    questions: string[]
  }> {
    const { uploadFile } = useApi()
    return await uploadFile<{
      session_id: string
      role_id: string
      questions: string[]
    }>('/interview/upload-pdf', formData)
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
