/**
 * Interview Store
 * Manages interview session state
 */

import { defineStore } from 'pinia'
import type { InterviewState, QuestionResponse } from '@/types'

export const useInterviewStore = defineStore('interview', {
  state: (): InterviewState & { responses: QuestionResponse[] } => ({
    sessionId: '',
    candidateName: '',
    selectedRole: null,
    currentQuestionIndex: 0,
    currentQuestion: '',
    totalQuestions: 0,
    isRecording: false,
    hasStarted: false,
    isCompleted: false,
    responses: []
  }),

  getters: {
    progress: (state) => {
      if (state.totalQuestions === 0) return 0
      return Math.round((state.currentQuestionIndex / state.totalQuestions) * 100)
    },

    isLastQuestion: (state) => {
      return state.currentQuestionIndex >= state.totalQuestions - 1
    },

    canProceed: (state) => {
      return state.selectedRole !== null && state.candidateName.trim() !== ''
    }
  },

  actions: {
    startSession(candidateName: string, role: { id: string; name: string }, totalQuestions: number) {
      this.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      this.candidateName = candidateName
      this.selectedRole = role
      this.totalQuestions = totalQuestions
      this.currentQuestionIndex = 0
      this.hasStarted = true
      this.isCompleted = false
      this.responses = []
    },

    setCurrentQuestion(question: string, index: number) {
      this.currentQuestion = question
      this.currentQuestionIndex = index
    },

    setRecording(isRecording: boolean) {
      this.isRecording = isRecording
    },

    addResponse(response: QuestionResponse) {
      this.responses.push(response)
    },

    nextQuestion() {
      if (this.currentQuestionIndex < this.totalQuestions - 1) {
        this.currentQuestionIndex++
      }
    },

    completeSession() {
      this.isCompleted = true
      this.hasStarted = false
    },

    resetSession() {
      this.$reset()
    }
  }
})
