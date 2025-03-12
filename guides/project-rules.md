# Project Rules for Constructiv AI

## 1. Development Environment Rules

---

```yaml
description: Rules for maintaining consistent development environments
applies_to: All developers and environments
priority: High
```

### Environment Setup

- Use PowerShell Core 7.4.6+ as primary shell on Windows
- Maintain Node.js LTS version (currently 22.14.0 ARM64)
- Use pnpm 9.15.3+ as package manager
- Enable Windows Developer Mode

### Architecture Considerations

- Ensure all development tools are ARM64 native where possible
- Use x64 emulation only when ARM64 versions are unavailable
- Verify native module compatibility before adding dependencies
- Monitor performance metrics for emulated tools

### IDE Configuration

- Use Cursor as primary IDE
- Enable TypeScript strict mode
- Configure ESLint and Prettier
- Set up Git hooks for pre-commit linting

### Local Development

- Run development server on default port 3000
- Use local Supabase instance for development
- Enable hot reloading
- Configure environment variables per `.env.example`

## 2. Code Architecture Rules

---

```yaml
description: Structural and architectural guidelines
applies_to: All TypeScript/JavaScript files
priority: High
```

### Project Structure

- Follow Next.js 14 App Router conventions
- Implement feature-based folder organization
- Use atomic design for components
- Maintain clear separation of concerns

### State Management

- Use Zustand for global state
- Implement React Query for server state
- Keep component state minimal
- Follow immutability patterns

### API Design

- RESTful endpoints in `app/api`
- Implement proper error handling
- Use TypeScript interfaces for requests/responses
- Follow API versioning conventions

## 3. UI/UX Development Rules

---

```yaml
description: Guidelines for consistent user interface development
applies_to: All frontend components and styles
priority: Medium
```

### Component Development

- Use shadcn/ui as component foundation
- Implement responsive design patterns
- Follow accessibility guidelines
- Maintain consistent styling

### Design System

- Use Tailwind CSS for styling
- Follow color palette definitions
- Maintain consistent spacing
- Use defined typography scale

### User Experience

- Implement loading states
- Add error boundaries
- Provide user feedback
- Ensure mobile responsiveness

## 4. Testing & Quality Assurance Rules

---

```yaml
description: Standards for testing and code quality
applies_to: All source code and test files
priority: High
```

### Testing Requirements

- Write unit tests for utilities
- Create integration tests for features
- Implement E2E tests for critical flows
- Maintain 80% code coverage

### Code Quality

- Follow TypeScript best practices
- Implement proper error handling
- Use proper typing (no `any`)
- Follow naming conventions

### Review Process

- Require peer code reviews
- Use pull request templates
- Follow semantic versioning
- Maintain changelog

## 5. Deployment & DevOps Rules

---

```yaml
description: Guidelines for deployment and operations
applies_to: All deployment and infrastructure
priority: High
```

### Deployment Process

- Use Vercel for production deployments
- Implement staging environment
- Follow GitFlow branching strategy
- Maintain deployment documentation

### Performance Requirements

- Meet Core Web Vitals thresholds
- Implement proper caching
- Enable edge functions where applicable
- Monitor API response times

### Security

- Follow security best practices
- Implement proper authentication
- Use environment variables
- Regular security audits

---

## Rule Enforcement

### Automated Enforcement

- ESLint configuration
- TypeScript compiler options
- Git hooks
- CI/CD pipelines

### Manual Enforcement

- Code review checklist
- Documentation requirements
- Performance benchmarks
- Security reviews

## Updates and Maintenance

These rules should be reviewed and updated:

- Monthly for development rules
- Quarterly for architectural decisions
- As needed for security requirements

## Questions and Clarifications

For questions about these rules:

1. Check existing documentation
2. Ask in the development channel
3. Create a discussion in GitHub
4. Update rules after team consensus
