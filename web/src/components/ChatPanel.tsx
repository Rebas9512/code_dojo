import { useEffect, useRef, useState } from 'react'
import { api, preferredAgent, serverStatus, type Agent, type ChatMessage, type ExtraSummary, type TutorEdit, type ReviewContext } from '../api'
import { writePref } from '../theme'
import { Icon } from './WorkbenchLayout'
import { Markdown } from './Markdown'

export interface ApplyResult {
  applied: number
  failed: number
}

interface Props {
  aiOn: boolean
  close: () => void
  onReply: () => void
  /** 原题 id：原题和它的附加题共用这一段对话 */
  problemId: string
  /** 学生正在看的题（原题或附加题 x-12），助教按它组织上下文 */
  review: ReviewContext
  currentId: string
  choice: boolean
  /** 发送时读取编辑框里的当前内容（代码 / predict 题的答案） */
  getCode: () => string
  getAnswer: () => string | null
  /** 把助教的修改直接写进共享编辑框，返回改上了几处、几处没改上 */
  onEdits: (edits: TutorEdit[]) => ApplyResult
  lastFailed: boolean
  /** 助教出了 / 删了附加题 */
  onExtras: (newExtra: ExtraSummary | null, deleted: number[]) => void
}

const QUICK: [string, string][] = [
  ['讲讲思路', '讲讲思路'],
  ['我卡住了', '我卡住了'],
  ['帮我补一下', '帮我补一下'],
  ['出一道附加题', '再出一道类似的附加题，巩固一下'],
]

function EditsView({ msg, result }: { msg: ChatMessage; result?: ApplyResult }) {
  const n = msg.edits.length
  return (
    <details className="edits-view">
      <summary className="faint">
        {result
          ? `改了编辑框 ${result.applied} 处${result.failed ? `，${result.failed} 处没改上（内容已经变了）` : ''} · Ctrl+Z 撤销`
          : `改过编辑框 ${n} 处`}
      </summary>
      {msg.edits.map((e, k) => (
        <div key={k} className="edit-item">
          <pre className="diff">
            {e.old &&
              e.old.split('\n').map((l, i) => (
                <span key={`o${i}`} className="del">
                  {'- ' + l + '\n'}
                </span>
              ))}
            {e.new.split('\n').map((l, i) => (
              <span key={`n${i}`} className="add">
                {'+ ' + l + '\n'}
              </span>
            ))}
          </pre>
          {e.why && <p className="why faint">{e.why}</p>}
        </div>
      ))}
    </details>
  )
}

export function ChatPanel({ aiOn, close, onReply, problemId, currentId, review, choice, getCode, getAnswer, onEdits, lastFailed, onExtras }: Props) {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selected, setSelected] = useState('')
  useEffect(() => {
    serverStatus().then(({ ai_agents }) => {
      setAgents(ai_agents)
      setSelected(preferredAgent(ai_agents)?.id ?? '')
    })
  }, [])
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<Record<number, ApplyResult>>({})
  const activeId = useRef(currentId)
  activeId.current = currentId
  const listRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    setMessages([])
    setError(null)
    setResults({})
    if (!review.review_source) api.chat(problemId).then(setMessages)
  }, [problemId, review.review_source])

  useEffect(() => {
    const el = listRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages, sending])

  const send = async (text: string) => {
    const message = text.trim()
    if (!message || sending) return
    setSending(true)
    setError(null)
    setInput('')
    const pending: ChatMessage = {
      id: -Date.now(),
      role: 'user',
      agent: null,
      content: message,
      edits: [],
      applied: false,
      created_at: '',
    }
    setMessages((m) => [...m, pending])
    try {
      const r = await api.chatSend(problemId, { ...review, message, code: getCode(), answer: getAnswer(), current: currentId })
      const reply = r.assistant
      onReply()
      if (r.new_extra || r.deleted_extras.length > 0) onExtras(r.new_extra, r.deleted_extras)
      if (reply.edits.length > 0 && activeId.current === currentId) {
        // 共享编辑框：助教的修改直接写进去
        const res = onEdits(reply.edits)
        setResults((x) => ({ ...x, [reply.id]: res }))
        if (res.applied > 0) {
          reply.applied = true
          void api.chatApplied(problemId, reply.id)
        }
      }
      setMessages((m) => [...m.filter((x) => x.id !== pending.id), r.user, reply])
    } catch (e) {
      setMessages((m) => m.filter((x) => x.id !== pending.id))
      setInput(message)
      setError((e as Error).message)
    } finally {
      setSending(false)
      inputRef.current?.focus()
    }
  }

  const clear = async () => {
    await api.chatClear(problemId)
    setMessages([])
    setResults({})
  }

  const quick: [string, string][] = lastFailed ? [...QUICK, ['这个错误是什么意思', '这个错误是什么意思']] : QUICK

  return (
    <aside className="chat" aria-label="AI 助教">
      <header className="chat-head">
        <Icon name="comment-discussion" /><span className="chat-title">{choice ? '助教' : '助教 · 共享编辑框'}</span>
        <span className="bar-spacer" />
        {messages.length > 0 && (
          <button className="ghost" onClick={clear} title="清空这道题的对话">
            清空
          </button>
        )}
        <button className="icon-btn" onClick={close} title="收起助教（Ctrl+Alt+I）"><Icon name="close" /></button>
      </header>

      {agents.length > 0 && (
        <select className="chat-agent" aria-label="选择助教" value={selected} disabled={agents.length === 1}
          onChange={event => {
            writePref('dojo-ai-agent', event.target.value)
            setSelected(event.target.value)
          }}>
          {agents.map(agent => <option key={agent.id} value={agent.id}>{agent.name} · {agent.model}</option>)}
        </select>
      )}

      <div className="chat-list" ref={listRef}>
        {!aiOn && <p className="faint chat-empty">AI 助教没有开启。安装并登录 Claude Code 或 Codex 后重新打开应用。</p>}
        {aiOn && messages.length === 0 && (
          <p className="faint chat-empty">
            {choice ? '可以问助教怎么看数据，或让它出一道相似的题。' :
              '卡住了就问。助教看得到题目、课、编辑框里的内容和最近一次运行结果，需要时会直接在编辑框里改；想多练就让它出附加题。'}
          </p>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`msg msg-${m.role}`}>
            {m.role === 'user' ? <p>{m.content}</p> : <Markdown>{m.content}</Markdown>}
            {m.edits.length > 0 && <EditsView msg={m} result={results[m.id]} />}
            {m.agent && <small className="chat-author">{m.agent === 'codex' ? 'Codex' : 'Claude'}</small>}
          </div>
        ))}
        {sending && <p className="msg msg-assistant faint">……</p>}
        {error && <p className="tone-fail chat-error">{error}</p>}
      </div>

      <div className="chat-quick">
        {quick.filter(([label]) => !choice || label !== '帮我补一下').map(([label, text]) => (
          <button key={label} className="ghost" disabled={sending || !aiOn} onClick={() => send(text)}>
            {label}
          </button>
        ))}
      </div>
      <textarea
        ref={inputRef}
        className="chat-input"
        value={input}
        disabled={!aiOn}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
            e.preventDefault()
            send(input)
          }
        }}
        placeholder="问助教（Enter 发送，Shift+Enter 换行）"
        rows={3}
      />
    </aside>
  )
}
