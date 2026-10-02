## What it does

This notebook builds a minimal knowledge graph in Cognite Data Fusion on the Core Data Model. A coffee roastery is the example: equipment, sensors, work orders, and a P&ID, linked so you can walk from an asset to its readings, its maintenance history, and the drawing.

Each step is a Python SDK write in the same shape an extractor or transformation would use in production, with a short check in Fusion when the step is done.

## Prerequisites

- Python 3.14 or newer, and [uv](https://docs.astral.sh/uv/)
- Read and write access to a CDF project

## How to use

1. Clone this repo and open it.
2. Install dependencies, including the notebook kernel:

   ```bash
   uv sync
   ```

3. Copy an existing working `.env` file into the repo root, or create one from `.env.example` and fill in your project values. See [Configuration](#configuration).
4. Using your desktop coding IDE (VS Code, Cursor, etc.), open `minimal_knowledge_graph/minimal_knowledge_graph.ipynb` and select the `.venv` kernel.
5. Run the cells in order from **Setup** through **Step 7**. After each step, follow that step's **Verify in Fusion** notes.
6. `run_cleanup` defaults to `False`, so **Run All** leaves the graph in place for you to explore in Fusion. When you want the demo removed, set `run_cleanup = True` in the **Cleanup** cell and run it.

To write into a different space, change `SPACE` in `helpers/constants.py` before Setup.

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```
