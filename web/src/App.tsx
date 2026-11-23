import { lazy, Suspense, useState } from 'react'
import {
  createBrowserRouter, Link, Navigate, NavLink, Outlet, RouterProvider,
  useLoaderData, useMatches, useParams, useRouteError,
} from 'react-router-dom'
import { api, type ProblemDetail } from './api'
import { TodayPage, StatsPage } from './pages/PlanPages'
import { LoginPage, loginLoader } from './pages/LoginPage'
import { MapPage } from './pages/MapPage'
import { SkillsPage } from './pages/SkillsPage'
import { TrackPage } from './pages/TrackPage'
import { useTheme } from './theme'
import { useTracks } from './tracks'
import { SyncStatus } from './components/SyncStatus'

// 做题页带 Monaco，单独打包。
const ProblemPage = lazy(() => import('./pages/ProblemPage').then((m) => ({ default: m.ProblemPage })))

function Shell() {
  const { session } = useLoaderData<typeof loadMap>()
  const [logoutError, setLogoutError] = useState('')
  const tracks = useTracks()
  const { track } = useParams()
  const problem = useMatches().find((m) => m.id === 'problem')?.data as ProblemDetail | undefined
  const current = tracks.find((t) => t.id === (problem?.track ?? track))
  const [theme, toggleTheme] = useTheme()
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
      <header className="topbar">
        <Link to="/" className="wordmark">code-dojo</Link>
        {current && <>
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
        <SyncStatus />
        <button className="ghost theme-toggle" onClick={toggleTheme} title={themeLabel} aria-label={themeLabel}>
          {theme === 'dark' ? '☀' : '☾'}
        </button>
        {session.enabled && <button className="ghost logout" onClick={logout}>退出</button>}
      </header>
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
  hydrateFallbackElement: <main />,
  children: [
    { index: true, element: <MapPage /> },
    { path: 'today', loader: api.today, element: <TodayPage />, errorElement: <RouteError /> },
    { path: 'stats', loader: api.stats, element: <StatsPage />, errorElement: <RouteError /> },
    { path: 'sql', element: <Navigate to="/t/sql" replace /> },
    {
      path: 't/:track', element: <TrackPage />, errorElement: <RouteError />,
      loader: ({ params }) => Promise.all([api.problems(params.track!), api.skills(params.track!), api.status()]),
    },
    {
      path: 't/:track/skills', element: <SkillsPage />, errorElement: <RouteError />,
      loader: ({ params }) => api.skills(params.track!),
    },
    {
      id: 'problem', path: 'p/:id', element: <ProblemPage />, errorElement: <RouteError />,
      loader: ({ params }) => api.problem(params.id!),
    },
  ],
}])

window.addEventListener('dojo-login-required', () => {
  const { pathname, search, hash } = router.state.navigation.location ?? window.location
  window.location.replace('/login?' + new URLSearchParams({ next: pathname + search + hash }))
})

window.addEventListener('pageshow', (event) => {
  if (event.persisted) void router.revalidate()
})

export function App() {
  return <RouterProvider router={router} />
}
