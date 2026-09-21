# React — Exam-Day Quick Reference
**Confirmed format (from real candidate reports):** you get an EXISTING React project (not a blank file). You complete MISSING functionality — e.g. an Amazon/Flipkart-style product catalog needing search, category filter, price filter, sorting, multi-filter combination, and re-rendering the filtered list.

**Do NOT modify existing `id`/`className` attributes** — test cases likely depend on them to find elements. Only fill in the logic you're asked to.

---

## The exact pattern you'll almost certainly see

A list of items (products) in state, several filter/sort controls, and a function that combines them all before rendering. The rendering and state setup will likely already be done — your job is the FILTER/SORT LOGIC functions themselves.

```javascript
const [searchTerm, setSearchTerm] = useState("");
const [category, setCategory] = useState("All");
const [maxPrice, setMaxPrice] = useState(20000);
const [sortBy, setSortBy] = useState("name-asc");
```

---

## TODO 1: Search filter (case-insensitive "contains")

```javascript
function filterBySearch(products, term) {
  if (!term) return products;              // empty search = show all
  const lower = term.toLowerCase();
  return products.filter(p =>
    p.name.toLowerCase().includes(lower)
  );
}
```
**Key ideas:** `.filter()` keeps only matching items. `.includes()` checks substring presence, not exact match. `.toLowerCase()` on BOTH sides makes it case-insensitive. The `if (!term) return products` guard isn't strictly required (empty string `.includes("")` is always true anyway) but makes intent explicit and is safe to include.

---

## TODO 2: Category filter (exact match, with an "All" bypass)

```javascript
function filterByCategory(products, category) {
  if (category === "All") return products;
  return products.filter(p => p.category === category);
}
```
**Key idea:** always handle the "no filter selected" case (`"All"`) as an early return — a very common pattern across all filter functions.

---

## TODO 3: Price filter (numeric comparison)

```javascript
function filterByPrice(products, max) {
  return products.filter(p => p.price <= max);
}
```
**Key idea:** simplest of the four — just a numeric comparison inside `.filter()`.

---

## TODO 4: Sorting (multiple sort keys)

```javascript
function sortProducts(products, sortKey) {
  const sorted = [...products];   // COPY the array — never mutate original state directly
  switch (sortKey) {
    case "name-asc":
      return sorted.sort((a, b) => a.name.localeCompare(b.name));
    case "name-desc":
      return sorted.sort((a, b) => b.name.localeCompare(a.name));
    case "price-asc":
      return sorted.sort((a, b) => a.price - b.price);
    case "price-desc":
      return sorted.sort((a, b) => b.price - a.price);
    case "rating-desc":
      return sorted.sort((a, b) => b.rating - a.rating);
    default:
      return sorted;
  }
}
```
**Key ideas:**
- `[...products]` spreads into a NEW array before sorting — `.sort()` mutates in place, and mutating state directly is a classic React bug/red flag graders look for.
- String comparison: use `.localeCompare()`, not `<`/`>` (works correctly for strings; `<`/`>` technically works for simple ASCII too but `localeCompare` is the "correct" idiomatic choice).
- Number comparison: `a.price - b.price` gives ascending, flip to `b.price - a.price` for descending — this subtraction trick is the standard JS sort-by-number pattern.

---

## Combining multiple filters (the "pipeline" pattern)

```javascript
function getDisplayedProducts() {
  let result = ALL_PRODUCTS;
  result = filterBySearch(result, searchTerm);
  result = filterByCategory(result, category);
  result = filterByPrice(result, maxPrice);
  result = sortProducts(result, sortBy);
  return result;
}
```
Apply each filter in sequence, each one narrowing the previous result. Order usually doesn't matter for correctness (filtering commutes), but doing sort LAST is important — sorting then filtering can still work, but filtering then sorting is more intuitive and avoids sorting items you're about to throw away anyway.

---

## Core React syntax cheat sheet (in case you need vanilla basics too)

**useState:**
```javascript
const [value, setValue] = useState(initialValue);
// NEVER mutate state directly: value.push(x) is WRONG
// Always: setValue([...value, x])  (for arrays)
// Always: setValue({...value, key: newVal})  (for objects)
```

**Controlled input:**
```javascript
<input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
```

**Rendering a list (never forget `key`):**
```javascript
{items.map(item => <li key={item.id}>{item.name}</li>)}
```

**Event handler — common mistake to avoid:**
```javascript
onClick={handleClick}        // correct — passes the function reference
onClick={handleClick()}      // WRONG — calls it immediately on render
onClick={() => handleClick(id)}  // correct way to pass an argument
```

**Conditional rendering:**
```javascript
{items.length === 0 && <p>No results found.</p>}
```

**Basic form validation pattern:**
```javascript
const [email, setEmail] = useState("");
const [error, setError] = useState("");

function validate() {
  if (!email.includes("@")) {
    setError("Enter a valid email");
    return false;
  }
  setError("");
  return true;
}

function handleSubmit(e) {
  e.preventDefault();
  if (validate()) {
    // proceed
  }
}
```

**Array methods you'll lean on constantly:**
- `.filter(fn)` — keep items matching a condition, returns new array
- `.map(fn)` — transform each item, returns new array
- `.sort(fn)` — sort in place (spread `[...arr]` first to avoid mutating original)
- `.find(fn)` — get the first matching item (or undefined)
- `.reduce(fn, initial)` — combine into a single value (sums, groupings, etc.)

---

## Pre-submission checklist for the React section

```
[ ] Did I touch ANY existing id/className? (Don't — revert if so.)
[ ] Does the app actually render without a red error screen?
[ ] Am I mutating state directly anywhere? (arr.push, obj.key = x are red flags)
[ ] Did I include `key` on every mapped list item?
[ ] Did I test: empty search, "All" category, max price slider at both ends?
[ ] Click "Run Tests" (if available) before final submit — use the iteration,
    don't submit blind.
```

---

## If it's NOT this exact filtering pattern

If the actual task is something else entirely (a to-do list, a form, a counter, basic routing), fall back to these fundamentals:
- Get SOMETHING rendering first, even ugly — partial/working beats broken/ambitious.
- `useState` for anything that changes on screen.
- `useEffect(() => {...}, [deps])` only if something needs to run on mount or when a value changes — empty `[]` = run once, no array = every render (usually a bug).
- Basic routing: `<Routes><Route path="/x" element={<X/>} /></Routes>`, `useNavigate()`, `<Link to="/x">`.
- If genuinely stuck and time is short: per every Reddit report, this is the LOWEST priority section — don't let it eat time you need to double check DP/RAG/other sections if you still have time left there instead.