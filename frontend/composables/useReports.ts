/**
 * useReports Composable
 * 
 * Provides functions to interact with HR reporting API endpoints:
 * - Fetch all interview reports with filtering
 * - Get detailed report for a specific session
 * - Download PDF reports
 * - Fetch overall statistics
 */

export const useReports = () => {
  const api = useApi();

  /**
   * Get all interview reports with optional filtering
   */
  const getAllReports = async (filters?: {
    roleId?: string;
    minScore?: number;
    recommendation?: string;
  }) => {
    const params = new URLSearchParams();
    
    if (filters?.roleId) params.append('role_id', filters.roleId);
    if (filters?.minScore !== undefined) params.append('min_score', filters.minScore.toString());
    if (filters?.recommendation) params.append('recommendation', filters.recommendation);

    const queryString = params.toString();
    const endpoint = `/reports/all${queryString ? `?${queryString}` : ''}`;

    return await api.get<any[]>(endpoint);
  };

  /**
   * Get detailed report for a specific interview session
   */
  const getReportDetails = async (sessionId: string) => {
    return await api.get(`/reports/${sessionId}`);
  };

  /**
   * Download PDF report for an interview
   */
  const downloadPDF = async (sessionId: string) => {
    try {
      const config = useRuntimeConfig();
      const baseURL = config.public.apiBaseUrl || 'http://localhost:8000';
      
      const response = await fetch(`${baseURL}/reports/${sessionId}/pdf`, {
        method: 'GET',
        headers: {
          'accept': 'application/pdf'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to download PDF');
      }

      // Extract filename from Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `interview_report_${sessionId}.pdf`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=([^;]+)/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/"/g, '').trim();
        }
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      
      // Cleanup after a longer delay to ensure download completes
      setTimeout(() => {
        if (link.parentNode) {
          document.body.removeChild(link);
        }
        window.URL.revokeObjectURL(url);
      }, 1000);

      return true;
    } catch (error) {
      console.error('Error downloading PDF:', error);
      throw error;
    }
  };

  /**
   * Get overall statistics
   */
  const getStatistics = async () => {
    return await api.get('/reports/statistics/overview');
  };

  return {
    getAllReports,
    getReportDetails,
    downloadPDF,
    getStatistics
  };
};
