# 🔴 Lesson 6 — Sets & Sorted Sets

---

## Part 1: Sets — unordered, unique values

No duplicates. No order. Super fast membership checks.

### Core Commands

```bash
SADD skills:user7 "React" "Node.js" "Redis"
SADD skills:user7 "React"           # ignored — already exists

SMEMBERS skills:user7               # all members
SISMEMBER skills:user7 "React"      # → 1 (yes) or 0 (no)
SCARD skills:user7                  # count of members
SREM skills:user7 "Redis"           # remove one member
```

### Set Operations (the real power)

```bash
SADD jd:skills "React" "Node.js" "AWS"
SADD resume:user7 "React" "Node.js" "Redis"

SINTER jd:skills resume:user7       # → common skills: React, Node.js
SDIFF jd:skills resume:user7        # → skills JD wants that user lacks: AWS
SUNION jd:skills resume:user7       # → all skills combined
```

**Elevate AI use case:** Instant skill-gap analysis between JD required skills and user's resume skills — no AI call needed, pure Redis set math, microseconds fast.

---

## Part 2: Sorted Sets (ZSET) — unique values WITH a score

Each member has a **score** (number). Redis keeps it **automatically sorted** by score.

### Core Commands

```bash
ZADD leaderboard 780 "user7"
ZADD leaderboard 650 "user12"
ZADD leaderboard 910 "user3"

ZRANGE leaderboard 0 -1 WITHSCORES         # ascending
ZREVRANGE leaderboard 0 -1 WITHSCORES      # descending (highest first)
```

```bash
ZSCORE leaderboard "user7"                 # → 780
ZRANK leaderboard "user7"                  # position (ascending)
ZREVRANK leaderboard "user7"               # position (descending) — true "rank"
ZINCRBY leaderboard 10 "user7"             # increase score atomically
```

```bash
ZRANGEBYSCORE leaderboard 700 900          # everyone scoring between 700–900
```

**Elevate AI use case:** ElevateScore (0–1000) leaderboard — instant ranking, no SQL ORDER BY + LIMIT:
```bash
ZADD elevatescore_leaderboard 845 "user7"
ZREVRANK elevatescore_leaderboard "user7"   # instant rank
```

---

## Quick Comparison

| Type | Order | Duplicates | Best For |
|---|---|---|---|
| List | Insertion order | Yes | Queues, recent activity |
| Set | None | No | Skill matching, tags, uniqueness checks |
| Sorted Set | By score | No (unique member) | Leaderboards, rankings, scores |

---

## Practice Task

```bash
SADD jd:skills "Python" "FastAPI" "Redis" "Docker"
SADD resume:user7:skills "Python" "FastAPI" "Postgres"
SINTER jd:skills resume:user7:skills
SDIFF jd:skills resume:user7:skills

ZADD scores 780 "userA" 910 "userB" 650 "userC"
ZREVRANGE scores 0 -1 WITHSCORES
ZREVRANK scores "userA"
```