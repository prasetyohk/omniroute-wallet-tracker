# OmniRoute — Universal Cross-Chain Wallet Intelligence Tool

> **Bahasa Indonesia 🇮🇩 | English 🇬🇧** — Panduan lengkap dan visual alur kerja tersedia dalam dua bahasa di bawah.

**Built with passion by Prasetyo HK**  
[![X (Twitter)](https://img.shields.io/badge/X-@Prasetyo_HK-black?style=flat&logo=x)](https://x.com/Prasetyo_HK)
[![GitHub](https://img.shields.io/badge/GitHub-prasetyohk-181717?style=flat&logo=github)](https://github.com/prasetyohk)

![OmniRoute Header & Analytics Engines](assets/omniroute_hero_tabs.png)

---

## 🇮🇩 Bahasa Indonesia

### Tentang OmniRoute

**OmniRoute** adalah platform intelijen dan pelacak wallet lintas rantai (*cross-chain*) berbasis Python yang berjalan 100% secara lokal dan privat di komputer Anda. Dirancang khusus untuk membedah transaksi jembatan (*bridge*), memverifikasi keaslian wallet vs smart contract, menelusuri klaster pendanaan (*wallet genealogy*), serta mengaudit aliran deposit exchange dengan filter anti-spam multi-tier.

Antarmuka dirancang dengan standar **FinTech X** (latar hitam obsidian `#06080C` dipadukan dengan aksen *electric lime* `#9EFF00`) yang responsif, modern, dan dilengkapi dukungan dwibahasa (ID/EN).

---

### 🔄 Diagram Alur Kerja Sistem (Workflow Architecture)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           OmniRoute Intelligence Core                           │
└─────────────────────────────────────┬───────────────────────────────────────────┘
                                      │
       ┌──────────────────────────────┼─────────────────────────────┐
       ▼                              ▼                             ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│    Tab 1     │              │    Tab 3     │              │    Tab 4     │
│Route Resolver│              │Wallet Cluster│              │Deposit Tracer│
└──────┬───────┘              └──────┬───────┘              └──────┬───────┘
       │                             │                             │
       ▼                             ▼                             ▼
[Parse TX Hash/URL]           [Trace Genealogy]             [Auto Multi-Chain]
  - Origin Sender               - Genesis Funder              - Parallel 5 EVM Chains
  - Protocol Solver             - All-Time Senders            - Solana ATA Resolution
  - Destination Target          - Cashout / Exit Hub          - Multi-Tier Spam Filter
  - Fill Settlement TX          - GMGN Watchlist Sync         - DexScreener USD Valuation
```

---

### Fitur Utama & Cara Kerja — 4 Mesin Analisis

---

#### 🔁 Tab 1: Route Resolver (Pelacak Rute Swap & Bridge)

Lacak rute transaksi swap atau bridge dari wallet pengirim ➔ router/solver protokol ➔ dompet penerima di rantai tujuan.

![Route Resolver Breakdown](assets/omniroute_route_breakdown.png)

**Cara Kerja & Alur Analisis:**
1. Masukkan tautan block explorer (RobinScan, Etherscan, Arbiscan, Basescan, Bscscan, Polygonscan, Solscan) atau langsung TX hash mentah.
2. Mesin OmniRoute membaca calldata, mendeteksi protokol bridge (**Relay.link**, **Li.Fi / Jumper Exchange**, **Across Protocol**, **LayerZero / Stargate**, atau **Universal EVM Fallback**).
3. Menguraikan 3 simpul utama:
   * **From (Pengirim):** Wallet asal, jaringan pengirim, dan aset yang didepositkan.
   * **Router / Solver / Bridge:** Kontrak pintar atau solver relay yang memfasilitasi pertukaran.
   * **Destination Wallet:** Alamat penerima akhir di chain tujuan, jumlah token yang diterima, serta tautan TX penyelesaian (*fill settlement*).
4. Tombol 1-klik untuk menyalin wallet tujuan, membuka explorer tujuan, serta opsi *"Analyze Wallet Flow"* untuk meneruskan analisis ke Tab 3.

---

#### 🔍 Tab 2: Target & Address Verifier (Verifikasi Alamat & Target)

Verifikasi apakah suatu alamat merupakan **dompet pribadi (EOA)** atau **smart contract** sebelum melakukan transaksi atau penyalinan alamat.

**Cara Kerja & Fitur:**
* **EIP-55 Checksum Guard:** Menghasilkan format huruf besar/kecil resmi untuk mencegah salah kirim dana.
* **On-Chain Bytecode Inspector:** Memeriksa RPC langsung ke blockchain untuk memastikan apakah target memiliki bytecode kontrak atau merupakan EOA murni.
* **Known Protocol Registry:** Otomatis menandai jika alamat tersebut adalah router publik (Uniswap, 1inch, Across, Relay, dll.) atau hot wallet bursa terpusat.
* **Live Native Balance:** Menampilkan saldo asli (ETH, SOL, BNB, POL) langsung dari node RPC publik.

---

#### 🕸️ Tab 3: Wallet Cluster & Relationship Tracer (Pelacak Silsilah & Relasi Dompet)

Lacak asal modal pertama (*genesis funder*), relasi antar-dompet, dan muara pencairan dana (*cashout exit*) secara menyeluruh.

![Wallet Cluster Tracer](assets/omniroute_wallet_cluster.png)

**Cara Kerja & Fitur:**
* **Genesis Funder (Gas Provider Pertama):** Mengidentifikasi wallet root yang pertama kali mendanai gas native ke wallet target.
* **Top Senders (All-Time Inflow):** Mengagregasi penyumbang dana terbesar dengan tombol salin alamat per-baris.
* **Exit & Outflow Targets (Cash Out):** Menampilkan ke mana saja dana dialirkan, lengkap dengan persentase dominasi dan deteksi pola (CEX, DEX Liquidity, Bridge, Mixer).
* **Batch Relationship Analysis (2–20 Wallets):** Membandingkan beberapa wallet sekaligus untuk mendeteksi apakah memiliki kesamaan *genesis funder* atau *consolidation hub*.
* **Confidence Score (0–100%):** Skor probabilitas relasi pribadi yang aman dari *false positive* (CEX hot wallet & faucet publik dikecualikan secara otomatis).
* **GMGN Watchlist Export:** Export seluruh wallet terkait ke format CSV atau copy langsung untuk dimasukkan ke GMGN.

---

#### 📥 Tab 4: Exchange Deposit Inflow Tracer (Pelacak Aliran Masuk Deposit)

Berikan satu alamat deposit bursa (misal deposit Binance, Bybit, OKX, atau personal vault), OmniRoute akan membedah seluruh pengirim dana dan total volume kumulatifnya.

![Exchange Deposit Inflow Tracer](assets/omniroute_deposit_tracer.png)

**Cara Kerja & Alur Pemindaian:**
1. **Multi-Chain EVM Auto-Scan:**
   * Saat memilih mode `auto` pada alamat EVM, OmniRoute **memindai 5 chain EVM sekaligus secara paralel** (Ethereum, Arbitrum One, Base, Polygon, Optimism) menggunakan `ThreadPoolExecutor`.
   * Mendukung Solana dengan resolusi ATA (*Associated Token Account*) ke *owner* wallet asli.
2. **Multi-Tier Anti-Spam & Dust Engine:**
   * **Cumulative Min Threshold:** Menyaring berdasarkan akumulasi total deposit pengirim (bukan per transaksi).
   * **Single-Tx Dust Attack Filter:** Membuang transaksi spam microrate (< $5).
   * **Phishing Token Blacklist:** Mengeliminasi airdrop scam dengan regex pola URL / homoglyph token palsu.
3. **Filtered Senders Drawer:**
   * Transparansi penuh: semua transaksi yang disaring disimpan dalam *drawer* khusus dengan alasan jelas (*below min threshold*, *single-tx dust*, atau *phishing token*).
4. **Export & Deep Trace:**
   * Setiap baris pengirim yang lolos kualifikasi dilengkapi tombol salin, tautan explorer spesifik chain, serta tombol pintas *"Trace in Tab 3"*.

---

### ⚡ Performa & Tips Penggunaan

* **Pemindaian paralel** — Tab 1 mengecek Relay, Li.Fi, Across, LayerZero dan RPC 7 chain secara bersamaan (bukan satu per satu). Transaksi Relay/Li.Fi biasanya selesai < 1 detik.
* **Cache pintar** — hasil yang sama dalam 60 detik (ganti bahasa, klik ulang) tampil instan tanpa memanggil API lagi; harga token & data chain di-cache otomatis.
* **Tempel = lacak** — menempel link explorer / TX hash di Tab 1 langsung memulai pelacakan.
* **Pintasan** — `Alt+1…4` pindah tab, `Ctrl+Enter` mengirim isian batch / CSV. Tab & bahasa terakhir diingat.
* **Batas sumber data publik** — RPC Solana publik hanya mengizinkan ±10 transaksi / 10 detik, jadi pemindaian deposit Solana (25 tx) butuh ±30–40 detik. Bila Blockscout membatasi permintaan, aplikasi menampilkan pesan jelas (bukan hasil kosong).

#### 🕸️ Tab 5: Fund Flow Graph (Graf Aliran Dana Multi-Hop)

Menelusuri dana melewati beberapa hop dari 1–10 dompet seed, lalu menampilkannya sebagai graf interaktif.

1. **Arah:** maju (dana dikirim ke mana), mundur (dana berasal dari mana), atau dua arah. Kedalaman bisa 1–4 hop, dengan 1–8 cabang per dompet.
2. **Filter anti-spam:** hanya token target per chain yang diikuti (Solana: SOL, USDC, USDT, USDG; EVM: koin native, USDC, USDT, USDG). Token dicocokkan lewat **alamat kontrak**, jadi token palsu bernama "USDT" otomatis ditolak. Transfer di bawah minimum (default 0,1 SOL / 0,005 ETH / $10 stablecoin) tidak membuat cabang baru.
3. **Berhenti di infrastruktur:** penelusuran tidak menembus hot wallet CEX, bridge, router, mixer, atau dompet "hub" yang sangat sibuk.
4. **Deteksi pola otomatis:**
   * **Alamat deposit CEX:** dompet yang menyapu ≥70% dana keluarnya ke hot wallet exchange.
   * **Klaster alamat deposit bersama:** ≥2 dompet yang menyetor ke alamat deposit yang sama. Exchange memberi satu alamat per pengguna, jadi ini sinyal kuat satu pemilik.
   * **Peeling chain, konsolidasi, dan pola bintang CEX.**
5. **Graf interaktif:** ketebalan garis sebanding dengan nilai USD. Klik node untuk detail; klik dua kali untuk **Expand +1 hop**. Klaster bisa diekspor ke GMGN CSV, dan seluruh graf ke CSV atau JSON.

6. **EOA vs Smart Contract:** setiap node diberi label EOA (dompet biasa), Smart Account (EIP-7702), Smart Contract, Program, atau PDA (akun milik program di Solana). Kontrak tanpa label otomatis tidak ditelusuri lebih jauh, tapi tetap bisa di-Expand manual.
7. **Tandai & simpan:**
   * Klik node, lalu **Tandai alamat** dengan label, warna, dan catatan. Alamat yang ditandai tersorot di setiap trace berikutnya.
   * **Simpan trace** menyimpan hasil beserta pengaturannya. Dari daftar *Trace tersimpan*, **Buka** menampilkan snapshot tanpa memanggil API, sedangkan **Trace ulang** menjalankan ulang dan menandai node **BARU** sejak terakhir disimpan.
   * Data tersimpan di folder lokal `data/` dan tidak ikut ter-upload ke GitHub.

**RPC PublicNode (gratis, tanpa key):** Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain, opBNB, Robinhood, Ink, Arc, dan Solana. Endpoint ini dipakai sebagai RPC cadangan dan untuk mendeteksi EOA vs kontrak (`eth_getCode` / `getMultipleAccounts`). PublicNode **tidak** menyediakan riwayat transaksi per alamat, jadi penelusuran tetap memakai Helius/Etherscan/Blockscout. RPC kustom per chain bisa diisi di `.env` (`RPC_ETHEREUM=...`).

**Sumber data (key gratis, opsional, di `.env`):**

| Kebutuhan | Disarankan | Tanpa key |
|---|---|---|
| Solana | `HELIUS_API_KEY` (dashboard.helius.dev) | RPC publik: maks. 2 hop / 3 cabang, sekitar 15 detik per dompet |
| EVM | `ETHERSCAN_API_KEY` (satu key untuk semua chain) | Blockscout publik (bisa terkena rate-limit; BNB Chain butuh key) |

WebSocket (WSS) **tidak dibutuhkan** untuk penelusuran, karena tracing membaca riwayat lewat HTTP. WSS baru berguna untuk fitur pemantauan live di masa depan. Pilihan gratisnya: Helius WSS (Solana) atau `wss://ethereum-rpc.publicnode.com` (EVM, tanpa key).

### 🔑 Relay API Key (wajib mulai 24 November 2026)

Relay menghentikan endpoint `/requests/v2` pada **24 November 2026** (batasnya juga diperketat bertahap sebelum itu). OmniRoute sudah mendukung `/requests/v3`, yang membutuhkan API key:

1. Buat key di https://dashboard.relay.link → tab **API keys** → **Create key**.
2. Salin `.env.example` menjadi `.env`, lalu isi `RELAY_API_KEY=key_anda`.
3. Restart OmniRoute.

Tanpa key, aplikasi tetap memakai v2 selama masih tersedia. File `.env` tidak ikut ter-upload ke GitHub.

### Cara Menjalankan

#### Cara 1: Double-Click Launcher (Windows)
1. Buka folder proyek.
2. Klik ganda **`start_omniroute.bat`**.
3. Browser akan otomatis terbuka ke `http://127.0.0.1:5000`.

#### Cara 2: Terminal / Command Prompt
```bash
pip install -r requirements.txt
python app.py
```
Akses di browser: `http://127.0.0.1:5000`

---

---

## 🇬🇧 English

### About OmniRoute

**OmniRoute** is a locally-hosted, privacy-first cross-chain wallet intelligence platform built with Python. It is engineered to decode complex cross-chain bridge swaps, verify wallet vs contract authenticity, map funder genealogy, and inspect centralized exchange deposit inflows with multi-tier spam filtering.

Crafted with a sleek **FinTech X** UI (obsidian black `#06080C` with vibrant electric lime `#9EFF00`), OmniRoute offers zero-latency local execution and seamless bilingual support (Indonesian & English).

---

### 🔄 System Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           OmniRoute Intelligence Core                           │
└─────────────────────────────────────┬───────────────────────────────────────────┘
                                      │
       ┌──────────────────────────────┼─────────────────────────────┐
       ▼                              ▼                             ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│    Tab 1     │              │    Tab 3     │              │    Tab 4     │
│Route Resolver│              │Wallet Cluster│              │Deposit Tracer│
└──────┬───────┘              └──────┬───────┘              └──────┬───────┘
       │                             │                             │
       ▼                             ▼                             ▼
[Parse TX Hash/URL]           [Trace Genealogy]             [Auto Multi-Chain]
  - Origin Sender               - Genesis Funder              - Parallel 5 EVM Chains
  - Protocol Solver             - All-Time Senders            - Solana ATA Resolution
  - Destination Target          - Cashout / Exit Hub          - Multi-Tier Spam Filter
  - Fill Settlement TX          - GMGN Watchlist Sync         - DexScreener USD Valuation
```

---

### Key Features & Mechanics — 4 Analytics Engines

---

#### 🔁 Tab 1: Route Resolver

Decodes complex cross-chain bridges and swaps, revealing the exact path from source sender ➔ solver/router contract ➔ final destination wallet on the target chain.

![Route Resolver Breakdown](assets/omniroute_route_breakdown.png)

**Workflow & Core Capabilities:**
1. Paste any explorer URL (RobinScan, Etherscan, Arbiscan, Basescan, Bscscan, Polygonscan, Solscan) or raw transaction hash.
2. Protocol-aware decoding supports **Relay.link**, **Li.Fi / Jumper Exchange**, **Across Protocol**, **LayerZero / Stargate**, and generic **Universal EVM Fallback**.
3. 3-node visual breakdown:
   * **From (Sender):** Origin address, source blockchain, and deposited asset valuation.
   * **Router / Solver / Bridge:** Intermediary smart contract or relay solver handling the cross-chain execution.
   * **Destination Wallet:** Final recipient wallet on the target network, received token amount, USD equivalent, and the fill settlement transaction link.
4. Instant copy actions for destination wallet, origin TX hash, and settlement TX, plus a direct shortcut to analyze fund flow in Tab 3.

---

#### 🔍 Tab 2: Target & Address Verifier

Validates address integrity and detects whether a target is a **personal wallet (EOA)** or a **smart contract** before sending transactions.

**Workflow & Capabilities:**
* **EIP-55 Checksum Enforcement:** Converts raw hex to official mixed-case checksum format to prevent typos.
* **On-Chain Bytecode Inspector:** Queries live blockchain nodes to determine contract code presence vs pure EOA.
* **Known Entity & Router Guard:** Flags recognized routers, DEX pools, CEX deposit gateways, and bridge contracts.
* **Live Native Balance:** Fetches real-time ETH, SOL, BNB, or POL balance directly from RPC.

---

#### 🕸️ Tab 3: Wallet Cluster & Relationship Tracer

Maps capital genealogy, detects shared funding origins, and identifies cashout destinations across all historical activity.

![Wallet Cluster Tracer](assets/omniroute_wallet_cluster.png)

**Workflow & Capabilities:**
* **Genesis Funder (Root Wallet):** Pinpoints the earliest transaction that funded native gas into the target address.
* **Top Senders (All-Time Inflows):** Aggregates major depositors with individual copy controls.
* **Exit & Outflow Destinations:** Analyzes cashout behaviors with automatic category classification (CEX, DEX Liquidity, Bridge, Mixer).
* **Batch Cluster Analysis (2–20 Wallets):** Tests multiple wallets for common private genesis funders or consolidation hubs.
* **False-Positive Resistant Confidence Scoring (0–100%):** Excludes noisy public entities (CEX hot wallets, faucets) to prevent erroneous clustering.
* **GMGN Watchlist Export:** One-click CSV download or clipboard copy formatted for direct import into GMGN.

---

#### 📥 Tab 4: Exchange Deposit Inflow Tracer

Given an exchange deposit address, OmniRoute scans and aggregates all incoming funding wallets and their cumulative volume.

![Exchange Deposit Inflow Tracer](assets/omniroute_deposit_tracer.png)

**Workflow & Scanning Pipeline:**
1. **Parallel Multi-Chain EVM Scanning:**
   * When `auto` chain is selected for EVM addresses, OmniRoute **queries 5 major chains simultaneously** (Ethereum, Arbitrum One, Base, Polygon, Optimism) via `ThreadPoolExecutor`.
   * Full Solana support with automated Associated Token Account (ATA) to wallet owner resolution.
2. **Multi-Tier Anti-Spam & Phishing Filter:**
   * **Cumulative USD Filter:** Evaluates total deposit volume per sender rather than individual transactions.
   * **Dust Attack Filter:** Removes single micro-transactions (< $5).
   * **Phishing Token Guard:** Regex blacklist filters out spam airdrops and deceptive zero-value tokens.
3. **Transparent Filtered Log Drawer:**
   * Inspect all excluded wallets and review exact filter reasons (*below threshold*, *dust attack*, or *phishing token*).
4. **Actionable Registry:**
   * Displays qualified senders sorted by deposit volume with chain badges, explorer links, and direct *"Trace in Tab 3"* shortcuts.

---

### ⚡ Performance & Usage Tips

* **Parallel scanning** — Tab 1 queries Relay, Li.Fi, Across, LayerZero and 7 chain RPCs at the same time instead of one by one. Relay/Li.Fi transactions usually resolve in under 1 second.
* **Smart caching** — repeating a lookup within 60s (language switch, re-click) is instant; token prices and chain data are cached automatically.
* **Paste = track** — pasting an explorer link / TX hash into Tab 1 starts tracking immediately.
* **Shortcuts** — `Alt+1…4` switch tabs, `Ctrl+Enter` submits the batch / CSV box. Last tab and language are remembered.
* **Public data-source limits** — the public Solana RPC allows ~10 transactions per 10s, so a Solana deposit scan (25 txs) takes ~30–40s. When Blockscout rate-limits requests, the app shows a clear message instead of an empty result.

#### 🕸️ Tab 5: Fund Flow Graph (Multi-Hop Tracing)

Traces funds across several hops from 1–10 seed wallets and shows them as an interactive graph.

1. **Direction:** forward (where did funds go), backward (where did they come from), or both. Depth is 1–4 hops, with 1–8 branches per wallet.
2. **Anti-spam filters:** only each chain's target tokens are followed (Solana: SOL, USDC, USDT, USDG; EVM: native coin, USDC, USDT, USDG). Tokens are matched by **contract address**, so fake tokens named "USDT" are rejected. Transfers below the minimum (default 0.1 SOL / 0.005 ETH / $10 stablecoin) never start a new branch.
3. **Stops at infrastructure:** tracing never walks through CEX hot wallets, bridges, routers, mixers, or very busy "hub" wallets.
4. **Automatic pattern detection:**
   * **CEX deposit addresses:** wallets that sweep ≥70% of their outflow into an exchange hot wallet.
   * **Shared-deposit clusters:** ≥2 wallets depositing into the same deposit address. Exchanges issue one address per user, so this is a strong same-owner signal.
   * **Peeling chains, consolidation, and CEX star patterns.**
5. **Interactive graph:** line thickness follows USD value. Click a node for details; double-click it to **Expand +1 hop**. Clusters export to GMGN CSV, and the whole graph to CSV or JSON.

6. **EOA vs Smart Contract:** every node is labelled EOA (regular wallet), Smart Account (EIP-7702), Smart Contract, Program, or PDA (program-owned account on Solana). Unlabelled contracts stop automatic tracing, but you can still expand them by hand.
7. **Mark & save:**
   * Click a node, then **Mark this address** with a label, colour, and note. Marked addresses are highlighted in every later trace.
   * **Save trace** stores the result together with its settings. From *Saved traces*, **Open** shows the snapshot without any API call, and **Re-trace** runs it again and tags every node that is **NEW** since it was saved.
   * Data lives in the local `data/` folder and is never uploaded to GitHub.

**PublicNode RPCs (free, no key):** Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain, opBNB, Robinhood, Ink, Arc, and Solana. These endpoints serve as fallback RPCs and power EOA-vs-contract detection (`eth_getCode` / `getMultipleAccounts`). PublicNode does **not** serve per-address transaction history, so tracing still uses Helius/Etherscan/Blockscout. Custom per-chain RPCs can be set in `.env` (`RPC_ETHEREUM=...`).

**Data sources (free, optional keys in `.env`):**

| Need | Recommended | Without a key |
|---|---|---|
| Solana | `HELIUS_API_KEY` (dashboard.helius.dev) | public RPC: max 2 hops / 3 branches, about 15s per wallet |
| EVM | `ETHERSCAN_API_KEY` (one key for every chain) | public Blockscout (may be rate-limited; BNB Chain needs a key) |

WebSockets (WSS) are **not needed** for tracing, because tracing reads history over HTTP. WSS only matters for a future live-monitoring feature. Free options: Helius WSS (Solana) or `wss://ethereum-rpc.publicnode.com` (EVM, no key).

### 🔑 Relay API Key (required from November 24, 2026)

Relay retires `/requests/v2` on **November 24, 2026** (with tightening rate limits before then). OmniRoute already supports `/requests/v3`, which needs an API key:

1. Create a key at https://dashboard.relay.link → **API keys** → **Create key**.
2. Copy `.env.example` to `.env` and set `RELAY_API_KEY=your_key`.
3. Restart OmniRoute.

Without a key the app keeps using v2 while it is still available. The `.env` file is never uploaded to GitHub.

### How to Run

#### Option 1: Double-Click Launcher (Windows)
1. Open the project folder.
2. Double-click **`start_omniroute.bat`**.
3. Your default browser will automatically open `http://127.0.0.1:5000`.

#### Option 2: Command Line
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

---

### Tech Stack

- **Backend**: Python 3.10+ / Flask
- **Concurrency**: `concurrent.futures.ThreadPoolExecutor` for high-speed multi-chain querying
- **Pricing Engine**: DexScreener API (highest-liquidity pair selection) + CoinGecko
- **Frontend**: Vanilla HTML5 + CSS3 (Glassmorphism / FinTech X Design System) + Modern JavaScript
- **Typography**: Google Fonts (Plus Jakarta Sans & JetBrains Mono)
- **Icons**: Font Awesome 6 Pro Free CDN
- **Chains Supported**: Ethereum, Base, Arbitrum One, BNB Chain, Polygon, Optimism, Solana

---

### ⚠️ Disclaimer

> **EN**: OmniRoute is an on-chain data correlation tool. All relationship and cluster outputs are probabilistic heuristics. Wallets may share transaction histories for legitimate reasons. Always conduct independent research (DYOR).  
> **ID**: OmniRoute adalah alat korelasi data on-chain. Semua hasil analisis klaster dan relasi bersifat heuristik probabilistik. Selalu lakukan riset mandiri (DYOR) sebelum mengambil keputusan.

---

## Author / Pembuat

| | |
|---|---|
| **Developer** | Prasetyo HK |
| **X (Twitter)** | [@Prasetyo_HK](https://x.com/Prasetyo_HK) |
| **GitHub** | [prasetyohk](https://github.com/prasetyohk) |

---

## ☕ Support & Donations / Dukung Proyek Ini

> **EN**: If OmniRoute streamlined your on-chain research and workflow, contributions are always appreciated!  
> **ID**: Jika OmniRoute membantu riset on-chain dan alur kerja Anda, dukungan Anda sangat berarti!

| Network | Address |
|---------|---------|
| **EVM** (Ethereum / Base / Arbitrum / BSC / Polygon) | `0xbfcba220bc538af067fd74e74ae59a9eb1b94bf6` |
| **Solana** | `Ae2BrzfsSsRekrX17kAMd2NM69jupVPeheRETsmXPDFh` |
| **Sui** | `0xab8e9a1a3e191e2db9d967004e993b0d1aafeb1dcc23615843713a7c7b56b0d1` |
| **Bitcoin** | `bc1q390kc993fw8jx5l876vth7jcw4j99e30kppq7j` |

*Terima kasih / Thank you!* 🙏

---

*OmniRoute — Universal Cross-Chain Wallet Intelligence. Built locally, runs privately.*
