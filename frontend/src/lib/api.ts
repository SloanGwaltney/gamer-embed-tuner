const API_BASE = "http://localhost:8000"

export interface Model {
  key: string
  name: string
  description: string
}

export interface ResultItem {
  text: string
  conf: number
}

export interface CompareResponse {
  query: string
  results: Record<string, ResultItem[]>
}

export interface CompareRequest {
  text: string
  models: string[]
  n: number
}

export async function fetchModels(): Promise<Model[]> {
  const res = await fetch(`${API_BASE}/models`)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json() as Promise<Model[]>
}

export async function compareModels(request: CompareRequest): Promise<CompareResponse> {
  const res = await fetch(`${API_BASE}/api/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  const data = (await res.json()) as CompareResponse & { error?: string }
  if (data.error) throw new Error(data.error)
  return data
}
