# Data Visualization Expert Skill - Changelog

## Version 1.2.0 - 2026-03-05

### Documentation & Testing Improvements

#### Changes Made

**1. Added Prerequisites Section (`SKILL.md`)**
- Documented Python 3.8+ requirement
- Listed required packages: matplotlib, seaborn, pandas, numpy
- Added platform-specific Japanese font support guidance
- Included pip install command for quick setup

**2. Added Output Section (`SKILL.md`)**
- Documented output formats: PNG, PDF, SVG
- Specified default 300 DPI resolution
- Added output characteristics table
- Included example output locations

**3. Added Test Suite (`scripts/tests/test_create_visualization.py`)**
- 30+ test cases covering all chart creation functions
- Test fixtures for categorical, time series, scatter, and distribution data
- Configuration tests (palettes, fonts, style)
- Chart creation tests (bar, line, scatter, heatmap, distribution)
- File output tests (PNG, PDF, SVG)
- Color palette application tests

#### Impact
- Improved operator guidance with Prerequisites and Output sections
- Better code quality assurance with comprehensive test coverage
- Easier onboarding for new users

---

## Version 1.1.0 - 2025-11-15

### 🎌 Japanese Font Support Enhancement

#### Background
When creating visualizations with Japanese text, incorrect font configuration caused mojibake (文字化け) - characters rendering as boxes (□□□) or garbled text. This was a critical issue for Japanese-language projects.

#### Changes Made

**1. Updated Script Template (`scripts/create_visualization.py`)**
- Added `get_japanese_fonts()` function with platform-specific font detection
  - macOS: Hiragino Sans, Arial Unicode MS, etc.
  - Windows: Yu Gothic, Meiryo, etc.
  - Linux: Noto Sans CJK JP, Takao, etc.
- Modified `setup_style()` to apply Japanese fonts AFTER matplotlib style
- Set both `font.sans-serif` and `font.monospace` to support Japanese
- Added `axes.unicode_minus = False` to fix minus sign rendering

**2. Updated Documentation (`SKILL.md`)**
- Added comprehensive "Japanese and International Font Support" section
- Documented common causes of mojibake
- Provided platform-specific font configuration code examples
- Added critical DO's and DON'Ts
- Included quick template for Japanese visualizations
- Updated "Common Mistakes to Avoid" checklist
- Added "Configure Japanese/international font support" to creation checklist

**3. Key Technical Insights**
- Font configuration MUST be applied AFTER `plt.style.use()` to prevent overriding
- Both `font.sans-serif` AND `font.monospace` need Japanese fonts
- The `family='monospace'` parameter in text() calls causes mojibake and should be avoided
- Platform detection ensures cross-platform compatibility

#### Testing
- Created comprehensive test script (`test_japanese_fonts.py`)
- Verified Japanese text rendering in:
  - Chart titles and labels
  - Axis labels
  - Text boxes and annotations
  - Negative numbers (minus signs)

#### Impact
- **Before:** Japanese text rendered as boxes (□□□)
- **After:** Perfect Japanese text rendering across all chart elements
- **Cross-platform:** Works on macOS, Windows, and Linux

#### Example Usage

```python
from create_visualization import setup_style
import matplotlib.pyplot as plt

# Setup with Japanese font support
colors = setup_style('default')

# Create chart with Japanese labels
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('日本語タイトル')  # Works perfectly!
ax.set_xlabel('横軸ラベル')
ax.set_ylabel('縦軸ラベル')
```

### Backward Compatibility
✅ Fully backward compatible - existing code continues to work
✅ Japanese fonts added as additional fallback options
✅ English/Latin text rendering unchanged

### Future Enhancements
- Consider adding support for Chinese (Simplified/Traditional)
- Consider adding support for Korean
- Explore auto-detection of text language to optimize font selection

---

## Version 1.0.0 - Initial Release
- Professional data visualization creation
- Chart type selection guidance
- Colorblind-safe palettes
- Dashboard design best practices
- Accessibility guidelines
