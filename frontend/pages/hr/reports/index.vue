<template>
  <div class="reports-container">
    <div class="mb-6">
      <NuxtLink to="/hr/dashboard" class="text-minimal-info hover:text-sky-600">
        ← Back to Dashboard
      </NuxtLink>
    </div>
    <h1>Interview Reports</h1>

    <!-- Statistics Cards -->
    <div v-if="statistics" class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <UsersIcon class="icon-svg" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.total_candidates }}</div>
          <div class="stat-label">Total Candidates</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <ChartBarIcon class="icon-svg" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.average_score }}</div>
          <div class="stat-label">Average Score</div>
        </div>
      </div>
      <div class="stat-card">
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
    <div class="filter-panel">
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
    <table v-else class="reports-table">
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

const getScoreClass = (score: number | null) => {
  if (score === null) return 'score-pending'
  if (score >= 8) return 'score-excellent'
  if (score >= 6) return 'score-good'
  if (score >= 4) return 'score-fair'
  return 'score-poor'
}

const getRecommendationClass = (rec: string | null) => {
  if (!rec) return 'rec-pending'
  if (rec === 'Strong Pass') return 'rec-strong-pass'
  if (rec === 'Pass') return 'rec-pass'
  if (rec === 'Review') return 'rec-review'
  return 'rec-fail'
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
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #1a1a1a;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  color: white;
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
  opacity: 0.9;
}

.filter-panel {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  color: #555;
}

.filter-group input,
.filter-group select {
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #e0e0e0;
  color: #555;
}

.btn-secondary:hover {
  background: #d0d0d0;
}

.reports-table {
  width: 100%;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.reports-table th {
  background: #f5f5f5;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

.reports-table th:hover {
  background: #e8e8e8;
}

.reports-table td {
  padding: 1rem;
  border-top: 1px solid #f0f0f0;
}

.clickable-row {
  cursor: pointer;
  transition: background 0.2s;
}

.clickable-row:hover {
  background: #f9f9f9;
}

.score-badge,
.recommendation-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
}

.score-excellent {
  background: #10b981;
  color: white;
}

.score-good {
  background: #3b82f6;
  color: white;
}

.score-fair {
  background: #f59e0b;
  color: white;
}

.score-poor {
  background: #ef4444;
  color: white;
}

.score-pending {
  background: #9ca3af;
  color: white;
}

.rec-strong-pass {
  background: #10b981;
  color: white;
}

.rec-pass {
  background: #3b82f6;
  color: white;
}

.rec-review {
  background: #f59e0b;
  color: white;
}

.rec-fail {
  background: #ef4444;
  color: white;
}

.rec-pending {
  background: #9ca3af;
  color: white;
}

.btn-view,
.btn-download {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: transform 0.2s;
}

.btn-view:hover,
.btn-download:hover {
  transform: scale(1.2);
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
  color: #666;
}

.error {
  color: #ef4444;
}
</style>
