---
name: frontend-implementation
description: Comprehensive frontend development patterns for React, Vue, and modern JavaScript applications including state management, routing, and performance.
license: Apache-2.0
metadata:
  category: frontend-development
  tags: [react, vue, javascript, typescript, frontend, ui]
---

# Frontend Implementation

This skill provides comprehensive guidance for building modern frontend applications with React, Vue, and JavaScript.

## React Development

### 1. Component Architecture
```typescript
// Good: Small, focused components
import React, { useState, useEffect } from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled || false}
      className="px-4 py-2 bg-blue-500 text-white rounded"
    >
      {label}
    </button>
  );
};

// Bad: God component doing too much
export const SuperComponent: React.FC = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Too many responsibilities
  return (
    <div className="super-component">
      {/* 200 more lines */}
    </div>
  );
};
```

### 2. Custom Hooks
```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(initialValue);

  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key);
      if (item) setStoredValue(JSON.parse(item));
    } catch (error) {
      console.error(`Failed to load ${key}:`, error);
    }
  }, [key]);

  const setValue = useCallback((value: T) => {
    setStoredValue(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  }, []);

  return [storedValue, setStoredValue];
}

// Usage
function UserProfile() {
  const [user, setUser] = useLocalStorage<User>('user', null);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={() => setUser(null)}>Logout</button>
    </div>
  );
}
```

### 3. Performance Optimization
```typescript
import React, { memo, useMemo, useState } from 'react';

// Memo: Prevent unnecessary re-renders
const ExpensiveComponent = memo(({ data }: { data: any[] }) => {
  return (
    <ul>
      {data.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

// useMemo: Cache expensive calculations
const List = ({ items }: { items: number[] }) => {
  const sortedItems = useMemo(() => {
    return items.slice().sort((a, b) => a - b);
  }, [items]);

  return <ul>{sortedItems.map((i) => <li key={i}>{i}</li>)}</ul>;
};

// Lazy loading with React.lazy
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <React.Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </React.Suspense>
  );
}
```

### 4. State Management

```typescript
// Context API for global state
import React, { createContext, useContext, useState } from 'react';

interface AppContextType {
  user: User | null;
  login: () => void;
  logout: () => void;
}

const AppContext = createContext<AppContextType | null>(null);

export const AppProvider: React.FC = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback((username: string, password: string) => {
    // Login logic
    setUser({ id: 1, name: username });
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  return (
    <AppContext.Provider value={{ user, login, logout }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
};
```

### 5. Routing
```typescript
import { BrowserRouter, Routes, Route, Link, useLocation, useParams } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

function UserProfile() {
  const { id } = useParams();

  if (!id) return <div>Invalid user ID</div>;

  return <div>User {id}</div>;
}

// Navigation with Link
function Navigation() {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <nav>
      <Link to="/" className={isActive('/') ? 'active' : ''}>Home</Link>
      <Link to="/users" className={isActive('/users') ? 'active' : ''}>Users</Link>
      <Link to="/about" className={isActive('/about') ? 'active' : ''}>About</Link>
    </nav>
  );
}
```

### 6. Forms and Validation
```typescript
import { useState } from 'react';

interface FormErrors {
  [key: string]: string;
}

interface FormState {
  values: Record<string, string>;
  errors: FormErrors;
  touched: Record<string, boolean>;
}

function useForm(initialValues: Record<string, string>) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validate = (name: string, value: string): string | null => {
    // Validation logic
    if (name === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return 'Invalid email address';
    }
    if (name === 'password' && value.length < 8) {
      return 'Password must be at least 8 characters';
    }
    return null;
  };

  const handleChange = (name: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setValues({ ...values, [name]: e.target.value });
    setTouched({ ...touched, [name]: true });
    const error = validate(name, e.target.value);
    setErrors({ ...errors, [name]: error || '' });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formErrors = Object.entries(values).reduce<FormErrors>((acc, [key, value]) => ({
      ...acc,
      [key]: validate(key, value) || ''
    }), {});

    if (Object.values(formErrors).some(err => err !== '')) {
      return; // Has errors
    }

    // Submit form
    console.log('Form submitted:', values);
  };

  return { values, errors, touched, handleChange, handleSubmit };
}

// Usage
function LoginForm() {
  const { values, errors, touched, handleChange, handleSubmit } = useForm({
    email: '',
    password: '',
  });

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={values.email}
        onChange={(e) => handleChange('email', e)}
      />
      {touched.email && errors.email && <span className="error">{errors.email}</span>}

      <input
        type="password"
        value={values.password}
        onChange={(e) => handleChange('password', e)}
      />
      {touched.password && errors.password && <span className="error">{errors.password}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

### 7. API Integration
```typescript
import { useState, useEffect } from 'react';

function useFetchData(url: string) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const jsonData = await response.json();
        setData(jsonData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [url]);

  return { data, loading, error, refetch: () => fetchData() };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useFetchData(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data</div>;

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  );
}
```

## Vue Development

### 1. Composition API
```typescript
import { defineComponent, ref, computed, onMounted } from 'vue';

export default defineComponent({
  name: 'Counter',
  setup() {
    const count = ref(0);
    const doubled = computed(() => count.value * 2);

    const increment = () => {
      count.value++;
    };

    onMounted(() => {
      console.log('Component mounted');
    });

    return { count, doubled, increment };
  },
});
```

### 2. Reactive State
```typescript
import { reactive, computed } from 'vue';

export default defineComponent({
  name: 'Form',
  setup() {
    const form = reactive({
      username: '',
      email: '',
      password: '',
      errors: {} as Record<string, string>,
    });

    const isValid = computed(() => {
      return form.username.length > 0 &&
             form.email.includes('@') &&
             form.password.length >= 8;
    });

    const submitForm = () => {
      if (isValid.value) {
        console.log('Form submitted:', form);
      } else {
        form.errors = { submit: 'Please fix errors before submitting' };
      }
    };

    return { form, isValid, submitForm };
  },
});
```

### 3. Pinia State Management
```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null);
  const isLoggedIn = computed(() => !!user.value);

  const login = async (username: string, password: string) => {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      user.value = await response.json();
    }
  };

  const logout = () => {
    user.value = null;
  };

  return { user, isLoggedIn, login, logout };
});
```

### 4. Vue Router
```typescript
import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import About from './views/About.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/about', component: About },
  ],
});

export default router;
```

## Modern JavaScript

### 1. ES Modules
```javascript
// math.js
export const add = (a, b) => a + b;
export const multiply = (a, b) => a * b;
export const divide = (a, b) => a / b;

// main.js
import { add, multiply, divide } from './math.js';

console.log(add(2, 3)); // 5
console.log(multiply(4, 5)); // 20
console.log(divide(10, 2)); // 5
```

### 2. Async/Await
```javascript
async function fetchData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}

async function main() {
  const [user, post] = await Promise.all([
    fetchData('/api/user'),
    fetchData('/api/posts'),
  ]);

  console.log('User:', user);
  console.log('Post:', post);
}
```

### 3. Error Handling
```javascript
async function safeFetch(url, options = {}) {
  try {
    const response = await fetch(url, {
      timeout: 5000,
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      console.error('Type error:', error);
    } else if (error instanceof SyntaxError) {
      console.error('JSON parsing error:', error);
    } else {
      console.error('Unknown error:', error);
    }
    throw error;
  }
}
```

## Performance Best Practices

### 1. Code Splitting
```javascript
// Dynamic imports
async function loadComponent(componentName) {
  const module = await import(`./components/${componentName}.js`);
  return module.default;
}

// Usage
loadComponent('UserProfile');
```

### 2. Tree Shaking
```javascript
// Export only what's needed
export const addUser = (user) => {
  users.push(user);
};

export const getUser = (id) => {
  return users.find(u => u.id === id);
};

// Don't export unused functions
```

### 3. Lazy Loading Images
```javascript
// Load images only when visible
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
    }
  });
});

document.querySelectorAll('img[data-src]').forEach((img) => {
  observer.observe(img);
});
```

### 4. Virtual Scrolling
```javascript
const listSize = 20;
let startIndex = 0;

function renderList() {
  const list = document.getElementById('list');
  const endIndex = Math.min(startIndex + listSize, items.length);

  list.innerHTML = items
    .slice(startIndex, endIndex)
    .map((item) => `<li>${item}</li>`)
    .join('');
}

document.getElementById('load-more').addEventListener('click', () => {
  startIndex += listSize;
  renderList();
});
```

## TypeScript Integration

### 1. Type Definitions
```typescript
// types.d.ts
interface User {
  id: number;
  name: string;
  email: string;
}

interface ApiResponse<T> {
  data: T;
  error: string | null;
  status: number;
}

interface FormProps {
  onSubmit: (data: any) => void;
  initialValues: any;
}
```

### 2. Generic Types
```typescript
function identity<T>(value: T): T {
  return value;
}

function first<T>(array: T[]): T | undefined {
  return array[0];
}

// Usage
identity<string>('hello'); // 'hello'
first<number>([1, 2, 3]); // 1
```

## CSS/Styling

### 1. CSS-in-JS
```javascript
const styles = {
  button: {
    backgroundColor: '#3b82f6',
    color: 'white',
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    cursor: 'pointer',
  },
  input: {
    padding: '8px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
  },
};

function Button({ label, onClick }) {
  const button = document.createElement('button');
  Object.assign(button.style, styles.button);
  button.textContent = label;
  button.addEventListener('click', onClick);
  return button;
}
```

### 2. CSS Modules
```css
/* styles.css */
:root {
  --primary-color: #3b82f6;
  --secondary-color: #6c757d;
  --text-color: #1f2937;
  --background-color: #ffffff;
}

.button {
  background-color: var(--primary-color);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.button:hover {
  background-color: var(--secondary-color);
}
```

## Accessibility

### 1. ARIA Labels
```html
<button aria-label="Close dialog" onClick={closeDialog}>
  Close
</button>

<input
  type="search"
  aria-label="Search products"
  placeholder="Search products..."
/>

<nav aria-label="Main navigation">
  <ul role="menu">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

### 2. Keyboard Navigation
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }

  if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
    e.target.blur();
  }
});
```

### 3. Focus Management
```typescript
function focusNextElement(elements: HTMLElement[]) {
  const currentIndex = Array.from(elements).indexOf(document.activeElement);

  if (currentIndex < elements.length - 1) {
    elements[currentIndex + 1].focus();
  }
}

// Usage
const inputs = Array.from(document.querySelectorAll('input'));
document.querySelector('button').addEventListener('click', () => {
  focusNextElement(inputs);
});
```

## Testing

### 1. React Testing Library
```typescript
import { render, screen, fireEvent } from '@testing-library/react';

import Button from './Button';

test('renders button with label', () => {
  render(<Button label="Click me" />);
  const button = screen.getByText('Click me');
  expect(button).toBeInTheDocument();
});

test('calls onClick handler', () => {
  const handleClick = jest.fn();
  render(<Button label="Click me" onClick={handleClick} />);
  const button = screen.getByText('Click me');
  fireEvent.click(button);
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

### 2. Component Testing
```vue
import { mount } from '@vue/test-utils';
import Counter from './Counter.vue';

test('increments counter', () => {
  const wrapper = mount(Counter);
  const button = wrapper.find('button');
  const count = wrapper.vm.count;

  expect(count).toBe(0);
  await button.trigger('click');
  expect(wrapper.vm.count).toBe(1);
});
```

### 3. E2E Testing
```javascript
// Cypress E2E test
describe('User Login Flow', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('testuser');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });

  it('should show error for invalid credentials', () => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('invalid');
    cy.get('input[name="password"]').type('wrong');
    cy.get('button[type="submit"]').click();
    cy.get('.error').should('contain', 'Invalid credentials');
  });
});
```

## Deployment

### 1. Vite Build
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  server: {
    port: 3000,
  },
});
```

### 2. Next.js Build
```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['example.com'],
  },
  env: {
    production: {
      API_URL: 'https://api.example.com',
    },
  },
};
```

### 3. Static Site Generation
```bash
# Build with Vite
npm run build

# Deploy to Netlify
npx netlify-cli deploy --prod --dir=dist

# Deploy to Vercel
npx vercel --prod

# Deploy to GitHub Pages
npm run build
gh-pages -d dist
```

## Best Practices

### 1. Component Design
- Single responsibility
- Reusable props interface
- Default prop values
- Type checking with TypeScript
- Memoization for expensive computations

### 2. State Management
- Local state for component-specific data
- Context/API for shared state
- Server state for backend data
- Persistent storage for user preferences

### 3. Performance
- Code splitting and lazy loading
- Image optimization
- Virtual scrolling for long lists
- Debouncing and throttling
- Service worker for caching

### 4. Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support
- Focus management
- Color contrast

### 5. Security
- XSS prevention with escaping
- CSRF protection
- Content security policy
- HTTPS in production
- Input validation and sanitization

## References
- [React Documentation](https://react.dev/)
- [Vue Documentation](https://vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Next.js](https://nextjs.org/)
- [Testing Library](https://testing-library.com/)
- [Cypress](https://www.cypress.io/)
