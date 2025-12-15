import { describe, it, expect, vi, beforeEach } from 'vitest'
import type { Ref } from 'vue'

// Create state store for useState mock
const stateStore = new Map<string, any>()

// Mock useState from Nuxt
const mockUseState = <T>(key: string, init: () => T): Ref<T> => {
  if (!stateStore.has(key)) {
    stateStore.set(key, init())
  }
  const state = {
    get value() {
      return stateStore.get(key)
    },
    set value(val: T) {
      stateStore.set(key, val)
    }
  }
  return state as Ref<T>
}

// Mock the useApi composable
const mockGet = vi.fn()
const mockPost = vi.fn()
const mockUploadFile = vi.fn()

const mockUseApi = () => ({
  get: mockGet,
  post: mockPost,
  uploadFile: mockUploadFile
})

// Setup mocks before importing the composable
vi.stubGlobal('useState', mockUseState)
vi.stubGlobal('useApi', mockUseApi)

// Now import the composable
import { useInterview } from '../../../composables/useInterview'

describe('useInterview', () => {
  beforeEach(() => {
    // Clear all mocks
    vi.clearAllMocks()
    // Reset state store
    stateStore.clear()
  })

  it('should initialize with default state', () => {
    const interview = useInterview()
    
    expect(interview.candidateName.value).toBe('')
    expect(interview.selectedRole.value).toBeNull()
    expect(interview.currentQuestionIndex.value).toBe(0)
    expect(interview.currentQuestion.value).toBe('')
    expect(interview.sessionId.value).toBe('')
    expect(interview.analysisResult.value).toBeNull()
  })

  it('should set candidate name', () => {
    const interview = useInterview()
    
    interview.setCandidateName('John Doe')
    
    expect(interview.candidateName.value).toBe('John Doe')
  })

  it('should set selected role and generate session ID', () => {
    const interview = useInterview()
    
    const role = { id: 'role123', name: 'Software Engineer' }
    interview.setSelectedRole(role)
    
    expect(interview.selectedRole.value).toEqual(role)
    expect(interview.sessionId.value).toMatch(/^session_\d+_[a-z0-9]+$/)
    expect(interview.currentQuestionIndex.value).toBe(0)
  })

  it('should reset interview state', () => {
    const interview = useInterview()
    
    // Set some state
    interview.setCandidateName('John Doe')
    interview.setSelectedRole({ id: 'role123', name: 'Developer' })
    
    // Reset
    interview.resetInterview()
    
    expect(interview.selectedRole.value).toBeNull()
    expect(interview.currentQuestionIndex.value).toBe(0)
    expect(interview.currentQuestion.value).toBe('')
    expect(interview.sessionId.value).toBe('')
    expect(interview.analysisResult.value).toBeNull()
  })

  it('should fetch question from API', async () => {
    const interview = useInterview()
    const mockQuestion = { status: 'continue', question: 'What is your experience?' }
    mockGet.mockResolvedValue(mockQuestion)
    
    const result = await interview.getQuestion('role123', 0)
    
    expect(mockGet).toHaveBeenCalledWith('/interview/question/role123/0')
    expect(result).toEqual(mockQuestion)
    expect(interview.currentQuestion.value).toBe('What is your experience?')
    expect(interview.currentQuestionIndex.value).toBe(0)
  })

  it('should complete interview', async () => {
    const interview = useInterview()
    interview.setSelectedRole({ id: 'role123', name: 'Developer' })
    
    const mockResponse = {
      message: 'Interview completed',
      session_id: interview.sessionId.value,
      recommendation: 'Recommended',
      total_score: 85
    }
    mockPost.mockResolvedValue(mockResponse)
    
    const result = await interview.completeInterview()
    
    expect(mockPost).toHaveBeenCalledWith(`/interview/complete/${interview.sessionId.value}`)
    expect(result).toEqual(mockResponse)
  })
})
