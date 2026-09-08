# Brand assets

The Attestar identity: an eight-point star held inside a hexagonal seal, with
six vertex nodes converging on the star. The hexagon is the on-chain record,
the nodes are the inputs and the model, and the star is the single verified
proof they collapse into.

## Files

| File | Use |
| ---- | --- |
| `logo.svg` | Primary mark, 512×512 app-icon shape. Source of truth — edit this, then re-export the rasters. |
| `logo.png` | 1024×1024 raster export. Referenced by the root `README.md`. |
| `logo.jpg` | 1024×1024 flattened export for contexts that reject PNG alpha. |
| `icon.svg` | Small-size variant: heavier stroke, no vertex beads or rays. Use at 64px and below. |
| `icon.png` | 256×256 raster export of the icon variant. |
| `banner-attestar.svg` | 2048×576 social/README banner. |

## Palette

| Token | Hex | Use |
| ----- | --- | --- |
| Ground | `#05070F` | Page and canvas background |
| Deep | `#0A1024` | Panels, gradient top stop |
| Panel | `#0E1630` | Diagram node fills |
| Primary | `#22D3EE` | Cyan — strokes, rules, primary accent |
| Bright | `#67E8F9` | Highlights, node rings, eyebrow text |
| Dim | `#0891B2` | Gradient end stop, secondary badges |
| Accent | `#FFFFFF` | Star core, wordmark gradient start |
| Text | `#A9BBD4` | Body copy on dark |
| Muted | `#7C8BA8` | Secondary copy, muted strokes |

Gradients run `Bright → Primary → Dim` on a 0,0 → 1,1 diagonal for strokes,
and `White → Bright → Primary` for the star and wordmark.

## Regenerating

The SVGs are emitted by `generate.py` rather than hand-edited, so the
hexagon geometry, starfields, and palette stay consistent across all three
assets. Run `python3 assets/generate.py` from the repository root, then
re-export the rasters from the SVGs at 1024px (logo) and 256px (icon).
