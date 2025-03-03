# Overview

This is a add-on designed to export from the Anki flashcard software desktop
application (Anki) all information necessary to recreate the statistical
reports that are available in the `Stats` window of Anki. The export must
be done on the same day the `Stats` window is opened for results to match
(where 'same day' is with respect to the rollover hour configured in Anki that
defines day boundaries).

This is a modification of add-on [export cards/notes from browser with
metadata to csv or xlsx](https://ankiweb.net/shared/info/1967530655) (updated:
2024-03-28) (the 'original add-on').

# Functionality
The add-on adds three menu items to the card/note browser in Anki. The user
selects cards or notes in the browser and then can select one of:
- **Export selected cards to csv**
- **Export notes for selected cards to csv (one file per note type)**
- **Export selected cards with columns shown to csv**

For the first option, the output fields are pre-defined in the `config.json`
file in the add-on directory. This can be edited either manually or
with the add-on configuration manager. Available fields are described
in [config.md](config.md). For the third option, only the columns shown
in the browser and `cid` (the card unique identifier) are exported.
The expectation is that the first option will be most commonly used.

The program will take some time to run with a large number of cards.
For reference, a deck with 32000 cards (only a quarter of which are
actively studied) takes about 25 seconds to export using the first
option, with the second and third options significantly faster.

## Supported Versions

This add-on was tested on Anki v25.02 on Linux. It may not work on
earlier versions, and it seems especially likely it will not work on
versions that predate the integration of the FSRS algorithm in Anki, but
this has not been tested.

# Comparison to Original Add-On
Below is a high-level summary of functionality added and removed compared
to the original add-on. This list may not be exhaustive.
- The ability to export the raw values of FSRS retrievability, difficulty,
  stability, and desired retention was added. For example, difficulty and
  stability are exported with three decimal digits of precision to match
  the values as stored in the database. These values are currently available
  in the original add-on only by downloading the rounded fields displayed
  in the browser.
- The ability to export the following variables was added:
  - Last interval (`lastivl`) for each review. This is used to differentiate
    between `Young` and `Mature` reviews for reporting.
  - Days elapsed since collection start (`col_TodayDaysElapsed`). This is used
    to determine the day a review is due when `due`/`odue` is not recorded
    as a time stamp.
  - Collection rollover hour (`col_RolloverHour`). This is used to assign
    date/times to the correct day (adjusted for rollover).
- Fields are now for the most part passed through out without modification. For
  example:
  - The database field `card.due` is output in the `c_due` field. There is no
    attempt to determine when this represents a local datetime and to then 
    convert it to such a date-time value.
  - Datetime values stored in the database as milli-seconds are not divided by
    1000 or converted to time-stamps, unless this is already done by the Anki
    application.
- Fields not necessary to recreate the `Stats` window and not loaded using 
  `card._load_backend_data` or `card.card_stats_data` were removed to simplify
  the code. These might be re-added in the future. In particular, code for
  exporting a number of deck properties is removed.
- Output variable names were sometimes changed. In particular, `c_var` is now
  used when outputting `card.var`, i.e, the `var` attribute of the Python `card`
  object, and `csd_var` is used for a variable returned by
  `card.card_stats_data()`. (Here `card.var` and `card.card_stats_data()` refer
  to the Anki desktop application code.)
- Code for writing to Excel-formatted output (xlsx files) was removed.
- HTML can no longer by removed from output during the export. The functions
  that perform these operations were kept in the module, so users can call these
  if desired by post-processing the export file.
- Function names that generated deprecation warnings were updated.
- `meta.json` was removed. It's unclear if this is an old file format required
  by AnkiWeb or a file automatically generated by AnkiWeb. In any case, the
  AnkiWeb documentation now makes reference to `manifest.json` and a
  `manifest.json` was created.
- The code was standardized using `pylint`.

# Using the Output
An example Python program that shows how to recreate (in tabular form) the
charts and tables in the `Stats` window is
[here](https://github.com/ghrgriner/anki-stats). The same repository also
contains a [wiki](https://github.com/ghrgriner/anki-stats/wiki) with
documentation on the analysis population used in each report in the `Stats`
window.
