import { useState } from 'react'
import { Link, useLoaderData, useOutletContext } from 'react-router-dom'
import { api, type ProjectDetail, type ProjectEvent, type ProjectResult } from '../api'
import { CodeEditor } from '../components/CodeEditor'
import { ProblemStatus, STATUS_NAME } from '../components/ProblemStatus'
import { runProject } from '../sql/client'
import type { Theme } from '../theme'
import './project.css'

async function readLog(response: Response, receive: (event: ProjectEvent) => void) {
  const reader = response.body!.pipeThrough(new TextDecoderStream()).getReader()
  let pending = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    const lines = (pending + value).split('\n')
    pending = lines.pop()!
    for (const line of lines) receive(JSON.parse(line) as ProjectEvent)
  }
}

function Project({ initial }: { initial: ProjectDetail }) {
  const theme = useOutletContext<Theme>()
  const [project, setProject] = useState(initial)
  const [busy, setBusy] = useState(false)
  const [logs, setLogs] = useState<string[]>([])
  const [result, setResult] = useState<ProjectResult | null>(null)
  const [error, setError] = useState('')
  const python = project.language === 'python'
  const solved = project.parts.filter(p => p.status === 'solved' || p.status === 'assisted').length
  const addLine = (line: string) => setLogs(previous => [...previous, line])

  async function assemble() {
    setBusy(true)
    setError('')
    try {
      setProject(await api.project(project.id))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setBusy(false)
    }
  }

  async function run() {
    setBusy(true)
    setError('')
    setLogs([])
    setResult(null)
    function finish(outcome: ProjectResult) {
      setResult(outcome)
      if (outcome.verdict === 'accepted') setProject(p => ({ ...p, completed: true }))
    }
    try {
      const response = await api.runProject(project.id)
      if (python) {
        await readLog(response, event => 'line' in event ? addLine(event.line) : finish(event.result))
      } else {
        const checks = await runProject(await response.json())
        for (const check of checks) addLine(check.label + ' · ' + (check.difference?.message ?? '通过'))
        const passed = checks.map(c => !c.difference)
        addLine(`检查通过 ${passed.filter(Boolean).length} / ${passed.length}`)
        finish(await api.projectChecks(project.id, passed))
      }
    } catch (e) {
      finish({ verdict: 'runtime_error', error: (e as Error).message })
    } finally {
      setBusy(false)
    }
  }

  return <main className="project-page">
    <Link className="faint" to={'/t/' + project.track}>← 学习线题目</Link>
    <h1>{project.title}</h1>
    <p>{project.summary}</p>
    <div className="project-columns">
      <section className="project-parts" aria-label="项目部分">
        <h2>项目部分 <small>{solved} / {project.parts.length}</small></h2>
        <ol>{project.parts.map(part => <li key={part.id}>
          <Link to={'/p/' + part.id}><span>{part.title}</span>
            <small><ProblemStatus status={part.status} /> {part.status ? STATUS_NAME[part.status] : '未提交'}</small>
          </Link></li>)}</ol>
        <h2>完成条件</h2>
        {project.success === 'all_checks' ? <p>通过全部项目检查</p> :
          Object.entries(project.success).map(([name, rules]) =>
            <p key={name}><code>{Object.entries(rules).map(([op, n]) => `${name} ${op} ${n}`).join('，')}</code></p>)}
        <p className="faint">运行时限 {project.timeout} 秒</p>
        {project.completed && <p className="tone-pass">已完成项目</p>}
      </section>
      <section className="project-script" aria-label="拼装脚本">
        <div className="project-bar"><h2>{project.id}.{python ? 'py' : 'sql'}</h2>
          <button className="ghost" onClick={assemble} disabled={busy}>拼起来</button>
          <a download href={`/api/projects/${project.id}/data`}>下载数据</a>
          {(python ? ['py', 'ipynb'] : ['sql']).map(ext => <a key={ext} download
            href={`/api/projects/${project.id}/export/${ext}`}>导出 .{ext}</a>)}
        </div>
        <div className="project-preview"><CodeEditor value={project.code} onChange={() => {}}
          bare readOnly theme={theme} language={python ? 'python' : 'pgsql'} /></div>
        <div className="project-bar"><h2>运行日志</h2>
          <button className="primary" disabled={busy || solved !== project.parts.length} onClick={run}>
            完整跑一遍</button>
        </div>
        <div className="project-output" aria-live="polite">
          {busy && <span className="faint">处理中…</span>}
          {logs.length > 0 && <pre>{logs.join('\n')}</pre>}
          {result && <p className={result.verdict === 'accepted' ? 'tone-pass' : 'tone-fail'}>
            {result.verdict === 'accepted' ? '已达标' : '未达标'}{result.error && ' · ' + result.error}</p>}
          {error && <p className="tone-fail" role="alert">{error}</p>}
        </div>
      </section>
    </div>
  </main>
}

export default function ProjectPage() {
  const initial = useLoaderData() as ProjectDetail
  return <Project key={initial.id} initial={initial} />
}
