# Contracts First

This project treats contracts as the source of truth.

## Order

- define schema first
- define pipeline stages second
- define validation rules third
- define success criteria before coding

## Coding Rule

Code must conform to the contract.

- implementation does not invent new structure mid-build
- stage outputs should be legible and stable
- schema identity and key rules must be explicit

## Review Rule

When implementation and contract disagree, fix the implementation or update the contract intentionally. Do not let the mismatch linger.
