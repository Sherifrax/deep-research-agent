# Claude Integration

This repository is configured for Claude Code integration, allowing Claude to fix issues and work on the codebase directly.

## How to Use

### From GitHub Issues
1. Create an issue describing the bug or feature request
2. Use Claude Code to reference the issue (e.g., `/code-review #1` for PR #1)
3. Claude can read the issue, implement fixes, and create PRs

### From Command Line
```bash
# Work on the repo with Claude Code
claude /code-review <branch>
```

## Permissions

Claude has read/write access to:
- Source code (read/edit)
- Git operations (commits, branches)
- Tests and documentation

## GitHub Integration

Claude can:
- Fix bugs identified in issues
- Create pull requests with solutions
- Review code changes
- Run tests locally
- Update documentation

## Best Practices

1. **Describe issues clearly** - include error messages, steps to reproduce
2. **Label issues** - use labels like `bug`, `enhancement`, `help-wanted`
3. **Reference related work** - link to related issues or PRs
4. **Test locally** - Claude will test fixes before pushing

## Environment Setup

Required for Claude operations:
- Python 3.9+
- Git configured
- Environment variables set (.env file)

See `requirements.txt` and `.env.example` for setup details.

## Support

When asking Claude to fix issues, be specific:
- What's broken and how to reproduce it
- Expected vs actual behavior
- Error messages or logs
- Relevant code snippets
