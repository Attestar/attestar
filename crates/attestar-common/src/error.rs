//! Error types shared across the Attestar crates.

#[cfg(not(feature = "std"))]
use alloc::string::String;

use serde::{Deserialize, Serialize};

/// Errors that can occur during model handling, quantization, inference,
/// or proof preparation in the off-chain components.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AttestarError {
    /// The number of inputs did not match the model's expected feature count.
    FeatureCountMismatch { expected: usize, got: usize },
    /// A model definition was structurally invalid.
    InvalidModel(String),
    /// Parsing an external model representation failed.
    ParseError(String),
    /// A fixed-point operation overflowed.
    ArithmeticOverflow,
    /// Quantization validation failed.
    QuantizationError(String),
}

impl core::fmt::Display for AttestarError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            AttestarError::FeatureCountMismatch { expected, got } => {
                write!(f, "feature count mismatch: expected {expected}, got {got}")
            }
            AttestarError::InvalidModel(m) => write!(f, "invalid model: {m}"),
            AttestarError::ParseError(m) => write!(f, "parse error: {m}"),
            AttestarError::ArithmeticOverflow => write!(f, "arithmetic overflow"),
            AttestarError::QuantizationError(m) => write!(f, "quantization error: {m}"),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for AttestarError {}
