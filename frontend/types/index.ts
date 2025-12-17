/**
 * Central export for all type definitions
 * Import types from here: import type { ... } from '@/types'
 */

// API types
export type {
  ApiError,
  ApiResponse,
  PaginatedResponse,
  LoginResponse,
  User,
  HRUser,
  Role,
  Question,
  Evaluation,
  AnalysisResponse,
  AggregatedScore,
  SessionSummary,
  JDInput,
  SaveQuestionsRequest,
  TTSRequest,
  GenerateQuestionsResponse,
  TTSResponse
} from './api'

// Candidate types
export type {
  Candidate,
  CandidateProfile,
  CandidateWithSession
} from './candidate'

// Interview types
export type {
  InterviewSession,
  InterviewState,
  VideoRecording,
  QuestionResponse,
  InterviewProgress
} from './interview'

// Question types
export type {
  QuestionWithRole,
  RoleWithQuestions,
  QuestionBank,
  RoleStatistics
} from './question'

// Report types
export type {
  DetailedReport,
  ScoreBreakdown,
  ScoreDetail,
  ComparisonMetrics,
  ReportSummary,
  ReportFilter,
  DashboardAnalytics,
  RolePerformance,
  RecentActivity,
  ScoreDistribution
} from './report'

// Re-export enums for value access
export { CandidateStatus } from './candidate'
export { InterviewSessionStatus } from './interview'
export { QuestionCategory, QuestionDifficulty } from './question'
export {
  ReportStatus,
  RecommendationType,
  ScoreGrade,
  ActivityType
} from './report'
export { UserRole } from './api'
