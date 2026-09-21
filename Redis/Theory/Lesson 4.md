# 🔴 Lesson 4 — Lists (Queues & Stacks)

## What is a Redis List?
Ordered collection of strings. Optimized for adding/removing from the **ends**.

---

## Core Commands

```bash
RPUSH tasks "task1"     # push to right (end)
RPUSH tasks "task2"
RPUSH tasks "task3"
LRANGE tasks 0 -1       # get ALL items (0 = start, -1 = end)
```

```bash
LPUSH tasks "urgent"    # push to left (front)
```

```bash
LPOP tasks              # remove & return from front
RPOP tasks              # remove & return from end
LLEN tasks              # count of items
```

---

## Pattern 1: Queue (FIFO — first in, first out)

```bash
RPUSH queue "job1"
RPUSH queue "job2"
LPOP queue              # → "job1" (oldest first)
```

**Elevate AI use case:** Background job queue — push "generate curriculum for user X", a worker pops and processes.

---

## Pattern 2: Stack (LIFO — last in, first out)

```bash
RPUSH stack "step1"
RPUSH stack "step2"
RPOP stack              # → "step2" (most recent first)
```

**Use case:** Undo history, recent activity feed.

---

## Capped Lists (keep only N recent items)

```bash
LPUSH recent_logs "User logged in"
LTRIM recent_logs 0 9   # keep only latest 10
```

**Elevate AI use case:** "Last 10 AI interactions" per user — push new, trim old automatically.

---

## Practice Task

```bash
RPUSH user:7:activity "Started DSA module"
RPUSH user:7:activity "Completed Subsets problem"
RPUSH user:7:activity "Started Redis lesson"
LRANGE user:7:activity 0 -1
LTRIM user:7:activity 0 1
LRANGE user:7:activity 0 -1
```