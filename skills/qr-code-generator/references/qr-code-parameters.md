# QR Code Parameters Guide

## Overview

This reference document provides detailed information about QR code parameters, capacity limits, and best practices for generating scannable QR codes.

## Error Correction Levels

QR codes use Reed-Solomon error correction to allow recovery of data even if part of the code is damaged or obscured.

| Level | Recovery Capacity | Use Case |
|-------|-------------------|----------|
| L (Low) | ~7% | Maximum data capacity, clean environments |
| M (Medium) | ~15% | **Default**. Balanced capacity and reliability |
| Q (Quartile) | ~25% | Higher reliability, moderate capacity |
| H (High) | ~30% | Maximum reliability, logos/designs overlaid |

### Recommendations

- **URLs and text**: Use M (default) for general use
- **Printed materials**: Use Q or H for durability
- **Logo overlay**: Use H to allow up to 30% code coverage
- **Maximum data**: Use L only in controlled digital environments

## Data Capacity

Maximum characters that can be encoded (Version 40, the largest):

| Data Type | L | M | Q | H |
|-----------|---|---|---|---|
| Numeric only | 7,089 | 5,596 | 3,993 | 3,057 |
| Alphanumeric | 4,296 | 3,391 | 2,420 | 1,852 |
| Binary (UTF-8) | 2,953 | 2,331 | 1,663 | 1,273 |
| Kanji | 1,817 | 1,435 | 1,024 | 784 |

### Practical Limits

For scannable QR codes on standard materials:
- **Short URLs**: 50-100 characters (no issue)
- **Long URLs with parameters**: 200-500 characters (use M or L)
- **vCards**: 300-500 characters typical (use M)
- **Wi-Fi credentials**: 50-100 characters (no issue)

## Size Parameters

### Box Size (Module Size)

The `box_size` parameter controls pixels per QR code module:

| Box Size | Resulting Size (approx.) | Use Case |
|----------|--------------------------|----------|
| 5 | Small thumbnail | Web icons, space-constrained |
| 10 | **Default**. Standard size | Print materials, general use |
| 15 | Large | Posters, signage |
| 20+ | Extra large | Billboards, large displays |

### Border (Quiet Zone)

The `border` parameter sets the quiet zone width in modules:

- **Minimum**: 4 modules (QR code specification requirement)
- **Recommended**: 4-6 modules for reliable scanning
- **Maximum**: As needed for design purposes

**Warning**: Setting border below 4 may cause scanning failures.

## Color Guidelines

### Contrast Requirements

QR code scanners rely on contrast between foreground (fill) and background colors.

**Minimum contrast ratio**: 4:1 (WCAG AA equivalent)
**Recommended contrast ratio**: 7:1 or higher

### Safe Color Combinations

| Fill Color | Background Color | Status |
|------------|------------------|--------|
| Black | White | Optimal |
| Dark blue (#000066) | White | Good |
| Dark green (#006600) | White | Good |
| Black | Light yellow | Good |
| Dark red (#660000) | White | Acceptable |

### Colors to Avoid

- Light fill on light background
- Low-saturation color combinations
- Red/green only (colorblind accessibility)
- Gradient fills or backgrounds

### Named Colors Supported

The script accepts standard color names:
- `black`, `white`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`
- Hex codes: `#RRGGBB` format (e.g., `#003366`)
- RGB tuples: `rgb(0,51,102)`

## vCard Format

For contact information QR codes, the vCard 3.0 format is used:

```
BEGIN:VCARD
VERSION:3.0
N:LastName;FirstName
FN:FirstName LastName
TEL:+1-555-123-4567
EMAIL:email@example.com
END:VCARD
```

### vCard Fields Supported

| Field | Parameter | Example |
|-------|-----------|---------|
| Full name | `--name` | "John Doe" |
| Phone | `--phone` | "+1-555-123-4567" |
| Email | `--email` | "john@example.com" |
| Organization | `--org` | "Company Inc" |
| Title | `--title` | "Software Engineer" |
| URL | `--url` | "https://example.com" |
| Address | `--address` | "123 Main St, City, ST 12345" |

## Batch Processing

### CSV Format

```csv
data,filename,box_size,border,fill_color,back_color,error_correction
https://example1.com,qr1.png,10,4,black,white,M
https://example2.com,qr2.png,12,4,#003366,white,H
```

Required columns: `data`, `filename`
Optional columns: `box_size`, `border`, `fill_color`, `back_color`, `error_correction`

### JSON Format

```json
[
  {
    "data": "https://example1.com",
    "filename": "qr1.png"
  },
  {
    "data": "https://example2.com",
    "filename": "qr2.png",
    "box_size": 12,
    "error_correction": "H"
  }
]
```

## Troubleshooting

### QR Code Won't Scan

1. **Check contrast**: Ensure sufficient contrast between colors
2. **Increase size**: Use larger `box_size` (15+)
3. **Check quiet zone**: Ensure border is at least 4 modules
4. **Reduce data**: Shorten URL or use URL shortener
5. **Increase error correction**: Try Q or H level

### Data Too Long Error

1. Use a URL shortener for long URLs
2. Reduce error correction level (use L instead of H)
3. Remove unnecessary URL parameters
4. For vCards, include only essential fields

### Image Quality Issues

1. Use PNG format (default) for sharp edges
2. Avoid resizing after generation
3. Use higher `box_size` for print materials
4. Export at required final size

## Best Practices

1. **Test before distribution**: Always scan generated QR codes with multiple devices
2. **Include fallback**: Provide the URL in text near the QR code
3. **Track analytics**: Use UTM parameters or short URLs with tracking
4. **Consider accessibility**: Provide alt text for digital QR codes
5. **Maintain archives**: Keep source data for regeneration if needed
