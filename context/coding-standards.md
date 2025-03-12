# Coding Standards & Best Practices

## Overview

This guide is written in the spirit of [Google Style Guides](https://github.com/google/styleguide), especially the most well written ones like for [Obj-C](https://github.com/google/styleguide/blob/gh-pages/objcguide.md).

Coding style guides are meant to help everyone who contributes to a project to forget about how code feels and easily understand the logic.

These are guidelines with rationales for all rules. If the rationale doesn't apply, or changes make the rationale moot, the guidelines can safely be ignored.

## Development Environment

### Shell Standards

PowerShell Core 7+ is our standard shell environment. All scripts and commands should use PowerShell syntax:

```powershell
# Directory operations
New-Item -ItemType Directory -Path "new-directory"
Copy-Item -Path "source" -Destination "target" -Recurse
Remove-Item -Path "to-remove" -Recurse

# Environment variables
$env:NODE_ENV = "development"

# Path operations
Join-Path -Path "dir1" -ChildPath "dir2"
```

**Rationale**: PowerShell provides better Windows integration and consistent behavior across our development environment.

## General Principles

### Consistency is king

Above all other principles, be consistent.

If a single file all follows one convention, just keep following the convention. Separate style changes from logic changes.

**Rationale**: If same thing is named differently (`Apple`, `a`, `fruit`, `redThing`), it becomes hard to understand how they're related.

### Readability above efficiency

Prefer readable code over fewer lines of cryptic code.

**Rationale**: Code will be read many more times than it will be written, by different people. Different people includes you, only a year from now.

### All code is either obviously right, or non-obviously wrong

Almost all code should strive to be obviously right at first glance. It shouldn't strike readers as "somewhat odd", and need detailed study to read and decipher.

**Rationale**: If code is obviously right, it's probably right. The goal is to have suspicious code look suspiciously wrong and stick out like a sore thumb.

*Corollary*: Code comments are a sign that the code isn't particularly well explained via the code itself. While not explicitly disallowed, strive to make code require almost no comments.

### Boring is best

Make your code the most boring version it could be.

**Rationale**: The goal of production code is NOT to have the smartest code that only geniuses can figure out, but that which can easily be maintained.

### Split Implementation from Interface

Storage, presentation, and communication protocols should always be separate.

**Rationale**: Different layers have different uses. Tying things to the wrong layer leads to unintentional breakages.

### Interface Design Principles

1. **Easy to Use Correctly, Hard to Use Incorrectly**

   ```typescript
   // Bad
   function processFile(file: string) {
     // Caller needs to remember to close the file
   }

   // Good
   function processFile(file: string) {
     return using file = openFile(file); // Resource automatically closed
   }
   ```

2. **Fail Fast and Report Actionable Errors**

   ```typescript
   // Bad
   throw new Error('Invalid input');

   // Good
   throw new Error(
     `Invalid project status "${status}". Must be one of: ${Object.values(ProjectStatus).join(', ')}`
   );
   ```

3. **Minimize Mutability**

   ```typescript
   // Bad
   interface ProjectConfig {
     name: string;
     settings: Record<string, any>;
   }

   // Good
   interface ProjectConfig {
     readonly name: string;
     readonly settings: Readonly<Record<string, any>>;
   }
   ```

## Coding Guidelines

### Naming Conventions

#### Variables should be named semantically

Names should reflect their content and intent. Use specific, descriptive names. Only use well-known abbreviations.

```typescript
// Bad
input = "123-4567"
dialPhoneNumber(input) // unclear whether this makes semantic sense

// Good
phoneNumber = "123-4567"
dialPhoneNumber(phoneNumber) // more obvious that this is intentional

// Bad
text = 1234
address = "http://some-address/patient/" + text  // why is text being added?

// Good
patientId = 1234
address = "http://some-address/patient/" + patientId // clearly adding an ID
```

#### Always add units for measures

Time and measurements should be explicit:

- Time intervals: `timeoutSec`, `timeoutMs`, `refreshIntervalHours`
- Timestamps: `startTimestamp`, `createdAtTimestamp`
- Computer space: `sizeMb`, `limitGb`
- Currency: `amountUsd`, `priceInCents`

```typescript
// Bad
const timeout = 5000 // What unit?
const size = 250 // Bytes? KB? MB?

// Good
const timeoutMs = 5000
const sizeInMb = 250
```

### Constants

#### Literal values should be constants

Every string or numeric literal should be assigned to a descriptively named constant.

**Exceptions**: Identity values like `0`, `1`, `-1`, `""`

```typescript
// Bad
if (status === 'in_progress') {
  timeoutMs = 1000 * 60 * 5 // Magic numbers
}

// Good
const STATUS_IN_PROGRESS = 'in_progress'
const FIVE_MINUTES_MS = 1000 * 60 * 5

if (status === STATUS_IN_PROGRESS) {
  timeoutMs = FIVE_MINUTES_MS
}
```

### Documentation

#### TODO and FIXME Comments

Use these to mark code that needs attention:

```typescript
// TODO(JIRA-123): Add error handling for network failures
// FIXME: This is a temporary workaround, must be fixed before production
```

- `TODO`: Future improvements or additions
- `FIXME`: Critical issues that must be addressed

## Testing Guidelines

### Test Structure

1. **Small, Focused Tests**

   ```typescript
   // Bad
   it('handles all project operations', () => {
     // 100 lines testing everything
   })

   // Good
   it('creates a new project', () => {
     // 10 lines testing project creation
   })

   it('updates project status', () => {
     // 10 lines testing status update
   })
   ```

2. **Descriptive Test Names**

   ```typescript
   // Bad
   describe('project', () => {
     it('works', () => {})
   })

   // Good
   describe('ProjectCard', () => {
     it('displays project title in header', () => {})
     it('shows error state when project fails to load', () => {})
   })
   ```

3. **Test Data Guidelines**

   ```typescript
   // Bad
   const testId = "12345" // Looks like real data
   const testName = "x" // Too vague

   // Good
   const TEST_PROJECT_ID = "test-project-id"
   const TEST_PROJECT_NAME = "Test Project Name"
   ```

### Avoid "Spooky Action at a Distance"

Keep related test logic together:

```typescript
// Bad
const projectId = "test-id";
createProject();
// ... 50 lines of other test code ...
updateProject();
expect(getProject()).toHaveStatus("completed"); // Why completed?

// Good
const projectId = "test-id";
const initialStatus = "planning";
const finalStatus = "completed";

createProject({ status: initialStatus });
updateProject({ status: finalStatus });
expect(getProject()).toHaveStatus(finalStatus);
```

## Project Structure

```file-structure
constructiv-ai/
├── .github/              # GitHub Actions and workflows
├── app/                  # Next.js App Router directory
│   ├── (auth)/          # Authentication routes group
│   │   ├── login/
│   │   ├── register/
│   │   └── layout.tsx
│   ├── (dashboard)/     # Dashboard routes group
│   │   ├── projects/
│   │   ├── documents/
│   │   ├── tasks/
│   │   └── layout.tsx
│   ├── api/            # API routes
│   │   ├── auth/
│   │   ├── documents/
│   │   ├── projects/
│   │   ├── tasks/
│   │   ├── ai/
│   │   └── webhooks/
│   └── layout.tsx
├── components/         # React components
│   ├── auth/          # Authentication components
│   ├── dashboard/     # Dashboard specific components
│   ├── documents/     # Document management components
│   ├── forms/         # Reusable form components
│   ├── layouts/       # Layout components
│   ├── projects/      # Project management components
│   ├── tasks/         # Task management components
│   ├── ui/           # UI components (shadcn)
│   └── shared/       # Shared components
├── config/           # Configuration files
│   ├── ai.ts        # AI configuration
│   ├── auth.ts      # Auth configuration
│   ├── navigation.ts # Navigation configuration
│   └── site.ts      # Site-wide configuration
├── hooks/           # Custom React hooks
│   ├── auth/        # Authentication hooks
│   ├── data/        # Data fetching hooks
│   └── ui/          # UI-related hooks
├── lib/            # Utility libraries
│   ├── supabase/   # Supabase client & utilities
│   ├── ai/         # AI utilities
│   ├── utils/      # General utilities
│   └── validations/ # Validation schemas
├── public/         # Static files
│   ├── fonts/
│   └── images/
├── styles/         # Global styles
├── types/          # TypeScript types
└── projectdocs/    # Project documentation
```

## Frontend Development

### React/Next.js Standards

#### Component Structure

```typescript
// components/projects/ProjectCard.tsx
import { type FC } from 'react'
import { type Project } from '@/types'

interface ProjectCardProps {
  project: Project
  onSelect?: (id: string) => void
}

export const ProjectCard: FC<ProjectCardProps> = ({
  project,
  onSelect
}) => {
  return (
    // Component JSX
  )
}
```

#### Custom Hooks

```typescript
// hooks/data/useProjects.ts
import { useQuery } from '@tanstack/react-query'
import { type Project } from '@/types'

export const useProjects = () => {
  return useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: async () => {
      // Fetch logic
    }
  })
}
```

### TypeScript Guidelines

```typescript
// types/projects.ts
export interface Project {
  id: string
  name: string
  description: string
  status: ProjectStatus
  createdAt: Date
  updatedAt: Date
}

export enum ProjectStatus {
  PLANNING = 'planning',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}
```

## Testing Standards

### Test File Structure

```typescript
// __tests__/components/ProjectCard.test.tsx
import { render, screen } from '@testing-library/react'
import { ProjectCard } from '@/components/projects/ProjectCard'

describe('ProjectCard', () => {
  it('renders project details correctly', () => {
    const project = {
      id: '1',
      name: 'Test Project',
      // ... other fields
    }
    
    render(<ProjectCard project={project} />)
    expect(screen.getByText('Test Project')).toBeInTheDocument()
  })
})
```

## Documentation Requirements

### Component Documentation

```typescript
/**
 * Displays a project card with basic project information
 * @param project - The project data to display
 * @param onSelect - Optional callback when project is selected
 */
export const ProjectCard = ...
```

### API Documentation

```typescript
/**
 * @api {get} /api/projects Get all projects
 * @apiName GetProjects
 * @apiGroup Projects
 * @apiSuccess {Project[]} projects List of projects
 */
```

## Version Control

### Branch Naming

- Feature branches: `feature/project-cards`
- Bug fixes: `fix/project-status`
- Releases: `release/1.0.0`

### Commit Messages

```commit messages
feat(projects): add project card component
fix(auth): resolve login redirect issue
docs(api): update project endpoints documentation
```

## Security Guidelines

### Data Validation

```typescript
import { z } from 'zod'

export const ProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  status: z.enum(['planning', 'in_progress', 'completed'])
})
```

### Authentication

```typescript
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })
  await supabase.auth.getSession()
  return res
}
```

## Performance Considerations

### Code Splitting

```typescript
// Use dynamic imports for large components
const ProjectAnalytics = dynamic(() => 
  import('@/components/projects/ProjectAnalytics'),
  { ssr: false }
)
```

### Caching Strategy

```typescript
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 30 * 60 * 1000 // 30 minutes
  })
}
```
