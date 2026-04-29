# Researcher and Participant Study Prototype

A local web prototype for running researcher-led social media study sessions. The project connects a researcher authoring interface, invite-code publishing, participant onboarding, camera calibration, and a participant feed styled after common social platforms.

The prototype is designed for local demos, usability testing, and research workflow development. It is not a production authentication, storage, or eye-tracking system.

## Features

- Researcher sign-up and login flow
- Researcher post editor with A/B version controls
- News link metadata fetching for title and image previews
- Platform-style previews for Instagram, Facebook, X, and TikTok
- Invite-code based participant access
- Participant camera calibration flow
- MediaPipe-based face landmark processing through a local Socket.IO backend
- Participant feed rendering based on the platform selected by the researcher
- PostgreSQL-backed storage for researcher accounts, sessions, surveys, survey versions, publish logs, participant sessions, calibration results, gaze records, and raw payload archives
- Automatic database and table bootstrap during launcher startup
- Dual-save participant runtime flow: local JSON backup plus PostgreSQL persistence

## Current Database Status

The project now includes a dedicated `project_database/` package.

At startup, the launcher:

1. Creates or reuses the local virtual environment
2. Installs dependencies
3. Ensures the PostgreSQL database `capstone5703` exists
4. Creates all SQLAlchemy tables
5. Starts the bridge and internal services

The bridge and backend now read and write these flows through PostgreSQL:

- researcher registration
- researcher login
- researcher sessions
- survey creation during publish
- survey version persistence during publish
- invite-code lookup for published participant content
- participant creation
- study session creation and updates
- participant interaction logs
- calibration result summaries
- calibration point samples
- gaze samples during study
- raw payload archive snapshots

Participant-facing eye-tracking data is now saved in two places:

- PostgreSQL, through `project_database/db_bridge.py`
- local JSON files under `CS14_Temp117-Backend/data/` for debugging and recovery

## Project Structure

```text
.
|-- run_prototype.py
|-- requirements.txt
|-- README.md
|-- bridge/
|   |-- __init__.py
|   `-- bridge.py
|-- project_database/
|   |-- __init__.py
|   |-- db.py
|   |-- db_bridge.py
|   |-- create_tables.py
|   `-- database_structure/
|       |-- __init__.py
|       |-- auth_models.py
|       |-- survey_models.py
|       |-- participant_models.py
|       `-- gaze_models.py
|-- researcher login/
|   |-- researcher-login.html
|   |-- researcher-register.html
|   |-- researcher-login.js
|   |-- researcher-register.js
|   `-- researcher-login.css
|-- researcher main/
|   |-- index.html
|   |-- app.js
|   |-- style.css
|   |-- server.py
|   `-- requirements.txt
`-- CS14_Temp117-Backend/
    |-- app.py
    |-- participant.html
    |-- data/
    `-- face_landmarker.task
```

### Main Components

- `run_prototype.py` creates the local virtual environment, installs dependencies, prepares the database, and starts the bridge.
- `bridge/bridge.py` serves the researcher and participant entry points, handles local sessions, publishes posts, and validates invite codes.
- `project_database/db.py` manages PostgreSQL connectivity and automatic database creation.
- `project_database/create_tables.py` ensures the target database exists and creates all SQLAlchemy tables.
- `project_database/db_bridge.py` acts as the database service layer used by the bridge and eye-tracking backend.
- `researcher main/server.py` provides the news metadata scraping API.
- `CS14_Temp117-Backend/app.py` runs the camera, MediaPipe, and Socket.IO backend, and now writes participant payloads to both JSON files and PostgreSQL.
- `CS14_Temp117-Backend/participant.html` contains the participant onboarding, calibration, feed, data export, and invite-code-aware payload sending logic.

## Requirements

- Python 3.11 is recommended.
- Python 3.12 is also supported by the launcher.
- macOS, Linux, and Windows 10/11 are supported as long as Python and the required packages install successfully.
- PostgreSQL must be installed locally and running.
- The PostgreSQL user configured in `project_database/db.py` must be able to connect to the server.
- To allow automatic creation of `capstone5703`, that PostgreSQL user should also have permission to create databases.
- A webcam is required for the participant calibration flow.
- Browser camera permission must be granted for `127.0.0.1`.
- Internet access is required during first setup to install Python packages.
- Internet access is also useful for CDN assets and news metadata fetching.

MediaPipe can be sensitive to Python version support. If dependency installation fails, try Python 3.11 first.

On Windows, the commands below use the Python Launcher (`py`), which is included when Python is installed from python.org. If `py` is not available, use `python` after confirming it points to Python 3.11 or 3.12.

Check your Python version:

macOS / Linux:

```bash
python3.11 --version
```

Windows PowerShell:

```powershell
py -3.11 --version
```

## Database Configuration

Open `project_database/db.py` and update the PostgreSQL connection settings before first launch:

```python
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "capstone5703"
```

If the configured PostgreSQL user has permission to create databases, the launcher will create `capstone5703` automatically when it does not already exist.

## Quick Start

After downloading or cloning the repository, open a terminal in the repository root. This is the folder that contains `run_prototype.py`.

macOS / Linux:

```bash
python3.11 run_prototype.py
```

Windows PowerShell:

```powershell
py -3.11 run_prototype.py
```

If your default Python command already points to Python 3.11 or 3.12, these also work:

```bash
python3 run_prototype.py
```

```powershell
python run_prototype.py
```

The launcher will:

1. Create a local `.venv`
2. Install `requirements.txt`
3. Ensure the PostgreSQL database `capstone5703` exists
4. Create all SQLAlchemy tables
5. Start the bridge
6. Start the researcher scraping backend
7. Start the camera backend
8. Print the researcher and participant URLs

Open the two public-facing local URLs:

- Researcher: `http://127.0.0.1:8120/`
- Participant: `http://127.0.0.1:8121/`

Internal services are started automatically:

- Scraper API: `127.0.0.1:5001`
- Camera backend: `127.0.0.1:5050`

Stop the prototype with `Ctrl+C` in the terminal.

## Demo Flow

### Researcher

1. Open `http://127.0.0.1:8120/`.
2. Create a researcher account from the sign-up page.
3. Log in with the same email and password.
4. Choose `Version A` or `Version B`.
5. Optionally paste a public news URL and click `Fetch Image`.
6. Choose a platform style: Instagram, Facebook, X, or TikTok.
7. Edit the caption, likes, comments, and shares.
8. Click `Generate Invite Code`.
9. Click `Publish Survey Link`.
10. Copy the generated invite code or participant link.

### Participant

1. Open `http://127.0.0.1:8121/`.
2. Enter the invite code, or open the generated participant link.
3. Allow browser camera access.
4. Complete the calibration flow.
5. Start the study and browse the rendered post feed.
6. Use the platform rail to switch between published platform styles for the invite code.
7. Interact with posts or export the collected JSON data.

## Useful Commands

Run with custom ports:

macOS / Linux:

```bash
python3 run_prototype.py --researcher-port 8122 --participant-port 8123 --camera-port 5051
```

Windows PowerShell:

```powershell
py -3.11 run_prototype.py --researcher-port 8122 --participant-port 8123 --camera-port 5051
```

Run the bridge without auto-starting internal backends:

macOS / Linux:

```bash
python3 -m bridge.bridge --no-backends
```

Windows PowerShell:

```powershell
py -3.11 -m bridge.bridge --no-backends
```

Create database and tables manually without starting the full prototype:

macOS / Linux:

```bash
python3 -m project_database.create_tables
```

Windows PowerShell:

```powershell
py -3.11 -m project_database.create_tables
```

Check Python syntax:

macOS / Linux:

```bash
python3 -m py_compile run_prototype.py bridge/bridge.py project_database/db.py project_database/create_tables.py "researcher main/server.py" CS14_Temp117-Backend/app.py
```

Windows PowerShell:

```powershell
py -3.11 -m py_compile run_prototype.py bridge/bridge.py project_database/db.py project_database/create_tables.py "researcher main/server.py" CS14_Temp117-Backend/app.py
```

## Database Tables

The current schema is split into four modules:

### Authentication
- `researchers`
- `researcher_sessions`

### Survey / researcher main
- `surveys`
- `survey_versions`
- `survey_publish_logs`

### Participant
- `participants`
- `study_sessions`
- `participant_interaction_logs`

### Gaze / calibration
- `calibration_results`
- `calibration_samples`
- `gaze_records`
- `gaze_payload_archives`

Use pgAdmin4 or the PostgreSQL command line tools to inspect the `capstone5703` database during testing.

## Runtime Data

Current runtime data behavior is split across PostgreSQL and local files:

### Stored in PostgreSQL
- researcher accounts
- researcher sessions
- survey records
- survey version records
- survey publish logs
- invite-code lookup data
- participant records
- study sessions
- participant interaction logs
- calibration result summaries
- calibration samples
- gaze records
- raw payload archives

### Still useful as local runtime files
- `CS14_Temp117-Backend/data/` contains participant calibration, gaze, and interaction payload snapshots written by the eye-tracking backend
- `CS14_Temp117-Backend/.runtime_cache/` stores runtime cache files
- `.venv/` stores the local Python virtual environment

If you want to inspect database data after a run, connect to PostgreSQL and open:

- database: `capstone5703`
- schema: `public`

## Testing the Database Integration

A practical end-to-end validation flow is:

1. Run `python run_prototype.py`
2. Confirm `capstone5703` exists in pgAdmin4
3. Confirm all tables exist in `public`
4. Register and log in as a researcher
5. Publish a survey/post with an invite code
6. Open the participant page and enter that invite code
7. Complete calibration
8. Stay in the study for 20 to 30 seconds and interact with at least one post
9. Close or leave the page to trigger a final save
10. Inspect PostgreSQL tables and the local `CS14_Temp117-Backend/data/` JSON snapshots

Recommended pgAdmin4 checks:

```sql
SELECT * FROM researchers ORDER BY created_at DESC;
SELECT * FROM researcher_sessions ORDER BY issued_at DESC;
SELECT * FROM surveys ORDER BY created_at DESC;
SELECT * FROM survey_versions ORDER BY created_at DESC;
SELECT * FROM survey_publish_logs ORDER BY published_at DESC;
SELECT * FROM participants ORDER BY created_at DESC;
SELECT * FROM study_sessions ORDER BY created_at DESC;
SELECT * FROM participant_interaction_logs ORDER BY event_timestamp DESC;
SELECT * FROM calibration_results ORDER BY completed_at DESC;
SELECT * FROM calibration_samples ORDER BY sample_timestamp DESC;
SELECT * FROM gaze_records ORDER BY recorded_at DESC;
SELECT * FROM gaze_payload_archives ORDER BY saved_at DESC;
```

## Security Notes

This project is a local research prototype.

- Do not use the included login flow for production authentication.
- Password handling is still prototype-grade and should not be treated as production secure.
- Do not commit participant data, private researcher accounts, or generated runtime files to a public repository.
- The news scraping service rejects local and private network URLs as a basic SSRF protection measure.
- Automatic database creation depends on the PostgreSQL account permissions configured locally.

## Troubleshooting

### Database creation fails

Check the PostgreSQL settings in `project_database/db.py`.

Common causes:
- wrong PostgreSQL password
- PostgreSQL service is not running
- the configured user cannot create databases
- `psycopg2-binary` was not installed successfully

You can also test database bootstrap directly:

```bash
python -m project_database.create_tables
```

### Tables exist but eye-tracking rows are missing

Check all three layers:

- `participant.html` must send `inviteCode` inside `studyData`
- `CS14_Temp117-Backend/app.py` must save both JSON and database rows inside `handle_save_data()`
- `project_database/db_bridge.py` must be importable from the backend process

Also inspect:

- terminal logs for `[SAVED]` or `[ERROR] save: ...`
- local JSON snapshots under `CS14_Temp117-Backend/data/`
- PostgreSQL tables `calibration_results`, `calibration_samples`, `gaze_records`, and `gaze_payload_archives`

### Dependency installation fails

Use Python 3.11.

macOS / Linux:

```bash
python3.11 run_prototype.py
```

Windows PowerShell:

```powershell
py -3.11 run_prototype.py
```

If you are using a newer Python release, MediaPipe or OpenCV wheels may not be available for your platform.

### A port is already in use

Find the process using the port:

macOS / Linux:

```bash
lsof -nP -iTCP:8120 -sTCP:LISTEN
```

Windows PowerShell:

```powershell
netstat -ano | findstr :8120
```

Stop the process:

macOS / Linux:

```bash
kill <PID>
```

Windows PowerShell:

```powershell
taskkill /PID <PID> /F
```

Or run the prototype on different ports:

macOS / Linux:

```bash
python3 run_prototype.py --researcher-port 8122 --participant-port 8123
```

Windows PowerShell:

```powershell
py -3.11 run_prototype.py --researcher-port 8122 --participant-port 8123
```

### The camera does not work

- Allow camera access in the browser.
- Close other apps that may be using the webcam.
- Confirm the camera backend is running on the expected port.
- Try refreshing the participant page after granting permission.

### News metadata fetching fails

- Confirm the researcher scraper backend started successfully.
- Use a public `http` or `https` URL.
- Some websites block scraping or omit Open Graph / Twitter metadata.
- Localhost and private network URLs are intentionally rejected.

### The invite code is not accepted

- Make sure the researcher clicked `Publish Survey Link`, not only `Generate Invite Code`.
- Check that the participant entered the same invite code shown after publishing.
- Confirm the survey publish record exists in PostgreSQL.

## Limitations

- Authentication is still a local demo flow.
- The current bridge integration is database-backed mainly for researcher accounts, sessions, survey publish flow, invite lookup, and participant runtime persistence.
- Participant runtime currently uses a dual-save approach: PostgreSQL plus local JSON payload snapshots.
- News scraping depends on each website's metadata and access rules.
- Gaze and face-landmark data quality depends on camera quality, lighting, participant position, and MediaPipe detection.
- The prototype is intended for local research workflow validation, not production deployment.
