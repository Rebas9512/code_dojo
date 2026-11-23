import { useEffect, useRef, useState, type KeyboardEvent, type ReactNode } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { practicePath, type MapUnit, type TrackInfo } from '../api'
import { ProblemStatus } from '../components/ProblemStatus'
import { readPref, writePref } from '../theme'
import { useTracks } from '../tracks'
import { unitAnchor } from './unitAnchor'
import { mapTree, type Branch, type MapTab, type Station } from './mapTree'
import './map.css'

const tabNames = { python: 'Python', sql: 'SQL' } as const
const tabs: MapTab[] = ['python', 'sql']
const shortName = (name: string) => Array.from(name).length > 6 ? Array.from(name).slice(0, 5).join('') + '…' : name

function SkillList({ skills }: { skills: MapUnit['skills'] }) {
  const renderSkill = (skill: MapUnit['skills'][number]) =>
    <li key={skill.id}><ProblemStatus status={skill.status} />{skill.name}</li>
  return <section className="unit-skills">
    <h3>知识点 <span>{skills.length}</span></h3>
    <ul>{skills.slice(0, 10).map(renderSkill)}</ul>
    {skills.length > 10 && <details><summary>其余 {skills.length - 10} 个</summary>
      <ul>{skills.slice(10).map(renderSkill)}</ul>
    </details>}
  </section>
}

function UnitDetails({ station, onReturn }: { station: Station; onReturn: () => void }) {
  const { track, stage, unit } = station
  const base = '/t/' + track.id
  const hash = '#' + unitAnchor(stage.id, unit.id)
  const planned = track.status === 'planned'
  return <aside className="unit-detail" aria-labelledby="unit-title" id="unit-detail">
    <div className="unit-crumb"><Link to={base}>{track.name}</Link> <span aria-hidden="true">›</span> {stage.name}</div>
    <h2 id="unit-title" tabIndex={-1}>{unit.name}</h2>
    {planned ? <p className="unit-plan">规划中 · {stage.name}</p> : <>
      <div className="unit-progress"><span>已通过</span><strong>{unit.solved} <small>/ {unit.total}</small></strong></div>
      <div className="unit-meter" aria-hidden="true"><i style={{ width: (unit.total ? 100 * unit.solved / unit.total : 0) + '%' }} /></div>
      <div className="unit-progress"><span>掌握</span><strong>{unit.mastered} <small>/ {unit.skills.length}</small></strong></div>
      {unit.skills.length > 0 && <SkillList skills={unit.skills} />}
      {unit.next && <Link className="unit-continue" to={practicePath(unit.next)}>继续：{unit.next.title}<span aria-hidden="true">→</span></Link>}
    </>}
    <nav className="unit-links" aria-label="单元内容">
      <Link to={base + hash}>题目</Link><Link to={base + '/skills' + hash}>知识点</Link>
    </nav>
    <button type="button" className="map-return" onClick={onReturn}>↑ 返回单元</button>
  </aside>
}

interface TreeProps {
  branches: Branch[]
  tracks: TrackInfo[]
  selected?: string
  next?: string
  onSelect: (key: string, openDetail: boolean) => void
}

function moveStation(event: KeyboardEvent<HTMLButtonElement>, onSelect: TreeProps['onSelect']) {
  const { key, currentTarget } = event
  if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(key)) return
  event.preventDefault()
  const chain = currentTarget.closest<HTMLElement>('.unit-chain')!
  const stations = (row: HTMLElement) => Array.from(row.querySelectorAll<HTMLButtonElement>('.station'))
  let target
  if (key === 'ArrowLeft' || key === 'ArrowRight') {
    const buttons = stations(chain)
    target = buttons[buttons.indexOf(currentTarget) + (key === 'ArrowLeft' ? -1 : 1)]
  } else {
    const rows = Array.from(chain.closest('.map-tree')!.querySelectorAll<HTMLElement>('.unit-chain'))
    const row = rows[rows.indexOf(chain) + (key === 'ArrowUp' ? -1 : 1)]
    if (row) {
      const center = (button: HTMLElement) => {
        const rect = button.getBoundingClientRect()
        return rect.left + rect.width / 2
      }
      const x = center(currentTarget)
      const buttons = stations(row)
      if (buttons.length) target = buttons.reduce((a, b) => Math.abs(center(a) - x) <= Math.abs(center(b) - x) ? a : b)
    }
  }
  if (target) {
    target.focus()
    // 方向键留在树里，回车才在窄屏定位到详情。
    onSelect(target.dataset.key!, false)
  }
}

function UnitChain({ name, children }: { name: string; children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const chain = ref.current!
    function edges() {
      chain.toggleAttribute('data-more-left', chain.scrollLeft > 1)
      chain.toggleAttribute('data-more-right', chain.scrollLeft + chain.clientWidth < chain.scrollWidth - 1)
    }
    const observer = new ResizeObserver(edges)
    observer.observe(chain)
    for (const stage of chain.children) observer.observe(stage)
    chain.addEventListener('scroll', edges, { passive: true })
    edges()
    return () => {
      observer.disconnect()
      chain.removeEventListener('scroll', edges)
    }
  }, [children])
  return <div ref={ref} className="unit-chain" role="group" aria-label={name + '单元'}>{children}</div>
}

function BranchList(props: TreeProps) {
  const { branches, tracks, next, selected, onSelect } = props
  const navigate = useNavigate()
  const wrangle = tracks.find((t) => t.id === 'wrangle') ?? tracks.find((t) => t.id === 'data' && t.language === 'python')
  return <ul className="map-branches">{branches.map((branch) => {
    const { track, stations, children } = branch
    const planned = track.status === 'planned'
    return <li key={track.id}>
      <div className={'track-line' + (planned ? ' is-planned' : '')}>
        <div className="route-heading">
          <h2><Link to={'/t/' + track.id}>{track.name}</Link></h2>
          <div className="route-meta"><span>已通过 {track.solved} / {track.total}</span>{!planned && <span>掌握 {track.mastered} / {track.skills}</span>}{planned && '规划中'}</div>
          {track.requires.length > 1 && <div className="route-note">也要先学：{track.requires.slice(1).map((id, i) =>
            <span key={id}>{i > 0 && '、'}<Link to={'/t/' + id}>{tracks.find((t) => t.id === id)?.name ?? id}</Link></span>)}</div>}
        </div>
        <div className="route-path">
          <UnitChain name={track.name}>
            {track.stages.map(stage => <div className="station-stage" key={stage.id} role="group" aria-label={stage.name}>
              {stations.filter(s => s.stage.id === stage.id).map(s => {
                const { unit } = s
                const upcoming = s.key === next
                const fill = unit.total ? unit.solved / unit.total : 0
                const label = [s.stage.name, unit.name, planned ? '规划中' : `已通过 ${unit.solved} / ${unit.total}`,
                  unit.assisted ? '含 AI 协助' : '', upcoming ? '下一步' : ''].filter(Boolean).join('，')
                return <button key={s.key} type="button" className="station"
                  data-key={s.key} aria-pressed={selected === s.key} aria-controls="unit-detail" aria-label={label}
                  title={label + '（双击进入题目）'} onClick={() => onSelect(s.key, true)}
                  onDoubleClick={() => navigate(`/t/${track.id}#${unitAnchor(s.stage.id, unit.id)}`)}
                  onKeyDown={(e) => moveStation(e, onSelect)}>
                  <span className={'station-dot' + (upcoming ? ' is-next' : '') + (fill === 1 ? ' is-complete' : '')}>
                    {fill > 0 && fill < 1 && <svg className="station-arc" viewBox="0 0 16 16" aria-hidden="true">
                      <circle cx="8" cy="8" r="6" pathLength="100" strokeDasharray={`${100 * fill} 100`} />
                    </svg>}
                    {unit.assisted > 0 && <i className="assist-mark" />}
                  </span>
                  <span className="station-name">{shortName(unit.name)}</span>
                </button>
              })}
            </div>)}
          </UnitChain>
          {track.id === 'sql' && wrangle && <div className="pandas-note">pandas 互通：
            <Link to={'/t/' + wrangle.id}>{wrangle.name}{wrangle.status === 'planned' && '（规划中）'}</Link>
          </div>}
        </div>
      </div>
      {children.length > 0 && <BranchList {...props} branches={children} />}
    </li>
  })}</ul>
}

function TabTree({ tracks, tab }: { tracks: TrackInfo[]; tab: MapTab }) {
  const { roots, stations, next } = mapTree(tracks, tab)
  const [chosen, setChosen] = useState<string | null>(null)
  const tree = useRef<HTMLDivElement>(null)
  const selected = stations.find((s) => s.key === chosen) ?? next ?? stations[0]
  const selectedKey = selected?.key
  useEffect(() => {
    const button = tree.current?.querySelector<HTMLButtonElement>('[aria-pressed="true"]')
    const chain = button?.closest<HTMLElement>('.unit-chain')
    if (!button || !chain) return
    const rect = button.getBoundingClientRect()
    const bounds = chain.getBoundingClientRect()
    if (rect.left < bounds.left) chain.scrollLeft += rect.left - bounds.left
    if (rect.right > bounds.right) chain.scrollLeft += rect.right - bounds.right
  }, [selectedKey])
  function select(key: string, openDetail: boolean) {
    setChosen(key)
    if (openDetail && window.matchMedia('(max-width: 800px)').matches) {
      requestAnimationFrame(() => document.getElementById('unit-title')?.focus())
    }
  }
  return <div className="map-layout" role="tabpanel" id="map-panel" aria-labelledby={'tab-' + tab}>
    <div className="map-tree" ref={tree}>
      <BranchList tracks={tracks} branches={roots} next={next?.key} selected={selectedKey} onSelect={select} />
      {!roots.length && <p className="muted">暂时没有学习线</p>}
    </div>
    {selected && <UnitDetails key={selected.key} station={selected}
      onReturn={() => tree.current?.querySelector<HTMLButtonElement>('[aria-pressed="true"]')?.focus()} />}
  </div>
}

export function MapPage() {
  const tracks = useTracks()
  const [params, setParams] = useSearchParams()
  const query = params.get('tab')
  const tab: MapTab = (query ?? readPref('dojo-map-tab', 'python')) === 'sql' ? 'sql' : 'python'
  useEffect(() => {
    writePref('dojo-map-tab', tab)
    if (!query && tab === 'sql') setParams({ tab }, { replace: true })
  }, [tab, query, setParams])
  return <main className="learning-map">
    <header className="map-bar">
      <div className="map-tabs" role="tablist" aria-label="学习路线">
        {tabs.map((key) => <button key={key} id={'tab-' + key} role="tab" aria-controls="map-panel"
          tabIndex={tab === key ? 0 : -1} aria-selected={tab === key} onClick={() => setParams({ tab: key })}
          onKeyDown={(e) => {
            if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) {
              e.preventDefault()
              const dest = e.key === 'Home' ? 'python' : e.key === 'End' ? 'sql' : tab === 'python' ? 'sql' : 'python'
              document.getElementById('tab-' + dest)?.focus()
              setParams({ tab: dest })
            }
          }}>{tabNames[key]}</button>)}
      </div>
      <div className="map-legend"><span><i className="legend-next" />下一步</span><span><i className="legend-assist" />AI 协助</span></div>
    </header>
    <TabTree key={tab} tracks={tracks} tab={tab} />
  </main>
}
