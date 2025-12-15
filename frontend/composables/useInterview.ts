import type { Question, AnalysisResponse, SessionSummary } from '../types/api';

/**
 * Updated Interview composable with API integration
 */
export const useInterview = () => {
  const { get, post, uploadFile } = useApi();

  // State management
  const candidateName = useState<string>('candidateName', () => '');
  const selectedRole = useState<{ id: string; name: string } | null>('selectedRole', () => null);
  const currentQuestionIndex = useState<number>('currentQuestionIndex', () => 0);
  const currentQuestion = useState<string>('currentQuestion', () => '');
  const sessionId = useState<string>('sessionId', () => '');
  const analysisResult = useState<AnalysisResponse | null>('analysisResult', () => null);

  // Setters
  const setCandidateName = (name: string) => {
    candidateName.value = name;
  };

  const setSelectedRole = (role: { id: string; name: string }) => {
    selectedRole.value = role;
    // Generate session ID when role is selected
    sessionId.value = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    currentQuestionIndex.value = 0;
  };

  const setAnalysisResult = (result: AnalysisResponse) => {
    analysisResult.value = result;
  };

  /**
   * Fetch question from API
   */
  const getQuestion = async (roleId: string, index: number) => {
    try {
      const response = await get<Question>(`/interview/question/${roleId}/${index}`);
      
      if (response.status === 'continue' && response.question) {
        currentQuestion.value = response.question;
        currentQuestionIndex.value = index;
        return response;
      }
      
      return response;
    } catch (error) {
      console.error('Error fetching question:', error);
      throw error;
    }
  };

  /**
   * Upload answer video and get evaluation
   */
  const uploadAnswer = async (videoBlob: Blob, question: string) => {
    try {
      const formData = new FormData();
      formData.append('file', videoBlob, 'interview_answer.webm');
      formData.append('question', question);
      formData.append('session_id', sessionId.value);
      formData.append('role_id', selectedRole.value?.id || '');
      formData.append('candidate_name', candidateName.value || 'Anonymous');

      const response = await uploadFile<AnalysisResponse>('/interview/upload-answer', formData);
      
      analysisResult.value = response;
      return response;
    } catch (error) {
      console.error('Error uploading answer:', error);
      throw error;
    }
  };

  /**
   * Get interview summary
   */
  const getSummary = async () => {
    try {
      return await get<SessionSummary>(`/interview/summary/${sessionId.value}`);
    } catch (error) {
      console.error('Error fetching summary:', error);
      throw error;
    }
  };

  /**
   * Complete interview and calculate aggregated scores
   */
  const completeInterview = async () => {
    try {
      const response = await post<{
        message: string;
        session_id: string;
        recommendation: string;
        total_score: number;
      }>(`/interview/complete/${sessionId.value}`);
      return response;
    } catch (error) {
      console.error('Error completing interview:', error);
      throw error;
    }
  };

  /**
   * Reset interview state
   */
  const resetInterview = () => {
    selectedRole.value = null;
    currentQuestionIndex.value = 0;
    currentQuestion.value = '';
    sessionId.value = '';
    analysisResult.value = null;
  };

  return {
    // State
    candidateName,
    selectedRole,
    currentQuestionIndex,
    currentQuestion,
    sessionId,
    analysisResult,
    
    // Methods
    setCandidateName,
    setSelectedRole,
    setAnalysisResult,
    getQuestion,
    uploadAnswer,
    getSummary,
    completeInterview,
    resetInterview,
  };
};
