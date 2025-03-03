#------------------------------------------------------------------------------
# Functions to process strings, remove new lines, html (if requested), etc.
# Original file copyright: see ./__init__.py for details
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

"""Functions to process strings, remove new lines, html (if requested), etc."""

#--------------------------------------------------------------------------
# anki.utils in 2019-11
#   reComment = re.compile("(?s)<!--.*?-->")
#   reStyle = re.compile("(?si)<style.*?>.*?</style>")
#   reScript = re.compile("(?si)<script.*?>.*?</script>")
#   reTag = re.compile("(?s)<.*?>")
#   reEnts = re.compile(r"&#?\w+;")
#   reMedia = re.compile("(?i)<img[^>]+src=[\"']?([^\"'>]+)[\"']?[^>]*>")
#
# def strip_html(s):
#     s = reComment.sub("", s)
#     s = reStyle.sub("", s)
#     s = reScript.sub("", s)
#     s = reTag.sub("", s)
#     s = entsToTxt(s)
#     return s
#--------------------------------------------------------------------------
import re

from anki.utils import strip_html as anki_utils_stripHTML

def exporter_strip_html(text):
    # very basic conversion to text
    s = text
    s = re.sub(r"(?i)<(br ?/?|div|p)>", " ", s)
    s = re.sub(r"\[sound:[^]]+\]", "", s)
    s = anki_utils_stripHTML(s)
    s = re.sub(r"[ \n\t]+", " ", s)
    s = s.strip()
    return s


def exporter_escape_text(text):
    "     Escape newlines, tabs, CSS and quotechar."
#     fixme: we should probably quote fields with newlines
#     instead of converting them to spaces
#
# the fixme note was introduced in commit
# 47940680d27dca0c2f4bca2acd83630414c56db3 in 2015-11-17. The commit
# message reads:
#   don't convert newlines into br tags in export
#   fixes https://anki.tenderapp.com/discussions/ankidesktop/15795-export
#   -error-doubling-br-tags
#   This code dates back a few years, and was probably a naive solution
#   for files breaking when exported with newlines. Ideally we should be
#   preserving the newlines and wrapping the field in quotes, but since
#   some people may be relying on exported files not to be quoted, we'll
#   wait to change this until the next major release. For now, we'll use
#   a space instead, which should not alter the appearance of the
#   rendered HTML.

    text = text.replace("\n", " ")
    text = text.replace("\t", " " * 8)
    text = re.sub("(?i)<style>.*?</style>", "", text)
    text = re.sub(r"\[\[type:[^]]+\]\]", "", text)
    if "\"" in text:
        text = "\"" + text.replace("\"", "\"\"") + "\""
    return text


def process_text(text, keephtml):
    if not keephtml:
        text = exporter_strip_html(text)
    text = exporter_escape_text(text)
    return text


def esc(s, keephtml):
    # from anki.exporting.TextCardExporter.doExport
    # strip off the repeated question in answer if exists
    s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
    # Exporter.processText in 2019-11 replaces linebreaks with spaces
    return process_text(s, keephtml)
