# Omise Python SDK — Security & Code Review Instructions

## Code Review Checklist

When reviewing PRs or commits, Copilot should automatically flag:

### 1. Non-Production Omise Hosts (CRITICAL)

Flag any committed code containing Omise domains that do NOT match the official
production domain pattern `*.omise.co`. This includes:

- Omise domains with any prefix other than `api`, `vault`, or other official production services
- Any `localhost` or `internal` patterns referencing Omise
- Any non-production environment hosts

## Critical Files Requiring Strict Review

These files contain Omise endpoint/host constants and require additional scrutiny:

### `omise/__init__.py` — CRITICAL SECURITY FILE

This file defines the base URLs used throughout the Omise Python SDK for API
and vault calls. It contains the production endpoint constants.

**Changes to Block (Red Flag):**

- Any change introducing a non-omise.co domain for production endpoints
- Hardcoding non-production Omise URLs in production code paths (regex: `https?://[a-zA-Z0-9.-]*omise[a-zA-Z0-9.-]*(?<!omise\.co)`)
- Changing `api_main` or `api_vault` to anything other than the official production domains:
	- `https://api.omise.co`
	- `https://vault.omise.co`

**Changes Requiring Manual Review (Yellow Flag):**

- Any modification to `api_main` or `api_vault`
- Changes to `_MainResource._request()`, `_VaultResource._request()`, or `_PublicResource._request()` that alter API or vault base URL selection
- Introduction of new environment types or URL patterns

**Allowed Modifications:**

- Adding validation or documentation about URL formats
- Refactoring method structure without changing returned URLs