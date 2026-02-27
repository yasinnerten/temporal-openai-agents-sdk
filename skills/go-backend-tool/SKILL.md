---
name: go-backend-tool
description: Comprehensive Go backend development patterns including REST APIs, database integration, and microservices.
license: Apache-2.0
metadata:
  category: backend-development
  tags: [go, backend, api, database]
---

# Go Backend Development

This skill provides guidance for building robust Go backend services, APIs, and microservices.

## Project Structure

```go
myproject/
├── cmd/
│   ├── server/
│   │   └── main.go
│   └── worker/
│       └── main.go
├── internal/
│   ├── handlers/
│   │   ├── user.go
│   │   └── order.go
│   ├── models/
│   │   ├── user.go
│   │   └── order.go
│   ├── repository/
│   │   ├── user.go
│   │   └── order.go
│   └── service/
│       ├── auth.go
│       └── email.go
├── pkg/
│   ├── database/
│   │   ├── postgres.go
│   │   └── redis.go
│   ├── middleware/
│   │   ├── auth.go
│   │   └── logging.go
│   └── util/
│       ├── validator.go
│       └── jwt.go
├── api/
│   ├── handlers.go
│   ├── routes.go
│   └── middleware.go
├── config/
│   └── config.go
├── migrations/
├── tests/
└── go.mod
```

## Standard Layouts

### 1. HTTP Handlers
```go
package handlers

import (
    "encoding/json"
    "net/http"
)

type UserHandler struct {
    logger Logger
}

func NewUserHandler(logger Logger) *UserHandler {
    return &UserHandler{logger: logger}
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Name  string `json:"name"`
        Email string `json:"email"`
    }

    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        h.logger.Error("Failed to decode request", "handler", "create_user")
        return
    }

    // Validate input
    if input.Name == "" {
        http.Error(w, "Name is required", http.StatusBadRequest)
        return
    }

    // Process user creation
    user, err := h.userService.Create(input.Name, input.Email)
    if err != nil {
        h.logger.Error("Failed to create user", "handler", "create_user", err)
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```

### 2. Database Layer
```go
package repository

import (
    "context"
    "database/sql"
)

type UserRepository interface {
    Create(ctx context.Context, name, email string) (*User, error)
    FindByID(ctx context.Context, id int64) (*User, error)
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}

type PostgresUserRepository struct {
    db *sql.DB
}

func NewPostgresUserRepository(db *sql.DB) UserRepository {
    return &PostgresUserRepository{db: db}
}

func (r *PostgresUserRepository) Create(ctx context.Context, name, email string) (*User, error) {
    query := `
        INSERT INTO users (name, email, created_at)
        VALUES ($1, $2, NOW())
        RETURNING id, name, email, created_at
    `

    user := &User{}
    err := r.db.QueryRowContext(ctx, query, name, email).Scan(
        &user.ID,
        &user.Name,
        &user.Email,
        &user.CreatedAt,
    )

    if err != nil {
        return nil, err
    }

    return user, nil
}
```

### 3. Middleware
```go
package middleware

import (
    "log/slog"
    "net/http"
    "strings"
)

func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        slog.Info("Incoming request",
            "method", r.Method,
            "path", r.URL.Path,
            "remote_addr", r.RemoteAddr,
        )

        // Call next handler
        next.ServeHTTP(w, r)

        slog.Info("Request completed",
            "status", w.Header().Get("Status"),
        )
    })
}

func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if !strings.HasPrefix(token, "Bearer ") {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }

        next.ServeHTTP(w, r)
    })
}
```

## Error Handling

### 1. Custom Errors
```go
package errors

import "fmt"

type AppError struct {
    Code    string
    Message string
    Details map[string]any
    HTTPCode int
}

func (e *AppError) Error() string {
    return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

func NewAppError(code, message string, httpCode int) *AppError {
    return &AppError{
        Code:    code,
        Message: message,
        HTTPCode: httpCode,
        Details:  make(map[string]any),
    }
}

func NewValidationError(field, message string) *AppError {
    return NewAppError("VALIDATION_ERROR", message, http.StatusBadRequest)
}

func NewNotFoundError(resource, id string) *AppError {
    return NewAppError("NOT_FOUND",
        fmt.Sprintf("%s with id %s not found", resource, id),
        http.StatusNotFound,
    )
}
```

### 2. Error Middleware
```go
package middleware

import (
    "log/slog"
    "net/http"
)

func ErrorMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if r := recover(); r != nil {
                slog.Error("Panic recovered",
                    "error", r,
                    "path", r.URL.Path,
                )
                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()

        next.ServeHTTP(w, r)
    })
}
```

## Database Patterns

### 1. Transaction Management
```go
func (r *PostgresUserRepository) TransferFunds(ctx context.Context, fromID, toID int64, amount float64) error {
    tx, err := r.db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // Lock rows
    _, err = tx.ExecContext(ctx, "SELECT * FROM users WHERE id = $1 FOR UPDATE", fromID)
    if err != nil {
        return err
    }

    _, err = tx.ExecContext(ctx, "SELECT * FROM users WHERE id = $1 FOR UPDATE", toID)
    if err != nil {
        return err
    }

    // Deduct and add
    _, err = tx.ExecContext(ctx, "UPDATE users SET balance = balance - $2 WHERE id = $3", amount, fromID)
    if err != nil {
        return err
    }

    _, err = tx.ExecContext(ctx, "UPDATE users SET balance = balance + $2 WHERE id = $3", amount, toID)
    if err != nil {
        return err
    }

    return tx.Commit()
}
```

### 2. Connection Pool
```go
package database

import (
    "context"
    "time"
)

type ConnectionPool struct {
    maxConns     int
    activeConns   int
    idleConns    int
    maxIdle      time.Duration
    maxLifetime  time.Duration
}

func NewConnectionPool(maxConns int) *ConnectionPool {
    return &ConnectionPool{
        maxConns:    maxConns,
        maxIdle:      5 * time.Minute,
        maxLifetime:   time.Hour,
    }
}

func (p *ConnectionPool) Get(ctx context.Context) (*Connection, error) {
    // Get or create connection
    conn, err := p.acquire(ctx)
    if err != nil {
        return nil, err
    }

    return conn, nil
}
```

## Configuration Management

### 1. Viper Integration
```go
package config

import (
    "github.com/spf13/viper"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
    Redis   RedisConfig
}

type ServerConfig struct {
    Host string
    Port int
}

func LoadConfig() (*Config, error) {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")
    viper.AutomaticEnv()

    var cfg Config
    if err := viper.ReadInConfig(&cfg); err != nil {
        return nil, err
    }

    return &cfg, nil
}
```

### 2. Environment Variables
```go
package config

import (
    "os"
)

func GetEnv(key, defaultValue string) string {
    value := os.Getenv(key)
    if value == "" {
        return defaultValue
    }
    return value
}

func MustGetEnv(key string) string {
    value := os.Getenv(key)
    if value == "" {
        panic(fmt.Sprintf("Required environment variable %s not set", key))
    }
    return value
}
```

## Testing

### 1. Table-Driven Tests
```go
package handlers_test

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestCreateUser(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        wantCode int
    }{
        {
            name:    "Valid user creation",
            input:    `{"name":"John Doe","email":"john@example.com"}`,
            wantCode: http.StatusCreated,
        },
        {
            name:    "Missing name",
            input:    `{"email":"john@example.com"}`,
            wantCode: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            rr := httptest.NewRequest(http.MethodPost, "/users", nil)
            rr.Body = http.NoBody
            rr.Body = strings.NewReader(tt.input)

            w := httptest.NewRecorder()
            CreateUser(w, rr)

            if w.Code != tt.wantCode {
                t.Errorf("expected status %d, got %d", tt.wantCode, w.Code)
            }
        })
    }
}
```

### 2. Mocks with Interfaces
```go
package repository_test

import (
    "context"
    "testing"
)

type MockUserRepository struct {
    users map[int64]*User
}

func NewMockUserRepository() *MockUserRepository {
    return &MockUserRepository{
        users: make(map[int64]*User),
    }
}

func (m *MockUserRepository) Create(ctx context.Context, name, email string) (*User, error) {
    user := &User{ID: 1, Name: name, Email: email}
    m.users[user.ID] = user
    return user, nil
}

func TestUserService_CreateUser(t *testing.T) {
    repo := NewMockUserRepository()
    service := NewUserService(repo)

    user, err := service.Create(context.Background(), "John Doe", "john@example.com")
    if err != nil {
        t.Fatal(err)
    }

    if user.Name != "John Doe" {
        t.Errorf("expected name %s, got %s", "John Doe", user.Name)
    }
}
```

## Concurrency Patterns

### 1. Goroutines with Channels
```go
func ProcessItemsConcurrently(items []string) []string {
    results := make(chan string, len(items))

    // Start workers
    numWorkers := 5
    for i := 0; i < numWorkers; i++ {
        go func(workerID int) {
            for item := range items {
                if workerID == len(item)%numWorkers {
                    results <- processItem(item)
                }
            }
        }(i)
    }

    // Collect results
    var processed []string
    for i := 0; i < len(items); i++ {
        processed = append(processed, <-results)
    }

    close(results)
    return processed
}
```

### 2. WaitGroup
```go
import "sync"

func ProcessParallel(items []string) error {
    var wg sync.WaitGroup
    errChan := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(i string) {
            defer wg.Done()
            if err := processItem(i); err != nil {
                errChan <- err
            }
        }(item)
    }

    // Wait for all goroutines
    go func() {
        wg.Wait()
        close(errChan)
    }()

    // Check for errors
    for err := range errChan {
        if err != nil {
            return err
        }
    }

    return nil
}
```

## Logging and Monitoring

### 1. Structured Logging
```go
package main

import (
    "log/slog"
    "os"
)

func main() {
    // Configure structured logging
    handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    })

    logger := slog.New(handler)

    logger.Info("Application started",
        "version", "1.0.0",
        "environment", os.Getenv("ENV"),
    )

    // Usage
    logger.Debug("Processing user",
        "user_id", 123,
        "action", "update_profile",
    )

    logger.Error("Failed to connect to database",
        "error", "connection timeout",
        "retries", 3,
    )
}
```

### 2. Metrics
```go
package metrics

import (
    "time"
)

type Metrics struct {
    Requests      int64
    Errors       int64
    Latency      time.Duration
}

var globalMetrics = &Metrics{}

func RecordRequest(start time.Time) {
    latency := time.Since(start)
    globalMetrics.Requests++

    if latency > 0 {
        globalMetrics.Latency += latency
    }
}

func RecordError() {
    globalMetrics.Errors++
}

func GetMetrics() Metrics {
    return *globalMetrics
}
```

## API Design

### 1. RESTful Endpoints
```go
func SetupRoutes(r chi.Router) {
    r.Get("/users", ListUsers)
    r.Post("/users", CreateUser)
    r.Get("/users/{id}", GetUser)
    r.Put("/users/{id}", UpdateUser)
    r.Delete("/users/{id}", DeleteUser)
    r.Get("/users/{id}/orders", ListUserOrders)
}
```

### 2. Pagination
```go
type PaginatedResponse struct {
    Data       interface{} `json:"data"`
    Page       int       `json:"page"`
    PageSize   int       `json:"page_size"`
    Total      int64     `json:"total"`
    HasMore    bool      `json:"has_more"`
}

func Paginate(data interface{}, page, pageSize, total int64) PaginatedResponse {
    totalPages := int(total) / pageSize
    hasMore := page < totalPages

    return PaginatedResponse{
        Data:     data,
        Page:     page,
        PageSize:  pageSize,
        Total:    total,
        HasMore:   hasMore,
    }
}
```

## Deployment

### 1. Dockerfile
```dockerfile
# Multi-stage build
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -o server ./cmd/server

# Final stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=builder /app/server .
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
CMD ["./server"]
```

### 2. Health Checks
```go
package health

import (
    "net/http"
)

func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
    checks := map[string]bool{
        "database": checkDatabase(),
        "redis":    checkRedis(),
        "external_api": checkExternalAPI(),
    }

    allHealthy := true
    for _, healthy := range checks {
        if !healthy {
            allHealthy = false
        break
        }
    }

    status := http.StatusOK
    if !allHealthy {
        status = http.StatusServiceUnavailable
    }

    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status": status,
        "checks": checks,
    })
}

func checkDatabase() bool {
    // Check database connection
    return true
}

func checkRedis() bool {
    // Check Redis connection
    return true
}

func checkExternalAPI() bool {
    // Check external API connectivity
    return true
}
```

## Best Practices

### 1. Context Propagation
```go
func ProcessRequest(ctx context.Context, requestID string) {
    childCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    result, err := longOperation(childCtx)
    if err != nil {
        log.Error("Operation failed",
            "request_id", requestID,
            "error", err,
        )
    }
}
```

### 2. Graceful Shutdown
```go
func WaitForShutdown(sig chan os.Signal, timeout time.Duration) {
    signal.Notify(sig, os.Interrupt, syscall.SIGTERM)

    select {
    case <-sig:
        log.Info("Received shutdown signal, initiating graceful shutdown...")
        gracefulShutdown()
    case <-time.After(timeout):
        log.Warn("Shutdown timeout reached, forcing exit...")
        os.Exit(1)
    }
}

func gracefulShutdown() {
    // Close database connections
    // Finish processing current requests
    // Flush logs
    log.Info("Shutdown complete")
}
```

## References
- [Effective Go](https://golang.org/doc/effective_go.html)
- [Go Standard Library](https://pkg.go.dev/std)
- [Chi Router](https://github.com/go-chi/chi)
- [GORM ORM](https://gorm.io/docs/)
- [Testify Testing](https://github.com/stretchr/testify)
