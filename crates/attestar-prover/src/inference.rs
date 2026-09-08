//! Model inference engine.
//!
//! Re-exports the shared implementation from `attestar-common` so existing
//! `attestar_prover::inference` call sites keep working. The proven guest path
//! uses the same `attestar_common::inference` module directly.

pub use attestar_common::inference::*;
