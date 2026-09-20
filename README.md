# OmniRoute — Universal Cross-Chain Wallet Intelligence Tool

> **Bahasa Indonesia 🇮🇩 | English 🇬🇧** — Panduan lengkap tersedia dalam dua bahasa di bawah.

**Built with passion by Prasetyo HK**
[![X (Twitter)](https://img.shields.io/badge/X-@Prasetyo_HK-black?style=flat&logo=x)](https://x.com/Prasetyo_HK)
[![GitHub](https://img.shields.io/badge/GitHub-prasetyohk-181717?style=flat&logo=github)](https://github.com/prasetyohk)

---

## 🇮🇩 Bahasa Indonesia

### Tentang OmniRoute

**OmniRoute** adalah alat intelijen wallet cross-chain berbasis Python yang berjalan lokal di komputer Anda. Alat ini dirancang untuk menelusuri, memverifikasi, dan menganalisis wallet serta transaksi lintas rantai dengan akurasi tinggi. Antarmukanya menggunakan gaya **FinTech X** (latar hitam obsidian `#06080C` + aksen *electric lime* `#9EFF00`) dengan dukungan bilingual Bahasa Indonesia dan Inggris.

---

### Fitur Utama — 4 Tab Analisis

#### 🔁 Tab 1: Route Resolver (Pelacak Rute Swap & Bridge)

Lacak rute transaksi swap/bridge dari wallet pengirim ➔ router protokol ➔ wallet tujuan penerima akhir.

**Yang bisa dianalisis:**
- Protokol: **Relay.link**, **Li.Fi / Jumper Exchange**, **Across Protocol**, **LayerZero / Stargate**, dan **Universal On-Chain EVM Fallback**
- Paste link explorer (Etherscan, Arbiscan, BaseScan, BscScan, Polygonscan, Solscan, RobinScan) atau raw TX hash
- Breakdown 3 langkah: **From (Pengirim) ➔ Router / Solver / Bridge ➔ Wallet Tujuan**
- Menampilkan aset yang dikirim dan aset yang diterima di chain tujuan (termasuk nama token, jumlah, dan estimasi USD)
- Tombol copy 1x klik untuk wallet tujuan, TX hash origin, dan TX hash penerimaan (fill settlement)
- Link explorer langsung ke chain tujuan (Solscan untuk Solana, Basescan untuk Base, dll.)

```
Contoh input yang didukung:
• https://robin.etherscan.io/tx/0x2a17e...
• https://basescan.org/tx/0xabc...
• 0xda166887e41e61838ae518bedc05c7735270f84d7...
```

---

#### 🔍 Tab 2: Address Verifier (Verifikasi Alamat & Target)

Verifikasi apakah suatu alamat adalah **dompet biasa (EOA)** atau **smart contract** sebelum melakukan transfer.

**Fitur:**
- **EIP-55 Checksum Address** — format checksum resmi alamat EVM
- **Router Guard** — deteksi bytecode on-chain untuk membedakan EOA vs smart contract
- **Saldo Native** — tampilkan saldo ETH/BNB/MATIC/SOL via RPC langsung
- Label protokol terkenal (Uniswap, Li.Fi, 1inch, Across, Relay, dll.)
- Mendukung EVM multi-chain dan Solana

---

#### 🕸️ Tab 3: Wallet Cluster & Relationship Tracer (Pelacak Relasi Dompet)

Lacak silsilah modal (genesis funder), relasi antar-dompet, dan target pencairan dana (exit/cashout) secara all-time.

**Mode A — Analisis Dompet Tunggal:**
- **Genesis / First Funder**: Siapa wallet pertama yang mengirim gas native ke dompet ini?
- **Top Senders (All-Time Inflow)**: Siapa yang paling banyak mengirim dana ke dompet ini?
  → Setiap baris memiliki **tombol copy** agar bisa dilacak mandiri
- **Exit & Outflow Targets**: Kemana saja dana dari dompet ini dikirim?
  → Setiap baris memiliki **tombol copy** (hijau untuk inflow, merah untuk outflow)
- **Exit Pattern Detected**: Badge yang mendeteksi pola cashout (CEX, Private, Bridge, Mixer, dll.)
- **GMGN Sync**: Export daftar wallet terhubung ke format GMGN Watchlist (copy semua atau unduh CSV)

**Mode B — Analisis Relasi Batch (2–20 Dompet):**
- Analisis apakah ada irisan **genesis funder atau consolidation hub** yang sama
- **Confidence Score** (0–100%): Seberapa kuat indikasi relasi pribadi antar-dompet
- **False Positive Guard**: Hot wallet CEX (Binance, Bybit, OKX, Coinbase) dan faucet publik dikecualikan
- Badge "Possible Sybil Pattern" hanya muncul jika confidence ≥ 85%

> ⚠️ Klaster relasi adalah estimasi korelasi on-chain publik. Wallet bisa terhubung karena alasan legit. Selalu DYOR sebelum menarik kesimpulan.

---

#### 📥 Tab 4: Exchange Deposit Inflow Tracer (Pelacak Aliran Masuk Deposit)

Berikan satu alamat deposit exchange, sistem akan menemukan semua wallet pengirim dan mengagregasi total volume kumulatif.

**Mode A — Pemindaian Alamat Langsung:**
- Support Solana (base58) dan EVM (0x) dengan deteksi chain otomatis
- Memindai hingga **100 transaksi terbaru**
- Resolusi ATA → wallet owner untuk Solana SPL token
- Valuasi USD via DexScreener (diurutkan berdasarkan likuiditas pool tertinggi)

**Mode B — Upload CSV Manual:**
- Format: `from, to, amount, token_symbol, token_decimal, timestamp, tx_hash`

**Filter Spam & Dust (Level Agregasi Kumulatif):**
- Ambang batas minimum USD (slider $0–$500, default $50)
- Filter Dust Attack (1x kirim < $5)
- Blacklist token phishing / airdrop spam
- Filtered Log Drawer: semua wallet yang dibuang ditampilkan dengan alasan filternya

**Output:**
- Tabel Qualified Senders: ranking, total deposit USD, breakdown token, jumlah TX, tanggal kirim
- Per baris: tombol copy alamat, link explorer, tombol "Trace Relationship (Tab 3)"
- Badge **Smart Contract / Vault Detected** jika alamat target adalah kontrak publik
- Catatan: valuasi USD menggunakan harga saat ini, bukan harga historis saat transaksi

---

### Cara Menjalankan

#### Cara 1: Double-click `.bat` (Windows)
1. Buka folder proyek
2. Klik ganda **`start_omniroute.bat`**
3. Browser akan otomatis terbuka ke `http://127.0.0.1:5000`

#### Cara 2: Manual via Terminal
```bash
pip install -r requirements.txt
python app.py
```
Buka browser: `http://127.0.0.1:5000`

---

### API Key yang Dibutuhkan

Edit `relay_core.py` atau set sebagai environment variable:

| API | Digunakan untuk | Cara dapatkan |
|-----|----------------|---------------|
| `HELIUS_API_KEY` | Solana RPC + parsed tx | [helius.dev](https://helius.dev) |
| `ALCHEMY_API_KEY` | EVM RPC (Ethereum, Base, dll.) | [alchemy.com](https://alchemy.com) |
| `ETHERSCAN_API_KEY` | EVM TX data fallback | [etherscan.io/apis](https://etherscan.io/apis) |

> DexScreener (price lookup) tidak memerlukan API key.

---

### Tech Stack

- **Backend**: Python 3.10+ / Flask
- **Frontend**: Vanilla HTML + CSS + JavaScript
- **Font**: Plus Jakarta Sans + JetBrains Mono (Google Fonts)
- **Icons**: Font Awesome 6
- **Chain Support**: EVM (Ethereum, Base, Arbitrum, BSC, Polygon, Optimism) + Solana

---

---

## 🇬🇧 English

### About OmniRoute

**OmniRoute** is a locally-run Python-based cross-chain wallet intelligence tool. It traces, verifies, and analyzes wallets and cross-chain transactions with high accuracy. The interface uses a **FinTech X** aesthetic (obsidian black `#06080C` + electric lime `#9EFF00`) with full bilingual support.

---

### Key Features — 4 Analysis Tabs

#### 🔁 Tab 1: Route Resolver

Trace transaction routes from sender wallet ➔ bridge/protocol router ➔ final destination wallet.

**Supported:**
- Protocols: **Relay.link**, **Li.Fi / Jumper Exchange**, **Across Protocol**, **LayerZero / Stargate**, **Universal On-Chain EVM Fallback**
- Paste any explorer link or raw TX hash
- 3-step breakdown: **From (Sender) ➔ Router / Solver / Bridge ➔ Destination Wallet**
- Shows sent asset and received asset on the destination chain (token name, amount, USD estimate)
- One-click copy buttons for destination wallet, origin TX hash, and fill/settlement TX hash
- Direct explorer links to the destination chain

---

#### 🔍 Tab 2: Address Verifier

Verify whether an address is a **regular EOA wallet** or a **smart contract** before sending funds.

**Features:**
- EIP-55 Checksum Address
- Router Guard (on-chain bytecode detection)
- Native Balance via direct RPC
- Known protocol labels (Uniswap, Li.Fi, 1inch, Across, Relay, etc.)
- Multi-chain EVM + Solana support

---

#### 🕸️ Tab 3: Wallet Cluster & Relationship Tracer

Trace capital genealogy (genesis funder), cross-wallet relationships, and cashout destination targets.

**Mode A — Single Wallet Analysis:**
- **Genesis / First Funder**: Who first sent native gas to this wallet?
- **Top Senders (All-Time Inflow)**: Who sent the most funds to this wallet?
  → Each row has a **copy button** for independent tracking
- **Exit & Outflow Targets**: Where has this wallet sent its funds?
  → Each row has a **copy button** (lime for inflow, red for outflow)
- **Exit Pattern Detected**: Badge for cashout patterns (CEX, Private, Bridge, Mixer, etc.)
- **GMGN Sync**: Export linked wallets to GMGN Watchlist format (copy all or download CSV)

**Mode B — Batch Relationship Analysis (2–20 Wallets):**
- Check for shared private genesis funders or consolidation hubs
- **Confidence Score** (0–100%)
- **False Positive Guard**: Major CEX hot wallets (Binance, Bybit, OKX, Coinbase) and public faucets excluded
- "Possible Sybil Pattern" badge only appears when confidence ≥ 85%

> ⚠️ Relationship clusters are probabilistic on-chain correlation estimates. Always DYOR.

---

#### 📥 Tab 4: Exchange Deposit Inflow Tracer

Given a single exchange deposit address, find all wallets that sent funds to it and aggregate cumulative volumes.

**Mode A — Direct Address Scan:**
- Solana (base58) and EVM (0x) with automatic chain detection
- Up to **100 recent transactions** via Helius API / Alchemy / Infura
- ATA → wallet owner resolution for Solana SPL tokens
- USD valuation via DexScreener (sorted by highest pool liquidity)

**Mode B — Manual CSV Upload:**
- Format: `from, to, amount, token_symbol, token_decimal, timestamp, tx_hash`

**Spam & Dust Filters (Cumulative Level):**
- Minimum USD threshold slider ($0–$500, default $50)
- Dust Attack Filter (single tx < $5)
- Phishing Token Blacklist
- Filtered Log Drawer: transparent display of all filtered wallets with reasons

**Output:**
- Qualified Senders table: rank, total deposit USD, token breakdown, TX count, first/last deposit date
- Per row: copy address button, explorer link, "Trace Relationship (Tab 3)" button
- **Smart Contract / Vault Detected** badge if target is a public contract
- Note: USD valuation uses current price (not historical price at time of transaction)

---

### How to Run

#### Option 1: Double-click `.bat` (Windows)
1. Open the project folder
2. Double-click **`start_omniroute.bat`**
3. Browser auto-opens at `http://127.0.0.1:5000`

#### Option 2: Manual via Terminal
```bash
pip install -r requirements.txt
python app.py
```
Open browser: `http://127.0.0.1:5000`

---

### Required API Keys

Edit `relay_core.py` or set as environment variables:

| API | Used for | How to get |
|-----|----------|------------|
| `HELIUS_API_KEY` | Solana RPC + parsed transactions | [helius.dev](https://helius.dev) |
| `ALCHEMY_API_KEY` | EVM RPC (Ethereum, Base, etc.) | [alchemy.com](https://alchemy.com) |
| `ETHERSCAN_API_KEY` | EVM TX data fallback | [etherscan.io/apis](https://etherscan.io/apis) |

> DexScreener (price lookup) requires no API key.

---

### Tech Stack

- **Backend**: Python 3.10+ / Flask
- **Frontend**: Vanilla HTML + CSS + JavaScript (no heavy frameworks)
- **Font**: Plus Jakarta Sans + JetBrains Mono (Google Fonts)
- **Icons**: Font Awesome 6
- **Chain Support**: EVM (Ethereum, Base, Arbitrum, BSC, Polygon, Optimism) + Solana

---

### Disclaimer

> **EN**: OmniRoute is an on-chain data correlation tool only. It does not make legal or fraud determinations. All cluster/relationship analysis is probabilistic — wallets can be linked for legitimate reasons. Always DYOR.
>
> **ID**: OmniRoute hanya merupakan alat korelasi data on-chain. Semua analisis klaster bersifat probabilistik. Selalu lakukan riset mandiri (DYOR) sebelum menarik kesimpulan.

---

## Author / Pembuat

| | |
|---|---|
| **Developer** | Prasetyo HK |
| **X (Twitter)** | [@Prasetyo_HK](https://x.com/Prasetyo_HK) |
| **GitHub** | [prasetyohk](https://github.com/prasetyohk) |

---

## ☕ Support & Donations / Dukung Proyek Ini

> **EN**: If OmniRoute helped your on-chain workflow, any contribution is greatly appreciated!  
> **ID**: Kalau OmniRoute membantu pekerjaanmu, kontribusi sekecil apapun sangat berarti!

| Network | Address |
|---------|---------|
| **EVM** (Ethereum / Base / Arbitrum / BSC / Polygon) | `0xFCDD187D32cFaecD8B07638BD6004fA2bF6838C6` |
| **Solana** | `2zyBHgVYNp5WnKUK25WsdsQbsMzkj8Kzw2wDePWAnGZYS` |
| **Sui** | `0xfac84087048bf82f4f99c7704ee0cf9b1386c064b8ea845ab6baf65d1153eb09` |
| **Bitcoin** | `bc1qulgaaddxhl9qz5jcs4wu5tx5j3g9ng3lfd4cl0` |

*Terima kasih / Thank you!* 🙏

---

*OmniRoute — Universal Cross-Chain Wallet Intelligence. Built locally, runs privately.*
