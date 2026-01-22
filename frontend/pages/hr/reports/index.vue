<template>
  <div class="reports-container">
    <div class="mb-6">
      <NuxtLink 
        to="/hr/dashboard" 
        class="inline-flex items-center gap-2 px-4 py-2 text-interview-text-secondary hover:text-interview-text-primary hover:bg-interview-surface rounded-xl transition-all duration-300 -ml-4"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </NuxtLink>
    </div>
    <h1 class="reports-anim text-3xl font-bold mb-8 text-interview-text-primary" style="--delay: 0ms">Interview Reports</h1>

    <!-- Statistics Cards -->
    <div v-if="statistics" class="stats-grid">
      <div class="stat-card reports-anim" style="--delay: 80ms">
        <div class="stat-icon">
          <UsersIcon class="icon-svg" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.total_candidates }}</div>
          <div class="stat-label">Total Candidates</div>
        </div>
      </div>
      <div class="stat-card reports-anim" style="--delay: 160ms">
        <div class="stat-icon">
          <ChartBarIcon class="icon-svg" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.average_score }}</div>
          <div class="stat-label">Average Score</div>
        </div>
      </div>
      <div class="stat-card reports-anim" style="--delay: 240ms">
        <div class="stat-icon">
          <CheckCircleIcon class="icon-svg" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.pass_rate }}%</div>
          <div class="stat-label">Pass Rate</div>
        </div>
      </div>
    </div>

    <!-- Filter Panel -->
    <div class="filter-panel reports-anim" style="--delay: 320ms">
      <div class="filter-group">
        <label>Role:</label>
        <select v-model="filters.roleId">
          <option value="">All Roles</option>
          <option v-for="role in roles" :key="role.id" :value="role.id">
            {{ role.title }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label>Min Score:</label>
        <input
          v-model.number="filters.minScore"
          type="number"
          min="0"
          max="10"
          step="0.1"
          placeholder="0-10"
        />
      </div>

      <div class="filter-group">
        <label>Recommendation:</label>
        <select v-model="filters.recommendation">
          <option value="">All</option>
          <option value="Strong Pass">Strong Pass</option>
          <option value="Pass">Pass</option>
          <option value="Review">Review</option>
          <option value="Fail">Fail</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Search:</label>
        <input v-model="searchQuery" type="text" placeholder="Search by name..." />
      </div>

      <button @click="loadReports" class="btn-primary">Apply Filters</button>
      <button @click="clearFilters" class="btn-secondary">Clear</button>
    </div>

    <!-- Reports Table -->
    <div v-if="loading" class="loading">Loading reports...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="filteredReports.length === 0" class="empty">No reports found</div>
    <table v-else class="reports-table reports-anim" style="--delay: 400ms">
      <thead>
        <tr>
          <th @click="sort('name')">Name {{ getSortIcon('name') }}</th>
          <th @click="sort('role_id')">Role {{ getSortIcon('role_id') }}</th>
          <th @click="sort('interview_date')">Date {{ getSortIcon('interview_date') }}</th>
          <th @click="sort('average_score')">Score {{ getSortIcon('average_score') }}</th>
          <th @click="sort('overall_recommendation')">
            Recommendation {{ getSortIcon('overall_recommendation') }}
          </th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="report in sortedReports"
          :key="report.session_id"
          @click="viewReport(report.session_id)"
          class="clickable-row"
        >
          <td>{{ report.name }}</td>
          <td>{{ report.role_id }}</td>
          <td>{{ formatDate(report.interview_date) }}</td>
          <td>
            <span class="score-badge" :class="getScoreClass(report.average_score)">
              {{ report.average_score ? report.average_score.toFixed(0) : 'N/A' }}
            </span>
          </td>
          <td>
            <span
              class="recommendation-badge"
              :class="getRecommendationClass(report.overall_recommendation)"
            >
              {{ report.overall_recommendation || 'Pending' }}
            </span>
          </td>
          <td @click.stop>
            <button @click="viewReport(report.session_id)" class="btn-view" title="View Details">
              <EyeIcon class="icon-btn" />
            </button>
            <button
              @click="downloadReport(report.session_id)"
              class="btn-download"
              title="Download PDF"
            >
              <ArrowDownTrayIcon class="icon-btn" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import {
  UsersIcon,
  ChartBarIcon,
  CheckCircleIcon,
  EyeIcon,
  ArrowDownTrayIcon,
} from '@heroicons/vue/24/solid'

const { getAllReports, getStatistics, downloadPDF } = useReports()
const { getRoles } = useHR()
const router = useRouter()

const statistics = ref<any>(null)
const reports = ref<any[]>([])
const roles = ref<any[]>([])
const loading = ref(false)
const error = ref('')

const filters = reactive({
  roleId: '',
  minScore: undefined as number | undefined,
  recommendation: '',
})

const searchQuery = ref('')
const sortKey = ref('average_score')
const sortOrder = ref<'asc' | 'desc'>('desc')

// Load initial data
onMounted(async () => {
  await loadStatistics()
  await loadRoles()
  await loadReports()
})

const loadStatistics = async () => {
  try {
    statistics.value = await getStatistics()
  } catch (err: any) {
    console.error('Error loading statistics:', err)
  }
}

const loadRoles = async () => {
  try {
    roles.value = await getRoles()
  } catch (err: any) {
    console.error('Error loading roles:', err)
  }
}

const loadReports = async () => {
  try {
    loading.value = true
    error.value = ''

    const filterParams: any = {}
    if (filters.roleId) filterParams.roleId = filters.roleId
    if (filters.minScore !== undefined) filterParams.minScore = filters.minScore
    if (filters.recommendation) filterParams.recommendation = filters.recommendation

    reports.value = await getAllReports(filterParams)
  } catch (err: any) {
    error.value = err.message || 'Failed to load reports'
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.roleId = ''
  filters.minScore = undefined
  filters.recommendation = ''
  searchQuery.value = ''
  loadReports()
}

const filteredReports = computed(() => {
  if (!searchQuery.value) return reports.value

  const query = searchQuery.value.toLowerCase()
  return reports.value.filter(report => report.name.toLowerCase().includes(query))
})

const sortedReports = computed(() => {
  const sorted = [...filteredReports.value]

  sorted.sort((a, b) => {
    let aVal = a[sortKey.value]
    let bVal = b[sortKey.value]

    if (aVal === null || aVal === undefined) return 1
    if (bVal === null || bVal === undefined) return -1

    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    }

    if (sortOrder.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })

  return sorted
})

const sort = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'desc'
  }
}

const getSortIcon = (key: string) => {
  if (sortKey.value !== key) return ''
  return sortOrder.value === 'asc' ? '↑' : '↓'
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

// Unified color scheme:
// Green (22c55e) = Excellent (Score >= 4/5, Strong Pass)
// Blue (3b82f6) = Good (Score >= 3/5, Pass)
// Amber (FFC428) = Fair (Score >= 2/5, Review)
// Red (ef4444) = Poor (Score < 2/5, Fail)
// Gray = Pending/Unknown

const getScoreClass = (score: number | null) => {
  if (score === null) return 'score-pending'
  if (score >= 4) return 'score-excellent'   // 4-5: Excellent (Green)
  if (score >= 3) return 'score-good'        // 3-4: Good (Blue)
  if (score >= 2) return 'score-fair'        // 2-3: Fair (Amber)
  return 'score-poor'                        // 0-2: Poor (Red)
}

const getRecommendationClass = (rec: string | null) => {
  if (!rec) return 'rec-pending'
  if (rec === 'Strong Pass') return 'rec-strong-pass'  // Green
  if (rec === 'Pass') return 'rec-pass'                // Blue
  if (rec === 'Review') return 'rec-review'            // Amber
  return 'rec-fail'                                    // Red
}

const viewReport = (sessionId: string) => {
  router.push(`/hr/reports/${sessionId}`)
}

const downloadReport = async (sessionId: string) => {
  try {
    await downloadPDF(sessionId)
  } catch (err: any) {
    alert('Failed to download PDF: ' + err.message)
  }
}
</script>

<style scoped>
.reports-container {
  padding: 0;
  max-width: 1400px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #FFB128 0%, #FF9500 100%);
  color: #0a0a0f;
  padding: 1.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 0 30px rgba(255, 177, 40, 0.2);
}

.stat-icon {
  font-size: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg {
  width: 3rem;
  height: 3rem;
  color: #0a0a0f;
}

.icon-btn {
  width: 1.2rem;
  height: 1.2rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.filter-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #a1a1aa;
}

.filter-group input,
.filter-group select {
  padding: 0.6rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  font-size: 0.95rem;
  color: #ffffff;
}

.filter-group input::placeholder {
  color: #71717a;
}

.filter-group select option {
  background: #12121a;
  color: #ffffff;
}

.btn-primary,
.btn-secondary {
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: #FFB128;
  color: #0a0a0f;
}

.btn-primary:hover {
  background: #FF9500;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #a1a1aa;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}

.reports-table {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border-radius: 1rem;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.reports-table th {
  background: rgba(255, 255, 255, 0.08);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
  color: #ffffff;
}

.reports-table th:hover {
  background: rgba(255, 255, 255, 0.12);
}

.reports-table td {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  color: #a1a1aa;
}

.clickable-row {
  cursor: pointer;
  transition: background 0.2s;
}

.clickable-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.clickable-row:hover td {
  color: #ffffff;
}

.score-badge,
.recommendation-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
}

.score-excellent {
  background: #22c55e;
  color: white;
}

.score-good {
  background: #3b82f6;
  color: white;
}

.score-fair {
  background: #FFC428;
  color: #0a0a0f;
}

.score-poor {
  background: #ef4444;
  color: white;
}

.score-pending {
  background: rgba(255, 255, 255, 0.2);
  color: #a1a1aa;
}

.rec-strong-pass {
  background: #22c55e;
  color: white;
}

.rec-pass {
  background: #3b82f6;
  color: white;
}

.rec-review {
  background: #FFC428;
  color: #0a0a0f;
}

.rec-fail {
  background: #ef4444;
  color: white;
}

.rec-pending {
  background: rgba(255, 255, 255, 0.2);
  color: #a1a1aa;
}

.btn-view,
.btn-download {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.2s;
  color: #a1a1aa;
}

.btn-view:hover {
  color: #FFB128;
  transform: scale(1.2);
}

.btn-download:hover {
  color: #22c55e;
  transform: scale(1.2);
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
  color: #a1a1aa;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error {
  color: #ef4444;
}

/* Smooth staggered animation */
.reports-anim {
  opacity: 0;
  transform: translate3d(0, 20px, 0);
  animation: reports-fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: var(--delay, 0ms);
}

@keyframes reports-fade-in {
  from {
    opacity: 0;
    transform: translate3d(0, 20px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
</style>
