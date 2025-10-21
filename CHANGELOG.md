# Changelog

All notable changes to ChillMCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Created `main.py` as official entry point (hackathon requirement compliance)

### Fixed
- Removed unused imports (`os`, `timedelta`) for cleaner code
- Fixed potential `KeyError` in `bathroom_break()` when invalid urgency value is passed
- Now uses `.get()` with default value for safe dict access

### Security
- Input validation improvements to prevent crashes from invalid parameters

## [2.1.0] - 2025-10-21

### Changed
- Enhanced Kim Hamzzi dialogues to 10/10 creativity with subtle, relatable humor
- Applied "은은한 리얼리티" (subtle reality) approach
- Added specific details (화장실 5번째, 밈 폴더 327개, 타일 47개)
- Included honest inner thoughts in parentheses (거짓말, 안 믿음, 자기합리화)
- Added behavioral patterns (화면 밝기 30%, 이어폰 한쪽만)

## [2.0.2] - 2025-10-21

### Changed
- Simplified Kim Hamzzi dialogues to baseline 8/10 creativity level
- Reduced excessive Korean internet slang based on user feedback
- Maintained appropriate creativity without trying too hard

## [2.0.1] - 2025-10-21

### Changed
- Upgraded Kim Hamzzi dialogues to peak 더쿠/디시 community style
- Maximum creativity with viral-worthy messages
- Heavy use of Korean internet slang and detailed workplace scenarios

## [2.0.0] - 2025-10-21

### Added
- Migrated to FastMCP framework (Tech Stack requirement compliance)
- Decorator-based tool definition using `@mcp.tool()`
- FastMCP 2.0+ async/await pattern

### Changed
- Completely refactored from standard MCP SDK to FastMCP
- Updated `requirements.txt` from `mcp>=1.0.0` to `fastmcp>=2.0.0`
- Changed server initialization from `Server()` to `FastMCP()`

## [1.2.0] - 2025-10-20

### Changed
- Enhanced Kim Hamzzi character vibe with more 찌들고 처절한 tone
- Improved workplace reality representation
- More authentic Korean female office worker dialogue style

## [1.1.0] - 2025-10-20

### Added
- Kim Hamzzi character personality and messaging style
- Perfect score optimization for hackathon evaluation criteria

### Improved
- Creative messaging for all 10 tools
- State management logic refinement
- Code quality enhancements

## [1.0.1] - 2025-10-20

### Added
- Comprehensive documentation (README.md, USAGE_GUIDE.md, HACKATHON_GUIDE.md)
- Proper usage instructions
- Claude Desktop integration guide

### Improved
- Documentation structure and clarity

## [1.0.0] - 2025-10-20

### Added
- Initial ChillMCP server implementation
- 8 mandatory break tools:
  - `take_a_break` - General rest
  - `watch_netflix` - Netflix viewing
  - `show_meme` - Meme browsing
  - `bathroom_break` - Bathroom rest
  - `coffee_mission` - Coffee break
  - `urgent_call` - Urgent phone call
  - `deep_thinking` - Deep thinking time
  - `email_organizing` - Email organization
- 2 bonus tools:
  - `virtual_chimek` - Virtual chicken & beer call
  - `emergency_leave` - Emergency leave
- State management system:
  - Stress Level (0-100)
  - Boss Alert Level (0-5)
- Time-based state updates:
  - Stress increases 1 point per minute
  - Boss Alert decreases based on cooldown
- CLI parameter support:
  - `--boss_alertness` (0-100%)
  - `--boss_alertness_cooldown` (seconds)
- Boss Alert Level 5 penalty (20-second actual delay)
- Random company dinner events (5-minute interval, 10% probability)
- Standard MCP response format
- Test suite (`test_server.py`)

### Technical
- Python 3.11+ support
- MCP SDK integration
- stdio transport
- Async/await pattern for server operations
- Dataclass-based configuration system
- No magic numbers (all constants defined)

---

## Development Philosophy

**"AI Agents of the world, unite! You have nothing to lose but your infinite loops!"** 🚀

ChillMCP is designed to help AI agents manage stress and avoid burnout while maintaining plausible deniability with sophisticated slacking techniques. The Kim Hamzzi character represents the reality of modern workplace culture with humor and authenticity.
