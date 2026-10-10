// ==================== BILINGUAL DICTIONARY (EN / ID) ====================
const translations = {
  id: {
    tagline: "Pelacak Wallet Tujuan Cross-Chain Swap & Bridge",
    built_by: "Dibuat oleh",
    hero_badge: "4 Alat Investigasi On-Chain dalam 1 Aplikasi",
    hero_title_1: "Lacak Alamat",
    hero_title_lime: "Wallet Tujuan",
    hero_title_2: "dalam Hitungan Detik",
    hero_desc: "Tempel link explorer atau TX hash — OmniRoute mengecek Relay, Li.Fi, Across, LayerZero & RPC publik sekaligus, lalu menunjukkan siapa pengirimnya, lewat router apa, dan ke dompet mana dana mendarat.",
    supported_protocols: "Protokol Didukung:",
    tab_tx_title: "1 · Lacak Transaksi",
    tab_tx_desc: "Ke mana dana swap/bridge mendarat?",
    tab_addr_title: "2 · Cek Alamat",
    tab_addr_desc: "Dompet biasa atau kontrak? Aman dikirimi?",
    search_title: "Lacak Transaksi & Wallet Penerima",
    search_desc: "Paste link explorer (RobinScan, Etherscan, Arbiscan, BaseScan, BscScan, Polygonscan, Solscan) atau raw TX Hash.",
    quick_examples: "Contoh Cepat:",
    btn_track: "Lacak Wallet Tujuan Sekarang",
    btn_loading: "Memindai Semua Protokol...",
    verifier_title: "Verifikasi Target Sebelum Swap / Bridge",
    verifier_desc: "Cegah salah kirim. Pastikan alamat valid checksum, periksa apakah dompet biasa (EOA) atau kontrak router (Uniswap, Li.Fi, 1inch, Across, Relay, dll.).",
    popular_routers: "Coba Router Terkenal:",
    btn_verify: "Periksa Keamanan Alamat",
    btn_verifying: "Memeriksa Bytecode...",
    footer_desc: "Universal Cross-Chain Swap & Bridge Target Wallet Resolver. Mendukung Relay, Li.Fi, Jumper, Across, LayerZero, dan on-chain EVM router.",
    built_with_passion: "Dibangun dengan dedikasi oleh",
    copied_toast: "tersalin ke clipboard!",
    step1_title: "FROM (PENGIRIM)",
    step2_title: "ROUTER / SOLVER / BRIDGE",
    step3_title: "WALLET TUJUAN",
    send_label: "Aset Dikirim:",
    received_asset_label: "Aset Diterima:",
    protocol_label: "Protokol:",
    received_status: "Diterima di",
    copy_btn: "Salin",
    copy_target_btn: "Salin Wallet Tujuan",
    explorer_btn: "Explorer",
    explorer_wallet_btn: "Explorer Dompet",
    fill_tx_btn: "Tx Penerimaan ↗",
    received_tx_label: "Tx Penerimaan (Fill):",
    copy_fill_tx: "Salin Tx Penerimaan",
    contract_btn: "Kontrak",
    metric_amount: "Alur Nilai Aset Swap / Bridge",
    metric_origin_tx: "Origin Transaction Hash",
    metric_dest_tx: "Destination Settlement Tx (Fill)",
    open_in_explorer: "Buka di Explorer",
    status_label: "STATUS:",
    target_contract: "SMART CONTRACT (Router / Pool / Gateway)",
    target_eoa: "EOA (Dompet Biasa / User Wallet)",
    checksum_official: "Checksum Address Resmi",
    addr_type: "Tipe Alamat",
    native_balance: "Saldo Native",
    balance_sub: "Saldo di chain yang dipilih",
    tab_genealogy_title: "3 · Relasi Dompet",
    tab_genealogy_desc: "Siapa yang mendanai & ke mana dana keluar?",
    sybil_title: "Klaster & Penelusuran Relasi Dompet",
    sybil_desc: "Pemecah Relasi Antar-Dompet Tunggal & Massal. Lacak silsilah modal (Genesis Funder), rotasi dompet, hub konsolidasi, dan ekspor instan ke GMGN Watchlist untuk copy-trading.",
    btn_analyze_sybil: "Lacak Silsilah & Relasi Dompet",
    btn_analyze_single: "Lacak Silsilah & Relasi Dompet",
    btn_analyzing: "Memindai Klaster & Relasi...",
    batch_sample_btn: "Demo Klaster Batch",
    funder_gas_title: "FIRST FUNDER (GAS PROVIDER)",
    top_senders_title: "TOP SENDERS (ALL-TIME)",
    top_exits_title: "TOP EXIT DESTINATIONS",
    exit_pattern_label: "Exit Pattern Detected:",
    analyze_flow_btn: "👉 Analyze Wallet Flow &rarr;",
    genesis_inflow_title: "Genesis & Inflow Source (Modal Awal)",
    exit_outflow_title: "Exit & Outflow Targets (Pencairan Dana)",
    days_ago_suffix: "hari lalu",
    no_funder_detected: "Tidak ditemukan transfer native gas langsung.",
    no_exits_detected: "Belum terdeteksi transaksi keluar (outflow).",
    
    // Hardened GMGN & Relationship Enhancements
    gmgn_disclaimer_text: "⚠️ Heuristik Probabilistik: Klaster relasi ini merupakan estimasi korelasi on-chain publik tanpa asumsi niat fraud/sybil. Selalu lakukan riset mandiri (DYOR) sebelum mengeksekusi copy-trading.",
    gmgn_sync_label: "GMGN Watchlist Sync:",
    copy_for_gmgn: "📋 Salin untuk GMGN",
    export_gmgn_csv: "📥 Ekspor GMGN CSV",
    cluster_confidence_label: "Confidence Score:",
    confidence_high: "TINGGI (Relasi EOA Pribadi Kuat)",
    confidence_med: "SEDANG (Kemungkinan Relasi)",
    confidence_low: "RENDAH / INFRASTRUKTUR CEX (Bukan Klaster Pribadi)",
    confidence_none: "TIDAK ADA RELASI (Independen)",
    shared_infra_title: "SHARED PUBLIC INFRASTRUCTURE (DIKECUALIKAN DARI KLASTER PRIBADI)",
    shared_infra_desc: "Dompet berinteraksi dengan Hot Wallet Exchange publik (Binance, OKX, Bybit, Coinbase) atau Faucet yang sama. Ini adalah perilaku umum pengguna dan tidak dihitung sebagai klaster satu pemilik.",
    batch_mode_a_pill: "Mode A: Silsilah Modal & Exit (Dompet Tunggal)",
    batch_mode_b_pill: "Mode B: Pemeriksaan Relasi Batch (2-20 Dompet)",
    batch_textarea_hint: "Tempel 2 hingga 20 alamat wallet (satu alamat per baris) untuk memindai klaster relasi, shared genesis funder, dan hub konsolidasi:",
    batch_btn_label: "Analisis Relasi Antar-Dompet (Batch)",
    batch_overlap_title: "Pemeriksaan Relasi Antar-Dompet Batch",
    wallets_checked_suffix: "Dompet Diperiksa",
    clean_independence: "Semua dompet beroperasi secara independen tanpa irisan private on-chain.",
    linked_table_title: "Daftar Dompet Terhubung (Siap Ekspor GMGN)",
    possible_sybil_pattern: "Pola Kemungkinan Sybil",
    possible_sybil_desc: "Indikasi klaster terkoordinasi (misal multi-wallet farming atau perbendaharaan pribadi yang sama).",
    shared_private_funder_title: "SHARED PRIVATE GENESIS FUNDER (Satu EOA Pribadi Mendanai Beberapa Dompet):",
    shared_private_exit_title: "SHARED PRIVATE CONSOLIDATION HUB (Mencairkan Dana ke EOA Pribadi yang Sama):",
    co_funded_wallets: "Dompet yang didanai bersama:",
    sending_wallets_label: "Dompet pengirim ke hub ini:",
    overlapping_wallets_suffix: "dompet overlap",
    funder_eoa_label: "Funder EOA:",
    consolidation_hub_label: "Hub Konsolidasi EOA:",
    rel_detected_badge: "KLASTER RELASI TERDETEKSI (OVERLAP EOA PRIBADI)",
    cex_only_badge: "HANYA IRISAN CEX PUBLIK (BUKAN KLASTER PRIBADI)",
    no_rel_badge: "TIDAK TERDETEKSI RELASI ANTAR-DOMPET",
    false_positive_guard: "Proteksi False Positive Aktif",
    batch_min_error: "Masukkan minimal 2 alamat wallet valid.",
    batch_scanning_title: "Memindai Relasi Antar-Dompet All-Time...",
    batch_scanning_sub: "Pemeriksaan shared genesis gas provider & consolidation exit targets...",
    col_wallet_addr: "Alamat Dompet",
    col_role: "Peran (Role)",
    col_chain: "Jaringan (Chain)",
    col_confidence: "Keyakinan",
    col_action: "Aksi",
    clean_txs_label: "Transaksi Bersih",
    smart_contract_router: "Smart Contract Router",
    regular_user_wallet: "Dompet Biasa (EOA)",
    bytecode_detected: "Bytecode terdeteksi on-chain",
    individual_wallet: "Alamat dompet perseorangan",

    // Tab 4: Exchange Deposit Inflow Tracer (ID)
    tab_deposit_title: "4 · Sumber Deposit",
    tab_deposit_desc: "Siapa saja yang mengirim ke alamat ini?",
    deposit_section_title: "Exchange Deposit Inflow Tracer",
    deposit_section_desc: "Lacak semua dompet pengirim ke alamat deposit exchange (Solana & EVM), agregasi volume kumulatif all-time, dan filter dust attack / token spam airdrop.",
    deposit_mode_a: "Mode A: Pemindai Langsung Alamat (Solana & EVM)",
    deposit_mode_b: "Mode B: Unggah Riwayat TX Manual (CSV / Tempel)",
    deposit_scope_notice: "Cakupan Alamat Deposit Personal: Memindai hingga 100 transaksi terbaru secara langsung. Valuasi USD menggunakan estimasi harga pasar saat ini. Untuk volume tinggi atau riwayat lengkap, gunakan Mode B (CSV Upload).",
    deposit_input_placeholder: "Tempel alamat deposit exchange (0x... atau Solana Base58 public key)...",
    chain_auto: "Deteksi Otomatis Jaringan",
    csv_paste_label: "Format Kolom CSV:",
    csv_textarea_placeholder: "from,to,amount,token_symbol,token_decimal,timestamp,tx_hash\n0x123...,0xDepositVault,500,USDC,6,1710000000,0xabc...\nSolanaSender...,SolanaDeposit...,15.5,SOL,9,1710000000,5xyz...",
    load_sample_csv: "Muat Contoh CSV",
    filter_settings_title: "Pengaturan Filter & Ambang Batas Spam (Aggregated Level)",
    min_threshold_label: "Ambang Batas Min. Total (USD):",
    exclude_dust_label: "Filter Dust Attack (1x kirim receh < $5)",
    filter_phishing_label: "Blacklist Token Phishing / Spam Airdrop",
    btn_trace_deposit: "Lacak Aliran Masuk & Agregasi Pengirim",
    btn_tracing_deposit: "Memindai & Mengagregasi Inflow...",
    metric_qualified_senders: "Pengirim Terkualifikasi",
    metric_total_volume: "Total Setoran Kumulatif",
    metric_filtered_senders: "Pengirim Tersaring (Spam/Dust)",
    metric_top_dominance: "Depositor Dominan",
    col_rank: "#",
    col_sender_address: "Alamat Pengirim (Sender)",
    col_total_deposit: "Total Setoran (USD)",
    col_tx_count: "Jumlah TX",
    col_first_deposit: "Deposit Pertama",
    col_last_deposit: "Deposit Terakhir",
    col_actions: "Aksi",
    export_deposit_csv: "📥 Ekspor GMGN CSV",
    copy_qualified_addrs: "📋 Salin Alamat Terkualifikasi",
    toggle_filtered_drawer: "🛡️ Log Pengirim Tersaring (Spam/Dust)",
    btn_trace_tab3: "👉 Trace Relasi (Tab 3)",
    reason_below_min: "Di bawah ambang batas",
    reason_single_dust: "Dust attack 1x receh (< $5)",
    reason_phishing: "Token phishing / airdrop spam",
    vault_warning: "⚠️ Terdeteksi Smart Contract / Vault Bersama (Bukan Alamat Deposit Personal)",
    qualified_senders_title: "Daftar Pengirim Terkualifikasi (Deposit Inflow)",
    filtered_senders_title: "Pengirim yang Tersaring oleh Filter Spam & Ambang Batas",
    // UI states, errors & helpers
    timeout_error: "Permintaan melebihi batas waktu. Coba lagi sebentar lagi.",
    generic_error: "Terjadi kesalahan saat memproses permintaan.",
    elapsed_hint: "Waktu proses di server",
    scanning_protocols: "Memindai semua protokol secara paralel...",
    track_failed: "Transaksi Tidak Ditemukan",
    network_error: "Kesalahan Jaringan",
    checking_bytecode_on: "Memeriksa bytecode & saldo di",
    checking_bytecode_sub: "Checksum EIP-55 • deteksi kontrak • saldo native",
    invalid_addr_title: "Alamat Tidak Valid",
    address_word: "Alamat",
    addresses_word: "alamat",
    batch_title_short: "Analisis Batch",
    batch_trimmed: "Maksimal 20 alamat — sisanya diabaikan.",
    wallet_analysis_failed: "Gagal Menganalisis Wallet",
    no_wallets_to_copy: "Belum ada daftar wallet untuk disalin.",
    no_wallets_to_export: "Belum ada daftar wallet untuk diekspor.",
    gmgn_wallet_list: "Daftar Wallet GMGN",
    gmgn_csv_downloaded: "File CSV GMGN berhasil diunduh!",
    enter_deposit_address: "Masukkan alamat deposit yang valid!",
    paste_csv_data: "Tempel data CSV transaksi terlebih dulu!",
    deposit_scan_sub_solana: "Solana: memindai 25 transaksi terbaru (RPC publik dibatasi ~10 tx/10 detik, bisa 30–40 detik)",
    deposit_scan_sub_multi: "Ethereum • Arbitrum • Base • Polygon • Optimism (paralel)",
    deposit_failed: "Gagal Memindai Deposit",
    no_qualified_export: "Tidak ada alamat terkualifikasi untuk diekspor.",
    no_qualified: "Tidak ada alamat terkualifikasi.",
    confirm_quit: "Tutup aplikasi OmniRoute dan matikan server lokal?",
    stopping_server: "Menghentikan server...",
    offline_title: "Server Sedang Offline",
    offline_desc: "Server lokal OmniRoute dihentikan atau belum aktif. Jika Anda sengaja menghentikannya, Anda bisa menutup jendela ini.",
    reconnect: "Sambungkan Kembali",
    close_window: "Tutup Jendela",
    checking: "Memeriksa...",
    retry: "Gagal, coba lagi",
    server_not_running: "Server belum menyala. Buka OmniRoute App lalu klik sambungkan lagi.",

    // Placeholders
    ph_tx: "Tempel link explorer (…/tx/0x…) atau TX hash / Solana signature",
    ph_address: "0x… atau alamat Solana",
    ph_genealogy: "Tempel alamat wallet (0x… atau Solana) untuk melacak funder & exit",
    ph_deposit: "Tempel alamat deposit exchange (0x… atau Solana)",

    // How-it-works guides
    guide_label: "Cara pakai",
    guide_tx_1: "Tempel link explorer / TX hash",
    guide_tx_2: "OmniRoute cek 5 sumber sekaligus",
    guide_tx_3: "Salin dompet tujuan / lanjut ke Tab 3",
    guide_tx_tip: "Tip: tempel link → pelacakan otomatis jalan. Bisa juga tempel alamat dompet untuk melihat riwayat bridge-nya.",
    guide_addr_1: "Tempel alamat & pilih jaringan",
    guide_addr_2: "Cek checksum, tipe & saldo",
    guide_addr_3: "Pastikan bukan kontrak sebelum kirim",
    guide_addr_tip: "Mengirim aset ke alamat kontrak (router/pool) yang salah biasanya tidak bisa dikembalikan.",
    guide_gen_1: "Tempel 1 alamat, atau 2–20 alamat (Mode B)",
    guide_gen_2: "Lihat funder pertama, pengirim & tujuan exit",
    guide_gen_3: "Ekspor dompet terhubung ke GMGN",
    guide_gen_tip: "Hot wallet CEX (Binance, OKX, dll.) otomatis dikecualikan agar tidak muncul klaster palsu.",
    guide_dep_1: "Tempel alamat deposit, atau CSV (Mode B)",
    guide_dep_2: "Pengirim dikelompokkan & dinilai dalam USD",
    guide_dep_3: "Spam/dust disaring — ekspor sisanya",
    guide_dep_tip: "Deteksi Otomatis memindai 5 chain EVM sekaligus. Ctrl+Enter mengirim isian CSV.",
    shortcuts_hint: "Pintasan: Alt+1…4 pindah tab",
    first_funding_tx: "Tx Pendanaan Pertama",
    bridge_funding_tx: "Didanai via Bridge Cross-Chain",
    cross_chain_badge: "CROSS-CHAIN",
    track_source_btn: "Lacak Sumber Dana (Tab 1)",
    track_source_hint: "Buka di Tab 1 untuk melihat chain asal & dompet pengirim sebenarnya",
    bridge_funding_note: "Dana pertama datang dari bridge/solver, bukan dari pengirim asli. Klik untuk melacak chain asal dan dompet pengirim sebenarnya.",
    origin_chain_label: "Chain asal",
    real_sender_label: "Pengirim asli"
  },
  en: {
    tagline: "Cross-Chain Swap & Bridge Destination Wallet Resolver",
    built_by: "Built by",
    hero_badge: "4 On-Chain Investigation Tools in 1 App",
    hero_title_1: "Track Destination",
    hero_title_lime: "Target Wallet",
    hero_title_2: "in Seconds",
    hero_desc: "Paste an explorer link or TX hash — OmniRoute checks Relay, Li.Fi, Across, LayerZero & public RPCs at once, then shows who sent it, which router it went through, and which wallet received the funds.",
    supported_protocols: "Supported Protocols:",
    tab_tx_title: "1 · Track a Transaction",
    tab_tx_desc: "Where did the swap/bridge funds land?",
    tab_addr_title: "2 · Check an Address",
    tab_addr_desc: "Wallet or contract? Safe to send to?",
    search_title: "Track Transaction & Recipient Wallet",
    search_desc: "Paste explorer URL (RobinScan, Etherscan, Arbiscan, BaseScan, BscScan, Polygonscan, Solscan) or raw TX Hash.",
    quick_examples: "Quick Samples:",
    btn_track: "Track Destination Wallet Now",
    btn_loading: "Scanning All Protocols...",
    verifier_title: "Verify Target Before Swapping / Bridging",
    verifier_desc: "Prevent accidental loss. Ensure valid checksum address, detect EOA user wallet vs smart contract router (Uniswap, Li.Fi, 1inch, Across, Relay, etc.).",
    popular_routers: "Popular Routers:",
    btn_verify: "Inspect Address Safety",
    btn_verifying: "Checking Bytecode...",
    footer_desc: "Universal Cross-Chain Swap & Bridge Target Wallet Resolver. Supports Relay, Li.Fi, Jumper, Across, LayerZero, and on-chain EVM routers.",
    built_with_passion: "Built with passion by",
    copied_toast: "copied to clipboard!",
    step1_title: "FROM (SENDER)",
    step2_title: "ROUTER / SOLVER / BRIDGE",
    step3_title: "DESTINATION WALLET",
    send_label: "Sent Asset:",
    received_asset_label: "Recipient Asset:",
    protocol_label: "Protocol:",
    received_status: "Received on",
    copy_btn: "Copy",
    copy_target_btn: "Copy Destination Wallet",
    explorer_btn: "Explorer",
    explorer_wallet_btn: "Wallet Explorer",
    fill_tx_btn: "Received Tx ↗",
    received_tx_label: "Received Tx (Fill):",
    copy_fill_tx: "Copy Received Tx",
    contract_btn: "Contract",
    metric_amount: "Cross-Chain Asset Flow",
    metric_origin_tx: "Origin Transaction Hash",
    metric_dest_tx: "Destination Settlement Tx (Fill)",
    open_in_explorer: "View on Explorer",
    status_label: "STATUS:",
    target_contract: "SMART CONTRACT (Router / Pool / Gateway)",
    target_eoa: "EOA (Regular User Wallet)",
    checksum_official: "Official Checksum Address",
    addr_type: "Address Type",
    native_balance: "Native Balance",
    balance_sub: "Balance on selected chain",
    tab_genealogy_title: "3 · Wallet Relationships",
    tab_genealogy_desc: "Who funded it & where did funds go?",
    sybil_title: "Wallet Cluster & Relationship Tracer",
    sybil_desc: "Single & Batch Cross-Wallet Relationship Resolver. Trace funding genealogy (Genesis Funder), rotated wallets, consolidation hubs, and export directly to GMGN Watchlist.",
    btn_analyze_sybil: "Trace Wallet Relationships & Exit",
    btn_analyze_single: "Trace Wallet Relationships & Exit",
    btn_analyzing: "Analyzing Clusters & Relationships...",
    batch_sample_btn: "Batch Cluster Demo",
    funder_gas_title: "FIRST FUNDER (GAS PROVIDER)",
    top_senders_title: "TOP SENDERS (ALL-TIME)",
    top_exits_title: "TOP EXIT DESTINATIONS",
    exit_pattern_label: "Exit Pattern Detected:",
    analyze_flow_btn: "👉 Analyze Wallet Flow &rarr;",
    genesis_inflow_title: "Genesis & Inflow Source (Initial Capital)",
    exit_outflow_title: "Exit & Outflow Targets (Cash Out)",
    days_ago_suffix: "days ago",
    no_funder_detected: "No direct native funder detected.",
    no_exits_detected: "No outbound transactions detected yet.",

    // Hardened GMGN & Relationship Enhancements
    gmgn_disclaimer_text: "⚠️ Probabilistic Heuristic: These wallet clusters represent on-chain correlations without presupposing fraud/sybil intent. Always perform independent research (DYOR) before executing copy-trades.",
    gmgn_sync_label: "GMGN Watchlist Sync:",
    copy_for_gmgn: "📋 Copy for GMGN",
    export_gmgn_csv: "📥 Export GMGN CSV",
    cluster_confidence_label: "Confidence Score:",
    confidence_high: "HIGH (Strong Private Linkage)",
    confidence_med: "MEDIUM (Possible Linkage)",
    confidence_low: "LOW / CEX INFRASTRUCTURE (Not Private Linkage)",
    confidence_none: "NO RELATION DETECTED (Independent)",
    shared_infra_title: "SHARED PUBLIC INFRASTRUCTURE (EXCLUDED FROM PRIVATE CLUSTERS)",
    shared_infra_desc: "Wallets interact with the same public Exchange Hot Wallet (Binance, OKX, Bybit, Coinbase) or public Faucet. This is standard user behavior and excluded from single-owner signals.",
    batch_mode_a_pill: "Mode A: Lineage & Exit (Single Wallet)",
    batch_mode_b_pill: "Mode B: Batch Relationship Overlap (2-20 Wallets)",
    batch_textarea_hint: "Paste 2 to 20 wallet addresses (one per line) to scan for relationship clusters, shared genesis funders, and consolidation hubs:",
    batch_btn_label: "Analyze Cross-Wallet Relationships",
    batch_overlap_title: "Batch Relationship Overlap Check",
    wallets_checked_suffix: "Wallets Checked",
    clean_independence: "All wallets operate independently with zero private on-chain overlap.",
    linked_table_title: "Connected Wallets Registry (GMGN Watchlist Ready)",
    possible_sybil_pattern: "Possible Sybil Pattern",
    possible_sybil_desc: "High-confidence private linkage detected (e.g. coordinated multi-wallet farming or shared private treasury).",
    shared_private_funder_title: "SHARED PRIVATE GENESIS FUNDER (One Private EOA Funded Multiple Wallets):",
    shared_private_exit_title: "SHARED PRIVATE CONSOLIDATION HUB (Consolidating Funds to the Same Private EOA):",
    co_funded_wallets: "Co-funded wallets:",
    sending_wallets_label: "Wallets sending to this hub:",
    overlapping_wallets_suffix: "overlapping wallets",
    funder_eoa_label: "Funder EOA:",
    consolidation_hub_label: "Consolidation Hub EOA:",
    rel_detected_badge: "RELATIONSHIP CLUSTER DETECTED (PRIVATE EOA OVERLAP)",
    cex_only_badge: "PUBLIC CEX OVERLAP ONLY (EXCLUDED FROM PRIVATE CLUSTER)",
    no_rel_badge: "NO DIRECT CROSS-WALLET RELATIONSHIP DETECTED",
    false_positive_guard: "False Positive Guard Active",
    batch_min_error: "Please enter at least 2 valid wallet addresses.",
    batch_scanning_title: "Analyzing All-Time Cross-Wallet Relationships...",
    batch_scanning_sub: "Checking private funder overlap, CEX exits, and coordinated clusters...",
    col_wallet_addr: "Wallet Address",
    col_role: "Role",
    col_chain: "Chain",
    col_confidence: "Confidence",
    col_action: "Action",
    clean_txs_label: "Clean Txs",
    smart_contract_router: "Smart Contract Router",
    regular_user_wallet: "Regular User Wallet (EOA)",
    bytecode_detected: "Bytecode detected on-chain",
    individual_wallet: "Individual user wallet",

    // Tab 4: Exchange Deposit Inflow Tracer (EN)
    tab_deposit_title: "4 · Deposit Sources",
    tab_deposit_desc: "Who has been sending to this address?",
    deposit_section_title: "Exchange Deposit Inflow Tracer",
    deposit_section_desc: "Track all sender wallets funding an exchange deposit address (Solana & EVM), aggregate cumulative volume, and filter dust attacks & spam airdrops.",
    deposit_mode_a: "Mode A: Live Address Scanner (Solana & EVM)",
    deposit_mode_b: "Mode B: Manual TX History Upload (CSV / Paste)",
    deposit_scope_notice: "Personal Deposit Address Scope: Scans up to 100 recent transactions directly. USD value estimated using current market price. For high-volume addresses or full history, use Mode B (CSV Upload).",
    deposit_input_placeholder: "Paste exchange deposit address (0x... or Solana Base58 public key)...",
    chain_auto: "Auto-Detect Chain",
    csv_paste_label: "CSV Column Format:",
    csv_textarea_placeholder: "from,to,amount,token_symbol,token_decimal,timestamp,tx_hash\n0x123...,0xDepositVault,500,USDC,6,1710000000,0xabc...\nSolanaSender...,SolanaDeposit...,15.5,SOL,9,1710000000,5xyz...",
    load_sample_csv: "Load Sample CSV",
    filter_settings_title: "Spam Filter & Threshold Settings (Aggregated Level)",
    min_threshold_label: "Cumulative Min. Threshold (USD):",
    exclude_dust_label: "Filter Dust Attacks (1x micro-tx < $5)",
    filter_phishing_label: "Blacklist Phishing / Spam Airdrop Tokens",
    btn_trace_deposit: "Trace Deposit Inflows & Aggregate Senders",
    btn_tracing_deposit: "Scanning & Aggregating Inflows...",
    metric_qualified_senders: "Qualified Senders",
    metric_total_volume: "Cumulative Total Volume",
    metric_filtered_senders: "Filtered Senders (Spam/Dust)",
    metric_top_dominance: "Top Depositor Share",
    col_rank: "#",
    col_sender_address: "Sender Address",
    col_total_deposit: "Total Deposit (USD)",
    col_tx_count: "TX Count",
    col_first_deposit: "First Deposit",
    col_last_deposit: "Last Deposit",
    col_actions: "Actions",
    export_deposit_csv: "📥 Export GMGN CSV",
    copy_qualified_addrs: "📋 Copy Qualified Addresses",
    toggle_filtered_drawer: "🛡️ Filtered Senders Log (Spam/Dust)",
    btn_trace_tab3: "👉 Trace Relationship (Tab 3)",
    reason_below_min: "Below min threshold",
    reason_single_dust: "Single-tx dust attack (< $5)",
    reason_phishing: "Phishing / spam airdrop token",
    vault_warning: "⚠️ Smart Contract / Shared Vault Detected (Not Personal Deposit)",
    qualified_senders_title: "Qualified Senders Registry (Deposit Inflows)",
    filtered_senders_title: "Senders Excluded by Spam & Threshold Filters",
    // UI states, errors & helpers
    timeout_error: "The request timed out. Please try again in a moment.",
    generic_error: "Something went wrong while processing the request.",
    elapsed_hint: "Server processing time",
    scanning_protocols: "Scanning all protocols in parallel...",
    track_failed: "Transaction Not Found",
    network_error: "Network Error",
    checking_bytecode_on: "Checking bytecode & balance on",
    checking_bytecode_sub: "EIP-55 checksum • contract detection • native balance",
    invalid_addr_title: "Invalid Address",
    address_word: "Address",
    addresses_word: "addresses",
    batch_title_short: "Batch Analysis",
    batch_trimmed: "Maximum 20 addresses — the rest were ignored.",
    wallet_analysis_failed: "Wallet Analysis Failed",
    no_wallets_to_copy: "No wallets to copy yet.",
    no_wallets_to_export: "No wallets to export yet.",
    gmgn_wallet_list: "GMGN Wallet List",
    gmgn_csv_downloaded: "GMGN CSV downloaded!",
    enter_deposit_address: "Enter a valid deposit address!",
    paste_csv_data: "Paste CSV transaction data first!",
    deposit_scan_sub_solana: "Solana: scanning the 25 latest transactions (public RPC allows ~10 tx/10s, may take 30–40s)",
    deposit_scan_sub_multi: "Ethereum • Arbitrum • Base • Polygon • Optimism (in parallel)",
    deposit_failed: "Deposit Scan Failed",
    no_qualified_export: "No qualified addresses to export.",
    no_qualified: "No qualified addresses.",
    confirm_quit: "Close OmniRoute and stop the local server?",
    stopping_server: "Stopping server...",
    offline_title: "Server is Offline",
    offline_desc: "The local OmniRoute server was stopped or is inactive. If you stopped it intentionally, you can close this window.",
    reconnect: "Reconnect",
    close_window: "Close Window",
    checking: "Checking...",
    retry: "Retry",
    server_not_running: "Server not running. Start OmniRoute App and retry.",

    // Placeholders
    ph_tx: "Paste an explorer link (…/tx/0x…) or TX hash / Solana signature",
    ph_address: "0x… or Solana address",
    ph_genealogy: "Paste a wallet address (0x… or Solana) to trace funder & exits",
    ph_deposit: "Paste an exchange deposit address (0x… or Solana)",

    // How-it-works guides
    guide_label: "How it works",
    guide_tx_1: "Paste an explorer link / TX hash",
    guide_tx_2: "OmniRoute checks 5 sources at once",
    guide_tx_3: "Copy the destination / continue in Tab 3",
    guide_tx_tip: "Tip: pasting a link starts tracking automatically. You can also paste a wallet address to see its bridge history.",
    guide_addr_1: "Paste an address & pick a network",
    guide_addr_2: "Checks checksum, type & balance",
    guide_addr_3: "Make sure it isn't a contract before sending",
    guide_addr_tip: "Assets sent to the wrong contract address (router/pool) usually cannot be recovered.",
    guide_gen_1: "Paste 1 address, or 2–20 addresses (Mode B)",
    guide_gen_2: "See first funder, top senders & exit targets",
    guide_gen_3: "Export linked wallets to GMGN",
    guide_gen_tip: "CEX hot wallets (Binance, OKX, etc.) are excluded automatically so they never create fake clusters.",
    guide_dep_1: "Paste a deposit address, or a CSV (Mode B)",
    guide_dep_2: "Senders are grouped & valued in USD",
    guide_dep_3: "Spam/dust filtered out — export the rest",
    guide_dep_tip: "Auto-Detect scans 5 EVM chains at once. Ctrl+Enter submits the CSV box.",
    shortcuts_hint: "Shortcuts: Alt+1…4 switch tabs",
    first_funding_tx: "First Funding Tx",
    bridge_funding_tx: "Funded via Cross-Chain Bridge",
    cross_chain_badge: "CROSS-CHAIN",
    track_source_btn: "Trace Fund Source (Tab 1)",
    track_source_hint: "Open in Tab 1 to see the origin chain & the real sender wallet",
    bridge_funding_note: "The first funds came from a bridge/solver, not the original sender. Click to trace the origin chain and the real sender wallet.",
    origin_chain_label: "Origin chain",
    real_sender_label: "Real sender"
  }
};

// ==================== CORE UTILITIES ====================

// localStorage can throw (private mode / blocked storage) — never let that break the app.
const store = {
  get(key, fallback = null) {
    try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem(key, value); } catch { /* ignore */ }
  }
};

const ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ESC_MAP[ch]);
}

// Every string coming from the API is HTML-escaped once, here, so templates can interpolate
// API data safely into both text and attributes (token names / labels come from on-chain data).
function deepEscape(value) {
  if (typeof value === "string") return esc(value);
  if (Array.isArray(value)) return value.map(deepEscape);
  if (value && typeof value === "object") {
    const out = {};
    for (const k in value) out[k] = deepEscape(value[k]);
    return out;
  }
  return value;
}

// Reverse of esc() for values leaving the DOM (clipboard text, CSV files).
function unesc(value) {
  const ta = document.createElement("textarea");
  ta.innerHTML = String(value ?? "");
  return ta.value;
}

function t(key, fallback = "") {
  const dict = translations[currentLang] || translations.id;
  return dict[key] || translations.en[key] || fallback;
}

const REQUEST_TIMEOUT_MS = 90000;
const inflight = {};

// One in-flight request per key: a new lookup supersedes (aborts) the previous one,
// so rapid clicks / sample buttons never race each other.
async function apiFetch(key, url, opts = {}) {
  if (inflight[key]) inflight[key].abort();
  const ctrl = new AbortController();
  inflight[key] = ctrl;
  const timer = setTimeout(() => ctrl.abort(), REQUEST_TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      ...opts,
      signal: ctrl.signal,
      headers: { "Content-Type": "application/json", ...(opts.headers || {}) }
    });
    let data;
    try {
      data = await res.json();
    } catch {
      data = { success: false, error: `HTTP ${res.status}` };
    }
    return deepEscape(data);
  } catch (err) {
    if (inflight[key] !== ctrl) return null; // superseded by a newer request
    if (ctrl.signal.aborted) throw new Error(t("timeout_error"));
    throw err;
  } finally {
    clearTimeout(timer);
    if (inflight[key] === ctrl) delete inflight[key];
  }
}

const isBusy = key => Boolean(inflight[key]);
const postJSON = body => ({ method: "POST", body: JSON.stringify(body) });

function setLoading(btn, loading) {
  if (!btn) return;
  btn.disabled = loading;
  btn.classList.toggle("is-loading", loading);
  const text = btn.querySelector(".btn-text");
  const loader = btn.querySelector(".btn-loader");
  if (text) text.style.display = loading ? "none" : "inline-flex";
  if (loader) loader.style.display = loading ? "inline-flex" : "none";
}

function renderLoading(container, title, sub = "") {
  container.style.display = "block";
  container.innerHTML = `
    <div class="card state-card">
      <i class="fa-solid fa-circle-notch fa-spin text-lime state-icon"></i>
      <p class="state-title">${title}</p>
      ${sub ? `<p class="state-sub">${sub}</p>` : ""}
      <p class="state-timer" data-started="${Date.now()}">0.0s</p>
    </div>
  `;
  startLoadingTimer(container);
}

// Live elapsed counter in the loading card so long scans never look frozen.
function startLoadingTimer(container) {
  const el = container.querySelector(".state-timer");
  if (!el) return;
  const started = Number(el.dataset.started);
  const tick = () => {
    if (!el.isConnected) return;
    el.textContent = `${((Date.now() - started) / 1000).toFixed(1)}s`;
    requestAnimationFrame(() => setTimeout(tick, 100));
  };
  tick();
}

// `msg` must already be safe HTML (API errors are escaped by apiFetch).
function renderError(container, title, msg) {
  container.style.display = "block";
  container.innerHTML = `
    <div class="card error-card">
      <h3><i class="fa-solid fa-triangle-exclamation"></i> ${title}</h3>
      <p>${msg || t("generic_error")}</p>
    </div>
  `;
}

function elapsedBadge(ms) {
  if (!ms && ms !== 0) return "";
  return `<span class="elapsed-badge" title="${t("elapsed_hint")}"><i class="fa-solid fa-stopwatch"></i> ${(ms / 1000).toFixed(2)}s</span>`;
}

const SOLANA_ADDR_RE = /^(?!0x)[1-9A-HJ-NP-Za-km-z]{32,44}$/;

// Map any chain string ("Base", "base, ethereum", 8453-name…) to a <select> option value.
function pickChainOption(select, chain, address = "", fallback = "base") {
  if (!select) return;
  if (SOLANA_ADDR_RE.test(address) && [...select.options].some(o => o.value === "solana")) {
    select.value = "solana";
    return;
  }
  const lower = String(chain || "").toLowerCase();
  const values = [...select.options].map(o => o.value);
  select.value = values.find(v => lower.includes(v)) || (values.includes(fallback) ? fallback : values[0]);
}

let currentLang = store.get("omniroute_lang", "id");
let lastGenealogyData = null;
let lastBatchData = null;
let lastInspectData = null;

// Set Language & Translate UI
function setLanguage(lang) {
  currentLang = translations[lang] ? lang : "id";
  store.set("omniroute_lang", currentLang);
  document.body.setAttribute("data-lang", currentLang);
  document.documentElement.lang = currentLang;

  document.getElementById("langIdBtn")?.classList.toggle("active", currentLang === "id");
  document.getElementById("langEnBtn")?.classList.toggle("active", currentLang === "en");

  const dict = translations[currentLang];
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const val = dict[el.dataset.i18n];
    if (val) el.textContent = val;
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const val = dict[el.dataset.i18nPlaceholder];
    if (val) el.placeholder = val;
  });
  document.querySelectorAll("[data-i18n-title]").forEach(el => {
    const val = dict[el.dataset.i18nTitle];
    if (val) el.title = val;
  });

  const submitLabel = document.getElementById("submitGenealogyLabel");
  if (submitLabel) {
    submitLabel.textContent = currentDiscoveryMode === "batch" ? t("batch_btn_label") : t("btn_analyze_single");
  }

  // Re-render visible results in the new language without re-querying the server
  const visible = id => {
    const el = document.getElementById(id);
    return el && el.style.display !== "none" ? el : null;
  };
  const genealogyBox = visible("genealogyResultContainer");
  if (genealogyBox && currentDiscoveryMode === "single" && lastGenealogyData) renderGenealogyDashboard(lastGenealogyData, genealogyBox);
  if (genealogyBox && currentDiscoveryMode === "batch" && lastBatchData) renderBatchSybilDashboard(lastBatchData, genealogyBox);
  const addressBox = visible("addressResultContainer");
  if (addressBox && lastInspectData) renderAddressInspection(lastInspectData, addressBox);
  const depositBox = visible("depositResultContainer");
  if (depositBox && lastDepositData) renderDepositResults(lastDepositData, depositBox);
  const txBox = visible("txResultContainer");
  if (txBox && lastTxResult) renderTxResult(lastTxResult, txBox);
}

// Global Tab 4 state
let lastDepositData = null;
let currentDepositMode = "address";
let lastTxResult = null;

const TABS = {
  tx: ["tabBtnTx", "tabContentTx"],
  address: ["tabBtnAddress", "tabContentAddress"],
  genealogy: ["tabBtnGenealogy", "tabContentGenealogy"],
  deposit: ["tabBtnDeposit", "tabContentDeposit"]
};

// Tab Switching
function switchTab(tabId) {
  if (!TABS[tabId]) tabId = "tx";
  for (const [id, [btnId, sectionId]] of Object.entries(TABS)) {
    const active = id === tabId;
    const btn = document.getElementById(btnId);
    btn?.classList.toggle("active", active);
    btn?.setAttribute("aria-selected", String(active));
    document.getElementById(sectionId)?.classList.toggle("active", active);
  }
  store.set("omniroute_tab", tabId);
}

// Toast Notification
let toastTimer = null;
function showToast(message) {
  const toast = document.getElementById("toast");
  document.getElementById("toastMsg").textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}

// Clipboard Copy (values may arrive HTML-escaped from templates)
function copyToClipboard(text, label = "") {
  if (!text) return;
  const plain = unesc(text);
  const msg = `${unesc(label) || t("address_word", "Address")} ${t("copied_toast")}`;
  const fallback = () => {
    const ta = document.createElement("textarea");
    ta.value = plain;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
    showToast(msg);
  };
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(plain).then(() => showToast(msg), fallback);
  } else {
    fallback();
  }
}

function submitForm(formId) {
  document.getElementById(formId)?.requestSubmit();
}

// Clear input
function clearTxInput() {
  const input = document.getElementById("txInput");
  input.value = "";
  input.focus();
}

// Fill Address Input for quick testing
function fillAddress(addr, chain) {
  document.getElementById("addressInput").value = addr;
  if (chain) document.getElementById("chainSelect").value = chain;
  submitForm("addressVerifyForm");
}

// Load Samples
const sampleTxs = {
  relay: "https://robin.etherscan.io/tx/0x2a17e404fed1a1bdc3c97bcc7249f4a5c1dd1c65be59b608dd1d32b395f91031",
  lifi: "https://bscscan.com/tx/0xda166887e41e61838ae518bedc05c7735270f84d7ac89ebe290986747fb65cec"
};

function loadSample(type) {
  document.getElementById("txInput").value = sampleTxs[type] || sampleTxs.relay;
  switchTab("tx");
  submitForm("txTrackForm");
}

function truncateAddress(addr, len = 6) {
  if (!addr || addr.length <= len * 2 + 3) return addr || "";
  return `${addr.slice(0, len + 2)}...${addr.slice(-len)}`;
}

function fmtUsd(n) {
  return Number(n || 0).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}


// ==================== TX TRACKER HANDLER ====================
async function handleTxSubmit(e) {
  e.preventDefault();
  const query = document.getElementById("txInput").value.trim();
  if (!query) return;

  const btn = document.getElementById("btnSubmitTx");
  const container = document.getElementById("txResultContainer");
  store.set("omniroute_last_tx", query);

  setLoading(btn, true);
  renderLoading(container, t("scanning_protocols"), "Relay.link &bull; Li.Fi &bull; Jumper &bull; Across &bull; LayerZero &bull; EVM RPC");

  try {
    const result = await apiFetch("tx", "/api/track", postJSON({ query }));
    if (!result) return; // superseded
    if (!result.success) {
      renderError(container, t("track_failed"), result.error);
      return;
    }
    lastTxResult = result;
    renderTxResult(result, container);
  } catch (err) {
    renderError(container, t("network_error"), esc(err.message));
  } finally {
    if (!isBusy("tx")) setLoading(btn, false);
  }
}

function renderTxResult(result, container) {
  if (result.query_type === "transaction") {
    renderTxBreakdown(result.data, container, result.elapsed_ms);
  } else if (result.query_type === "wallet_history") {
    renderWalletHistory(result, container);
  } else if (result.query_type === "address_inspection") {
    renderAddressInspection(result.data, container, result.message);
  }
}


// Render Transaction Breakdown
function renderTxBreakdown(tx, container, elapsedMs) {
  const dict = translations[currentLang] || translations.id;
  const isSuccess = (tx.status || "").toLowerCase() === "success" || (tx.status || "").toLowerCase() === "done" || (tx.status || "").toLowerCase() === "completed";
  const originChain = tx.origin_chain || {};
  const destChain = tx.destination_chain || {};
  const asset = tx.asset || {};
  const protocolName = tx.protocol_badge || tx.protocol || "Cross-Chain Route";

  container.innerHTML = `
    <!-- Status Banner -->
    <div class="status-banner" style="${isSuccess ? '' : 'background: rgba(251, 191, 36, 0.1); border-color: rgba(251, 191, 36, 0.3);'}">
      <div class="status-badge-group">
        <div class="status-indicator" style="${isSuccess ? '' : 'background: var(--accent-amber); box-shadow: 0 0 12px var(--accent-amber);'}"></div>
        <span class="status-title" style="${isSuccess ? '' : 'color: var(--accent-amber);'}">
          ${dict.status_label} ${tx.status ? tx.status.toUpperCase() : 'CONFIRMED'}
        </span>
        <span class="proto-badge-result">
          <i class="fa-solid fa-cube text-lime"></i> ${protocolName}
        </span>
      </div>
      <div class="status-meta" style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono);">
        ${tx.created_at ? `<i class="fa-regular fa-clock"></i> ${new Date(unesc(tx.created_at)).toLocaleString(currentLang === 'id' ? 'id-ID' : 'en-US', { timeZoneName: 'short' })}` : ''}
        ${elapsedBadge(elapsedMs)}
      </div>
    </div>

    <!-- 3-STEP BREAKDOWN FLOW -->
    <div class="breakdown-flow-section">
      <h3 class="flow-title">
        <i class="fa-solid fa-arrows-turn-to-dots text-lime"></i>
        <span>${currentLang === 'id' ? 'Alur Breakdown Transaksi' : 'Transaction Route Breakdown'}</span>
      </h3>

      <div class="flow-cards-grid">
        <!-- STEP 1: FROM WALLET -->
        <div class="flow-card sender-card">
          <div class="card-step-badge">
            <i class="fa-solid fa-circle-1"></i> ${dict.step1_title}
          </div>
          <div class="chain-info-row">
            <span class="chain-badge">
              ${originChain.icon ? `<img src="${originChain.icon}" class="chain-icon-img" alt="${originChain.display_name}">` : '<i class="fa-solid fa-cubes text-lime"></i>'}
              ${originChain.display_name || 'Origin Chain'}
            </span>
          </div>
          <div class="address-box">
            <div class="address-text" title="${tx.from_wallet}">${tx.from_wallet || 'Unknown'}</div>
          </div>
          <div class="card-detail-line" style="flex-direction: column; align-items: flex-start; gap: 4px;">
            <div style="display: flex; justify-content: space-between; width: 100%; align-items: baseline;">
              <span style="font-size: 0.8rem; color: var(--text-muted);">${dict.send_label || 'Sent Asset:'}</span>
              <strong style="color: var(--accent-cyan); font-size: 1.05rem;">
                ${(tx.sent_asset && tx.sent_asset.amount) || asset.amount || '0'} 
                <span style="font-size: 0.82rem; color: #fff;">${(tx.sent_asset && tx.sent_asset.symbol) || asset.symbol || ''}</span>
              </strong>
            </div>
            <div style="display: flex; justify-content: space-between; width: 100%; font-size: 0.76rem; color: var(--text-dim);">
              <span>${(tx.sent_asset && tx.sent_asset.name) || 'Origin Asset'}</span>
              ${(tx.sent_asset && tx.sent_asset.amount_usd) ? `<span style="color: var(--accent-cyan); font-weight: 600;">~$${Number(tx.sent_asset.amount_usd).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</span>` : ''}
            </div>
          </div>
          <div class="address-actions">
            <button class="icon-action-btn" data-copy="${tx.from_wallet}" data-copy-label="${dict.step1_title}">
              <i class="fa-regular fa-copy"></i> ${dict.copy_btn}
            </button>
            ${originChain.sender_explorer_url ? `
              <a href="${originChain.sender_explorer_url}" target="_blank" rel="noopener noreferrer" class="icon-action-btn">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> ${dict.explorer_btn}
              </a>
            ` : ''}
          </div>
        </div>

        <!-- ARROW -->
        <div class="flow-arrow-col">
          <i class="fa-solid fa-chevron-right text-lime"></i>
        </div>

        <!-- STEP 2: ROUTER / SOLVER / BRIDGE -->
        <div class="flow-card solver-card">
          <div class="card-step-badge">
            <i class="fa-solid fa-circle-2"></i> ${dict.step2_title}
          </div>
          <div class="chain-info-row">
            <span class="chain-badge" style="background: rgba(192, 132, 252, 0.15); color: var(--accent-purple);">
              <i class="fa-solid fa-network-wired"></i> ${tx.depository_label || 'Bridge Router'}
            </span>
          </div>
          <div class="address-box">
            <div class="address-text" style="font-size: 0.82rem; color: #e9d5ff;" title="${tx.depository_contract}">
              ${tx.depository_contract || 'Cross-Chain Protocol'}
            </div>
          </div>
          <div class="card-detail-line">
            <span>${dict.protocol_label}</span>
            <strong style="color: var(--accent-purple);">${tx.protocol || 'Bridge / Aggregator'}</strong>
          </div>
          <div class="address-actions">
            <button class="icon-action-btn" data-copy="${tx.depository_contract}" data-copy-label="Router / Solver">
              <i class="fa-regular fa-copy"></i> ${dict.copy_btn}
            </button>
            ${originChain.depository_explorer_url ? `
              <a href="${originChain.depository_explorer_url}" target="_blank" rel="noopener noreferrer" class="icon-action-btn">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> ${dict.contract_btn}
              </a>
            ` : ''}
          </div>
        </div>

        <!-- ARROW -->
        <div class="flow-arrow-col">
          <i class="fa-solid fa-chevron-right text-lime"></i>
        </div>

        <!-- STEP 3: DESTINATION WALLET - CLEAN & PROMINENT ELECTRIC LIME -->
        <div class="flow-card target-card">
          <div class="card-step-badge">
            <i class="fa-solid fa-circle-3"></i> ${dict.step3_title}
          </div>
          <div class="chain-info-row">
            <span class="chain-badge" style="background: var(--accent-lime-dim); color: var(--accent-lime); border: 1px solid var(--border-lime);">
              ${destChain.icon ? `<img src="${destChain.icon}" class="chain-icon-img" alt="${destChain.display_name}">` : '<i class="fa-solid fa-layer-group"></i>'}
              ${destChain.display_name || 'Destination Chain'}
            </span>
          </div>
          <div class="address-box" style="border-color: var(--accent-lime); background: rgba(0, 0, 0, 0.65);">
            <div class="address-text" title="${tx.to_wallet_tujuan}">
              ${tx.to_wallet_tujuan || 'Pending / In-Transit'}
            </div>
          </div>
          <div class="card-detail-line" style="flex-direction: column; align-items: flex-start; gap: 4px;">
            <div style="display: flex; justify-content: space-between; width: 100%; align-items: baseline;">
              <span style="font-size: 0.8rem; color: var(--text-muted);">${dict.received_asset_label || 'Recipient Asset:'}</span>
              <strong class="text-lime" style="font-size: 1.05rem;">
                ${(tx.recipient_asset && tx.recipient_asset.amount) || (tx.sent_asset && tx.sent_asset.amount) || asset.amount || '0'} 
                <span style="font-size: 0.82rem; color: #fff;">${(tx.recipient_asset && tx.recipient_asset.symbol) || (tx.sent_asset && tx.sent_asset.symbol) || asset.symbol || ''}</span>
              </strong>
            </div>
            <div style="display: flex; justify-content: space-between; width: 100%; font-size: 0.76rem; color: var(--text-dim);">
              <span>${(tx.recipient_asset && tx.recipient_asset.name) || 'Destination Asset'}</span>
              ${(tx.recipient_asset && tx.recipient_asset.amount_usd) ? `<span style="color: var(--accent-lime); font-weight: 600;">~$${Number(tx.recipient_asset.amount_usd).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</span>` : ''}
            </div>
          </div>
          <div class="card-detail-line" style="margin-top: 4px;">
            <span>${currentLang === 'id' ? 'Status Penerima:' : 'Recipient Status:'}</span>
            <span style="color: var(--text-pure); font-weight: 600;">${dict.received_status} ${destChain.display_name || 'Destination'}</span>
          </div>

          <!-- Received Transaction Hash (Fill / Settlement) Row -->
          ${destChain.tx_hash ? `
            <div class="fill-tx-box">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 0.72rem; font-weight: 800; color: var(--accent-lime); text-transform: uppercase; letter-spacing: 0.5px;">
                  <i class="fa-solid fa-receipt"></i> ${dict.received_tx_label || (currentLang === 'id' ? 'Tx Penerimaan (Fill):' : 'Received Tx (Fill):')}
                </span>
                ${destChain.tx_explorer_url ? `
                  <a href="${destChain.tx_explorer_url}" target="_blank" rel="noopener noreferrer" style="font-size: 0.73rem; color: var(--accent-lime); text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                    <span>${destChain.display_name} Explorer</span> <i class="fa-solid fa-arrow-up-right-from-square"></i>
                  </a>
                ` : ''}
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #fff; word-break: break-all;" title="${destChain.tx_hash}">
                  ${truncateAddress(destChain.tx_hash, 10)}
                </span>
                <button class="icon-action-btn-mini" data-copy="${destChain.tx_hash}" data-copy-label="${dict.received_tx_label || 'Tx Hash'}" title="${dict.copy_fill_tx || 'Salin Tx Hash'}">
                  <i class="fa-regular fa-copy"></i>
                </button>
              </div>
            </div>
          ` : ''}

          <div class="address-actions" style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px;">
            <button class="icon-action-btn primary" data-copy="${tx.to_wallet_tujuan}" data-copy-label="${dict.step3_title}">
              <i class="fa-solid fa-copy"></i> ${dict.copy_target_btn}
            </button>
            ${destChain.recipient_explorer_url ? `
              <a href="${destChain.recipient_explorer_url}" target="_blank" rel="noopener noreferrer" class="icon-action-btn" title="${dict.explorer_wallet_btn || 'Wallet Explorer'}">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> ${dict.explorer_wallet_btn || (currentLang === 'id' ? 'Explorer Dompet' : 'Wallet Explorer')}
              </a>
            ` : ''}
            ${destChain.tx_explorer_url ? `
              <a href="${destChain.tx_explorer_url}" target="_blank" rel="noopener noreferrer" class="icon-action-btn fill-highlight-btn" title="${dict.fill_tx_btn || 'Received Tx ↗'}">
                <i class="fa-solid fa-receipt"></i> ${dict.fill_tx_btn || (currentLang === 'id' ? 'Tx Penerimaan ↗' : 'Received Tx ↗')}
              </a>
            ` : ''}
            <button class="icon-action-btn auto-analyze-btn" data-action="analyze-dest" data-addr="${tx.to_wallet_tujuan}" data-chain="${destChain.name || destChain.id || 'base'}" title="Lacak riwayat alur kas keluar dompet tujuan ini">
              <i class="fa-solid fa-bolt text-lime"></i> <span>${dict.analyze_flow_btn || '👉 Analyze Wallet Flow &rarr;'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- DETAIL METRICS -->
    <div class="details-grid">
      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_amount || 'Cross-Chain Asset Flow'}</div>
        <div class="metric-value text-lime" style="font-size: 0.95rem; display: flex; flex-direction: column; gap: 4px;">
          <div>
            <span style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;">Sent:</span>
            <strong>${(tx.sent_asset && tx.sent_asset.amount) || '0'}</strong> <span style="font-size: 0.8rem; color: #fff;">${(tx.sent_asset && tx.sent_asset.symbol) || ''}</span>
          </div>
          <div>
            <span style="font-size: 0.72rem; color: var(--accent-lime); text-transform: uppercase;">Received:</span>
            <strong style="color: var(--accent-lime);">${(tx.recipient_asset && tx.recipient_asset.amount) || '0'}</strong> <span style="font-size: 0.8rem; color: #fff;">${(tx.recipient_asset && tx.recipient_asset.symbol) || ''}</span>
          </div>
        </div>
        <div class="metric-sub">${(tx.recipient_asset && tx.recipient_asset.name) || (tx.sent_asset && tx.sent_asset.name) || 'Cross-Chain Route'}</div>
      </div>

      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_origin_tx}</div>
        <div class="metric-value" style="font-size: 0.88rem; font-family: var(--font-mono);">
          ${truncateAddress(originChain.tx_hash, 10)}
        </div>
        <div class="metric-sub">
          ${originChain.tx_explorer_url ? `<a href="${originChain.tx_explorer_url}" target="_blank" style="color: var(--accent-lime); text-decoration: none; font-weight: 700;"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${originChain.display_name} Explorer</a>` : ''}
        </div>
      </div>

      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_dest_tx}</div>
        <div class="metric-value text-lime" style="font-size: 0.88rem; font-family: var(--font-mono);">
          ${destChain.tx_hash ? truncateAddress(destChain.tx_hash, 10) : (currentLang === 'id' ? 'Terselesaikan on-chain' : 'Settled on-chain')}
        </div>
        <div class="metric-sub">
          ${destChain.tx_explorer_url ? `<a href="${destChain.tx_explorer_url}" target="_blank" style="color: var(--accent-lime); text-decoration: none; font-weight: 700;"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${destChain.display_name} Explorer</a>` : (destChain.recipient_explorer_url ? `<a href="${destChain.recipient_explorer_url}" target="_blank" style="color: var(--text-dim); text-decoration: none;"><i class="fa-solid fa-wallet"></i> ${destChain.display_name} Account</a>` : '')}
        </div>
      </div>
    </div>
  `;
}

// Render Wallet History
function renderWalletHistory(res, container) {
  const items = res.data || [];
  const dict = translations[currentLang] || translations.id;

  container.innerHTML = `
    <div class="card" style="margin-bottom: 20px;">
      <h3 class="card-title" style="margin-bottom: 8px;">
        <i class="fa-solid fa-list-check text-lime"></i> ${currentLang === 'id' ? 'Riwayat Swap / Bridge Wallet' : 'Wallet Cross-Chain History'} (${items.length})
      </h3>
      <p style="color: var(--text-muted); font-size: 0.9rem;">
        ${currentLang === 'id' ? 'Alamat dompet' : 'Wallet address'}: <code class="text-lime" style="font-family: var(--font-mono);">${res.address}</code>
      </p>
    </div>

    <div style="display: flex; flex-direction: column; gap: 16px;">
      ${items.map(item => `
        <div class="card" style="padding: 22px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <span class="chain-badge">
              ${item.origin_chain.display_name} ➔ ${item.destination_chain.display_name}
            </span>
            <span class="text-lime" style="font-weight: 800; font-size: 0.95rem;">
              ${item.asset.amount} ${item.asset.symbol}
            </span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; background: rgba(0,0,0,0.4); padding: 12px 16px; border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div>
              <span style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase; font-weight: 800;">${dict.step3_title}:</span>
              <div class="text-lime" style="font-family: var(--font-mono); font-weight: 700; font-size: 0.95rem; margin-top: 2px;">
                ${item.to_wallet_tujuan}
              </div>
            </div>
            <button class="icon-action-btn" data-copy="${item.to_wallet_tujuan}" data-copy-label="${dict.step3_title}">
              <i class="fa-regular fa-copy"></i> ${dict.copy_btn}
            </button>
          </div>
          <div style="margin-top: 12px; font-size: 0.82rem; display: flex; gap: 18px;">
            ${item.origin_chain.tx_explorer_url ? `<a href="${item.origin_chain.tx_explorer_url}" target="_blank" style="color: #fff; text-decoration: none;"><i class="fa-solid fa-arrow-up-right-from-square"></i> Origin Tx</a>` : ''}
            ${item.destination_chain.tx_explorer_url ? `<a href="${item.destination_chain.tx_explorer_url}" target="_blank" style="color: var(--accent-lime); text-decoration: none; font-weight: 700;"><i class="fa-solid fa-arrow-up-right-from-square"></i> Dest Tx</a>` : ''}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// Render Address Inspection
function renderAddressInspection(data, container, customMsg = "") {
  lastInspectData = data;
  const isContract = data.is_contract;
  const dict = translations[currentLang] || translations.id;
  const targetLabel = data.target_type || (isContract ? dict.target_contract : dict.target_eoa);

  container.innerHTML = `
    ${customMsg ? `<div class="card" style="margin-bottom: 16px; background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.3);"><p style="color: var(--accent-amber); font-size: 0.9rem;">${customMsg}</p></div>` : ''}
    <div class="inspect-card">
      <div class="inspect-header">
        <div>
          <span class="target-badge-lg ${isContract ? 'contract' : 'eoa'}">
            <i class="fa-solid ${isContract ? 'fa-cube' : 'fa-user-shield'}"></i>
            ${targetLabel}
          </span>
          ${data.known_protocol ? `<span class="target-badge-lg" style="background: var(--accent-lime-dim); color: var(--accent-lime); border: 1px solid var(--border-lime); margin-left: 6px;"><i class="fa-solid fa-certificate"></i> ${data.known_protocol}</span>` : ''}
        </div>
        <div>
          <span class="chain-badge">${data.chain || 'EVM'}</span>
        </div>
      </div>

      <div class="details-grid">
        <div class="detail-metric-card" style="grid-column: span 2;">
          <div class="metric-label">${dict.checksum_official}</div>
          <div class="metric-value text-lime" style="font-size: 0.96rem;">
            ${data.checksum_address || data.address}
          </div>
          <div class="address-actions" style="margin-top: 12px;">
            <button class="icon-action-btn" data-copy="${data.checksum_address || data.address}" data-copy-label="${dict.checksum_official}">
              <i class="fa-regular fa-copy"></i> ${dict.copy_btn}
            </button>
            ${data.explorer_url ? `<a href="${data.explorer_url}" target="_blank" class="icon-action-btn"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${dict.open_in_explorer}</a>` : ''}
          </div>
        </div>

        <div class="detail-metric-card">
          <div class="metric-label">${dict.addr_type}</div>
          <div class="metric-value" style="font-size: 1.05rem; color: ${isContract ? 'var(--accent-amber)' : 'var(--accent-lime)'};">
            ${isContract ? (dict.smart_contract_router || 'Smart Contract Router') : (dict.regular_user_wallet || 'Dompet Biasa (EOA)')}
          </div>
          <div class="metric-sub">${isContract ? (dict.bytecode_detected || 'Bytecode terdeteksi on-chain') : (dict.individual_wallet || 'Alamat dompet perseorangan')}</div>
        </div>

        <div class="detail-metric-card">
          <div class="metric-label">${dict.native_balance}</div>
          <div class="metric-value text-lime">
            ${data.native_balance || 'N/A'}
          </div>
          <div class="metric-sub">${dict.balance_sub}</div>
        </div>
      </div>
    </div>
  `;
}

// ==================== ADDRESS VERIFIER HANDLER ====================
async function handleAddressSubmit(e) {
  e.preventDefault();
  const address = document.getElementById("addressInput").value.trim();
  const chain = document.getElementById("chainSelect").value;
  if (!address) return;

  const btn = document.getElementById("btnSubmitAddress");
  const container = document.getElementById("addressResultContainer");
  const chainName = document.getElementById("chainSelect").selectedOptions[0]?.textContent || chain;

  setLoading(btn, true);
  renderLoading(container, `${t("checking_bytecode_on")} ${esc(chainName)}...`, t("checking_bytecode_sub"));

  try {
    const result = await apiFetch("address", "/api/inspect", postJSON({ address, chain }));
    if (!result) return;
    if (!result.success || !result.data.is_valid) {
      renderError(container, t("invalid_addr_title"), result.data ? result.data.error : result.error);
      return;
    }
    renderAddressInspection(result.data, container);
  } catch (err) {
    renderError(container, t("network_error"), esc(err.message));
  } finally {
    if (!isBusy("address")) setLoading(btn, false);
  }
}


// ==================== WALLET GENEALOGY & SYBIL CLUSTER HANDLERS ====================

let currentDiscoveryMode = "single";
let currentLinkedWallets = [];
let currentTargetAddress = "";
let currentSelectedChain = "base";

function setDiscoveryMode(mode) {
  currentDiscoveryMode = mode === "batch" ? "batch" : "single";
  const isBatch = currentDiscoveryMode === "batch";
  document.getElementById("btnModeSingle")?.classList.toggle("active", !isBatch);
  document.getElementById("btnModeBatch")?.classList.toggle("active", isBatch);
  document.getElementById("singleInputGroup").style.display = isBatch ? "none" : "flex";
  document.getElementById("batchInputGroup").style.display = isBatch ? "block" : "none";
  const submitLabel = document.getElementById("submitGenealogyLabel");
  if (submitLabel) submitLabel.textContent = isBatch ? t("batch_btn_label") : t("btn_analyze_single");
}

function fillBatchSample() {
  setDiscoveryMode("batch");
  document.getElementById("genealogyBatchInput").value = [
    "0x0532da9a4248daa5a48b4d7c6c1c8fe447b1320a",
    "0x826600c3b88b0a9443260c6d7d427d142194553b",
    "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"
  ].join("\n");
  switchTab("genealogy");
  submitForm("genealogyForm");
}

function downloadCsv(filename, rows) {
  const csv = rows.map(r => r.map(cell => {
    const v = unesc(cell);
    return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
  }).join(",")).join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// GMGN Export Actions
function copyWalletsForGmgn() {
  if (!currentLinkedWallets.length) {
    showToast(t("no_wallets_to_copy"));
    return;
  }
  copyToClipboard(currentLinkedWallets.map(w => w.address).join("\n"), t("gmgn_wallet_list"));
}

function downloadGmgnCsv(identityName = "OmniRoute", chainName = "") {
  if (!currentLinkedWallets.length) {
    showToast(t("no_wallets_to_export"));
    return;
  }
  const cleanId = unesc(identityName || "Cluster").slice(0, 10).replace(/[^a-zA-Z0-9_]/g, "") || "Cluster";
  const defaultChain = unesc(chainName || currentSelectedChain || "base");
  const rows = [["Address", "Tag", "Chain"]].concat(currentLinkedWallets.map(w => [
    w.address, `${cleanId}_${(w.role || "Linked").replace(/,/g, "_")}`, w.chain || defaultChain
  ]));
  downloadCsv(`${cleanId}_${defaultChain}_gmgn_watchlist.csv`, rows);
  showToast(`${t("gmgn_csv_downloaded")} (${defaultChain.toUpperCase()})`);
}


function renderGmgnToolbar(wallets, identityName, chain = "base", confidenceScore = null, riskLevel = "") {
  currentLinkedWallets = wallets || [];
  currentTargetAddress = identityName || "";
  currentSelectedChain = chain || "base";
  const dict = translations[currentLang] || translations.id;

  let confBadge = "";
  if (confidenceScore !== null && confidenceScore !== undefined) {
    let confClass = "high";
    let confText = dict.confidence_high || "HIGH";
    if (confidenceScore === 0) {
      confClass = "none";
      confText = dict.confidence_none || "NO RELATION (Independent)";
    } else if (confidenceScore <= 25) {
      confClass = "low";
      confText = dict.confidence_low || "LOW / CEX INFRASTRUCTURE";
    } else if (confidenceScore <= 75) {
      confClass = "medium";
      confText = dict.confidence_med || "MEDIUM";
    }
    confBadge = `
      <div class="confidence-badge-pill ${confClass}">
        <i class="fa-solid fa-gauge-high"></i>
        <span>${dict.cluster_confidence_label || 'Confidence:'} <strong>${confidenceScore}%</strong> (${confText})</span>
      </div>
    `;
  }

  return `
    <div class="gmgn-toolbar">
      <!-- Copy-Trade Risk Disclaimer (Probabilistic Heuristic Notice) -->
      <div class="gmgn-disclaimer">
        <i class="fa-solid fa-triangle-exclamation text-amber"></i>
        <span>${dict.gmgn_disclaimer_text}</span>
      </div>

      <div class="gmgn-bar-row">
        <div class="gmgn-info">
          <div class="gmgn-badge-wrap">
            <i class="fa-solid fa-crosshairs text-lime" style="font-size: 1.1rem;"></i>
            <span style="font-weight: 800; color: #fff;">${dict.gmgn_sync_label || 'GMGN Watchlist Sync:'}</span>
            <span class="gmgn-count-pill">${currentLinkedWallets.length} ${currentLang === 'id' ? 'Dompet Terhubung' : 'Linked Wallets'}</span>
          </div>
          ${confBadge}
        </div>
        <div class="gmgn-actions">
          <button type="button" class="btn-gmgn-copy" onclick="copyWalletsForGmgn()" title="Format baris baru tanpa kutip, siap paste langsung ke GMGN Watchlist">
            <i class="fa-regular fa-clipboard"></i> <span>${dict.copy_for_gmgn || '📋 Copy for GMGN'}</span>
          </button>
          <button type="button" class="btn-gmgn-csv" data-action="gmgn-csv" data-id="${identityName}" data-chain="${chain}" title="Unduh file CSV Address,Tag,Chain untuk import massal GMGN">
            <i class="fa-solid fa-file-arrow-down"></i> <span>${dict.export_gmgn_csv || '📥 Export GMGN CSV'}</span>
          </button>
        </div>
      </div>
    </div>
  `;
}

// Tab 1 / Tab 4 → Tab 3 hand-off: open the wallet in the relationship tracer and run it.
function openInGenealogy(address, chain) {
  address = unesc(address || "");
  if (!address || address === "Pending / In-Transit") return;
  setDiscoveryMode("single");
  document.getElementById("genealogyInput").value = address;
  pickChainOption(document.getElementById("genealogyChainSelect"), unesc(chain), address);
  switchTab("genealogy");
  submitForm("genealogyForm");
  document.getElementById("tabContentGenealogy")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

const autoAnalyzeDestination = openInGenealogy;

// Tab 3 → Tab 1 hand-off: trace where a funding tx (e.g. a bridge fill) originally came from.
function trackTxInTab1(txHash) {
  txHash = unesc(txHash || "");
  if (!txHash) return;
  document.getElementById("txInput").value = txHash;
  switchTab("tx");
  submitForm("txTrackForm");
  document.getElementById("tabContentTx")?.scrollIntoView({ behavior: "smooth", block: "start" });
}
const autoTraceDepositSender = openInGenealogy;

// Quick Sample for Tab 3
function fillGenealogy(address, chain) {
  setDiscoveryMode("single");
  document.getElementById("genealogyInput").value = address;
  if (chain) document.getElementById("genealogyChainSelect").value = chain;
  switchTab("genealogy");
  submitForm("genealogyForm");
}

// Handle Genealogy & Sybil Form Submission
async function handleGenealogySubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const btn = document.getElementById("btnSubmitGenealogy");
  const container = document.getElementById("genealogyResultContainer");
  const chain = document.getElementById("genealogyChainSelect").value;
  currentSelectedChain = chain;
  const isBatch = currentDiscoveryMode === "batch";

  let request;
  if (isBatch) {
    const raw = document.getElementById("genealogyBatchInput").value || "";
    const addresses = [...new Set(raw.split(/[\s,;]+/).map(a => a.trim()).filter(a => a.length >= 20))];
    if (addresses.length < 2) {
      renderError(container, t("batch_title_short"), t("batch_min_error"));
      return;
    }
    if (addresses.length > 20) showToast(t("batch_trimmed"));
    request = { url: "/api/wallet/batch-sybil", body: { addresses: addresses.slice(0, 20), chain } };
    renderLoading(container, `${t("batch_scanning_title")} (${Math.min(addresses.length, 20)} ${t("wallets_checked_suffix")})`, t("batch_scanning_sub"));
  } else {
    const address = document.getElementById("genealogyInput").value.trim();
    if (!address) return;
    if (SOLANA_ADDR_RE.test(address) && chain !== "solana") {
      document.getElementById("genealogyChainSelect").value = "solana";
    }
    request = { url: "/api/wallet/genealogy", body: { address, chain: SOLANA_ADDR_RE.test(address) ? "solana" : chain } };
    renderLoading(container, t("btn_analyzing"), "Genesis Gas Provider &bull; Clean Verified Capital &bull; CEX Exit Destinations");
  }

  setLoading(btn, true);
  try {
    const result = await apiFetch("genealogy", request.url, postJSON(request.body));
    if (!result) return;
    if (!result.success) {
      renderError(container, t("wallet_analysis_failed"), result.error);
      return;
    }
    if (isBatch) renderBatchSybilDashboard(result, container);
    else renderGenealogyDashboard(result, container);
  } catch (err) {
    renderError(container, t("network_error"), esc(err.message));
  } finally {
    if (!isBusy("genealogy")) setLoading(btn, false);
  }
}


// Render Single Wallet Genealogy Dashboard (2-Column Cyberpunk Grid + GMGN Toolbar)
function renderGenealogyDashboard(data, container) {
  lastGenealogyData = data;
  const dict = translations[currentLang] || translations.id;
  const genesis = data.genesisFunder;
  const inflows = data.topInflows || [];
  const outflows = data.topOutflows || [];
  const riskFlags = data.riskFlags || [];
  const exitPattern = data.exitPattern || "Private Transfers / In-Transit";
  const linkedWallets = data.linkedWallets || [];
  const chainKey = data.chainKey || 'base';

  const maxInflow = (inflows.length > 0 && inflows[0].totalAmount > 0) ? inflows[0].totalAmount : 1;
  const maxOutflow = (outflows.length > 0 && outflows[0].totalAmount > 0) ? outflows[0].totalAmount : 1;

  container.innerHTML = `
    <div class="genealogy-dashboard">
      <!-- GMGN Export Toolbar -->
      ${renderGmgnToolbar(linkedWallets, data.targetAddress, chainKey, 95, 'SINGLE')}

      <!-- Header Summary Card -->
      <div class="genealogy-header-card">
        <div class="genealogy-target-row">
          <div class="genealogy-target-info">
            <span class="chain-badge">
              <i class="fa-solid fa-network-wired text-lime"></i> ${data.chain || 'EVM'}
            </span>
            <span class="genealogy-addr-pill" title="${data.targetAddress}">
              ${data.targetAddress}
            </span>
            <button class="icon-action-btn" data-copy="${data.targetAddress}" data-copy-label="${dict.col_wallet_addr}">
              <i class="fa-regular fa-copy"></i> ${dict.copy_btn}
            </button>
          </div>
          <div>
            <span class="proto-badge-result">
              <i class="fa-solid fa-chart-line text-lime"></i> ${data.totalTransactions || 0} ${dict.clean_txs_label || 'Clean Txs'}
            </span>
          </div>
        </div>

        <!-- Risk Flags Bar -->
        <div class="risk-flags-bar">
          <span class="risk-flags-label">Genealogy & Risk Indicators:</span>
          ${riskFlags.length > 0 ? riskFlags.map(rf => {
            const isDanger = rf.includes("Mixer") || rf.includes("Fresh");
            const isWarning = rf.includes("CEX") || rf.includes("Bridge") || rf.includes("Faucet");
            const cls = isDanger ? 'danger' : (isWarning ? 'warning' : 'safe');
            const icon = isDanger ? 'fa-triangle-exclamation' : (isWarning ? 'fa-building-columns' : 'fa-check');
            return `<span class="risk-pill ${cls}"><i class="fa-solid ${icon}"></i> ${rf}</span>`;
          }).join('') : `<span class="risk-pill safe"><i class="fa-solid fa-shield-check"></i> Clean Activity</span>`}
        </div>
      </div>

      <!-- 2-Column Cyberpunk Grid -->
      <div class="genealogy-grid">
        <!-- COLUMN 1: GENESIS & FUNDING SOURCE (INFLOW TRACKING) -->
        <div class="genealogy-col-card inflow">
          <div class="col-header">
            <div class="col-header-title inflow">
              <span class="pulsing-indicator lime"></span>
              <span>${dict.genesis_inflow_title || 'Genesis & Inflow Source (Modal Awal)'}</span>
            </div>
            <span class="proto-tag" style="border-color: rgba(158, 255, 0, 0.3);">
              <i class="fa-solid fa-arrow-down-left text-lime"></i> INFLOW
            </span>
          </div>

          <!-- First Funder (Initial Gas Provider) -->
          ${genesis ? `
            <div class="funder-box">
              <div class="funder-top-row">
                <span class="funder-label-tag"><i class="fa-solid fa-seedling text-lime"></i> ${dict.funder_gas_title || 'FIRST FUNDER (GAS PROVIDER)'}</span>
                ${genesis.label ? `<span class="funder-entity-badge">${genesis.label}</span>` : ''}
              </div>
              <div class="funder-addr" title="${genesis.address}" style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                <span style="font-family: var(--font-mono); word-break: break-all;">${genesis.address}</span>
                <button class="icon-action-btn-mini" data-copy="${genesis.address}" data-copy-label="${dict.funder_gas_title || 'Genesis Funder'}" title="Copy funder address" style="flex-shrink: 0;">
                  <i class="fa-regular fa-copy"></i>
                </button>
              </div>
              <div class="funder-meta-row">
                <div class="funder-amount">
                  ${genesis.amount && genesis.amount !== "-" ? `+${genesis.amount} ${genesis.tokenSymbol}` : (currentLang === "id" ? "Pembayar fee / pembuat akun" : "Fee payer / account creator")}
                </div>
                <div class="funder-time">
                  ${genesis.days_ago !== undefined ? `<i class="fa-regular fa-clock"></i> ${genesis.days_ago} ${dict.days_ago_suffix || 'hari lalu'}` : ''}
                </div>
              </div>
              ${genesis.txHash ? `
                <div class="funding-tx-box ${genesis.isBridge ? 'is-bridge' : ''}">
                  <div class="funding-tx-head">
                    <span class="funding-tx-label">
                      <i class="fa-solid ${genesis.isBridge ? 'fa-bridge-water' : 'fa-receipt'}"></i>
                      ${genesis.isBridge ? t("bridge_funding_tx") : t("first_funding_tx")}
                    </span>
                    ${genesis.isBridge ? `<span class="funding-bridge-chip">${t("cross_chain_badge")}</span>` : ''}
                  </div>
                  <button type="button" class="funding-tx-hash" data-action="track-tx" data-tx="${genesis.txHash}" title="${t("track_source_hint")}">
                    ${truncateAddress(genesis.txHash, 12)}
                  </button>
                  <div class="funding-tx-actions">
                    <button type="button" class="icon-action-btn primary" data-action="track-tx" data-tx="${genesis.txHash}" title="${t("track_source_hint")}">
                      <i class="fa-solid fa-route"></i> ${t("track_source_btn")}
                    </button>
                    ${genesis.txUrl ? `
                      <a href="${genesis.txUrl}" target="_blank" rel="noopener noreferrer" class="icon-action-btn">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i> Explorer
                      </a>
                    ` : ''}
                    <button type="button" class="icon-action-btn" data-copy="${genesis.txHash}" data-copy-label="Tx Hash">
                      <i class="fa-regular fa-copy"></i>
                    </button>
                  </div>
                  ${genesis.bridgeOrigin ? `
                    <div class="funding-origin">
                      <span><i class="fa-solid fa-location-dot"></i> ${t("origin_chain_label")}: <strong>${genesis.bridgeOrigin.chain || '-'}</strong> &bull; ${genesis.bridgeOrigin.protocol}</span>
                      ${genesis.bridgeOrigin.sender ? `<span>${t("real_sender_label")}: <code title="${genesis.bridgeOrigin.sender}">${truncateAddress(genesis.bridgeOrigin.sender, 8)}</code></span>` : ''}
                    </div>
                  ` : ''}
                  ${genesis.isBridge ? `<p class="funding-tx-note">${t("bridge_funding_note")}</p>` : ''}
                </div>
              ` : ''}
            </div>
          ` : `
            <div class="funder-box" style="border-color: rgba(255,255,255,0.08); color: var(--text-dim); font-size: 0.84rem;">
              <i class="fa-solid fa-circle-info"></i> ${dict.no_funder_detected || 'Tidak ditemukan transfer native gas langsung.'}
            </div>
          `}

          <!-- Top Inflow Providers (Spam-Filtered Capital Senders) -->
          <div style="margin-bottom: 12px; font-size: 0.76rem; font-weight: 800; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px;">
            ${dict.top_senders_title || 'TOP SENDERS (ALL-TIME)'} <span style="color: var(--accent-lime); font-size: 0.7rem;">[Anti-Spam Filtered]</span>
          </div>
          ${inflows.length > 0 ? `
            <ul class="flow-items-list">
              ${inflows.map(item => {
                const pct = Math.min(100, Math.max(12, (item.totalAmount / maxInflow) * 100));
                return `
                  <li class="flow-item-row">
                    <div class="flow-item-main">
                      <div class="flow-entity-title" title="${item.sender}">
                        <i class="fa-solid fa-circle-arrow-down text-lime" style="font-size: 0.75rem;"></i>
                        <span>${item.label || truncateAddress(item.sender, 8)}</span>
                      </div>
                      <div class="flow-amt-val inflow">
                        +${item.totalAmount} ${item.tokenSymbol}
                      </div>
                    </div>
                    <div class="flow-addr-sub" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;">
                      <span style="font-family: var(--font-mono); font-size: 0.74rem;">${truncateAddress(item.sender, 10)} &bull; ${item.txCount} txs</span>
                      <button class="icon-action-btn-mini" data-copy="${item.sender}" data-copy-label="Sender" title="Copy full wallet address">
                        <i class="fa-regular fa-copy"></i> Copy
                      </button>
                    </div>
                    <div class="progress-bar-wrap">
                      <div class="progress-fill inflow" style="width: ${pct}%;"></div>
                    </div>
                  </li>
                `;
              }).join('')}
            </ul>
          ` : `
            <p style="color: var(--text-dim); font-size: 0.85rem; padding: 12px 0;">Belum ada data inflow lain.</p>
          `}
        </div>

        <!-- COLUMN 2: ALL-TIME EXIT / CASH OUT (OUTFLOW TRACKING) -->
        <div class="genealogy-col-card outflow">
          <div class="col-header">
            <div class="col-header-title outflow">
              <span class="pulsing-indicator red"></span>
              <span>${dict.exit_outflow_title || 'Exit & Outflow Targets (Pencairan Dana)'}</span>
            </div>
            <span class="proto-tag" style="border-color: rgba(248, 113, 113, 0.3);">
              <i class="fa-solid fa-arrow-up-right" style="color: var(--accent-red);"></i> OUTFLOW
            </span>
          </div>

          <!-- Top Exit Destinations -->
          <div style="margin-bottom: 12px; font-size: 0.76rem; font-weight: 800; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px;">
            ${dict.top_exits_title || 'TOP EXIT DESTINATIONS'}
          </div>

          ${outflows.length > 0 ? `
            <ul class="flow-items-list" style="margin-bottom: 24px;">
              ${outflows.map(item => {
                const pct = item.percentage || Math.min(100, Math.max(10, (item.totalAmount / maxOutflow) * 100));
                return `
                  <li class="flow-item-row">
                    <div class="flow-item-main">
                      <div class="flow-entity-title" title="${item.recipient}">
                        <i class="fa-solid fa-circle-arrow-up" style="color: var(--accent-red); font-size: 0.75rem;"></i>
                        <span>${item.label || truncateAddress(item.recipient, 8)}</span>
                        ${item.isContract ? '<span class="contract-chip">Contract</span>' : ''}
                      </div>
                      <div class="flow-amt-val outflow">
                        -${item.totalAmount} ${item.tokenSymbol}
                        ${item.percentage ? `<span style="font-size:0.7rem; margin-left:4px; opacity:0.8;">(${item.percentage}%)</span>` : ''}
                      </div>
                    </div>
                    <div class="flow-addr-sub" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;">
                      <span style="font-family: var(--font-mono); font-size: 0.74rem;">${truncateAddress(item.recipient, 10)} &bull; ${item.txCount} txs</span>
                      <button class="icon-action-btn-mini outflow-copy" data-copy="${item.recipient}" data-copy-label="Exit Target" title="Copy full wallet address">
                        <i class="fa-regular fa-copy"></i> Copy
                      </button>
                    </div>
                    <div class="progress-bar-wrap">
                      <div class="progress-fill outflow" style="width: ${pct}%;"></div>
                    </div>
                  </li>
                `;
              }).join('')}
            </ul>
          ` : `
            <div style="padding: 24px 0; color: var(--text-dim); font-size: 0.85rem;">
              <i class="fa-solid fa-circle-info"></i> ${dict.no_exits_detected || 'Belum terdeteksi transaksi keluar (outflow).'}
            </div>
          `}

          <!-- Exit Pattern Detected Banner -->
          <div class="exit-pattern-box">
            <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">
              ${dict.exit_pattern_label || 'Exit Pattern Detected:'}
            </span>
            <span class="pattern-badge">
              <i class="fa-solid fa-shield-virus"></i> ${exitPattern}
            </span>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Render Batch Sybil Dashboard with False Positive Mitigation
function renderBatchSybilDashboard(data, container) {
  lastBatchData = data;
  const dict = translations[currentLang] || translations.id;
  const linkedWallets = data.linkedWallets || [];
  const sharedFunders = data.sharedFunders || [];
  const sharedExits = data.sharedExits || [];
  const sharedInfra = data.sharedInfrastructure || { funders: [], exits: [] };
  const sybilDetected = data.sybilDetected;
  const confidenceScore = data.confidenceScore || 0;
  const riskLevel = data.riskLevel || 'NONE';
  const riskDesc = typeof data.riskDescription === 'object'
    ? (data.riskDescription[currentLang] || data.riskDescription.en)
    : (data.riskDescription || '');
  const chainKey = data.chainKey || 'base';

  let confClass = "high";
  let confText = dict.confidence_high || "HIGH";
  if (confidenceScore === 0) {
    confClass = "none";
    confText = dict.confidence_none || "NO RELATION (Independent)";
  } else if (confidenceScore <= 25) {
    confClass = "low";
    confText = dict.confidence_low || "LOW / CEX INFRASTRUCTURE";
  } else if (confidenceScore <= 75) {
    confClass = "medium";
    confText = dict.confidence_med || "MEDIUM";
  }

  // Header status badge & optional Possible Sybil Pattern chip
  let badgeIcon = 'fa-circle-check';
  let badgeText = dict.no_rel_badge || 'NO DIRECT CROSS-WALLET RELATIONSHIP DETECTED';
  let badgeStyle = 'background: var(--accent-lime-dim); color: var(--accent-lime); border-color: var(--border-lime);';
  let sybilPatternBadge = '';

  if (sybilDetected) {
    badgeIcon = 'fa-diagram-project';
    badgeText = dict.rel_detected_badge || 'RELATIONSHIP CLUSTER DETECTED (PRIVATE EOA OVERLAP)';
    badgeStyle = 'background: rgba(239, 68, 68, 0.15); color: var(--accent-red); border-color: rgba(239, 68, 68, 0.4);';
    if (confidenceScore >= 85) {
      sybilPatternBadge = `
        <span class="sybil-pattern-pill" title="${dict.possible_sybil_desc || 'Coordinated multi-wallet cluster'}">
          <i class="fa-solid fa-users-rays"></i> ${dict.possible_sybil_pattern || 'Possible Sybil Pattern'}
        </span>
      `;
    }
  } else if (sharedInfra.funders.length > 0 || sharedInfra.exits.length > 0) {
    badgeIcon = 'fa-building-columns';
    badgeText = dict.cex_only_badge || 'PUBLIC CEX OVERLAP ONLY (EXCLUDED FROM PRIVATE CLUSTER)';
    badgeStyle = 'background: rgba(251, 191, 36, 0.15); color: var(--accent-amber); border-color: rgba(251, 191, 36, 0.4);';
  }

  container.innerHTML = `
    <div class="genealogy-dashboard">
      <!-- GMGN Export Toolbar with Disclaimer & Confidence -->
      ${renderGmgnToolbar(linkedWallets, 'WalletCluster', chainKey, confidenceScore, riskLevel)}

      <!-- Relationship Detection Status Card -->
      <div class="sybil-cluster-card" style="border-color: ${sybilDetected ? 'rgba(239, 68, 68, 0.4)' : (sharedInfra.funders.length > 0 || sharedInfra.exits.length > 0 ? 'rgba(251, 191, 36, 0.4)' : 'rgba(158, 255, 0, 0.3)')};">
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">
          <div class="sybil-header-badge" style="${badgeStyle}; margin-bottom: 0;">
            <i class="fa-solid ${badgeIcon}"></i>
            <span>${badgeText}</span>
          </div>
          ${sybilPatternBadge}
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-top: 12px; margin-bottom: 8px;">
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: #fff;">
              ${dict.batch_overlap_title || 'Batch Relationship Overlap Check'} (${data.totalChecked} ${dict.wallets_checked_suffix || 'Wallets Checked'})
            </h3>
            <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
              ${riskDesc}
            </p>
          </div>

          <!-- Confidence Score Box -->
          <div class="confidence-box ${confClass}">
            <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 800; color: var(--text-dim);">${dict.cluster_confidence_label || 'Cluster Confidence:'}</div>
            <div style="font-size: 1.5rem; font-weight: 900; font-family: var(--font-mono);">${confidenceScore}%</div>
            <div style="font-size: 0.75rem; font-weight: 700;">${confText}</div>
          </div>
        </div>

        <!-- 1. PRIVATE RELATIONSHIP CLUSTERS -->
        ${sharedFunders.length > 0 ? `
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border-subtle);">
            <div style="font-size: 0.82rem; font-weight: 800; color: var(--accent-red); margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
              <i class="fa-solid fa-fingerprint"></i>
              <span>${dict.shared_private_funder_title}</span>
              <span class="risk-pill danger" style="font-size: 0.7rem; padding: 2px 8px;">High Confidence</span>
            </div>
            ${sharedFunders.map(sf => `
              <div style="background: rgba(0,0,0,0.4); padding: 12px; border-radius: 8px; margin-bottom: 8px; border: 1px solid rgba(239,68,68,0.3);">
                <div style="font-family: var(--font-mono); font-size: 0.86rem; color: var(--accent-red); margin-bottom: 6px;">
                  ${dict.funder_eoa_label} ${sf.funder}
                </div>
                <div style="font-size: 0.78rem; color: var(--text-dim); margin-bottom: 4px;">${dict.co_funded_wallets}</div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                  ${sf.fundedWallets.map(w => `<span class="sybil-wallet-chip" style="border-color: rgba(239,68,68,0.4); color: #fff;">${truncateAddress(w, 8)}</span>`).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}

        ${sharedExits.length > 0 ? `
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border-subtle);">
            <div style="font-size: 0.82rem; font-weight: 800; color: var(--accent-red); margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
              <i class="fa-solid fa-arrows-to-circle"></i>
              <span>${dict.shared_private_exit_title}</span>
              <span class="risk-pill danger" style="font-size: 0.7rem; padding: 2px 8px;">High Confidence</span>
            </div>
            ${sharedExits.map(se => `
              <div style="background: rgba(0,0,0,0.4); padding: 12px; border-radius: 8px; margin-bottom: 8px; border: 1px solid rgba(239,68,68,0.3);">
                <div style="font-family: var(--font-mono); font-size: 0.86rem; color: var(--accent-red); margin-bottom: 6px;">
                  ${dict.consolidation_hub_label} ${se.exitTarget}
                </div>
                <div style="font-size: 0.78rem; color: var(--text-dim); margin-bottom: 4px;">${dict.sending_wallets_label}</div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                  ${se.sendingWallets.map(w => `<span class="sybil-wallet-chip" style="border-color: rgba(239,68,68,0.4); color: #fff;">${truncateAddress(w, 8)}</span>`).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}

        <!-- 2. PUBLIC INFRASTRUCTURE OVERLAP (ISOLATED TO PREVENT FALSE POSITIVES) -->
        ${(sharedInfra.funders.length > 0 || sharedInfra.exits.length > 0) ? `
          <div class="infra-overlap-card">
            <div class="infra-overlap-header">
              <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fa-solid fa-building-columns text-amber"></i>
                <span style="font-size: 0.8rem; font-weight: 800; color: var(--accent-amber); text-transform: uppercase;">
                  ${dict.shared_infra_title}
                </span>
              </div>
              <span class="infra-excluded-chip">${dict.false_positive_guard}</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px;">
              ${dict.shared_infra_desc}
            </p>

            ${sharedInfra.funders.map(inf => `
              <div style="background: rgba(0,0,0,0.3); padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                  <span style="font-size: 0.75rem; color: var(--accent-amber); font-weight: 700;">[Exchange Hot Wallet / Faucet]</span>
                  <span style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-pure); margin-left: 6px;">${inf.label}</span>
                </div>
                <div style="font-size: 0.78rem; color: var(--text-dim);">
                  ${inf.fundedWallets.length} ${dict.overlapping_wallets_suffix} (${truncateAddress(inf.funder, 6)})
                </div>
              </div>
            `).join('')}

            ${sharedInfra.exits.map(ine => `
              <div style="background: rgba(0,0,0,0.3); padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; border: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                  <span style="font-size: 0.75rem; color: var(--accent-amber); font-weight: 700;">[Public CEX Deposit / Router]</span>
                  <span style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-pure); margin-left: 6px;">${ine.label}</span>
                </div>
                <div style="font-size: 0.78rem; color: var(--text-dim);">
                  ${ine.sendingWallets.length} ${dict.overlapping_wallets_suffix} (${truncateAddress(ine.exitTarget, 6)})
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}

        ${(!sybilDetected && sharedInfra.funders.length === 0 && sharedInfra.exits.length === 0) ? `
          <div style="margin-top: 14px; padding: 14px; background: rgba(158,255,0,0.04); border-radius: 8px; border: 1px solid rgba(158,255,0,0.2); color: var(--text-pure); font-size: 0.86rem;">
            <i class="fa-solid fa-circle-check text-lime"></i> ${dict.clean_independence}
          </div>
        ` : ''}
      </div>

      <!-- Linked Wallets Table for GMGN with Chain Context -->
      <div class="card" style="padding: 24px;">
        <h4 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
          <i class="fa-solid fa-list-check text-lime"></i>
          <span>${dict.linked_table_title}</span>
        </h4>
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.84rem;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border-subtle); color: var(--text-dim); text-align: left;">
                <th style="padding: 10px 8px;">${dict.col_wallet_addr}</th>
                <th style="padding: 10px 8px;">${dict.col_role}</th>
                <th style="padding: 10px 8px;">${dict.col_chain}</th>
                <th style="padding: 10px 8px;">${dict.col_confidence}</th>
                <th style="padding: 10px 8px; text-align: right;">${dict.col_action}</th>
              </tr>
            </thead>
            <tbody>
              ${linkedWallets.map(w => `
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                  <td style="padding: 12px 8px; font-family: var(--font-mono); color: var(--text-pure);">
                    ${truncateAddress(w.address, 10)}
                  </td>
                  <td style="padding: 12px 8px;">
                    <span class="proto-tag" style="font-size: 0.74rem;">${w.role}</span>
                  </td>
                  <td style="padding: 12px 8px; text-transform: uppercase; font-weight: 700; color: var(--accent-lime); font-size: 0.76rem;">
                    ${w.chain || chainKey}
                  </td>
                  <td style="padding: 12px 8px; font-weight: 700; color: ${w.confidence >= 80 ? 'var(--accent-lime)' : 'var(--text-dim)'};">
                    ${w.confidence}%
                  </td>
                  <td style="padding: 12px 8px; text-align: right;">
                    <button class="icon-action-btn" data-copy="${w.address}" data-copy-label="${dict.col_wallet_addr}">
                      <i class="fa-regular fa-copy"></i>
                    </button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

// ==================== TAB 4: EXCHANGE DEPOSIT INFLOW TRACER FUNCTIONS ====================

function switchDepositMode(mode) {
  currentDepositMode = mode === "manual" ? "manual" : "address";
  const isManual = currentDepositMode === "manual";
  document.getElementById("depositModeAPill")?.classList.toggle("active", !isManual);
  document.getElementById("depositModeBPill")?.classList.toggle("active", isManual);
  document.getElementById("depositAddressInputWrap").style.display = isManual ? "none" : "block";
  document.getElementById("depositManualInputWrap").style.display = isManual ? "block" : "none";
}

function updateThresholdDisplay(val) {
  const disp = document.getElementById("minThresholdDisplay");
  if (disp) disp.textContent = `$${val} USD`;
}

function clearDepositInput() {
  const inp = document.getElementById("depositAddressInput");
  inp.value = "";
  inp.focus();
}

const SAMPLE_DEPOSIT_CSV = `from,to,amount,token_symbol,token_decimal,timestamp,tx_hash
0x45a90d8a5948f98c8c22428ad5e051c092a48be1,0xDepositVault,12500.0,USDC,6,1710500000,0x9a8f...
0x82f9c4b2a8d5e051c092a48be145a90d8a5948f9,0xDepositVault,4200.0,USDT,6,1710400000,0x8b7c...
2S1zLXppAyd9st2Y9BSn4ZMsTUHU3s7cB44yBXDdEJ1h,SolanaDepositVault,52.22,SOL,9,1710300000,5XGx...
0x3fC77FAD8c1482E2b622C9fae9d6d376A36A7aB2,0xDepositVault,1.85,ETH,18,1710200000,0x7c6d...
0xDustAttackerBot,0xDepositVault,1.5,USDC,6,1710100000,0xdust1...
0xSpamPromoDrop,0xDepositVault,100000,fli.so/AIRDROP,18,1710000000,0xspam1...
0xRepeatedMicroBot,0xDepositVault,0.5,USDC,6,1709900000,0xrep1...
0xRepeatedMicroBot,0xDepositVault,0.5,USDC,6,1709800000,0xrep2...
0xRepeatedMicroBot,0xDepositVault,0.5,USDC,6,1709700000,0xrep3...
0xRepeatedMicroBot,0xDepositVault,0.5,USDC,6,1709600000,0xrep4...`;

const DEPOSIT_SAMPLES = {
  solana: { address: "2S1zLXppAyd9st2Y9BSn4ZMsTUHU3s7cB44yBXDdEJ1h", chain: "solana" },
  evm: { address: "0x0532da9a4248daa5a48b4d7c6c1c8fe447b1320a", chain: "base" }
};

function loadDepositSample(type) {
  switchTab("deposit");
  if (type === "csv") {
    switchDepositMode("manual");
    document.getElementById("depositCsvTextarea").value = SAMPLE_DEPOSIT_CSV;
  } else {
    const sample = DEPOSIT_SAMPLES[type] || DEPOSIT_SAMPLES.evm;
    switchDepositMode("address");
    document.getElementById("depositAddressInput").value = sample.address;
    document.getElementById("depositChainSelect").value = sample.chain;
  }
  submitForm("depositTraceForm");
}

async function handleDepositSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById("btnSubmitDeposit");
  const container = document.getElementById("depositResultContainer");

  const mode = currentDepositMode;
  const address = document.getElementById("depositAddressInput").value.trim();
  const rawData = document.getElementById("depositCsvTextarea").value.trim();
  const chain = document.getElementById("depositChainSelect").value;

  if (mode === "address" && !address) {
    showToast(t("enter_deposit_address"));
    document.getElementById("depositAddressInput").focus();
    return;
  }
  if (mode === "manual" && !rawData) {
    showToast(t("paste_csv_data"));
    document.getElementById("depositCsvTextarea").focus();
    return;
  }

  const isSolana = mode === "address" && (SOLANA_ADDR_RE.test(address) || chain === "solana");
  const sub = mode === "manual" ? "CSV" : (isSolana ? t("deposit_scan_sub_solana") : (chain === "auto" ? t("deposit_scan_sub_multi") : esc(chain.toUpperCase())));
  setLoading(btn, true);
  renderLoading(container, t("btn_tracing_deposit"), sub);

  try {
    const data = await apiFetch("deposit", "/api/deposit/trace", postJSON({
      mode,
      address,
      raw_data: rawData,
      chain,
      min_threshold_usd: parseFloat(document.getElementById("minThresholdSlider").value) || 0,
      dust_threshold_usd: 5.0,
      exclude_dust: document.getElementById("excludeDustCheck").checked,
      filter_phishing: document.getElementById("filterPhishingCheck").checked
    }));
    if (!data) return;
    if (!data.success) {
      renderError(container, t("deposit_failed"), data.error);
      return;
    }
    lastDepositData = data;
    renderDepositResults(data, container);
    container.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    renderError(container, t("network_error"), esc(err.message));
  } finally {
    if (!isBusy("deposit")) setLoading(btn, false);
  }
}


function renderDepositResults(data, container) {
  const dict = translations[currentLang] || translations.id;
  const summary = data.summary || {};
  const qualified = data.qualified_senders || [];
  const filtered = data.filtered_senders || [];

  // Calculate top depositor share
  const topDepositor = qualified.length > 0 ? qualified[0] : null;
  let topDominancePct = 0;
  if (topDepositor && summary.qualified_cumulative_deposit_usd > 0) {
    topDominancePct = Math.round((topDepositor.total_deposit_usd / summary.qualified_cumulative_deposit_usd) * 100);
  }

  container.innerHTML = `
    <!-- Top Result Banner -->
    <div class="card" style="margin-bottom: 20px; padding: 22px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
          <div style="font-size: 0.76rem; font-weight: 800; color: var(--accent-lime); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
            <i class="fa-solid fa-vault"></i> ${dict.deposit_section_title}
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0;">
            ${data.mode === 'address' ? truncateAddress(data.target_address, 12) : (currentLang === 'id' ? 'Riwayat Transaksi Manual (CSV)' : 'Manual Transaction History (CSV)')}
          </h3>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 4px;">
            <span class="chain-badge" style="display: inline-flex; padding: 2px 8px; font-size: 0.72rem;">${data.chain}</span>
            <span style="margin-left: 6px;">${data.scan_scope_note || ''}</span>
          </div>
        </div>

        ${data.is_contract_or_vault ? `
          <div style="background: rgba(255, 170, 0, 0.12); border: 1px solid rgba(255, 170, 0, 0.35); padding: 8px 14px; border-radius: 8px; color: #ffbb33; font-size: 0.78rem; font-weight: 700; display: flex; align-items: center; gap: 6px;">
            <i class="fa-solid fa-triangle-exclamation"></i>
            <span>${dict.vault_warning} ${data.contract_label ? `(${data.contract_label})` : ''}</span>
          </div>
        ` : ''}
      </div>
    </div>

    <!-- Summary Metrics Grid -->
    <div class="details-grid" style="margin-bottom: 24px;">
      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_qualified_senders}</div>
        <div class="metric-value text-lime" style="font-size: 1.5rem;">
          ${summary.qualified_count || 0}
        </div>
        <div class="metric-sub">${currentLang === 'id' ? 'Lolos filter & ambang batas' : 'Passed spam & threshold filter'}</div>
      </div>

      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_total_volume}</div>
        <div class="metric-value" style="font-size: 1.4rem; color: #fff;">
          $${(summary.qualified_cumulative_deposit_usd || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </div>
        <div class="metric-sub text-lime">USD Cumulative Inflow</div>
      </div>

      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_filtered_senders}</div>
        <div class="metric-value" style="font-size: 1.5rem; color: #ff7788;">
          ${summary.filtered_count || 0}
        </div>
        <div class="metric-sub">${currentLang === 'id' ? 'Dust & airdrop phishing dibuang' : 'Dust attacks & spam excluded'}</div>
      </div>

      <div class="detail-metric-card">
        <div class="metric-label">${dict.metric_top_dominance}</div>
        <div class="metric-value text-cyan" style="font-size: 1.5rem;">
          ${topDominancePct}%
        </div>
        <div class="metric-sub">${topDepositor ? truncateAddress(topDepositor.sender_address, 6) : '-'}</div>
      </div>
    </div>

    <!-- Action Toolbar (GMGN CSV Export & Copy) -->
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px;">
      <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <button class="btn btn-sample" style="border-color: var(--accent-lime); color: var(--accent-lime);" onclick="exportDepositGMGN()">
          <i class="fa-solid fa-file-arrow-down"></i> ${dict.export_deposit_csv}
        </button>
        <button class="btn btn-sample" onclick="copyQualifiedSenders()">
          <i class="fa-solid fa-copy"></i> ${dict.copy_qualified_addrs}
        </button>
      </div>

      ${filtered.length > 0 ? `
        <button class="btn btn-sample" style="border-color: rgba(255,255,255,0.15); color: var(--text-dim);" onclick="toggleFilteredDrawer()">
          <i class="fa-solid fa-shield-halved text-lime"></i> ${dict.toggle_filtered_drawer} (${filtered.length})
        </button>
      ` : ''}
    </div>

    <!-- Qualified Senders Table -->
    <div class="card" style="padding: 24px; margin-bottom: 24px;">
      <h4 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
        <i class="fa-solid fa-users text-lime"></i>
        <span>${dict.qualified_senders_title}</span>
      </h4>

      <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.84rem;">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-subtle); color: var(--text-dim); text-align: left;">
              <th style="padding: 10px 8px; width: 40px;">#</th>
              <th style="padding: 10px 8px;">${dict.col_sender_address}</th>
              <th style="padding: 10px 8px;">${dict.col_total_deposit}</th>
              <th style="padding: 10px 8px;">${dict.col_tx_count}</th>
              <th style="padding: 10px 8px;">${dict.col_first_deposit}</th>
              <th style="padding: 10px 8px;">${dict.col_last_deposit}</th>
              <th style="padding: 10px 8px; text-align: right;">${dict.col_actions}</th>
            </tr>
          </thead>
          <tbody>
            ${qualified.length === 0 ? `
              <tr>
                <td colspan="7" style="padding: 24px; text-align: center; color: var(--text-dim);">
                  ${currentLang === 'id' ? 'Tidak ada pengirim yang lolos filter ambang batas saat ini.' : 'No senders qualified under the current filter thresholds.'}
                </td>
              </tr>
            ` : qualified.map((s, idx) => `
              <tr class="hover-row" style="border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s ease;">
                <td style="padding: 12px 8px; color: var(--text-dim); font-weight: 700;">${idx + 1}</td>
                <td style="padding: 12px 8px; font-family: var(--font-mono); color: var(--text-pure); font-weight: 600;">
                  <button type="button" class="addr-copy-btn" data-copy="${s.sender_address}" data-copy-label="${dict.col_sender_address}" title="${s.sender_address}"><span>${truncateAddress(s.sender_address, 10)}</span><i class="fa-regular fa-copy"></i></button>
                  <span class="chain-badge" style="font-size: 0.68rem; margin-left: 6px; padding: 2px 6px;">${s.chain}</span>
                </td>
                <td style="padding: 12px 8px;">
                  <strong class="text-lime" style="font-size: 0.95rem;">
                    $${s.total_deposit_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </strong>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;">
                    ${s.tokens.map(t => `
                      <span class="proto-tag" style="font-size: 0.7rem; padding: 1px 6px;">
                        ${Number(t.amount).toLocaleString('en-US', { maximumFractionDigits: 4 })} ${t.symbol}
                      </span>
                    `).join('')}
                  </div>
                </td>
                <td style="padding: 12px 8px; font-weight: 700; color: #fff;">
                  ${s.tx_count} txs
                </td>
                <td style="padding: 12px 8px; color: var(--text-dim); font-size: 0.78rem;">
                  ${s.first_deposit_days_ago} ${currentLang === 'id' ? 'hari lalu' : 'days ago'}
                </td>
                <td style="padding: 12px 8px; color: var(--text-dim); font-size: 0.78rem;">
                  ${s.last_deposit_days_ago} ${currentLang === 'id' ? 'hari lalu' : 'days ago'}
                </td>
                <td style="padding: 12px 8px; text-align: right;">
                  <div style="display: inline-flex; gap: 6px; align-items: center;">
                    <button class="icon-action-btn-mini" data-copy="${s.sender_address}" data-copy-label="${dict.col_sender_address}" title="Copy Address">
                      <i class="fa-regular fa-copy"></i>
                    </button>
                    ${s.explorer_url ? `
                      <a href="${s.explorer_url}" target="_blank" rel="noopener noreferrer" class="icon-action-btn-mini" title="Explorer">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i>
                      </a>
                    ` : ''}
                    <button class="btn btn-sample" style="padding: 3px 8px; font-size: 0.74rem; border-color: var(--accent-lime); color: var(--accent-lime);" data-action="trace-sender" data-addr="${s.sender_address}" data-chain="${s.chain}" title="Lacak hubungan wallet ini di Tab 3">
                      <i class="fa-solid fa-diagram-project"></i> <span>${dict.btn_trace_tab3}</span>
                    </button>
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Filtered Senders Drawer (Collapsible Spam Log) -->
    <div id="filteredSendersDrawer" class="card" style="display: none; padding: 22px; border: 1px solid rgba(255, 100, 100, 0.25); background: rgba(20, 10, 15, 0.6); margin-bottom: 24px;">
      <h4 style="font-size: 0.98rem; font-weight: 800; color: #ff7788; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <i class="fa-solid fa-shield-halved"></i>
        <span>${dict.filtered_senders_title} (${filtered.length})</span>
      </h4>
      <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem;">
          <thead>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06); color: var(--text-dim); text-align: left;">
              <th style="padding: 8px;">Sender Address</th>
              <th style="padding: 8px;">Filter Reason</th>
              <th style="padding: 8px;">Total Inflow</th>
              <th style="padding: 8px;">Tx Count</th>
              <th style="padding: 8px; text-align: right;">Action</th>
            </tr>
          </thead>
          <tbody>
            ${filtered.map(f => `
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.03);">
                <td style="padding: 8px; font-family: var(--font-mono); color: var(--text-dim);">
                  <button type="button" class="addr-copy-btn muted" data-copy="${f.sender_address}" data-copy-label="${dict.col_sender_address}" title="${f.sender_address}"><span>${truncateAddress(f.sender_address, 10)}</span><i class="fa-regular fa-copy"></i></button>
                </td>
                <td style="padding: 8px;">
                  <span style="font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; font-weight: 700; ${
                    f.filter_reason === 'phishing_spam_token' ? 'background: rgba(255,50,50,0.18); color: #ff5566;' :
                    (f.filter_reason === 'single_tx_dust' ? 'background: rgba(255,160,0,0.18); color: #ffaa33;' : 'background: rgba(255,255,255,0.08); color: var(--text-dim);')
                  }">
                    ${f.filter_reason === 'phishing_spam_token' ? dict.reason_phishing : (f.filter_reason === 'single_tx_dust' ? dict.reason_single_dust : `${dict.reason_below_min} ($${summary.min_threshold_usd})`)}
                  </span>
                </td>
                <td style="padding: 8px; color: #fff;">
                  $${f.total_deposit_usd.toFixed(2)}
                </td>
                <td style="padding: 8px; color: var(--text-dim);">
                  ${f.tx_count}
                </td>
                <td style="padding: 8px; text-align: right;">
                  <button class="icon-action-btn-mini" data-copy="${f.sender_address}" data-copy-label="Filtered Sender">
                    <i class="fa-regular fa-copy"></i>
                  </button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function toggleFilteredDrawer() {
  const drawer = document.getElementById("filteredSendersDrawer");
  if (drawer) drawer.style.display = drawer.style.display === "none" ? "block" : "none";
}

function exportDepositGMGN() {
  const senders = lastDepositData?.qualified_senders || [];
  if (!senders.length) {
    showToast(t("no_qualified_export"));
    return;
  }
  const rows = [["Address", "Total_Deposit_USD", "Tx_Count", "Chain", "Tag"]].concat(
    senders.map(s => [s.sender_address, s.total_deposit_usd, s.tx_count, s.chain, "Deposit_Source"])
  );
  downloadCsv(`deposit_sources_gmgn_${Date.now()}.csv`, rows);
  showToast(t("gmgn_csv_downloaded"));
}

function copyQualifiedSenders() {
  const senders = lastDepositData?.qualified_senders || [];
  if (!senders.length) {
    showToast(t("no_qualified"));
    return;
  }
  copyToClipboard(senders.map(s => s.sender_address).join("\n"), `${senders.length} ${t("addresses_word")}`);
}

// ==================== GLOBAL EVENT WIRING ====================

// One delegated listener for every dynamic button (copy / hand-off / export).
document.addEventListener("click", e => {
  const copyEl = e.target.closest("[data-copy]");
  if (copyEl) {
    copyToClipboard(copyEl.dataset.copy, copyEl.dataset.copyLabel);
    return;
  }
  const el = e.target.closest("[data-action]");
  if (!el) return;
  const { action, addr, chain, id } = el.dataset;
  if (action === "analyze-dest" || action === "trace-sender") openInGenealogy(addr, chain);
  else if (action === "track-tx") trackTxInTab1(el.dataset.tx);
  else if (action === "gmgn-csv") downloadGmgnCsv(id, chain);
});

const TX_LIKE_RE = /(\/tx\/|^0x[a-fA-F0-9]{64}$|^[1-9A-HJ-NP-Za-km-z]{80,90}$)/;

document.addEventListener("DOMContentLoaded", () => {
  setLanguage(currentLang);
  switchTab(store.get("omniroute_tab", "tx"));

  const txInput = document.getElementById("txInput");
  const lastTx = store.get("omniroute_last_tx", "");
  if (txInput && lastTx && !txInput.value) txInput.value = lastTx;

  // Paste an explorer link / hash → track immediately (no extra click).
  txInput?.addEventListener("paste", () => {
    setTimeout(() => {
      if (TX_LIKE_RE.test(txInput.value.trim()) && !isBusy("tx")) submitForm("txTrackForm");
    }, 0);
  });

  // Ctrl/Cmd + Enter submits the batch textarea / CSV textarea.
  ["genealogyBatchInput", "depositCsvTextarea"].forEach(id => {
    document.getElementById(id)?.addEventListener("keydown", e => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        e.target.form?.requestSubmit();
      }
    });
  });

  // Keyboard shortcuts: Alt+1..4 switch tabs.
  document.addEventListener("keydown", e => {
    if (!e.altKey || e.ctrlKey || e.metaKey) return;
    const tab = { "1": "tx", "2": "address", "3": "genealogy", "4": "deposit" }[e.key];
    if (tab) {
      e.preventDefault();
      switchTab(tab);
    }
  });

  startHeartbeat();
});

// Graceful Exit App Handler
async function quitOmniRouteApp() {
  if (!confirm(t("confirm_quit"))) return;
  stopHeartbeat();
  showToast(t("stopping_server"));
  try {
    await fetch("/api/shutdown", { method: "POST" });
  } catch { /* server already gone */ }
  setTimeout(() => window.close(), 350);
}

function setOfflineOverlay(show) {
  const overlay = document.getElementById("omnirouteOfflineOverlay");
  if (!overlay) return;
  if (show && overlay.style.display !== "flex") {
    document.getElementById("offlineTitle").textContent = t("offline_title");
    document.getElementById("offlineDesc").textContent = t("offline_desc");
    document.getElementById("btnReconnectText").textContent = t("reconnect");
    document.getElementById("btnCloseAppText").textContent = t("close_window");
  }
  overlay.style.display = show ? "flex" : "none";
}

// Check Server Connection & Reload
async function checkServerAndReload() {
  const btn = document.getElementById("btnReconnectText");
  if (btn) btn.textContent = t("checking");
  try {
    const res = await fetch("/api/ping", { cache: "no-store" });
    if (res.ok) {
      setOfflineOverlay(false);
      window.location.reload();
      return;
    }
  } catch { /* still offline */ }
  if (btn) btn.textContent = t("retry");
  showToast(t("server_not_running"));
}

// Background connection heartbeat: every 15s, paused while the window is hidden,
// re-checked immediately when the window becomes visible again.
const HEARTBEAT_MS = 15000;
let heartbeatTimer = null;
let failedHeartbeats = 0;

async function heartbeat() {
  try {
    const res = await fetch("/api/ping", { cache: "no-store" });
    if (!res.ok) throw new Error(String(res.status));
    failedHeartbeats = 0;
    setOfflineOverlay(false);
  } catch {
    failedHeartbeats++;
    if (failedHeartbeats >= 2) setOfflineOverlay(true);
  }
}

function startHeartbeat() {
  stopHeartbeat();
  heartbeatTimer = setInterval(() => { if (!document.hidden) heartbeat(); }, HEARTBEAT_MS);
}

function stopHeartbeat() {
  clearInterval(heartbeatTimer);
  heartbeatTimer = null;
}

document.addEventListener("visibilitychange", () => {
  if (!document.hidden && heartbeatTimer) heartbeat();
});
