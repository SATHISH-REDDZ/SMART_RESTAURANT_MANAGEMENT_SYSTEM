# System Design Document

## 1. Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                      CUSTOMER / ADMIN                       │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       FLASK BACKEND                         │
│  ┌──────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │ Auth & Session│  │ Order Processing │  │ ML Recommender│  │
│  └──────────────┘  └──────────────────┘  └───────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ SQL
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       SQLite DATABASE                       │
│ (users, categories, foods, cart, orders, order_items, etc.) │
└─────────────────────────────────────────────────────────────┘
```

## 2. Recommendation Algorithm Workflow
1. **Data Preprocessing**: Extract food attributes (name, category, description, diet type).
2. **Feature Vectorization**: Apply `TfidfVectorizer(stop_words='english')`.
3. **Similarity Computation**: Compute pairwise `cosine_similarity(matrix)`.
4. **Ranking**: Sort foods in descending similarity order and return top-$N$ recommendations.
