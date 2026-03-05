import { Loader2, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface QueryPanelProps {
  query: string
  onQueryChange: (v: string) => void
  n: number
  onNChange: (v: number) => void
  onSubmit: () => void
  loading: boolean
  disabled: boolean
}

export function QueryPanel({
  query,
  onQueryChange,
  n,
  onNChange,
  onSubmit,
  loading,
  disabled,
}: QueryPanelProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault()
      onSubmit()
    }
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Query</CardTitle>
        <CardDescription>Type a prompt to retrieve similar support tickets</CardDescription>
      </CardHeader>

      <CardContent className="flex flex-col gap-4 flex-1">
        <Textarea
          placeholder="e.g. my game keeps crashing when I open the inventory..."
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 min-h-[120px] text-sm"
          disabled={loading}
        />

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs text-muted-foreground font-medium">
              Results per model
            </label>
            <span className="text-sm font-mono font-semibold text-primary tabular-nums w-4 text-right">
              {n}
            </span>
          </div>
          <Slider
            min={1}
            max={10}
            step={1}
            value={[n]}
            onValueChange={([v]) => onNChange(v)}
            disabled={loading}
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>1</span>
            <span>10</span>
          </div>
        </div>

        <Button
          onClick={onSubmit}
          disabled={disabled || loading || !query.trim()}
          className="w-full gap-2"
          size="lg"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Comparing...
            </>
          ) : (
            <>
              <Zap className="h-4 w-4" />
              Compare
              <span className="text-xs opacity-60 ml-1">Ctrl+Enter</span>
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
