import type { Question, AnalysisResponse, SessionSummary } from '../types/api';

/**
 * Updated Interview composable with API integration
 */
export const useInterview = () => {
  const { get, post, uploadFile } = useApi();

  // State management
  const candidateName = useState<string>('candidateName', () => '');
  const candidateEmail = useState<string>('candidateEmail', () => '');
  const selectedRole = useState<{ id: string; name: string } | null>('selectedRole', () => null);
  const currentQuestionIndex = useState<number>('currentQuestionIndex', () => 0);
  const currentQuestionId = useState<number>('currentQuestionId', () => -1);
  const currentQuestion = useState<string>('currentQuestion', () => '');
  const currentAudioPath = useState<string | null>('currentAudioPath', () => null);
  const sessionId = useState<string>('sessionId', () => '');
  const analysisResult = useState<AnalysisResponse | null>('analysisResult', () => null);

  // Setters
  const setCandidateInfo = (name: string, email: string) => {
    candidateName.value = name;
    candidateEmail.value = email;
  };
  
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
        currentQuestionId.value = response.question_id || -1;
        currentQuestionIndex.value = index;
        currentAudioPath.value = response.audio_path || null;
        return response;
      }
      
      return response;
    } catch (error) {
      console.error('Error fetching question:', error);
      throw error;
    }
  };

  /**
   * Play audio for current question
   */
  const playAudio = async () => {
    if (currentAudioPath.value) {
      const audio = new Audio(currentAudioPath.value);
      await audio.play(); // Return promise for error handling
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
      formData.append('question_id', currentQuestionId.value.toString());
      formData.append('session_id', sessionId.value);
      formData.append('role_id', selectedRole.value?.id || '');
      formData.append('candidate_name', candidateName.value || 'Anonymous');
      formData.append('candidate_email', candidateEmail.value || '');

      const response = await uploadFile<AnalysisResponse>('/interview/upload-answer', formData);
      
      analysisResult.value = response;
      return response;
    } catch (error) {
      console.error('Error uploading answer:', error);
      throw error;
    }
  };

  /**
   * Upload resume PDF and generate questions
   */
  const uploadResume = async (file: File, roleId: string) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('role_id', roleId);

      // Expect back: { role_id: "new_id", base_role_id: "old_id", questions: [...] }
      const response = await uploadFile<{
         role_id: string; 
         base_role_id: string; 
         questions: string[]
      }>('/interview/upload-pdf', formData);
      
      return response;
    } catch (error) {
      console.error('Error uploading resume:', error);
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
    candidateName.value = '';
    candidateEmail.value = '';
  };

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
    uploadAnswer,
    uploadResume,
    getSummary,
    completeInterview,
    resetInterview,
  };
};
