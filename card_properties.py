#------------------------------------------------------------------------------
# Get card properties and a few collectoin properties.
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

"""Get card properties and a few collection properties."""

from aqt import mw

from .helper_functions import (
    all_reviews_for_card,
    all_review_memory_states,
)

def current_card_deck_properties(card):
    #############
    data = mw.col.db.scalar(
        "select data from cards where id = ?", card.id)

    template = card.template()
    model = card.note_type()
    p = dict()
    # (mostly) Card Stats as seen in Browser
    # Use names in original addon, except for fields taken unmodified from
    # an attribute of Card. For these, use:
    # - `c_var_name` for `Card.var_name`, i.e., a property taken directly
    # from an attribute of the Python Card object,
    # - `c_PropName` for some other card property
    # - `col_prop_name` for some property of the collection.
    p["c_Ease"] = f"{card.factor // 10}"
    p["c_CardType"] = template["name"]
    p["c_NoteType"] = model["name"]
    p["c_ModelId"] = model["id"]  # changed from c_model_id in orig addon
    p["c_Deck"] = mw.col.decks.name(card.did)
    p["c_Data"] = data
    p["col_RolloverHour"] = mw.col.conf.get("rollover", 4)
    p["col_TodayDaysElapsed"] = mw.col.sched.today

    p["c_due"] = card.due
    p["c_factor"] = card.factor
    p["c_odue"] = card.odue
    p["c_odid"] = card.odid
    p["c_ivl"] = card.ivl
    p["c_queue"] = card.queue
    p["c_nid"] = card.nid
    p["c_id"] = card.id
    p["c_type"] = card.type

    if card.memory_state:
        # these are stored with 3 decimal places in cards.data so re-round
        # before export.
        p["c_stability"] = f"{card.memory_state.stability:.3f}"
        p["c_difficulty"] = f"{card.memory_state.difficulty:.3f}"
    else:
        p["c_stability"] = ""
        p["c_difficulty"] = ""
    p["desired_retention"] = (f"{card.desired_retention:.3f}"
                                   if card.desired_retention else "")

    csd = mw.col.card_stats_data(card.id)
    p["revlog_entries"] = all_reviews_for_card(card.id)
    p["revlog_memory_states"] = all_review_memory_states(csd)

    # Get anything else loaded by Card._load_from_backend_card
    # this and the previous variables also give everything needed
    p["c_mod"] = card.mod
    p["c_usn"] = card.usn
    p["c_reps"] = f"{card.reps:d}"
    p["c_lapses"] = f"{card.lapses:d}"
    p["c_left"] = card.left
    p["c_flags"] = card.flags
    p["c_custom_data"] = card.custom_data
    p["c_original_position"] = (card.original_position
                                    if card.original_position else "")

    retr = csd.fsrs_retrievability
    p["csd_fsrs_retrievability"] = retr if retr else ""
    p["csd_preset"] = csd.preset
    p["csd_first_review"] = csd.first_review
    p["csd_latest_review"] = csd.latest_review
    p["csd_due_date"] = csd.due_date if csd.due_date else ""
    p["csd_average_secs"] = csd.average_secs
    p["csd_total_secs"] = csd.total_secs

    return p
