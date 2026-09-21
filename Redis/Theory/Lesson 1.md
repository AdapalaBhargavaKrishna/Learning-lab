# 🔴 Lesson 1 — What is Redis?

## The Core Idea
Redis = **Re**mote **Di**ctionary **S**erver.  
Stores data **in RAM** (not disk) → microsecond response times.

Think of it like your app's **short-term memory** vs a database being **long-term memory**.

---

## Where Redis Fits in System Design
```
Client → Your Server → Redis (cache) → Database
                    ↑
              If data is here, skip DB entirely
```

---

## Use Cases

| Use Case | Example in Elevate AI |
|---|---|
| **Caching** | Cache generated curriculum so AI isn't called twice |
| **Sessions** | Store user login sessions |
| **Rate Limiting** | Limit AI calls per user per minute |
| **Queues** | Background job for generating content |
| **Pub/Sub** | Real-time notifications |

---

## Key Traits
- **In-memory** → blazing fast, but RAM is limited
- **Key-Value** → everything has a key to look it up
- **TTL support** → data can auto-expire
- **Single-threaded** → no race conditions on reads/writes

---

## Mental Model
```
Redis is like a whiteboard in your office.
DB is like filing cabinets in the basement.

You write frequent stuff on the whiteboard (Redis).
Permanent stuff goes in the cabinet (DB).
```