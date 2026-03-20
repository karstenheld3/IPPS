---
name: youtube-downloader
description: Download YouTube content as MP3 audio or video using yt-dlp with PowerShell cmdlet parameters.
---

# YouTube Downloader Skill

Prerequisites: PowerShell 5.1+, Internet connection (auto-downloads yt-dlp and ffmpeg), Windows Terminal (optional, parallel tabs)

## Scripts

- Download-Youtube-To-Mp3.ps1 - Extract audio as MP3
- Download-Youtube-To-Video.ps1 - Download video files

## MP3 Download

```powershell
.\Download-Youtube-To-Mp3.ps1 -Urls "https://youtu.be/abc" -Quality 320k -Playlist
```

### MP3 Parameters

- -Urls (required) - YouTube URLs
- -OutputFolder - Default: `[WORKSPACE]/../.tools/_downloaded_audio`
- -Quality - `128k`, `192k`, `256k`, `320k` (default: `192k`)
- -Playlist - Download entire playlist (switch)
- -UseCookies - Use Chrome cookies (default: `$true`)
- -ChromeProfile - Chrome profile name (auto-detected)
- -ToolsFolder - Binaries location (default: `[WORKSPACE]/../.tools/youtube-downloader`)

## Video Download

```powershell
.\Download-Youtube-To-Video.ps1 -Urls "https://youtu.be/abc" -Format mp4 -Quality 1080p -Playlist
```

### Video Parameters

- -Urls (required) - YouTube URLs
- -OutputFolder - Default: `[WORKSPACE]/../.tools/_downloaded_video`
- -Format - `best`, `mp4`, `webm`, `mkv` (default: `best`)
- -Quality - `best`, `1080p`, `720p`, `480p`, `360p` (default: `best`)
- -Playlist - Download entire playlist (switch)
- -UseCookies - Use Chrome cookies (default: `$true`)
- -ChromeProfile - Chrome profile name (auto-detected)
- -ToolsFolder - Binaries location (default: `[WORKSPACE]/../.tools/youtube-downloader`)

## Shared Features

- Auto-download yt-dlp and ffmpeg if missing
- yt-dlp version checking and auto-update
- Chrome cookie auto-detection for age-restricted content
- DPAPI error fallback (retries without cookies)
- Pipeline input and playlist support

## Parallel Downloads (Cascade)

Multiple URLs: Cascade spawns terminals (max 10), splits URLs evenly, runs with `-UseCookies $false`.

## Output Locations

- Audio: `[WORKSPACE]/../.tools/_downloaded_audio/`
- Video: `[WORKSPACE]/../.tools/_downloaded_video/`
- Binaries: `[WORKSPACE]/../.tools/youtube-downloader/`