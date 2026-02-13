import csv
import random
from pathlib import Path

# -------------------------
# Setări dataset (cerința ta)
# -------------------------
SEED = 42
N_AUTHORS = 200
N_PAPERS = 1500
N_KEYWORDS = 300
N_CITES = 8000

MIN_AUTHORS_PER_PAPER = 1
MAX_AUTHORS_PER_PAPER = 4

MIN_KW_PER_PAPER = 2
MAX_KW_PER_PAPER = 6

VENUES = [
    ("V1", "ICDM", "conference"),
    ("V2", "KDD", "conference"),
    ("V3", "NeurIPS", "conference"),
    ("V4", "TKDE", "journal"),
    ("V5", "VLDB", "conference"),
]

INSTITUTIONS = [
    ("I1", "University of Bucharest", "RO"),
    ("I2", "Politehnica University of Bucharest", "RO"),
    ("I3", "Babeș-Bolyai University", "RO"),
    ("I4", "TU Munich", "DE"),
    ("I5", "EPFL", "CH"),
]

YEARS = list(range(2016, 2026))  # 2016..2025

random.seed(SEED)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data"
OUT_DIR.mkdir(exist_ok=True)

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

# -------------------------
# Authors
# -------------------------
first_names = ["Andrei", "Ioana", "Mihai", "Alex", "Bianca", "Elena", "Vlad", "Ana", "Radu", "Daria"]
last_names = ["Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Stan", "Marin", "Ilie", "Matei", "Voicu", "Toma"]

authors = []
for i in range(1, N_AUTHORS + 1):
    aid = f"A{i}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    h_index = random.randint(1, 30)
    authors.append((aid, name, h_index))

write_csv(OUT_DIR / "authors.csv", ["id", "name", "h_index"], authors)

# -------------------------
# Keywords
# -------------------------
kw_bases = ["graph", "database", "recommender", "learning", "mining", "networks",
            "security", "nlp", "vision", "systems", "distributed", "optimization"]

keywords = []
for i in range(1, N_KEYWORDS + 1):
    kid = f"K{i}"
    value = f"{random.choice(kw_bases)} {random.choice(kw_bases)}"
    keywords.append((kid, value))

write_csv(OUT_DIR / "keywords.csv", ["id", "value"], keywords)

# -------------------------
# Venues & Institutions
# -------------------------
write_csv(OUT_DIR / "venues.csv", ["id", "name", "type"], VENUES)
write_csv(OUT_DIR / "institutions.csv", ["id", "name", "country"], INSTITUTIONS)

# -------------------------
# Papers
# -------------------------
papers = []
for i in range(1, N_PAPERS + 1):
    pid = f"P{i}"
    year = random.choice(YEARS)
    title = f"Paper {i}: {random.choice(kw_bases).title()} for {random.choice(kw_bases).title()}"
    papers.append((pid, title, year))

write_csv(OUT_DIR / "papers.csv", ["id", "title", "year"], papers)

# -------------------------
# AUTHORED (author -> paper)
# -------------------------
authored = []
for pid, _, _ in papers:
    n = random.randint(MIN_AUTHORS_PER_PAPER, MAX_AUTHORS_PER_PAPER)
    chosen = random.sample(authors, n)
    for pos, (aid, _, _) in enumerate(chosen, start=1):
        authored.append((aid, pid, pos))

write_csv(OUT_DIR / "authored.csv", ["author_id", "paper_id", "pos"], authored)

# -------------------------
# HAS_KEYWORD (paper -> keyword)
# -------------------------
has_keyword = []
for pid, _, _ in papers:
    n = random.randint(MIN_KW_PER_PAPER, MAX_KW_PER_PAPER)
    chosen = random.sample(keywords, n)
    for kid, _ in chosen:
        has_keyword.append((pid, kid))

write_csv(OUT_DIR / "has_keyword.csv", ["paper_id", "keyword_id"], has_keyword)

# -------------------------
# PUBLISHED_IN (paper -> venue)
# -------------------------
published_in = []
for pid, _, _ in papers:
    vid, _, _ = random.choice(VENUES)
    published_in.append((pid, vid))

write_csv(OUT_DIR / "published_in.csv", ["paper_id", "venue_id"], published_in)

# -------------------------
# AFFILIATED_WITH (author -> institution)
# -------------------------
affiliated = []
for aid, _, _ in authors:
    iid, _, _ = random.choice(INSTITUTIONS)
    since = random.randint(2015, 2025)
    affiliated.append((aid, iid, since))

write_csv(OUT_DIR / "affiliated.csv", ["author_id", "inst_id", "since"], affiliated)

# -------------------------
# CITES (paper -> paper) - fără self, fără duplicate
# -------------------------
paper_ids = [p[0] for p in papers]
cites_set = set()

while len(cites_set) < N_CITES:
    src = random.choice(paper_ids)
    dst = random.choice(paper_ids)
    if src == dst:
        continue
    cites_set.add((src, dst))

cites = list(cites_set)
write_csv(OUT_DIR / "cites.csv", ["src_paper_id", "dst_paper_id"], cites)

print("CSV files generated in:", OUT_DIR)
print("Files:", [p.name for p in OUT_DIR.glob('*.csv')])
