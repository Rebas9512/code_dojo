import { lazy, Suspense, useEffect, useState } from 'react'
import {
  createBrowserRouter, Link, Navigate, NavLink, Outlet, RouterProvider,
  useLoaderData, useMatches, useNavigation, useParams, useRouteError,
} from 'react-router-dom'
import { api, invalidate, loadWorkspace, trackRows, type WorkspaceData } from './api'
import { TodayPage, StatsPage } from './pages/PlanPages'
import { LoginPage, loginLoader } from './pages/LoginPage'
import { MapPage } from './pages/MapPage'
import { SessionPage } from './pages/SessionPage'
import { TrackPage } from './pages/TrackPage'
import { readPref, writePref, useTheme } from './theme'
import { useTracks } from './tracks'
import { DesktopBridge } from './components/DesktopBridge'
import { SyncStatus } from './components/SyncStatus'

import { QuickOpen, usePickerShortcut } from './components/Picker'

// 做题页带 Monaco，单独打包。知识点页带 Markdown（约 160 KB），也不放进首页的包。
const ProblemPage = lazy(() => import('./pages/ProblemPage').then((m) => ({ default: m.ProblemPage })))
const SkillsPage = lazy(() => import('./pages/SkillsPage').then((m) => ({ default: m.SkillsPage })))

// 页面画好后趁空闲先载入做题页和 Monaco（约 4 MB，执行约 0.3 秒），第一次点开题目不用再等。
// Safari 没有 requestIdleCallback，改为稍等一会儿。
let warmed = false
function warmEditor() {
  if (warmed) return
  warmed = true
  const idle = window.requestIdleCallback ?? ((run: () => void) => window.setTimeout(run, 1000))
  idle(() => {
    void import('./pages/ProblemPage')
    void import('./components/CodeEditor')
  }, { timeout: 3000 })
}

function Shell() {
  const { session } = useLoaderData<typeof loadMap>()
  const [logoutError, setLogoutError] = useState('')
  const tracks = useTracks()
  const [quick, setQuick] = useState(() => readPref('dojo-search-after-login', '') === '1')
  function closeQuick() {
    writePref('dojo-search-after-login', null)
    setQuick(false)
  }
  usePickerShortcut(false, () => setQuick(true))
  useEffect(warmEditor, [])
  const { track } = useParams()
  const problem = useMatches().find((m) => m.id === 'problem')?.data as WorkspaceData | undefined
  const current = tracks.find((t) => t.id === (problem?.parent.track ?? track))
  const [theme, toggleTheme] = useTheme()
  const navigating = useNavigation().state !== 'idle'
  const themeLabel = theme === 'dark' ? '切到浅色' : '切到深色'
  async function logout() {
    try {
      await api.logout()
      window.location.replace('/login')
    } catch (error) {
      setLogoutError((error as Error).message)
    }
  }
  return (
    <div className="shell">
      {navigating && <div className="nav-progress" aria-hidden="true" />}
      <header className={problem ? "topbar wb-titlebar" : "topbar"}>
        <Link to="/" className="wordmark">code-dojo</Link>
        {current && !problem && <>
          <span className="current-track">{current.name}</span>
          <nav className="tracks" aria-label="学习线视图">
            <NavLink end to={`/t/${current.id}`} className={({ isActive }) => isActive || problem ? 'active' : ''}>题目</NavLink>
            <NavLink to={`/t/${current.id}/skills`}>知识点</NavLink>
          </nav>
        </>}
        <span className="bar-spacer" />
        <nav className="tracks plan-nav" aria-label="练习计划">
          <NavLink to="/today">今日计划</NavLink><NavLink to="/stats">手感统计</NavLink>
        </nav>
        {!problem && <><SyncStatus /><DesktopBridge /></>}
        {problem && <button className="quick-trigger" onClick={() => setQuick(true)} title="快速打开（Ctrl+P）">
          <span aria-hidden="true" className="codicon codicon-search" /> 快速打开题目 <kbd>Ctrl P</kbd></button>}
        <button className="ghost theme-toggle" onClick={toggleTheme} title={themeLabel} aria-label={themeLabel}>
          {theme === 'dark' ? '☀' : '☾'}
        </button>
        {session.enabled && <button className="ghost logout" onClick={logout}>退出</button>}
      </header>
      {quick && <QuickOpen tracks={tracks} close={closeQuick} />}
      {logoutError && <p className="tone-fail" role="alert">{logoutError}</p>}
      <Suspense fallback={<main />}><Outlet context={theme} /></Suspense>
    </div>
  )
}

function RouteError() {
  const error = useRouteError()
  return <main className="track"><p role="alert">{error instanceof Error ? error.message : '页面加载失败'}</p>
    <Link to="/">返回学习地图</Link></main>
}

async function loadMap() {
  const [tracks, session] = await Promise.all([api.tracks(), api.session()])
  return { tracks, session }
}

const router = createBrowserRouter([{
  path: '/login', loader: loginLoader, element: <LoginPage />, errorElement: <RouteError />,
  hydrateFallbackElement: <main />,
}, {
  id: 'map', path: '/', loader: loadMap, element: <Shell />, errorElement: <RouteError />,
  // 只运行样例也会改变最近练习的线，返回地图时读取最新进度。
  shouldRevalidate: ({ currentUrl, nextUrl, defaultShouldRevalidate }) =>
    defaultShouldRevalidate || (nextUrl.pathname === '/' && currentUrl.pathname !== '/'),
  hydrateFallbackElement: <main />,
  children: [
    { index: true, element: <MapPage /> },
    { path: 'session', element: <SessionPage /> },
    { path: 'today', loader: api.today, element: <TodayPage />, errorElement: <RouteError /> },
    { path: 'stats', loader: api.stats, element: <StatsPage />, errorElement: <RouteError /> },
    { path: 'sql', element: <Navigate to="/t/sql" replace /> },
    {
      path: 't/:track', element: <TrackPage />, errorElement: <RouteError />,
      loader: ({ params }) => Promise.all([trackRows(params.track!), api.skills(params.track!), api.status()]),
    },
    {
      path: 't/:track/skills', element: <SkillsPage />, errorElement: <RouteError />,
      loader: ({ params }) => api.skills(params.track!),
    },
    {
      id: 'problem', path: 'p/:id', element: <ProblemPage />, errorElement: <RouteError />,
      loader: ({ params }) => loadWorkspace(params.id!),
    },
  ],
}])

window.addEventListener('dojo-login-required', () => {
  const { pathname, search, hash } = router.state.navigation.location ?? window.location
  window.location.replace('/login?' + new URLSearchParams({ next: pathname + search + hash }))
})

window.addEventListener('pageshow', (event) => {
  if (!event.persisted) return
  invalidate()
  void router.revalidate()
})

export function App() {
  return <RouterProvider router={router} />
}
