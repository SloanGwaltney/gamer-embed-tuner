import { AlertCircle, SearchX } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import type { CompareResponse, Model, ResultItem } from "@/lib/api"

interface ResultsPanelProps {
  models: Model[]
  selectedModels: string[]
  results: CompareResponse | null
  loading: boolean
  error: string | null
}

function ConfidenceBadge({ conf }: { conf: number }) {
  const pct = Math.round(conf * 100)
  const colorClass =
    conf >= 0.8
      ? "text-green-400 bg-green-950 border-green-800"
      : conf >= 0.65
        ? "text-yellow-400 bg-yellow-950 border-yellow-800"
        : "text-orange-400 bg-orange-950 border-orange-800"

  return (
    <span
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-mono font-semibold ${colorClass}`}
    >
      {pct}%
    </span>
  )
}

interface ModelColumnProps {
  model: Model
  results: ResultItem[] | undefined
  loading: boolean
  columnIndex: number
}

function ModelColumn({ model, results, loading, columnIndex }: ModelColumnProps) {
  const accentColors = [
    "from-violet-500/10 to-transparent border-violet-500/20",
    "from-cyan-500/10 to-transparent border-cyan-500/20",
    "from-emerald-500/10 to-transparent border-emerald-500/20",
    "from-rose-500/10 to-transparent border-rose-500/20",
  ]
  const headerAccent = accentColors[columnIndex % accentColors.length]

  return (
    <div className="flex flex-col gap-3 min-w-0">
      {/* Column header */}
      <div
        className={`rounded-lg border bg-gradient-to-b ${headerAccent} p-3`}
      >
        <p className="text-xs text-muted-foreground mb-1 font-medium uppercase tracking-wider">
          Model
        </p>
        <p className="text-sm font-semibold font-mono truncate" title={model.name}>
          {model.name}
        </p>
        <p className="text-xs text-muted-foreground mt-1 leading-relaxed line-clamp-2">
          {model.description}
        </p>
        {!loading && results !== undefined && (
          <div className="mt-2">
            <Badge variant="secondary" className="text-xs h-5">
              {results.length} result{results.length !== 1 ? "s" : ""}
            </Badge>
          </div>
        )}
      </div>

      {/* Loading skeletons */}
      {loading && (
        <>
          <Skeleton className="h-28 w-full" />
          <Skeleton className="h-28 w-full" />
          <Skeleton className="h-28 w-full" />
        </>
      )}

      {/* Empty state */}
      {!loading && results !== undefined && results.length === 0 && (
        <Card className="border-dashed border-border/50">
          <CardContent className="flex flex-col items-center justify-center py-10 gap-2 text-center">
            <SearchX className="h-8 w-8 text-muted-foreground/40" />
            <p className="text-sm text-muted-foreground">No results above confidence floor</p>
            <p className="text-xs text-muted-foreground/60">
              Try a different query or lower the threshold in the backend
            </p>
          </CardContent>
        </Card>
      )}

      {/* Result cards */}
      {!loading &&
        results &&
        results.map((item, i) => (
          <Card
            key={i}
            className="border-border/50 transition-colors hover:border-border"
          >
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2 gap-2">
                <span className="text-xs text-muted-foreground tabular-nums">#{i + 1}</span>
                <ConfidenceBadge conf={item.conf} />
              </div>
              <p className="text-sm leading-relaxed text-foreground/85">{item.text}</p>
            </CardContent>
          </Card>
        ))}
    </div>
  )
}

export function ResultsPanel({
  models,
  selectedModels,
  results,
  loading,
  error,
}: ResultsPanelProps) {
  const displayModels = models.filter((m) => selectedModels.includes(m.key))
  const colCount = displayModels.length || 1

  return (
    <div className="mt-10">
      {/* Section header */}
      <div className="flex items-baseline gap-3 mb-5">
        <h2 className="text-lg font-semibold">Results</h2>
        {results && (
          <p className="text-sm text-muted-foreground truncate">
            for &ldquo;{results.query}&rdquo;
          </p>
        )}
      </div>

      {/* Error */}
      {error && (
        <Card className="border-destructive/50 mb-4">
          <CardContent className="flex items-center gap-3 py-4">
            <AlertCircle className="h-5 w-5 text-destructive shrink-0" />
            <p className="text-sm text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Grid of model columns */}
      {!error && (
        <div
          className="grid gap-5"
          style={{ gridTemplateColumns: `repeat(${colCount}, minmax(0, 1fr))` }}
        >
          {displayModels.map((model, i) => (
            <ModelColumn
              key={model.key}
              model={model}
              results={results?.results[model.key]}
              loading={loading}
              columnIndex={i}
            />
          ))}
        </div>
      )}
    </div>
  )
}
