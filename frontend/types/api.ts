// API Response Types

import type { AxiosPromise } from 'axios'

export type Response<T> = {
    error?: {
        code: never
        message: string
    }
    data?: {
        title: string
        description: string
    } & T
}

export type ApiResponse<T> = AxiosPromise<
    Response<
        T extends unknown[]
            ? {
                  items: T
              }
            : { item: T }
    >
>

export interface LoginResponse {
    accessToken: string
    refreshToken: string
}

export interface Role {
  id: string;
  name: string;
}

export interface Question {
  status: 'continue' | 'finished';
  question?: string;
  total?: number;
}

export interface Evaluation {
  scores: {
    communication: number;
    relevance: number;
    quality: number;
    total: number;
  };
  feedback: {
    strengths: string;
    weaknesses: string;
    summary: string;
  };
  pass_prediction: boolean;
}

export interface AnalysisResponse {
  question: string;
  transcript: string;
  evaluation: Evaluation;
}

export interface AggregatedScore {
  total_score: number;
  communication_avg: number;
  relevance_avg: number;
  quality_avg: number;
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
