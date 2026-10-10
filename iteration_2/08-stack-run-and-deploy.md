# 08. Tech stack, running it, and hosting it

**Draft v1, Oct 10 2026 (iteration 2).** Applies to branch `feat/traffic-ai` (commit `3a789e8`).

## The real stack (replaces the "tentative stack" in iteration 1)

| Layer | What's used | Notes |
|---|---|---|
| Traffic simulation | **SUMO 1.28** via `eclipse-sumo` (pip), controlled with **TraCI** | Runs headless; no SUMO GUI needed |
| AI | **PyTorch 2.x (CPU)**, PPO written in the repo | Small 2×64 network; ~35 min training on a CPU |
| Backend / API | Python standard library `ThreadingHTTPServer` (`src/telemetry.py`) | Serves the viewer and JSON at `http://127.0.0.1:8000` |
| Frontend | One HTML file, `viewer/index.html` (canvas, vanilla JS) | Loads IBM Plex fonts from Google Fonts; falls back to system fonts offline |
| Config | JSON in `configs/` | Safety timings, scenarios, training, alerts |
| Language | Python 3.12 | Tested on Windows |
| **Not used** | Supabase, LLM API, database | Iteration 1 assumed these; they're not in the build |

## Run it on your laptop (Windows)

**1. Get the code into its own folder.** Don't switch branches in `DSC Hackathon`; that folder holds the planning docs.

```powershell
cd C:\Users\awsza\Desktop
git clone -b feat/traffic-ai https://github.com/Omar8921/dsc-hackathon.git faris-traffic-ai
```

**2. Open `C:\Users\awsza\Desktop\faris-traffic-ai` in VS Code** (File → Open Folder), then open a terminal there (Ctrl + `).

**3. One-time setup** (5–10 min; PyTorch is a few hundred MB):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install eclipse-sumo traci sumolib numpy
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**4. Run the demo** (rush hour, AI in control):

```powershell
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\ew_heavy.sumocfg --controller ppo
```

**5. Open http://127.0.0.1:8000** in a browser. You can switch scenario, controller (timer / sensors / AI) and speed on the page. Stop with Ctrl + C in the terminal.

Other useful runs:

```powershell
.\.venv\Scripts\python.exe scripts\run_simulation.py --scenario simulation\scenarios\demo_incident.sumocfg --controller ppo
```
```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py --checkpoint models\ppo_main\checkpoint_0120.pt
```

The first opens the incident demo, where the alert fires at B0. The second re-runs the full held-out comparison (it takes a while).

### If the page stays on "connecting"
- **Look for a "Windows Security Alert" pop-up** for `sumo.exe` or `python.exe`. It can hide behind other windows. Click **Allow** (private networks). Until you do, Python can't talk to SUMO and the run hangs. This is what blocked our test on Oct 10.
- Check that nothing else uses port 8000, or add `--port 8001`.
- Run commands from the project root (the folder that has `scripts\` and `configs\`).

## Demo script for the live run (2–3 min)
1. Scenario **Main-road rush hour**, controller **Fixed-time timer**, speed 10×. Point at the long east–west queues.
2. Switch the controller to **AI controller (PPO)** and let it run. Read the "average time a car spent stopped" number.
3. Say the measured result from the slides (10% less waiting, 23% less time lost, unseen traffic), not the live number. One live run is a single seed.
4. Switch the scenario to **Incident at B0**. Wait for the congestion alert at B0 (~80 s of simulated time after the blockage at ~4:40) and its resolution.
5. Optional: open "Show technical details" to show the phase the AI chose, what the lights show, and any timing rule that delayed a change.

Record this once as a backup video.

## Hosting / deployment options

The viewer needs a **running Python + SUMO process behind it**, so it **can't be hosted as a static site** (GitHub Pages, Netlify, Vercel won't work). Also, the server runs **one simulation shared by everyone**: if one viewer switches the scenario, every viewer sees the switch.

| Option | Effort | Good for | How |
|---|---|---|---|
| **A. Your laptop** (recommended for the pitch) | None | Live demo in the hall | Steps above. Works offline (fonts fall back) |
| **B. Same Wi-Fi** | 1 min | Judges/teammates on their phones in the room | Add `--host 0.0.0.0`, find your IP with `ipconfig`, open `http://<your-IP>:8000`. Allow the firewall prompt for `python.exe` |
| **C. Public link from your laptop** | 5 min | Sharing a link while your laptop runs | `winget install --id Cloudflare.cloudflared`, then `cloudflared tunnel --url http://127.0.0.1:8000`. It prints an `https://….trycloudflare.com` link. Anyone with it can switch runs |
| **D. Always-on cloud VM** | 30–60 min | A link that works after the hackathon | Ubuntu VM (2 vCPU / 4 GB), Python 3.12 venv, the same pip installs, run with `--host 0.0.0.0 --port 8000` under `tmux`/`systemd`, open the port. **Not yet tested on Linux by us** |
| **E. Container platform** (Render, Railway, Fly.io, Hugging Face Spaces) | 1 h+ | Same as D, without managing a VM | Dockerfile below. Free tiers sleep and have little RAM; PyTorch makes the image large. **Untested** |

Dockerfile sketch for E (untested; check that SUMO starts inside the container first):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir eclipse-sumo traci sumolib numpy \
 && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
ENV PORT=8000
CMD python scripts/run_simulation.py --host 0.0.0.0 --port ${PORT} --scenario simulation/scenarios/ew_heavy.sumocfg --controller ppo
```

**Recommendation:** run **A** for the pitch, keep a **recorded video** as backup, and use **C** only if a judge wants a link during the event. Do D/E after the hackathon if the project continues.
