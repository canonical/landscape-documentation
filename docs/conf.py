import datetime
import ast

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Our starter pack uses the custom Canonical Sphinx extension
# to keep all documentation based on it consistent and on brand:
# https://github.com/canonical/canonical-sphinx


#######################
# Project information #
#######################

# Project name

project = "Landscape"
author = "Canonical Ltd."


# Sidebar documentation title; best kept reasonably short
# To include a version number, add it here (hardcoded or automated).
# To disable the title, set to an empty string.

html_title = project + " documentation"


# Copyright string; shown at the bottom of the page
#
# Now, the starter pack uses CC-BY-SA as the license
# and the current year as the copyright year.
#
# If your docs need another license, specify it instead of 'CC-BY-SA'.
#
# If your documentation is a part of the code repository of your project,
# it inherits the code license instead; specify it instead of 'CC-BY-SA'.
#
# NOTE: For static works, it is common to provide the first publication year.
#       Another option is to provide both the first year of publication
#       and the current year, especially for docs that frequently change,
#       e.g. 2022–2023 (note the en-dash).
#
#       A way to check a repo's creation date is to get a classic GitHub token
#       with 'repo' permissions; see https://github.com/settings/tokens
#       Next, use 'curl' and 'jq' to extract the date from the API's output:
#
#       curl -H 'Authorization: token <TOKEN>' \
#         -H 'Accept: application/vnd.github.v3.raw' \
#         https://api.github.com/repos/canonical/<REPO> | jq '.created_at'

copyright = "%s CC-BY-SA, %s" % (datetime.date.today().year, author)


# Documentation website URL
# NOTE: The Open Graph Protocol (OGP) enhances page display in a social graph
#       and is used by social media platforms; see https://ogp.me/

ogp_site_url = ""


# Preview name of the documentation website
ogp_site_name = project


# Preview image URL
ogp_image = \
    "https://assets.ubuntu.com/v1/253da317-image-document-ubuntudocs.svg"

# Product favicon; shown in bookmarks, browser tabs, etc. - can set custom one here
# html_favicon = '.sphinx/_static/favicon.png'

# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context

html_context = {
    # Product page URL; can be different from product docs URL
    "product_page": "ubuntu.com/landscape",

    # Product tag image; the orange part of your logo, shown in the page header

    # To add a tag image, uncomment and update as needed.
    # 'product_tag': '_static/tag.png',

    # Your Discourse instance URL
    "discourse": "https://discourse.ubuntu.com/c/project/landscape/89",

    # Your Mattermost channel URL
    "mattermost":
    "",

    # Your Matrix channel URL
    "matrix": "",

    # Your documentation GitHub repository URL
    "github_url": "https://github.com/canonical/landscape-documentation",

    # Docs branch in the repo; used in links for viewing the source files
    # 'github_version': 'main',
    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "/docs/",

    # To enable or disable the Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    # "sequential_nav": "both",

    # Enabling GH issues so the feedback button shows up
    'github_issues': 'enabled',

    "repo_default_branch": "main",
}

# Project slug; see https://meta.discourse.org/t/what-is-category-slug/87897
#
# If your documentation is hosted on https://docs.ubuntu.com/,
#       uncomment and update as needed.

# slug = ''

# Template and asset locations

html_static_path = [".sphinx/_static"]
templates_path = [".sphinx/_templates"]

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
    "http://nfs.sourceforge.net/#faq_d2"
]


# A regex list of URLs where anchors are ignored by 'make linkcheck'

linkcheck_anchors_ignore_for_url = [r"https://github\.com/.*",
                                    r"https://ubuntu.com/landscape"]

linkcheck_retries = 3

########################
# Configuration extras #
########################

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
#
# NOTE: By default, the following MyST extensions are enabled:
#       substitution, deflist, linkify

# myst_enable_extensions = set()

# MyST configurations
myst_heading_anchors = 4


# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html

# NOTE: The canonical_sphinx extension is required for the starter pack.
#       It automatically enables the following extensions:
#       - custom-rst-roles
#       - myst_parser
#       - notfound.extension
#       - related-links
#       - sphinx_copybutton
#       - sphinx_design
#       - sphinx_reredirects
#       - sphinx_tabs.tabs
#       - sphinxcontrib.jquery
#       - sphinxext.opengraph
#       - terminal-output
#       - youtube-links

extensions = [
    "canonical_sphinx",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx_sitemap"
]


# Excludes files or directories from processing

exclude_patterns = [
    "doc-cheat-sheet*",
]

# Adds custom CSS files, located under 'html_static_path'

html_css_files = [
    "css/pdf.css",
    "css/cookie-banner.css"
]

# Adds custom JavaScript files, located under 'html_static_path'
html_js_files = [
    "js/bundle.js"
 ]

# Specifies a reST snippet to be appended to each .rst file
rst_epilog = """
.. include:: /reuse/links.txt
"""

# Feedback button at the top; enabled by default
disable_feedback_button = False


# Your manpage URL
# NOTE: If set, adding ':manpage:' to an .rst file
#       adds a link to the corresponding man section at the bottom of the page.
# manpages_url = f'https://manpages.ubuntu.com/manpages/{codename}/en/' + \
#     f'man{section}/{page}.{section}.html'


# Specifies a reST snippet to be prepended to each .rst file
# This defines a :center: role that centers table cell content.
# This defines a :h2: role that styles content for use with PDF generation.

rst_prolog = """
.. role:: center
   :class: align-center
.. role:: h2
    :class: hclass2
"""

# Workaround for https://github.com/canonical/canonical-sphinx/issues/34

if "discourse_prefix" not in html_context and "discourse" in html_context:
    html_context["discourse_prefix"] = html_context["discourse"] + "/t/"

#####################
# PDF configuration #
#####################

latex_additional_files = [
    "./.sphinx/fonts/Ubuntu-B.ttf",
    "./.sphinx/fonts/Ubuntu-R.ttf",
    "./.sphinx/fonts/Ubuntu-RI.ttf",
    "./.sphinx/fonts/UbuntuMono-R.ttf",
    "./.sphinx/fonts/UbuntuMono-RI.ttf",
    "./.sphinx/fonts/UbuntuMono-B.ttf",
    "./.sphinx/images/Canonical-logo-4x.png",
    "./.sphinx/images/front-page-light.pdf",
    "./.sphinx/images/normal-page-footer.pdf",
]

latex_engine = "xelatex"
latex_show_pagerefs = True
latex_show_urls = "footnote"

with open(".sphinx/latex_elements_template.txt", "rt") as file:
    latex_config = file.read()

latex_elements = ast.literal_eval(latex_config.replace("$PROJECT", project))

## Sitemap configuration

html_baseurl = "https://documentation.ubuntu.com/landscape/"
sitemap_url_scheme = "{link}"

#############
# Redirects #
#############

# To set up redirects: https://documatt.gitlab.io/sphinx-reredirects/usage.html
# For example: 'explanation/old-name.html': '../how-to/prettify.html',

# To set up redirects in the Read the Docs project dashboard:
# https://docs.readthedocs.io/en/stable/guides/redirects.html

# NOTE: If undefined, set to None, or empty,
#       the sphinx_reredirects extension will be disabled.

redirects = {
    'how-to-guides/landscape-installation-and-set-up/install-on-google-cloud': '../cloud-providers/install-on-google-cloud',
    'how-to-guides/landscape-installation-and-set-up/install-on-microsoft-azure': '../cloud-providers/install-on-microsoft-azure',
    'how-to-guides/security/manage-repositories-in-an-air-gapped-or-offline-environment': '../../repository-mirrors/manage-repositories-in-an-air-gapped-or-offline-environment',
    'how-to-guides/security/install-landscape-in-an-air-gapped-or-offline-environment': '../../landscape-installation-and-set-up/install-landscape-in-an-air-gapped-or-offline-environment',
    'getting-started-with-landscape': '/tutorial'
}
