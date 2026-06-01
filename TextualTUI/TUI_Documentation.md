# Sudoku Variant Puzzle Edit Assistant — Design Doc & Manual

This is a Terminal User Interface or TUI built in one session using [Textual](https://github.com/Textualize/textual), a Python TUI framework with the help of Claude LLM.

The assistant helps the user to transcribe Sudoku variant puzzles from visual sources (YouTube, images) into JSON fragments that can be used to create the input JSONs that the OmniSolver can directly consume.

If you want to understand how to use it, skip to the sample example section below.

---

## Why This Exists

To build my OmniSolver, I needed to transcribe many hundreds of puzzles for testing and validation.

Manually transcribing puzzles by hand meant:
- Counting row/column indices by eye from a screenshot/paused video
- Typing `[[r1, c1], [r2, c2]]` dozens of times per puzzle
- Keeping parallel arrays (pairs + their values) in sync
- No way to verify coordinates until the solver ran except for error-free human checking

The issues were obvious. It was a time consuming process and often times it took 20-60 minutes to transcribe extremely hard puzzles with multiple rulesets/constraints. While this was not a big deal for smaller puzzles or puzzles with simpler aesthetics, the pain of manual transcription became unavoidable when dealing with constraint-laden puzzles.

A single complex puzzle (e.g. 30+ XV pairs + German Whispers lines) can take a very long time to transcribe. With this TUI, you navigate the grid visually and enter the values. The coordinates are implicit — you simply cannot get them wrong because you *are* looking at the grid. The coordinate conversion is built implicitly into the assistant and thus it is error free.

The TUI doesn't reduce the chances for error to a zero. It significantly reduces the friction in the transcription. Marking cells with constraints and then retrieving them automatically is easier and more error-free than directly writing the retrieved value just by looking at the puzzle. So, it doesn't replace the need for the manual transcription, it just assists the transcription to make the process faster, less prone to errors, and less taxing. However, the burden of making the transcription accurate still relies on the user.

I did consider to directly take the JSON from the puzzles hosted on Sudokupad, Penpa, and F-Puzzles websites using Marktekfan's [SudokuPad Penpa Converter](https://marktekfan.github.io/sudokupad-penpa-import/). This application gave the JSON from the puzzle links it is fed into. But the JSON schema is inconsistent between puzzles and thus developing a unified converter is hard. The information contained in the JSON is often incomplete and for many puzzles, manual intervention has to happen afterwards. It contains some visual aesthetic information like line widths, line colours, etc., which is useful and cannot be ignored.

After trying to build a converter, the mess due to the lack of non-standardized JSON schema was compounding and it felt pointless. While the JSON provided by this converter and from these sources fit the needs of the interfaces they work, my solver needs boolean flags that enable constraint stacking, and that was something I can't autogenerate from these JSON schemas. The result of this exercise gave birth to a transcription assistant.

---

## Why not make a full transcriber?

It is a trade-off between work needed and the goal to achieve. If too many features were added, this assistant becomes a software on its own. While that is feasible, the development of this assistant takes away from the development of the solver. And for me, the developer of the solver backend and the solver frontent takes more precedence. This assistant was made as a stop-gap to make the transcriptions easier.

This is the same reason why the JSON converter idea that takes the JSON from Marktekfan's [SudokuPad Penpa Converter](https://marktekfan.github.io/sudokupad-penpa-import/) was abandoned.

That said, the full transcriber idea is not closed and shut. I might consider developing this in the future if there is an opening, or think of integrating the changes into the Solver Frontend itself.

---

## Why use AI for this?

This assistant is supposed to be a respite to ease the manual transcription of puzzles and save time. At present, neither do I have adequate knowledge to build a TUI nor any plans in the future to build TUI applications. So, I was okay with using AI LLMs for this. In the future, if I were to expand this into something bigger and sophisticated or build this again from ground-up, I will make this with very little or no AI usage.

---

## Quick Start

To get this running, just install the library/framework and launch the program. It is as easy as that.

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

This setup enables the grid to look like Sudoku grids, or as plane grids as per user needs. Tweaking the parameters is easier due to the TUI application being a simple one script. And if a puzzle has extra rows or columns padded on the sides, you can pad them here.

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

If you're comfortable or familiar with VIM editor, then you'll feel this setup natural. The assistant has two modes. Normal and Insert.

In the Normal mode, you can do non-editing higher-order tasks. In the insert mode, you are restricted to only inserting/modifying inputs.

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

> **Note:** `Q` does nothing in insert mode — it just types "q" into the buffer. This is intentional. You can only quit from normal mode.

---

## Export Modes

The OmniSolver and the other adjacent solvers in the future will all use simple matrix/coordinate system inputs for boundaries, boxes, lines, pairs of cells connected to a particular relation, cells with specific functions/features, etc.,

Keeping this in mind, the export mode exports the inputs into a Matrix, list of line coordinates, or a list of pairs of points accordingly.

### Matrix Mode (`M`)

Each cell value is written as-is into a 2D grid. Empty cells become `0`. Covers the full padded grid if padding is non-zero.

**Use for:** Givens (pre-filled digits), RegionSumLinesGridMap, any constraint
that is naturally expressed as a spatial map, like Irregular Sudoku Regions, 
Clone Regions, branched Renban lines, Killer Cages, etc.,

This can also be used for mapping irregular regions used in puzzles like Nori-Nori, Starbattle, and also as inputs for puzzles like Sumplete.

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

On export, cells are grouped by `LineID` and sorted by `PositionID`. The result is a 3D list: outer = lines, inner = ordered `[row, col]` pairs.

**Use for:** GermanWhispersLines, RenbanLines, DutchWhispersLines, ThermoLines ArrowLines, PalindromeLines, and any other ordered line constraint.

```json
{
  "mode": "line",
  "lines": [
    [[1, 1], [2, 2], [3, 3], [4, 3]],
    [[0, 3], [1, 4], [1, 5], [0, 6]]
  ]
}
```

> **Why explicit position IDs?** Line order matters for thermos (small→large), arrows (bulb first), and palindromes (reading direction). Auto-connecting by adjacency is ambiguous when lines branch or loop. Explicit IDs are unambiguous.

> **Loops and branches:** For lines that loop back or branch (some Renban variants), use **matrix mode** instead. Mark all cells of a line with its ID number. The solver reads the matrix and infers connectivity itself. This handles any topology — loops, branches, regions — without needing ordered cell lists.

### Pair Mode (`P`)

A cell can belong to multiple pairs by separating pair IDs with underscores.

- `5` — this cell belongs to pair 5
- `5_6` — this cell belongs to pairs 5 AND 6
- `5_6_7` — this cell belongs to pairs 5, 6, AND 7

Each pair ID must appear in exactly 2 cells. If a pair ID is found in only 1 cell or 3+ cells, it is skipped and a warning toast is shown.

**Use for:** AdditionPairs (XV), DifferencePairs (consecutive/Kropki white), RatioPairs (Kropki black), and any other constraint defined on cell pairs.

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

> **Note:** The TUI only exports coordinates. The constraint type (addition, difference, ratio) and its value (sum=10, difference=1, ratio=2) are added manually when assembling the final puzzle JSON. This keeps the TUI generic and reusable across all pair constraint types.

---

## Padding Cells

Some Sudoku variants add extra rows or columns outside the main grid (e.g. a row above row 0 for clues/extra solving regions, etc.,). Configure with:

```python
NRowsTop    = 1   # one extra row above
NRowsBottom = 0
NColsLeft   = 1   # one extra column to the left
NColsRight  = 0
```

Padding cells are rendered **dimmed** to distinguish them from the core grid. A dotted line (`┊` / `─`) marks the boundary between padding and core.

**Coordinate system:** The top-left cell of the *core* grid is always `(0, 0)`.
Padding cells get negative coordinates:
- Top padding row: `(-1, 0)`, `(-1, 1)`, ...
- Left padding column: `(0, -1)`, `(1, -1)`, ...
- Bottom padding row: `(NRows, 0)`, `(NRows, 1)`, ...
- Right padding column: `(0, NCols)`, `(1, NCols)`, ...

All three export modes (matrix, line, pair) use these exported coordinates, so negative indices flow directly into the solver JSON without remapping.

---

## Design Decisions

### Why Textual?

Textual gives a clean component model — `render()` describes what the widget
looks like, `reactive` variables trigger automatic re-renders, `on_key()`
handles input. No manual screen buffer management, no curses complexity.
The mental model is similar to React but for the terminal.

From a user point of view, my language of preference is Python and it was quite a relief to see this library existing in Python itself. It was rather intuitive and easy to follow along. So, it was decided to use this.

### Why Vim-style modes?

Normal mode / insert mode prevents accidental edits while navigating.
For puzzle transcription where accuracy matters, this is not just aesthetic —
accidentally typing a digit while scrolling would silently corrupt the puzzle.
`Q` only works in normal mode for the same reason.

This also prevents any accidental command issues. Let's say a puzzle has ``E`` to be entered as an input. In the absence of this mode, typing ``E`` will export the puzzle incompletely.

### Why implicit commit on arrow key?

Multi-character cell values (e.g. `1_3`, `A_12`) need a confirmation signal. Arrow key movement felt the most natural — you finish typing and just move on. `Escape` also commits before returning to normal mode.

In many UIs for Sudoku and other puzzle solving interfaces, for example [SudokuPad](https://sudokupad.app/) by [Sven Neumann](https://svencodes.com/), once you enter a value in a cell, it is registered as is. You don't need to press enter to confirm your choice. Once you enter a value, you click/move to another cell and enter a new value. This style of entry recording is intuitive and seamless.

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

## Importance of User Intervention and Workflow

The OmniSolver and other adjacent puzzle solvers in the future expects the input puzzle in the form of a JSON assembled from multiple TUI exports.

The assistant gives JSON fragments in the exports abiding an export mode. It falls on the user's discretion to pick the right mode for input and export.

Do note that the assistant DOES NOT GIVE THE FINAL format of the JSON expected by the solvers. It gives partial informations. As stated before, it falls on the user's discretion and judgement to transcribe individual parts of the puzzle and assemble them.

A typical workflow for one puzzle is as follows:

1. Analyze the puzzle in hand and identify the input modes for different constraints or variants.
2. Find which puzzle components will benefit from Matrix mode, Line mode, and Pair mode transcribings if present.
3. Transcribe the given constraints one at a time with the right export mode and get the partial JSON in `puzzle.json`.
4. As and when you get the partial JSON, copy-paste the JSON objects (arrays, lists) into the puzzle and add supplementary information as the solver requires.
5. Repeat steps 3 and 4 till the entire puzzle is transcribed.

**IMPORTANT**: Each export overwrites `puzzle.json` in the current directory. Copy the relevant array/list/object out before the next export. Otherwise, the information is lost.

## Sample Example

Take the example of the Sudoku Variant puzzle, [An Advent of Sudoku](https://www.youtube.com/watch?v=lCz_e3Nwij4), made by Philip Newman and solved by Simon Anthony of [Cracking the Cryptic](https://www.youtube.com/@CrackingTheCryptic).

This puzzle has multiple constraints.

So, identify the variants and decide the transcribing mode.

* Classic Sudoku - Just needs a boolean flag in the input JSON. No transcribing needed.
* Disjoint Sudoku - Just needs a boolean flag in the input JSON. No transcribing needed.
* It has givens - This can be transcribed as a 9x9 matrix using the Matrix Mode.
* White Kropki Dots - This can be transcribed as a list of pairs of points using the pair mode.
* Thermometers - This can be transcribed as a list of lines using the line mode.
* Little killer cages - Matrix Mode for the cages.
* Quadruple/Quads - Manual transcribing or a list of cells.
* XV - Pair mode transcribing. Once for Xs and ones for Vs separately.
* Arrow Sums - Line mode transcribing for arrow lines.
* Killer Cage - Matrix mode transcribing for the cages
* Odd/Even cells - Matrix mode transcribing special restricted cells.
* Black Kropki Dots - Pair mode transcribring.

Next, transcribe one variant at a time in the right mode to get the `puzzle.json`. Copy-paste the contents of the JSON into the input accordingly. Ofcourse, add supplementary information manually in the input JSON. When all is done, the final input JSON should look like this.

```json
{
    "url":"https://www.youtube.com/watch?v=lCz_e3Nwij4",
    "title":"Advent Of Sudoku",
    "author":"Philip Newman",
    "PuzzleTestStatus": "Verified",

    "Matrix": [[1, 0, 0, 2, 0, 0, 3, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [4, 0, 0, 5, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7, 0, 0, 8, 0, 0, 9, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    
    "DisjointSudoku": true,

    "DifferencePairsCondition": true,
    "DifferencePairs": [[[0, 1], [0, 2]],
                        [[1, 1], [2, 1]],
                        [[1, 2], [2, 2]]],
    "DifferencePairsDifferences":[1, 1, 1],
    

    "KillerCage": true,
    "KillerCageMap": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 0, 0, 0, 0, 0, 0]],
    "KillerCageSums": [25],

    "OddEvenCell": true,
    "OddEvenCellMap": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0, 0]],

    "LittleKillerCage": true,
    "LittleKillerCageMap": [[0, 0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "LittleKillerCageSums": [12],

    "RatioPairsCondition": true,
    "RatioPairs": [[[6, 7], [6, 8]],
                   [[7, 7], [8, 7]],
                   [[7, 8], [8, 8]]],
    "RatioPairsNumerators":[1, 1, 1],
    "RatioPairsDenominators":[2, 2, 2],

    "ThermometerConstraint": true,
    "Thermometers": [
                        [[1, 5], [1, 4], [2, 4], [2, 5]]
                    ],

    "ArrowSumSudoku": true,
    "ArrowSumSudokuCircles": [[5, 7]],
    "ArrowSumSudokuBodies": [
                            [[4, 8], [3, 7]]
                            ],

    "QuadsCondition": true,
    "QuadIDs": [[4, 0]],
    "QuadVals": [[1, 2]],

    "AdditionPairsCondition": true,
    "AdditionPairs": [
                        [[3, 4], [3, 5]],
                        [[4, 4], [5, 4]],
                        [[4, 5], [5, 5]]
                    ],
    "AdditionPairsSums": [10, 10, 5]
}
```