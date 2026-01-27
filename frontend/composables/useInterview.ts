import type { Question, AnalysisResponse, SessionSummary } from '../types/api';
import { interviewService } from '../services/interview';

/**
 * Updated Interview composable with API integration
 */
export const useInterview = () => {


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
   * @param skipTts - If true, skip TTS audio generation (for checking next question status)
   */
  const getQuestion = async (roleId: string, index: number, skipTts: boolean = false) => {
    try {
      // If we have a server-generated session (from uploadResume), use the session endpoint
      // Client-generated sessions start with 'session_', server ones with 'sess_'
      if (sessionId.value && sessionId.value.startsWith('sess_')) {
        const response = await interviewService.getSessionQuestion(sessionId.value, index, skipTts);
        
        if (response.status === 'continue' && response.question) {
          currentQuestion.value = response.question;
          currentQuestionId.value = response.question_id || -1;
          currentQuestionIndex.value = index;
          currentAudioPath.value = response.audio_path || null;
          return response;
        }
        return response;
      }
      
      // If no valid session-based question found
      console.warn('No session question found or invalid session ID');
      return { status: 'finished' } as Question;
    } catch (error) {
      console.error('Error fetching question:', error);
      throw error;
    }
  };

  // Track current audio instance for cleanup
  let currentAudioInstance: HTMLAudioElement | null = null;

  /**
   * Play audio for current question
   * Supports both .mp3 (Edge TTS) and .wav (Gemini TTS) formats
   */
  const playAudio = async () => {
    if (!currentAudioPath.value) {
      console.warn('No audio path available for playback');
      return;
    }

    // Stop and cleanup previous audio if playing
    if (currentAudioInstance) {
      currentAudioInstance.pause();
      currentAudioInstance.src = '';
      currentAudioInstance = null;
    }

    try {
      const audio = new Audio(currentAudioPath.value);
      currentAudioInstance = audio;
      
      // Add error handler for audio loading/playback issues
      audio.onerror = (e) => {
        console.error('Audio playback error:', e);
        console.error('Failed to load audio from:', currentAudioPath.value);
      };

      await audio.play();
    } catch (error) {
      // Handle autoplay restrictions or other playback errors
      if (error instanceof DOMException && error.name === 'NotAllowedError') {
        console.log('Autoplay blocked by browser. User interaction required.');
      } else {
        console.error('Failed to play audio:', error);
      }
      throw error; // Re-throw for caller to handle
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

      const response = await interviewService.uploadAnswer(formData);
      
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
      formData.append('candidate_name', candidateName.value || 'Anonymous');
      if (candidateEmail.value) {
        formData.append('candidate_email', candidateEmail.value);
      }

      // Now endpoint returns { session_id, role_id, questions }
      const response = await interviewService.uploadResume(formData);
      
      // Update session ID immediately
      if (response.session_id) {
          sessionId.value = response.session_id;
      }

      return response;
    } catch (error) {
      console.error('Error uploading resume:', error);
      throw error;
    }
  };

  /**
   * Get interview summary
   */
  /**
   * Get interview session summary
   */
  const getSummary = async () => {
    try {
      return await interviewService.getSummary(sessionId.value);
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
      const response = await interviewService.completeInterview(sessionId.value);
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
