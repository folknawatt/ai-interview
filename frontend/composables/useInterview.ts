// import { useState } from '#imports'

export const useInterview = () => {
  const candidateName = useState<string>('candidateName', () => '')
  const question = useState<string>('question', () => 'ช่วยแนะนำตัวและบอกจุดแข็งของคุณหน่อยครับ')
  const videoFile = useState<File | null>('videoFile', () => null)
  const analysisResult = useState<any>('analysisResult', () => null)

  const setCandidateName = (name: string) => {
    candidateName.value = name
  }

  const setQuestion = (q: string) => {
    question.value = q
  }

  const setVideoFile = (file: File) => {
    videoFile.value = file
  }

  const setAnalysisResult = (result: any) => {
    analysisResult.value = result
  }

  return {
    candidateName,
    question,
    videoFile,
    analysisResult,
    setCandidateName,
    setQuestion,
    setVideoFile,
    setAnalysisResult
  }
}
