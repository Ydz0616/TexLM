# 🧭 Project To-Do Tracker

---

## 📅 Timeline Overview

| Date | Milestone | Deliverable |
|------|------------|-------------|
| **Nov 7** | First Report | Initial Report & Project Setup |
| **Nov 21** | Second Report | Progress Report (Core Features Implemented) |
| **Dec 12** | Final Week | Final Report + Presentation |

---
## 📈 Weekly Summary

### Week 1 — Nov 1 - Nov 7 (Completed)
- [x] include edited Proposal (changes highlighted w.r.t Prof's feedback)
- [x] include our AWESOME DSL grammar + project + project link in github
- [x] include week2 todos

### Week 2 — Nov 7 - Nov 14 (Core Implementation)
- [x] implement calculations (AST -> Numpy)
- [x] implement matrix to regex (Constraint Generation)
- [x] implement prompt-to-prompt for correctness (Verifier & Super-Generator)
- [ ] try small LM other than openai (Moved to Backlog)

### Week 3 — Nov 14 - Nov 21 (Refinement)
- [x] Human-in-the-loop design (Retry Logic & Manual Fallback implemented in main.py)
- [x] One-Pass Super-Generator (Reasoning + DSL)
- [ ] prepare for presentation (In Progress)

### Week 4 — Nov 21 - Nov 28 (Robustness & Demo)
**Focus: System Stability & Visualization**

- [ ] **Function Testing**:
    - [ ] Extensive testing on the functions we implemented.
- [ ] **Error Handling & Robustness**:
    - [ ] Update `evaluate.py` to catch Singular Matrix / Dimension Mismatch errors.
    - [ ] Update prompt to reject irrelevant inputs (e.g. "I want to be a carpenter").
- [ ] **Streamlit Visualization**:
    - [ ] Build `app.py` with Chat Interface.
    - [ ] Display intermediate "AI Thought" and "Verification Status".
    - [ ] Deploy to my cloud server
- [ ] **Evaluation Dataset**:
    - [ ] Create a benchmark set (30-50 examples: Simple, Nested, Adversarial).
    - [ ] Run automated tests to measure success rate.

---

## 📊 Progress Overview

| Week | Completed | Total | Progress |
|------|------------|--------|-----------|
| Week 1 | 3 | 3 | 100% |
| Week 2 | 3 | 4 | 75% |
| Week 3 | 2 | 3 | 66% |
| Week 4 | 0 | 3 | 0% |

---

## 🧱 Backlog

- [ ] Scalar Support (Determinant, Trace)
- [ ] Server Deployment
- [ ] Try small LM (Llama/Mistral)