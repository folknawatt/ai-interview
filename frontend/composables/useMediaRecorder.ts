export const useMediaRecorder = () => {
  const videoPreview = ref<HTMLVideoElement | null>(null)
  const mediaRecorder = ref<MediaRecorder | null>(null)
  const recordedChunks = ref<Blob[]>([])
  const recordedBlob = ref<Blob | null>(null)
  const isRecording = ref(false)
  const timer = ref(120)
  const error = ref<string | null>(null)
  let timerInterval: ReturnType<typeof setInterval>

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      })
      if (videoPreview.value) {
        videoPreview.value.srcObject = stream
      }
      error.value = null
    } catch (e) {
      console.error('Error accessing camera:', e)
      error.value = 'ไม่สามารถเข้าถึงกล้อง/ไมโครโฟนได้'
    }
  }

  const startRecording = async () => {
    if (!videoPreview.value?.srcObject) await startCamera()

    const stream = videoPreview.value?.srcObject as MediaStream
    if (!stream) return

    recordedChunks.value = []
    const mimeType = MediaRecorder.isTypeSupported('video/mp4') ? 'video/mp4' : 'video/webm'

    const recorder = new MediaRecorder(stream, { mimeType })

    recorder.ondataavailable = e => {
      if (e.data.size > 0) {
        recordedChunks.value.push(e.data)
      }
    }

    recorder.onstop = () => {
      recordedBlob.value = new Blob(recordedChunks.value, { type: mimeType })
      clearInterval(timerInterval)
      isRecording.value = false
    }

    recorder.start()
    mediaRecorder.value = recorder
    isRecording.value = true
    timer.value = 120 // Always reset before counting down

    // Reset timer or set it to initial value if needed, 
    // but usually we count down from 120 so we just ensure it's running
    timerInterval = setInterval(() => {
      if (timer.value > 0) {
        timer.value--
      } else {
        stopRecording()
      }
    }, 1000)
  }

  const stopRecording = () => {
    if (mediaRecorder.value && isRecording.value) {
      mediaRecorder.value.stop()
    }
  }

  const resetRecording = () => {
    recordedBlob.value = null
    recordedChunks.value = []
    timer.value = 120
    stopCamera() // Stop existing stream before starting a new one to prevent device/memory leak
    startCamera()
  }

  const stopCamera = () => {
      clearInterval(timerInterval)
      if (videoPreview.value?.srcObject) {
         const tracks = (videoPreview.value.srcObject as MediaStream).getTracks()
         tracks.forEach(track => track.stop())
      }
  }

  return {
    videoPreview,
    recordedBlob,
    isRecording,
    timer,
    error,
    formatTime,
    startCamera,
    stopCamera,
    startRecording,
    stopRecording,
    resetRecording
  }
}
