# CLI Tools Guide

This guide documents the Command Line Interface (CLI) tools installed in our development environment and how to use them effectively in projects.

## Node.js and npm

### Installation Details

- Node.js Version: v22.14.0 (ARM64)
- npm Version: 11.1.0
- Architecture: arm64
- Installation Location: `C:\Program Files\nodejs`

### Usage

```bash
# Check versions
node -v    # View Node.js version
npm -v     # View npm version

# Package management
npm install <package>        # Install a package locally
npm install -g <package>     # Install a package globally
npm uninstall <package>      # Remove a package
npm update                   # Update packages

# Project initialization
npm init                     # Initialize a new project
npm init -y                  # Initialize with defaults
```

## Framework CLIs

### Angular CLI

- Version: 19.1.6
- Installation: Global
- Command: `ng`

```bash
# Common commands
ng new <app-name>           # Create new Angular project
ng serve                    # Start development server
ng build                    # Build the application
ng test                     # Run tests
ng generate component       # Generate new component
```

### Vue CLI

- Version: 5.0.8
- Installation: Global
- Command: `vue`

```bash
# Common commands
vue create <app-name>       # Create new Vue project
vue serve                   # Start development server
vue build                   # Build the application
vue add <plugin>           # Add a Vue CLI plugin
```

### Create React App

- Version: 5.0.1
- Installation: Global via npx
- Command: `create-react-app`

```bash
# Project creation
npx create-react-app <app-name>                    # Create new React project
npx create-react-app <app-name> --template typescript  # Create with TypeScript
```

## UI Component CLIs

### shadcn/ui

- Access: Via npx (recommended approach)
- Usage: Project-specific (not global)

```bash
# Initialize in a project
npx shadcn@latest init     # Initialize shadcn in a project

# Add components
npx shadcn@latest add button    # Add button component
npx shadcn@latest add card      # Add card component

# Check for updates
npx shadcn@latest diff         # Check for component updates

# Get project information
npx shadcn@latest info        # View project configuration
```

## Best Practices

### Version Management

- Regularly check for updates using `npm outdated -g`
- Update global packages with `npm update -g`
- Keep Node.js up to date for ARM64 compatibility

### Project Setup

1. Initialize with proper package manager:

   ```bash
   npm init -y
   ```

2. Install necessary development dependencies:

   ```bash
   npm install -D typescript @types/node
   ```

3. Add UI components as needed:

   ```bash
   npx shadcn@latest add [component-name]
   ```

### Troubleshooting

- If a CLI command isn't recognized, try:
  1. Check if it's installed: `npm list -g`
  2. Verify PATH environment variables
  3. Try using `npx` for one-time execution

## Environment Variables

Important paths to maintain:

- `C:\Program Files\nodejs`
- `%APPDATA%\npm`

## Security Considerations

- Always use trusted sources for packages
- Regularly audit dependencies: `npm audit`
- Keep CLIs updated to patch security vulnerabilities

## Additional Resources

- [Node.js Documentation](https://nodejs.org/docs)
- [npm Documentation](https://docs.npmjs.com)
- [Angular CLI Documentation](https://angular.io/cli)
- [Vue CLI Documentation](https://cli.vuejs.org)
- [Create React App Documentation](https://create-react-app.dev)
- [shadcn/ui Documentation](https://ui.shadcn.com)
