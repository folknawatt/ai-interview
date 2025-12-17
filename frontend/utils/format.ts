/**
 * String and number formatting utilities
 */

/**
 * Format a score as a percentage
 * @param score - Score value (0-100)
 * @param decimals - Number of decimal places
 * @returns Formatted percentage string
 */
export function formatScore(score: number, decimals = 1): string {
  return `${score.toFixed(decimals)}%`
}

/**
 * Format duration in MM:SS format
 * @param seconds - Duration in seconds
 * @returns Formatted duration string (MM:SS or HH:MM:SS)
 */
export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

/**
 * Truncate text to a maximum length with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @param ellipsis - Ellipsis string (default: '...')
 * @returns Truncated text
 */
export function truncate(text: string, maxLength: number, ellipsis = '...'): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength - ellipsis.length) + ellipsis
}

/**
 * Capitalize first letter of a string
 * @param text - Text to capitalize
 * @returns Capitalized text
 */
export function capitalize(text: string): string {
  if (!text) return ''
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

/**
 * Capitalize first letter of each word
 * @param text - Text to capitalize
 * @returns Title-cased text
 */
export function titleCase(text: string): string {
  if (!text) return ''
  return text
    .split(' ')
    .map(word => capitalize(word))
    .join(' ')
}

/**
 * Format a number with thousand separators
 * @param value - Number to format
 * @returns Formatted number string
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value)
}

/**
 * Format bytes to human-readable size
 * @param bytes - Size in bytes
 * @param decimals - Number of decimal places
 * @returns Formatted size string (e.g., "1.5 MB")
 */
export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`
}

/**
 * Convert snake_case to Title Case
 * @param text - Snake case text
 * @returns Title case text
 */
export function snakeToTitle(text: string): string {
  return text
    .split('_')
    .map(word => capitalize(word))
    .join(' ')
}

/**
 * Convert camelCase to Title Case
 * @param text - Camel case text
 * @returns Title case text
 */
export function camelToTitle(text: string): string {
  return text
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim()
}

/**
 * Pluralize a word based on count
 * @param count - Number of items
 * @param singular - Singular form
 * @param plural - Optional plural form (default: adds 's')
 * @returns Pluralized text with count
 */
export function pluralize(count: number, singular: string, plural?: string): string {
  const word = count === 1 ? singular : (plural || `${singular}s`)
  return `${count} ${word}`
}

/**
 * Format a list of items with proper grammar
 * @param items - Array of items
 * @param conjunction - Conjunction word (default: 'and')
 * @returns Formatted list string
 */
export function formatList(items: string[], conjunction = 'and'): string {
  if (items.length === 0) return ''
  if (items.length === 1) return items[0] ?? ''
  if (items.length === 2) return `${items[0] ?? ''} ${conjunction} ${items[1] ?? ''}`

  const last = items[items.length - 1]
  const rest = items.slice(0, -1)
  return `${rest.join(', ')}, ${conjunction} ${last ?? ''}`
}
