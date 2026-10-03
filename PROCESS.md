# Process

I used VS Code to organise the files and Python scripts, and ChatGPT/Codex to help inspect the assignment, plan the data workflow, and draft the first version of the plotting code. I checked the script against the actual USGS GeoJSON fields (`features`, `geometry.coordinates`, and `properties.mag`) and bundled 513-event data snapshot rather than assuming a generic CSV layout.

I kept the suggestion to make marker size reflect magnitude and colour reflect depth because both visual channels map directly to measured values in the source. I rejected the idea of plotting only the strongest handful of earthquakes: it would make the image simpler, but it would hide much of the selected feed without a data-based reason. I also kept the raw GeoJSON unchanged and made the plotting script read that local file, so the same picture can be regenerated offline.

Before submitting, I will add my own notes about any edits I make to the code, design, or explanation, and record the work in several plain-language Git commits across more than one day.
