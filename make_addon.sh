rm -f anki_stats_exporter.addon
rm -rf anki_stats_exporter/*
cp -p *.py *.md LICENSE* *.json anki_stats_exporter
cd anki_stats_exporter && zip -r ../anki_stats_exporter.ankiaddon *
