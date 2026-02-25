import type { Question, AnalysisResponse, SessionSummary } from '../types/api'

/**
 * Updated Interview composable with API integration
 */
export const useInterview = () => {
  const { get, post, uploadFile } = useApi()

  // State management - Persistent (Cookies)
  const candidateName = useCookie<string>('curr_candidate_name', {
    default: () => '',
    maxAge: 86400,
  })
  const candidateEmail = useCookie<string>('curr_candidate_email', {
    default: () => '',
    maxAge: 86400,
  })
  const sessionId = useCookie<string>('curr_session_id', { default: () => '', maxAge: 86400 })
  const selectedRole = useCookie<{ id: string; name: string } | null>('curr_selected_role', {
    default: () => null,
    maxAge: 86400,
  })

  // State management - Ephemeral (Memory/State)
  // These can be reset on reload without breaking the flow too much,
  // or logic will re-fetch them based on sessionId/index
  const currentQuestionIndex = useState<number>('currentQuestionIndex', () => 0)
  const currentQuestionId = useState<number>('currentQuestionId', () => -1)
  const currentQuestion = useState<string>('currentQuestion', () => '')
  const currentAudioPath = useState<string | null>('currentAudioPath', () => null)
  const analysisResult = useState<AnalysisResponse | null>('analysisResult', () => null)

  // Setters
  const setCandidateInfo = (name: string, email: string) => {
    candidateName.value = name
    candidateEmail.value = email
  }

  const setCandidateName = (name: string) => {
    candidateName.value = name
  }

  const setSelectedRole = (role: { id: string; name: string }) => {
    selectedRole.value = role
    // Don't auto-generate session ID here.
    // We must wait for uploadResume() to return the real server session ID.
    currentQuestionIndex.value = 0
  }

  const setAnalysisResult = (result: AnalysisResponse) => {
    analysisResult.value = result
  }

  /**
   * Fetch question from API
   * @param skipTts - If true, skip TTS audio generation (for checking next question status)
   */
  const getQuestion = async (roleId: string, index: number, skipTts: boolean = false) => {
    try {
      // If we have a server-generated session (from uploadResume), use the session endpoint
      // Client-generated sessions start with 'session_', server ones with 'sess_'
      // Strict Mode: Session ID from backend is REQUIRED (must start with 'sess_')
      if (sessionId.value && sessionId.value.startsWith('sess_')) {
        const params = skipTts ? '?skip_tts=true' : ''
        const response = await get<Question>(
          `/interview/session/${sessionId.value}/question/${index}${params}`
        )

        if (response.status === 'continue' && response.question) {
          currentQuestion.value = response.question
          currentQuestionId.value = response.question_id || -1
          currentQuestionIndex.value = index
          currentAudioPath.value = response.audio_path || null
          return response
        }
        return response
      }

      console.warn('Invalid session state: Missing resume-generated session ID')
      return { status: 'finished' } as Question
    } catch (error) {
      console.error('Error fetching question:', error)
      throw error
    }
  }

  // Track current audio instance for cleanup
  let currentAudioInstance: HTMLAudioElement | null = null

  /**
   * Play audio for current question
   * Supports both .mp3 (VachanaTTS) and .wav (Gemini TTS) formats
   */
  const playAudio = async () => {
    if (!currentAudioPath.value) {
      console.warn('No audio path available for playback')
      return
    }

    // Stop and cleanup previous audio if playing
    if (currentAudioInstance) {
      currentAudioInstance.pause()
      currentAudioInstance.src = ''
      currentAudioInstance = null
    }

    try {
      const audio = new Audio(currentAudioPath.value)
      currentAudioInstance = audio

      // Add error handler for audio loading/playback issues
      audio.onerror = e => {
        console.error('Audio playback error:', e)
        console.error('Failed to load audio from:', currentAudioPath.value)
      }

      await audio.play()
    } catch (error) {
      // Handle autoplay restrictions or other playback errors
      if (error instanceof DOMException && error.name === 'NotAllowedError') {
        // Autoplay blocked by browser - user interaction required
      } else {
        console.error('Failed to play audio:', error)
      }
      throw error // Re-throw for caller to handle
    }
  }

  /**
   * Stop currently playing audio
   */
  const stopAudio = () => {
    if (currentAudioInstance) {
      currentAudioInstance.pause()
      currentAudioInstance.currentTime = 0
      currentAudioInstance.src = ''
      currentAudioInstance = null
    }
  }

  /**
   * Upload answer video and get evaluation
   */
  const uploadAnswer = async (videoBlob: Blob, question: string) => {
    try {
      const formData = new FormData()
      formData.append('file', videoBlob, 'interview_answer.webm')
      formData.append('question', question)
      formData.append('question_id', currentQuestionId.value.toString())
      formData.append('session_id', sessionId.value)
      formData.append('role_id', selectedRole.value?.id || '')
      formData.append('candidate_name', candidateName.value || 'Anonymous')
      formData.append('candidate_email', candidateEmail.value || '')

      const response = await uploadFile<AnalysisResponse>('/interview/upload-answer', formData)

      analysisResult.value = response
      return response
    } catch (error) {
      console.error('Error uploading answer:', error)
      throw error
    }
  }

  /**
   * Upload resume PDF and generate questions
   */
  const uploadResume = async (file: File, roleId: string) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('role_id', roleId)
      formData.append('candidate_name', candidateName.value || 'Anonymous')
      if (candidateEmail.value) {
        formData.append('candidate_email', candidateEmail.value)
      }

      // Now endpoint returns { session_id, role_id, questions }
      const response = await uploadFile<{
        session_id: string
        role_id: string
        questions: string[]
      }>('/interview/upload-pdf', formData)

      // Update session ID immediately
      if (response.session_id) {
        sessionId.value = response.session_id
      }

      return response
    } catch (error) {
      console.error('Error uploading resume:', error)
      throw error
    }
  }

  /**
   * Get interview session summary
   */
  const getSummary = async () => {
    try {
      return await get<SessionSummary>(`/interview/summary/${sessionId.value}`)
    } catch (error) {
      console.error('Error fetching summary:', error)
      throw error
    }
  }

  /**
   * Complete interview and calculate aggregated scores
   */
  const completeInterview = async () => {
    try {
      const response = await post<{
        message: string
        session_id: string
        recommendation: string
        average_score: number
      }>(`/interview/complete/${sessionId.value}`)
      return response
    } catch (error) {
      console.error('Error completing interview:', error)
      throw error
    }
  }

  /**
   * Reset interview state
   */
  const resetInterview = () => {
    selectedRole.value = null
    currentQuestionIndex.value = 0
    currentQuestion.value = ''
    sessionId.value = ''
    analysisResult.value = null
    candidateName.value = ''
    candidateEmail.value = ''
  }

  return {
    // State
    candidateName,
    candidateEmail,
    selectedRole,
    currentQuestionIndex,
    currentQuestion,
    currentAudioPath,
    sessionId,
    analysisResult,

    // Methods
    setCandidateName,
    setCandidateInfo,
    setSelectedRole,
    setAnalysisResult,
    getQuestion,
    playAudio,
    stopAudio,
    uploadAnswer,
    uploadResume,
    getSummary,
    completeInterview,
    resetInterview,
  }
}
