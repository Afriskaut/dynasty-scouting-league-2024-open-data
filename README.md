# Afriskaut Dynasty Scouting League 2024 – Open Data

This repository contains open event data from the **Dynasty Scouting League 2024**. The dataset is released for analysts, developers, researchers, and football enthusiasts interested in football data analysis, scouting models, and event-based match analysis.

The data includes detailed match events, player information, and match metadata, collected using the Afriskaut proprietary event tracking system.

---

## Repository Structure

```
├── Datasets.zip                                  ← All match data (unzip to use)
│   └── Datasets/
│       └── <MatchID>/
│           ├── events.jsonl                      ← Match events (one JSON object per line)
│           └── match.json                        ← Match metadata and lineups
│
├── getting_started.ipynb                         ← Starter notebook (begin here)
├── Afriskaut Event Map - 2024.pdf                ← Event type definitions
├── Pitch Coordinates For Afriskaut Event Data.pdf ← Visual pitch coordinate reference
├── summary.csv                                   ← Event count summary across all matches
├── Afriskaut.png
└── README.md
```

---

## Getting Started

### 1. Download and unzip the dataset

The match data is distributed as a single zip file due to size. Download it from the GitHub interface or via the command line:

```bash
# Download the zip
wget https://github.com/Afriskaut/dynasty-scouting-league-2024-open-data/raw/main/Datasets.zip

# Unzip
unzip Datasets.zip
```

This will produce a `Datasets/` folder with one subfolder per match, identified by `MatchID`.

### 2. Open the starter notebook

Open `getting_started.ipynb` to see a working example that loads a match, filters for a specific event type, and visualises events on the pitch. It requires only `pandas` and `matplotlib`.

---

## Data Format

### events.jsonl

Each line in this file is a self-contained JSON object representing a single event. JSONL (JSON Lines) format means you can stream or process events line by line without loading the full file into memory.

```python
import json

with open("Datasets/<MatchID>/events.jsonl") as f:
    events = [json.loads(line) for line in f]
```

### match.json

A single JSON object containing match metadata:

- Home and away team names
- Match score
- Lineups and player names
- Starting directions
- Match information

```python
import json

with open("Datasets/<MatchID>/match.json") as f:
    match = json.load(f)
```

---

## Pitch Coordinate System

All event locations use a custom pitch coordinate system.

**Pitch dimensions:**
- Length (X axis): **497**
- Width (Y axis): **328**

```
(0,0) ---------------------- (497,0)
  |                            |
  |          PITCH             |
  |                            |
(0,328) -------------------- (497,328)
```

- `(0,0)` is the **top-left corner**
- `(497,328)` is the **bottom-right corner**

A full visual reference is provided in `Pitch Coordinates For Afriskaut Event Data.pdf`.

---

## Event Definitions

All event types, tags, and their meanings are defined in `Afriskaut Event Map - 2024.pdf`.

The event map covers:
- Event names and descriptions
- Tagging rules
- How events are represented in the data
- Additional attributes attached to each event type

Consult the Event Map when interpreting event data.

---

## Event Summary File

`summary.csv` contains a summary of event counts per match. Use it for:
- Quick exploratory analysis
- Dataset overview and validation
- Statistical summaries

---

## Example Use Cases

- Football event data analysis
- Player scouting and profiling models
- Passing networks and press maps
- Tactical and positional analysis
- Data visualisation projects

---

## Notes

- All coordinates follow the **497 × 328** pitch system described above
- Event types and tags must be interpreted using `Afriskaut Event Map - 2024.pdf`
- Each match is stored independently under its `MatchID`
- Event data uses **JSONL format** (one event per line); match metadata uses standard **JSON**

---

## License

This dataset is released under the [Apache 2.0 License](LICENSE).

Please credit **Afriskaut** when using this dataset in research, publications, or public projects.

---

## Contact

For questions, collaborations, or issues:

**[tayo@afriskaut.com](mailto:tayo@afriskaut.com)**  
**[www.afriskaut.com](https://www.afriskaut.com)**
