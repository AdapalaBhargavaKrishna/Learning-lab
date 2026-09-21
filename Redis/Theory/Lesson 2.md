# 🔴 Lesson 2 — Installation & Redis CLI Basics

## Installation (Windows)
Installed via `.msi` from: https://github.com/tporadowski/redis/releases

Redis runs as a **Windows service** by default.  
Check status:
```bash
sc query Redis
```

---

## Connect to Redis CLI
```bash
redis-cli
```
If not recognized, navigate to install directory (usually `C:\Program Files\Redis`) and run `redis-cli.exe`.

---

## First Command
```bash
PING          # → PONG ✅ (Redis is alive)
```

---

## Basic Commands

```bash
SET name "Bhargava"     # store a key
GET name                # retrieve it
DEL name                # delete it
GET name                # → (nil) — key is gone
```

```bash
EXISTS name             # → 0 (false) or 1 (true)
```

```bash
KEYS *                  # list ALL keys — ⚠️ don't use in production (slow on big DBs)
```

```bash
FLUSHALL                # ⚠️ clears EVERYTHING — be careful!
```

---

## Practice Task
1. Open `redis-cli`, confirm `PING` → `PONG`
2. SET 3 different keys
3. GET them all
4. DEL one
5. Confirm with EXISTS