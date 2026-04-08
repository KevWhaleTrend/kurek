/**
 * scanner.js — ChainScan Wallet Scanner
 * GERÇEK APİ ENTEGRASYONU (Moralis + LLM)
 * 
 * LÜTFEN AŞAĞIDAKİ KEY'LERİ KENDİ KEYLERİNİZLE DEĞİŞTİRİN:
 */
const CONFIG = {
  // Moralis (veya Alchemy) API Key'inizi buraya yapıştırın:
  MORALIS_API_KEY: "",
  // LLM API Key (Örn: Google Gemini API Key - ücretsiz ve hızlıdır. Claude tercih ediyorsanız mantık aynıdır):
  GEMINI_API_KEY: "",
  
  // Taranacak zincir (eth, base, polygon, bsc vb.)
  DEFAULT_CHAIN: "eth",
};

let isScanning = false;

// ── Helpers ──
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function appendLine(container, text, cls) {
  const existingCursor = container.querySelector('.term-cursor');
  if (existingCursor) existingCursor.remove();

  const line = document.createElement('div');
  line.className = `term-line${cls ? ' ' + cls : ''}`;
  line.textContent = text || '\u00a0';
  container.appendChild(line);

  const cursor = document.createElement('span');
  cursor.className = 'term-cursor';
  container.appendChild(cursor);

  container.scrollTop = container.scrollHeight;
}

function clearTerminal(container) {
  container.innerHTML = '';
}

function validateAddress(addr) {
  const evmRegex = /^0x[a-fA-F0-9]{40}$/;
  const solanaRegex = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
  if (evmRegex.test(addr)) return 'EVM';
  if (solanaRegex.test(addr)) return 'SOL';
  return null;
}

// ── Gerçek API Çağrıları ──

// Moralis'den işlem geçmişini ve bakiyeyi çek
async function fetchWalletFromMoralis(address) {
  const headers = {
    'accept': 'application/json',
    'X-API-Key': CONFIG.MORALIS_API_KEY
  };

  try {
    // 1. Native balance (ETH çekimi)
    const balRes = await fetch(`https://deep-index.moralis.io/api/v2.2/${address}/balance?chain=${CONFIG.DEFAULT_CHAIN}`, { headers });
    const balData = await balRes.json();
    const balanceEth = balData.balance ? (parseInt(balData.balance) / 1e18).toFixed(4) : 0;

    // 2. Token Bakiyeleri (Hangi tokenleri tutuyor?)
    const tokenRes = await fetch(`https://deep-index.moralis.io/api/v2.2/${address}/erc20?chain=${CONFIG.DEFAULT_CHAIN}`, { headers });
    const tokenData = await tokenRes.json();
    
    // 3. Son 20 işlem geçmişi
    const txRes = await fetch(`https://deep-index.moralis.io/api/v2.2/${address}?chain=${CONFIG.DEFAULT_CHAIN}&limit=20`, { headers });
    const txData = await txRes.json();
    
    return {
      balance: balanceEth,
      tokens: tokenData.length ? tokenData.slice(0, 5) : [], // Sadece en çok tutulan 5 token
      txCount: txData.total !== undefined ? txData.total : (txData.result ? txData.result.length : 0),
      rawTransactions: txData.result || [],
      error: false
    };
  } catch (error) {
    console.error("Moralis API Error:", error);
    return { error: true, message: error.message };
  }
}

// Çekilen gerçek veriyi Yapay Zeka'ya (Gemini) gönderip analiz raporu oluştur
async function generateAIReport(walletData) {
  // LLM'e gönderilecek prompt (Verileri verip özet formatı istiyoruz)
  const prompt = `
Bir kripto para cüzdanının onchain verilerini analiz et. Uydurma bilgi kullanma! Sadece aşağıdaki verilere dayanarak kısa, tek düze bir 'ChainScan İstihbarat Raporu' hazırla.

Cüzdan Verileri:
- Bakiye: ${walletData.balance} ETH
- Bulunan İşlem Sayısı (Son çekilen): ${walletData.txCount} işlem var
- Tutan İlk 5 Token (Sembol/Bakiye): ${walletData.tokens.map(t => `${t.symbol}: ${(t.balance / Math.pow(10, t.decimals)).toFixed(2)}`).join(', ') || 'Yok / Bulunamadı'}

Lütfen sonucu SADECE aşağıdaki formatta ver (çizgiler kullan, ekstra giriş/çıkış cümlesi yazma):

│ Profil: [Cüzdanın durumunu özetleyen 2 kelimelik başlık (Örn: Hareketsiz, Yeni Cüzdan, Aktif Trader)]
│ İşlem Skoru: [Aktiviteye göre 1 ile 10 arası bir puan]
│ Zeka Notu: [Bu cüzdanla ilgili 1 cümlelik Türkçe yapay zeka analizi veya dikkate değer durum]
  `;

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${CONFIG.GEMINI_API_KEY}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
    });

    const data = await response.json();
    
    // API'den dönen cevabı ayıkla
    if (data.candidates && data.candidates.length > 0) {
      return data.candidates[0].content.parts[0].text.trim();
    }
    return "│ Analiz Raporu Oluşturulamadı.";
  } catch (err) {
    console.error("AI API Error:", err);
    return "│ AI servis hatası.";
  }
}

// ── Ana Tarayıcı Fonksiyonu ──
async function runWalletScan() {
  if (isScanning) return;

  const input = document.getElementById('wallet-input');
  const btn = document.getElementById('scan-btn');
  const terminal = document.getElementById('terminal-body');

  if (!input || !terminal) return;
  const raw = input.value.trim();

  if (!raw) {
    input.focus();
    input.style.borderColor = '#f87171';
    setTimeout(() => { input.style.borderColor = ''; }, 1500);
    return;
  }

  isScanning = true;
  btn.disabled = true;
  btn.textContent = 'Scanning...';
  input.disabled = true;

  clearTerminal(terminal);

  const type = validateAddress(raw);

  // 1. DOĞRULAMA
  if (!type) {
    appendLine(terminal, `$ chainscan analyze --wallet ${raw}`, '');
    await sleep(400);
    appendLine(terminal, `[ERROR] Geçersiz cüzdan formatı.`, 'alert');
    isScanning = false;
    btn.disabled = false;
    btn.textContent = 'Scan Wallet';
    input.disabled = false;
    return;
  }

  const shortAddr = raw.length > 20 ? `${raw.slice(0,6)}...${raw.slice(-4)}` : raw;
  appendLine(terminal, `$ chainscan analyze --address ${shortAddr}`, '');
  await sleep(300);
  appendLine(terminal, `  Hedef saptanıyor... ✓ ${type} adresi`, 'info');
  await sleep(200);

  // API KEY KONTROLÜ
  if (!CONFIG.MORALIS_API_KEY || !CONFIG.GEMINI_API_KEY) {
    appendLine(terminal, ``, '');
    appendLine(terminal, `[UYARI] API Key Bulunamadı (Moralis veya AI)`, 'warn');
    appendLine(terminal, `  scanner.js dosyasının en üstüne API keylerinizi girmeniz gerekmektedir.`, 'dim');
    appendLine(terminal, `  Simüle edilmiş, uydurma veriler DEVRE DIŞI BIRAKILMIŞTIR. İşlem durduruldu.`, 'alert');
    isScanning = false;
    btn.disabled = false;
    btn.textContent = 'Scan Wallet';
    input.disabled = false;
    return;
  }

  // 2. GERÇEK VERİ ÇEKME İşlemi (MORALIS)
  appendLine(terminal, `  Moralis API üzerinden on-chain veriler çekiliyor...`, 'info');
  
  const realData = await fetchWalletFromMoralis(raw);

  if (realData.error) {
    appendLine(terminal, `[ERROR] Veri çekilirken hata oluştu: ${realData.message}`, 'alert');
    isScanning = false;
    btn.disabled = false;
    btn.textContent = 'Scan Wallet';
    input.disabled = false;
    return;
  }

  await sleep(500);
  appendLine(terminal, `  ✓ İşlem tamamlandı. Bulunan zincir işlemi: ${realData.txCount}`, 'ok');
  appendLine(terminal, `  ✓ Gerçek ETH Bakiyesi: ${realData.balance} ETH`, 'ok');
  
  if (realData.tokens.length > 0) {
    const tokenStr = realData.tokens.map(t => t.symbol).join(', ');
    appendLine(terminal, `  ✓ Tespit edilen cüzdan varlıkları: ${tokenStr}`, 'dim');
  }

  if (realData.txCount === 0) {
    appendLine(terminal, ``, '');
    appendLine(terminal, `  ! Bu cüzdan (şu anki ağda) tamamen boş ve işlem yapmamış.`, 'warn');
  }

  // 3. YAPAY ZEKA İLE ANALİZ (GEMİNİ/CLAUDE)
  appendLine(terminal, ``, '');
  appendLine(terminal, `  Yapay Zeka raporu hazırlanıyor... (Gerçek LLM API Çağrısı)`, 'info');
  
  const aiReport = await generateAIReport(realData);
  
  await sleep(500);
  appendLine(terminal, ``, '');
  appendLine(terminal, `  ┌─ CHAINSCAN GERÇEK ZAMANLI RAPOR ──────────┐`, 'result');
  
  // Gelen sonucu satırlara bölüp bas
  const reportLines = aiReport.split('\n');
  reportLines.forEach(line => {
    if(line.trim().length > 0) {
      appendLine(terminal, `  ${line}`, 'result');
    }
  });

  appendLine(terminal, `  └───────────────────────────────────────────┘`, 'result');

  // Done
  isScanning = false;
  btn.disabled = false;
  btn.textContent = 'Scan Wallet';
  input.disabled = false;
}

document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('wallet-input');
  if (input) {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') runWalletScan();
    });
  }
});

window.runWalletScan = runWalletScan;
