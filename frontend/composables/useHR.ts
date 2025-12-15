import type { JDInput, SaveQuestionsRequest, GenerateQuestionsResponse, Role } from '../types/api';

/**
 * Composable for HR-related API operations
 */
export const useHR = () => {
  const { get, post, put, del } = useApi();

  /**
   * Generate interview questions using AI
   */
  const generateQuestions = async (roleTitle: string, jobDescription: string) => {
    const data: JDInput = {
      role_title: roleTitle,
      job_description: jobDescription,
    };

    return await post<GenerateQuestionsResponse>('/hr/generate-questions', data);
  };

  /**
   * Save questions to database
   */
  const saveQuestions = async (roleId: string, roleTitle: string, questions: string[]) => {
    const data: SaveQuestionsRequest = {
      role_id: roleId,
      role_title: roleTitle,
      questions,
    };

    return await post('/hr/save-questions', data);
  };

  /**
   * Get all available roles
   */
  const getRoles = async () => {
    return await get<Role[]>('/hr/roles');
  };

  /**
   * Get detailed information for a specific role
   */
  const getRoleDetails = async (roleId: string) => {
    return await get(`/hr/roles/${roleId}`);
  };

  /**
   * Update questions for an existing role
   */
  const updateQuestions = async (roleId: string, questions: string[]) => {
    return await put(`/hr/roles/${roleId}/questions`, { questions });
  };

  /**
   * Delete a role
   */
  const deleteRole = async (roleId: string) => {
    return await del(`/hr/roles/${roleId}`);
  };

  return {
    generateQuestions,
    saveQuestions,
    getRoles,
    getRoleDetails,
    updateQuestions,
    deleteRole,
  };
};
