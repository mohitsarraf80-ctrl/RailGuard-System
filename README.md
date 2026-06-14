# 🚆 RailGuard Agent

An autonomous railway monitoring system powered by the **Anthropic Claude API**.  
RailGuard watches your rail network in real time, detects faults and disruptions, and dispatches structured alerts — all driven by an AI agent using tool use.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RailGuard System                      │
│                                                          │
│  ┌──────────────┐    ┌──────────────────────────────┐   │
│  │  FastAPI     │    │      Agent Orchestrator       │   │
│  │  REST API    │◄───│  (Claude claude-sonnet-4-6 + tools)  │   │
│  │              │    └──────────────┬───────────────┘   │
│  │  /api/alerts │                   │                    │
│  │  /api/trains │         ┌─────────▼──────────┐        │
│  │  /api/tracks │         │    Tool Registry    │        │
│  └──────┬───────┘         │                    │        │
│         │                 │ • check_track_cond │        │
│         │                 │ • get_train_status │        │
│         └─────────────────│ • dispatch_alert   │        │
│                           └────────────────────┘        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │            Background Scheduler                    │  │
│  │   Runs a sweep every SWEEP_INTERVAL_SECONDS       │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Component overview

| Path | Purpose |
|------|---------|
| `api/models/` | Pydantic models: `Alert`, `TrainPosition`, `TrackSegment` |
| `api/routes/alerts.py` | Alert CRUD + `push_alert_from_agent` internal hook |
| `api/routes/trains.py` | Train position store + query filters |
| `api/routes/tracks.py` | Track segment store + condition filters |
| `api/main.py` | FastAPI app with CORS, lifespan seeding, router mounting |
| `agent/orchestrator.py` | Agentic loop: drives Claude through tool-use iterations |
| `agent/tools/` | Three tools: track checker, train monitor, alert dispatcher |
| `agent/prompts/system.py` | System prompt defining agent behaviour and output format |
| `agent/scheduler.py` | Async background task running sweeps on a configurable interval |
| `run_sweep.py` | CLI script for manual sweeps during development |

---

## Quickstart

### 1. Clone & install

```bash
git clone https://github.com/your-org/railguard-agent.git
cd railguard-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### 3. Run the API

```bash
uvicorn api.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### 4. Run a manual sweep

```bash
python run_sweep.py
```

### 5. Run tests

```bash
pytest tests/ -v
```

---

## API Reference

### Alerts

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/alerts?limit=20` | List recent alerts (newest first) |
| `POST` | `/api/alerts` | Create an alert manually |

**Alert body:**
```json
{
  "track_id": "T-07",
  "message": "Signal fault at km 14.2",
  "severity": "HIGH",
  "affected_trains": ["TRN-002"]
}
```

### Trains

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/trains` | List all trains (filter by `?line=Red&status=STOPPED`) |
| `GET` | `/api/trains/{id}` | Get a single train |
| `PUT` | `/api/trains/{id}` | Upsert a train position |
| `DELETE` | `/api/trains/{id}` | Remove a train |

### Tracks

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/tracks` | List all segments (filter by `?condition=FAULT`) |
| `GET` | `/api/tracks/{id}` | Get a single segment |
| `PUT` | `/api/tracks/{id}` | Upsert a segment |

---

## Agent Tools

The agent has three tools available during each sweep:

### `check_track_conditions`
Scans all track segments, returns non-CLEAR ones grouped by severity indicators.

### `get_train_status`
Returns all trains, with `STOPPED`, `DELAYED`, and `OUT_OF_SERVICE` trains flagged separately.

### `dispatch_alert`
Creates an alert via `push_alert_from_agent`. Required fields: `track_id`, `message`, `severity`.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | **Required.** Your Anthropic API key |
| `SWEEP_INTERVAL_SECONDS` | `60` | Background scheduler interval |

---

## Extending RailGuard

### Add a new tool

1. Create `agent/tools/my_tool.py` with a function and a `TOOL_DEFINITION` dict.
2. Register it in `agent/tools/__init__.py` — add to `ALL_TOOL_DEFINITIONS` and `TOOL_REGISTRY`.
3. Update the system prompt in `agent/prompts/system.py` if needed.

### Swap in a database

The in-memory stores in `api/routes/*.py` are designed for easy replacement.  
Each module has a `_store` dict and internal getter functions (`get_all_trains`, etc.) — replace those with SQLAlchemy or asyncpg queries without touching the agent or the REST layer.

---

## CI

GitHub Actions runs on every push to `main` / `develop`:
- Tests on Python 3.11 and 3.12
- `ruff` linting

Add `ANTHROPIC_API_KEY` to your repository secrets for integration tests.

---

## License

MIT
