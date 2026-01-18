<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: N/A → 1.0.0 (Initial ratification)
Date: 2025-01-17

Modified Principles: N/A (Initial creation)

Added Sections:
  - Core Principles (6 principles derived from existing constitution.md)
  - Technical Standards (code quality, testing, security, performance)
  - Architecture Constraints (phase-specific rules, technology stack)
  - Governance (amendment procedure, versioning, compliance)

Removed Sections: N/A

Templates Requiring Updates:
  - .specify/templates/plan-template.md: ⚠ pending (to be created)
  - .specify/templates/spec-template.md: ⚠ pending (to be created)
  - .specify/templates/tasks-template.md: ⚠ pending (to be created)

Follow-up TODOs:
  - Create template files in .specify/templates/
  - Set up command files in .specify/templates/commands/
================================================================================
-->

# Project Constitution

**Project Name:** The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI

**Constitution Version:** 1.0.0

**Ratification Date:** 2025-01-17

**Last Amended Date:** 2025-01-17

---

## Purpose

This constitution defines the non-negotiable principles, technical standards, and architectural
constraints that govern all development decisions across all five phases of the Todo App
evolution. Every agent, developer, and contributor MUST adhere to these principles.

---

## Core Principles

### Principle 1: Spec-Driven Development

All implementation work MUST be traceable to formal specifications.

**Non-Negotiable Rules:**
- No code without specification: Every feature MUST have a corresponding entry in the spec
- No architecture without plan: System changes MUST be documented in the plan before implementation
- No implementation without tasks: Code MUST map to specific task IDs
- Iterative refinement: Specs evolve through feedback; code follows specs, not intuition

**Rationale:** Specifications provide a single source of truth, enable AI-assisted development,
and ensure all stakeholders have visibility into what is being built and why.

### Principle 2: AI-Native Development

AI agents are first-class development tools, not afterthoughts.

**Non-Negotiable Rules:**
- Claude Code First: Use Claude Code as the primary development tool
- Prompt engineering over manual coding: Refine specifications until AI generates correct output
- Reusable intelligence: Build and leverage agent skills and subagents
- Documentation as code: All architectural decisions MUST be documented in markdown

**Rationale:** AI-native development maximizes productivity and ensures consistency across
the codebase while creating reusable patterns for future work.

### Principle 3: Progressive Evolution

The project evolves through five distinct phases, each building on the previous.

**Non-Negotiable Rules:**
- Each phase builds on previous: No skipping phases; maintain backward compatibility
- Incremental complexity: Start simple (console) → end complex (distributed cloud)
- Learning through building: Each phase teaches new concepts and technologies

**Phases:**
1. Phase I: Console App (Pure Python, in-memory)
2. Phase II: Web App (FastAPI + Next.js, Neon PostgreSQL)
3. Phase III: AI Chatbot (OpenAI Agents SDK, MCP)
4. Phase IV: Local K8s (Minikube, Helm, kubectl-ai)
5. Phase V: Cloud K8s (Managed K8s, Kafka/Dapr, CI/CD)

**Rationale:** Progressive complexity ensures solid foundations and prevents over-engineering
in early phases while building toward production-grade distributed systems.

### Principle 4: Code Quality Excellence

Code MUST be clear, consistent, and maintainable.

**Non-Negotiable Rules:**
- Clarity over cleverness: Code MUST be self-documenting and easy to understand
- Consistency over individual style: Follow established patterns across the codebase
- Composition over inheritance: Favor functional composition and dependency injection
- Fail fast and loud: Use explicit error handling; NEVER silently fail
- Immutability by default: Prefer immutable data structures; mutate only when necessary
- Type safety: All code MUST use type hints (Python) or strict TypeScript

**Rationale:** High code quality reduces bugs, accelerates onboarding, and makes AI-assisted
development more effective.

### Principle 5: Security by Design

Security is a first-class concern, not a bolt-on feature.

**Non-Negotiable Rules:**
- Input validation: All user input MUST be validated at API boundaries
- Authentication: JWT tokens with short-lived access (15 min) and refresh (7 days)
- HTTPS only: All production API communication MUST use HTTPS
- No secrets in code: Use environment variables; NEVER commit secrets
- Parameterized queries: SQL injection prevention is mandatory
- Dependency scanning: Automated vulnerability scanning in CI

**Rationale:** Security vulnerabilities can be catastrophic. Building security in from the
start is far more effective than retrofitting.

### Principle 6: Test-Driven Quality

All code MUST be tested before deployment.

**Non-Negotiable Rules:**
- Unit tests: Minimum 80% coverage for business logic
- Integration tests: All API endpoints MUST have integration tests
- E2E tests: Critical user journeys MUST have end-to-end tests
- No deployment without tests: CI MUST pass all tests before merge
- Test structure: Use Arrange-Act-Assert pattern; one assertion per test

**Rationale:** Automated testing catches regressions, enables refactoring, and provides
living documentation of expected behavior.

---

## Technical Standards

### Python Standards
- Python 3.13+ required
- Type hints on all function parameters and return values
- Docstrings required for all public functions, classes, and modules
- Async/await for all I/O operations
- F-strings only (no .format() or % formatting)
- Max line length: 100 characters
- Imports grouped: standard library, third-party, local

### TypeScript/JavaScript Standards
- TypeScript 5+ with strict mode enabled
- Server Components by default; Client Components only when needed
- Named exports preferred over default exports
- Functional components only; no class components
- Tailwind CSS for styling; no inline styles or CSS-in-JS
- Max line length: 100 characters

### Database Standards
- SQLModel ORM (Pydantic + SQLAlchemy)
- Connection pooling required (5-20 connections)
- Async sessions for all operations
- All schema changes via Alembic migrations
- No N+1 queries; use eager loading

### Performance Standards
- API response time: 95th percentile < 200ms
- Lighthouse score: Minimum 90 for Performance, Accessibility, Best Practices
- First Contentful Paint: < 1.5s
- Bundle size: Main bundle < 200KB gzipped

### Accessibility Standards (WCAG 2.1 AA)
- Keyboard navigation for all interactive elements
- Screen reader support with proper ARIA labels
- Color contrast: Minimum 4.5:1 for normal text
- Touch targets: Minimum 44×44px

---

## Architecture Constraints

### Technology Stack

**Allowed:**
- Languages: Python 3.13+, TypeScript 5+, JavaScript (ES2023+)
- Frameworks: FastAPI, Next.js 15+ (App Router)
- Database: Neon Serverless PostgreSQL only
- AI: OpenAI Agents SDK, Official MCP SDK
- Cloud: DigitalOcean, Google Cloud, Azure, Oracle Cloud
- Containerization: Docker, Kubernetes (Minikube, AKS, GKE, OKE)

**Forbidden:**
- Alternative ORMs: No Prisma, TypeORM, raw SQL
- Alternative auth: No Auth0, Clerk, Supabase Auth
- Alternative AI: No LangChain, LlamaIndex, other frameworks
- Alternative databases: No MongoDB, Redis as primary DB
- Alternative K8s: No EKS, self-managed clusters

### Phase-Specific Constraints

| Phase | Constraints |
|-------|-------------|
| Phase I | Pure Python, in-memory only, single file allowed |
| Phase II | Monorepo, REST API only, Neon + Better Auth |
| Phase III | OpenAI Agents SDK, MCP SDK, stateless chat |
| Phase IV | Minikube only, Helm charts, kubectl-ai |
| Phase V | Managed K8s, Kafka, Dapr, GitHub Actions |

---

## Governance

### Amendment Procedure

1. Propose amendment via specification document
2. Document rationale and impact analysis
3. Review by project stakeholders
4. Update constitution with new version number
5. Propagate changes to dependent templates and documentation

### Versioning Policy

This constitution follows semantic versioning:
- **MAJOR:** Backward-incompatible principle removals or redefinitions
- **MINOR:** New principles added or existing guidance materially expanded
- **PATCH:** Clarifications, wording improvements, typo fixes

### Compliance Review

- Pre-commit hooks enforce code standards automatically
- CI pipeline blocks merges that violate standards
- Spec reviews verify alignment before implementation begins
- Architecture reviews verify plans align with constraints
- Code reviews ensure implementation follows standards

### Exception Policy

Deviations are allowed only when:
1. **Technically impossible:** The constraint cannot be met with available tools
2. **Spec-approved:** Deviation is documented in specification or plan
3. **Time-critical:** Deadline requires pragmatic trade-offs
4. **Documented:** Deviation is clearly documented with rationale

All deviations MUST be logged with date, reason, impact, and approval.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-17 | Initial constitution ratified |

---

## References

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Documentation](https://nextjs.org/docs)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Twelve-Factor App](https://12factor.net/)
