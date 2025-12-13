import { describe, it, expect } from 'vitest'
import { useInterview } from '~/composables/useInterview'

describe('useInterview', () => {
  it('should initialize with default state', () => {
    const {
      currentQuestionIndex,
      currentQuestion,
      allQuestions
    } = useInterview()
    
    expect(currentQuestionIndex.value).toBe(0)
    expect(currentQuestion.value).toBeNull()
    expect(allQuestions.value).toEqual([])
  })

  it('should load questions when setQuestions is called', () => {
    const { setQuestions, allQuestions, currentQuestion } = useInterview()
    
    const mockQuestions = [
      'Question 1',
      'Question 2',
      'Question 3'
    ]
    
    setQuestions(mockQuestions)
    
    expect(allQuestions.value).toEqual(mockQuestions)
    expect(currentQuestion.value).toBe('Question 1')
  })

  it('should navigate to the next question', () => {
    const { setQuestions, nextQuestion, currentQuestion, currentQuestionIndex } = useInterview()
    
    const mockQuestions = ['Q1', 'Q2', 'Q3']
    setQuestions(mockQuestions)
    
    nextQuestion()
    
    expect(currentQuestionIndex.value).toBe(1)
    expect(currentQuestion.value).toBe('Q2')
  })

  it('should not go beyond the last question', () => {
    const { setQuestions, nextQuestion, currentQuestion, currentQuestionIndex } = useInterview()
    
    const mockQuestions = ['Q1', 'Q2']
    setQuestions(mockQuestions)
    
    nextQuestion() // Index 1
    nextQuestion() // Try to go to index 2 (doesn't exist)
    
    expect(currentQuestionIndex.value).toBe(1)
    expect(currentQuestion.value).toBe('Q2')
  })
})
