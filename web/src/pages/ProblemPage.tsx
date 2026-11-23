import { useLoaderData, useLocation, useOutletContext } from 'react-router-dom'
import type { ProblemDetail } from '../api'
import { ProblemWorkspace } from '../components/ProblemWorkspace'
import type { Theme } from '../theme'

export function ProblemPage() {
  const location = useLocation()
  const parent = useLoaderData() as ProblemDetail
  const theme = useOutletContext<Theme>()
  return <ProblemWorkspace key={parent.id + location.search} parent={parent} theme={theme} />
}
