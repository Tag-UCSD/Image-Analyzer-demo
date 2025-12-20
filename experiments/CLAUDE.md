# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Experiments** - Prototype and experimental code directory containing early-stage features and design system experiments.

**Status:** Experimental/Prototype

**Purpose:** Houses experimental code, prototypes, and design system documentation that may be integrated into main projects or serve as reference implementations.

## Contents

### Adaptive_Preference_GUI-main/

**Adaptive Preference GUI System** - Design system and UI framework for creating consistent, accessible user interfaces.

**Location:** `Adaptive_Preference_GUI-main/Adaptive_Preference _3.5.11_Handoff/`

**Key Files:**
- Design system components
- Style guidelines
- UI patterns and templates

**Related Usage:**
- The `graphical-model/` project uses the Adaptive Preference design system
- Base CSS: `graphical-model/style_system/adaptive_preference_base.css`
- Style primer: `graphical-model/style_system/adaptive_preference_ai_style_primer.md`

### Documentation Files

**Adaptive_Preference_System_Documentation.md:**
- Comprehensive documentation for the Adaptive Preference design system
- Component library
- Usage guidelines
- Design principles

**RUNNING_THE_SYSTEM.md:**
- Setup instructions for experimental systems
- Development environment configuration
- Testing and deployment notes

## Purpose of This Directory

The `experiments/` directory serves as:

1. **Prototype Staging Area** - Test new features before integration into main projects
2. **Design System Repository** - Store design system assets and documentation
3. **Reference Implementations** - Working examples of patterns to be used in production
4. **Exploration Space** - Try new approaches without affecting stable codebases

## Relationship to Other Projects

### graphical-model

The graphical-model project actively uses the Adaptive Preference design system from this directory:
- Frontend applications use Adaptive Preference CSS
- Style guide informs UI decisions
- Design tokens may be sourced from here

### image-tagger

May reference design patterns or components from experimental work here.

### article-eater

May incorporate UI patterns or design elements tested in experiments.

## Working with Experiments

### Guidelines

1. **Experimental Nature** - Code here may be incomplete, undocumented, or unstable
2. **No Production Use** - Don't deploy experimental code directly to production
3. **Extract Patterns** - Successful experiments should be extracted and integrated into main projects
4. **Document Learnings** - Keep notes on what works and what doesn't

### Adding New Experiments

When adding experimental code:

```bash
# Create a descriptive directory
mkdir experiments/new-feature-experiment/

# Include a README
echo "# New Feature Experiment" > experiments/new-feature-experiment/README.md

# Document purpose, approach, and findings
# Include date and context
```

### Graduating Experiments

When an experiment is ready for production:

1. **Extract Core Code** - Take the stable, useful parts
2. **Integrate into Target Project** - Move to appropriate main project
3. **Document in Experiment** - Leave note about where it was integrated
4. **Keep Experiment** - Don't delete, serves as historical reference

## Commands

### Adaptive Preference System

```bash
cd Adaptive_Preference_GUI-main/Adaptive_Preference _3.5.11_Handoff/

# Follow instructions in RUNNING_THE_SYSTEM.md
```

## File Organization

```
experiments/
├── Adaptive_Preference_GUI-main/
│   └── Adaptive_Preference _3.5.11_Handoff/
│       └── COMPLETE_v3.5.11_SYSTEM/
│           ├── Design system assets
│           └── Documentation
├── Adaptive_Preference_System_Documentation.md
├── RUNNING_THE_SYSTEM.md
└── CLAUDE.md (this file)
```

## Known Contents

### Design Systems

**Adaptive Preference (v3.5.11):**
- Complete design system handoff
- CSS framework
- Component library
- Style tokens and guidelines

## Future Experiments

Potential experimental work that could land here:

- **ML Model Experiments** - Testing new prediction models
- **UI Pattern Prototypes** - New interaction patterns
- **Integration Experiments** - Connecting different systems
- **Performance Optimizations** - Testing optimization strategies
- **Alternative Architectures** - Exploring different tech stacks

## Important Notes

1. **Not for Production** - This is an experimental workspace
2. **May be Incomplete** - Code may be partial, untested, or documented poorly
3. **Subject to Change** - Experiments can be modified or removed freely
4. **Learning Space** - Focus is on exploration, not stability
5. **Extract Success** - Good experiments graduate to main projects

## Related Projects

**For production-ready design system usage, see:**
- `graphical-model/style_system/` - Production Adaptive Preference implementation
- `graphical-model/frontend/` - Frontend applications using the design system

**For stable, production-ready code, see:**
- `graphical-model/` - Bayesian causal modeling system
- `image-tagger/` - Image tagging and annotation system
- `article-eater/` - Evidence extraction and analysis system
- `knowledge-graph-ui/` - Graph visualization interface

## Support Resources

**Documentation:**
- `Adaptive_Preference_System_Documentation.md` - Design system reference
- `RUNNING_THE_SYSTEM.md` - Setup and running instructions

**For Design System Usage:**
- See `graphical-model/style_system/adaptive_preference_ai_style_primer.md` for AI-friendly style guide
- See `graphical-model/style_system/adaptive_preference_base.css` for production CSS

## Contributing Experiments

When contributing experimental code:

1. **Clear Purpose** - Document what you're experimenting with
2. **Date Context** - Include when the experiment was created
3. **Dependencies** - List any dependencies or requirements
4. **Findings** - Document what you learned, even if experiment "failed"
5. **Next Steps** - Note potential next steps or integration paths

## Maintenance

**This directory requires minimal maintenance:**
- Experiments can remain indefinitely as reference
- Successful experiments get extracted to main projects
- Failed experiments stay as documentation of what was tried
- No obligation to keep experiments working as dependencies change
