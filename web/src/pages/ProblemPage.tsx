import { useLoaderData, useLocation, useOutletContext } from 'react-router-dom'
import type { WorkspaceData } from '../api'
import { ProblemWorkspace } from '../components/ProblemWorkspace'
import type { Theme } from '../theme'

export function ProblemPage() {
  const location = useLocation()
  const data = useLoaderData() as WorkspaceData
  const theme = useOutletContext<Theme>()
  return <ProblemWorkspace key={data.parent.id + location.search} data={data} theme={theme} />
}
