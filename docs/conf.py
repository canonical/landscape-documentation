import datetime
import os
import textwrap

import yaml

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# The Sphinx Stack uses the Canonical Sphinx theme to keep all documentation consistent
# and on brand:
# https://github.com/canonical/canonical-sphinx

#######################
# Project information #
#######################

# Project name
project = "Landscape"

# Author name; used in the default copyright statement in the page footer
author = "Canonical Ltd."

# The year in the copyright statement. The canonical-sphinx footer renders this as
# "© {copyright} {author}" (e.g. "© 2026 Canonical Ltd."), matching other Canonical
# documentation. The documentation content remains licensed under CC-BY-SA.
copyright = f"{datetime.date.today().year}"

# Sidebar documentation title
# To disable the title, set it to an empty string.
html_title = project + " documentation"

# Documentation website URL
# NOTE: The Landscape documentation is published at ubuntu.com/landscape/docs, so the
# canonical and Open Graph URLs are set explicitly rather than derived from
# READTHEDOCS_CANONICAL_URL.
ogp_site_url = "https://ubuntu.com/landscape/docs/"

# Preview name of the documentation website
ogp_site_name = project

# Preview image URL
ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"

# Product favicon; shown in bookmarks, browser tabs, etc.
# html_favicon = "_static/favicon.png"

# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
html_context = {
    # Product page URL; can be different from product docs URL
    "product_page": "ubuntu.com/landscape",
    # Product tag image; the orange part of your logo, shown in the page header
    # 'product_tag': '_static/tag.png',
    # Your Discourse instance URL
    "discourse": "https://discourse.ubuntu.com/c/project/landscape/89",
    # Your Mattermost channel URL
    "mattermost": "",
    # Your Matrix channel URL
    "matrix": "",
    # Your documentation GitHub repository URL If set, links for viewing the
    # documentation source files and creating GitHub issues are added at the bottom of
    # each page.
    "github_url": "https://github.com/canonical/landscape-documentation",
    # Docs branch in the repo; used in links for viewing the source files
    "repo_default_branch": "main",
    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "/docs/",
    # To enable or disable the Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    # "sequential_nav": "",
    # To enable listing contributors on individual pages, set to True
    "display_contributors": False,
    # Required for feedback button
    "github_issues": "enabled",
    # Passes the top-level 'author' value to the theme
    "author": author,
}

# Enables the edit button on pages, linking to the documentation source on GitHub.
html_theme_options = {
    "source_edit_link": "https://github.com/canonical/landscape-documentation",
}

# Project slug; used by canonical-sphinx for the documentation feedback path.
slug = "landscape/docs"

#######################
# Sitemap configuration: https://sphinx-sitemap.readthedocs.io/
#######################

# The base URL is set explicitly because the Landscape documentation is served from
# ubuntu.com/landscape/docs (it was changed during the Read the Docs domain migration).
html_baseurl = "https://ubuntu.com/landscape/docs/"

# sphinx-sitemap uses html_baseurl to generate the full URL for each page:
sitemap_url_scheme = "{link}"

# Custom sitemap filename for the ubuntu.com/landscape/docs publishing path:
sitemap_filename = "doc-sitemap.xml"

# Include `lastmod` dates in the sitemap:
sitemap_show_lastmod = True

# Pages excluded from the sitemap:
sitemap_excludes = [
    "404/",
    "genindex/",
    "search/",
]

################################
# Template and asset locations #
################################

html_static_path = ["_static"]
# _templates overrides only the footer, to restore the "Manage your tracker
# settings" link (the canonical-sphinx built-in footer leaves that slot empty).
# The header uses the canonical-sphinx built-in template.
templates_path = ["_templates"]

#############
# Redirects #
#############

# Add redirects to the 'redirects.txt' file
# https://sphinxext-rediraffe.readthedocs.io/en/latest/

# To set up redirects in the Read the Docs project dashboard:
# https://docs.readthedocs.io/en/stable/guides/redirects.html

rediraffe_redirects = "redirects.txt"

# Strips '/index.html' from destination URLs when building with 'dirhtml'
rediraffe_dir_only = True

############################
# sphinx-llm configuration #
############################

# This description is included in llms.txt to provide some initial context for the
# product docs.
llms_txt_description = textwrap.dedent(
    """\
    This is the documentation for Landscape, Canonical's systems management tool for
    managing and monitoring Ubuntu deployments across desktops, servers, cloud
    instances, and IoT devices.
    """
)

# The base URL for references built by sphinx-markdown-builder.
if os.environ.get("READTHEDOCS"):
    markdown_http_base = html_baseurl

###########################
# Link checker exceptions #
###########################

# A regex list of URLs that are ignored by 'make linkcheck'
linkcheck_ignore = [
    "http://127.0.0.1:8000",
    "https://github.com/canonical/landscape-documentation/*",
    "https://ubuntu.com/pro/dashboard",
    "https://support.canonical.com/",
    "https://support-portal.canonical.com/",
    "https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html",
    "https://wiki.ubuntu.com/Membership",
    "https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server",
    "https://ubuntu.com/aws#get-in-touch",
    "http://nfs.sourceforge.net/#faq_d2",
    "https://www.hashicorp.com/en/products/vault",
    "https://developer.hashicorp.com/vault/docs/concepts/production-hardening",
]

# A regex list of URLs where anchors are ignored by 'make linkcheck'
linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/.*",
    r"https://ubuntu.com/landscape",
]

# Give linkcheck multiple tries on failure
linkcheck_retries = 3

########################
# Configuration extras #
########################

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
# NOTE: By default, the following MyST extensions are enabled:
#   - substitution
#   - deflist
#   - linkify
# myst_enable_extensions = set()

# MyST configuration
myst_heading_anchors = 4

# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html
extensions = [
    "canonical_sphinx",
    "notfound.extension",
    "sphinx_design",
    "sphinx_rerediraffe",
    "sphinxcontrib.jquery",
    "sphinxext.opengraph",
    "sphinx_llm.txt",
    "sphinx_roles",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
    "sphinxcontrib.mermaid",
]

# Excludes files or directories from processing. The 'reuse' and '_includes'
# directories hold snippet files that are pulled in with MyST '{include}' rather than
# built as standalone pages, so they are excluded from source discovery.
exclude_patterns = [
    "doc-cheat-sheet*",
    ".venv*",
    "reuse/**",
    "**/_includes/**",
]

# Adds custom CSS files, located remotely or in 'html_static_path'.
html_css_files = [
    "https://assets.ubuntu.com/v1/d86746ef-cookie_banner.css",
]

# Adds custom JavaScript files, located remotely or in 'html_static_path'.
# overwrite_links.js rewrites the Read the Docs-hosted domain to the published
# ubuntu.com/landscape/docs domain in the header and Read the Docs flyout.
html_js_files = [
    "https://assets.ubuntu.com/v1/287a5e8f-bundle.js",
    "overwrite_links.js",
]

# Specifies a reST snippet to be prepended to each .rst file
# This defines a :center: role that centers table cell content.
# This defines a :h2: role that styles content for use with PDF generation.
rst_prolog = """
.. role:: center
   :class: align-center
.. role:: h2
    :class: hclass2
.. role:: woke-ignore
    :class: woke-ignore
.. role:: vale-ignore
    :class: vale-ignore
"""

# Configuration for Intersphinx projects
#
# intersphinx_mapping = {
#     "snap": ("https://snapcraft.io/docs/", None),
# }

#####################
# MyST substitutions #
#####################

# Landscape-specific: load global MyST text substitutions from reuse/substitutions.yaml
# so shared values can be reused across documentation pages.
if os.path.exists("./reuse/substitutions.yaml"):
    with open("./reuse/substitutions.yaml", "r") as fd:
        myst_substitutions = yaml.safe_load(fd.read())
