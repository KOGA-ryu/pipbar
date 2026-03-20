# Future Optimization Policy

Optimization is allowed as a note before it is allowed as work.

## Policy

- leave short upgrade notes only in likely hot paths
- keep the notes narrow and explicit
- no native code before profiling
- no performance work before profiling

## First Optimization Path

Prefer the simplest optimization that fits the existing design.

- batching before native extensions
- prepared statements before lower-level rewrites
- compiled code only when profiling shows a real bottleneck

## Orchestration Rule

Keep orchestration in Python unless profiling proves coordination overhead matters. That is unlikely in this kind of pipeline.
