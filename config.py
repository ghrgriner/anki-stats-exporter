#------------------------------------------------------------------------------
# Get configuration information.
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

"""Get configuration information."""

from aqt import mw


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def get_anki_version():
    try:
        # 2.1.50+ because of bdd5b27715bb11e4169becee661af2cb3d91a443,
        #  https://github.com/ankitects/anki/pull/1451
        from anki.utils import point_version
    except:
        try:
            # introduced with 66714260a3c91c9d955affdc86f10910d330b9dd in
            # 2020-01-19, should be in 2.1.20+
            from anki.utils import pointVersion
        except:
            # <= 2.1.19
            from anki import version as anki_version
            return int(anki_version.split(".")[-1])
        else:
            return pointVersion()
    else:
        return point_version()
anki_point_version = get_anki_version()
