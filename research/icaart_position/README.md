# Consolidated ICAART position paper

The active submission candidate for this consolidation is `paper/icaart_position/main.pdf` (eight pages). Its complete authored text, tables, equations, captions and bibliography are in `paper/icaart_position/main.tex`. No supplementary document is required. Earlier manuscripts are preserved as historical work.

The position is an explicit, individually authorized review-and-release workflow and a conditional analysis of source reuse. The computational evidence supports source-aware navigation as the essential simple comparator, not a demonstrated human benefit of grouping cards. No participant observations or new inference were produced.

## Compile without the repository

Copy only these files into a directory:

- `main.tex`
- `article.cls`, `SCITEPRESS.sty`, `apalike.sty` (unmodified official template files)
- `figures/workflow.pdf`, `figures/reference.pdf`, `figures/orientation.pdf`, `figures/tradeoffs.pdf`

With a standard TeX Live installation including `algorithm2e`, `footmisc`, `pslatex`, `hyperref` and the packages named in the preamble:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

There is no BibTeX step, external manuscript fragment, generated numbers file or extra methods PDF. The official template requires loading `algorithm2e` even though this paper does not use an algorithm float. Body text is 10 point and references use the official 9-point setting. No template margins, columns or fonts were reduced to fit.

## Reproduce figures from saved evidence

From the repository root (Python, NumPy, pandas and Matplotlib as used by the existing analyses):

```sh
python3 -m research.icaart_position.evidence
python3 -m research.icaart_position.figures
(cd paper/icaart_position && pdflatex -interaction=nonstopmode -halt-on-error main.tex && pdflatex -interaction=nonstopmode -halt-on-error main.tex)
python3 -m research.icaart_position.verify
```

The evidence command independently aggregates the saved simulation rows and checks the means and Monte Carlo intervals. The figure command writes vector PDFs into the submission directory, with SVG/PNG previews under `artifacts/icaart_position/figures/`. It does not run inference or new simulations. The verification command builds a temporary isolated copy containing only the submission sources and figure assets, checks its extracted text against the delivered PDF, and verifies the protected historical hashes. It never resets a historical freeze.

The final figures are:

1. Workflow schematic: what remains stable and what each decision authorizes.
2. Five-policy reference comparison: correct, incorrect and unfinished work, plus paired contrasts.
3. Discrete operating map: orientation and familiarity against both FIFO and the bounded source queue.
4. Tradeoffs: demand, carryover errors and draft verification versus manual construction.

## Remaining author-only submission decisions

Authors must review and take responsibility for the content, finalize authorship and affiliations for the submission system, and supply truthful conflict, funding, contribution and data-sharing declarations where requested. Do not reuse the template's example declarations as facts.

The manuscript is anonymous and discloses Codex assistance throughout. The official general guidelines request section-level AI citations and acknowledgment disclosure, while double-blind review excludes identifying acknowledgments. This draft uses section-level notes and a nonidentifying AI disclosure. Authors should confirm the portal's required placement/declaration without weakening the disclosure.

Choose the ICAART 2027 position-paper category. The verified ordinary limit is eight proceedings pages and 8,000–40,000 non-whitespace submission characters. The anonymous paper omits the identifying project URL. The project already has public historical artifacts, so authors must consider that history in their anonymity/data-release decisions and observe the conference's restriction on posting a submitted paper during review. Nothing was pushed or submitted here.

Human effectiveness remains unmeasured. A later human comparison must be authorized and collected under its own frozen protocol; the preserved prospective study is not a result of this paper.
