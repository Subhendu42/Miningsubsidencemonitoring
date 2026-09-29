---
name: My Design System 2
colors:
  surface: '#fff8f4'
  surface-dim: '#ffd2a0'
  surface-bright: '#fff8f4'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1e6'
  surface-container: '#ffead7'
  surface-container-high: '#ffe4c8'
  surface-container-highest: '#ffddb8'
  on-surface: '#2a1700'
  on-surface-variant: '#44464f'
  inverse-surface: '#462a02'
  inverse-on-surface: '#ffeede'
  outline: '#757780'
  outline-variant: '#c5c6d0'
  surface-tint: '#4b5d8a'
  primary: '#4b5d8a'
  on-primary: '#ffffff'
  primary-container: '#8294c4'
  on-primary-container: '#192c56'
  inverse-primary: '#b3c6f8'
  secondary: '#575c7d'
  on-secondary: '#ffffff'
  secondary-container: '#d3d8fe'
  on-secondary-container: '#585d7e'
  tertiary: '#5a5f68'
  on-tertiary: '#ffffff'
  tertiary-container: '#90959f'
  on-tertiary-container: '#292e36'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d9e2ff'
  primary-fixed-dim: '#b3c6f8'
  on-primary-fixed: '#031943'
  on-primary-fixed-variant: '#334671'
  secondary-fixed: '#dee1ff'
  secondary-fixed-dim: '#bfc4ea'
  on-secondary-fixed: '#141936'
  on-secondary-fixed-variant: '#3f4564'
  tertiary-fixed: '#dee2ed'
  tertiary-fixed-dim: '#c2c6d1'
  on-tertiary-fixed: '#171c24'
  on-tertiary-fixed-variant: '#424750'
  background: '#fff8f4'
  on-background: '#2a1700'
  surface-variant: '#ffddb8'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

# Design System

## Brand & Style
The design system adopts a **fidelity** modern corporate aesthetic using the **Inter** typeface family. It prioritizes clarity, structure, and a balanced, reliable visual hierarchy suited for professional interfaces.

## Colors
The palette is built upon a soft, calming foundation of muted blues and warm neutrals. 
- **Primary (`#8294C4`)**: Used for primary actions, active states, and key focal points.
- **Secondary (`#ACB1D6`)**: Used for supporting interactive elements and complementary highlights.
- **Tertiary (`#DBDFEA`)**: Used for subtle accents, backgrounds, and low-priority visual chunks.
- **Neutral (`#FDCD96`)**: A warm, approachable base for surfaces, text contrast, and structural dividers.

## Typography
All text elements utilize the **Inter** font family, ensuring high legibility across all screen sizes. The typographic scale employs clear modular steps to maintain a crisp, modern hierarchy.

## Layout & Spacing
A consistent 8px-based spacing rhythm is maintained across all layouts (`spacing` level 2), ensuring clean whitespace and predictable alignment for all interactive components.

## Elevation & Depth
Elevation is achieved through subtle tonal variations and gentle, low-opacity ambient shadows that complement the cool blue primary palette and warm neutral surfaces.

## Shapes
A roundedness level of `2` provides friendly, approachable surfaces with standard 0.5rem radii for buttons and inputs, scaling up for larger containers.

## Components
Components leverage the primary and secondary color palette, utilizing Inter typography and rounded corners (roundedness level 2) to maintain a cohesive, accessible experience across buttons, inputs, cards, and navigation elements.