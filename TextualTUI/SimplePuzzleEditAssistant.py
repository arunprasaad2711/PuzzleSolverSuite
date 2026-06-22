from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.reactive import reactive
from textual import events
from rich.text import Text
from collections import defaultdict
import json


class SudokuGrid(Static):

    can_focus = True

    CELL_W = 7

    # Core grid size
    NRows = 9
    NCols = 9

    # For Sudoku grid
    # For a 4x4 grid: box_rows=2, box_cols=2
    # For a 9x9 grid: box_rows=3, box_cols=3
    # For a 6x6 grid 2x3 style: box_rows=2, box_cols=3
    # For a 6x6 grid 3x2 style: box_rows=3, box_cols=2
    # For a 16x16 grid: box_rows=4, box_cols=4

    box_rows = 3
    box_cols = 3

    IsSudoku = True

    # Padding around the core grid
    # Exported coordinates for padding cells will be negative (top/left)
    # or >= NRows/NCols (bottom/right)
    NRowsTop    = 0
    NRowsBottom = 0
    NColsLeft   = 0
    NColsRight  = 0

    total_rows = NRowsTop  + NRows + NRowsBottom
    total_cols = NColsLeft + NCols + NColsRight

    cursor_row: reactive[int] = reactive(0)  # visual row index
    cursor_col: reactive[int] = reactive(0)  # visual col index
    insert_mode: reactive[bool] = reactive(False)
    export_mode: reactive[str] = reactive("matrix")  # "matrix", "line", or "pair"

    def __init__(self):
        super().__init__()
        self.givens = {}   # (exported_row, exported_col) -> str
        self.buffer = ""   # accumulates keystrokes for current cell

    # -- Coordinate helpers ---------------------------------------------------

    def to_exported(self, visual_row, visual_col):
        """Convert visual (0-based) coordinates to exported coordinates."""
        return (visual_row - self.NRowsTop, visual_col - self.NColsLeft)

    def is_padding(self, visual_row, visual_col):
        """True if this visual cell is outside the core grid."""
        er, ec = self.to_exported(visual_row, visual_col)
        return er < 0 or er >= self.NRows or ec < 0 or ec >= self.NCols

    # -- Buffer / movement ----------------------------------------------------

    def _commit_buffer(self):
        cell = self.to_exported(self.cursor_row, self.cursor_col)
        if self.buffer:
            self.givens[cell] = self.buffer
        else:
            self.givens.pop(cell, None)
        self.buffer = ""

    def _move(self, drow, dcol):
        self._commit_buffer()
        self.cursor_row = max(0, min(self.total_rows - 1, self.cursor_row + drow))
        self.cursor_col = max(0, min(self.total_cols - 1, self.cursor_col + dcol))
        ec = self.to_exported(self.cursor_row, self.cursor_col)
        self.buffer = self.givens.get(ec, "")
        self.refresh()

    # -- Rendering ------------------------------------------------------------

    def _vsep(self, vcol, ec):
        """Return the vertical separator character after column vcol, or '' if none.
        Depends only on column position so every row has identical separators."""
        if vcol >= self.total_cols - 1:
            return ""
        is_left_pad_boundary  = (vcol + 1 == self.NColsLeft)
        is_right_pad_boundary = (vcol + 1 == self.NColsLeft + self.NCols)
        if is_left_pad_boundary or is_right_pad_boundary:
            return "\u250a"   # dotted vertical: padding boundary
        # Both columns are in core if ec >= 0 and ec+1 < NCols
        both_in_core = (ec >= 0 and ec + 1 < self.NCols)
        if self.IsSudoku and both_in_core and (ec + 1) % self.box_cols == 0:
            return "\u2502"   # solid vertical: box boundary within core
        return ""

    def _h_line(self):
        """Horizontal separator line that exactly mirrors _vsep width."""
        w = self.CELL_W
        parts = []
        for vcol in range(self.total_cols):
            parts.append("\u2500" * w)
            _, ec = self.to_exported(0, vcol)
            sep = self._vsep(vcol, ec)
            if sep:
                parts.append("\u253c")   # cross wherever a vertical sep would be
            # no extra char where _vsep returns '' -- keeps widths identical
        return "".join(parts) + "\n"

    def render(self) -> Text:
        t = Text()
        w = self.CELL_W

        for vrow in range(self.total_rows):
            er_row, _ = self.to_exported(vrow, 0)

            for vcol in range(self.total_cols):
                is_cursor  = (vrow == self.cursor_row and vcol == self.cursor_col)
                in_padding = self.is_padding(vrow, vcol)
                er, ec     = self.to_exported(vrow, vcol)

                if is_cursor and self.insert_mode:
                    display = (self.buffer + "\u258c") if self.buffer else "\u258c"
                else:
                    val = self.givens.get((er, ec))
                    display = val if val else "\u00b7"

                cell_text = display.center(w)

                if is_cursor:
                    style = "black on yellow" if self.insert_mode else "black on white"
                elif in_padding:
                    style = "dim"   # visually distinguish padding cells
                else:
                    style = ""

                t.append(cell_text, style=style)

                sep = self._vsep(vcol, ec)
                if sep:
                    t.append(sep)

            t.append("\n")

            # Horizontal separator after this row (not after last row)
            if vrow < self.total_rows - 1:
                curr_is_pad_row = vrow < self.NRowsTop or vrow >= self.NRowsTop + self.NRows
                next_is_pad_row = (vrow + 1) < self.NRowsTop or (vrow + 1) >= self.NRowsTop + self.NRows

                if curr_is_pad_row != next_is_pad_row:
                    # padding boundary row -- always draw
                    t.append(self._h_line())
                elif not curr_is_pad_row and self.IsSudoku:
                    # both in core -- draw on box boundary
                    if (er_row + 1) % self.box_rows == 0 and er_row + 1 < self.NRows:
                        t.append(self._h_line())

        # Status bar -- show exported coordinates
        er, ec = self.to_exported(self.cursor_row, self.cursor_col)
        t.append("\n")
        mode_str   = "[INSERT]" if self.insert_mode else "[NORMAL]"
        export_str = f"export: {self.export_mode}"
        coord_str  = f"({er}, {ec})"
        mode_color = "yellow" if self.insert_mode else "white"
        t.append(f" {mode_str}  {export_str}  cursor: {coord_str}", style=mode_color)

        return t

    # -- Key handling ---------------------------------------------------------

    def on_key(self, event: events.Key) -> None:

        SPECIAL_CHARS = {
            "underscore": "_",
            "minus": "-",
            "plus": "+",
            "slash": "/",
        }

        if self.insert_mode:
            if event.key == "escape":
                self._commit_buffer()
                self.insert_mode = False
            elif event.key == "up":
                self._move(-1, 0)
            elif event.key == "down":
                self._move(1, 0)
            elif event.key == "left":
                self._move(0, -1)
            elif event.key == "right":
                self._move(0, 1)
            elif event.key == "backspace":
                self.buffer = self.buffer[:-1]
                self.refresh()
            elif event.key == "delete":
                self.buffer = ""
                self.givens.pop(self.to_exported(self.cursor_row, self.cursor_col), None)
                self.refresh()
            elif len(event.key) == 1 and event.key.isprintable():
                self.buffer += event.key
                self.refresh()
            elif event.key in SPECIAL_CHARS:
                self.buffer += SPECIAL_CHARS[event.key]
                self.refresh()

        else:  # normal mode
            if event.key == "up":
                self.cursor_row = max(0, self.cursor_row - 1)
            elif event.key == "down":
                self.cursor_row = min(self.total_rows - 1, self.cursor_row + 1)
            elif event.key == "left":
                self.cursor_col = max(0, self.cursor_col - 1)
            elif event.key == "right":
                self.cursor_col = min(self.total_cols - 1, self.cursor_col + 1)
            elif event.key == "i":
                self.buffer = self.givens.get(self.to_exported(self.cursor_row, self.cursor_col), "")
                self.insert_mode = True
            elif event.key == "m":
                self.export_mode = "matrix"
            elif event.key == "l":
                self.export_mode = "line"
            elif event.key == "p":
                self.export_mode = "pair"
            elif event.key == "e":
                self._export()
            elif event.key == "q":
                self.app.exit()

        self.refresh()

    # -- Parsers --------------------------------------------------------------

    def _parse_cell_id(self, value: str):
        """Parse 'LineID_PositionID' into (line_id, position_id).
        Returns None if the value is not a valid line ID."""
        if "_" not in value:
            return None
        parts = value.split("_", 1)
        line_id = parts[0].strip()
        pos_id  = parts[1].strip()
        if not line_id or not pos_id:
            return None
        # Use numeric sort if possible, else string sort
        try:
            return (line_id, int(pos_id))
        except ValueError:
            return (line_id, pos_id)

    def _parse_pair_ids(self, value: str):
        """Parse a cell value into a list of pair IDs.
        A cell with value '5_6_7' belongs to pairs 5, 6, and 7."""
        parts = [p.strip() for p in value.split("_") if p.strip()]
        return parts if parts else []

    # -- Serializers ----------------------------------------------------------

    def compact_lines(self, data):
        """Serialize with inner [row, col] pairs kept on one line."""
        lines_str = []
        for line in data["lines"]:
            cells = ", ".join(f"[{r}, {c}]" for r, c in line)
            lines_str.append(f"    [{cells}]")
        inner = ",\n".join(lines_str)
        return f'{{\n  "mode": "line",\n  "lines": [\n{inner}\n  ]\n}}'

    def compact_matrix(self, data):
        """Serialize with each row on one line."""
        rows_str = []
        for row in data["grid"]:
            cells = ", ".join(str(v) for v in row)
            rows_str.append(f"    [{cells}]")
        inner = ",\n".join(rows_str)
        return f'{{\n  "mode": "matrix",\n  "grid": [\n{inner}\n  ]\n}}'

    def compact_pairs(self, data):
        """Serialize with each pair on one line."""
        pairs_str = []
        for pair in data["pairs"]:
            (r1, c1), (r2, c2) = pair
            pairs_str.append(f"    [[{r1}, {c1}], [{r2}, {c2}]]")
        inner = ",\n".join(pairs_str)
        return f'{{\n  "mode": "pair",\n  "pairs": [\n{inner}\n  ]\n}}'

    # -- Export ---------------------------------------------------------------

    def _export(self):
        if self.export_mode == "matrix":
            # Matrix covers the full padded grid
            grid = []
            for vrow in range(self.total_rows):
                row = []
                for vcol in range(self.total_cols):
                    er, ec = self.to_exported(vrow, vcol)
                    row.append(self.givens.get((er, ec), 0))
                grid.append(row)
            data = {"mode": "matrix", "grid": grid}
            with open("puzzle.json", "w") as f:
                f.write(self.compact_matrix(data))

        elif self.export_mode == "line":
            # Group cells by LineID, sorted by PositionID within each line
            lines: dict[str, list] = defaultdict(list)

            for (er, ec), v in self.givens.items():
                parsed = self._parse_cell_id(v)
                if parsed is None:
                    continue
                line_id, pos_id = parsed
                lines[line_id].append((pos_id, er, ec))

            # Sort outer list by LineID (numeric if possible, else string)
            def line_sort_key(k):
                try:
                    return (0, int(k))
                except ValueError:
                    return (1, k)

            result = []
            for line_id in sorted(lines.keys(), key=line_sort_key):
                cells = sorted(lines[line_id], key=lambda x: x[0])  # sort by pos_id
                result.append([[r, c] for _, r, c in cells])

            data = {"mode": "line", "lines": result}
            with open("puzzle.json", "w") as f:
                f.write(self.compact_lines(data))

        elif self.export_mode == "pair":
            # For each pair ID, collect all cells that contain it
            pair_cells: dict[str, list] = defaultdict(list)

            for (er, ec), v in self.givens.items():
                for pair_id in self._parse_pair_ids(v):
                    pair_cells[pair_id].append((er, ec))

            # Sort by pair ID (numeric if possible, else string)
            def pair_sort_key(k):
                try:
                    return (0, int(k))
                except ValueError:
                    return (1, k)

            pairs = []
            warnings = []
            for pair_id in sorted(pair_cells.keys(), key=pair_sort_key):
                cells = pair_cells[pair_id]
                if len(cells) != 2:
                    warnings.append(f"pair {pair_id} has {len(cells)} cell(s) -- skipped")
                    continue
                pairs.append(cells)

            data = {"mode": "pair", "pairs": pairs}
            with open("puzzle.json", "w") as f:
                f.write(self.compact_pairs(data))

            if warnings:
                self.app.notify(f"Warnings: {'; '.join(warnings)}", severity="warning")

        self.app.notify("Exported to puzzle.json")


class GridApp(App):

    CSS = """
    SudokuGrid {
        width: 100%;
        height: 100%;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield SudokuGrid()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(SudokuGrid).focus()


if __name__ == "__main__":
    GridApp().run()