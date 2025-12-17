/**
 * Question and role-related types
 */

export interface QuestionWithRole {
  id: string
  question: string
  roleId: string
  roleTitle: string
  category?: QuestionCategory
  difficulty?: QuestionDifficulty
  order: number
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export enum QuestionCategory {
  TECHNICAL = 'technical',
  BEHAVIORAL = 'behavioral',
  SITUATIONAL = 'situational',
  GENERAL = 'general'
}

export enum QuestionDifficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard'
}

export interface RoleWithQuestions {
  id: string
  title: string
  description?: string
  department?: string
  questions: QuestionWithRole[]
  questionCount: number
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export interface QuestionBank {
  roleId: string
  roleTitle: string
  questions: string[]
  totalQuestions: number
}

export interface RoleStatistics {
  roleId: string
  roleTitle: string
  totalCandidates: number
  completedInterviews: number
  averageScore: number
  passRate: number
}
