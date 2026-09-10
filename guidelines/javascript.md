# JavaScript Engineering & Review Guidelines

## 1. Modern Syntax & Readability
- Follow modern **ES6+** standards. Use `const` by default and `let` only when re-assignment is needed. Strictly avoid `var` (function-scoping and hoisting hazards).
- Use descriptive `camelCase` for variables and functions, `PascalCase` for classes/constructors, and `UPPER_SNAKE_CASE` for configuration constants.
- Prefer arrow functions for callbacks, template literals for strings, and destructuring for cleaner parameter handling.

## 2. Common Bug Prevention & Edge Cases
- **Strict Equality**: Always use strict equality (`===` and `!==`) to prevent unintended type coercion bugs.
- **Nullish Safety**: Use optional chaining (`?.`) and nullish coalescing (`??`) instead of logical OR (`||`) when checking defaults for boolean or numeric zero values.
- **Asynchronous Flow**: Always wrap `async/await` in `try...catch` blocks or chain `.catch()` on Promises to avoid unhandled promise rejections.
- **Array Mutation**: Be cautious with in-place mutating methods (`splice`, `sort`, `reverse`) on shared state; prefer immutable patterns or spreading (`[...arr]`).

## 3. Security Best Practices
- **Prevent Injection**: Never use `eval()`, `new Function()`, or `setTimeout(string)`.
- **XSS Prevention**: Avoid inserting unsanitized HTML via `innerHTML` or `document.write()`. Use `textContent` or framework-sanitized bindings.
- **Secrets Management**: Do not hardcode credentials, private tokens, or backend API keys in client-side code.
- **Prototype Pollution**: Avoid recursive object merging without validating keys against `__proto__`, `constructor`, and `prototype`.

## 4. Performance & Memory Considerations
- **Data Structures**: Use `Set` and `Map` for fast lookups and keyed collections instead of object-as-map patterns.
- **Event Listeners & Cleanup**: Ensure event listeners, intervals, and observers are cleaned up when no longer needed to prevent memory leaks.
- **DOM Access**: Minimize DOM queries inside loops; cache references or use DocumentFragments for batch mutations.
