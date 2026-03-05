import { useEffect, useState } from "react"
import { ModelSelector } from "@/components/ModelSelector"
import { QueryPanel } from "@/components/QueryPanel"
import { ResultsPanel } from "@/components/ResultsPanel"
import { compareModels, fetchModels } from "@/lib/api"
import type { CompareResponse, Model } from "@/lib/api"

export default function App() {
  // Model list
  const [models, setModels] = useState<Model[]>([])
  const [modelsLoading, setModelsLoading] = useState(true)
  const [modelsError, setModelsError] = useState<string | null>(null)

  // Selection state
  const [selectedModels, setSelectedModels] = useState<string[]>([])
  const [query, setQuery] = useState("")
  const [n, setN] = useState(3)

  // Compare state
  const [comparing, setComparing] = useState(false)
  const [results, setResults] = useState<CompareResponse | null>(null)
  const [compareError, setCompareError] = useState<string | null>(null)
  const [hasCompared, setHasCompared] = useState(false)

  useEffect(() => {
    fetchModels()
      .then((data) => {
        setModels(data)
        setSelectedModels(data.map((m) => m.key))
      })
      .catch((err: unknown) =>
        setModelsError(err instanceof Error ? err.message : "Unknown error")
      )
      .finally(() => setModelsLoading(false))
  }, [])

  const handleCompare = async () => {
    if (!query.trim() || selectedModels.length === 0) return
    setComparing(true)
    setCompareError(null)
    setResults(null)
    setHasCompared(true)

    try {
      const data = await compareModels({ text: query, models: selectedModels, n })
      setResults(data)
    } catch (err: unknown) {
      setCompareError(err instanceof Error ? err.message : "Unknown error")
    } finally {
      setComparing(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Top glow accent */}
      <div
        aria-hidden
        className="pointer-events-none fixed top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/60 to-transparent"
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Header */}
        <header className="mb-10">
          <div className="flex items-start gap-3">
            <span className="text-2xl leading-tight">🎮</span>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">GamerLink RAG Comparator</h1>
              <p className="text-muted-foreground text-sm mt-1">
                Compare embedding models side-by-side against your gaming support ticket corpus
              </p>
            </div>
          </div>
        </header>

        {/* Config row — models left, query right */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
          <ModelSelector
            models={models}
            selected={selectedModels}
            onChange={setSelectedModels}
            loading={modelsLoading}
            error={modelsError}
          />
          <QueryPanel
            query={query}
            onQueryChange={setQuery}
            n={n}
            onNChange={setN}
            onSubmit={handleCompare}
            loading={comparing}
            disabled={selectedModels.length === 0 || modelsLoading}
          />
        </div>

        {/* Divider */}
        {hasCompared && (
          <div className="h-px w-full bg-border mt-6" />
        )}

        {/* Results */}
        {hasCompared && (
          <ResultsPanel
            models={models}
            selectedModels={selectedModels}
            results={results}
            loading={comparing}
            error={compareError}
          />
        )}
      </div>
    </div>
  )
}
