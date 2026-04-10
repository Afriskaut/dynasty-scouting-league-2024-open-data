# Afriskaut Dynasty Scouting League 2024 – Open Data

This repository contains open event data from the **Dynasty Scouting League 2024**. The dataset is released for analysts, developers, researchers, and football enthusiasts interested in football data analysis, scouting models, and event-based match analysis.

The data includes detailed match events, player information, and match metadata, collected using the Afriskaut proprietary event tracking system.

---

## Repository Structure

```
├── Datasets.zip                                   ← All match data (unzip to use)
│   └── Datasets/
│       └── <MatchID>/
│           ├── events.jsonl                       ← Match events (one JSON object per line)
│           └── match.json                         ← Match metadata and lineups
│
├── getting_started.ipynb                          ← Start here
├── afriskaut_utils.py                             ← Utility functions used by the notebook
├── Afriskaut Event Map - 2024.pdf                 ← Event type definitions
├── Pitch Coordinates For Afriskaut Event Data.pdf ← Visual pitch coordinate reference
├── Afriskaut.png                                  ← Logo
├── summary.csv                                    ← Event count summary across all matches
└── README.md
```

---

## Getting Started

### 1. Download and unzip the dataset

```bash
wget https://github.com/Afriskaut/dynasty-scouting-league-2024-open-data/raw/main/Datasets.zip
unzip Datasets.zip
```

This produces a `Datasets/` folder with one subfolder per match, identified by `MatchID`.

### 2. Install dependencies

```bash
pip install pandas matplotlib
```

### 3. Open the notebook

Open `getting_started.ipynb`. It uses helper functions from `afriskaut_utils.py` — make sure both files are in the same directory.

The notebook covers:
- Listing available matches
- Loading match metadata and events
- Exploring event type distributions
- Plotting any event type on a correctly oriented pitch
- Loading the full dataset across all matches

---

## Data Format

### events.jsonl

Each line is a self-contained JSON object representing one event. JSONL format means you can stream or process events line by line without loading the full file into memory.

```python
from afriskaut_utils import load_match, load_events

match  = load_match("Datasets/<MatchID>")
events = load_events("Datasets/<MatchID>")
```

### match.json

A single JSON object containing match metadata: team names, score, lineups, starting directions, substitutions, and timing information.

---

## Pitch Coordinate System

All event locations use a custom coordinate system.

**Pitch dimensions:**
- Length (X axis): **497**
- Width (Y axis): **328**

```
(0,0) ---------------------- (497,0)
  |          PITCH             |
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

---

## Event Summary File

`summary.csv` contains a summary of event counts per match, useful for quick exploratory analysis and dataset validation.

---

## Example Use Cases

- Player scouting and profiling models
- Passing networks and press maps
- Shot maps and expected goals models
- Tactical and positional analysis
- Data visualisation projects

---

## Notes

- All coordinates follow the **497 × 328** pitch system
- Event data uses **JSONL format** (one event per line); match metadata uses standard **JSON**
- Each match is stored independently under its `MatchID`
- Event types must be interpreted using `Afriskaut Event Map - 2024.pdf`

---

## License

This dataset is released under the [Apache 2.0 License](LICENSE).

Please credit **Afriskaut** when using this dataset in research, publications, or public projects.

---

## Contact

For questions, collaborations, or issues:

**[tayo@afriskaut.com](mailto:tayo@afriskaut.com)**  
**[www.afriskaut.com](https://www.afriskaut.com)**
