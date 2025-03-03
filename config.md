- also see https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
- for details see the source code of this add-on
- this modified add-on was tested on Anki v25.02 on Linux. It might not work
  on other platforms or versions. The original add-on was tested with
  Anki 2.1.15 on Linux.

### csv options
for exporting to csv this add-on uses python's csv module.
For details about this see https://docs.python.org/3.11/library/csv.html

You can set these values:

- `format_csv_dialect`: You can set 'excel', 'excel-tab', 'unix'.

- `format_csv_delimiter`: if empty uses the default delimiter of the selectd
  dialect. Must be one-character string (or something like "\t" - otherwise
  python's csv module won't work. , see 
  https://docs.python.org/3.11/library/csv.html#csv.Dialect.delimiter. If you
  set a delimiter here that's longer than one character this add-on will not
  use python's csv module for exporting. Instead it writes a text file and
  ignores the settings format_csv_dialect, format_csv_quotechar,
  format_csv_quotechar.

- `format_csv_quotechar`: if empty uses the default delimiter of the selected
  dialect. A one-character string, see:
  https://docs.python.org/3.11/library/csv.html#csv.Dialect.quotechar

- `format_csv_quoting`: if empty uses the default delimiter of the selected
  dialect. You can set "ALL", "MINIMAL", "NONNUMERIC", "NONE", for details see
  https://docs.python.org/3.11/library/csv.html#csv.QUOTE_ALL

### export values
You can use the following values in your export:

- question, answer: These values produce the same content that Anki's
  built-in "Cards in Plain Text ('\*.txt)" uses. Mostly what you would see
  during reviews.  - field_a, field_b, field_X, .... (Or, at least this is
  what the documentation in the original add-on states. This hasn't been
  checked for the modified add-on. Instead of the whole question and answer
  you can also export fields from the underyling notes.  You can add as many
  "field_" values as you like. In each "field_" value you must list for each
  note type which field should be used. As an example see the default config
- tags: whether tags should be included.
- any property `var` created as `p["var"]` in card_properties.py. See that
  file for details and naming conventions.

