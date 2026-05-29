# Sudoku Variant Puzzle Edit Assistant — Design Doc & Manual

Built in one session using [Textual](https://github.com/Textualize/textual), a Python TUI framework with the help of Claude LLM.
The assistant transcribes Sudoku variant puzzles from visual sources (YouTube, images) into JSON
that the OmniPuzzleSolver can directly consume.

---

## Why This Exists

Manually transcribing puzzles by hand meant:
- Counting row/column indices by eye from a screenshot
- Typing `[[r1, c1], [r2, c2]]` dozens of times per puzzle
- Keeping parallel arrays (pairs + their values) in sync
- No way to verify coordinates until the solver ran

A single complex puzzle (e.g. 30+ XV pairs + German Whispers lines) took a very long time to
transcribe. With this TUI, you navigate the grid visually and the coordinates are implicit —
you simply cannot get them wrong because you *are* looking at the grid.

---

## Quick Start

```bash
pip install textual
python SimplePuzzleEditAssistant.py
```

**To configure the grid**, edit the class-level constants at the top of `SudokuGrid`:

```python
NRows    = 9      # core grid rows
NCols    = 9      # core grid cols
box_rows = 3      # box height (for Sudoku separators)
box_cols = 3      # box width
IsSudoku = True   # draw box separators?
CELL_W   = 7      # visual width of each cell in characters

# Optional padding (default 0)
NRowsTop    = 0
NRowsBottom = 0
NColsLeft   = 0
NColsRight  = 0
```

Common grid configurations:
| Puzzle type     | NRows | NCols | box_rows | box_cols |
|-----------------|-------|-------|----------|----------|
| Standard 9×9    | 9     | 9     | 3        | 3        |
| 6×6 (2×3 boxes) | 6     | 6     | 2        | 3        |
| 6×6 (3×2 boxes) | 6     | 6     | 3        | 2        |
| 4×4             | 4     | 4     | 2        | 2        |
| 16×16           | 16    | 16    | 4        | 4        |

---

## Controls

### Normal Mode (default)

| Key        | Action                        |
|------------|-------------------------------|
| Arrow keys | Navigate grid                 |
| `I`        | Enter insert mode             |
| `M`        | Switch export mode to matrix  |
| `L`        | Switch export mode to line    |
| `P`        | Switch export mode to pair    |
| `E`        | Export to `puzzle.json`       |
| `Q`        | Quit                          |

### Insert Mode (cursor turns yellow)

| Key              | Action                              |
|------------------|-------------------------------------|
| Arrow keys       | Commit current cell and move        |
| Any printable    | Append to current cell buffer       |
| `_`              | Append underscore (special-cased)   |
| `Backspace`      | Delete last character in buffer     |
| `Delete`         | Wipe cell entirely                  |
| `Escape`         | Commit and return to normal mode    |

> **Note:** `Q` does nothing in insert mode — it just types "q" into the buffer.
> This is intentional. You can only quit from normal mode.

---

## Export Modes

### Matrix Mode (`M`)

Each cell value is written as-is into a 2D grid. Empty cells become `0`.
Covers the full padded grid if padding is non-zero.

**Use for:** Givens (pre-filled digits), RegionSumLinesGridMap, any constraint
that is naturally expressed as a spatial map, like Irregular Sudoku Regions, 
Clone Regions, branched Renban lines, Killer Cages, etc.,

```json
{
  "mode": "matrix",
  "grid": [
    [0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0],
    ...
  ]
}
```

### Line Mode (`L`)

Cell values must follow the format `LineID_PositionID`.

- `LineID` — which line this cell belongs to (number or letter)
- `PositionID` — order of this cell within the line (1, 2, 3, ...)

Example: `1_1`, `1_2`, `1_3` marks the first three cells of line 1.

On export, cells are grouped by `LineID` and sorted by `PositionID`.
The result is a 3D list: outer = lines, inner = ordered `[row, col]` pairs.

**Use for:** GermanWhispersLines, RenbanLines, DutchWhispersLines, ThermoLines,
ArrowLines, PalindromeLines, and any other ordered line constraint.

```json
{
  "mode": "line",
  "lines": [
    [[1, 1], [2, 2], [3, 3], [4, 3]],
    [[0, 3], [1, 4], [1, 5], [0, 6]]
  ]
}
```

> **Why explicit position IDs?** Line order matters for thermos (small→large),
> arrows (bulb first), and palindromes (reading direction). Auto-connecting by
> adjacency is ambiguous when lines branch or loop. Explicit IDs are unambiguous.

> **Loops and branches:** For lines that loop back or branch (some Renban variants),
> use **matrix mode** instead. Mark all cells of a line with its ID number.
> The solver reads the matrix and infers connectivity itself. This handles any
> topology — loops, branches, regions — without needing ordered cell lists.

### Pair Mode (`P`)

A cell can belong to multiple pairs by separating pair IDs with underscores.

- `5` — this cell belongs to pair 5
- `5_6` — this cell belongs to pairs 5 AND 6
- `5_6_7` — this cell belongs to pairs 5, 6, AND 7

Each pair ID must appear in exactly 2 cells. If a pair ID is found in only 1
cell or 3+ cells, it is skipped and a warning toast is shown.

**Use for:** AdditionPairs (XV), DifferencePairs (consecutive/Kropki white),
RatioPairs (Kropki black), and any other constraint defined on cell pairs.

```json
{
  "mode": "pair",
  "pairs": [
    [[0, 2], [0, 3]],
    [[0, 3], [1, 3]],
    [[1, 7], [1, 8]]
  ]
}
```

> **Note:** The TUI only exports coordinates. The constraint type (addition,
> difference, ratio) and its value (sum=10, difference=1, ratio=2) are added
> manually when assembling the final puzzle JSON. This keeps the TUI generic
> and reusable across all pair constraint types.

---

## Padding Cells

Some Sudoku variants add extra rows or columns outside the main grid
(e.g. a row above row 0 for clues). Configure with:

```python
NRowsTop    = 1   # one extra row above
NRowsBottom = 0
NColsLeft   = 1   # one extra column to the left
NColsRight  = 0
```

Padding cells are rendered **dimmed** to distinguish them from the core grid.
A dotted line (`┊` / `─`) marks the boundary between padding and core.

**Coordinate system:** The top-left cell of the *core* grid is always `(0, 0)`.
Padding cells get negative coordinates:
- Top padding row: `(-1, 0)`, `(-1, 1)`, ...
- Left padding column: `(0, -1)`, `(1, -1)`, ...
- Bottom padding row: `(NRows, 0)`, `(NRows, 1)`, ...
- Right padding column: `(0, NCols)`, `(1, NCols)`, ...

All three export modes (matrix, line, pair) use these exported coordinates,
so negative indices flow directly into the solver JSON without remapping.

---

## Design Decisions

### Why Textual?

Textual gives a clean component model — `render()` describes what the widget
looks like, `reactive` variables trigger automatic re-renders, `on_key()`
handles input. No manual screen buffer management, no curses complexity.
The mental model is similar to React but for the terminal.

### Why Vim-style modes?

Normal mode / insert mode prevents accidental edits while navigating.
For puzzle transcription where accuracy matters, this is not just aesthetic —
accidentally typing a digit while scrolling would silently corrupt the puzzle.
`Q` only works in normal mode for the same reason.

### Why implicit commit on arrow key?

Multi-character cell values (e.g. `1_3`, `A_12`) need a confirmation signal.
Arrow key movement felt the most natural — you finish typing and just move on.
`Escape` also commits before returning to normal mode.

### Why `LineID_PositionID` instead of auto-connect?

Auto-connecting adjacent cells by topology is ambiguous:
- Which direction does a diagonal go?
- What if a line crosses itself?
- What if two lines share a cell?

Explicit position IDs are unambiguous and give you full control.
The cost is typing `1_1`, `1_2` instead of just `1` — a reasonable trade.

### Why is `givens` stored in exported coordinates?

`givens` is a `dict` keyed by `(exported_row, exported_col)`, not visual
coordinates. This means the export functions never need to do any coordinate
conversion — they read `givens` directly and the coordinates are already correct.
The only place visual↔exported conversion happens is in `to_exported()`,
called at input time.

### Why `_vsep()` as a single source of truth?

An early bug: the horizontal separator line (`─────`) was wider than the cell
rows because it added joining characters in places where cell rows had no
separator. This caused visual column drift with padding.

The fix was extracting `_vsep(vcol, ec)` — a single function that returns the
separator character for a given column position. Both cell row rendering and
`_h_line()` call this same function, guaranteeing identical widths. The key
insight: vertical separators depend only on *column position*, never on row.

### Why check `ec >= 0 and ec + 1 < NCols` instead of `is_padding()`?

`is_padding()` takes a visual row argument. Inside `_vsep()`, we don't have a
meaningful visual row (separators are column-only). An early version used
`is_padding(0, vcol)` which broke when `NRowsTop > 0` because row 0 was
always a padding row. Using the exported column coordinate `ec` directly
sidesteps this entirely.

---

## Output Format

The solver expects puzzle JSON assembled from multiple TUI exports.
A typical workflow for one puzzle:

1. **Matrix mode** → transcribe the givens grid → paste as `"Matrix"`
2. **Line mode** → transcribe each line type separately → paste as
   `"GermanWhispersLines"`, `"RenbanLines"`, etc.
3. **Pair mode** → transcribe all pairs of one type → paste as
   `"AdditionPairs"`, `"DifferencePairs"`, etc., then add the parallel
   values array (`"AdditionPairsSums"`, etc.) by hand
4. **Matrix mode** again → for region maps like `"RegionSumLinesGridMap"`

Each export overwrites `puzzle.json` in the current directory.
Copy the relevant array out before the next export.