#------------------------------------------------------------------------------
# Helper functions to get review log, save dialog box, and current time, etc.
# Copyright (C) 2025 Ray Griner (for modifications to original)
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

"""Helper functions to get review log, save dialog box, and current time."""

import datetime

from aqt import mw
from aqt.qt import (
    QFileDialog,
    QStandardPaths,
)

# No last interval in `entry`, so we won't do this all in same fn.
def all_review_memory_states(csd):
    all_reviews = ""
    for entry in csd.revlog:
        all_reviews += "#".join((str(entry.time),
                            (f"{entry.memory_state.difficulty:.3f}"
                                     if entry.memory_state else ""),
                            (f"{entry.memory_state.stability:.3f}"
                                     if entry.memory_state else ""),
                          )) + "-----"
    return all_reviews

def all_reviews_for_card(cid):
    entries = mw.col.db.all(
        "select id, type, ease, ivl, lastivl, time, factor "
        "from revlog where cid = ?", cid)
    if not entries:
        return ""
    all_reviews = ""
    for (date_millis, review_kind, ease, ivl, lastivl, taken_millis,
         factor) in entries:
        all_reviews += "#".join((str(date_millis),
                             str(review_kind),
                             str(ease),
                             str(ivl),
                             str(lastivl),
                             str(taken_millis),
                             str(factor) if factor else "",
                           )) + "-----"
    return all_reviews


def getSaveDir(parent, title, identifier_for_last_user_selection):  # pylint: disable=invalid-name
    config_key = identifier_for_last_user_selection + "Directory"
    default_path = QStandardPaths.writableLocation(
                       QStandardPaths.StandardLocation.DocumentsLocation)
    path = mw.pm.profile.get(config_key, default_path)
    return QFileDialog.getExistingDirectory(parent, title, path,
                                            QFileDialog.Option.ShowDirsOnly)


def now():    #time
    return datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

