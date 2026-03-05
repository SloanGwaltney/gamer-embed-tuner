import { Checkbox } from "@/components/ui/checkbox"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Model } from "@/lib/api"

interface ModelSelectorProps {
  models: Model[]
  selected: string[]
  onChange: (selected: string[]) => void
  loading: boolean
  error: string | null
}

export function ModelSelector({ models, selected, onChange, loading, error }: ModelSelectorProps) {
  const toggle = (key: string) => {
    onChange(
      selected.includes(key) ? selected.filter((k) => k !== key) : [...selected, key]
    )
  }

  const allSelected = models.length > 0 && selected.length === models.length
  const toggleAll = () => onChange(allSelected ? [] : models.map((m) => m.key))

  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Models</CardTitle>
          {!loading && models.length > 1 && (
            <button
              onClick={toggleAll}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              {allSelected ? "Deselect all" : "Select all"}
            </button>
          )}
        </div>
        <CardDescription>Choose which embedding models to compare</CardDescription>
      </CardHeader>

      <CardContent className="space-y-2">
        {loading && (
          <>
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </>
        )}

        {error && (
          <div className="rounded-md bg-destructive/10 border border-destructive/30 p-3">
            <p className="text-sm text-destructive">Failed to load models: {error}</p>
            <p className="text-xs text-muted-foreground mt-1">Is the API running on localhost:8000?</p>
          </div>
        )}

        {!loading &&
          !error &&
          models.map((model) => (
            <div
              key={model.key}
              onClick={() => toggle(model.key)}
              className="flex items-start gap-3 rounded-md border border-border p-3 cursor-pointer transition-colors hover:bg-accent/40 hover:border-primary/40"
              style={{
                backgroundColor: selected.includes(model.key)
                  ? "hsl(var(--accent) / 0.5)"
                  : undefined,
                borderColor: selected.includes(model.key)
                  ? "hsl(var(--primary) / 0.4)"
                  : undefined,
              }}
            >
              <Checkbox
                id={model.key}
                checked={selected.includes(model.key)}
                onCheckedChange={() => toggle(model.key)}
                onClick={(e) => e.stopPropagation()}
                className="mt-0.5 shrink-0"
              />
              <div className="flex-1 min-w-0">
                <label
                  htmlFor={model.key}
                  className="text-sm font-medium font-mono cursor-pointer leading-none"
                >
                  {model.name}
                </label>
                <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                  {model.description}
                </p>
              </div>
            </div>
          ))}

        {!loading && !error && selected.length === 0 && models.length > 0 && (
          <p className="text-xs text-destructive text-center py-1">
            Select at least one model to run a comparison
          </p>
        )}
      </CardContent>
    </Card>
  )
}
