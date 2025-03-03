#------------------------------------------------------------------------------
# Set up menus and do most work except writing and getting card properties.
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

"""Set up menus and do most work except writing and getting card properties."""

from anki.hooks import addHook
from anki.utils import (
    ids2str,
    split_fields,
)
from aqt import mw
from aqt.qt import (
    QAction,
    Qt,
)
from aqt.utils import (
    askUser,
    getSaveFile,
    tooltip,
)

from .config import gc
from .card_properties import current_card_deck_properties
from .helper_functions import (
    now,
    getSaveDir,
)
from .string_processing import(
    esc,
    process_text,
)
from .writing import (
    write_rows_to_csv,
    write_to_multiple_csvs,
)

def make_row_list_for_card(cid, columns_to_export, keephtml):
    card = mw.col.get_card(cid)
    note = card.note()
    model = card.note_type()
    props = current_card_deck_properties(card)
    outlist = []
    for i in columns_to_export:
        thisstr = ""
        if i == "question":
            q = esc(card.question(), keephtml)
            if gc("card_export_maxLength"):
                q = q[:gc("card_export_maxLength")]
            thisstr = q
        elif i == "answer":
            a = esc(card.answer(), keephtml)
            if gc("card_export_maxLength"):
                a = a[:gc("card_export_maxLength")]
            thisstr = a
        elif i == "tags":
            thisstr = " ".join(note.tags)
        elif i in props:
            thisstr = props[i]
        elif i.startswith("card_export_column__field_"):
            try:
                cd = gc(i)
            except:
                tooltip(f"Error in Add-on. '{i}' not in config. Aborting ...")
            else:
                if isinstance(cd, dict):
                    field_to_fetch = cd.get(props["c_NoteType"])
                    if field_to_fetch:
                        for index, fi in enumerate(model["flds"]):
                            if fi["name"] == field_to_fetch:
                                fi_cnt = note.fields[index]
                                fi_cnt = process_text(fi_cnt, keephtml)
                                if gc("card_export_maxLength"):
                                    fi_cnt = fi_cnt[:gc("card_export_maxLength")]  # pylint: disable=line-too-long
                                thisstr = fi_cnt
        outlist.append(thisstr)
    return outlist


def info_for_cids_to_list_of_lists(cids, keephtml):
    columns_to_export = gc("card_export__columns")
    if not columns_to_export:
        tooltip("error in add-on config. No setting found which columns to "
                "export. Aborting ...")
        return
    rows = []
    rows.append(columns_to_export)
    for c in cids:
        rows.append(make_row_list_for_card(c, columns_to_export, keephtml))
    return rows


def get_notes_info(cids, keephtml):
    # extracted from anki.exporting.TextNoteExporter
    d = {}
    for e in [m["id"] for m in mw.col.models.all()]:
        d[str(e)] = []
    for id_, modelid, mod, flds, tags in mw.col.db.execute(f"""
select id, mid, mod, flds, tags from notes
where id in
(select nid from cards
where cards.id in {ids2str(cids)})"""):
        row = []
        if gc("note_export_include_note_id"):
            row.append(str(id_))
        if gc("note_export_include_modification_time"):
            row.append(str(mod))
        if gc("note_export_include_tags"):
            row.append(tags.strip())
        row.extend([process_text(f, keephtml) for f in split_fields(flds)])
        d[str(modelid)].append(row)
    # remove empty keys
    out = {k: v for k, v in d.items() if v}
    return out


def uniquify_clean_model_names_in_dict(dol, limitlength):
    # dict of lists
    # model names, but don't just rely on model names in case someone uses
    # "Basic_" and "Basic*" ...
    illegal = [">", "<", ":", "/", "\\", '"', "|", "*", ]
    out = {}
    for k, v in dol.items():
        modelname = ""
        for c in mw.col.models.get(int(k))["name"]:
            modelname += c if c not in illegal else "_"
        if limitlength:
            # Excel worksheet names must be under 30 chars
            newkey = modelname[:15] + "___" + k
        else:
            newkey = modelname + "___" + k
        out[newkey] = v
    return out


def add_column_names_for_notes_as_first_element(dol):
    # dict of lists
    for k, v in dol.items():
        cnames = []
        if gc("note_export_include_note_id"):
            cnames.append("note_id")
        if gc("note_export_include_modification_time"):
            cnames.append("last modification time")
        if gc("note_export_include_tags"):
            cnames.append("tags")
        model = mw.col.models.get(int(k))
        fnames = [f["name"] for f in model["flds"]]
        cnames.extend(fnames)
        v.insert(0, cnames)
    return dol


def save_helper(browser, ftype, notesonly):
    if notesonly and ftype == "csv":
        out = getSaveDir(parent=browser,
                title="Select Folder for csv files for exported notes",
                identifier_for_last_user_selection="notesOnlyCsvExport")
    nownow = now()
    if not notesonly and ftype == "csv":
        out = getSaveFile(browser,
                "Export Selected From Browser to Csv",  # windowtitle
                "export_cards_csv",  # dir_description - used to remember
                                     # last user choice
                "Cards as CSV",  # key
                ".csv",  # ext
                f"Anki_cards___{nownow}.csv")  # filename
    return out


def exp(browser, ftype, keephtml, notesonly):
    cids = browser.selectedCards()
    if cids:
        msg = f'Exporting many {"notes" if notesonly else "cards"} might take a while. Continue?'   # pylint: disable=line-too-long
        if not askUser(msg, defaultno=True):
            return
        save_path = save_helper(browser, ftype, notesonly)
        if not save_path:
            return
        mw.progress.start(immediate=True)
        try:
            if notesonly:
                rows_by_model_raw = get_notes_info(sorted(cids), keephtml)
                if gc("row_on_top_has_column_names"):
                    rows_by_model_raw = add_column_names_for_notes_as_first_element(rows_by_model_raw)  # pylint: disable=line-too-long
                if ftype == "csv":
                    rows_by_model = uniquify_clean_model_names_in_dict(
                                        rows_by_model_raw, False)
                    write_to_multiple_csvs(save_path, rows_by_model)
            else:
                rows = info_for_cids_to_list_of_lists(sorted(cids), keephtml)
                if ftype == "csv":
                    write_rows_to_csv(save_path, rows, True)
        finally:
            mw.progress.finish()
            tooltip(f"Export to {str(save_path)} finished", period=6000)


def exp_browser_visible___45_and_newer(browser, ftype, keephtml):
    save_path = save_helper(browser, ftype, notesonly=False)
    if not save_path:
        return

    rows = []  # list of lists

    # write column names (header) as first row
    # not translated
    column_names__technical = browser.table._model._state.active_columns    # pylint: disable=protected-access
    #column_names__displayed = []
    column_names__displayed = ["cid"]  # make first column always cid (card id)
    for i in range(browser.table._model.len_columns()):  # pylint: disable=protected-access
        column_names__displayed.append(
            browser.table._model.headerData(i, Qt.Orientation.Horizontal,   # pylint: disable=protected-access
                                            Qt.ItemDataRole.DisplayRole))
    rows.append(column_names__displayed)

    for qmi in browser.table._selected():  # qmi = QModelIndex, # pylint: disable=protected-access
        # row_idx = qmi.row()
        # browser.table._model.get_note_id(qmi) is not in .45
        nid = browser.table._model.get_note_ids([qmi])[0]  # pylint: disable=protected-access
        cid = browser.table._model.get_card_ids([qmi])[0]  # pylint: disable=protected-access

        this_card_field_names = None
        row = browser.table._model.get_row(qmi)   # pylint: disable=protected-access
        contents_one_row = ["" for i in range(len(column_names__displayed)+ 1)]
        contents_one_row[0] = cid
        for idxc, _ in enumerate(row.cells):
            this_column_name_technical = column_names__technical[idxc]
            field_content = ""
            if keephtml and (this_column_name_technical.startswith("_field_")
                             or this_column_name_technical == "noteFld"):
                if not this_card_field_names:
                    note = browser.col.get_note(nid)
                    # same as Card.note_type (which was Card.model)
                    note_type = browser.col.models.get(note.mid)
                    this_card_field_names = browser.mw.col.models.field_names(
                                                    note_type)
                if this_column_name_technical == "noteFld":
                    # code taken from browser.DataModel.columnData
                    note_type_sort_field = note_type.get("sortf")
                    field_content = note.fields[note_type_sort_field]
                else:
                    for fidx, fname in enumerate(this_card_field_names):
                        if fname in this_column_name_technical:
                            field_content = note.fields[fidx]
                content = field_content
            else:
                content = row.cells[idxc].text
            #contents_one_row[idxc] = content
            contents_one_row[idxc+1] = content
        rows.append(contents_one_row)

    if ftype == "csv":
        write_rows_to_csv(save_path, rows, True)

    tooltip(f'Export to "{str(save_path)}" finished', period=6000)


def exp_brows_visi(browser, ftype, keephtml):
    exp_browser_visible___45_and_newer(browser, ftype, keephtml)


def setupMenu(browser):     # pylint: disable=invalid-name
    new_action1 = QAction("Export selected cards to csv", browser)
    new_action1.triggered.connect(lambda _,
                                  b=browser: exp(b, ftype="csv", keephtml=True,
                                                 notesonly=False))

    new_action2 = QAction("Export notes for selected cards to csv (one file"
                          " per note type)", browser)
    new_action2.triggered.connect(lambda _,
                                  b=browser: exp(b, ftype="csv", keephtml=True,
                                                 notesonly=True))

    new_action3 = QAction("Export selected cards with columns shown to csv",
                          browser)
    new_action3.triggered.connect(lambda _,
                                  b=browser: exp_brows_visi(b, ftype="csv",
                                                            keephtml=True))

    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(new_action1)
    browser.form.menuEdit.addAction(new_action2)
    browser.form.menuEdit.addAction(new_action3)

addHook("browser.setupMenus", setupMenu)
