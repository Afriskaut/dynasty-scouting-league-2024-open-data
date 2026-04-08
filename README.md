# Afriskaut Dynasty Scouting League 2024 – Open Data

This repository contains open event data from the **Dynasty Scouting League 2024**.
The dataset is released for analysts, developers, researchers, and football enthusiasts interested in football data analysis, scouting models, and event-based match analysis.

The data is provided in **JSON format** and includes detailed match events, player information, and match metadata.

---

# Repository Structure

```
├── Datasets/
│   ├── MatchID/
│   │   ├── events.json
│   │   └── match.json
│
├── Afriskaut Event Map 2024.pdf
├── Pitch Coordinated For Afriskaut Event Data.pdf
├── summary.csv
└── README.md
```

### Datasets/

Contains all match data. Each match is stored in its own folder using the **MatchID**.

Each match folder contains:

**events.jsonl**
Contains all event data recorded during the match.

**match.json**
Contains match metadata including:

* Home team name
* Away team name
* Match score
* Lineups
* Player names
* Starting directions
* Match information

---

# Pitch Coordinate System

All event locations use a custom pitch coordinate system.

Pitch Dimensions:

* **Length (X axis): 497**
* **Width (Y axis): 328**

```
(0,0) ---------------------- (497,0)
  |                            |
  |                            |
  |                            |
(0,328) -------------------- (497,328)
```

* `(0,0)` represents the **top-left corner**
* `(497,328)` represents the **bottom-right corner**

All event coordinates in the dataset follow this system.

A visual reference of the pitch coordinates is provided in:

**Pitch Coordinated For Afriskaut Event Data.gdoc**

---

# Event Definitions

All event types, tags, and their meanings are defined in:

**Afriskaut Event Map - 2024.pdf**

The event map explains:

* Event names
* Event descriptions
* Tagging rules
* How events are represented in the dataset
* Additional attributes attached to events

Users should consult the **Event Map** when interpreting the event data.

---

# Event Summary File

The file:

**summary.csv**

Contains a summary of event counts for each match.

This file can be used for:

* Quick exploratory analysis
* Dataset overview
* Data validation
* Statistical summaries

---

# Data Format

All match data is provided in **JSON format**.

Typical workflow for users:

1. Select a match folder inside `Datasets/`
2. Load `match.json` for match metadata
3. Load `events.json` for detailed event data
4. Use the `Afriskaut Event Map - 2024.pdf` to interpret event types
5. Use pitch coordinates to map spatial data

---

# Example Use Cases

This dataset can be used for:

* Football event data analysis
* Player scouting models
* Passing networks
* Tactical analysis
* Visualization projects

---

# Notes

* All coordinates follow the **497 x 328 pitch system**
* Event meanings and tags must be interpreted using **Afriskaut Event Map - 2024.pdf**
* Each match is stored independently using **MatchID**

---

# License

This dataset is released as **open data for research and educational purposes**.

Please credit **Afriskaut** when using the dataset in research, publications, or public projects.

---

# Contact

For questions, collaborations, or issues regarding the dataset, please contact:

**tayo@Afriskaut.com**
