# **AI Application Development: Optimized Worksheet**

This document merges the **12-step outline** with the **Initial Prompt for LLM & Question Set** to create a **single, streamlined** approach for gathering requirements and generating all project documentation. The result is an **iterative**, **flexible**, and **well-structured** methodology that you can use to plan and build your app with AI assistance.

## Project Variables Registry

This registry tracks key variables across all steps. Each variable is documented with its source, current value, and last update.

| Variable Name           | Source Step | Current Value | Last Updated |
|------------------------|-------------|---------------|--------------|
| [product_name]         | Step 1      | -            | -           |
| [target_audience]      | Step 2      | -            | -           |
| [core_features]        | Step 3      | -            | -           |
| [tech_stack]           | Step 6      | -            | -           |
| [ai_integration_type]  | Step 8      | -            | -           |

## How to Use This Worksheet

1. Move Sequentially through each step—start with defining your project goals, then proceed to user needs, features, and so on.
2. Update the Project Variables Registry at each step with new information.
3. Generate Artifacts at each step using the standardized templates provided.
4. Use version control (e.g., Git) to track changes with consistent commit messages.
5. Validate completion of each step using the provided checklists.
6. Migrate this outline into your Next.js application once you're satisfied.

## Standardized Templates

### Document Template

```markdown
# [Document Title]

## Project Variables Used
${List variables from registry used in this document}

## Content
1. [Section 1]
2. [Section 2]

## Version History
| Version | Date | Changes |
|---------|------|---------|
| v1.0    | -    | Initial |
```

### Version Control Template

```text
feat(step-X): Add [document_name]
- Added variables: [var1], [var2]
- Updated registry
- Completed validation checklist
```

## Validation Gates

### Pre-Step Validation

Before starting each step:

1. Confirm all previous step variables are in registry
2. Review dependencies on previous artifacts
3. Check for any blocking issues

### Post-Step Validation

After completing each step:

1. Update Project Variables Registry
2. Verify all required artifacts are generated
3. Run through artifact quality checklist:
   - [ ] Uses standardized template
   - [ ] References all relevant variables
   - [ ] Includes version history
   - [ ] Has clear next steps
4. Create Git commit with standardized message

## Artifact Structure

### Required for Every Step

```markdown
docs/
├── step-${step_number}/
│   ├── README.md           # Step summary
│   ├── variables.md        # Variables added/updated
│   └── artifacts/          # Step-specific documents
└── registry.md            # Master variables registry
```

### Example for Step 1 (Project Vision)

```markdown
docs/step-01/
├── README.md              # Step 1 overview
├── variables.md           # product_name, target_market
└── artifacts/
    ├── vision.md         # Project vision document
    └── goals.md          # Project goals document
```

## AI Collaboration Protocol

### AI Interaction Guidelines

1. **Variable-Aware Prompting**
   - Always reference existing variables from registry in prompts
   - Use consistent variable naming across conversations
   - Document new variables discovered during AI interactions

2. **Context Preservation**

   ```markdown
   conversation-context/
   ├── step-${step_number}/
   │   ├── prompts.md        # AI prompts used
   │   ├── decisions.md      # Key decisions made
   │   └── variables.md      # Variables discussed
   ```

3. **Decision Documentation**
   - Record all significant AI-suggested decisions
   - Note alternatives considered
   - Document rationale for choices
   - Track impact on project variables

4. **Quality Assurance**
   - AI suggestions should reference existing variables
   - Validate AI outputs against project requirements
   - Ensure consistency with previous decisions
   - Flag potential conflicts or inconsistencies

### Construction Industry Context

For Constructiv AI's specific needs:

- Focus on construction workflow terminology
- Map technical concepts to construction analogies
- Prioritize practical, industry-specific examples
- Consider integration with existing construction tools

Example Mapping:

- Project Variables → Building Specifications
- Validation Gates → Building Inspections
- Artifact Structure → Blueprint Organization
- Version Control → Change Order Management

---

## **1. Overview of the Merged Approach**

### **Goal**

- Provide a **step-by-step** framework for building an app with AI
- Integrate **iterative Q&A** with **document generation**
- Maintain a **version-controlled** set of Markdown files that describe every aspect of the application

### **Core Idea**

1. **Session Zero**: Introduce the project idea, process, and rules.
2. **Iterative Q&A**: Use the **13-section question set** (from the "Initial Prompt for LLM") in **smaller batches**. After each batch, generate the corresponding docs.
3. **Map Questions to the 12 Steps**: Each major step in the 12-step outline references and clarifies relevant questions from the big question list.
4. **Document Generation**: Produce final `.md` files—PRD, frontend, backend, user-flow, third-party-libraries, etc.—as you progress.
5. **Version Control & Final Handoff**: Commit changes and finalize the docs in a structured folder.

---

## **2. High-Level Workflow**

Below is the **merged** flow, showing how the question bank (A) ties into the 12-step outline (B). You'll cycle through smaller Q&A segments, then produce the relevant docs, ensuring **iterative** development.

### **A. "Session Zero" – Introduction**

1. **Explain the Process**
   - Present the user with the "Initial Prompt for LLM" instructions:
     - *You are a Senior Technical Project Planning Assistant…*
     - *We will gather information in small Q&A sessions…*
     - *We will generate documents in Markdown format at each milestone.*
   - **Ask** the user for a brief **app idea** (the first question from the set: *"Can you describe your app idea in detail? What problem are we solving or opportunity are we pursuing?"*).
2. **Confirm** or **Refine** the user's initial response.
   - If the user's idea is unclear, ask follow-ups until you have **enough clarity** to proceed.

> **Outcome**: You now have a basic sense of the app's purpose.

---

### **B. Step 1: Clarify the Project Vision & Goals**

AI Prompt: "Please describe the [goal/intended outcome] of this project. Include any specific [features, functionality, or user experience] you envision. For context, this is for [product name or category]."

- **Relevant Questions** from the question set:
  - 1. App Idea & Scope
    - Q1: *"Can you describe your app idea in detail? What problem does it solve, and who is it for?"*
    - Q2: *"What are the high-level objectives or outcomes?"*
    - Q3: *"Who is the target market/industry?"*
    - Q4: *"How does AI fit into this vision?"*
    - Q5: *"Who are the primary users of your app? Describe their demographics, goals, and pain points."*
    - Q6: *"What are the main features? List them in order of priority."*
    - Q7: *"Will this be mobile, web, or both?"*
    - Q8: *"Desired timeline?"*

- **AI Action**:
  1. Ask these questions (one at a time).
  2. Gather answers.
  3. If answers are unclear, prompt for follow-ups.

- **Document Generated**:
  - **Product Requirements Document (PRD)** (version 1)
    - Include the app's vision, goals, features overview, timeline, and assumptions.

- **Version Control**:
  - Commit as `docs/prd.md` or `docs/product/prd.md` (whichever structure you prefer).
  - Tag as `v1.0`.

---

### **C. Step 2: Define User Needs & Target Audience**

- **(Though we partially covered audience needs in the prior step, we can go deeper here.)**

AI Prompt: "Who are the [primary users] of this project? What [problems, needs, or pain points] are they experiencing that this [product/app/service] will solve?"

- **Relevant Questions**:
  - Q2 (Target Audience, more detail)
  - Q5 (Timeline, if not fully defined)
  - Q3 (Key Features) can be revisited

- **AI Action**:
  1. Ask for more context on user personas, pain points, usage scenarios.
  2. Incorporate clarifications into the PRD or create a separate **"User Personas"** doc.

- **Document Generated**:
  - Update the **PRD** with more user-focused details: demographics, motivations, pain points.
  - Or create `docs/product/user-personas.md`.

- **Version Control**:
  - Commit as new version or a separate doc.

---

### **D. Step 3: Brainstorm & Prioritize Features**

- **Relevant Questions** (revisited):
  - Q3: *"What are the main features of your app?"* (We can refine priorities now.)
  - Q1–Q5 might be rechecked for missed details.

- **AI Action**:
  1. Ask for further details on each feature.
  2. Possibly reference other question sections (e.g., Q15 on 3rd-party APIs) if relevant for feature sets.

- **Document Generated**:
  - Update the **PRD** with a thorough "Features" section:
    - *Core Features*, *Differentiators*, *Future Add-Ons*
  - Could also create a dedicated `docs/product/feature-list.md` if desired.

---

### **E. Step 4: Map User Journeys & Workflows**

- **Relevant Questions**:
  - In the original question set, see "User Flow" section (especially Q1–Q5 in that block):
    - *User Onboarding?*
    - *Core User Journey?*
    - *Page Interactions?*
    - *Edge Cases?*
    - *Alternative Flows?*

- **AI Action**:
  1. Ask each "User Flow" question in small chunks.
  2. Confirm how each flow interacts with the app's features.

- **Document Generated**:
  - **`docs/product/user-flow.md`** or equivalent
    - Could include a **Mermaid diagram** for visualizing the steps.

- **Version Control**:
  - Tag the doc as v1.0 or combine with the PRD if that's simpler.

---

### **F. Step 5: Design Data Flows & Architecture**

- **Relevant Questions**:
  - "Backend" section: Q11, Q12, Q14
  - "Database" section: Q20, Q21
  - "API Communication" section: Q24, Q25
  - Possibly "Performance Optimization" if user has concerns about data throughput

- **AI Action**:
  1. Confirm backend framework, database type, API style (REST vs. GraphQL).
  2. Create an outline for data flow, including requests, responses, and concurrency.

- **Document Generated**:
  - A **data-flow** or **architecture** doc:
    - `docs/backend/architecture.md`
    - `docs/backend/api-specs.md` (if you want to detail endpoints now)

---

### **G. Step 6: Define Project Structure & Tech Stack**

- **Relevant Questions**:
  - Check all "Frontend" + "Backend" + "DevOps" sections:
    - Q6 (UI framework), Q7 (UI library), Q11 (Backend framework), Q28 (Hosting), Q29 (CI/CD)
  - Also check "State Management" section if relevant to your front-end structure.

- **AI Action**:
  1. Ask the user what frameworks/libraries they prefer; if they don't know, suggest default solutions (e.g., Next.js, React, Node.js with Express, etc.).
  2. Document the chosen stack, folder structure, environment strategy.

- **Document Generated**:
  - **Frontend** doc: `docs/frontend/architecture.md`
  - **Backend** doc (if not already started): `docs/backend/architecture.md`
  - Possibly a top-level `README.md` summarizing the chosen tech stack.

---

### **H. Step 7: Database & Schema Design**

- **Relevant Questions**:
  - "Database" (Q20–Q23), plus "Backend" details if needed.
  - If advanced or special DB features: indexing (Q21), migrations (Q22), backups (Q23).

- **AI Action**:
  1. Gather details on entity relationships, indexing needs, etc.
  2. Generate initial schema or diagram.

- **Document Generated**:
  - `docs/backend/database-schema.md`
  - Migrations approach mentioned in doc or code snippet references.

---

### **I. Step 8: AI Integration & Prompt Refinement**

- **(If this app includes AI features; if not, skip or adapt accordingly.)**

- **Relevant Questions**:
  - Third-party integrations (Q15) if you're using external AI APIs, or your own custom AI.
  - "Third-Party Libraries" (final section) if you're using NLP, Vision, or other ML services.
  - Any specialized questions from the user about model usage, prompt engineering, etc.

- **AI Action**:
  1. Confirm how AI fits: do we have a "model-integration.md," or is it purely 3rd-party calls?
  2. Outline prompts or workflows for AI-based functionality.

- **Document Generated**:
  - If AI is central: `docs/ai/prompt-engineering.md`
  - If minimal: mention AI in `docs/backend/api-specs.md` under "external calls."

---

### **J. Step 9: Testing & QA Strategy**

- **Relevant Questions**:
  - "Testing" (Q32–Q35): unit, integration, E2E, manual.
  - Possibly "DevOps" again for continuous testing in CI.

- **AI Action**:
  1. Clarify how thorough testing needs to be.
  2. Suggest frameworks (Jest, Cypress, etc.) based on user skill or preference.

- **Document Generated**:
  - `docs/testing/strategy.md` (include coverage goals, tool choices, test structure).

---

### **K. Step 10: Documentation & Project Management**

- **Relevant Questions**:
  - "Documentation" (Q36–Q39)
  - "DevOps" (Q30, Q31) if relevant to how you manage docs or releases.

- **AI Action**:
  1. Decide on API documentation style (OpenAPI?), code comments, readme structure.
  2. Possibly formalize a project management approach if the user wants that.

- **Document Generated**:
  - Additional docs: `docs/README.md` or `docs/development/…`
  - Enhanced API docs: `docs/backend/api-specs.md`
  - Final structure is now fairly complete.

---

### **L. Step 11: Performance, Security & Deployment**

- **Relevant Questions**:
  - "Security" (Q40–Q43)
  - "Performance Optimization" (Q44–Q46)
  - "DevOps" (Q28–Q31) if not already fully covered

- **AI Action**:
  1. Address deployment environment, scaling strategy, environment variable handling, etc.
  2. Document caching or load balancing if needed.

- **Document Generated**:
  - `docs/security/auth.md`, `docs/security/authorization.md`, `docs/performance/frontend-opt.md`, etc.
  - `docs/devops/deployment.md` for hosting details.

---

### **M. Step 12: Iteration & Maintenance**

- **Relevant Questions**:
  - Re-ask or clarify any questions that changed mid-project.
  - Possibly mention final user-flow changes or new features.

- **AI Action**:
  1. Gather final user feedback or pivot points.
  2. Update docs as needed.

- **Document Generated**:
  - This is essentially a **review cycle**, so you might update multiple docs.
  - Final step: produce a clean `third-party-libraries.md` if not done already.

---

## **3. Third-Party Libraries Document**

- **Why**

- As mandated by your initial instructions, we must maintain a file describing libraries used.

- **When**

- Each time you identify a new tool or service in the Q&A (e.g., "We'll use Stripe for payments," "We'll integrate SendGrid for emails"), add an entry to `docs/third-party-libraries.md`.

- **Structure**

```markdown
# Third-Party Libraries

- **Library**: <Name>
  - **Purpose**: <Brief usage explanation>
  - **License**: <If relevant>
  - **Integration Steps**: <Install instructions, config notes>

**Where**   
- In the final folder structure, place it at `docs/third-party-libraries.md` or inside `docs/integrations/third-party-libraries.md`.

## **4. Final Output Folder Structure**

Below is a simpler variation (you can expand if you want subfolders like `docs/backend`, `docs/frontend`, etc.):
**Example**
project-name/
├── docs/
│   ├── prd.md                       # Product Requirements Document
│   ├── backend.md                   # Backend architecture + API design
│   ├── frontend.md                  # Frontend architecture + UI approach
│   ├── user-flow.md                 # Flow diagrams, user steps
│   ├── testing.md                   # Testing strategy
│   ├── database-schema.md           # DB schema design
│   ├── third-party-libraries.md     # External libraries doc
│   └── security-and-deployment.md   # Any security/performance/deployment notes
└── README.md
Where each .md file is generated at the end of a major Q&A cycle (or updated if the Q&A cycle refined prior docs).

## **5. Notes for Effective Iteration**

1. **Ask One Question at a Time**
    - Helps the user focus on short answers.
    - Improves clarity—AI or user can quickly identify missing details.
2. **Check for Understanding**
    - If the user is unsure about a technical aspect, propose defaults or best practices based on their use case.
3. **Version Control Everything**
    - Each doc or doc update is a commit with a clear message, e.g. `git commit -m "Add user-flow.md after Q&A on user journey"`
4. **Allow Mid-Project Pivots**
    - If the user changes direction (e.g., switches DBs from PostgreSQL to MongoDB), revisit the relevant question subset.
    - Update the docs, commit the changes, and re-tag them accordingly.
5. **End with a Final Handoff**
    - The user receives a structured folder with all docs, plus any code scaffolding if the AI is generating code in parallel.
