# Agentic AI Platform for Industry 4.0 School-Factory Pilot Assistance

Engineering Project (PJE) - Weeks 1 to 3: Business Framing, Functional Analysis & Target Architecture.  
Supervisor: Esma Yahia

---

## Project Overview
This project aims to develop a modular platform connected to the industrial systems of the Industry 4.0 school-factory (TULIP, Node-RED, Shizen). The objective is to assist line managers in daily production tracking, anomaly detection, industrial diagnosis, and the proposal of concrete corrective actions.

---

## 1. Functional & Technical Architecture
The system relies on a hybrid and modular architecture ensuring robustness, scalability, and the prevention of infinite communication loops:
* Conversational Interface: A single entry point enabling users to express their needs in natural language.
* Centralized Orchestration: A deterministic orchestrator that plans and delegates tasks.
* BDI Cognitive Model (Beliefs, Desires, Intentions): The diagnostic agent updates its beliefs by querying real-time feeds before formulating an action intention.
* Agentic RAG Module: An iterative and proactive connection with the technical documentation base (procedures, manuals) to eliminate errors without re-training.

---

## 2. Business Framing & Scope
* Primary Target (MVP): Line managers, to reduce cognitive load caused by data dispersion.
* Secondary Target (Lot 2): Line operators (field assistance and future prospects for hands-free voice interaction).
* Human-in-the-Loop Approach: The system assists, diagnoses, and recommends, but the line manager retains final validation authority for all high-impact decisions.

---

## 3. Functional Analysis & Requirements (APTE)
The system is articulated around key service functions:
* FP1 / FP2: Natural language querying and automated anomaly diagnosis by cross-referencing TULIP, Node-RED, and Shizen data.
* FP3: Association of the diagnosis with internal procedures to recommend corrective actions.
* FC1 to FC5: Constraints regarding API interoperability, modularity (microservices), determinism (BDI), ergonomics, and governance (AgentOps).

---

## 4. Governance & Risk Management
| Identified Risk | Level | Mitigation Strategy |
| :--- | :--- | :--- |
| Erroneous decisions | High | Use of the BDI model to validate the actual state of the plant via API before acting. |
| Document hallucinations | Critical | Strict RAG approach with exact context injection and source traceability. |
| Multi-agent deadlocks | Medium | Selection of a centralized orchestration structure. |
| User rejection | Medium | Assistant positioning with mandatory human validation (Human-in-the-Loop). |

---

## Next Steps
- Finalize technical infrastructure and development environments.
- Develop initial API connectors for TULIP, Node-RED, and Shizen.
- Implement the document search module (RAG).
- Prototype the orchestrator and validate a first end-to-end test scenario.
