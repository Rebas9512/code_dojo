import {
  forwardRef,
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useImperativeHandle,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { Link, useNavigate, useRevalidator, useSearchParams } from 'react-router-dom'
import {
  api,
  itemPath,
  practicePath,
  type ReviewContext,
  type ExtraSummary,
  type ItemRef,
  type JudgeResult,
  type JudgeRequest,
  type ProblemDetail,
  type TutorEdit,
} from '../api'
import { variantRequest } from '../pages/PlanPages'
import { FORMAT_NAME } from '../labels'
import { readPref, writePref, type Theme } from '../theme'
import { useTracks } from '../tracks'
import { DsPreparation } from './DsPreparation'
import { ChatPanel, type ApplyResult } from './ChatPanel'
import type { CodeEditorHandle } from './CodeEditor'
import { CodeEditor } from './LazyCodeEditor'
import { InspectData } from './InspectData'
import { Markdown } from './Markdown'
import { ResultPanel } from './ResultPanel'

const LessonView = lazy(() => import('./LessonView').then(m => ({ default: m.LessonView })))

function paramNames(signature: string | null): string[] {
  const m = signature?.match(/def\s+\w+\s*\((.*)\)/)
  if (!m) return []
  return m[1]
    .split(',')
    .map((s) => s.split(/[:=]/)[0].trim())
    .filter((s) => s && s !== 'self')
}

/** 把 text 里唯一出现的 old 换成 next；old 为空则接在末尾。定位不到返回 null。 */
function replaceOnce(text: string, old: string, next: string, singleLine: boolean): string | null {
  if (singleLine && /[\r\n]/.test(next)) return null
  if (!old) return !singleLine && text && !text.endsWith('\n') ? `${text}\n${next}` : text + next
  const at = text.indexOf(old)
  if (at < 0 || text.indexOf(old, at + 1) >= 0) return null
  return text.slice(0, at) + next + text.slice(at + old.length)
}

function useElapsed(resetKey: string) {
  const start = useRef(Date.now())
  const [now, setNow] = useState(Date.now())
  useEffect(() => {
    start.current = Date.now()
    setNow(Date.now())
    const t = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [resetKey])
  const ms = Math.max(0, now - start.current)
  const label = `${Math.floor(ms / 60000)}:${String(Math.floor((ms / 1000) % 60)).padStart(2, '0')}`
  return { ms, label }
}

// ---------------------------------------------------------------------------
// 当前这道题：编辑框 + 判题 + 计时。切换题目（原题 / 附加题）时整体换掉，各题草稿分开保存。
// ---------------------------------------------------------------------------

interface ActiveHandle {
  getCode(): string
  getAnswer(): string | null
  applyEdits(edits: TutorEdit[]): ApplyResult
}

interface ActiveProps {
  review: ReviewContext
  waiting: boolean
  generating: boolean
  onExtra: (request: string, skill: string, anchor?: string) => Promise<void>
  id: string
  parent: ProblemDetail
  theme: Theme
  /** 原题的上下题导航（附加题也沿用原题的） */
  nav: { prev: ItemRef | null; crumbTrack: string; stage: string }
  bare: boolean
  setBare: (f: (b: boolean) => boolean) => void
  chatOpen: boolean
  setChatOpen: (f: (b: boolean) => boolean) => void
  /** 左栏顶部的标签条 */
  tabs: ReactNode
  /** 左栏显示什么：这道题的题面 / 课 / 别的内容（比如附加题还在出） */
  left: 'statement' | 'lesson' | ReactNode
  onShowLesson: () => void
  onResult: (failed: boolean) => void
  onDetail: (detail: ProblemDetail) => void
}

const ActiveProblem = forwardRef<ActiveHandle, ActiveProps>(function ActiveProblem(
  { id, parent, review, waiting, generating, onExtra, theme, nav, bare, setBare, chatOpen, setChatOpen, tabs, left, onShowLesson, onResult, onDetail },
  ref,
) {
  const navigate = useNavigate()
  const { revalidate } = useRevalidator()
  const track = useTracks().find((t) => t.id === nav.crumbTrack)!
  const [initial] = useState(id === parent.id ? parent : null)
  const [p, setP] = useState<ProblemDetail | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [code, setCode] = useState('')
  const [answer, setAnswer] = useState('')
  const [busy, setBusy] = useState<'run' | 'submit' | null>(null)
  const [result, setResult] = useState<{ r: JudgeResult; kind: 'run' | 'submit' } | null>(null)
  const [requestError, setRequestError] = useState<string | null>(null)
  const scope = review.review_source ? `review:${review.review_source}:${review.review_due}:${id}` : id
  const hintKey = `dojo-hints:${scope}`
  const aiKey = `dojo-ai-lines:${scope}`
  const [hintsShown, setHintsShown] = useState(() => Number(readPref(hintKey, '0')) || 0)
  const [aiLines, setAiLines] = useState(() => Number(readPref(aiKey, '0')) || 0)
  const [solution, setSolution] = useState('')
  const [loadingHelp, setLoadingHelp] = useState(false)
  const [finished, setFinished] = useState(false)
  const editorRef = useRef<CodeEditorHandle>(null)
  const latest = useRef({ code: '', answer: '' })
  latest.current = { code, answer }
  const elapsed = useElapsed(id)
  const draftKey = `dojo-draft:${id}`
  const isReview = !!review.review_source
  const next = !isReview || finished ? parent.continue_with : null

  useEffect(() => {
    let current = true
    const detail = initial ? Promise.resolve(initial) : api.problem(id)
    detail
      .then((d) => {
        if (!current) return
        setP(d)
        onDetail(d)
        const draft = isReview ? '' : readPref(draftKey, '')
        if (d.mode === 'predict' || d.format === 'inspect' || d.language === 'none') setAnswer(draft)
        else setCode(draft || d.starter)
      })
      .catch((e: Error) => setLoadError(e.message))
    return () => { current = false }
  }, [id, draftKey, initial, onDetail, isReview])

  const isPredict = p?.mode === 'predict'
  const isInspect = p?.format === 'inspect' || p?.language === 'none'
  const textAnswer = isPredict || p?.answer?.type === 'short'
  const isSql = p?.language === 'sql' && !isInspect
  const [preparing, setPreparing] = useState(false)
  useEffect(() => {
    if (!isSql) return
    let current = true
    setPreparing(true)
    import('../sql/client').then(m => m.prepare())
      .catch((e: Error) => { if (current) setRequestError(e.message) })
      .finally(() => { if (current) setPreparing(false) })
    return () => { current = false }
  }, [isSql])
  const judgeable = !!p && !preparing && !waiting && !finished && !loadingHelp

  const updateCode = (v: string) => {
    setCode(v)
    if (!isReview) writePref(draftKey, v)
  }
  const updateAnswer = useCallback((v: string) => {
    setAnswer(v)
    if (!isReview) writePref(draftKey, v)
  }, [draftKey, isReview])
  const resetCode = () => {
    if (!p) return
    if (!isReview) writePref(draftKey, null)
    setCode(p.starter)
    setAnswer('')
  }

  // 共享编辑框：助教的修改按顺序直接写进去（代码题走 Monaco，可 Ctrl+Z 撤销；predict 题改答案文本），记下 AI 写入的行数
  const applyEdits = (edits: TutorEdit[]): ApplyResult => {
    let applied = 0
    let failed = 0
    let lines = 0
    let answerText = latest.current.answer
    for (const e of edits) {
      let ok: boolean
      if (textAnswer) {
        const next = replaceOnce(answerText, e.old, e.new, isInspect)
        ok = next !== null
        if (next !== null) answerText = next
      } else {
        ok = !!editorRef.current?.applyEdit(e.old, e.new)
      }
      if (!ok) {
        failed++
        continue
      }
      applied++
      const oldLines = new Set(e.old.split('\n'))
      lines += Math.max(e.new.split('\n').filter((l) => l.trim() && !oldLines.has(l)).length, 1)
    }
    if (textAnswer && applied > 0) updateAnswer(answerText)
    if (lines > 0) {
      setAiLines((n) => {
        const next = n + lines
        writePref(aiKey, String(next))
        return next
      })
    }
    return { applied, failed }
  }

  useImperativeHandle(ref, () => ({
    getCode: () => latest.current.code,
    getAnswer: () => ((isPredict || isInspect) ? latest.current.answer : null),
    applyEdits,
  }))

  const judge = useCallback(
    async (kind: 'run' | 'submit') => {
      if (!p || !judgeable || busy || (isInspect && !answer.trim())) return
      setBusy(kind)
      setRequestError(null)
      try {
        const body: JudgeRequest = isPredict || isInspect
          ? { answer, elapsed_ms: elapsed.ms, hints_used: hintsShown, ai_lines: aiLines }
          : { code, elapsed_ms: elapsed.ms, hints_used: hintsShown, ai_lines: aiLines }
        Object.assign(body, review)
        if (isSql) body.sql_result = await (await import('../sql/client')).grade(p.id, code, kind)
        const r = kind === 'run' ? await api.run(p.id, body) : await api.submit(p.id, body)
        // 修改题当场对照 Worker 留下的表格预览，提交记录仍使用服务器的紧凑摘要。
        setResult({ r: p.mode === 'dml' && body.sql_result ? { ...r, cases: body.sql_result.cases } : r, kind })
        if (kind === 'submit') {
          if (isReview) setFinished(true)
          void revalidate()
          if (id !== parent.id) setP(await api.problem(id))
        }
        onResult(r.verdict !== 'accepted')
      } catch (e) {
        setRequestError((e as Error).message)
      } finally {
        setBusy(null)
      }
    },
    [p, judgeable, busy, id, parent.id, review, isReview, isSql, isPredict, isInspect, answer, code, elapsed.ms, hintsShown, aiLines, onResult, revalidate],
  )

  // 编辑器外的快捷键（编辑器内的由 CodeEditor 注册）
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const mod = e.ctrlKey || e.metaKey
      if (e.defaultPrevented || e.isComposing) return
      const target = e.target instanceof HTMLElement ? e.target : null
      if (isInspect && target?.closest('.chat, .lesson-view')) return
      if (p?.answer?.type === 'choice' && !mod && !e.altKey && /^[1-9]$/.test(e.key) &&
          !target?.closest('input:not([type="radio"]), textarea, [contenteditable="true"]')) {
        const index = Number(e.key) - 1
        if (index < p.answer.options.length) {
          e.preventDefault()
          updateAnswer(String(index))
        }
      } else if (mod && e.key === 'Enter') {
        e.preventDefault()
        judge(isInspect || e.shiftKey ? 'submit' : 'run')
      } else if (e.altKey && e.key === 'ArrowLeft' && nav.prev) {
        e.preventDefault()
        navigate(itemPath(nav.prev))
      } else if (e.altKey && e.key === 'ArrowRight' && next) {
        e.preventDefault()
        navigate(practicePath(next))
      } else if (!isInspect && e.altKey && (e.key === 'b' || e.key === '∫')) {
        e.preventDefault()
        setBare((b) => !b)
      } else if (e.altKey && (e.key === 'i' || e.key === 'ˆ')) {
        e.preventDefault()
        setChatOpen((c) => !c)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [judge, navigate, nav, next, setBare, setChatOpen, isInspect, p?.answer, updateAnswer])

  const names = useMemo(() => paramNames(p?.signature ?? null), [p])
  const newSkill = p?.skill_cards.find((s) => s.new)

  const stuck = id === parent.id ? parent.stuck : p?.stuck
  async function showHelp(full: boolean) {
    if (!p || loadingHelp) return
    setLoadingHelp(true)
    setRequestError(null)
    try {
      if (full) {
        const r = await api.solution(id, review)
        setSolution(r.solution)
        if (isReview) setFinished(true)
        void revalidate()
      } else {
        const n = hintsShown + 1
        await api.hint(id, n, review)
        setHintsShown(n)
        writePref(hintKey, String(n))
      }
    } catch (err) {
      setRequestError((err as Error).message)
    } finally { setLoadingHelp(false) }
  }

  const runStatus = track.runtime === 'ds' && <DsPreparation />
  let leftBody: ReactNode
  if (left === 'lesson') {
    leftBody = <Suspense fallback={null}><LessonView problemId={id} theme={theme} runStatus={runStatus} /></Suspense>
  } else if (left !== 'statement') {
    leftBody = left
  } else if (loadError) {
    leftBody = <p className="tone-fail">{loadError}</p>
  } else if (p) {
    leftBody = (
      <>
        <h1>{p.title}</h1>
        <p className="meta faint">
          {p.extra_seq ? `附加题 ${p.extra_seq} · AI 出题 · ` : ''}
          {FORMAT_NAME[p.format]} · 难度 {p.difficulty}
          {p.leetcode && (
            <>
              {' · '}
              <a href={`https://leetcode.com/problems/${p.leetcode}/`} target="_blank" rel="noreferrer">
                原题 ↗
              </a>
            </>
          )}
        </p>
        <Markdown>{p.statement}</Markdown>
        {p.data?.map((block, i) => <InspectData key={i} block={block} />)}
        {isPredict && (
          <pre className="program">
            <code>{p.program}</code>
          </pre>
        )}
        {newSkill && (
          <p className="lesson-pointer">
            <span className="accent">新</span> 这道题要用到新知识「{newSkill.name}」
            {p.has_lesson && (
              <>
                {' · '}
                <button className="link" onClick={onShowLesson}>
                  去「课」里看
                </button>
              </>
            )}
          </p>
        )}
        {stuck && !isReview && <aside className="study-note"><p>卡在{stuck.skill}上了，要不要先做一道{stuck.root ? '更小的练习' : '前置技能的小题'}？</p>
          {stuck.problem && <Link to={practicePath(stuck.problem)}>去做 {stuck.problem.title}</Link>}
          <button className="link" onClick={() => onExtra('出一道只练习「' + stuck.target + '」的小题，不引入新技能。', stuck.target_id, stuck.problem?.id)}>让助教出一道</button>
        </aside>}
        {p.hints.length > 0 && (
          <section className="hints">
            {p.hints.slice(0, hintsShown).map((h, i) => (
              <p key={i}>
                <span className="faint">提示 {i + 1}</span> {h}
              </p>
            ))}
            {hintsShown < p.hints.length && (
              <button className="ghost" disabled={!judgeable || !!busy} onClick={() => showHelp(false)}>
                提示 {hintsShown + 1}/{p.hints.length}
              </button>
            )}
          </section>
        )}
        {hintsShown >= p.hints.length && (solution ? <><p className="muted">明天从空白重写</p><pre className="io">{solution}</pre></> :
          <button className="link" disabled={!judgeable || !!busy} onClick={() => showHelp(true)}>看完整题解 · 明天重写</button>)}
      </>
    )
  }

  return (
    <>
      <div className="problem-bar">
        <Link to={`/t/${track.id}`} className="crumb">
          {track.name} / {nav.stage} · {track.stages.find((s) => s.id === nav.stage)?.name}
        </Link>
        <span className="bar-spacer" />
        {isReview && <Link to="/today" className="crumb">{finished ? '本轮已结束 · 今日计划' : '复习 · 今日计划'}</Link>}
        <span className="faint" title="本题用时">
          {elapsed.label}
        </span>
        {!isInspect && <button
          className={`toggle ${bare ? 'is-on' : ''}`}
          onClick={() => setBare((b) => !b)}
          title="裸写模式：关闭自动补全、括号配对、参数提示（Alt+B）"
          aria-pressed={bare}
        >
          裸写
        </button>}
        <button
          className={`toggle ${chatOpen ? 'is-on' : ''}`}
          onClick={() => setChatOpen((c) => !c)}
          title="AI 助教（Alt+I）"
          aria-pressed={chatOpen}
        >
          助教
        </button>
        <button className="ghost" onClick={resetCode} title={isInspect ? "清空答案" : "恢复这道题的初始代码"}>
          ↺
        </button>
        <span className="nav">
          <button
            className="ghost"
            disabled={!nav.prev}
            onClick={() => nav.prev && navigate(itemPath(nav.prev))}
            title={nav.prev ? `上一题：${nav.prev.title}（Alt+←）` : undefined}
          >
            ‹
          </button>
          {next && <Link className="crumb" to={practicePath(next)} title={`继续：${next.title}（Alt+→）`}>
            继续 →
          </Link>}
        </span>
      </div>

      <article className="statement">
        {tabs}
        {leftBody}
      </article>

      <section className={isInspect ? 'workspace inspect-workspace' : 'workspace'}>
        <div className={isInspect ? 'inspect-answer' : 'editor-wrap'}>
          {!p ? null : isInspect ? (
            <fieldset><legend>你的答案</legend>
              {p.answer?.type === 'choice' ? p.answer.options.map((option, i) =>
                <label className="inspect-option" key={i}>
                  <input type="radio" name="inspect-choice" checked={answer === String(i)}
                    onChange={() => updateAnswer(String(i))} />
                  <span className="option-number">{i + 1}</span><span>{option}</span>
                </label>) :
                <input className="short-answer" aria-label="短答案" autoComplete="off" spellCheck={false}
                  maxLength={20000} value={answer} onChange={(e) => updateAnswer(e.target.value)} />}
            </fieldset>
          ) : isPredict ? (
            <textarea
              className="answer"
              value={answer}
              onChange={(e) => updateAnswer(e.target.value)}
              placeholder="写出程序的输出"
              spellCheck={false}
              autoFocus
            />
          ) : (
            <CodeEditor
              ref={editorRef}
              value={code}
              onChange={updateCode}
              language={p.language === 'sql' ? 'pgsql' : 'python'}
              theme={theme}
              bare={bare}
              onRun={() => judge('run')}
              onSubmit={() => judge('submit')}
            />
          )}
        </div>
        <div className="actions">
          {(busy || generating) && runStatus}
          {preparing && <span className="faint" role="status">正在准备数据库…</span>}
          {!isInspect && aiLines > 0 && (
            <span className="ai-badge" title="编辑框里有助教写的代码；这次通过记为 AI 协助，不算独立掌握">
              AI 协助 {aiLines} 行
            </span>
          )}
          {requestError && <span className="tone-fail">{requestError}</span>}
          {!isInspect && <span className="bar-spacer" />}
          {!isInspect && <button
            className="secondary"
            disabled={!judgeable || !!busy}
            onClick={() => judge('run')}
            title="运行样例（Ctrl+Enter）"
          >
            {busy === 'run' ? '运行中' : '运行'}
          </button>}
          <button
            className="primary"
            disabled={!judgeable || !!busy || (isInspect && !answer.trim())}
            onClick={() => judge('submit')}
            title={isInspect ? "提交（Ctrl+Enter）" : "提交（Ctrl+Shift+Enter）"}
          >
            {busy === 'submit' ? '判题中' : '提交'}
          </button>
        </div>
        {result && p && <ResultPanel result={result.r} kind={result.kind} sql={isSql} mode={p.mode} paramNames={names} />}
      </section>
    </>
  )
})

// ---------------------------------------------------------------------------
// 做题页：标签"题目 | 课 | 附加题 1 | 附加题 2 … | ＋" + 当前这道题 + 助教。
// 用户需求（2026-11-22）："ai出题的话就加一个tab做成附加题1 … ai就可以增加管理这些附加题tab 我也能删除"
// ---------------------------------------------------------------------------

type LeftTab = 'problem' | 'lesson' | string // string = 附加题 id

export function ProblemWorkspace({ parent, theme }: { parent: ProblemDetail; theme: Theme }) {
  const id = parent.id
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const review = useMemo(() => ({
    review_source: params.get('review') || undefined, review_due: params.get('due') || undefined,
  }), [params])
  const variant = params.has('variant')
  const requestedExtra = params.get('extra')
  const [currentProblem, setCurrentProblem] = useState(parent)
  const [extraError, setExtraError] = useState<string | null>(null)
  const [extras, setExtras] = useState<ExtraSummary[]>([])
  const [tab, setTab] = useState<LeftTab>(requestedExtra ?? 'problem')
  const [activeId, setActiveId] = useState(id)
  const [bare, setBare] = useState(readPref('dojo-bare', '1') === '1')
  const [chatOpen, setChatOpen] = useState(readPref('dojo-chat', '1') === '1')
  const [lastFailed, setLastFailed] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null)
  const autoOpen = useRef<Set<string>>(new Set()) // 出好后要自动切过去的附加题
  const active = useRef<ActiveHandle>(null)

  useEffect(() => {
    api
      .extras(id)
      .then(list => {
        setExtras(list)
        const target = list.find(e => e.id === requestedExtra)
        if (target?.status === 'ready') setActiveId(target.id)
        else if (target?.status === 'generating') autoOpen.current.add(target.id)
        else if (requestedExtra && !target) setExtraError('这道附加题已删除。')
      })
      .catch(() => {})
  }, [id, requestedExtra])

  useEffect(() => writePref('dojo-bare', bare ? '1' : '0'), [bare])
  useEffect(() => writePref('dojo-chat', chatOpen ? '1' : '0'), [chatOpen])

  const reloadExtras = useCallback(() => {
    api
      .extras(id)
      .then((list) => {
        setExtras(list)
        for (const e of list) {
          if (e.status !== 'generating' && autoOpen.current.has(e.id)) {
            autoOpen.current.delete(e.id)
            setTab(e.id) // 出好或失败都切过去：好了就做题，失败就看原因
            if (e.status === 'ready') setActiveId(e.id)
          }
        }
      })
      .catch(() => {})
  }, [id])

  // 有附加题在出题时，每 2.5 秒刷新一次
  const generating = extras.some((e) => e.status === 'generating')
  useEffect(() => {
    if (!generating) return
    const t = setInterval(reloadExtras, 2500)
    return () => clearInterval(t)
  }, [generating, reloadExtras])

  const addExtra = async (req = '', skill?: string, anchor = id) => {
    setExtraError(null)
    try {
      const e = await api.createExtra(anchor, req, skill, review)
      if (anchor !== id) {
        navigate(practicePath({ id: e.id, parent: anchor, title: '' }))
        return
      }
      if (review.review_source) {
        navigate(practicePath({ id: e.id, title: '', parent: id, source: review.review_source, due: review.review_due }))
        return
      }
      autoOpen.current.add(e.id)
      setTab(e.id)
      setExtras((xs) => [...xs, e])
    } catch (err) {
      setExtraError((err as Error).message)
    }
  }

  const removeExtra = async (e: ExtraSummary) => {
    await api.deleteExtra(id, e.seq).catch(() => {})
    setConfirmDelete(null)
    writePref(`dojo-draft:${e.id}`, null)
    writePref(`dojo-ai-lines:${e.id}`, null)
    if (activeId === e.id) setActiveId(id)
    if (tab === e.id || activeId === e.id) setTab('problem')
    reloadExtras()
  }

  const onChatExtras = (newExtra: ExtraSummary | null, deleted: number[]) => {
    if (newExtra && !review.review_source) {
      autoOpen.current.add(newExtra.id)
      setExtras((xs) => [...xs, newExtra])
    }
    if (deleted.length > 0) {
      const gone = extras.filter((e) => deleted.includes(e.seq)).map((e) => e.id)
      if (gone.includes(activeId)) setActiveId(id)
      if (gone.includes(tab)) setTab('problem')
    }
    reloadExtras()
  }

  // Alt+L：在"课"和当前这道题之间切换
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.altKey && (e.key === 'l' || e.key === '¬')) {
        e.preventDefault()
        setTab((t) => (t === 'lesson' ? (activeId === id ? 'problem' : activeId) : 'lesson'))
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [activeId, id])

  const [generatingVariant, setGeneratingVariant] = useState(false)
  const parentNew = parent.skill_cards.some((s) => s.new) && parent.has_lesson
  const tabExtra = extras.find((e) => e.id === tab)

  const tabs = (
    <nav className="left-tabs" aria-label="题目、课和附加题">
      <button
        disabled={!!review.review_source && !!requestedExtra}
        className={tab === 'problem' ? 'is-active' : ''}
        onClick={() => {
          setTab('problem')
          setActiveId(id)
        }}
      >
        题目
      </button>
      <button
        className={tab === 'lesson' ? 'is-active' : ''}
        onClick={() => setTab('lesson')}
        title="这道题要用的知识点（Alt+L）"
      >
        课{parentNew ? <span className="tab-new">新</span> : null}
      </button>
      {extras.filter(e => !review.review_source || e.id === requestedExtra).map((e) => (
        <span key={e.id} className={`extra-tab ${tab === e.id ? 'is-active' : ''} ${e.status}`}>
          <button
            onClick={() => {
              setTab(e.id)
              if (e.status === 'ready') setActiveId(e.id)
            }}
            title={e.title ?? e.request}
          >
            附加题 {e.seq}
            {e.status === 'generating' && <span className="faint"> · 出题中</span>}
            {e.status === 'failed' && <span className="tone-fail"> · 失败</span>}
          </button>
          {e.status !== 'generating' && (
            <button
              className={`tab-close ${confirmDelete === e.seq ? 'is-confirm' : ''}`}
              onClick={() => (confirmDelete === e.seq ? removeExtra(e) : setConfirmDelete(e.seq))}
              onBlur={() => setConfirmDelete(null)}
              title={confirmDelete === e.seq ? '再点一次删除' : '删除这道附加题'}
            >
              {confirmDelete === e.seq ? '删除？' : '×'}
            </button>
          )}
        </span>
      ))}
      <button
        hidden={!!review.review_source}
        className="tab-add"
        onClick={() => addExtra()}
        title="让 AI 出一道相似的附加题（也可以在助教里说要什么样的）"
      >
        ＋
      </button>
    </nav>
  )

  // 左栏内容：题面 / 课 / 还没出好的附加题的状态
  let left: ActiveProps['left'] = tab === 'lesson' ? 'lesson' : 'statement'
  if (tabExtra && tabExtra.status !== 'ready') {
    left =
      tabExtra.status === 'generating' ? (
        <div className="extra-status">
          <p>
            正在出附加题 {tabExtra.seq}
            {tabExtra.request ? `：${tabExtra.request}` : ''}
          </p>
          <p className="faint">
            {parent.format === 'inspect' ? '正在核对数据和答案。' :
              '出题后会在判题沙箱里验证（参考解全过、典型错误写法被测试抓住），通常半分钟到一分钟，好了自动切过来。你可以先接着做原来的题。'}
          </p>
        </div>
      ) : (
        <div className="extra-status">
          <p className="tone-fail">附加题 {tabExtra.seq} 没出成</p>
          <pre className="io">{tabExtra.error}</pre>
          <p>
            <button className="secondary" onClick={() => removeExtra(tabExtra).then(() => addExtra(tabExtra.request, tabExtra.practice_skill ?? undefined))}>
              重新出一道
            </button>{' '}
            <button className="ghost" onClick={() => removeExtra(tabExtra)}>
              删掉
            </button>
          </p>
        </div>
      )
  }

  if (variant) left = <div className="extra-status"><h1>{parent.title}</h1>
    <p>这次换一道同套路的新题。</p><button className="secondary" disabled={generatingVariant}
      onClick={async () => { setGeneratingVariant(true); await addExtra(variantRequest); setGeneratingVariant(false) }}>
      让助教出一道同套路的</button></div>

  return (
    <main className={`problem ${chatOpen ? 'with-chat' : ''}`}>
      <ActiveProblem
        key={activeId}
        ref={active}
        id={activeId}
        parent={parent}
        review={review}
        generating={generating}
        waiting={variant || (!!requestedExtra && (tab === requestedExtra || !!review.review_source) && activeId !== requestedExtra) || (!!review.review_source && !!tabExtra && tabExtra.status !== 'ready')}
        onExtra={addExtra}
        theme={theme}
        nav={{ prev: parent.prev, crumbTrack: parent.track, stage: parent.stage }}
        bare={bare}
        setBare={setBare}
        chatOpen={chatOpen}
        setChatOpen={setChatOpen}
        tabs={<>{tabs}{extraError && <p role="alert" className="tone-fail">{extraError}</p>}</>}
        onDetail={setCurrentProblem}
        left={left}
        onShowLesson={() => setTab('lesson')}
        onResult={setLastFailed}
      />
      {chatOpen && (
        <ChatPanel
          review={review}
          problemId={id}
          currentId={activeId}
          choice={currentProblem.answer?.type === 'choice'}
          getCode={() => active.current?.getCode() ?? ''}
          getAnswer={() => active.current?.getAnswer() ?? null}
          onEdits={(edits) => active.current?.applyEdits(edits) ?? { applied: 0, failed: edits.length }}
          lastFailed={lastFailed}
          onExtras={onChatExtras}
        />
      )}
    </main>
  )
}
