# Code Documentation Template

## Function/Method Docstring

```python
def function_name(param1: type, param2: type) -> return_type:
    """[One-line summary of function purpose]

    A more detailed description of what this function does and why it exists.
    Include any important notes about the implementation.

    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2

    Returns:
        return_type: Description of what is returned

    Raises:
        ErrorType: Description of when/why this error is raised

    Example:
        ```python
        result = function_name(param1, param2)
        ```

    Note:
        Any additional notes, caveats, or important considerations.
        For detailed documentation, see: [link to main documentation file]
    """
    pass
```

## Class Docstring

```python
class ClassName:
    """[One-line summary of class purpose]

    A more detailed description of what this class represents and how it should be used.
    Include any important notes about the implementation.

    Attributes:
        attr1 (type): Description of attr1
        attr2 (type): Description of attr2

    Example:
        ```python
        instance = ClassName(param1, param2)
        result = instance.method()
        ```

    Note:
        Any additional notes, caveats, or important considerations.
        For detailed documentation, see: [link to main documentation file]
    """

    def __init__(self, param1: type, param2: type):
        """Initialize the class.

        Args:
            param1 (type): Description of param1
            param2 (type): Description of param2
        """
        pass
```

## TypeScript/JavaScript Docstring

```typescript
/**
 * [One-line summary of function purpose]
 * 
 * A more detailed description of what this function does and why it exists.
 * Include any important notes about the implementation.
 * 
 * @param {type} param1 - Description of param1
 * @param {type} param2 - Description of param2
 * @returns {type} Description of what is returned
 * @throws {ErrorType} Description of when/why this error is raised
 * 
 * @example
 * ```typescript
 * const result = functionName(param1, param2);
 * ```
 * 
 * @note
 * Any additional notes, caveats, or important considerations.
 * For detailed documentation, see: [link to main documentation file]
 */
function functionName(param1: type, param2: type): returnType {
    // Implementation
}
```

## Usage Guidelines

1. Use this template for inline code documentation (docstrings)
2. Keep docstrings concise and focused on immediate usage
3. For detailed documentation, theory, or extensive examples:
   - Create a separate markdown file using `documentation-template.md`
   - Link to it from the docstring using relative paths
4. Follow language-specific conventions:
   - Python: Use triple quotes (`"""`)
   - TypeScript/JavaScript: Use JSDoc format (`/** */`)
   - Other languages: Adapt format while maintaining structure

## Best Practices

1. Always include:
   - One-line summary
   - Parameter descriptions
   - Return value description
   - Basic usage example
   - Link to detailed documentation (if exists)

2. Optional but recommended:
   - Type hints
   - Error descriptions
   - Important notes/caveats
   - Performance considerations

3. Keep it DRY:
   - Don't repeat extensive documentation that exists elsewhere
   - Use links to reference detailed docs
   - Focus on information needed for immediate usage

---
*Last updated: [YYYY-MM-DD]* 