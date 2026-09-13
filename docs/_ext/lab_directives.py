"""Custom directives for lab manuals."""

from html import escape

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import texescape
from sphinx.util.docutils import SphinxDirective, SphinxRole


class BaseLabBlockDirective(SphinxDirective):
    """Render a standardized lab block."""

    has_content = True
    option_spec = {
        "title": directives.unchanged,
        "hide-title": directives.flag,
    }
    default_title = ""
    block_class = ""

    def run(self):
        title_text = self.options.get("title", self.default_title)
        if "hide-title" in self.options:
            container = nodes.container(classes=["lab-block", self.block_class])
            self.state.nested_parse(self.content, self.content_offset, container)
            return [container]

        admonition = nodes.admonition(classes=["lab-block", self.block_class])
        admonition += nodes.title(text=title_text)
        self.state.nested_parse(self.content, self.content_offset, admonition)
        return [admonition]


class LabGoalDirective(BaseLabBlockDirective):
    """Render a standardized lab goal block."""

    default_title = "Мета роботи"
    block_class = "lab-goal"


class LabPlanDirective(BaseLabBlockDirective):
    """Render a standardized lab plan block."""

    default_title = "План роботи"
    block_class = "lab-plan"


class TermBlockNode(nodes.General, nodes.Element):
    """A semantic definition block for a term."""


class TermDirective(SphinxDirective):
    """Render a term definition block."""

    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        term = self.arguments[0].strip()
        node = TermBlockNode(term=term, classes=["lab-term"])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_term_html(self, node):
    term = escape(node["term"])
    self.body.append(
        '<div class="lab-term">'
        f'<p class="lab-term-title">{term}</p>'
    )


def depart_term_html(self, node):
    self.body.append("</div>")


def visit_term_latex(self, node):
    term = texescape.escape(node["term"])
    self.body.append(f"\\begin{{sphinxtermblock}}{{{term}}}\n")


def depart_term_latex(self, node):
    self.body.append("\\end{sphinxtermblock}\n")


class FigNumNode(nodes.Inline, nodes.TextElement):
    """Inline node that renders a clickable figure number."""


class FigNumRole(SphinxRole):
    """Reference a figure by number without the figure prefix."""

    def run(self):
        target = self.text.strip()
        node = FigNumNode(
            "",
            target,
            reftarget=target,
            fromdocname=self.env.docname,
        )
        return [node], []


def _label_data(builder, target):
    std_domain = builder.env.get_domain("std")
    labels = getattr(std_domain, "labels", None)
    if labels is None:
        labels = std_domain.data.get("labels", {})
    return labels.get(target)


def _figure_info(builder, target):
    label = _label_data(builder, target)
    if label is None:
        return None

    docname, label_id, _ = label
    figures = builder.env.toc_fignumbers.get(docname, {}).get("figure", {})
    number = figures.get(label_id)
    if number is None:
        return None

    number_text = ".".join(str(part) for part in number)
    return docname, label_id, number_text


def _figure_number(builder, target):
    info = _figure_info(builder, target)
    if info is None:
        return "??"
    return info[2]


def visit_fig_num_html(self, node):
    info = _figure_info(self.builder, node["reftarget"])
    if info is None:
        self.body.append("??")
        raise nodes.SkipNode

    docname, label_id, number = info
    uri = self.builder.get_relative_uri(node["fromdocname"], docname)
    href = f"{uri}#{label_id}" if uri else f"#{label_id}"
    self.body.append(
        f'<a class="fig-num-reference" href="{escape(href, quote=True)}">'
        f'{escape(number)}</a>'
    )
    raise nodes.SkipNode


def visit_fig_num_latex(self, node):
    info = _figure_info(self.builder, node["reftarget"])
    if info is None:
        self.body.append("??")
        raise nodes.SkipNode

    docname, label_id, number = info
    self.body.append(
        f"\\hyperref[\\detokenize{{{docname}:{label_id}}}]{{{number}}}"
    )
    raise nodes.SkipNode


def visit_fig_num_text(self, node):
    self.add_text(_figure_number(self.builder, node["reftarget"]))
    raise nodes.SkipNode


class GoogleDocDirective(SphinxDirective):
    """Embed a Google Doc in HTML and link to it in print/PDF output."""

    has_content = False
    option_spec = {
        "doc-id": directives.unchanged_required,
        "title": directives.unchanged,
        "height": directives.nonnegative_int,
    }

    def run(self):
        doc_id = self.options["doc-id"].strip()
        title = self.options.get("title", "Документ онлайн")
        height = self.options.get("height", 800)
        preview_url = f"https://docs.google.com/document/d/{doc_id}/preview"
        view_url = f"https://docs.google.com/document/d/{doc_id}/view"

        if self.env.app.builder.format == "html":
            html = (
                '<iframe class="google-doc-embed" '
                f'style="width:100%;height:{height}px;border:0;" '
                f'title="{escape(title, quote=True)}" '
                f'src="{escape(preview_url, quote=True)}"></iframe>'
            )
            return [nodes.raw("", html, format="html")]

        paragraph = nodes.paragraph()
        paragraph += nodes.strong(text=f"{title}: ")
        paragraph += nodes.reference(view_url, view_url, refuri=view_url)
        return [paragraph]


class GoogleDrawingDirective(SphinxDirective):
    """Render a Google Drive image URL as a Sphinx figure."""

    has_content = True
    option_spec = {
        "url": directives.unchanged,
        "width": directives.nonnegative_int,
        "height": directives.nonnegative_int,
        "display-width": directives.length_or_percentage_or_unitless,
        "alt": directives.unchanged,
        "name": directives.unchanged,
    }

    def run(self):
        display_width = self.options.get("display-width", "100%")
        url = (self.options.get("url") or "").strip()
        is_empty_url = not url

        if is_empty_url:
            depth = self.env.docname.count("/")
            placeholder = "google-drawing-placeholder.png"
            if self.env.app.builder.format == "html":
                placeholder = "google-drawing-placeholder.svg"
            image_url = "../" * depth + f"_static/{placeholder}"
        else:
            image_url = url

        image = nodes.image(
            uri=image_url,
            alt=self.options.get("alt", "Рисунок з Google Drive"),
            width=display_width,
        )
        figure = nodes.figure("", image)
        if is_empty_url:
            figure["classes"].append("google-drawing-placeholder")
        self.add_name(figure)

        if self.content:
            parsed = nodes.Element()
            self.state.nested_parse(self.content, self.content_offset, parsed)
            if len(parsed) == 1 and isinstance(parsed[0], nodes.paragraph):
                figure += nodes.caption("", "", *parsed[0].children)
            else:
                figure += nodes.legend("", *parsed.children)

        return [figure]


def setup(app):
    app.add_node(
        FigNumNode,
        html=(visit_fig_num_html, None),
        latex=(visit_fig_num_latex, None),
        text=(visit_fig_num_text, None),
    )
    app.add_role("fig-num", FigNumRole())
    app.add_node(
        TermBlockNode,
        html=(visit_term_html, depart_term_html),
        latex=(visit_term_latex, depart_term_latex),
    )
    app.add_directive("term", TermDirective)
    app.add_directive("lab-goal", LabGoalDirective)
    app.add_directive("lab-plan", LabPlanDirective)
    app.add_directive("google-doc", GoogleDocDirective)
    app.add_directive("google-drawing", GoogleDrawingDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
