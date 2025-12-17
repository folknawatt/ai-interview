/**
 * Candidate-related types
 */

export interface Candidate {
  id: string
  name: string
  email?: string
  phone?: string
  status: CandidateStatus
  createdAt: string
  updatedAt: string
}

export enum CandidateStatus {
  INVITED = 'invited',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REVIEWED = 'reviewed',
  ARCHIVED = 'archived'
}

export interface CandidateProfile {
  id: string
  name: string
  currentRole?: string
  experience?: number
  education?: string
  skills?: string[]
}

export interface CandidateWithSession extends Candidate {
  sessionId: string
  roleId: string
  roleTitle: string
  startedAt?: string
  completedAt?: string
}
