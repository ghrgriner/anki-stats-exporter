#------------------------------------------------------------------------------
# Functions to write csv files.
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

"""Functions to write csv files."""

import csv
import os

from .config import gc

def write_to_multiple_csvs(dir_, rows_by_model):
    for modelname, list_of_lists in rows_by_model.items():
        outfile = os.path.join(dir_, modelname + ".csv")
        write_rows_to_csv(outfile, list_of_lists, False)

def write_rows_to_csv(path, list_of_rows, iscards):
    def fmtline(li):
        delimiter.join(str(e) for e in li)
    with open(path, mode="w", encoding="utf-8") as file:
#------------------------------------------------------------------------------
# - `format_csv_dialect`: You can set 'excel', 'excel-tab', 'unix'.
# - `format_csv_delimiter`: if empty uses the default delimiter of the selected
#    dialect. Must be one-character string - otherwise python's csv module
#    won't work, see:
#      https://docs.python.org/3.6/library/csv.html#csv.Dialect.delimiter.
#    If you set a delimiter here that's longer than one character this add-on
#    will not use python's csv module for exporting. Instead it writes a text
#    file and ignores the settings format_csv_dialect, format_csv_quotechar,
#    format_csv_quotechar.
# - `format_csv_quotechar`: if empty uses the default delimiter of the selected
#    dialect. A one-character string, see
#      https://docs.python.org/3.6/library/csv.html#csv.Dialect.quotechar
# - `format_csv_quoting`: if empty uses the default delimiter of the selected
#    dialect. You can set "ALL", "MINIMAL", "NONNUMERIC", "NONE". For details,
#    see https://docs.python.org/3.6/library/csv.html#csv.QUOTE_ALL.
#-----------------------------------------------------------------------------
        csvdialect = gc("format_csv_dialect")
        if csvdialect not in ["excel", "excel-tab", "unix"]:
            # this is the default value for csv.writer in 3.6
            csvdialect = "excel"
        fmtparams = {}
        quoting = gc("format_csv_quoting")
        if quoting:
            quoting = quoting.upper()
        if quoting not in ["ALL", "MINIMAL", "NONNUMERIC", "NONE"]:
            quoting = ""
        if quoting:
            fmtparams["quoting"] = f"csv.QUOTE_{quoting}"
        quotechar = gc("format_csv_quotechar")
        if quotechar and len(quotechar) == 1:
            fmtparams["quotechar"] = quotechar
        delimiter = gc("format_csv_delimiter")
        if delimiter and (delimiter in ["\t"] or len(delimiter) == 1):
            fmtparams["delimiter"] = delimiter
        if not delimiter or delimiter in ["\t"] or len(delimiter) == 1:
            # for k, v in fmtparams.items():
            #     print(str(k), str(v))
            writer = csv.writer(file, csvdialect, **fmtparams)
            if iscards and gc("row_on_top_has_column_names"):
                writer.writerow(gc("card_export__columns"))  # column names
        # https://docs.python.org/3/library/csv.html#csv.csvwriter.writerows
            writer.writerows(list_of_rows)
        elif len(delimiter) >= 2:
            if iscards and gc("row_on_top_has_column_names"):
                file.write(fmtline(gc("card_export__columns")) + "\n")
            for r in list_of_rows:
                file.write(fmtline(r) + "\n")

