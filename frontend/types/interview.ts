/**
 * Interview session and flow types
 */

import type { Evaluation } from './api'

export interface InterviewSession {
  id: string
  sessionId: string
  candidateId: string
  candidateName: string
  roleId: string
  roleTitle: string
  status: InterviewSessionStatus
  currentQuestionIndex: number
  totalQuestions: number
  startedAt: string
  completedAt?: string
  lastActivityAt: string
}

export enum InterviewSessionStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  ABANDONED = 'abandoned'
}

export interface InterviewState {
  sessionId: string
  candidateName: string
  selectedRole: {
    id: string
    name: string
  } | null
  currentQuestionIndex: number
  currentQuestion: string
  totalQuestions: number
  isRecording: boolean
  hasStarted: boolean
  isCompleted: boolean
}

export interface VideoRecording {
  blob: Blob
  duration: number
  mimeType: string
  size: number
  recordedAt: string
}

export interface QuestionResponse {
  questionId?: string
  question: string
  videoUrl?: string
  transcription?: string
  evaluation?: Evaluation
  recordedAt: string
  duration?: number
}

export interface InterviewProgress {
  current: number
  total: number
  percentage: number
  questionsAnswered: number
  questionsRemaining: number
}
