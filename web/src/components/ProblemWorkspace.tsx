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
import { flushSync } from 'react-dom'
import { Link, useNavigate, useRevalidator, useSearchParams } from 'react-router-dom'
import {
  api,
  itemPath,
  practicePath,
  prefetchProblem,
  type ReviewContext,
  type ExtraSummary,
  type ItemRef,
  type JudgeRequest,
  type ProblemDetail,
  type WorkspaceData,
  type TutorEdit,
} from '../api'
import { variantRequest } from '../pages/PlanPages'
import { FORMAT_NAME } from '../labels'
import { readPref, writePref, type Theme } from '../theme'
import { useTracks } from '../tracks'
import { playPassSound, recordHelp, recordSubmission, sessionItemPath, usePracticeSession, visitItem, type PracticeSession } from '../practiceSession'
import { DsPreparation } from './DsPreparation'
import { ChatPanel, type ApplyResult } from './ChatPanel'
import type { CodeEditorHandle } from './CodeEditor'
import { CodeEditor } from './LazyCodeEditor'
import { InspectData } from './InspectData'
import { Markdown } from './Markdown'
import { Picker, usePickerShortcut, type PickerItem } from './Picker'
import { STATUS_NAME } from './ProblemStatus'
import { DesktopBridge } from './DesktopBridge'
import { SyncStatus } from './SyncStatus'
import { SessionBar } from './SessionBar'
import { Explorer, Icon, Separator, useWorkbenchLayout, type WorkbenchLayout } from './WorkbenchLayout'
import { WorkbenchPanel, diagnostics, type Attempt, type ExampleOutput, type PanelOutput, type PanelTab } from './WorkbenchPanel'

const LessonView = lazy(() => import('./LessonView').then(m => ({ default: m.LessonView })))

const StandardAnswerView = lazy(() => import('./StandardAnswerView'))

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

// ---------------------------------------------------------------------------
// 当前这道题：编辑框 + 判题 + 计时。切换题目（原题 / 附加题）时整体换掉，各题草稿分开保存。
// ---------------------------------------------------------------------------

interface ActiveHandle {
  getCode(): string
  getAnswer(): string | null
  applyEdits(edits: TutorEdit[]): ApplyResult
}

interface ActiveProps {
  session: PracticeSession | null
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
  layout: WorkbenchLayout
  unit: string
  backend: string
  /** 左栏顶部的标签条 */
  tabs: ReactNode
  /** 左栏显示什么：这道题的题面 / 课 / 别的内容（比如附加题还在出） */
  left: 'statement' | 'lesson' | ReactNode
  onParentPassed: () => void
  onShowStandard?: () => void
  onShowLesson: () => void
  onResult: (failed: boolean) => void
  onDetail: (detail: ProblemDetail) => void
}

const ActiveProblem = forwardRef<ActiveHandle, ActiveProps>(function ActiveProblem(
  { id, parent, review, session, waiting, generating, onExtra, theme, nav, bare, setBare, layout, unit, backend, tabs, left, onShowLesson, onShowStandard, onParentPassed, onResult, onDetail },
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
  const scratchKey = `dojo-scratch:${id}`
  const [scratch, setScratch] = useState(() => readPref(scratchKey, ''))
  const scratchText = useRef(scratch)
  const [inScratch, setInScratch] = useState(false)
  const [scratchOpened, setScratchOpened] = useState(false)
  const [scratchBusy, setScratchBusy] = useState(false)
  const [busy, setBusy] = useState<'run' | 'submit' | null>(null)
  const [result, setResult] = useState<Attempt | null>(null)
  const [requestError, setRequestError] = useState<string | null>(null)
  const [panelTab, setPanelTab] = useState<PanelTab>('测试结果')
  const [output, setOutput] = useState<PanelOutput | null>(null)
  const scratchRun = useRef(0)
  const [commandsOpen, setCommandsOpen] = useState(false)
  const [answerCursor, setAnswerCursor] = useState({ line: 1, col: 1 })
  const [scratchCursor, setScratchCursor] = useState({ line: 1, col: 1 })
  const cursor = inScratch ? scratchCursor : answerCursor
  const problems = diagnostics(result, requestError)
  const { setPanel } = layout
  usePickerShortcut(true, () => setCommandsOpen(true))
  const scope = review.review_source ? `review:${review.review_source}:${review.review_due}:${id}` : id
  const hintKey = `dojo-hints:${scope}`
  const aiKey = `dojo-ai-lines:${scope}`
  const [hintsShown, setHintsShown] = useState(() => Number(readPref(hintKey, '0')))
  const [aiLines, setAiLines] = useState(() => Number(readPref(aiKey, '0')))
  const [solution, setSolution] = useState('')
  const [loadingHelp, setLoadingHelp] = useState(false)
  const [finished, setFinished] = useState(false)
  const editorRef = useRef<CodeEditorHandle>(null)
  const latest = useRef({ code: '', answer: '' })
  latest.current = { code, answer }
  const [started] = useState(Date.now)
  const [autoAt, setAutoAt] = useState<number | null>(null)
  useEffect(() => {
    if (left === 'standard' && autoAt !== null) setAutoAt(null)
  }, [left, autoAt])
  const [sound, setSound] = useState(() => readPref('dojo-sound', '0') === '1')
  const toggleSound = () => { writePref('dojo-sound', sound ? '0' : '1'); setSound(!sound) }
  const index = session && !session.ended && !waiting ? session.items.findIndex(item => item.id === id) : -1
  const item = session?.items[index]
  const openSessionId = item?.status === 'open' ? session?.id : undefined
  useEffect(() => {
    if (openSessionId) visitItem(openSessionId, index)
  }, [openSessionId, index])
  useEffect(() => {
    if (item?.status === 'open' && item.source && !item.reviewClosed && (item.source !== review.review_source || item.due !== review.review_due)) {
      void navigate(sessionItemPath(item), { replace: true })
    }
  }, [item, review, navigate])
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
  const textAnswer = p?.answer?.type === 'short'
  const isSql = p?.language === 'sql'
  const isSqlAnswer = isSql && !isInspect
  const inspectAnswerActive = isInspect && !inScratch
  const hasScratch = !!p
  const [preparing, setPreparing] = useState(false)
  useEffect(() => {
    if (!isSqlAnswer) return
    let current = true
    setPreparing(true)
    import('../sql/client').then(m => m.prepare())
      .catch((e: Error) => { if (current) setRequestError(e.message) })
      .finally(() => { if (current) setPreparing(false) })
    return () => { current = false }
  }, [isSqlAnswer])
  const judgeable = !!p && !preparing && !waiting && !finished && !(isReview && item?.reviewClosed) && !loadingHelp
  const canRun = inScratch ? hasScratch && !preparing && !waiting && !scratchBusy : judgeable && !busy && !isInspect

  const switchFile = (scratch: boolean) => {
    flushSync(() => {
      if (scratch) setScratchOpened(true)
      setInScratch(scratch)
    })
    const pane = document.getElementById(scratch ? 'scratch-editor' : 'answer-editor')
    const control = !scratch && isInspect
      ? pane?.querySelector<HTMLInputElement>('input:checked') ?? pane?.querySelector<HTMLInputElement>('input')
      : pane?.querySelector<HTMLElement>('[role="textbox"]')
    control?.focus()
  }

  const updateCode = (v: string) => {
    setCode(v)
    if (!isReview) writePref(draftKey, v)
  }
  const updateScratch = (v: string) => {
    // 输入后可以立刻按 Ctrl+Enter，运行时取 Monaco 刚写入的内容。
    scratchText.current = v
    setScratch(v)
    writePref(scratchKey, v)
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
      const previousScratchRun = scratchRun.current
      setPanel(true)
      setPanelTab('测试结果')
      setBusy(kind)
      setResult(null)
      setRequestError(null)
      try {
        const body: JudgeRequest = { ...(isPredict || isInspect ? { answer } : { code }),
          elapsed_ms: Math.max(0, Date.now() - started), hints_used: hintsShown, ai_lines: aiLines }
        Object.assign(body, review)
        if (isSqlAnswer) body.sql_result = await (await import('../sql/client')).grade(p.id, code, kind)
        const r = kind === 'run' ? await api.run(p.id, body) : await api.submit(p.id, body)
        // 当前 SQL 作答展示 Worker 返回的表格，历史提交继续使用服务端摘要。
        setResult({ r: body.sql_result ? { ...r, cases: body.sql_result.cases } : r, kind, source: code })
        if (kind === 'submit') {
          const passed = r.verdict === 'accepted'
          if (session && item?.status === 'open') {
            const updated = recordSubmission(session.id, index, passed)
            if (passed && updated) setAutoAt(Date.now() + 1500)
          }
          if (passed) {
            playPassSound()
            if (id === parent.id) onParentPassed()
          }
          if (isReview) setFinished(true)
          void revalidate()
          if (id !== parent.id) setP(await api.problem(id))
        }
        onResult(r.verdict !== 'accepted')
      } catch (e) {
        setRequestError((e as Error).message)
      } finally {
        if (previousScratchRun === scratchRun.current) {
          setPanel(true)
          setPanelTab('测试结果')
        }
        setBusy(null)
      }
    },
    [p, judgeable, busy, id, parent.id, review, isReview, isSqlAnswer, isPredict, isInspect, answer, code, started, session, item, index, hintsShown, aiLines, onResult, onParentPassed, revalidate, setPanel],
  )

  async function runCurrent() {
    if (!inScratch) return judge('run')
    if (!canRun) return
    const text = scratchText.current
    const pending: PanelOutput = { source: '草稿' }
    scratchRun.current++
    setOutput(pending)
    setPanel(true)
    setPanelTab('输出')
    setScratchBusy(true)
    let result: ExampleOutput
    try {
      if (isSql) {
        const setup = isInspect ? await api.bookstoreSetup() : (await api.sqlCases(id, 'sample')).datasets[0].setup
        const table = await (await import('../sql/client')).runExample(setup, text)
        result = { stdout: '', table }
      } else {
        result = await api.playground(text, '', id)
      }
    } catch (e) {
      result = { stdout: '', error: (e as Error).message }
    } finally {
      setScratchBusy(false)
    }
    setOutput(current => current === pending ? { source: '草稿', result } : current)
  }

  // 编辑器外的快捷键（编辑器内的由 CodeEditor 注册）
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const mod = e.ctrlKey || e.metaKey
      if (e.defaultPrevented || e.isComposing || document.querySelector('dialog[open]')) return
      const target = e.target instanceof HTMLElement ? e.target : null
      if (hasScratch && e.altKey && !mod && !e.shiftKey && e.code === 'KeyS') {
        e.preventDefault()
        switchFile(!inScratch)
        return
      }
      if (mod && e.shiftKey && e.key === 'Enter') {
        e.preventDefault()
        void judge('submit')
        return
      }
      if (inspectAnswerActive && target?.closest('.chat, .lesson-view')) return
      if (inspectAnswerActive && p?.answer?.type === 'choice' && !mod && !e.altKey && /^[1-9]$/.test(e.key) &&
          !target?.closest('input:not([type="radio"]), textarea, [contenteditable="true"]')) {
        const index = Number(e.key) - 1
        if (index < p.answer.options.length) {
          e.preventDefault()
          updateAnswer(String(index))
        }
      } else if (mod && e.key === 'Enter') {
        e.preventDefault()
        if (inspectAnswerActive) void judge('submit')
        else void runCurrent()
      } else if (e.altKey && e.key === 'ArrowLeft' && nav.prev) {
        e.preventDefault()
        navigate(itemPath(nav.prev))
      } else if (e.altKey && e.key === 'ArrowRight' && next) {
        e.preventDefault()
        navigate(practicePath(next))
      } else if (!inspectAnswerActive && e.altKey && (e.key === 'b' || e.key === '∫')) {
        e.preventDefault()
        setBare((b) => !b)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [judge, runCurrent, inScratch, hasScratch, navigate, nav, next, setBare, inspectAnswerActive, p?.answer, updateAnswer])

  const names = useMemo(() => paramNames(p?.signature ?? null), [p])
  const newSkill = p?.skill_cards.find((s) => s.new)

  const stuck = id === parent.id ? parent.stuck : p?.stuck
  // 原题的状态跟着路由数据刷新（提交后 revalidate），附加题提交后重新取详情
  const done = id === parent.id ? parent.status : p?.status ?? null
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
      if (session && item) recordHelp(session.id, index, 'hints', full)
    } catch (err) {
      setRequestError((err as Error).message)
    } finally { setLoadingHelp(false) }
  }

  const runStatus = track.runtime === 'ds' && <DsPreparation />
  const nextPath = isReview ? (next && practicePath(next)) : parent.next && itemPath(parent.next)
  const prevPath = nav.prev && itemPath(nav.prev)
  const nextTitle = (isReview ? next : parent.next)?.title ?? ''
  let leftBody: ReactNode
  if (left === 'lesson') {
    // 示例保留点击运行时的回调；晚返回的旧示例不能覆盖随后启动的草稿。
    const version = scratchRun.current
    leftBody = <Suspense fallback={null}><LessonView problemId={id} theme={theme} runStatus={runStatus}
      onOutput={result => {
        if (version !== scratchRun.current) return
        setOutput({ source: '课 · 示例', result })
        setPanelTab('输出')
        setPanel(true)
      }} /></Suspense>
  } else if (left === 'standard') {
    leftBody = <Suspense fallback={null}><StandardAnswerView id={id} code={code} theme={theme} /></Suspense>
  } else if (left !== 'statement') {
    leftBody = left
  } else if (loadError) {
    leftBody = <p className="tone-fail">{loadError}</p>
  } else if (p) {
    leftBody = (
      <>
        <div className="title-row">
          <h1>{p.title}{done && <span className={'title-status status ' + done}>
            {done === 'attempted' ? '◐' : '●'} {STATUS_NAME[done]}</span>}</h1>
          <nav className="title-nav" aria-label="切换题目">
            <button title={'上一题 · ' + (nav.prev?.title ?? '') + '（Alt+←）'} disabled={!prevPath}
              onClick={() => prevPath && navigate(prevPath)}><Icon name="chevron-left" />上一题</button>
            <button title={'下一题 · ' + nextTitle + '（Alt+→）'} disabled={!nextPath}
              onClick={() => nextPath && navigate(nextPath)}>下一题<Icon name="chevron-right" /></button>
          </nav>
        </div>
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

  const filename = isInspect ? 'answer' : isPredict ? 'answer.txt' : isSql ? 'query.sql' : 'solution.py'
  const runLabel = inScratch ? '运行草稿' : '运行样例'
  const crumbs = [track.name, nav.stage, unit, p?.title].filter(Boolean).join('  ›  ')
  const togglePanel = () => setPanel(!layout.panel)
  const showIssues = () => { setPanelTab('问题'); setPanel(true) }
  const commands: PickerItem[] = [
    { id: 'run', title: runLabel, shortcut: 'Ctrl+Enter', disabled: !canRun, run: runCurrent },
    { id: 'submit', title: '提交', shortcut: 'Ctrl+Shift+Enter', disabled: !judgeable || !!busy || (isInspect && !answer.trim()), run: () => judge('submit') },
    ...(hasScratch ? [{ id: 'scratch', title: '切换答案 / 草稿', shortcut: 'Alt+S', run: () => switchFile(!inScratch) }] : []),
    { id: 'bare', title: '切换裸写模式', shortcut: 'Alt+B', disabled: inspectAnswerActive, run: () => setBare(b => !b) },
    { id: 'focus', title: layout.focus ? '退出专注模式' : '开启专注模式', shortcut: 'Alt+Z', run: layout.toggleFocus },
    { id: 'sound', title: '开关通过提示音', run: toggleSound },
    { id: 'chat', title: '开关助教', shortcut: 'Ctrl+Alt+I', run: layout.toggleChat },
    { id: 'reset', title: isInspect ? '清空答案' : '重置代码', run: resetCode },
    ...(onShowStandard ? [{ id: 'standard', title: '打开参考答案', run: onShowStandard }] : []),
    { id: 'lesson', title: '打开课', shortcut: 'Alt+L', run: onShowLesson },
    { id: 'panel', title: '开关底部面板', shortcut: 'Ctrl+J', run: togglePanel },
    { id: 'files', title: '开关本单元题目列表', shortcut: 'Ctrl+B', disabled: layout.focus, run: layout.toggleFiles },
    { id: 'prev', title: '上一题', disabled: !prevPath, run: () => prevPath && navigate(prevPath) },
    { id: 'next', title: '下一题', disabled: !nextPath, run: () => nextPath && navigate(nextPath) },
    { id: 'map', title: '返回地图', run: () => navigate(isSql ? '/?tab=sql' : '/') },
  ]
  return <>
    <div className="wb-desk">
      {session && item && <SessionBar session={session} index={index} autoAt={left === 'standard' ? null : autoAt} setAutoAt={setAutoAt}
        busy={!!busy || loadingHelp} review={isReview} />}
      <div className="editor-groups">
        <section className="wb-reading">
          <div className="editor-tabs reading-tabs">
            {!layout.focus && <button className="icon-btn" title="本单元题目列表（Ctrl+B）" aria-pressed={layout.filesOpen}
              onClick={layout.toggleFiles}><Icon name="layout-sidebar-left" /></button>}{tabs}
            <button className="icon-btn chat-access" title="打开助教" aria-pressed={layout.chatOpen}
              onClick={layout.toggleChat}><Icon name="comment-discussion" /></button>
          </div>
          <div className="breadcrumbs" title={crumbs}>{crumbs}</div>
          <article className="statement">{leftBody}</article>
          <Separator side={layout.narrow ? 'top' : 'left'} size={layout.split} percent label="调整题面与编辑器比例" />
        </section>
        <section className="wb-code">
          <div className="editor-tabs file-tabs">
            <nav className="code-files" aria-label="编辑文件">
              <button className="file-tab" aria-pressed={!inScratch} aria-controls="answer-editor"
                onClick={() => switchFile(false)}><Icon name={isInspect ? 'table' : isPredict ? 'file-text' : isSql ? 'database' : 'code'} />{filename}</button>
              {hasScratch && <button className="file-tab" aria-pressed={inScratch} aria-controls="scratch-editor"
                title="切换答案 / 草稿（Alt+S）" onClick={() => switchFile(true)}>
                <Icon name="beaker" />{isSql ? 'scratch.sql' : 'scratch.py'}</button>}
            </nav>
            <span className="bar-spacer" />
            {!inspectAnswerActive && <button className="run-action" disabled={!canRun} title={runLabel + '（Ctrl+Enter）'}
              onClick={runCurrent}><Icon name="play" />{(inScratch ? scratchBusy : busy === 'run') ? '运行中' : '运行'}</button>}
            <button className="submit-action" disabled={!judgeable || !!busy || (isInspect && !answer.trim())}
              onClick={() => judge('submit')} title="提交（Ctrl+Shift+Enter）">{busy === 'submit' ? '判题中' : '提交'}</button>
            <button className="icon-btn" title="开关通过提示音" aria-label="开关通过提示音" aria-pressed={sound}
              onClick={toggleSound}><Icon name={sound ? 'unmute' : 'mute'} /></button>
            <button className="icon-btn" title="命令面板（Ctrl+Shift+P）" onClick={() => setCommandsOpen(true)}><Icon name="ellipsis" /></button>
          </div>
          <div className="breadcrumbs" title={crumbs}>{crumbs}</div>
          <div id="answer-editor" hidden={inScratch} className={isInspect ? 'inspect-answer' : 'editor-wrap'}>
          {!p ? null : isInspect ? (
            <fieldset><legend>你的答案</legend>
              {p.answer?.type === 'choice' ? p.answer.options.map((option, i) =>
                <label className="inspect-option" key={i}>
                  <input type="radio" name="inspect-choice" checked={answer === String(i)}
                    onChange={() => updateAnswer(String(i))} />
                  <span className="option-number">{i + 1}</span><span>{option}</span>
                </label>) :
                <input className="short-answer" aria-label="短答案" autoComplete="off" spellCheck={false}
                  onSelect={e => setAnswerCursor({ line: 1, col: (e.currentTarget.selectionStart ?? 0) + 1 })}
                  maxLength={20000} value={answer} onChange={(e) => updateAnswer(e.target.value)} />}
            </fieldset>
          ) : (
            <CodeEditor
              ref={editorRef}
              value={isPredict ? answer : code}
              onChange={isPredict ? updateAnswer : updateCode}
              onCursor={(line, col) => setAnswerCursor({ line, col })}
              language={isPredict ? 'plaintext' : isSql ? 'pgsql' : 'python'}
              placeholder={isPredict ? '写出程序的输出' : undefined}
              theme={theme}
              bare={bare}
              onRun={() => judge('run')}
              onSubmit={() => judge('submit')}
            />
          )}
          </div>
          {hasScratch && <div id="scratch-editor" hidden={!inScratch} className="editor-wrap">
            {scratchOpened && <Suspense fallback={null}><CodeEditor value={scratch} language={isSql ? 'pgsql' : 'python'}
              onChange={updateScratch}
              onCursor={(line, col) => setScratchCursor({ line, col })} theme={theme} bare={bare}
              placeholder="随手试代码，不判题" onRun={runCurrent} onSubmit={() => judge('submit')} /></Suspense>}
          </div>}
          {(preparing || aiLines > 0 || requestError || ((busy || scratchBusy || generating) && runStatus)) && <div className="editor-notice" role="status">
            {(busy || scratchBusy || generating) && runStatus}
            {preparing && '正在准备数据库…'}
            {aiLines > 0 && <span className="ai-badge">AI 协助 {aiLines} 行</span>}
            {requestError && <span className="tone-fail">{requestError}</span>}
          </div>}
        </section>
      </div>
      {layout.panel && <WorkbenchPanel layout={layout} tab={panelTab} setTab={setPanelTab}
        attempt={result} problems={problems} sql={isSqlAnswer} mode={p?.mode ?? null} names={names}
        jump={isInspect || isPredict ? undefined : n => {
          flushSync(() => setInScratch(false))
          editorRef.current?.jumpTo(n)
        }} output={output} busy={!!busy} />}
    </div>
    <footer className="wb-status">
      <div className="status-items">
        {!layout.focus && <>
          <Link to={'/t/' + track.id} title={track.name + ' · ' + nav.stage}><Icon name="source-control" />{track.name} · {nav.stage}</Link>
          <button title="查看问题" onClick={showIssues}><Icon name="error" />{problems.length}</button>
          <span>{backend}</span>
          {isReview && <Link to="/today">{finished ? '本轮已结束 · 今日计划' : '复习 · 今日计划'}</Link>}
        </>}
        <span className="bar-spacer" />
        {!layout.focus && <>
          <span aria-label="本题用时" onMouseEnter={e => {
            e.currentTarget.title = `本题用时 ${Math.floor((Date.now() - started) / 60000)} 分钟`
          }}><Icon name="clock" /></span>
          {(!inspectAnswerActive || textAnswer) && <span>行 {cursor.line}，列 {cursor.col}</span>}
        </>}
        <span>{inspectAnswerActive ? '数据' : isSql ? 'SQL' : 'Python'}</span>
        {!inspectAnswerActive && <button aria-pressed={bare} onClick={() => setBare(b => !b)} title="切换裸写（Alt+B）"><Icon name={bare ? 'check' : 'dash'} />裸写</button>}
        <button aria-pressed={layout.focus} onClick={layout.toggleFocus} title="开关专注模式（Alt+Z）"><Icon name="screen-full" />{layout.focus ? '退出专注' : '专注'}</button>
        {!layout.focus && <>
          <button aria-pressed={layout.chatOpen} onClick={layout.toggleChat} title="开关助教（Ctrl+Alt+I）"><Icon name="comment-discussion" />助教</button>
          <button onClick={togglePanel} title="开关底部面板（Ctrl+J）" aria-pressed={layout.panel}><Icon name="layout-panel" /></button>
        </>}
        <SyncStatus silent={layout.focus} />
        {!layout.focus && <>
          <button title="重置代码或答案" onClick={resetCode}><Icon name="discard" /></button>
          <button title={'上一题 · ' + (nav.prev?.title ?? '')} disabled={!prevPath} onClick={() => prevPath && navigate(prevPath)}><Icon name="chevron-left" /></button>
          <button title={'下一题 · ' + ((isReview ? next : parent.next)?.title ?? '')} disabled={!nextPath} onClick={() => nextPath && navigate(nextPath)}><Icon name="chevron-right" /></button>
          {next && practicePath(next) !== nextPath && <Link to={practicePath(next)} title={'继续 · ' + next.title + '（Alt+→）'}>继续 →</Link>}
        </>}
      </div>
      {!layout.focus && <div className="desktop-slot"><DesktopBridge /></div>}
    </footer>
    {commandsOpen && <Picker label="搜索命令" items={commands} close={() => setCommandsOpen(false)} />}
  </>

})

// ---------------------------------------------------------------------------
// 做题页：标签"题目 | 课 | 附加题 1 | 附加题 2 … | ＋" + 当前这道题 + 助教。
// 用户需求（2026-11-22）："ai出题的话就加一个tab做成附加题1 … ai就可以增加管理这些附加题tab 我也能删除"
// ---------------------------------------------------------------------------

type LeftTab = 'problem' | 'lesson' | string // string = 附加题 id

export function ProblemWorkspace({ data, theme }: { data: WorkspaceData; theme: Theme }) {
  const { parent, rows, reviews, status } = data
  const track = useTracks().find(t => t.id === parent.track)!
  const unitId = rows.find(p => p.id === (parent.parent || parent.id))?.unit
  const unit = track.stages.find(s => s.id === parent.stage)?.units.find(u => u.id === unitId)
  const unitRows = rows.filter(p => p.stage === parent.stage && p.unit === unitId)
  const due = new Set(reviews.map(item => item.source || item.id))
  const layout = useWorkbenchLayout()
  const session = usePracticeSession()
  const backend = track.runtime === 'pglite' || track.runtime === 'none' ? '本地' :
    status.judge_backends[track.runtime] === 'docker' ? 'Docker' : '本地'
  const id = parent.id
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const review = useMemo(() => ({
    review_source: params.get('review') || undefined, review_due: params.get('due') || undefined,
  }), [params])
  const variant = params.has('variant')
  const requestedExtra = params.get('extra')
  const [currentProblem, setCurrentProblem] = useState(parent)
  const [passedHere, setPassedHere] = useState(false)
  const [extraError, setExtraError] = useState<string | null>(null)
  const [extras, setExtras] = useState<ExtraSummary[]>([])
  const [tab, setTab] = useState<LeftTab>(requestedExtra ?? 'problem')
  const [activeId, setActiveId] = useState(id)
  const [bare, setBare] = useState(readPref('dojo-bare', '1') === '1')
  const [lastFailed, setLastFailed] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null)
  const autoOpen = useRef<Set<string>>(new Set()) // 出好后要自动切过去的附加题
  const active = useRef<ActiveHandle>(null)
  const recordAi = () => {
    if (!session || session.ended) return
    const index = session.items.findIndex(p => p.id === activeId)
    if (index >= 0) recordHelp(session.id, index, 'ai')
  }

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
  }, [id, requestedExtra])

  // 上一题、下一题和"继续"大概率是下一步，先取好，点击后路由立即就绪。
  useEffect(() => {
    const next = parent.continue_with
    for (const pid of [parent.prev?.id, parent.next?.id, next?.parent ?? next?.id]) if (pid) prefetchProblem(pid)
  }, [parent])

  useEffect(() => writePref('dojo-bare', bare ? '1' : '0'), [bare])
  useEffect(() => {
    function key(e: KeyboardEvent) {
      if (e.isComposing || document.querySelector('dialog[open]')) return
      const mod = e.ctrlKey || e.metaKey
      if (e.altKey && !mod && !e.shiftKey && e.code === 'KeyZ') layout.toggleFocus()
      else if (mod && !e.shiftKey && !e.altKey && e.code === 'KeyB' && !layout.focus) layout.toggleFiles()
      else if (mod && !e.shiftKey && !e.altKey && e.code === 'KeyJ') layout.setPanel(!layout.panel)
      else if (e.altKey && !e.shiftKey && e.code === 'KeyI') layout.toggleChat()
      else if (e.key === 'Escape' && layout.narrow && (layout.filesOpen || layout.chatOpen)) layout.closeDrawer()
      else return
      e.preventDefault()
      e.stopPropagation()
    }
    window.addEventListener('keydown', key, true)
    return () => window.removeEventListener('keydown', key, true)
  }, [layout])

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
      recordAi()
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
    await api.deleteExtra(id, e.seq)
    setConfirmDelete(null)
    writePref(`dojo-draft:${e.id}`, null)
    writePref(`dojo-scratch:${e.id}`, null)
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
      for (const extraId of gone) writePref(`dojo-scratch:${extraId}`, null)
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

  const showStandard = activeId === id && !parent.parent && !variant && !tab.startsWith('x-') &&
    !(review.review_source && requestedExtra) && parent.format !== 'predict' && parent.format !== 'inspect' &&
    (passedHere || parent.status === 'solved' || parent.status === 'assisted')
  const openStandard = () => setTab('standard')
  const tabs = (
    <nav className="left-tabs" aria-label="题目、课、参考答案和附加题">
      <button
        disabled={!!review.review_source && !!requestedExtra}
        className={tab === 'problem' ? 'is-active' : ''}
        onClick={() => {
          setTab('problem')
          setActiveId(id)
        }}
      >
        <Icon name="markdown" />题目
      </button>
      <button
        className={tab === 'lesson' ? 'is-active' : ''}
        onClick={() => setTab('lesson')}
        title="这道题要用的知识点（Alt+L）"
      >
        <Icon name="book" />课{parentNew ? <span className="tab-new">新</span> : null}
      </button>
      {showStandard && <button className={tab === 'standard' ? 'is-active' : ''} aria-pressed={tab === 'standard'}
        onClick={openStandard}>参考答案</button>}
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
  let left: ActiveProps['left'] = tab === 'standard' && showStandard ? 'standard' : tab === 'lesson' ? 'lesson' : 'statement'
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
    <main className={'workbench' + (layout.focus ? ' is-focused' : '')} style={layout.style}>
      {layout.narrow && (layout.filesOpen || layout.chatOpen) &&
        <button className="drawer-shade" aria-label="收起抽屉" onClick={layout.closeDrawer} />}
      {layout.filesOpen && <Explorer rows={unitRows} unit={unit?.name || parent.stage} layout={layout} parent={parent} due={due} />}
      <ActiveProblem
        key={activeId}
        ref={active}
        id={activeId}
        parent={parent}
        review={review}
        session={session}
        generating={generating}
        waiting={variant || (!!requestedExtra && (tab === requestedExtra || !!review.review_source) && activeId !== requestedExtra) || (!!review.review_source && !!tabExtra && tabExtra.status !== 'ready')}
        onExtra={addExtra}
        theme={theme}
        nav={{ prev: parent.prev, crumbTrack: parent.track, stage: parent.stage }}
        bare={bare}
        setBare={setBare}
        layout={layout} unit={unit?.name || parent.stage} backend={backend}
        tabs={<>{tabs}{extraError && <p role="alert" className="tone-fail">{extraError}</p>}</>}
        onDetail={setCurrentProblem}
        left={left}
        onParentPassed={() => setPassedHere(true)}
        onShowStandard={showStandard ? openStandard : undefined}
        onShowLesson={() => setTab('lesson')}
        onResult={setLastFailed}
      />
      <div className="wb-chat" hidden={!layout.chatOpen}>
        {!layout.narrow && layout.chatOpen && <Separator label="调整助教宽度" side="right" size={layout.tutor} />}
        <ChatPanel aiOn={status.ai !== 'off'} close={layout.toggleChat} onReply={recordAi}
          review={review}
          problemId={id}
          currentId={activeId}
          choice={currentProblem.answer?.type === 'choice'}
          getCode={() => active.current!.getCode()}
          getAnswer={() => active.current!.getAnswer()}
          onEdits={(edits) => active.current!.applyEdits(edits)}
          lastFailed={lastFailed}
          onExtras={onChatExtras}
        />
      </div>
    </main>
  )
}
