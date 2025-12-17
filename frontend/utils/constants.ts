/**
 * Application constants and configuration values
 */

/**
 * Score thresholds for evaluation
 */
export const SCORE_THRESHOLDS = {
  PASS_SCORE: 70,
  EXCELLENT_SCORE: 90,
  GOOD_SCORE: 75,
  AVERAGE_SCORE: 60,
  MIN_SCORE: 0,
  MAX_SCORE: 100
} as const

/**
 * Video recording constraints
 */
export const VIDEO_CONSTRAINTS = {
  VIDEO: {
    width: { ideal: 1280 },
    height: { ideal: 720 },
    facingMode: 'user'
  },
  AUDIO: {
    echoCancellation: true,
    noiseSuppression: true,
    sampleRate: 44100
  },
  MAX_DURATION: 300, // 5 minutes in seconds
  MIN_DURATION: 10,  // 10 seconds
  MIME_TYPE: 'video/webm;codecs=vp9,opus'
} as const

/**
 * Question limits per role
 */
export const QUESTION_LIMITS = {
  MIN_QUESTIONS: 3,
  MAX_QUESTIONS: 15,
  DEFAULT_QUESTIONS: 5,
  RECOMMENDED_QUESTIONS: 7
} as const

/**
 * Application routes
 */
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  ROLE_SELECTION: '/role-selection',
  QUESTION: '/question',
  RECORD: '/record',
  RESULT: '/result',
  HR: {
    DASHBOARD: '/hr/dashboard',
    ROLES: '/hr/roles',
    GENERATE: '/hr/generate',
    REPORTS: '/hr/reports',
    REPORT_DETAIL: (sessionId: string) => `/hr/reports/${sessionId}`
  }
} as const

/**
 * API endpoints
 */
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh-token',
    ME: '/auth/me'
  },
  INTERVIEW: {
    QUESTION: (roleId: string, index: number) => `/interview/question/${roleId}/${index}`,
    UPLOAD_ANSWER: '/interview/upload-answer',
    SUMMARY: (sessionId: string) => `/interview/summary/${sessionId}`,
    COMPLETE: (sessionId: string) => `/interview/complete/${sessionId}`
  },
  HR: {
    GENERATE_QUESTIONS: '/hr/generate-questions',
    SAVE_QUESTIONS: '/hr/save-questions',
    ROLES: '/hr/roles',
    ROLE_DETAIL: (roleId: string) => `/hr/roles/${roleId}`,
    UPDATE_QUESTIONS: (roleId: string) => `/hr/roles/${roleId}/questions`,
    DELETE_ROLE: (roleId: string) => `/hr/roles/${roleId}`
  },
  REPORTS: {
    LIST: '/reports',
    DETAIL: (sessionId: string) => `/reports/${sessionId}`,
    EXPORT: (sessionId: string, format: string) => `/reports/${sessionId}/export?format=${format}`,
    ANALYTICS: '/reports/analytics'
  },
  TTS: '/tts'
} as const

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'token',
  REFRESH_TOKEN: 'refresh-token',
  USER_DATA: 'user-data',
  INTERVIEW_STATE: 'interview-state',
  THEME: 'theme'
} as const

/**
 * Time constants (in milliseconds)
 */
export const TIME = {
  SECOND: 1000,
  MINUTE: 60 * 1000,
  HOUR: 60 * 60 * 1000,
  DAY: 24 * 60 * 60 * 1000
} as const

/**
 * Pagination defaults
 */
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
} as const
