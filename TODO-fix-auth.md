# Auth Bug Fix - Duplicate Username Error

## Issue:
Frontend `/auth/register` shows "Username already registered" (400) even for NEW users due to Pydantic validation failure on short test credentials.

## Root Cause:
Both endpoints use `UserCreate` model with strict validation:
- `username >= 3 chars`
- `password
