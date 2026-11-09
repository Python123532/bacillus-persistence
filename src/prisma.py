"""PRISMA 2020 flow diagram."""
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"

COUNTS = {                     # Counts found with the help of Claude AI, screening through over 750+ total papers would've been impossible or highly unlikely alone.
    "pubmed": 74,              # unique after dedup (Dataset Log)
    "europepmc": 701,          # unique after dedup (Dataset Log)
    "other": None,             # Google Scholar + reference lists + dissertations (Pasura, Tetteh, Krebs...)
    "duplicates_removed": None,  # overlap between PubMed and Europe PMC
    "screened": None,          # records screened on title/abstract
    "excluded_screening": None,
    "sought": None,            # full texts sought
    "not_retrieved": None,     # e.g. Felici 2008, Liu & Sinclair 1993
    "assessed": None,          # full texts assessed
    "excluded_fulltext": None, # with reasons (Lee 2014, Kanjanamaneesathian 2014, Grosch 1999, Khabbaz 2014, ...)
    "included_studies": None,  # persistence studies + yield studies
    "included_series": 38,
}

def box(ax, x, y, text, w=0.36, h=0.09):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fill=False))
    ax.text(x, y, text, ha="center", va="center", fontsize=8, wrap=True)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->"))

def main():
    missing = [k for k, v in COUNTS.items() if v is None]
    if missing:
        raise ValueError(f"fill these counts first: {missing}")
    c = COUNTS
    fig, ax = plt.subplots(figsize=(7, 8)); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    L, R = 0.3, 0.78
    box(ax, L, 0.92, f"Records identified\nPubMed n = {c['pubmed']}\nEurope PMC n = {c['europepmc']}\nOther sources n = {c['other']}")
    box(ax, R, 0.92, f"Duplicates removed\nn = {c['duplicates_removed']}", w=0.3)
    box(ax, L, 0.74, f"Records screened\nn = {c['screened']}")
    box(ax, R, 0.74, f"Records excluded\nn = {c['excluded_screening']}", w=0.3)
    box(ax, L, 0.56, f"Full texts sought\nn = {c['sought']}")
    box(ax, R, 0.56, f"Not retrieved\nn = {c['not_retrieved']}", w=0.3)
    box(ax, L, 0.38, f"Full texts assessed\nn = {c['assessed']}")
    box(ax, R, 0.38, f"Excluded, with reasons\nn = {c['excluded_fulltext']}", w=0.3)
    box(ax, L, 0.18, f"Studies included\nn = {c['included_studies']}\n({c['included_series']} persistence series)")
    for y1, y2 in [(0.875, 0.785), (0.695, 0.605), (0.515, 0.425), (0.335, 0.225)]:
        arrow(ax, L, y1, L, y2)
    for y in [0.92, 0.74, 0.56, 0.38]:
        arrow(ax, L + 0.18, y, R - 0.15, y)
    fig.savefig("figures/prisma.png", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
