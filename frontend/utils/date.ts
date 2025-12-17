/**
 * Date formatting and manipulation utilities
 */

/**
 * Format a date to a localized string
 * @param date - Date to format (Date object, string, or timestamp)
 * @param format - Format type: 'short', 'medium', 'long', 'full'
 * @returns Formatted date string
 */
export function formatDate(
  date: Date | string | number,
  format: 'short' | 'medium' | 'long' | 'full' = 'medium'
): string {
  const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date

  const formats: Record<string, Intl.DateTimeFormatOptions> = {
    short: { year: 'numeric', month: 'numeric', day: 'numeric' },
    medium: { year: 'numeric', month: 'short', day: 'numeric' },
    long: { year: 'numeric', month: 'long', day: 'numeric' },
    full: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
  }

  const options = formats[format]

  return new Intl.DateTimeFormat('en-US', options).format(dateObj)
}

/**
 * Format a date to include time
 * @param date - Date to format
 * @param includeSeconds - Whether to include seconds
 * @returns Formatted date and time string
 */
export function formatDateTime(
  date: Date | string | number,
  includeSeconds = false
): string {
  const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    ...(includeSeconds && { second: '2-digit' })
  }

  return new Intl.DateTimeFormat('en-US', options).format(dateObj)
}

/**
 * Get relative time string (e.g., "2 hours ago", "in 3 days")
 * @param date - Date to compare
 * @returns Relative time string
 */
export function getRelativeTime(date: Date | string | number): string {
  const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date
  const now = new Date()
  const diffInMs = dateObj.getTime() - now.getTime()
  const diffInSeconds = Math.floor(Math.abs(diffInMs) / 1000)

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ]

  for (const interval of intervals) {
    const count = Math.floor(diffInSeconds / interval.seconds)
    if (count >= 1) {
      const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
      return rtf.format(diffInMs > 0 ? count : -count, interval.label as Intl.RelativeTimeFormatUnit)
    }
  }

  return 'just now'
}

/**
 * Calculate duration between two dates
 * @param start - Start date
 * @param end - End date
 * @returns Duration object with days, hours, minutes, seconds
 */
export function getDuration(start: Date | string | number, end: Date | string | number) {
  const startObj = typeof start === 'string' || typeof start === 'number' ? new Date(start) : start
  const endObj = typeof end === 'string' || typeof end === 'number' ? new Date(end) : end

  const diffInMs = endObj.getTime() - startObj.getTime()
  const diffInSeconds = Math.floor(diffInMs / 1000)

  const days = Math.floor(diffInSeconds / 86400)
  const hours = Math.floor((diffInSeconds % 86400) / 3600)
  const minutes = Math.floor((diffInSeconds % 3600) / 60)
  const seconds = diffInSeconds % 60

  return { days, hours, minutes, seconds, totalSeconds: diffInSeconds }
}

/**
 * Format duration in human-readable format
 * @param seconds - Duration in seconds
 * @returns Formatted duration string
 */
export function formatDurationFromSeconds(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

/**
 * Check if a date is today
 * @param date - Date to check
 * @returns True if date is today
 */
export function isToday(date: Date | string | number): boolean {
  const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date
  const today = new Date()

  return (
    dateObj.getDate() === today.getDate() &&
    dateObj.getMonth() === today.getMonth() &&
    dateObj.getFullYear() === today.getFullYear()
  )
}

/**
 * Check if a date is in the past
 * @param date - Date to check
 * @returns True if date is in the past
 */
export function isPast(date: Date | string | number): boolean {
  const dateObj = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date
  return dateObj.getTime() < new Date().getTime()
}
