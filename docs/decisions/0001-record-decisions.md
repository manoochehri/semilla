# 0001: Keep project state in the repo

**Date:** YYYY-MM-DD  **Status:** accepted

## Context
AI sessions lose context when they end or reset. Decisions and status kept only in chat get lost.

## Decision
All durable state lives in `docs/` (charter, plan, architecture, status, decisions, workstreams, reports). Tasks live in GitHub Issues. Every session ends with `/wrapup`.

## Alternatives considered
- One long project log: grows unreadable; mixes status with history.
- External PM tool: agents can't reliably read or update it.

## Consequences
Any agent can be started fresh. Docs must be kept current; the PR template enforces it.
