import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

# ── Colour palette ───────────────────────────────────────────────
BG        = "#0D0D12"
SURFACE   = "#16161F"
SURFACE2  = "#1E1E2A"
SURFACE3  = "#252535"
ACCENT    = "#7C6EFA"
ACCENT2   = "#FA6E9A"
ACCENT3   = "#6EF0D4"
TEXT      = "#EAEAF5"
TEXT_DIM  = "#6A6A8A"
TEXT_MID  = "#A0A0C0"
SUCCESS   = "#6EFA9A"
DANGER    = "#FA6E6E"
WARN      = "#FAC96E"
BORDER    = "#2A2A3C"
BORDER2   = "#333348"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEAD  = ("Segoe UI", 14, "bold")
FONT_SUB   = ("Segoe UI", 11, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 10)

# ── File paths ───────────────────────────────────────────────────
DATA_FILE   = os.path.join("data_files", "personal_hub_data.json")
MOVIES_FILE = os.path.join("data_files", "movies.json")
QUOTES_FILE = os.path.join("data_files", "quotes.json")

DEFAULT_DATA = {"tasks": [], "goals": [], "fighters": []}

# ── JSON helpers ─────────────────────────────────────────────────
def load_json(path, fallback):
	try:
		if os.path.exists(path):
			with open(path, "r", encoding="utf-8") as f:
				data = json.load(f)
			if data:
				return data
	except Exception:
		pass
	return fallback

def save_json(path, data):
	try:
		os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
		with open(path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4, ensure_ascii=False)
	except Exception as e:
		print(f"Error saving to {path}: {e}")

# ── Widget helpers ───────────────────────────────────────────────
def _lighten(hex_color, amount=28):
	try:
		r = min(255, int(hex_color[1:3], 16) + amount)
		g = min(255, int(hex_color[3:5], 16) + amount)
		b = min(255, int(hex_color[5:7], 16) + amount)
		return f"#{r:02x}{g:02x}{b:02x}"
	except Exception:
		return hex_color

def fr(parent, bg=SURFACE, **kw):
	return tk.Frame(parent, bg=bg, **kw)

def lbl(parent, text="", font=FONT_BODY, fg=TEXT, bg=SURFACE, **kw):
	return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def entry(parent, width=24, **kw):
	return tk.Entry(parent, width=width, font=FONT_BODY,
					bg=SURFACE3, fg=TEXT, insertbackground=ACCENT3,
					relief=tk.FLAT, bd=7, highlightthickness=1,
					highlightbackground=BORDER2, highlightcolor=ACCENT, **kw)

def btn(parent, text, command, color=ACCENT, fg="white", font=FONT_SMALL, **kw):
	b = tk.Button(parent, text=text, command=command,
				bg=color, fg=fg, font=font,
				relief=tk.FLAT, bd=0, cursor="hand2",
				activebackground=_lighten(color), activeforeground=fg,
				  padx=12, pady=6, **kw)
	b.bind("<Enter>", lambda e: b.config(bg=_lighten(color)))
	b.bind("<Leave>", lambda e: b.config(bg=color))
	return b

def listbox(parent, height=12, **kw):
	return tk.Listbox(parent, font=FONT_BODY,
					bg=SURFACE3, fg=TEXT,
					selectbackground=ACCENT,
					selectforeground="white",
					activestyle="none",
					relief=tk.FLAT, bd=0,
					highlightthickness=0,
					  height=height, **kw)

def divider(parent, color=BORDER, pady=8):
	tk.Frame(parent, bg=color, height=1).pack(fill=tk.X, pady=pady)

def scrollbar(lb, parent):
	sb = tk.Scrollbar(parent, orient=tk.VERTICAL, command=lb.yview,
					bg=SURFACE2, troughcolor=SURFACE2,
					activebackground=ACCENT, width=6)
	lb.config(yscrollcommand=sb.set)
	return sb

def card(parent, bg=SURFACE2, **kw):
	return tk.Frame(parent, bg=bg, relief=tk.FLAT, bd=0,
					highlightbackground=BORDER2, highlightthickness=1, **kw)

def section_header(parent, icon, title, color, bg=SURFACE):
	row = fr(parent, bg=bg)
	row.pack(fill=tk.X, pady=(0, 4))
	lbl(row, f"{icon}  {title}", font=FONT_HEAD, fg=color, bg=bg).pack(side=tk.LEFT)
	return row

def placeholder_entry(parent, placeholder, width=20, **kw):
	e = entry(parent, width=width, **kw)
	e.insert(0, placeholder)
	e.config(fg=TEXT_DIM)
	def on_focus_in(ev):
		if e.get() == placeholder:
			e.delete(0, tk.END)
			e.config(fg=TEXT)
	def on_focus_out(ev):
		if not e.get():
			e.insert(0, placeholder)
			e.config(fg=TEXT_DIM)
	e.bind("<FocusIn>",  on_focus_in)
	e.bind("<FocusOut>", on_focus_out)
	e._placeholder = placeholder
	return e

def get_entry_val(e):
	v = e.get().strip()
	return "" if v == getattr(e, "_placeholder", None) else v


# ════════════════════════════════════════════════════════════════
class PersonalHubApp:

	def __init__(self, root):
		self.root = root
		self.root.title("Personal Hub")
		self.root.geometry("960x720")
		self.root.minsize(800, 600)
		self.root.config(bg=BG)
		self.root.resizable(True, True)

		self._ensure_data_dir()

		data = load_json(DATA_FILE, DEFAULT_DATA)
		self.tasks    = data.get("tasks",    [])
		self.goals    = data.get("goals",    [])
		self.fighters = data.get("fighters", [])

		# Movies and quotes live entirely in their own JSON files
		self.quotes = load_json(QUOTES_FILE, [])
		self.movies = load_json(MOVIES_FILE, [])

		self.save_hub()
		self.save_quotes()
		self.save_movies()

		self.show_main_hub()

	# ── Persistence ──────────────────────────────────────────────
	def save_hub(self):
		save_json(DATA_FILE, {
			"tasks":    self.tasks,
			"goals":    self.goals,
			"fighters": self.fighters,
		})

	def save_quotes(self):
		save_json(QUOTES_FILE, self.quotes)

	def save_movies(self):
		save_json(MOVIES_FILE, self.movies)

	def _ensure_data_dir(self):
		os.makedirs("data_files", exist_ok=True)

	# ── Helpers ──────────────────────────────────────────────────
	def clear(self):
		for w in self.root.winfo_children():
			w.destroy()

	def _topbar(self, title_text, back_cmd=None, back_label="← Hub"):
		bar = fr(self.root, bg=BG)
		bar.pack(fill=tk.X, padx=24, pady=(18, 0))
		lbl(bar, title_text, font=FONT_TITLE, fg=TEXT, bg=BG).pack(side=tk.LEFT)
		if back_cmd:
			btn(bar, back_label, back_cmd,
				color=SURFACE3, fg=TEXT_MID, font=FONT_SUB).pack(side=tk.RIGHT, pady=4)
		tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X, padx=24, pady=(10, 0))

	# ════════════════════════════════════════════════════════════
	# MAIN HUB
	# ════════════════════════════════════════════════════════════
	def show_main_hub(self):
		self.clear()
		bar = fr(self.root, bg=BG)
		bar.pack(fill=tk.X, padx=24, pady=(18, 0))
		lbl(bar, "⬡  Personal Hub", font=FONT_TITLE, fg=TEXT, bg=BG).pack(side=tk.LEFT)
		btn(bar, "✦  Workspace →", self.show_workspace,
			color=ACCENT, font=FONT_SUB).pack(side=tk.RIGHT, pady=4)
		tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X, padx=24, pady=(10, 0))

		body = fr(self.root, bg=BG)
		body.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)
		body.columnconfigure(0, weight=1)
		body.columnconfigure(1, weight=1)
		body.rowconfigure(0, weight=1)

		left = card(body, bg=SURFACE)
		left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
		self._tasks_panel(left)

		right = card(body, bg=SURFACE)
		right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
		self._goals_panel(right)

	# ── Tasks ────────────────────────────────────────────────────
	def _tasks_panel(self, parent):
		p = fr(parent, bg=SURFACE)
		p.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

		hrow = fr(p, bg=SURFACE)
		hrow.pack(fill=tk.X, pady=(0, 4))
		lbl(hrow, "📋  Task Agenda", font=FONT_HEAD, fg=ACCENT, bg=SURFACE).pack(side=tk.LEFT)
		self._task_count_var = tk.StringVar()
		lbl(hrow, "", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE,
			textvariable=self._task_count_var).pack(side=tk.RIGHT)

		divider(p, pady=6)

		irow = fr(p, bg=SURFACE)
		irow.pack(fill=tk.X, pady=4)
		self.task_entry = entry(irow, width=28)
		self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
		self.task_entry.bind("<Return>", lambda e: self._add_task())
		btn(irow, "+ Add", self._add_task, color=SUCCESS, fg=BG).pack(side=tk.LEFT)

		lb_fr = fr(p, bg=SURFACE)
		lb_fr.pack(fill=tk.BOTH, expand=True, pady=6)
		self.task_lb = listbox(lb_fr, height=14)
		sb = scrollbar(self.task_lb, lb_fr)
		sb.pack(side=tk.RIGHT, fill=tk.Y)
		self.task_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		btn(p, "✕  Remove Selected", self._remove_task,
			color=DANGER).pack(pady=(6, 0))
		self._refresh_tasks()

	def _add_task(self):
		t = self.task_entry.get().strip()
		if t:
			self.tasks.append(t)
			self.task_entry.delete(0, tk.END)
			self._refresh_tasks()
			self.save_hub()
		else:
			messagebox.showwarning("Empty Task", "Please enter a task.", parent=self.root)

	def _remove_task(self):
		sel = self.task_lb.curselection()
		if sel:
			self.tasks.pop(sel[0])
			self._refresh_tasks()
			self.save_hub()
		else:
			messagebox.showwarning("No Selection", "Select a task to remove.", parent=self.root)

	def _refresh_tasks(self):
		self.task_lb.delete(0, tk.END)
		for t in self.tasks:
			self.task_lb.insert(tk.END, f"  ›  {t}")
		n = len(self.tasks)
		self._task_count_var.set(f"{n} item{'s' if n != 1 else ''}")

	# ── Goals ────────────────────────────────────────────────────
	def _goals_panel(self, parent):
		p = fr(parent, bg=SURFACE)
		p.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

		hrow = fr(p, bg=SURFACE)
		hrow.pack(fill=tk.X, pady=(0, 4))
		lbl(hrow, "🎯  Goals List", font=FONT_HEAD, fg=ACCENT2, bg=SURFACE).pack(side=tk.LEFT)
		self._goals_count_var = tk.StringVar()
		lbl(hrow, "", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE,
			textvariable=self._goals_count_var).pack(side=tk.RIGHT)

		divider(p, pady=6)

		irow = fr(p, bg=SURFACE)
		irow.pack(fill=tk.X, pady=4)
		self.goals_entry = entry(irow, width=28)
		self.goals_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
		self.goals_entry.bind("<Return>", lambda e: self._add_goal())
		btn(irow, "+ Add", self._add_goal, color=SUCCESS, fg=BG).pack(side=tk.LEFT)

		lb_fr = fr(p, bg=SURFACE)
		lb_fr.pack(fill=tk.BOTH, expand=True, pady=6)
		self.goals_lb = listbox(lb_fr, height=14)
		sb = scrollbar(self.goals_lb, lb_fr)
		sb.pack(side=tk.RIGHT, fill=tk.Y)
		self.goals_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		btn(p, "✕  Remove Selected", self._remove_goal,
			color=DANGER).pack(pady=(6, 0))
		self._refresh_goals()

	def _add_goal(self):
		g = self.goals_entry.get().strip()
		if g:
			self.goals.append(g)
			self.goals_entry.delete(0, tk.END)
			self._refresh_goals()
			self.save_hub()
		else:
			messagebox.showwarning("Empty Goal", "Please enter a goal.", parent=self.root)

	def _remove_goal(self):
		sel = self.goals_lb.curselection()
		if sel:
			self.goals.pop(sel[0])
			self._refresh_goals()
			self.save_hub()
		else:
			messagebox.showwarning("No Selection", "Select a goal to remove.", parent=self.root)

	def _refresh_goals(self):
		self.goals_lb.delete(0, tk.END)
		for g in self.goals:
			self.goals_lb.insert(tk.END, f"  ›  {g}")
		n = len(self.goals)
		self._goals_count_var.set(f"{n} item{'s' if n != 1 else ''}")

	# ════════════════════════════════════════════════════════════
	# WORKSPACE
	# ════════════════════════════════════════════════════════════
	def show_workspace(self):
		self.clear()
		self._topbar("✦  Workspace", self.show_main_hub)

		style = ttk.Style()
		style.theme_use("default")
		style.configure("Hub.TNotebook",
						background=BG, borderwidth=0, tabmargins=0)
		style.configure("Hub.TNotebook.Tab",
						background=SURFACE2, foreground=TEXT_DIM,
						font=FONT_SUB, padding=[16, 8], borderwidth=0)
		style.map("Hub.TNotebook.Tab",
				background=[("selected", SURFACE)],
				foreground=[("selected", TEXT)])

		nb = ttk.Notebook(self.root, style="Hub.TNotebook")
		nb.pack(fill=tk.BOTH, expand=True, padx=24, pady=14)

		q_tab = fr(nb, bg=SURFACE)
		m_tab = fr(nb, bg=SURFACE)
		u_tab = fr(nb, bg=SURFACE)

		nb.add(q_tab, text="  💬  Quotes  ")
		nb.add(m_tab, text="  🎬  Movies  ")
		nb.add(u_tab, text="  🥊  UFC Tracker  ")

		self._build_quotes(q_tab)
		self._build_movies(m_tab)
		self._build_ufc(u_tab)

	# ════════════════════════════════════════════════════════════
	# QUOTES
	# ════════════════════════════════════════════════════════════
	def _build_quotes(self, parent):
		wrap = fr(parent, bg=SURFACE)
		wrap.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)

		# ── Featured quote card ──
		feat = card(wrap, bg=SURFACE2)
		feat.pack(fill=tk.X, pady=(0, 14))
		inner = fr(feat, bg=SURFACE2)
		inner.pack(fill=tk.X, padx=22, pady=18)

		top_row = fr(inner, bg=SURFACE2)
		top_row.pack(fill=tk.X, pady=(0, 10))
		lbl(top_row, "✦  Quote of the Day", font=FONT_SUB,
			fg=ACCENT3, bg=SURFACE2).pack(side=tk.LEFT)
		btn(top_row, "↻  Shuffle", self._random_quote,
			color=ACCENT3, fg=BG, font=FONT_SMALL).pack(side=tk.RIGHT)

		tk.Frame(inner, bg=BORDER2, height=1).pack(fill=tk.X, pady=(0, 12))

		self._quote_text_var = tk.StringVar()
		self._quote_auth_var = tk.StringVar()

		tk.Label(inner, textvariable=self._quote_text_var,
				font=("Segoe UI", 13, "italic"),
				fg=TEXT, bg=SURFACE2,
				wraplength=760, justify=tk.LEFT).pack(anchor="w")

		lbl(inner, textvariable=self._quote_auth_var,
			font=("Segoe UI", 10, "bold"), fg=ACCENT3, bg=SURFACE2).pack(anchor="e", pady=(8, 0))

		# ── Quotes list ──
		divider(wrap, color=BORDER2)

		list_hdr = fr(wrap, bg=SURFACE)
		list_hdr.pack(fill=tk.X, pady=(0, 6))
		lbl(list_hdr, "All Quotes", font=FONT_SUB, fg=TEXT_MID, bg=SURFACE).pack(side=tk.LEFT)
		self._quotes_count_var = tk.StringVar()
		lbl(list_hdr, "", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE,
			textvariable=self._quotes_count_var).pack(side=tk.RIGHT)

		lb_fr = fr(wrap, bg=SURFACE)
		lb_fr.pack(fill=tk.BOTH, expand=True)
		self.quotes_lb = listbox(lb_fr, height=7)
		sb = scrollbar(self.quotes_lb, lb_fr)
		sb.pack(side=tk.RIGHT, fill=tk.Y)
		self.quotes_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		# ── Add row ──
		add_card = card(wrap, bg=SURFACE2)
		add_card.pack(fill=tk.X, pady=(10, 0))
		add_inner = fr(add_card, bg=SURFACE2)
		add_inner.pack(fill=tk.X, padx=16, pady=12)

		lbl(add_inner, "Add New Quote", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE2).pack(anchor="w", pady=(0, 6))

		row = fr(add_inner, bg=SURFACE2)
		row.pack(fill=tk.X)
		self._q_text = placeholder_entry(row, "Enter quote text…", width=42)
		self._q_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
		self._q_auth = placeholder_entry(row, "Author", width=16)
		self._q_auth.pack(side=tk.LEFT, padx=(0, 6))
		btn(row, "+ Add", self._add_quote, color=SUCCESS, fg=BG).pack(side=tk.LEFT, padx=(0, 6))
		btn(row, "✕ Remove", self._remove_quote, color=DANGER).pack(side=tk.LEFT)

		self._refresh_quotes()
		self._random_quote()

	def _random_quote(self):
		if self.quotes:
			q = random.choice(self.quotes)
			self._quote_text_var.set(f"\u201c {q['quote']} \u201d")
			self._quote_auth_var.set(f"— {q['author']}")
		else:
			self._quote_text_var.set("No quotes yet — add one below!")
			self._quote_auth_var.set("")

	def _refresh_quotes(self):
		self.quotes_lb.delete(0, tk.END)
		for q in self.quotes:
			snippet = q["quote"][:72] + ("…" if len(q["quote"]) > 72 else "")
			self.quotes_lb.insert(tk.END, f"  {q['author']}  —  {snippet}")
		n = len(self.quotes)
		self._quotes_count_var.set(f"{n} quote{'s' if n != 1 else ''}")

	def _add_quote(self):
		text = get_entry_val(self._q_text)
		auth = get_entry_val(self._q_auth)
		if text and auth:
			self.quotes.append({"quote": text, "author": auth})
			self.save_quotes()
			self._q_text.delete(0, tk.END)
			self._q_text.insert(0, "Enter quote text…")
			self._q_text.config(fg=TEXT_DIM)
			self._q_auth.delete(0, tk.END)
			self._q_auth.insert(0, "Author")
			self._q_auth.config(fg=TEXT_DIM)
			self._refresh_quotes()
			self._random_quote()
		else:
			messagebox.showwarning("Incomplete", "Enter both quote text and author.", parent=self.root)

	def _remove_quote(self):
		sel = self.quotes_lb.curselection()
		if sel:
			self.quotes.pop(sel[0])
			self.save_quotes()
			self._refresh_quotes()
			self._random_quote()
		else:
			messagebox.showwarning("No Selection", "Select a quote to remove.", parent=self.root)

	# ════════════════════════════════════════════════════════════
	# MOVIES
	# ════════════════════════════════════════════════════════════
	def _build_movies(self, parent):
		wrap = fr(parent, bg=SURFACE)
		wrap.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)

		section_header(wrap, "🎬", "Movie List", ACCENT2)

		# ── Random pick card ──
		pick = card(wrap, bg=SURFACE2)
		pick.pack(fill=tk.X, pady=(6, 14))
		pick_inner = fr(pick, bg=SURFACE2)
		pick_inner.pack(fill=tk.X, padx=20, pady=14)

		top = fr(pick_inner, bg=SURFACE2)
		top.pack(fill=tk.X, pady=(0, 8))
		lbl(top, "🎲  Random Pick", font=FONT_SUB, fg=ACCENT2, bg=SURFACE2).pack(side=tk.LEFT)
		btn(top, "↻  Suggest One", self._random_movie,
			color=ACCENT2, fg="white", font=FONT_SMALL).pack(side=tk.RIGHT)

		tk.Frame(pick_inner, bg=BORDER2, height=1).pack(fill=tk.X, pady=(0, 10))
		self._movie_pick_var = tk.StringVar(value="Press 'Suggest One' to get a recommendation!")
		lbl(pick_inner, textvariable=self._movie_pick_var,
			font=("Segoe UI", 12), fg=TEXT, bg=SURFACE2).pack(anchor="w")

		# ── Movie listbox ──
		divider(wrap, color=BORDER2)

		hdr = fr(wrap, bg=SURFACE)
		hdr.pack(fill=tk.X, pady=(0, 6))
		lbl(hdr, "Your Movies", font=FONT_SUB, fg=TEXT_MID, bg=SURFACE).pack(side=tk.LEFT)
		self._movies_count_var = tk.StringVar()
		lbl(hdr, "", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE,
			textvariable=self._movies_count_var).pack(side=tk.RIGHT)

		lb_fr = fr(wrap, bg=SURFACE)
		lb_fr.pack(fill=tk.BOTH, expand=True)
		self.movies_lb = listbox(lb_fr, height=8)
		sb = scrollbar(self.movies_lb, lb_fr)
		sb.pack(side=tk.RIGHT, fill=tk.Y)
		self.movies_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		# ── Add row ──
		add_card = card(wrap, bg=SURFACE2)
		add_card.pack(fill=tk.X, pady=(10, 0))
		add_inner = fr(add_card, bg=SURFACE2)
		add_inner.pack(fill=tk.X, padx=16, pady=12)

		lbl(add_inner, "Add Movie", font=FONT_SMALL, fg=TEXT_DIM, bg=SURFACE2).pack(anchor="w", pady=(0, 6))

		row = fr(add_inner, bg=SURFACE2)
		row.pack(fill=tk.X)
		self._m_title  = placeholder_entry(row, "Title", width=22)
		self._m_title.pack(side=tk.LEFT, padx=(0, 6))
		self._m_genre  = placeholder_entry(row, "Genre", width=14)
		self._m_genre.pack(side=tk.LEFT, padx=(0, 6))
		self._m_year   = placeholder_entry(row, "Year", width=6)
		self._m_year.pack(side=tk.LEFT, padx=(0, 6))
		self._m_rating = placeholder_entry(row, "Rating", width=6)
		self._m_rating.pack(side=tk.LEFT, padx=(0, 6))
		btn(row, "+ Add", self._add_movie, color=SUCCESS, fg=BG).pack(side=tk.LEFT, padx=(0, 6))
		btn(row, "✕ Remove", self._remove_movie, color=DANGER).pack(side=tk.LEFT)

		self._refresh_movies()

	def _random_movie(self):
		if self.movies:
			m = random.choice(self.movies)
			parts = [m.get("title", "Unknown")]
			if m.get("genre"):  parts.append(m["genre"])
			if m.get("year"):   parts.append(str(m["year"]))
			if m.get("rating"): parts.append(f"⭐ {m['rating']}")
			self._movie_pick_var.set("  ·  ".join(parts))
		else:
			self._movie_pick_var.set("No movies in your list yet — add some below!")

	def _refresh_movies(self):
		self.movies_lb.delete(0, tk.END)
		for m in self.movies:
			row = f"  {m.get('title', 'Unknown')}"
			if m.get("genre"):  row += f"  |  {m['genre']}"
			if m.get("year"):   row += f"  |  {m['year']}"
			if m.get("rating"): row += f"  |  ⭐ {m['rating']}"
			self.movies_lb.insert(tk.END, row)
		n = len(self.movies)
		self._movies_count_var.set(f"{n} title{'s' if n != 1 else ''}")

	def _add_movie(self):
		title  = get_entry_val(self._m_title)
		genre  = get_entry_val(self._m_genre)
		year   = get_entry_val(self._m_year)
		rating = get_entry_val(self._m_rating)
		if title:
			self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
			self.save_movies()
			for e, ph in [(self._m_title, "Title"), (self._m_genre, "Genre"),
						(self._m_year, "Year"), (self._m_rating, "Rating")]:
				e.delete(0, tk.END)
				e.insert(0, ph)
				e.config(fg=TEXT_DIM)
			self._refresh_movies()
		else:
			messagebox.showwarning("Missing Title", "A title is required.", parent=self.root)

	def _remove_movie(self):
		sel = self.movies_lb.curselection()
		if sel:
			self.movies.pop(sel[0])
			self.save_movies()
			self._refresh_movies()
		else:
			messagebox.showwarning("No Selection", "Select a movie to remove.", parent=self.root)

	# ════════════════════════════════════════════════════════════
	# UFC TRACKER
	# ════════════════════════════════════════════════════════════
	def _build_ufc(self, parent):
		wrap = fr(parent, bg=SURFACE)
		wrap.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)

		section_header(wrap, "🥊", "UFC Fighter Tracker", WARN)

		# ── Add form ──
		form_card = card(wrap, bg=SURFACE2)
		form_card.pack(fill=tk.X, pady=(6, 14))
		form = fr(form_card, bg=SURFACE2)
		form.pack(fill=tk.X, padx=18, pady=14)

		lbl(form, "Track a Fighter", font=FONT_SUB, fg=WARN, bg=SURFACE2).pack(anchor="w", pady=(0, 10))

		row = fr(form, bg=SURFACE2)
		row.pack(fill=tk.X)
		self._f_fields = {}
		defs = [("name", "Fighter Name", 20), ("weightclass", "Weight Class", 14),
				("record", "Record (W-L-D)", 12), ("ranking", "Ranking / #", 8)]
		for key, ph, w in defs:
			e = placeholder_entry(row, ph, width=w)
			e.pack(side=tk.LEFT, padx=(0, 6))
			self._f_fields[key] = e

		btn(row, "+ Track", self._add_fighter,
			color=WARN, fg=BG).pack(side=tk.LEFT)

		# ── Treeview ──
		divider(wrap, color=BORDER2)
		lbl(wrap, "Tracked Fighters", font=FONT_SUB, fg=TEXT_MID, bg=SURFACE).pack(anchor="w", pady=(0, 8))

		tree_fr = fr(wrap, bg=SURFACE)
		tree_fr.pack(fill=tk.BOTH, expand=True)

		style = ttk.Style()
		style.configure("UFC.Treeview",
						background=SURFACE3, foreground=TEXT,
						fieldbackground=SURFACE3,
						rowheight=30, font=FONT_BODY, borderwidth=0)
		style.configure("UFC.Treeview.Heading",
						background=SURFACE2, foreground=WARN,
						font=FONT_SUB, relief=tk.FLAT)
		style.map("UFC.Treeview",
				background=[("selected", ACCENT)],
				foreground=[("selected", "white")])

		cols = ("Name", "Weight Class", "Record", "Ranking")
		self.fighter_tree = ttk.Treeview(tree_fr, columns=cols,
										show="headings", style="UFC.Treeview", height=10)
		for col, w in zip(cols, [200, 150, 110, 110]):
			self.fighter_tree.heading(col, text=col)
			self.fighter_tree.column(col, width=w, anchor="w")

		vsb = ttk.Scrollbar(tree_fr, orient=tk.VERTICAL,
							command=self.fighter_tree.yview)
		self.fighter_tree.configure(yscrollcommand=vsb.set)
		vsb.pack(side=tk.RIGHT, fill=tk.Y)
		self.fighter_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		btn(wrap, "✕  Remove Selected Fighter",
			self._remove_fighter, color=DANGER).pack(pady=(10, 0), anchor="w")

		self._refresh_fighters()

	def _add_fighter(self):
		f = self._f_fields
		name = get_entry_val(f["name"])
		if not name:
			messagebox.showwarning("Missing Name", "Fighter name is required.", parent=self.root)
			return
		self.fighters.append({
			"name":        name,
			"weightclass": get_entry_val(f["weightclass"]),
			"record":      get_entry_val(f["record"]),
			"ranking":     get_entry_val(f["ranking"]),
		})
		self.save_hub()
		defs = [("name", "Fighter Name"), ("weightclass", "Weight Class"),
				("record", "Record (W-L-D)"), ("ranking", "Ranking / #")]
		for key, ph in defs:
			f[key].delete(0, tk.END)
			f[key].insert(0, ph)
			f[key].config(fg=TEXT_DIM)
		self._refresh_fighters()

	def _remove_fighter(self):
		sel = self.fighter_tree.selection()
		if not sel:
			messagebox.showwarning("No Selection", "Select a fighter to remove.", parent=self.root)
			return
		for item in sel:
			self.fighters.pop(self.fighter_tree.index(item))
		self.save_hub()
		self._refresh_fighters()

	def _refresh_fighters(self):
		for row in self.fighter_tree.get_children():
			self.fighter_tree.delete(row)
		for f in self.fighters:
			self.fighter_tree.insert("", tk.END, values=(
				f.get("name", ""), f.get("weightclass", ""),
				f.get("record", ""), f.get("ranking", ""),
			))


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
	os.makedirs("data_files", exist_ok=True)
	root = tk.Tk()
	app = PersonalHubApp(root)
	root.mainloop()