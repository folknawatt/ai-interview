/**
 * HR Store
 * Manages HR dashboard state
 */

import { defineStore } from 'pinia'
import type { Role, ReportSummary } from '@/types'

interface HRState {
  selectedRole: Role | null
  generatedQuestions: string[]
  reports: ReportSummary[]
  isGenerating: boolean
  filter: {
    roleId?: string
    dateFrom?: string
    dateTo?: string
  }
}

export const useHRStore = defineStore('hr', {
  state: (): HRState => ({
    selectedRole: null,
    generatedQuestions: [],
    reports: [],
    isGenerating: false,
    filter: {}
  }),

  getters: {
    hasGeneratedQuestions: (state) => state.generatedQuestions.length > 0,
    
    filteredReports: (state) => {
      let filtered = state.reports

      if (state.filter.roleId) {
        filtered = filtered.filter(r => r.roleTitle === state.filter.roleId)
      }

      if (state.filter.dateFrom) {
        filtered = filtered.filter(r => r.interviewDate >= state.filter.dateFrom!)
      }

      if (state.filter.dateTo) {
        filtered = filtered.filter(r => r.interviewDate <= state.filter.dateTo!)
      }

      return filtered
    }
  },

  actions: {
    setSelectedRole(role: Role | null) {
      this.selectedRole = role
    },

    setGeneratedQuestions(questions: string[]) {
      this.generatedQuestions = questions
      this.isGenerating = false
    },

    addQuestion(question: string) {
      this.generatedQuestions.push(question)
    },

    removeQuestion(index: number) {
      this.generatedQuestions.splice(index, 1)
    },

    updateQuestion(index: number, question: string) {
      this.generatedQuestions[index] = question
    },

    clearQuestions() {
      this.generatedQuestions = []
    },

    setGenerating(isGenerating: boolean) {
      this.isGenerating = isGenerating
    },

    setReports(reports: ReportSummary[]) {
      this.reports = reports
    },

    updateFilter(filter: Partial<HRState['filter']>) {
      this.filter = { ...this.filter, ...filter }
    },

    clearFilter() {
      this.filter = {}
    }
  }
})
