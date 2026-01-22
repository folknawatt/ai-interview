/**
 * Report and analytics types
 */

import type { AggregatedScore, AnalysisResponse } from './api'

export interface DetailedReport {
  sessionId: string
  candidateId: string
  candidateName: string
  roleId: string
  roleTitle: string
  interviewDate: string
  duration: number
  status: ReportStatus
  scores: ScoreBreakdown
  questionResponses: AnalysisResponse[]
  aggregatedScore: AggregatedScore
  recommendation: RecommendationType
  notes?: string
}

export enum ReportStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  REVIEWED = 'reviewed'
}

export enum RecommendationType {
  STRONG_PASS = 'Strong Pass',
  PASS = 'Pass',
  REVIEW = 'Review',
  FAIL = 'Fail'
}

export interface ScoreBreakdown {
  communication: ScoreDetail
  relevance: ScoreDetail
  logicalThinking: ScoreDetail
  overall: ScoreDetail
}

export interface ScoreDetail {
  score: number
  maxScore: number
  percentage: number
  grade: ScoreGrade
}

export enum ScoreGrade {
  EXCELLENT = 'excellent',
  GOOD = 'good',
  AVERAGE = 'average',
  BELOW_AVERAGE = 'below_average',
  POOR = 'poor'
}

export interface ComparisonMetrics {
  candidateScore: number
  averageScore: number
  topScore: number
  percentile: number
  ranking: number
  totalCandidates: number
}

export interface ReportSummary {
  sessionId: string
  candidateName: string
  roleTitle: string
  totalScore: number
  recommendation: RecommendationType
  interviewDate: string
  status: ReportStatus
}

export interface ReportFilter {
  roleId?: string
  status?: ReportStatus
  dateFrom?: string
  dateTo?: string
  minScore?: number
  maxScore?: number
  recommendation?: RecommendationType
}

export interface DashboardAnalytics {
  totalInterviews: number
  completedToday: number
  averageScore: number
  passRate: number
  topRoles: RolePerformance[]
  recentActivity: RecentActivity[]
  scoreDistribution: ScoreDistribution[]
}

export interface RolePerformance {
  roleId: string
  roleTitle: string
  interviewCount: number
  averageScore: number
  passRate: number
}

export interface RecentActivity {
  type: ActivityType
  message: string
  timestamp: string
  sessionId?: string
  candidateName?: string
}

export enum ActivityType {
  INTERVIEW_COMPLETED = 'interview_completed',
  QUESTION_GENERATED = 'question_generated',
  ROLE_CREATED = 'role_created',
  REPORT_REVIEWED = 'report_reviewed'
}

export interface ScoreDistribution {
  range: string
  count: number
  percentage: number
}
