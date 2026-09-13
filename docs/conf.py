# Configuration file for the Sphinx documentation builder.

from pathlib import Path
import shutil
import sys
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Інформаційні технології у лінгвістиці"
copyright = "2025, Василь МАЦЕНКО, Володимир КОВДРИШ"
author = "Василь МАЦЕНКО, Володимир КОВДРИШ"
latex_title_subtitle = "Методичні вказівки до лабораторних занять"
latex_title_place = "Чернівці"
latex_title_year = "2026"
latex_imprint_udc = "004:81"
latex_imprint_bibliography = (
    r"Інформаційні технології у лінгвістиці: методичні вказівки до "
    r"лабораторних занять / уклад. Василь МАЦЕНКО, Володимир КОВДРИШ. "
    r"Чернівці, 2026. \ITinLingvoPages{} с."
)
latex_imprint_sheet_width_cm = 60
latex_imprint_sheet_height_cm = 84
latex_imprint_sheet_fraction = 16
latex_imprint_page_area_cm2 = (
    latex_imprint_sheet_width_cm
    * latex_imprint_sheet_height_cm
    / latex_imprint_sheet_fraction
)
latex_imprint_page_area_label = str(round(latex_imprint_page_area_cm2, 1)).replace(".", ",")
latex_imprint_extent = (
    r"Обсяг: \ITinLingvoPages{} с.; "
    r"\ITinLingvoConditionalPrintSheets{} ум. друк. арк. "
    f"(формат {latex_imprint_sheet_width_cm}×{latex_imprint_sheet_height_cm}/"
    f"{latex_imprint_sheet_fraction}; розрахунок: "
    rf"\ITinLingvoPages{{}} × {latex_imprint_page_area_label} / 5400)."
)
latex_imprint_annotation = (
    "Методичні вказівки призначені для студентів, які вивчають застосування "
    "інформаційних технологій у лінгвістичних дослідженнях та навчальній "
    "діяльності. Матеріали охоплюють роботу з офісними застосунками, "
    "вебсервісами, електронними ресурсами, цифровими інструментами "
    "опрацювання текстів і даних."
)
latex_imprint_keywords = (
    "інформаційні технології, лінгвістика, лабораторні заняття, "
    "цифрові інструменти, електронні ресурси"
)
latex_imprint_copyright = "© Василь МАЦЕНКО, Володимир КОВДРИШ, 2026"
latex_titlepage = (Path(__file__).parent / "_templates" / "latex" / "titlepage.tex").read_text()
latex_imprint = (Path(__file__).parent / "_templates" / "latex" / "imprint.tex").read_text()


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

master_doc = "index"
sys.path.insert(0, str(Path(__file__).parent / "_ext"))
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.graphviz",
    "sphinx_togglebutton",
    "lab_directives",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}


templates_path = ["_templates"]
exclude_patterns = []

language = "uk"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_provider": "github",
    "repository_url": "https://github.com/Volodymyr-Kovdrysh/ITinLingvo-students",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_source_button": True,
    # "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "home_page_in_toc": False,
    "show_navbar_depth": 2,
    "toc_title": "Зміст",
    "show_toc_level": 2,
}
html_static_path = ["_static"]
html_css_files = ["lab.css"]
html_title = project

# PDF output: xelatex handles Ukrainian Unicode text and symbols better than
# pdflatex, which fails on characters such as ⇒ used in the lab instructions.
latex_engine = "xelatex"
latex_elements = {
    "papersize": "a5paper",
    "pointsize": "10pt",
    "sphinxsetup": "hmargin=16mm, vmargin=18mm, marginpar=0mm",
    "fontpkg": r"""
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
""",
    "extrapackages": r"""
\usepackage{xurl}
\usepackage[most]{tcolorbox}
\usepackage{zref-totpages}
\usepackage{xfp}
\usepackage{siunitx}
""",
    "preamble": rf"""
\renewcommand{{\chaptername}}{{Заняття}}
\makeatletter
\renewcommand{{\@chapapp}}{{Заняття}}
\setlength{{\parindent}}{{1.25em}}
\setlength{{\parskip}}{{0pt}}
\newtcolorbox{{sphinxtermblock}}[1]{{%
  enhanced,
  breakable,
  colback=black!2,
  colframe=black!35,
  boxrule=0.35pt,
  arc=1mm,
  left=2mm,
  right=2mm,
  top=1mm,
  bottom=1mm,
  title={{\tikz[baseline=-0.6ex]\node[circle, fill=black!18, inner sep=1.1pt] {{\scriptsize i}};\ #1}},
  fonttitle=\bfseries,
  coltitle=black,
  colbacktitle=black!8,
  attach boxed title to top left={{yshift=-0.5mm, xshift=2mm}},
  boxed title style={{boxrule=0pt, arc=1mm}}
}}
\newcommand{{\ITinLingvoSubtitle}}{{{latex_title_subtitle}}}
\newcommand{{\ITinLingvoPlace}}{{{latex_title_place}}}
\newcommand{{\ITinLingvoYear}}{{{latex_title_year}}}
\newcommand{{\ITinLingvoUDC}}{{{latex_imprint_udc}}}
\newcommand{{\ITinLingvoPages}}{{\ztotpages}}
\newcommand{{\ITinLingvoConditionalPrintSheets}}{{%
  \num[
    round-mode=places,
    round-precision=1,
    minimum-decimal-digits=1,
    output-decimal-marker={{,}}
  ]{{\fpeval{{\ITinLingvoPages * {latex_imprint_page_area_cm2} / 5400}}}}%
}}
\newcommand{{\ITinLingvoBibliography}}{{{latex_imprint_bibliography}}}
\newcommand{{\ITinLingvoExtent}}{{{latex_imprint_extent}}}
\newcommand{{\ITinLingvoAnnotation}}{{{latex_imprint_annotation}}}
\newcommand{{\ITinLingvoKeywords}}{{{latex_imprint_keywords}}}
\newcommand{{\ITinLingvoCopyright}}{{{latex_imprint_copyright}}}
\newcommand{{\ITinLingvoImprintPage}}{{%
{latex_imprint}
}}
{latex_titlepage}
\makeatother
""",
}

myst_enable_extensions = [
    "deflist",
    "dollarmath",
    "amsmath",
    "colon_fence",
    "attrs_block",
    "attrs_inline",
    "fieldlist",
]

# нумерація фігур/таблиць/лістингів
numfig = True
# глибина секцій у номері (0 = глобальна нумерація; 1 = усередині розділу і т.д.)
numfig_secnum_depth = 1
# україномовні підписи
numfig_format = {
    "figure": "Рис. %s",
    "table": "Таблиця %s",
    "code-block": "Лістинг %s",
    "section": "Розділ %s",
}

PDF_DOWNLOAD_NAME = "ITinLingvo.pdf"


def copy_pdf_to_html(app, exception):
    if exception or app.builder.name != "html":
        return

    source_pdf = Path(app.srcdir) / "_build" / "latex" / "sphinx.pdf"
    if not source_pdf.exists():
        return

    target_pdf = Path(app.outdir) / "_static" / PDF_DOWNLOAD_NAME
    target_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_pdf, target_pdf)


def add_pdf_download_button(app, pagename, templatename, context, doctree):
    header_buttons = context.get("header_buttons")
    if header_buttons is None:
        return

    pdf_url = f"{context['pathto']('_static', 1)}/{PDF_DOWNLOAD_NAME}"
    header_buttons.append(
        {
            "type": "link",
            "url": pdf_url,
            "tooltip": "Завантажити PDF",
            "icon": "fas fa-file-pdf",
            "text": "PDF",
            "label": "download-course-pdf-button",
        }
    )


def setup(app):
    app.connect("build-finished", copy_pdf_to_html)
    # PDF button disabled in student HTML publication
