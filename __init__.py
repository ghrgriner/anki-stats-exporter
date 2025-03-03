#------------------------------------------------------------------------------
# Provide module-level information.
# Copyright (C) 2025 Ray Griner (for modifications to original)
# Original file copyright: see below for details
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

"""
This is a modification to an add-on that was released under the GNU Affero
General Public License, version 3. The modifications are copyright
Ray Griner (rgriner_fwd@outlook.com). The modifications are also released 
under the GNU Affero General Public License, version 3.

The original add-on was "export cards/notes from browser with metadata to csv
or xlsx" (updated: 2024-03-28) and is available on AnkiWeb at:
https://ankiweb.net/shared/info/1967530655.

The purpose of this modified add-on and a high-level summary of differences
from the original add-on are documented in README.md. The git repository
for this modified add-on is: https://github.com/ghrgriner/anki-stats-exporter.
Check there for the latest program version and documentation.

The remainder of this docstring after the horizontal line below is the
copyright and license information from the original add-on. However, it
should be noted that the directory `xlsxwriter` in the original add-on is
not included in this modified add-on. There was also no `gpl.py` file in
the original add-on.

-------------------------------------------------------------------------------

Add-on for Anki 2.1
Export Selected Cards from the Browser to csv. You can determine the columns in the csv
via the add-on config dialog.

Copyright: - Ankitects Pty Ltd and contributors
           - 2019 ijgnd
           - for bundled files see below

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.



This add-on uses the file gpl.py covered by the following copyright and  
permission notice:

    License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
    Copyright: Steve AW <steveawa@gmail.com>
               fickle_123@hotmail.com




This add-on incorporates work (xlsxwriter) covered by the following copyright and  
permission notice:

    XlsxWriter is released under a BSD license.

    Copyright (c) 2013, John McNamara <jmcnamara@cpan.org> All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted 
    provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this list of 
        conditions and the following disclaimer.
        2. Redistributions in binary form must reproduce the above copyright notice, this list of 
        conditions and the following disclaimer in the documentation and/or other materials provided 
        with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR 
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
    POSSIBILITY OF SUCH DAMAGE.

    The views and conclusions contained in the software and documentation are those of the authors 
    and should not be interpreted as representing official policies, either expressed or implied, 
    of the FreeBSD Project.
"""

__author__ = 'Ray Griner'
__version__ = '0.1.0'

from . import export
