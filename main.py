"""Sudoku Solver Using Recursive Backtracking - DAA Assignment 2.
Tkinter desktop GUI styled as a clean dashboard.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from copy import deepcopy

BG = "#F4F7FB"
WHITE = "#FFFFFF"
NAVY = "#172554"
BLUE = "#2447B8"
BLUE_DARK = "#18358F"
BLUE_LIGHT = "#E8EEFF"
TEXT = "#172033"
MUTED = "#64748B"
BORDER = "#CFD8E6"
GREEN = "#16803D"
GREEN_BG = "#DCFCE7"
RED = "#C52222"
RED_BG = "#FEE2E2"
AMBER = "#B45309"
AMBER_BG = "#FEF3C7"
GIVEN = "#EEF2F8"

SAMPLE = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9],
]


SAMPLES = {
    "Sample 1 — Easy": SAMPLE,
    "Sample 2 — Medium": [
        [0,0,0,2,6,0,7,0,1], [6,8,0,0,7,0,0,9,0], [1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0], [0,0,4,6,0,2,9,0,0], [0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4], [0,4,0,0,5,0,0,3,6], [7,0,3,0,1,8,0,0,0]
    ],
    "Sample 3 — Challenging": [
        [0,0,0,0,0,0,0,1,2], [0,0,0,0,0,0,0,0,0], [0,0,1,0,9,5,0,0,0],
        [0,0,0,0,0,0,0,0,0], [0,5,0,1,8,0,0,0,3], [0,0,0,3,0,6,0,4,5],
        [0,4,0,2,0,0,0,6,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
    ]
}


class SudokuDashboard:
    def __init__(self, root):
        self.root = root
        root.title("DAA Assignment 2 | Sudoku Backtracking Visualizer")
        root.geometry("1540x960")
        root.minsize(1280, 820)
        root.configure(bg=BG)

        self.entries = []
        self.given = set()
        self.initial = deepcopy(SAMPLE)
        self.events = []
        self.event_index = 0
        self.solution = None
        self.attempts = 0
        self.conflicts = 0
        self.backtracks = 0
        self.mode = "ready"
        self._build()
        self.load_sample()

    def _build(self):
        header = tk.Frame(self.root, bg=WHITE, padx=24, pady=14,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")
        tk.Label(header, text="SUDOKU SOLVER — RECURSIVE BACKTRACKING",
                 bg=WHITE, fg=BLUE, font=("Helvetica", 21, "bold")).pack(anchor="w")
        tk.Label(header, text="A constraint-search visualizer inspired by classic Backtracking problems such as N-Queens",
                 bg=WHITE, fg=MUTED, font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))

        self.body = tk.Frame(self.root, bg=BG, padx=20, pady=16)
        self.body.pack(fill="both", expand=True)
        self._build_app_view()

    def _panel(self, parent, title=None, **kwargs):
        frame = tk.Frame(parent, bg=WHITE, padx=18, pady=16,
                         highlightbackground=BORDER, highlightthickness=1, **kwargs)
        if title:
            tk.Label(frame, text=title.upper(), bg=WHITE, fg=BLUE,
                     font=("Helvetica", 12, "bold")).pack(anchor="w")
            tk.Frame(frame, bg="#E0E7F0", height=1).pack(fill="x", pady=(7, 10))
        return frame

    def _btn(self, parent, label, command, bg=BLUE, fg=WHITE):
        # A Frame + Label avoids macOS Aqua buttons overriding custom colours.
        button = tk.Frame(parent, bg=bg, cursor="hand2",
                          highlightbackground=bg, highlightthickness=1)
        text = tk.Label(button, text=label, bg=bg, fg=fg,
                        font=("Helvetica", 12, "bold"),
                        padx=12, pady=10, cursor="hand2")
        text.pack(fill="both", expand=True)

        hover_bg = BLUE_DARK if bg == BLUE else bg

        def enter(_event=None):
            button.configure(bg=hover_bg)
            text.configure(bg=hover_bg)

        def leave(_event=None):
            button.configure(bg=bg)
            text.configure(bg=bg)

        def click(_event=None):
            command()

        for widget in (button, text):
            widget.bind("<Button-1>", click)
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
        return button

    def _build_app_view(self):
        for child in self.body.winfo_children():
            child.destroy()

        side = tk.Frame(self.body, bg=BG, width=365)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        main = tk.Frame(self.body, bg=BG)
        main.pack(side="left", fill="both", expand=True, padx=(18, 0))

        # Left settings sidebar
        dims = self._panel(side, "1. Puzzle settings")
        dims.pack(fill="x", pady=(0, 12))
        tk.Label(dims, text="Grid size", bg=WHITE, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Label(dims, text="9 × 9 Sudoku (fixed)", bg="#F1F5F9", fg=TEXT,
                 font=("Helvetica", 11, "bold"), padx=10, pady=9).pack(fill="x", pady=(5, 10))
        tk.Label(dims, text="Rules", bg=WHITE, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Label(dims, text="Each row, column and 3×3 box must contain digits 1–9 without repeats.",
                 bg=WHITE, fg=MUTED, wraplength=285, justify="left",
                 font=("Helvetica", 10)).pack(anchor="w", pady=(4, 0))

        input_panel = self._panel(side, "2. Sample puzzles")
        input_panel.pack(fill="x", pady=(0, 12))
        tk.Label(input_panel, text="Choose one of three built-in puzzles, or enter your own numbers in the grid.",
                 bg=WHITE, fg=MUTED, wraplength=285, justify="left",
                 font=("Helvetica", 10)).pack(anchor="w", pady=(0, 8))
        self.sample_var = tk.StringVar(value="Sample 1 — Easy")
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Puzzle.TCombobox", fieldbackground="#FFFFFF",
                        background="#E8EEFF", foreground=TEXT,
                        arrowcolor=BLUE, padding=7)
        self.sample_combo = ttk.Combobox(input_panel, textvariable=self.sample_var,
                                         values=list(SAMPLES.keys()), state="readonly",
                                         font=("Helvetica", 11), style="Puzzle.TCombobox")
        self.sample_combo.pack(fill="x", pady=(0, 6))
        self._btn(input_panel, "Load Selected Sample", self.load_selected_sample, "#2447B8").pack(fill="x", pady=4)
        self._btn(input_panel, "Clear Grid", self.clear_grid, "#D9485F").pack(fill="x", pady=4)
        self._btn(input_panel, "Reset Puzzle", self.reset_grid, "#64748B").pack(fill="x", pady=4)

        action = self._panel(side, "3. Algorithm controls")
        action.pack(fill="x", pady=(0, 12))
        self._btn(action, "▶  Start / Prepare Search", self.start_search, "#2447B8").pack(fill="x", pady=4)
        self._btn(action, "Next Step  →", self.next_step, "#475569").pack(fill="x", pady=4)
        self._btn(action, "✓  Show Solution", self.show_solution, "#16803D").pack(fill="x", pady=4)

        # Right dashboard
        stats = tk.Frame(main, bg=BG)
        stats.pack(fill="x", pady=(0, 10))
        self.attempt_var = tk.StringVar(value="0")
        self.conflict_var = tk.StringVar(value="0")
        self.backtrack_var = tk.StringVar(value="0")
        self._metric(stats, "PLACEMENT ATTEMPTS", self.attempt_var, BLUE).pack(side="left", fill="x", expand=True)
        self._metric(stats, "CONFLICTS", self.conflict_var, RED).pack(side="left", fill="x", expand=True, padx=8)
        self._metric(stats, "BACKTRACKING OPERATIONS", self.backtrack_var, AMBER).pack(side="left", fill="x", expand=True)

        status = self._panel(main)
        status.pack(fill="x", pady=(0, 12))
        status_row = tk.Frame(status, bg=WHITE)
        status_row.pack(fill="x")
        tk.Label(status_row, text="STATUS:", bg=WHITE, fg=MUTED,
                 font=("Helvetica", 10, "bold")).pack(side="left")
        self.status_var = tk.StringVar(value="Ready. Load a puzzle or enter your own.")
        tk.Label(status_row, textvariable=self.status_var, bg=WHITE, fg=GREEN,
                 font=("Helvetica", 10, "bold"), wraplength=700,
                 justify="left").pack(side="left", padx=(10, 0))
        self.step_var = tk.StringVar(value="Step 0 of 0")
        tk.Label(status, textvariable=self.step_var, bg=WHITE, fg=MUTED,
                 font=("Helvetica", 10)).pack(anchor="w", pady=(8, 0))

        # Board and execution log sit side-by-side for better alignment and readability.
        workspace = tk.Frame(main, bg=BG)
        workspace.pack(fill="both", expand=True)

        board_panel = self._panel(workspace, "Sudoku board — 9 rows × 9 columns")
        board_panel.pack(side="left", fill="y", padx=(0, 12), anchor="n")
        board_center = tk.Frame(board_panel, bg="#CBD5E1", padx=3, pady=3)
        board_center.pack(anchor="center", pady=(8, 12))
        board = tk.Frame(board_center, bg=WHITE)
        board.pack()
        self.entries = []
        for r in range(9):
            row = []
            for c in range(9):
                e = tk.Entry(board, width=2, justify="center", font=("Helvetica", 18, "bold"),
                             bd=0, relief="flat", bg=WHITE, fg=TEXT,
                             highlightthickness=1, highlightbackground="#D8E0EB",
                             highlightcolor=BLUE, insertbackground=BLUE)
                e.grid(row=r, column=c, ipadx=8, ipady=8,
                       padx=(0, 3 if c in (2, 5) else 1),
                       pady=(0, 3 if r in (2, 5) else 1))
                e.bind("<KeyRelease>", self._on_edit)
                row.append(e)
            self.entries.append(row)

        legend = tk.Frame(board_panel, bg=WHITE)
        legend.pack(anchor="w", pady=(8, 0))
        self._legend(legend, GIVEN, "Given")
        self._legend(legend, AMBER_BG, "Current")
        self._legend(legend, RED_BG, "Rejected")
        self._legend(legend, GREEN_BG, "Solved")

        log_panel = self._panel(workspace, "Algorithm execution log")
        log_panel.pack(side="left", fill="both", expand=True, anchor="n")
        tk.Label(log_panel,
                 text="Each line explains the candidate being tested and why it is accepted or rejected.",
                 bg=WHITE, fg=MUTED, font=("Helvetica", 10),
                 wraplength=390, justify="left").pack(anchor="w", pady=(4, 10))
        log_area = tk.Frame(log_panel, bg="#F8FAFC",
                            highlightbackground=BORDER, highlightthickness=1)
        log_area.pack(fill="both", expand=True, pady=(0, 2))
        log_scroll = tk.Scrollbar(log_area, orient="vertical")
        log_scroll.pack(side="right", fill="y")
        self.log = tk.Text(log_area, height=24, width=48, wrap="word", bd=0,
                           bg="#F8FAFC", fg=TEXT, font=("Menlo", 11),
                           padx=14, pady=12, spacing1=2, spacing3=3,
                           yscrollcommand=log_scroll.set)
        self.log.pack(side="left", fill="both", expand=True)
        log_scroll.configure(command=self.log.yview)
        self.log.tag_configure("good", foreground=GREEN)
        self.log.tag_configure("bad", foreground=RED)
        self.log.tag_configure("info", foreground=BLUE)

    def _metric(self, parent, title, var, color):
        f = tk.Frame(parent, bg=WHITE, padx=16, pady=12,
                     highlightbackground=BORDER, highlightthickness=1)
        tk.Label(f, text=title, bg=WHITE, fg=MUTED,
                 font=("Helvetica", 10, "bold")).pack(anchor="w")
        tk.Label(f, textvariable=var, bg=WHITE, fg=color,
                 font=("Helvetica", 23, "bold")).pack(anchor="w", pady=(4, 0))
        return f

    def _legend(self, parent, color, text):
        item = tk.Frame(parent, bg=WHITE)
        item.pack(side="left", padx=(0, 12))
        tk.Frame(item, bg=color, width=12, height=12,
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left")
        tk.Label(item, text=text, bg=WHITE, fg=MUTED,
                 font=("Helvetica", 8)).pack(side="left", padx=4)

    def _read_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                s = self.entries[r][c].get().strip()
                if not s:
                    row.append(0)
                elif len(s) == 1 and s in "123456789":
                    row.append(int(s))
                else:
                    messagebox.showerror("Invalid input", f"Cell row {r+1}, column {c+1} must be blank or a digit from 1 to 9.")
                    return None
            board.append(row)
        if not self.valid_start(board):
            messagebox.showerror("Invalid puzzle", "Duplicate numbers exist in a row, column, or 3×3 box.")
            return None
        return board

    @staticmethod
    def valid_start(board):
        for r in range(9):
            a = [x for x in board[r] if x]
            if len(a) != len(set(a)): return False
        for c in range(9):
            a = [board[r][c] for r in range(9) if board[r][c]]
            if len(a) != len(set(a)): return False
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                a = [board[r][c] for r in range(br, br+3) for c in range(bc, bc+3) if board[r][c]]
                if len(a) != len(set(a)): return False
        return True

    @staticmethod
    def safe(board, r, c, n):
        if any(board[r][x] == n for x in range(9)): return False
        if any(board[x][c] == n for x in range(9)): return False
        br, bc = (r//3)*3, (c//3)*3
        return all(board[x][y] != n for x in range(br, br+3) for y in range(bc, bc+3))

    @staticmethod
    def conflict_reason(board, r, c, n):
        # Return the precise Sudoku constraint that rejects a candidate.
        for x in range(9):
            if x != c and board[r][x] == n:
                return f"{n} already exists in row {r+1}, column {x+1}."
        for x in range(9):
            if x != r and board[x][c] == n:
                return f"{n} already exists in column {c+1}, row {x+1}."
        br, bc = (r // 3) * 3, (c // 3) * 3
        for x in range(br, br + 3):
            for y in range(bc, bc + 3):
                if (x, y) != (r, c) and board[x][y] == n:
                    return f"{n} already exists in the same 3×3 box at row {x+1}, column {y+1}."
        return "The candidate violates a Sudoku constraint."

    def _paint(self, board, current=None, rejected=None, solved=False):
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                e.configure(state="normal", bg=GIVEN if (r,c) in self.given else WHITE,
                            fg=TEXT if (r,c) in self.given else BLUE)
                e.delete(0, "end")
                if board[r][c]: e.insert(0, str(board[r][c]))
                if current == (r,c): e.configure(bg=AMBER_BG)
                if rejected == (r,c): e.configure(bg=RED_BG)
                if solved and board[r][c] and (r,c) not in self.given:
                    e.configure(bg=GREEN_BG, fg=GREEN)

    def _log(self, text, tag="info"):
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")

    def _reset_log(self):
        self.log.delete("1.0", "end")

    def _stats(self, a=0, c=0, b=0):
        self.attempt_var.set(str(a))
        self.conflict_var.set(str(c))
        self.backtrack_var.set(str(b))

    def load_sample(self):
        self.sample_var.set("Sample 1 — Easy")
        self._load_puzzle(SAMPLES[self.sample_var.get()], "Sample 1 — Easy")

    def load_selected_sample(self):
        name = self.sample_var.get()
        self._load_puzzle(SAMPLES[name], name)

    def _load_puzzle(self, puzzle, name):
        self.initial = deepcopy(puzzle)
        self.given = {(r,c) for r in range(9) for c in range(9) if puzzle[r][c]}
        self._paint(puzzle)
        self._clear_state(f"{name} loaded. Click Start / Prepare Search.")

    def clear_grid(self):
        self.initial = [[0]*9 for _ in range(9)]
        self.given = set()
        self._paint(self.initial)
        self._clear_state("Grid cleared. Enter a puzzle or load the sample.")

    def reset_grid(self):
        self._paint(self.initial)
        self._clear_state("Grid reset to the starting puzzle.")

    def _clear_state(self, message):
        self.events, self.event_index, self.solution = [], 0, None
        self._stats()
        self._reset_log()
        self.status_var.set(message)
        self.step_var.set("Step 0 of 0")
        self._log(message)

    def _on_edit(self, _event=None):
        # Editing the puzzle invalidates old search events.
        self.events, self.solution, self.event_index = [], None, 0

    def _make_events(self, board):
        events, attempts, conflicts, backs = [], 0, 0, 0

        def solve():
            nonlocal attempts, conflicts, backs
            empty = None
            for rr in range(9):
                for cc in range(9):
                    if board[rr][cc] == 0:
                        empty = (rr, cc)
                        break
                if empty: break
            if empty is None:
                events.append(dict(kind="solved", board=deepcopy(board), attempts=attempts,
                                   conflicts=conflicts, backs=backs, message="Solution found!"))
                return True
            r, c = empty
            for n in range(1, 10):
                attempts += 1
                if self.safe(board, r, c, n):
                    board[r][c] = n
                    events.append(dict(kind="place", board=deepcopy(board), row=r, col=c, num=n,
                                       attempts=attempts, conflicts=conflicts, backs=backs,
                                       message=f"Try {n} at row {r+1}, column {c+1}: valid so far."))
                    if solve(): return True
                    board[r][c] = 0
                    backs += 1
                    events.append(dict(kind="backtrack", board=deepcopy(board), row=r, col=c, num=n,
                                       attempts=attempts, conflicts=conflicts, backs=backs,
                                       message=f"Backtrack: remove {n} from row {r+1}, column {c+1}."))
                else:
                    conflicts += 1
                    events.append(dict(kind="reject", board=deepcopy(board), row=r, col=c, num=n,
                                       attempts=attempts, conflicts=conflicts, backs=backs,
                                       message=f"Reject {n} at row {r+1}, column {c+1}: {self.conflict_reason(board, r, c, n)}"))
            return False

        ok = solve()
        return events, deepcopy(board) if ok else None

    def start_search(self):
        board = self._read_board()
        if board is None: return
        self.initial = deepcopy(board)
        self.given = {(r,c) for r in range(9) for c in range(9) if board[r][c]}
        self.events, self.solution = self._make_events(deepcopy(board))
        self.event_index = 0
        self._paint(board)
        self._stats()
        self._reset_log()
        self.step_var.set(f"Step 0 of {len(self.events)}")
        if self.solution is None:
            self.status_var.set("No solution exists for this puzzle.")
            self._log("Search exhausted: no solution exists.", "bad")
            messagebox.showwarning("No solution", "No solution exists for this puzzle.")
        else:
            self.status_var.set(f"Search prepared: {len(self.events)} algorithm events. Click Next Step.")
            self._log(f"Search prepared with {len(self.events)} genuine backtracking events.")

    def next_step(self):
        if not self.events:
            self.start_search()
            if not self.events: return
        if self.event_index >= len(self.events):
            self.status_var.set("Visualization complete.")
            return
        ev = self.events[self.event_index]
        self.event_index += 1
        cur = (ev.get("row"), ev.get("col")) if ev.get("kind") in ("place", "backtrack") else None
        rej = (ev.get("row"), ev.get("col")) if ev.get("kind") == "reject" else None
        self._paint(ev["board"], current=cur, rejected=rej, solved=ev["kind"] == "solved")
        self._stats(ev["attempts"], ev["conflicts"], ev["backs"])
        self.step_var.set(f"Step {self.event_index} of {len(self.events)}")
        tag = "good" if ev["kind"] in ("place", "solved") else "bad"
        self.status_var.set(ev["message"])
        self._log(ev["message"], tag)
        if self.event_index == len(self.events) and ev["kind"] == "solved":
            self.status_var.set("Solution arranged successfully using recursive backtracking.")

    def show_solution(self):
        if not self.events or self.solution is None:
            self.start_search()
        if self.solution is None: return
        final = self.events[-1]
        self._paint(self.solution, solved=True)
        self._stats(final["attempts"], final["conflicts"], final["backs"])
        self.step_var.set(f"Completed • {len(self.events)} events")
        self.status_var.set("Solved: every row, column, and 3×3 box contains no repeated digit.")
        self._log("FINAL RESULT: Solution found by recursive backtracking.", "good")
        self._log("Reason: every empty cell was assigned a digit that passed row, column, and 3×3-box checks.", "good")
        self._log("When a candidate could not lead to a solution, the solver removed it and tried the next candidate.", "info")


def main():
    root = tk.Tk()
    SudokuDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
