import { readPref } from './theme'
import type { SqlTable, Difference, SqlCheck, CheckValue } from './sql/compare'

// 和后端 server/app/main.py 对应的类型与请求

export type Track = string
export type Language = 'python' | 'sql' | 'none'

export interface PracticeLink {
  id: string
  title: string
  parent?: string
  source?: string
  due?: string
  step?: number
  rewrite?: boolean
  generate?: boolean
}

export function practicePath(item: PracticeLink) {
  const params = new URLSearchParams()
  if (item.source && item.due) {
    params.set('review', item.source)
    params.set('due', item.due)
  }
  if (item.parent) params.set('extra', item.id)
  if (item.generate) params.set('variant', '1')
  return '/p/' + encodeURIComponent(item.parent ?? item.id) + (params.size ? '?' + params : '')
}

export interface TodayPlan {
  date: string
  daily_limit: number
  first_rate: number | null
  first_count: number
  reviews: PracticeLink[]
  tracks: { id: string; name: string; next: PracticeLink | null }[]
}

export interface Week {
  week: string
  first_rate: number | null
  syntax_errors: number
  elapsed_ms: number | null
  hints: number
  ai_rate: number | null
}

export interface ReviewContext { review_source?: string; review_due?: string }

export interface MapUnit {
  project?: string
  id: string
  name: string
  total: number
  solved: number
  assisted: number
  attempted: number
  skills: { id: string; name: string; status: Status }[]
  mastered: number
  next: PracticeLink | null
}

export interface TrackStage {
  kind?: 'project'
  id: string
  name: string
  total: number
  solved: number
  units: MapUnit[]
}

export interface TrackInfo {
  id: Track
  name: string
  summary: string
  order: number
  language: Language
  runtime: 'python' | 'pglite' | 'ds' | 'none'
  status: 'active' | 'planned'
  requires: Track[]
  requires_done: boolean
  stages: TrackStage[]
  total: number
  solved: number
  assisted: number
  attempted: number
  skills: number
  mastered: number
  next: PracticeLink | null
  frontier: PracticeLink | null
  last_active: string | null
}
export type Format = 'predict' | 'complete' | 'fix' | 'write' | 'variant' | 'combine' | 'inspect'
export type Mode = 'function' | 'class' | 'stdio' | 'predict' | 'inspect' | 'dml' | 'script' | null
export type Status = 'solved' | 'assisted' | 'attempted' | null

export interface SkillRef {
  requires: string[]
  introduces: string | null
}

export interface ProblemSummary {
  id: string
  title: string
  track: Track
  stage: string
  order: number
  week?: number | null
  format: Format
  mode: Mode
  difficulty: number
  skills: SkillRef
  milestones: string[]
  leetcode: string | null
  optional: boolean
  status: Status
}

export interface TrackProblem extends ProblemSummary {
  unit: string
}

export interface SkillCard {
  id: string
  name: string
  card: string
  new: boolean
}

export interface ItemRef {
  kind: 'lesson' | 'problem'
  id: string
  title: string
}

export function itemPath(ref: { kind: 'lesson' | 'problem'; id: string }): string {
  return ref.kind === 'lesson' ? `/l/${ref.id}` : `/p/${ref.id}`
}

export interface DataBlock {
  kind: 'table' | 'csv' | 'json' | 'schema' | 'values'
  title: string
  content: string
  columns?: { name: string; type: string; nullable: boolean; primary_key: boolean }[]
}

export type LessonStep =
  | { type: 'read'; skill: string; md: string }
  | { type: 'example'; skill: string; code: string; md?: string; stdin?: string; db?: string; patch?: string; setup?: string[] }
  | { type: 'example'; skill: string; data: DataBlock; md?: string }
  | { type: 'quiz'; skill: string; q: string; options: string[]; answer: number; explain?: string }

/** 一道题的"课"里的一段：一个技能的教学内容（new = 本题新引入的技能） */
export interface LessonSection {
  skill: string
  name: string
  card: string
  new: boolean
  lesson: string | null
  steps: LessonStep[]
}

/** 附加题（AI 照着原题出、验证过的相似题）。id 形如 x-12 */
export interface ExtraSummary {
  id: string
  seq: number
  title: string | null
  status: 'generating' | 'ready' | 'failed'
  error: string | null
  request: string
  practice_skill: string | null
  created_at: string
}

export interface PlaygroundResult {
  status: 'ok' | 'runtime_error' | 'timeout' | 'compile_error' | 'system_error'
  stdout: string
  error: string | null
  time_ms: number
}

export interface StandardAnswer {
  code: string
  language: 'python' | 'sql'
  notes_md: string
  advanced_md: string
  has_notes: boolean
}

export interface ProjectDetail {
  id: string
  track: string
  title: string
  summary: string
  language: 'python' | 'sql'
  timeout: number
  success: Record<string, Record<string, number>> | 'all_checks'
  parts: { id: string; title: string; status: Status }[]
  code: string
  completed: boolean
}

export interface ProjectResult {
  verdict: string
  metrics?: Record<string, number>
  error?: string
}

export type ProjectEvent = { line: string } | { result: ProjectResult }
export interface ProblemDetail extends ProblemSummary {
  project?: { id: string; part: number; total: number; others: ItemRef[] }
  language: Language
  statement: string
  starter: string
  signature: string | null
  entry: string | null
  hints: string[]
  examples: Record<string, unknown>[]
  skill_cards: SkillCard[]
  stuck: { skill: string; target_id: string; target: string; root: boolean; problem: PracticeLink | null } | null
  continue_with: PracticeLink | null
  prev: ItemRef | null
  next: ItemRef | null
  has_lesson: boolean
  parent: string | null
  extra_seq: number | null
  data?: DataBlock[]
  answer?: { type: 'choice'; options: string[] } | { type: 'short' }
  program?: string
  datasets?: string[]
}

export interface Skill {
  id: string
  name: string
  stage: string
  prereqs: { id: string; name: string; track: Track }[]
  lesson: { id: string; title: string } | null
  problems: Pick<ProblemSummary, 'id' | 'title' | 'format' | 'status'>[]
  state: 'unlearned' | 'learning' | 'mastered' | 'review'
  counted_solves: number
  last_used: string | null
  used_by: number
  card: string
  group: number | null
}

export type CaseStatus = 'passed' | 'wrong_answer' | 'runtime_error' | 'timeout' | 'skipped'
export type Verdict = 'accepted' | 'compile_error' | 'constraint_error' | 'system_error' | CaseStatus

type SqlDataset<T> = { setup: string[]; hidden: boolean; expected: T }
type SqlPlan = { mode: 'script'; cte?: string; checks: SqlCheck[]; datasets: SqlDataset<{ checks: CheckValue[] }>[] } |
  { mode?: 'dml'; check_query?: string; ordered: boolean; tolerance: number; datasets: SqlDataset<SqlTable>[] }

export interface FullCaseResult {
  affected_rows?: number
  difference?: Difference
  status: CaseStatus
  input: Record<string, unknown>
  expected: unknown
  actual: unknown
  error: string | null
  stdout: string
  time_ms: number
  preview?: false
  hidden?: boolean
}

export type CaseResult = FullCaseResult | (Omit<FullCaseResult, 'preview' | 'input' | 'difference'> & {
  preview: true
  input?: Record<string, unknown> | string
  difference?: Difference | string
})

export interface JudgeResult {
  verdict: Verdict
  passed?: number
  total?: number
  error?: string
  cases: CaseResult[]
  explain?: string
  misconception?: { id: string; name: string; line: string }
  submission_id?: number
}

export type AgentId = 'claude' | 'codex'

export interface Agent {
  id: AgentId
  name: string
  model: string
}

export function preferredAgent(agents: Agent[]) {
  const saved = readPref('dojo-ai-agent', '')
  return agents.find(agent => agent.id === saved) ?? agents[0]
}

export interface ServerStatus {
  judge_mode: 'local' | 'docker'
  judge_backends: { python: 'local' | 'docker'; ds: 'local' | 'docker' }
  ok: boolean
  problems: number
  load_errors: { path: string; message: string }[]
  judge_image_present: boolean | null
  ai: AgentId | 'off'
  ai_agents: Agent[]
  ai_model: string | null
}

export interface Session { enabled: boolean; authenticated: boolean }

export interface SyncState {
  enabled: boolean
  last_sync: string | null
  pending: number
  error: string
  syncing: boolean
}

// 读接口的短期缓存：切题时直接用预取的结果。任何写请求完成后，已有缓存全部作废。
let generation = 0
const cache = new Map<string, { generation: number; at: number; value: Promise<unknown> }>()

export function invalidate() {
  generation++
}

function cached<T>(key: string, load: () => Promise<T>, ttl = 60_000): Promise<T> {
  const hit = cache.get(key)
  if (hit && hit.generation === generation && Date.now() - hit.at < ttl) return hit.value as Promise<T>
  const value = load()
  cache.set(key, { generation, at: Date.now(), value })
  value.catch(() => { if (cache.get(key)?.value === value) cache.delete(key) })  // 失败的请求不留在缓存里
  return value
}

async function response(path: string, init?: RequestInit) {
  const res = await fetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
  })
  if (init?.method) generation++
  if (!res.ok) {
    if (res.status === 401 && path !== '/api/auth/login') {
      window.dispatchEvent(new Event('dojo-login-required'))
    }
    let detail = `${res.status}`
    try {
      const body = await res.json()
      detail = body.detail ?? detail
    } catch {
      /* 非 JSON 错误体 */
    }
    throw new Error(detail)
  }
  return res
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  return (await response(path, init)).json() as Promise<T>
}

export const api = {
  project: (id: string) => request<ProjectDetail>(`/api/projects/${id}`),
  runProject: (id: string) => response(`/api/projects/${id}/run`, { method: 'POST', body: '{}' }),
  projectChecks: (id: string, passed: boolean[]) => request<ProjectResult>(`/api/projects/${id}/sql-result`, {
    method: 'POST', body: JSON.stringify({ passed }),
  }),
  syncStatus: () => request<SyncState>('/api/sync'),
  syncNow: () => request<SyncState>('/api/sync', { method: 'POST', body: '{}' }),
  session: () => request<Session>('/api/auth/session'),
  login: (password: string) => request('/api/auth/login', {
    method: 'POST', body: JSON.stringify({ password }),
  }),
  logout: () => request('/api/auth/logout', { method: 'POST', body: '{}' }),
  today: () => request<TodayPlan>('/api/today'),
  sessionPlan: (tab: 'python' | 'sql', size: number, warmup: boolean) =>
    request<PracticeLink[]>(`/api/session-plan?tab=${tab}&size=${size}&warmup=${warmup}`),
  stats: () => request<{ weeks: Week[] }>('/api/stats'),
  dailyLimit: (daily_limit: number) => request('/api/today/settings', {
    method: 'PUT', body: JSON.stringify({ daily_limit }),
  }),
  hint: (id: string, number: number, review: ReviewContext) => request(`/api/problems/${id}/hints/${number}`, {
    method: 'POST', body: JSON.stringify(review),
  }),
  standard: (id: string) => request<StandardAnswer>(`/api/problems/${encodeURIComponent(id)}/standard`),
  solution: (id: string, review: ReviewContext) => request<{ solution: string }>(`/api/problems/${id}/solution`, {
    method: 'POST', body: JSON.stringify(review),
  }),
  tracks: () => request<TrackInfo[]>('/api/tracks'),
  status: () => request<ServerStatus>('/api/status'),
  judgeStatus: () => request<{ ds_state: 'docker' | 'unprepared' | 'preparing' | 'ready' }>('/api/judge/status'),
  problems: (track: Track) => request<TrackProblem[]>(`/api/tracks/${track}/problems`),
  skills: (track: Track) => request<Skill[]>(`/api/tracks/${track}/skills`),
  problem: (id: string) => request<ProblemDetail>(`/api/problems/${encodeURIComponent(id)}`),
  sqlCases: (id: string, scope: 'sample' | 'all') =>
    request<SqlPlan>(
      `/api/problems/${encodeURIComponent(id)}/sql-cases?scope=${scope}`),
  bookstoreSetup: () => cached('bookstore-setup', () => request<string[]>('/api/playground/bookstore')),
  run: (id: string, body: JudgeRequest) =>
    request<JudgeResult>(`/api/problems/${encodeURIComponent(id)}/run`, { method: 'POST', body: JSON.stringify(body) }),
  submit: (id: string, body: JudgeRequest) =>
    request<JudgeResult>(`/api/problems/${encodeURIComponent(id)}/submit`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  problemLesson: (id: string) =>
    request<{ sections: LessonSection[] }>(`/api/problems/${encodeURIComponent(id)}/lesson`),
  playground: (code: string, stdin = '', problemId?: string) =>
    request<PlaygroundResult>('/api/playground/run', { method: 'POST', body: JSON.stringify({ code, stdin, problem_id: problemId }) }),
  chat: (id: string) => request<ChatMessage[]>(`/api/problems/${encodeURIComponent(id)}/chat`),
  extras: (id: string) => request<ExtraSummary[]>(`/api/problems/${encodeURIComponent(id)}/extras`),
  createExtra: async (id: string, req = '', practice_skill?: string, review: ReviewContext = {}) =>
    request<ExtraSummary>(`/api/problems/${encodeURIComponent(id)}/extras`, {
      method: 'POST',
      body: JSON.stringify({ request: req, practice_skill, ...review, agent: await requestAgent() }),
    }),
  deleteExtra: (id: string, seq: number) =>
    request<{ ok: boolean }>(`/api/problems/${encodeURIComponent(id)}/extras/${seq}`, { method: 'DELETE' }),
  chatSend: async (id: string, body: ReviewContext & { message: string; code?: string; scratch: string; answer?: string | null; current?: string }) =>
    request<{ user: ChatMessage; assistant: ChatMessage; new_extra: ExtraSummary | null; deleted_extras: number[] }>(
      `/api/problems/${encodeURIComponent(id)}/chat`,
      {
        method: 'POST',
        body: JSON.stringify({ ...body, agent: await requestAgent() }),
      },
    ),
  chatApplied: (id: string, messageId: number) =>
    request<{ ok: boolean }>(`/api/problems/${encodeURIComponent(id)}/chat/${messageId}/applied`, { method: 'POST' }),
  chatClear: (id: string) =>
    request<{ ok: boolean }>(`/api/problems/${encodeURIComponent(id)}/chat`, { method: 'DELETE' }),
}

export interface TutorEdit {
  target: 'answer' | 'scratch'
  old: string
  new: string
  why: string
}

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  agent: AgentId | null
  content: string
  edits: TutorEdit[]
  applied: boolean
  created_at: string
}

export interface JudgeRequest extends ReviewContext {
  sql_result?: JudgeResult
  code?: string
  answer?: string
  elapsed_ms?: number
  hints_used?: number
  ai_lines?: number
}

export const problemDetail = (id: string) => cached('problem:' + id, () => api.problem(id))
export const trackRows = (track: Track) => cached('rows:' + track, () => api.problems(track))

// 做题页和助教共用页面会话的状态快照，刷新后重新探测。
let status: Promise<ServerStatus> | undefined
export const serverStatus = (): Promise<ServerStatus> => status ??= api.status().catch((e) => { status = undefined; throw e })

async function requestAgent() {
  return preferredAgent((await serverStatus()).ai_agents)?.id
}

export async function loadWorkspace(id: string) {
  const parent = await problemDetail(id)
  // 同一学习线里切题时，题目列表、今日计划和判题状态都来自缓存，只等题目详情。
  const [rows, plan, server] = await Promise.all([trackRows(parent.track), cached('today', api.today), serverStatus()])
  return { parent, rows, reviews: plan.reviews, status: server }
}

/** 预取一道题的详情和所在学习线的列表，点过去时路由不用再等网络。失败不用管，真正打开时会重试并报错。 */
export function prefetchProblem(id: string) {
  problemDetail(id).then(p => trackRows(p.track)).catch(() => {})
}
export type WorkspaceData = Awaited<ReturnType<typeof loadWorkspace>>
