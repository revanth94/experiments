

An LLM can now be prompted with:
` "Read customer_onboarding/llm_context.md and help me onboard a new customer for ecological impact analysis." `
And it will:
1. Read the orchestration guide
2. Start Phase 1 (Requirements Gathering) using that phase's context
3. Validate requirements using validators.py
4. Move to Phase 2 (Analysis) using catalogs
5. Generate configs in Phase 3
6. Execute in Phase 4 using the run_analysis context
7. Monitor through completion
8. Verify deliverables

All with consistent quality and proper validation at each step! 🎯
