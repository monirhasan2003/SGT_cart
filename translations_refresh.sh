#!/usr/bin/env bash
# Refresh Babel translation catalogs.
#
# Run this whenever new `{{ _("...") }}` strings are added to templates
# or `gettext()` calls to Python. It:
#   1. Extracts every translatable string into messages.pot
#   2. Updates each per-locale messages.po with the new entries
#      (existing translations are preserved)
#   3. Compiles all .po -> .mo so the running app sees the changes
#
# Workflow: edit templates -> bash translations_refresh.sh ->
#   open app/translations/bn/LC_MESSAGES/messages.po -> fill in `msgstr`
#   -> bash translations_refresh.sh again -> restart sgtcart.
set -e
cd "$(dirname "$0")"

if [ -d venv/Scripts ]; then
    PYBABEL=venv/Scripts/pybabel
else
    PYBABEL=venv/bin/pybabel
fi

echo "[1/3] Extracting strings -> messages.pot..."
"$PYBABEL" extract -F babel.cfg -o messages.pot .

echo "[2/3] Updating per-locale .po files..."
"$PYBABEL" update -i messages.pot -d app/translations

echo "[3/3] Compiling .po -> .mo..."
# `pybabel update` marks lookalike entries `fuzzy`, which `compile` then
# silently skips. Strip those flags so every confirmed translation gets
# into the .mo file. Re-add manually after running `update` if you want
# to review fuzzy matches before publishing.
for po in app/translations/*/LC_MESSAGES/messages.po; do
    sed -i 's/^#, fuzzy$//; s/^#, fuzzy, /#, /' "$po"
done
"$PYBABEL" compile -d app/translations

echo "Done. Open app/translations/bn/LC_MESSAGES/messages.po and fill in msgstr entries."
