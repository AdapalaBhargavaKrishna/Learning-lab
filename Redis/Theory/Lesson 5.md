# 🔴 Lesson 5 — Hashes (Storing Objects/Records)

## What is a Hash?
A mini object stored under ONE key — multiple fields per key.
Perfect for users, sessions, curriculum records.

---

## Why Not Plain Strings?

❌ Without hashes (messy):
```bash
SET user:7:name "Bhargava"
SET user:7:email "bhargava@email.com"
SET user:7:cgpa "8.24"
# 3 separate keys for ONE user
```

✅ With hashes (clean):
```bash
HSET user:7 name "Bhargava" email "bhargava@email.com" cgpa "8.24"
```

---

## Core Commands

```bash
HSET user:7 name "Bhargava" email "bhargava@email.com" cgpa "8.24"

HGET user:7 name           # → "Bhargava"
HGETALL user:7             # → all fields & values

HSET user:7 cgpa "8.5"     # update a single field
HDEL user:7 cgpa            # delete one field
HEXISTS user:7 name         # → 1 or 0

HINCRBY user:7 ai_requests 1    # atomic increment on a hash field

HKEYS user:7               # just field names
HVALS user:7               # just values
HLEN user:7                # number of fields
```

---

## Elevate AI Use Cases

### Session storage (one key = entire session object)
```bash
HSET session:abc123 userId "7" plan "premium" lastActive "1718900000"
HINCRBY session:abc123 ai_requests_today 1
HGETALL session:abc123
```

### ATS score cache
```bash
HSET ats:resume42:jd17 score "780" status "computed" timestamp "1718900000"
```

---

## Hash vs JSON String — when to use which?

| Hash | String (JSON) |
|---|---|
| Update single fields cheaply (`HSET`) | Must read entire JSON, modify, rewrite |
| Atomic field-level increments (`HINCRBY`) | No atomic partial updates |
| Flat objects (user, session) ✅ | Nested/complex objects (AI response with arrays) ✅ |

**Rule of thumb:** flat objects → Hash. Nested/complex → JSON string.

---

## Practice Task

```bash
HSET project:elevateai name "ElevateAI" stack "Next.js,FastAPI,Postgres" commits "90"
HGETALL project:elevateai
HINCRBY project:elevateai commits 1
HGET project:elevateai commits
HDEL project:elevateai stack
HGETALL project:elevateai
```