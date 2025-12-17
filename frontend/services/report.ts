/**
 * Report Service
 * Handles all report and analytics API calls
 */

import type { DetailedReport, ReportSummary, DashboardAnalytics } from '@/types'

export const reportService = {
  /**
   * Get detailed report for a session
   */
  async getReport(sessionId: string): Promise<DetailedReport> {
    const { get } = useApi()
    return await get<DetailedReport>(`/reports/${sessionId}`)
  },

  /**
   * Get all reports list
   */
  async getAllReports(): Promise<ReportSummary[]> {
    const { get } = useApi()
    return await get<ReportSummary[]>('/reports')
  },

  /**
   * Export report in specified format
   */
  async exportReport(sessionId: string, format: 'pdf' | 'csv' | 'json' = 'pdf'): Promise<Blob> {
    const { get } = useApi()
    return await get<Blob>(`/reports/${sessionId}/export?format=${format}`)
  },

  /**
   * Get dashboard analytics
   */
  async getAnalytics(): Promise<DashboardAnalytics> {
    const { get } = useApi()
    return await get<DashboardAnalytics>('/reports/analytics')
  }
}
