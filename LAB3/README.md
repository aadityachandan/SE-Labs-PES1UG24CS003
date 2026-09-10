# Lab 3 — Component Modelling & Architectural Pattern Selection
## Problem Statement #03: Campus Placement & Internship Pipeline

**Name:** AADITYA SHANKAR CHANDAN
**SRN:** PES1UG24CS003

**Architecture selected:** Microservices Architecture (over Layered and Client-Server)

### Repository Contents

| File | Deliverable |
|---|---|
| `diagrams/01_Component_Diagram.svg` | UML Component Diagram — editable source (7 components, 8 interfaces, 2 `«use»` dependencies) |
| `diagrams/01_Component_Diagram.png` | PNG render of the diagram, for quick preview |
| `diagrams/01_Component_Diagram.pdf` | PDF render of the diagram, for submission |
| `docs/02_Architectural_Justification.docx` | One-page Word justification: architectural choice, two reasons, security advantage, performance benefit |

### Diagram Preview

![Component Diagram](diagrams/01_Component_Diagram.png)

### Components (7 — minimum required was 5)
1. **API Gateway** — routing, auth, rate-limiting; exposes the external `REST API`
2. **Resume & Eligibility Service** — FR-001
3. **Application & Drive Management Service** — FR-002
4. **Interview Scheduling Service** — FR-003
5. **Offer Management Service** — FR-004
6. **Reporting & Analytics Service** — FR-005
7. **Database Component** (shared) — encrypted (AES-256) persistence layer, NFR-001

### Interfaces (8 — minimum required was 4)
| Interface | Provided by | Required by |
|---|---|---|
| `REST API` | API Gateway | External Student / Placement Officer clients |
| `IEligibilityCheck` | Resume & Eligibility Service | Application & Drive Management Service |
| `IInterviewScheduling` | Interview Scheduling Service | Application & Drive Management Service |
| `IOfferIssuance` | Offer Management Service | Interview Scheduling Service |
| `DataAccess` ×4 | Database Component | Resume & Eligibility, Application & Drive Management, Interview Scheduling, Offer Management services |
| `ReportQuery` | Database Component | Reporting & Analytics Service |

### Why Microservices
Full reasoning is in `docs/02_Architectural_Justification.docx`. In short: each of the five Functional Requirements (FR-001–FR-005) maps to one independently deployable, independently scalable service, which matters because load is highly uneven across the placement lifecycle (application deadlines spike traffic on two services; reporting stays light and steady) and because a fault in one service (e.g. Interview Scheduling) should never be able to take down the student-facing application flow.
