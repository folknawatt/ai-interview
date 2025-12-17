// API Response Types

/**
 * Generic API error structure
 */
export interface ApiError {
  code: string
  message: string
  details?: Record<string, any>
}

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T> {
  data?: T
  error?: ApiError
  message?: string
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface LoginResponse {
  accessToken: string
  refreshToken: string
  user?: User
}

/**
 * User and authentication types
 */
export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  createdAt: string
}

export enum UserRole {
  HR = 'hr',
  ADMIN = 'admin',
  INTERVIEWER = 'interviewer'
}

export interface HRUser extends User {
  department?: string
  permissions: string[]
}

export interface Role {
  id: string;
  title: string;
}

export interface Question {
  status: 'continue' | 'finished';
  question?: string;
  question_id?: number;
  total?: number;
  audio_path?: string | null;
}

export interface Evaluation {
  scores: {
    communication: number;
    relevance: number;
    logical_thinking: number;
    total: number;
  };
  feedback: {
    strengths: string;
    weaknesses: string;
    summary: string;
    reasoning?: string;
  };
  pass_prediction: boolean;
}

export interface AnalysisResponse {
  question: string;
  transcript: string;
  evaluation: Evaluation;
}

export interface AggregatedScore {
  average_score: number;
  communication_avg: number;
  relevance_avg: number;
  logical_thinking_avg: number;
  pass_rate: number;
  overall_recommendation: string;
  questions_answered: number;
  total_questions: number;
}

export interface SessionSummary {
  total_questions: number;
  details: AnalysisResponse[];
  aggregated_score?: AggregatedScore;
}

// API Request Types

export interface JDInput {
  role_title: string;
  job_description: string;
}

export interface SaveQuestionsRequest {
  role_id: string;
  role_title: string;
  questions: string[];
}

export interface TTSRequest {
  text: string;
  provider?: 'gemini' | 'edge';
}

export interface GenerateQuestionsResponse {
  suggested_questions: string[];
}

export interface TTSResponse {
  success: boolean;
  audio_path: string;
  filename: string;
}
