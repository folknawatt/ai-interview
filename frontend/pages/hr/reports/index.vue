<template>
  <div class="relative min-h-screen pb-20">
    <!-- Ambient Background Elements -->
    <div
      class="absolute top-20 right-20 w-[400px] h-[400px] bg-interview-accent-rose/10 rounded-full blur-[100px] -z-10"
    ></div>
    <div
      class="absolute bottom-40 left-10 w-[300px] h-[300px] bg-interview-primary/5 rounded-full blur-[80px] -z-10"
    ></div>

    <!-- Header Section -->
    <div
      class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10 opacity-0 animate-fade-in-up"
    >
      <div>
        <NuxtLink
          to="/hr/dashboard"
          class="inline-flex items-center gap-2 text-interview-text-secondary hover:text-white transition-colors mb-4 group"
        >
          <ArrowLeftIcon class="w-4 h-4 transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </NuxtLink>
        <h1 class="text-4xl md:text-5xl font-black tracking-tight text-white mb-2">
          Interview Reports
        </h1>
        <p class="text-interview-text-secondary text-lg">
          Analyze candidate performance and review results.
        </p>
      </div>

      <!-- Top Level Actions or Summary -->
      <div v-if="statistics" class="flex gap-4">
        <div
          class="px-6 py-3 rounded-2xl bg-interview-surface border border-interview-surface-border backdrop-blur-md"
        >
          <div class="text-xs text-interview-text-secondary uppercase tracking-wider mb-1">
            Pass Rate
          </div>
          <div class="text-2xl font-bold text-interview-success">{{ statistics.pass_rate }}%</div>
        </div>
        <div
          class="px-6 py-3 rounded-2xl bg-interview-surface border border-interview-surface-border backdrop-blur-md"
        >
          <div class="text-xs text-interview-text-secondary uppercase tracking-wider mb-1">
            Avg Score
          </div>
          <div class="text-2xl font-bold text-interview-accent-sky">
            {{ statistics.average_score }}
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Bar (Floating Command Island) -->
    <div class="sticky top-4 z-30 mb-8 opacity-0 animate-fade-in-up" style="animation-delay: 100ms">
      <div
        class="bg-interview-bg-secondary/40 backdrop-blur-xl border border-interview-surface-border rounded-2xl p-2 shadow-xl flex flex-col md:flex-row items-center gap-2"
      >
        <!-- Search -->
        <div class="relative flex-1 w-full md:w-auto">
          <MagnifyingGlassIcon
            class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-interview-text-muted"
          />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search candidates..."
            class="w-full bg-transparent border-none text-white focus:ring-0 pl-10 pr-4 py-2 placeholder-interview-text-muted/50"
          />
        </div>

        <div class="h-8 w-px bg-interview-surface-border hidden md:block"></div>

        <!-- Filters Group -->
        <div class="flex items-center gap-2 w-full md:w-auto overflow-x-auto p-1">
          <select
            v-model="filters.roleId"
            class="bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl text-sm text-interview-text-secondary px-3 py-2 outline-none focus:border-interview-primary focus:text-white transition-colors"
          >
            <option value="" class="bg-interview-surface text-interview-text-primary">
              All Roles
            </option>
            <option
              v-for="role in visibleRoles"
              :key="role.id"
              :value="role.id"
              class="bg-interview-surface text-interview-text-primary"
            >
              {{ role.title }}
            </option>
          </select>

          <select
            v-model="filters.recommendation"
            class="bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl text-sm text-interview-text-secondary px-3 py-2 outline-none focus:border-interview-primary focus:text-white transition-colors"
          >
            <option value="" class="bg-interview-surface text-interview-text-primary">
              Recommendation
            </option>
            <option value="Strong Pass" class="bg-interview-surface text-interview-text-primary">
              Strong Pass
            </option>
            <option value="Pass" class="bg-interview-surface text-interview-text-primary">
              Pass
            </option>
            <option value="Review" class="bg-interview-surface text-interview-text-primary">
              Review
            </option>
            <option value="Fail" class="bg-interview-surface text-interview-text-primary">
              Fail
            </option>
          </select>

          <!-- Clear Button -->
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="p-2 rounded-xl hover:bg-interview-surface-hover text-interview-text-muted hover:text-white transition-colors"
            title="Clear Filters"
          >
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <div class="h-8 w-px bg-interview-surface-border hidden md:block"></div>

        <button
          @click="loadReports"
          class="bg-interview-primary text-interview-bg font-bold px-6 py-2 rounded-xl hover:bg-interview-primary-hover transition-colors shadow-glow-amber w-full md:w-auto"
        >
          Search
        </button>
      </div>
    </div>

    <!-- Reports Data Grid -->
    <!-- Loading State: Skeleton Loader -->
    <div v-if="loading" class="space-y-4">
      <div
        v-for="n in 5"
        :key="n"
        class="bg-interview-surface/50 border border-interview-surface-border/50 rounded-2xl p-4 md:grid md:grid-cols-12 md:gap-4 md:items-center animate-pulse"
      >
        <div class="col-span-3 flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-interview-surface-border"></div>
          <div class="space-y-2">
            <div class="h-4 w-32 bg-interview-surface-border rounded"></div>
            <div class="h-3 w-20 bg-interview-surface-border rounded md:hidden"></div>
          </div>
        </div>
        <div class="col-span-2 hidden md:block">
          <div class="h-4 w-24 bg-interview-surface-border rounded"></div>
        </div>
        <div class="col-span-2 hidden md:block">
          <div class="h-4 w-20 bg-interview-surface-border rounded"></div>
        </div>
        <div class="col-span-2 flex justify-center">
          <div class="h-8 w-16 bg-interview-surface-border rounded-full"></div>
        </div>
        <div class="col-span-2 flex justify-center">
          <div class="h-6 w-20 bg-interview-surface-border rounded"></div>
        </div>
        <div class="col-span-1"></div>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="text-center py-20 text-interview-warning bg-interview-surface/30 rounded-3xl border border-interview-warning/20"
    >
      <ExclamationTriangleIcon class="w-12 h-12 mx-auto mb-4 opacity-50" />
      <p>{{ error }}</p>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="filteredReports.length === 0"
      class="text-center py-20 bg-interview-surface/30 rounded-3xl border border-interview-surface-border"
    >
      <div
        class="bg-interview-bg-secondary w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
      >
        <MagnifyingGlassIcon class="w-8 h-8 text-interview-text-muted" />
      </div>
      <h3 class="text-xl font-bold text-white mb-2">No reports found</h3>
      <p class="text-interview-text-secondary">Try adjusting your filters or search query.</p>
      <button @click="clearFilters" class="mt-6 text-interview-primary hover:underline">
        Clear all filters
      </button>
    </div>

    <!-- Data State -->
    <div v-else class="space-y-4">
      <!-- Table Header (Pseudo-Table) -->
      <div
        class="hidden md:grid grid-cols-12 gap-4 px-6 text-xs font-bold text-interview-text-muted uppercase tracking-wider mb-2 opacity-0 animate-fade-in-up"
        style="animation-delay: 100ms"
      >
        <div
          class="col-span-2 cursor-pointer hover:text-white transition-colors"
          @click="sort('name')"
        >
          Candidate {{ getSortIcon('name') }}
        </div>
        <div
          class="col-span-1 cursor-pointer hover:text-white transition-colors"
          @click="sort('role_id')"
        >
          Role {{ getSortIcon('role_id') }}
        </div>
        <div
          class="col-span-1 cursor-pointer hover:text-white transition-colors"
          @click="sort('interview_date')"
        >
          Date {{ getSortIcon('interview_date') }}
        </div>
        <div
          class="col-span-2 text-center cursor-pointer hover:text-white transition-colors"
          @click="sort('average_score')"
        >
          Avg {{ getSortIcon('average_score') }}
        </div>
        <div
          class="col-span-1 text-center cursor-pointer hover:text-white transition-colors"
          @click="sort('communication_avg')"
        >
          Comm {{ getSortIcon('communication_avg') }}
        </div>
        <div
          class="col-span-1 text-center cursor-pointer hover:text-white transition-colors"
          @click="sort('relevance_avg')"
        >
          Rel {{ getSortIcon('relevance_avg') }}
        </div>
        <div
          class="col-span-1 text-center cursor-pointer hover:text-white transition-colors"
          @click="sort('logical_thinking_avg')"
        >
          Logic {{ getSortIcon('logical_thinking_avg') }}
        </div>
        <div
          class="col-span-2 text-center cursor-pointer hover:text-white transition-colors"
          @click="sort('overall_recommendation')"
        >
          Result {{ getSortIcon('overall_recommendation') }}
        </div>
        <div class="col-span-1 text-right">Actions</div>
      </div>

      <!-- Rows with TransitionGroup -->
      <TransitionGroup name="list" tag="div" class="space-y-4">
        <div
          v-for="(report, index) in sortedReports"
          :key="report.session_id"
          @click="viewReport(report.session_id)"
          class="group relative bg-interview-surface backdrop-blur-sm border border-interview-surface-border rounded-2xl p-4 md:grid md:grid-cols-12 md:gap-4 md:items-center transition-all duration-300 hover:scale-[1.01] hover:bg-interview-surface-hover hover:border-interview-primary/30 hover:shadow-lg cursor-pointer"
          :style="{ transitionDelay: `${index * 50}ms` }"
        >
          <!-- Name -->
          <div class="col-span-2 flex items-center gap-3 mb-2 md:mb-0">
            <div
              class="w-10 h-10 rounded-full bg-gradient-to-br from-interview-bg-secondary to-interview-surface border border-interview-surface-border flex items-center justify-center text-interview-text-primary font-bold shadow-inner flex-shrink-0"
            >
              {{ report.name.charAt(0).toUpperCase() }}
            </div>
            <div class="min-w-0">
              <div
                class="font-bold text-white group-hover:text-interview-primary transition-colors truncate"
              >
                {{ report.name }}
              </div>
              <div class="text-xs text-interview-text-muted md:hidden truncate">
                Applied for {{ formatRoleName(report.role_id) }}
              </div>
            </div>
          </div>

          <!-- Role -->
          <div
            class="col-span-1 text-sm text-interview-text-secondary hidden md:block text-ellipsis overflow-hidden whitespace-nowrap"
          >
            {{ formatRoleName(report.role_id) }}
          </div>

          <!-- Date -->
          <div
            class="col-span-1 text-sm text-interview-text-secondary flex items-center gap-1 hidden md:flex"
          >
            {{ new Date(report.interview_date).toLocaleDateString() }}
          </div>

          <!-- Score -->
          <div class="col-span-2 flex items-center justify-center mt-2 md:mt-0">
            <div
              class="px-3 py-1 rounded-full text-sm font-bold border"
              :class="getScoreBadgeClass(report.average_score)"
            >
              {{ report.average_score ? report.average_score.toFixed(1) : 'N/A' }}
            </div>
          </div>

          <!-- Communication -->
          <div class="col-span-1 flex justify-center items-center mt-2 md:mt-0">
             <div class="text-sm font-semibold text-interview-text-secondary">
               {{ report.communication_avg ? report.communication_avg.toFixed(1) : '-' }}
             </div>
          </div>
          
          <!-- Relevance -->
          <div class="col-span-1 flex justify-center items-center mt-2 md:mt-0">
             <div class="text-sm font-semibold text-interview-text-secondary">
               {{ report.relevance_avg ? report.relevance_avg.toFixed(1) : '-' }}
             </div>
          </div>

          <!-- Logical Thinking -->
          <div class="col-span-1 flex justify-center items-center mt-2 md:mt-0">
             <div class="text-sm font-semibold text-interview-text-secondary">
               {{ report.logical_thinking_avg ? report.logical_thinking_avg.toFixed(1) : '-' }}
             </div>
          </div>

          <!-- Recommendation -->
          <div class="col-span-2 flex justify-center mt-2 md:mt-0">
            <span
              class="text-xs font-bold px-2 py-1 rounded uppercase tracking-wide border border-transparent"
              :class="getRecTextClass(report.overall_recommendation)"
            >
              {{ report.overall_recommendation || 'PENDING' }}
            </span>
          </div>

          <!-- Actions -->
          <div
            class="col-span-1 flex justify-end gap-2 mt-4 md:mt-0 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <button
              @click.stop="downloadReport(report.session_id)"
              class="p-2 rounded-xl hover:bg-interview-bg hover:text-interview-success transition-all text-interview-text-muted hover:scale-110 active:scale-95"
              title="Download PDF"
            >
              <ArrowDownTrayIcon class="w-5 h-5" />
            </button>
            <button
              @click.stop="viewReport(report.session_id)"
              class="p-2 rounded-xl bg-interview-bg-secondary text-interview-text-primary border border-interview-surface-border hover:border-interview-primary hover:text-interview-primary transition-all hover:scale-110 active:scale-95"
              title="View Details"
            >
              <ChevronRightIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  UsersIcon,
  ChartBarIcon,
  CheckCircleIcon,
  EyeIcon,
  ArrowDownTrayIcon,
  ArrowLeftIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  XMarkIcon,
  CalendarIcon,
  ChevronRightIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

definePageMeta({
  layout: 'hr',
  middleware: ['hr'],
})

const { getAllReports, getStatistics, downloadPDF } = useReports()
const { getRoles } = useHR()
const router = useRouter()

const statistics = ref<any>(null)
const reports = ref<any[]>([])
const roles = ref<any[]>([])
const loading = ref(true)
const error = ref('')

const filters = reactive({
  roleId: '',
  minScore: undefined as number | undefined,
  recommendation: '',
})

const searchQuery = ref('')
const sortKey = ref('average_score') // Default to highest score first
const sortOrder = ref<'asc' | 'desc'>('desc')
const appliedRoleId = ref('')

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

    // Update applied role ID when applying filters
    appliedRoleId.value = filters.roleId

    const filterParams: any = {}
    if (filters.roleId) filterParams.roleId = filters.roleId
    if (filters.minScore !== undefined) filterParams.minScore = filters.minScore
    if (filters.recommendation) filterParams.recommendation = filters.recommendation
    if (searchQuery.value) filterParams.searchQuery = searchQuery.value

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

const hasActiveFilters = computed(() => {
  return filters.roleId || filters.recommendation || searchQuery.value
})

const visibleRoles = computed(() => {
  return roles.value.filter((role: any) => !role.title.includes('(Candidate'))
})

const filteredReports = computed(() => {
  // Client-side filtering is no longer needed as backend handles it along with search.
  // We just return the reports from backend.
  return reports.value
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
    sortOrder.value = 'desc' // Default to desc for new sort
  }
}

const getSortIcon = (key: string) => {
  if (sortKey.value !== key) return ''
  return sortOrder.value === 'asc' ? '↑' : '↓'
}

const formatRoleName = (roleId: string) => {
  const role = roles.value.find(r => r.id === roleId)
  if (role) {
    return role.title.replace(/\s*\(Candidate.*\)/, '')
  }
  return roleId
}

// New Visual Style Helpers
const getScoreBadgeClass = (score: number | null) => {
  if (score === null)
    return 'bg-interview-surface border-interview-surface-border text-interview-text-muted'
  if (score >= 4)
    return 'bg-interview-success/10 border-interview-success/30 text-interview-success shadow-[0_0_10px_rgba(34,197,94,0.2)]'
  if (score >= 3) return 'bg-interview-info/10 border-interview-info/30 text-interview-info'
  if (score >= 2)
    return 'bg-interview-warning/10 border-interview-warning/30 text-interview-warning'
  return 'bg-red-500/10 border-red-500/30 text-red-500'
}

const getRecTextClass = (rec: string | null) => {
  if (!rec) return 'text-interview-text-muted'
  if (rec === 'Strong Pass') return 'text-interview-success'
  if (rec === 'Pass') return 'text-interview-info'
  if (rec === 'Review') return 'text-interview-warning'
  return 'text-red-500'
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
/* Minimal override for select dropdown chevron color if needed, majority is tailwind */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23a1a1aa' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.list-move {
  transition: transform 0.4s ease;
}
</style>
