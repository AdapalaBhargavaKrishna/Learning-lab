# React Section Crash Course — Cognizant ACE

Target: complete missing functionality in an existing product-listing app
(search, category filter, price filter, sort, multi-filter combo).

---

## 1. The core mental model

Almost every task in this section is: **state (filters) → derived data (filtered list) → render**.

Never mutate the original array. Always derive a *new* filtered/sorted array from state, on every render (or in `useMemo`).

```jsx
import { useState, useMemo } from "react";

function ProductList({ products }) {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [maxPrice, setMaxPrice] = useState(Infinity);
  const [sortBy, setSortBy] = useState("default"); // "priceLowHigh" | "priceHighLow" | "nameAZ"

  const visibleProducts = useMemo(() => {
    let result = [...products];

    // 1. Search (case-insensitive, partial match)
    if (search.trim()) {
      result = result.filter((p) =>
        p.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    // 2. Category filter
    if (category !== "all") {
      result = result.filter((p) => p.category === category);
    }

    // 3. Price filter
    result = result.filter((p) => p.price <= maxPrice);

    // 4. Sort
    if (sortBy === "priceLowHigh") result.sort((a, b) => a.price - b.price);
    if (sortBy === "priceHighLow") result.sort((a, b) => b.price - a.price);
    if (sortBy === "nameAZ") result.sort((a, b) => a.name.localeCompare(b.name));

    return result;
  }, [products, search, category, maxPrice, sortBy]);

  return (
    <div>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search products..."
      />

      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>

      <input
        type="number"
        value={maxPrice === Infinity ? "" : maxPrice}
        onChange={(e) =>
          setMaxPrice(e.target.value ? Number(e.target.value) : Infinity)
        }
        placeholder="Max price"
      />

      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="default">Sort by</option>
        <option value="priceLowHigh">Price: Low to High</option>
        <option value="priceHighLow">Price: High to Low</option>
        <option value="nameAZ">Name: A-Z</option>
      </select>

      <div className="grid">
        {visibleProducts.length === 0 ? (
          <p>No products found.</p>
        ) : (
          visibleProducts.map((p) => (
            <div key={p.id} className="card">
              <h3>{p.name}</h3>
              <p>{p.category}</p>
              <p>₹{p.price}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
```

**This one component covers ~80% of what you'll be asked to "complete."** If you memorize this shape, you're mostly translating it into whatever partial code they give you.

---

## 2. Things that trip people up under time pressure

- **`key` prop when mapping** — always use a stable unique id (`p.id`), never array index if the list can reorder/filter.
- **Controlled inputs** — value comes from state, `onChange` updates state. Never read `e.target.value` without wiring it back into `setState`.
- **`.sort()` mutates in place** — if `products` is a prop, do `[...products].sort(...)` not `products.sort(...)`, or you'll cause bugs on re-filter.
- **Number vs string from inputs** — `e.target.value` is always a string. Wrap in `Number()` before comparing/sorting numerically.
- **Empty/undefined state on load** — guard with `products?.length` or default `[]` so you don't crash on first render before data arrives.
- **Multiple filters must compose (AND logic)** — chain `.filter()` calls or combine conditions in one filter; don't let each filter dropdown overwrite the others' results.
- **Debounce isn't usually needed** for this scope — don't over-engineer, just wire `onChange` directly unless they explicitly ask for debounced search.

---

## 3. Form validation quick pattern (if a form task shows up)

```jsx
function CheckoutForm() {
  const [values, setValues] = useState({ name: "", email: "", qty: 1 });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    const newErrors = {};
    if (!values.name.trim()) newErrors.name = "Name is required";
    if (!/^\S+@\S+\.\S+$/.test(values.email)) newErrors.email = "Invalid email";
    if (values.qty < 1) newErrors.qty = "Quantity must be at least 1";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log("Submitted:", values);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" value={values.name} onChange={handleChange} />
      {errors.name && <span>{errors.name}</span>}

      <input name="email" value={values.email} onChange={handleChange} />
      {errors.email && <span>{errors.email}</span>}

      <input
        type="number"
        name="qty"
        value={values.qty}
        onChange={handleChange}
      />
      {errors.qty && <span>{errors.qty}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## 4. Event handling / rendering basics refresher

- `onClick={() => doThing(id)}` — wrap in arrow function when passing args, otherwise it fires on render.
- Conditional rendering: `{condition && <Thing />}` or ternary `{condition ? <A /> : <B />}`.
- Lists: `.map()` always returns an array of elements with `key`.
- Lifting state up: if two sibling components need the same filter state, the state lives in their common parent and gets passed down as props + a setter callback.

---

## 5. Rendering elements — the basics

React renders based on what a component *returns*. A few patterns you should be fluent in:

```jsx
// Basic element
function Welcome() {
  return <h1>Hello</h1>;
}

// Embedding JS expressions with {}
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

// Rendering a list (always needs a key)
function List({ items }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.text}</li>
      ))}
    </ul>
  );
}

// Conditional rendering — three common ways
function Status({ isLoggedIn, isLoading, error }) {
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      {isLoggedIn && <p>Welcome back!</p>}
      {isLoggedIn ? <button>Logout</button> : <button>Login</button>}
    </div>
  );
}

// Fragments — when you need to return multiple elements without a wrapper div
function Row() {
  return (
    <>
      <td>Cell 1</td>
      <td>Cell 2</td>
    </>
  );
}
```

Rule of thumb: JSX is just JavaScript. Anything inside `{}` is evaluated as a JS expression (not a statement — no `if`/`for` directly inside JSX, use ternaries/`&&`/`.map()`).

---

## 6. State management (internal component state) — `useState` deep dive

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  // Direct set
  const increment = () => setCount(count + 1);

  // Functional update — ALWAYS prefer this when new state depends on old state,
  // especially in loops/async/rapid clicks, to avoid stale-state bugs
  const incrementSafe = () => setCount((prev) => prev + 1);

  return (
    <div>
      <p>{count}</p>
      <button onClick={incrementSafe}>+1</button>
    </div>
  );
}

// State with objects — never mutate directly, always spread
function ProfileForm() {
  const [profile, setProfile] = useState({ name: "", age: 0 });

  const updateName = (name) =>
    setProfile((prev) => ({ ...prev, name })); // keeps `age`, updates `name`

  return <input value={profile.name} onChange={(e) => updateName(e.target.value)} />;
}

// State with arrays — same rule, never mutate
function TodoList() {
  const [todos, setTodos] = useState([]);

  const addTodo = (text) =>
    setTodos((prev) => [...prev, { id: Date.now(), text, done: false }]);

  const toggleTodo = (id) =>
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t))
    );

  const removeTodo = (id) =>
    setTodos((prev) => prev.filter((t) => t.id !== id));

  return (
    <ul>
      {todos.map((t) => (
        <li key={t.id} onClick={() => toggleTodo(t.id)}>
          {t.done ? "✅" : "⬜"} {t.text}
          <button onClick={() => removeTodo(t.id)}>x</button>
        </li>
      ))}
    </ul>
  );
}
```

**Golden rule they will test:** never do `todos.push(...)` or `profile.name = x` directly. Always create a new array/object. This is the #1 React bug pattern in assessments.

---

## 7. Handling events

```jsx
function EventDemo() {
  // Inline arrow function — needed when passing arguments
  const handleClick = (id) => console.log("clicked", id);

  // Event object access
  const handleChange = (e) => console.log(e.target.value);

  // Preventing default (forms, links)
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("submitted");
  };

  // Keyboard events
  const handleKeyDown = (e) => {
    if (e.key === "Enter") console.log("Enter pressed");
  };

  return (
    <div>
      <button onClick={() => handleClick(1)}>Click</button>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
      <form onSubmit={handleSubmit}>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
```

Common trap: `onClick={handleClick(1)}` **calls it immediately on render** instead of on click. Must wrap: `onClick={() => handleClick(1)}`.

---

## 8. Basic routing (React Router)

Assume `react-router-dom` v6 (most common in these assessments).

```jsx
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

// Reading a URL param
function ProductDetail() {
  const { id } = useParams();
  return <h2>Product {id}</h2>;
}

// Programmatic navigation (e.g. after form submit or button click)
function Products() {
  const navigate = useNavigate();
  return (
    <button onClick={() => navigate("/products/42")}>
      View Product 42
    </button>
  );
}
```

If the starter project already has `<Routes>` set up, your job is usually just adding a missing `<Route>` line or reading a param with `useParams()` — don't rebuild the router from scratch unless asked.

---

## 9. ES6 & JavaScript essentials (the stuff React leans on constantly)

```js
// Destructuring — props and state
const { name, price } = product;
const [count, setCount] = useState(0);

// Spread — copying/merging arrays & objects (core to immutable state updates)
const newArr = [...arr, newItem];
const newObj = { ...obj, key: "newValue" };

// Arrow functions
const double = (x) => x * 2;

// Template literals
const label = `${name} - ₹${price}`;

// Array methods you WILL use
arr.map((x) => x * 2);               // transform
arr.filter((x) => x > 10);           // select subset
arr.reduce((sum, x) => sum + x, 0);  // aggregate
arr.find((x) => x.id === 5);         // first match
arr.some((x) => x.done);             // any match?
arr.every((x) => x.done);            // all match?
arr.sort((a, b) => a.price - b.price); // MUTATES — copy first: [...arr].sort(...)

// Optional chaining & nullish coalescing (avoids crashes on missing data)
const city = user?.address?.city ?? "Unknown";

// Default parameters
function greet(name = "Guest") { return `Hi ${name}`; }

// Ternary (very common inside JSX)
const label2 = isActive ? "Active" : "Inactive";

// Short-circuit rendering trick
{isLoggedIn && <Dashboard />}
```

If a task description says "fix a bug" and you can't find it in the React logic, check for a plain JS mistake first: wrong array method, mutated state, missing `return`, off-by-one in a `.slice()`, or a broken template literal.

---

## 10. In-the-moment strategy

1. **Read the existing code fully before typing anything.** These tasks are "complete the missing piece," not "build from scratch" — the state variables and prop names are often already defined for you. Match their naming, don't invent your own.
2. Find the `// TODO` / empty function bodies first — that tells you exactly what's expected.
3. Get it *working* before making it clean. Partial credit likely exists per working filter/sort/search feature.
4. Test each filter independently in your head: does search still work after you add price filter? (AND logic, not overwrite.)
5. If time is short, prioritize: **search → category filter → sort → price filter → combined filters** roughly in that order of likely weight/ease.

Good luck — you clearly already know this, it's just about pattern-matching fast under time pressure.