# VS Code Extensions Guide

## Overview

This guide covers the essential extensions installed in our development environment, organized by category with usage tips and best practices.

## Core Development Extensions

### Code Quality & Formatting

1. **ESLint** (`dbaeumer.vscode-eslint`)
   - Purpose: JavaScript/TypeScript code linting
   - Benefits: Catches errors and enforces coding standards
   - Usage:
     - Auto-fixes on save when configured
     - View problems in Problems panel (Ctrl+Shift+M)
   - Key Commands:

     ```json
     {
       "eslint.autoFixOnSave": true,
       "editor.codeActionsOnSave": {
         "source.fixAll.eslint": true
       }
     }
     ```

2. **Prettier** (`esbenp.prettier-vscode`)
   - Purpose: Code formatting
   - Benefits: Maintains consistent code style
   - Usage:
     - Format on save
     - Format selection: Ctrl+K Ctrl+F
   - Configuration:

     ```json
     {
       "editor.defaultFormatter": "esbenp.prettier-vscode",
       "editor.formatOnSave": true
     }
     ```

### Git Integration

1. **GitLens** (`eamodio.gitlens`)
   - Purpose: Enhanced Git capabilities
   - Features:
     - Inline blame annotations
     - File & line history
     - Branch/tag comparison
   - Key Commands:
     - Alt+B: Toggle blame
     - Ctrl+Shift+G G: Open source control
     - Ctrl+Shift+G H: View file history

### Java Development

1. **Java Extension Pack** (`vscjava.vscode-java-pack`)
   - Includes:
     - Language Support (`redhat.java`)
     - Debugger (`vscjava.vscode-java-debug`)
     - Maven (`vscjava.vscode-maven`)
     - Project Manager (`vscjava.vscode-java-dependency`)
   - Key Features:
     - IntelliSense
     - Debugging
     - Project management
     - Maven/Gradle support

### Web Development

1. **Tailwind CSS** (`bradlc.vscode-tailwindcss`)
   - Purpose: Tailwind CSS IntelliSense
   - Features:
     - Class suggestions
     - Syntax highlighting
     - CSS preview

2. **Auto Rename Tag** (`formulahendry.auto-rename-tag`)
   - Purpose: Automatically rename paired HTML/XML tags
   - Usage: Just start editing one tag

### Database Development

1. **Prisma** (`prisma.prisma`)
   - Purpose: Database schema development and ORM support
   - Features:
     - Schema syntax highlighting
     - Intelligent autocomplete
     - Real-time error detection
     - Format on save for .prisma files
   - Key Commands:
     - Ctrl + Space: Trigger suggestions
     - Ctrl + .: Quick fixes
     - F12: Go to definition
   - Usage Examples:

     ```prisma
     // Schema autocompletion
     model User {
       id    Int     @id @default(autoincrement())
       email String  @unique
       // Type Ctrl + Space here for field suggestions
     }

     // Relationship suggestions
     model Post {
       id       Int    @id @default(autoincrement())
       author   User   // Ctrl + Space here for relationship types
     }
     ```

   - Best Practices:
     - Keep schema file formatted (enabled by default)
     - Use suggestions for type definitions
     - Leverage quick fixes for common patterns
     - Use hover information for documentation

### Productivity Tools

1. **Thunder Client** (`rangav.vscode-thunder-client`)
   - Purpose: API testing (Postman alternative)
   - Features:
     - Request history
     - Environment variables
     - Collection organization
   - Usage:

     ```javascript
     // Example request
     GET http://api.example.com/data
     Authorization: Bearer {{token}}
     ```

2. **Todo Tree** (`gruntfuggly.todo-tree`)
   - Purpose: Track TODOs in codebase
   - Supported tags: TODO, FIXME, BUG, HACK
   - Company Format:

     ```javascript
     // TODO[(Context)]: <Action> by/when <Deadline Condition>
     // Example:
     // TODO(PROJ-123): Implement error handling when API is ready
     // FIXME: Remove hardcoded values _(Reviewer: suggest better approach)_
     ```

   - Usage:
     - View all TODOs in Todo Tree panel
     - Click to navigate to TODO location
     - Customize colors and icons in settings

3. **Code Spell Checker** (`streetsidesoftware.code-spell-checker`)
   - Purpose: Catch typos in code and comments
   - Usage:
     - Right-click to add words to dictionary
     - Quick fixes for suggestions

### Docker & Remote Development

1. **Docker** (`ms-azuretools.vscode-docker`)
   - Purpose: Docker integration
   - Features:
     - Dockerfile intellisense
     - Container management
     - Image management

2. **Remote Development Pack**
   - Includes:
     - Remote SSH (`ms-vscode-remote.remote-ssh`)
     - WSL (`ms-vscode-remote.remote-wsl`)
     - Containers (`ms-vscode-remote.remote-containers`)
   - Usage: Click remote indicator in bottom-left

## Best Practices

### Performance Optimization

1. Disable unused extensions
2. Use workspace-specific settings
3. Configure file watching:

   ```json
   {
     "files.watcherExclude": {
       "**/node_modules/**": true,
       "**/dist/**": true
     }
   }
   ```

### Extension Management

1. Regular maintenance:

   ```bash
   # List extensions
   code --list-extensions

   # Install extension
   code --install-extension <extension-id>

   # Uninstall extension
   code --uninstall-extension <extension-id>
   ```

2. Sync settings:
   - Use Settings Sync (built-in)
   - Ctrl+Shift+P → "Settings Sync"

## Keyboard Shortcuts

Common shortcuts for installed extensions:

```markdown
General:
- Ctrl+Shift+P: Command Palette
- Ctrl+P: Quick Open File
- Ctrl+Shift+F: Search in Files

Git:
- Ctrl+Shift+G G: Source Control
- Alt+B: Toggle GitLens Blame

Code Quality:
- Ctrl+Shift+I: Format Document
- Ctrl+K Ctrl+F: Format Selection

Java:
- F5: Start Debugging
- Ctrl+F5: Run Without Debugging
- Alt+Enter: Quick Fix
```

## Troubleshooting

### Common Issues

1. Extension conflicts:
   - Check output panel (Ctrl+Shift+U)
   - Disable conflicting extensions
   - Clear extension cache

2. Performance issues:
   - Use "Developer: Show Running Extensions"
   - Disable heavy extensions when not needed
   - Check extension logs

### Maintenance Tasks

Weekly:

- Update extensions
- Review extension settings
- Clean up extension data
- Check for new recommended extensions

## Related Documentation

- See `projectdocs/context/development-environment.md` for environment setup
- See `projectdocs/guides/java-development-guide.md` for Java-specific settings
