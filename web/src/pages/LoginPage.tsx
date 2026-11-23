import { useState, type FormEvent } from 'react'
import { replace, useLoaderData, type LoaderFunctionArgs } from 'react-router-dom'
import { writePref } from '../theme'
import { Picker, usePickerShortcut } from '../components/Picker'
import { api } from '../api'

export async function loginLoader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url)
  const next = url.searchParams.get('next') ?? '/'
  // 只允许回到本站页面，保留题目查询参数和单元锚点。
  let target = new URL('/', url)
  if (next.startsWith('/') && !next.startsWith('//') && !/[\\\u0000-\u001f]/.test(next)) {
    const parsed = new URL(next, url)
    if (parsed.origin === url.origin && !parsed.pathname.startsWith('//') && !/^\/login\/*$/i.test(parsed.pathname)) {
      target = parsed
    }
  }
  const path = target.pathname + target.search + target.hash
  if ((await api.session()).authenticated) throw replace(path)
  return path
}

export function LoginPage() {
  const next = useLoaderData<typeof loginLoader>()
  const [error, setError] = useState('')
  const [quick, setQuick] = useState(false)
  usePickerShortcut(false, () => { writePref('dojo-search-after-login', '1'); setQuick(true) })
  const [pending, setPending] = useState(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (pending) return
    const field = event.currentTarget.elements.namedItem('password') as HTMLInputElement
    setPending(true)
    setError('')
    try {
      await api.login(field.value)
      window.location.replace(next)
    } catch (err) {
      setError((err as Error).message)
      setPending(false)
      field.focus()
      field.select()
    }
  }

  return <div className="shell">
    <header className="topbar"><span className="wordmark">code-dojo</span></header>
    {quick && <Picker label="快速打开" items={[]} message="请先登录，登录后可搜索题库。"
      close={() => { setQuick(false); document.getElementById('password')?.focus() }} />}
    <main className="track login-page">
      <h1>登录</h1>
      <form onSubmit={submit} method="post">
        <label htmlFor="password">密码</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required autoFocus />
        {error && <p className="tone-fail" role="alert">{error}</p>}
        <button className="primary" disabled={pending}>{pending ? '登录中…' : '登录'}</button>
      </form>
    </main>
  </div>
}
