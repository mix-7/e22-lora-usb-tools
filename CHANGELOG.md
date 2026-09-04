
---

## 📄 `CHANGELOG.md` (готовый шаблон)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2024-XX-XX

### Added
- Initial release with core functionality
- `e22_usb.py`: Low-level driver for E22-xxxT22U USB modules
  - Register read/write via USB commands
  - Software mode switching (no GPIO required)
  - Configuration helper methods
- `lora_app.py`: Interactive chat application
  - Half-duplex text messaging
  - First-time setup wizard (`FIRST_RUN` mode)
  - Basic receive loop with UTF-8 decoding
- `config_tool.py`: CLI utility for module configuration
  - Read current parameters: `read`
  - Change channel: `channel <0-80>`
  - Change power: `power <22|17|13|10>`
- Bilingual documentation (English/Russian)
- MIT License

### Known Issues
- File transfer not yet implemented (planned for v0.2.0)
- No RSSI monitoring in chat mode
- Single-module testing only shows outgoing messages (half-duplex limitation)

---

## [0.2.0] - (planned)

### Planned Features
- 📦 File transfer with progress indicator and ACK protocol
- 📊 RSSI signal strength display in chat
- 🎛️ Inline config commands: `/channel`, `/power`, `/addr`
- 🔐 Optional message encryption (XOR/AES placeholder)
- 🌐 Multi-node addressing support

### Improvements
- Better error handling and timeout management
- Cross-platform port detection helper
- Unit tests for driver methods

---

## [0.1.1] - (patch, if needed)

### Fixed
- [To be filled if hotfixes are required]

### Changed
- [Minor documentation or dependency updates]