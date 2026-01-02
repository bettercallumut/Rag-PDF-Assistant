# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-02

### Added
- **Production-Ready Release** - Cleaned all debug statements and comments
- **Bilingual README** - Modern, dynamic README with English and Turkish support
- **Enhanced Audio Visualizer** - Siri-style waveform with FFT analysis
- **Streaming Responses** - Token-by-token answer generation for better UX
- **Auto-Summarization** - Condense long responses for voice synthesis
- **Platform Support** - Windows, Linux, and Android compatibility
- **Error Handling** - Robust error management and user feedback

### Changed
- **Optimized RAG Pipeline** - Improved context selection and token management
- **UI/UX Polish** - Refined animations and visual feedback
- **TTS Engine** - Enhanced voice synthesis with Turkish language support
- **Code Quality** - Removed all comment lines and debug prints
- **Dependencies** - Updated all packages to latest stable versions

### Fixed
- **StyledMessageBox** - Corrected dialog initialization and button handling
- **Audio Playback** - Fixed media player state management
- **Memory Leaks** - Proper cleanup of TTS workers and audio files
- **PDF Processing** - Enhanced error handling for corrupted PDFs

### Removed
- **Debug Code** - Eliminated all print statements and debug logs
- **Commented Code** - Cleaned up legacy comment blocks
- **Unused Imports** - Removed redundant dependencies

## [1.5.0] - 2025-12-23

### Added
- **Android Build Support** - Buildozer configuration for mobile deployment
- **Main Kivy App** - Alternative UI for mobile platforms
- **Platform Config** - Dynamic platform detection and adaptation

### Changed
- **Architecture** - Separated platform-specific code
- **Mobile Optimization** - Reduced context tokens for Android

## [1.0.0] - 2025-11-15

### Added
- **Initial Release** - First stable version
- **RAG System** - Core retrieval-augmented generation pipeline
- **PyQt6 UI** - Modern desktop interface
- **TTS Integration** - Text-to-speech with pyttsx3
- **3D Visualizations** - Thinking sphere and audio waveform
- **PDF Analysis** - Intelligent document processing
- **OpenAI Integration** - GPT-4 API support
- **Secure API Storage** - Encrypted key management

---

## Version History

- **2.0.0** - Production-ready release with full cleanup
- **1.5.0** - Android support and platform abstraction
- **1.0.0** - Initial stable release

---

## Project Information

**Creator:** Samet YILDIZ  
**University Project Assignment - 2026**

**Contributors:**
- Samet YILDIZ (Lead Developer)
- BetterCallUmut (UI/UX Developer)

---

**Note:** For detailed commit history, see the [Git Log](https://github.com/yourusername/Rag-PDF-Assistant/commits/main).
