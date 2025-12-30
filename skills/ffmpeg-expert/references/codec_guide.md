# FFmpeg Codec Guide

コーデック選択のための包括的ガイド。用途に応じた最適なコーデックと設定を解説します。

## 目次

- [コーデック比較表](#コーデック比較表)
- [H.264 (AVC)](#h264-avc)
- [H.265 / HEVC](#h265--hevc)
- [VP9](#vp9)
- [AV1](#av1)
- [ProRes](#prores)
- [用途別推奨コーデック](#用途別推奨コーデック)
- [音声コーデック](#音声コーデック)
- [CRF値ガイド](#crf値ガイド)
- [プリセットガイド](#プリセットガイド)

---

## コーデック比較表

| コーデック | 圧縮効率 | エンコード速度 | 互換性 | 主な用途 | FFmpegエンコーダ |
|-----------|---------|--------------|-------|----------|-----------------|
| H.264 (AVC) | 中 | 速い | 最高 | Web、モバイル、汎用 | libx264 |
| H.265 (HEVC) | 高 | 遅い | 高 | 4K、アーカイブ、ストリーミング | libx265 |
| VP9 | 高 | 遅い | 中 | YouTube、Web | libvpx-vp9 |
| AV1 | 最高 | 非常に遅い | 成長中 | 次世代ストリーミング | libaom-av1, libsvtav1 |
| ProRes | 低（編集用） | 速い | Apple中心 | 映像編集 | prores_ks |

### 圧縮効率の目安（同等画質での比較）

```
H.264 を基準（100%）とした場合:
├── H.264: 100%（基準）
├── H.265: 50-60%（40-50%削減）
├── VP9:   50-60%（40-50%削減）
└── AV1:   35-50%（50-65%削減）
```

---

## H.264 (AVC)

### 特徴

- **最も汎用的なコーデック**
- ほぼ全てのデバイス・ブラウザで再生可能
- エンコード・デコードが高速
- 特許ライセンス（H.264/AVC Patent Portfolio License）

### 推奨用途

- Web配信（汎用性重視）
- モバイルアプリ
- 一般的な動画配信
- リアルタイムエンコード

### FFmpeg設定

```bash
# 高品質（大きなファイルサイズ）
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -preset slow output.mp4

# バランス（推奨）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4

# 高圧縮（小さなファイルサイズ）
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast output.mp4

# Web最適化
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -movflags +faststart output.mp4
```

### プロファイル

| プロファイル | 用途 | 設定 |
|-------------|------|------|
| Baseline | 低スペックデバイス、ビデオ通話 | `-profile:v baseline -level 3.0` |
| Main | 標準的な配信 | `-profile:v main` |
| High | 高品質配信（デフォルト） | `-profile:v high` |

```bash
# Baseline（最大互換性）
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.0 output.mp4
```

---

## H.265 / HEVC

### 特徴

- H.264の後継、約40-50%のファイルサイズ削減
- 4K/8K動画に最適
- エンコードが遅い（H.264の2-4倍）
- ライセンス問題あり（商用利用時は要確認）

### 推奨用途

- 4K動画配信
- 長期アーカイブ（高圧縮）
- 帯域制限環境
- Apple デバイス（iOS 11+, macOS High Sierra+）

### FFmpeg設定

```bash
# 高品質
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -preset slow output.mp4

# バランス（推奨）
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium output.mp4

# 高圧縮
ffmpeg -i input.mp4 -c:v libx265 -crf 32 -preset fast output.mp4

# 10bit エンコード（HDR対応）
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -pix_fmt yuv420p10le output.mp4
```

### 注意点

- 古いデバイス（2015年以前）では再生不可の場合あり
- エンコード時間がH.264の2-4倍
- ハードウェアデコード非対応のデバイスあり

---

## VP9

### 特徴

- Google開発、ロイヤリティフリー
- H.265と同等の圧縮効率
- WebM/Matroskaコンテナで使用
- YouTube公式採用コーデック

### 推奨用途

- YouTube投稿
- Web配信（Chrome, Firefox中心）
- ロイヤリティフリー環境

### FFmpeg設定

```bash
# シングルパス（高速）
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 output.webm

# 2パスエンコード（推奨・高品質）
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 2 -c:a libopus output.webm

# 高品質
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 24 -b:v 0 output.webm
```

### 注意点

- Safari（macOS 11+/iOS 14+）でサポート
- エンコードが遅い
- `-b:v 0` を忘れるとCRFが効かない

---

## AV1

### 特徴

- 最新・最高圧縮効率
- ロイヤリティフリー
- Alliance for Open Media (AOMedia) 開発
- Netflix, YouTube, Amazonが採用

### 推奨用途

- 次世代ストリーミング
- 超高圧縮が必要な場合
- 長期アーカイブ

### FFmpegエンコーダ

| エンコーダ | 特徴 | 用途 |
|-----------|------|------|
| libaom-av1 | リファレンス実装、高品質、非常に遅い | 高品質エンコード |
| libsvtav1 | Intel開発、高速、実用的 | 一般用途（推奨） |
| librav1e | Rust実装 | 実験的 |

### FFmpeg設定

```bash
# libaom-av1（高品質・遅い）
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -cpu-used 4 output.mkv

# libsvtav1（高速・推奨）
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 30 -preset 6 output.mkv

# libsvtav1 高品質
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 25 -preset 4 output.mkv
```

### 注意点

- エンコードが非常に遅い（libaom）
- ハードウェアデコードサポートは限定的
- 2023年以降のブラウザ・デバイスで広くサポート

---

## ProRes

### 特徴

- Apple開発の編集用中間コーデック
- ほぼロスレス品質
- ファイルサイズが大きい
- 編集ソフトでのタイムライン負荷が軽い

### プロファイル

| プロファイル | 用途 | データレート目安（1080p） | FFmpeg設定 |
|-------------|------|-------------------------|------------|
| ProRes 422 Proxy | プロキシ編集 | ~45 Mbps | `-profile:v 0` |
| ProRes 422 LT | 軽量編集 | ~100 Mbps | `-profile:v 1` |
| ProRes 422 | 標準 | ~145 Mbps | `-profile:v 2` |
| ProRes 422 HQ | 高品質 | ~220 Mbps | `-profile:v 3` |
| ProRes 4444 | 最高品質（アルファ対応） | ~330 Mbps | `-profile:v 4` |
| ProRes 4444 XQ | 最高品質+ | ~500 Mbps | `-profile:v 5` |

### FFmpeg設定

```bash
# ProRes 422 LT（編集プロキシ用）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 1 output.mov

# ProRes 422（標準）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 2 output.mov

# ProRes 422 HQ（高品質）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 output.mov

# ProRes 4444（アルファチャンネル対応）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le output.mov
```

---

## 用途別推奨コーデック

### Web配信

| 優先度 | コーデック | 理由 |
|-------|-----------|------|
| 1 | H.264 | 最大互換性 |
| 2 | VP9 | YouTube最適化 |
| 3 | AV1 | 帯域節約（対応ブラウザ限定） |

```bash
# Web配信用（H.264）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k output.mp4
```

### モバイル

| 優先度 | コーデック | 理由 |
|-------|-----------|------|
| 1 | H.264 | iOS/Android両対応 |
| 2 | H.265 | 新しいデバイス向け高圧縮 |

```bash
# モバイル用（H.264）
ffmpeg -i input.mp4 -c:v libx264 -crf 26 -preset fast -vf "scale=-2:720" -c:a aac -b:a 96k -movflags +faststart output.mp4
```

### アーカイブ・長期保存

| 優先度 | コーデック | 理由 |
|-------|-----------|------|
| 1 | H.265 | 高圧縮・安定 |
| 2 | AV1 | 最高圧縮（将来性あり） |
| 3 | ProRes/FFV1 | 品質重視（ファイルサイズ大） |

```bash
# アーカイブ用（H.265）
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -preset slow -c:a flac output.mkv

# ロスレスアーカイブ（FFV1）
ffmpeg -i input.mp4 -c:v ffv1 -level 3 -c:a flac output.mkv
```

### 編集用中間ファイル

| 環境 | コーデック | 理由 |
|------|-----------|------|
| Apple (Final Cut Pro) | ProRes | ネイティブサポート |
| Avid | DNxHD/DNxHR | ネイティブサポート |
| 汎用 | FFV1 | ロスレス・オープン |

---

## 音声コーデック

| コーデック | 用途 | 推奨ビットレート | FFmpegエンコーダ |
|-----------|------|----------------|-----------------|
| AAC | 汎用（MP4） | 128-256 kbps | aac, libfdk_aac |
| MP3 | 互換性重視 | 192-320 kbps | libmp3lame |
| Opus | Web/VoIP（最高効率） | 64-128 kbps | libopus |
| Vorbis | WebM用 | 128-192 kbps | libvorbis |
| FLAC | ロスレス | - | flac |
| ALAC | Apple ロスレス | - | alac |
| PCM | 無圧縮 | - | pcm_s16le等 |

### 推奨設定

```bash
# AAC（MP4用・推奨）
ffmpeg -i input.mp4 -c:a aac -b:a 192k output.mp4

# AAC（高品質）
ffmpeg -i input.mp4 -c:a aac -b:a 256k output.mp4

# Opus（WebM用・高効率）
ffmpeg -i input.mp4 -c:a libopus -b:a 128k output.webm

# FLAC（ロスレス）
ffmpeg -i input.wav -c:a flac output.flac

# MP3（320kbps・最高品質）
ffmpeg -i input.wav -c:a libmp3lame -b:a 320k output.mp3
```

---

## CRF値ガイド

CRF (Constant Rate Factor) は品質を指定する値です。**低い値 = 高品質・大きなファイル**。

### H.264 (libx264)

| CRF | 品質 | 用途 |
|-----|------|------|
| 0 | ロスレス | アーカイブ（非推奨・巨大） |
| 17-18 | 視覚的ロスレス | マスター保存 |
| 19-22 | 高品質 | 高画質配信 |
| **23** | **バランス（デフォルト）** | **一般用途** |
| 24-27 | 中品質 | Web配信 |
| 28-32 | 低品質 | モバイル・低帯域 |

### H.265 (libx265)

| CRF | 品質 | 用途 |
|-----|------|------|
| 0 | ロスレス | - |
| 20-24 | 高品質 | マスター保存 |
| 25-27 | 高品質 | 高画質配信 |
| **28** | **バランス（デフォルト）** | **一般用途** |
| 29-32 | 中品質 | Web配信 |
| 33-38 | 低品質 | モバイル |

### VP9 (libvpx-vp9)

| CRF | 品質 | 用途 |
|-----|------|------|
| 0-15 | 高品質 | マスター保存 |
| 20-25 | 高品質 | 高画質配信 |
| **30-33** | **バランス** | **一般用途** |
| 35-40 | 低品質 | 低帯域 |

---

## プリセットガイド

プリセットはエンコード速度と圧縮効率のトレードオフを制御します。

### H.264/H.265 プリセット

| プリセット | 速度 | 圧縮効率 | 用途 |
|-----------|------|---------|------|
| ultrafast | 最速 | 最低 | テスト・プレビュー |
| superfast | 非常に速い | 低 | リアルタイム |
| veryfast | 速い | やや低 | 軽量エンコード |
| faster | やや速い | やや低 | - |
| fast | やや速い | 中-低 | 一般用途（時間制限あり） |
| **medium** | **中間（デフォルト）** | **中間** | **一般用途** |
| slow | 遅い | やや高 | 高品質配信 |
| slower | より遅い | 高 | アーカイブ |
| veryslow | 最遅 | 最高 | 最高品質アーカイブ |

```bash
# 速度優先
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset fast output.mp4

# 品質優先
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow output.mp4
```

### SVT-AV1 プリセット

| プリセット | 速度 | 用途 |
|-----------|------|------|
| 0-2 | 非常に遅い | 最高品質 |
| 3-4 | 遅い | 高品質 |
| 5-6 | 中間 | バランス |
| 7-8 | 速い | 一般用途 |
| 9-12 | 非常に速い | リアルタイム |

```bash
# バランス（推奨）
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 30 -preset 6 output.mkv
```
