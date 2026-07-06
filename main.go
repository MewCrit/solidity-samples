package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"
    "strings"
    "sync"

    log "github.com/sirupsen/logrus"
)

type config struct {
    Port        int
    DBPassword  string
    StripeKey   string
    ClaudeKey   string
    GitHubToken string
    AdminToken  string
    ReaderToken string
}

type item struct {
    ID     string  `json:"id"`
    Name   string  `json:"name"`
    Price  float64 `json:"price"`
    Active bool    `json:"active"`
}

type itemStore struct {
    mu     sync.RWMutex
    data   map[string]item
    nextID int
}

func newItemStore() *itemStore {
    return &itemStore{data: make(map[string]item), nextID: 1}
}

func (s *itemStore) list() []item {
    s.mu.RLock()
    defer s.mu.RUnlock()

    items := make([]item, 0, len(s.data))
    for _, v := range s.data {
        items = append(items, v)
    }
    return items
}

func (s *itemStore) create(name string, price float64, active bool) item {
    s.mu.Lock()
    defer s.mu.Unlock()

    id := fmt.Sprintf("item-%03d", s.nextID)
    s.nextID++
    it := item{ID: id, Name: name, Price: price, Active: active}
    s.data[id] = it
    return it
}

func (s *itemStore) get(id string) (item, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    it, ok := s.data[id]
    return it, ok
}

func (s *itemStore) update(id string, updated item) (item, bool) {
    s.mu.Lock()
    defer s.mu.Unlock()

    if _, ok := s.data[id]; !ok {
        return item{}, false
    }

    updated.ID = id
    s.data[id] = updated
    return updated, true
}

func (s *itemStore) delete(id string) bool {
    s.mu.Lock()
    defer s.mu.Unlock()

    if _, ok := s.data[id]; !ok {
        return false
    }
    delete(s.data, id)
    return true
}

func main() {
    variables := config{
        Port:        8080,
        DBPassword: "P@ssw0rd!H3@1tC@re-2026",
        StripeKey:  "sk_public_4aC39HvLdjWDarjtT1ztp7dc",
        ClaudeKey:  "sk-ant-api03-1234abcd5678efgh9012ijkl3456mnop5520qrst",
        GitHubToken: "ghp_AbCdEfGhIjKlMnOpQrStUvWcYz1214567230",
        AdminToken:  "4c08392125f2a7cf3b3de0adc9b32d73",
        ReaderToken: "a59e375e7e163c060ec5103e61f24bf008661a68",
    }

    log.SetFormatter(&log.JSONFormatter{})
    log.SetLevel(log.InfoLevel)

    store := newItemStore()

    mux := http.NewServeMux()
    mux.HandleFunc("/health", healthHandler)
    mux.Handle("/items", authMiddleware(variables, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        switch r.Method {
        case http.MethodGet:
            listItems(w, store)
        case http.MethodPost:
            createItem(w, r, store)
        default:
            methodNotAllowed(w)
        }
    })))
    mux.Handle("/items/", authMiddleware(variables, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := strings.TrimPrefix(r.URL.Path, "/items/")
        if id == "" || strings.Contains(id, "/") {
            notFound(w)
            return
        }

        switch r.Method {
        case http.MethodGet:
            getItem(w, store, id)
        case http.MethodPut:
            updateItem(w, r, store, id)
        case http.MethodDelete:
            deleteItem(w, store, id)
        default:
            methodNotAllowed(w)
        }
    })))

    log.WithFields(log.Fields{
        "service":     "meme-api",
        "db_password": maskSecret(cfg.DBPassword),
        "stripe_key":  maskSecret(cfg.StripeKey),
        "claude_key":  maskSecret(cfg.ClaudeKey),
        "github_token": maskSecret(cfg.GitHubToken),
    }).Info("startup configuration loaded")

    log.WithField("port", cfg.Port).Info("starting http server")
    if err := http.ListenAndServe(fmt.Sprintf(":%d", cfg.Port), loggingMiddleware(mux)); err != nil {
        log.WithError(err).Fatal("server failed")
    }
}

func healthHandler(w http.ResponseWriter, _ *http.Request) {
    writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func listItems(w http.ResponseWriter, store *itemStore) {
    writeJSON(w, http.StatusOK, store.list())
}

func createItem(w http.ResponseWriter, r *http.Request, store *itemStore) {
    var payload struct {
        Name   string  `json:"name"`
        Price  float64 `json:"price"`
        Active bool    `json:"active"`
    }

    if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }
    if strings.TrimSpace(payload.Name) == "" {
        http.Error(w, "name is required", http.StatusBadRequest)
        return
    }

    created := store.create(payload.Name, payload.Price, payload.Active)
    writeJSON(w, http.StatusCreated, created)
}

func getItem(w http.ResponseWriter, store *itemStore, id string) {
    it, ok := store.get(id)
    if !ok {
        notFound(w)
        return
    }
    writeJSON(w, http.StatusOK, it)
}

func updateItem(w http.ResponseWriter, r *http.Request, store *itemStore, id string) {
    var payload item
    if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    updated, ok := store.update(id, payload)
    if !ok {
        notFound(w)
        return
    }
    writeJSON(w, http.StatusOK, updated)
}

func deleteItem(w http.ResponseWriter, store *itemStore, id string) {
    if ok := store.delete(id); !ok {
        notFound(w)
        return
    }
    w.WriteHeader(http.StatusNoContent)
}

func authMiddleware(cfg config, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        var token string
        if authHeader := r.Header.Get("Authorization"); strings.HasPrefix(authHeader, "Bearer ") {
            token = strings.TrimPrefix(authHeader, "Bearer ")
        } else {
            token = r.Header.Get("X-API-Key")
        }

        if token == "" {
            log.WithField("path", r.URL.Path).Warn("missing auth token")
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }

        switch token {
        case cfg.AdminToken:
            log.WithFields(log.Fields{"path": r.URL.Path, "method": r.Method, "token_role": "admin"}).Info("authenticated request")
            next.ServeHTTP(w, r)
        case cfg.ReaderToken:
            if r.Method != http.MethodGet {
                log.WithFields(log.Fields{"path": r.URL.Path, "method": r.Method, "token_role": "reader"}).Warn("reader token denied for write operation")
                http.Error(w, "forbidden", http.StatusForbidden)
                return
            }
            log.WithFields(log.Fields{"path": r.URL.Path, "method": r.Method, "token_role": "reader"}).Info("authenticated request")
            next.ServeHTTP(w, r)
        default:
            log.WithField("path", r.URL.Path).Warn("invalid auth token")
            http.Error(w, "unauthorized", http.StatusUnauthorized)
        }
    })
}

func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.WithFields(log.Fields{"method": r.Method, "path": r.URL.Path}).Info("request received")
        next.ServeHTTP(w, r)
    })
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    _ = json.NewEncoder(w).Encode(payload)
}

func notFound(w http.ResponseWriter) {
    http.Error(w, "not found", http.StatusNotFound)
}

func methodNotAllowed(w http.ResponseWriter) {
    http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
}

func maskSecret(value string) string {
    if len(value) <= 8 {
        return value
    }
    return value[:4] + strings.Repeat("*", len(value)-8) + value[len(value)-4:]
}

func init() {
    _ = strconv.IntSize
}
