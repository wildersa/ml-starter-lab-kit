# Access roles and Lab Runtime boundaries

## Status

This document records cross-cutting architectural constraints that the Learning Portal design must now treat as **ADOPTED**.

These constraints apply before detailed API, database, runner, or deployment contracts are frozen.

---

# 1. Portal and Lab Runtime are separate responsibilities

The Learning Portal and the Lab Runtime must be designed as separate architectural responsibilities even when they are installed on the same machine.

The distinction is conceptual first and deployment-specific second.

## Portal / control plane

Owns product and learning state such as:

- authentication and authorization;
- learner identity and profile;
- curriculum/content delivery;
- Skill Graph and navigation;
- learner progress, mastery, review, notes and evidence records;
- activity orchestration;
- recommendations;
- runtime/session requests;
- presentation of execution results;
- administration/content-authoring capabilities when those are introduced.

The Portal must not require direct access to an arbitrary learner Python process or project filesystem in order to render the normal learning experience.

## Lab Runtime / execution plane

Owns execution-sensitive responsibilities such as:

- executing learner Python/code/data/ML workloads;
- allocating and enforcing execution resources;
- environment/dependency resolution;
- controlled access to project files and datasets when explicitly granted;
- producing structured execution outputs and artifacts;
- runtime-local adapters needed to inspect or act on a generated project;
- execution timeout/cancellation;
- isolation/sandboxing appropriate to the deployment model;
- cleanup of sessions/workspaces.

The Runtime must not become the authority for learner progression, permissions, curriculum, mastery, or product navigation.

## Architectural consequence

The Portal communicates with a Runtime through a stable capability/session boundary.

Conceptually:

```text
                 PORTAL / CONTROL PLANE

Browser
  |
  v
Web Portal / Learning API
  |
  +--> identity / authorization
  +--> content / Skill Graph
  +--> learner state / notes / mastery / review
  +--> evidence orchestration
  |
  +------ runtime request / session capability ------+
                                                     |
                                                     v
                 LAB RUNTIME / EXECUTION PLANE

                                             Runtime endpoint/agent
                                               |
                                               +--> Python execution
                                               +--> datasets/project files
                                               +--> ML dependencies
                                               +--> execution artifacts
                                               +--> runtime-local project adapter
```

The physical topology may change without collapsing these responsibilities.

---

# 2. Same boundary for local, SaaS and hybrid deployment

The Portal/Runtime split is not only a future SaaS concern.

## Local mode

Both can run on one computer, but they should remain separate processes/services/modules with an explicit boundary.

A local installation may look like:

```text
local Portal
   |
   v
local Runtime
   |
   v
local generated project / Python environment
```

The local Portal should not rely on importing execution internals directly merely because they are available on the same machine.

## SaaS mode

The hosted Portal remains the control plane. Execution occurs in an isolated runtime allocated to the learner/session/activity.

```text
hosted Portal
   |
   v
runtime broker/session boundary
   |
   v
isolated hosted Lab Runtime
```

The Portal application process must never execute arbitrary learner code.

## Hybrid mode

A hosted Portal may connect to a learner-controlled local Runtime/agent when work must occur against a local generated project or private dataset.

```text
hosted Portal
   |
   v
scoped authenticated connection
   |
   v
local Lab Runtime/agent
   |
   v
local project/data
```

This topology must not require uploading the project or dataset to the Portal by default.

---

# 3. Runtime capability model

The Portal should request **capabilities**, not assume one concrete runtime implementation.

Examples of eventual runtime capabilities may include:

- Python execution;
- DataFrame execution/inspection;
- chart/artifact production;
- model training/evaluation;
- access to a connected project;
- access to a named dataset;
- package/environment metadata;
- controlled file read/write where explicitly allowed.

The exact protocol belongs to Portal Stage `P2-S5`.

Until then, design work should preserve the possibility that the runtime is:

- local;
- hosted;
- remote;
- short-lived;
- containerized;
- attached to a generated project;
- unavailable for activities that do not require execution.

A Portal surface should therefore degrade gracefully when no Runtime is connected unless that specific activity fundamentally requires execution.

---

# 4. Project Adapter placement

Project access is execution-sensitive.

The Portal may own product-level project metadata such as:

- that a project is connected;
- project display name;
- declared capabilities;
- safe metadata returned by the runtime;
- transfer opportunities.

Direct project filesystem/environment inspection should occur through the Lab Runtime or a runtime-local Project Adapter rather than by giving the Portal process unrestricted filesystem access.

This is especially important for hybrid/SaaS deployment.

---

# 5. Access profiles and separation of duties

The first design should not assume that every authenticated user has the same responsibilities.

Authorization must be enforced by the backend/service boundary; hiding UI elements is not sufficient security.

The role model may evolve, but the architecture must support at least these responsibility classes.

## Learner

Primary product user.

May:

- consume published learning content;
- maintain own notes/progress/mastery/review state;
- start permitted learning/runtime sessions;
- run permitted lab activities;
- connect/use own projects or datasets according to policy;
- inspect own execution artifacts and evidence.

Must not implicitly receive content-authoring or platform-administration privileges.

## Content Author / Maintainer

Owns educational material rather than learner execution.

May eventually:

- create/edit/version curriculum content;
- define activities/checkpoints/reference material;
- validate draft content;
- submit/publish content according to governance.

This role should not automatically grant access to arbitrary learner projects, learner code, private datasets, or runtime sessions.

## Platform Administrator / Operator

Owns platform configuration and operations.

May eventually:

- configure runtime policies and deployment settings;
- manage platform-level access/policies;
- inspect service health/operational metadata;
- perform administrative maintenance.

Administrative privilege must not imply unrestricted pedagogical impersonation or routine access to learner project contents unless a separately authorized support/audit flow requires it.

## Reviewer / Instructor / Mentor

This is a possible later role, not required for the first local release.

If introduced, its permissions must be explicit, for example:

- view assigned learner progress/evidence;
- provide feedback;
- inspect submitted artifacts specifically shared for review.

It should not inherit broad platform-admin or content-author privileges by convenience.

---

# 6. Authorization dimensions

Do not reduce authorization to one global role string.

The eventual access model should be able to reason across dimensions such as:

- actor/user;
- role/responsibility;
- tenant/workspace when SaaS/multi-user exists;
- learner ownership;
- project ownership/access grant;
- runtime session ownership;
- content publication state;
- activity/runtime capability;
- administrative scope.

The exact RBAC/ABAC model is deferred, but the data model and Portal IA must not assume single-user global access forever.

---

# 7. Runtime identity and least privilege

A Runtime session should execute with a scoped identity/capability appropriate to one learner/session/project rather than reusing a broad Portal application identity.

Future contracts should support:

- session ownership;
- expiration;
- capability scope;
- project/dataset scope;
- cancellation/revocation;
- resource policy;
- audit/provenance of execution requests and returned artifacts.

The Runtime should receive only the minimum context needed to execute the requested activity.

---

# 8. Learner data and multi-user readiness

Local-first persistence may still use SQLite, but application semantics must preserve ownership boundaries.

Learner-specific records should conceptually belong to an actor/learner even when the first release has only one local user.

Examples:

- notes;
- attempts;
- mastery;
- evidence;
- review history;
- achievements;
- project/runtime associations.

This avoids making a future SaaS version require a semantic rewrite from global state to per-user state.

A local single-user mode may use an implicit local learner identity, but it should be treated as an implementation convenience rather than a different learning model.

---

# 9. Effect on the current Portal plan

The already completed Portal IA packages remain useful because they describe the learner-facing experience.

They should now be interpreted as the **Learner view** of the Portal unless explicitly stated otherwise.

The Portal plan must additionally account for:

- authentication/identity entry states where relevant;
- authorization-aware surface/action visibility;
- runtime-connected vs runtime-unavailable states;
- project access through scoped runtime/project capabilities;
- separation between learner surfaces and future author/admin surfaces;
- no assumption that Portal and Runtime share process, filesystem, deployment, or trust boundary.

No authoring/admin UI needs to be designed during `P2-S1` unless a later product decision brings it into first-release scope.

---

# 10. Effect on Portal stages

## P2-S1 — Information architecture

Every learner surface should identify when an action depends on:

- authenticated learner context;
- a permitted project;
- an available Runtime capability.

Do not design detailed auth screens or runtime protocol yet.

## P2-S2 — Workspace/interactions

Interaction designs must distinguish:

- UI-only activities;
- activities requiring Runtime execution;
- runtime unavailable/denied states.

## P2-S3 — Learner flows

Include relevant flows for:

- authentication/session recovery where product scope requires it;
- runtime connection loss/recovery;
- denied/expired project or runtime capability;
- execution cancellation.

## P2-S4 — Progress/mastery/review

Ensure learner-owned state and evidence visibility are access-aware.

## P2-S5 — Runtime interaction boundary

This stage must formalize the Portal/Runtime contract, including:

- session/capability negotiation;
- execution request/result families;
- authorization propagation;
- project/data access boundaries;
- runtime identity;
- timeout/cancellation/retry;
- local/hosted/hybrid compatibility;
- audit/provenance expectations.

## P2-S6 — First release

The implementation specification must state which roles and deployment modes are supported initially while preserving these boundaries for later expansion.

---

# 11. Architectural rules

Treat these as hard constraints unless explicitly reconsidered:

1. **Portal and Lab Runtime are separate responsibilities in every deployment mode.**
2. **Arbitrary learner code never executes inside the Portal/API application process.**
3. **Project filesystem/runtime access belongs behind a scoped Runtime/Project Adapter boundary.**
4. **Authorization is enforced server-side, not only by UI visibility.**
5. **Learner, content-authoring, and platform-administration responsibilities are distinct.**
6. **A role does not automatically inherit unrelated data/project/runtime access.**
7. **Learner state is ownership-aware even if the first local release uses one implicit learner.**
8. **The same learning/content semantics should work with local, hosted, or hybrid runtimes.**
9. **Portal UX should remain useful for activities that do not require a Runtime.**
10. **Detailed protocols and schemas remain deferred until the appropriate design stage.**
