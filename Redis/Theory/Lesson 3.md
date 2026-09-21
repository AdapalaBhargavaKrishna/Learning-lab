# 🔴 Lesson 3 — Strings, Numbers & Booleans

## Key Insight
Redis has ONE base type: **String**. Numbers, booleans, JSON — all strings under the hood. Redis just gives helper commands to work with them smartly.

---

## 1. Strings

```bash
SET user:1:name "Bhargava"
GET user:1:name
```

### Naming Convention — always use `:` to namespace
```
user:1:name
session:abc123
curriculum:userId:topic
```

---

## 2. Numbers (atomic counter commands)

```bash
SET views 100
INCR views          # → 101
INCR views          # → 102
DECR views          # → 101
INCRBY views 10     # → 111
DECRBY views 5      # → 106
```

**Elevate AI use case:** Track AI requests per user atomically — no race conditions
```bash
INCR user:42:ai_requests_today
```

---

## 3. Booleans (Redis has none — simulate them)

```bash
SET isVerified 1       # use 1/0
SET isVerified "true"  # or string — check truthiness in app code
```

---

## 4. Expiry on SET (preview of Lesson 7)

```bash
SET otp 4521 EX 60      # expires in 60 seconds
TTL otp                  # check seconds remaining
```

**Elevate AI use case:** OTP, temporary rate-limit flags, short-lived tokens.

---

## 5. SETNX — Set only if Not Exists

```bash
SETNX lock:job1 "processing"   # → 1 if set, 0 if key already exists
```

**Use case:** Prevent two requests generating the same AI curriculum simultaneously.

---

## Practice Task

```bash
SET user:7:name "Test"
SET user:7:requests 0
INCR user:7:requests
INCR user:7:requests
INCRBY user:7:requests 5
GET user:7:requests
SET user:7:otp 9999 EX 30
TTL user:7:otp
```