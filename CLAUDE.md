# Baklava — Türkçe kelime bulmacası

Waffle tarzı 5x5 günlük kelime oyunu. **Tek dosya, derleme adımı yok.**

## ⚠️ Önce bunu oku: `index.html` dosyasını BAŞTAN SONA OKUMA

205 KB / 1160 satır. İçinde 611 bulmacalık dev bir dizi ve base64 gömülü font/görseller (~100 KB) var.
Tamamını okumak bağlamı gereksiz yere doldurur. **Her zaman hedefli git:**

| Bölüm | Satır (yaklaşık) | Not |
|---|---|---|
| `<style>` … `</style>` | 7–221 | CSS, `:root` renk değişkenleri, 4 adet base64 `@font-face` |
| HTML işaretleme | 223–343 | Üst bar, tahta, tüm pencereler (`<body>` burada başlar) |
| `const PUZZLES = [` … `];` | 345–957 | **611 satır veri — asla okuma**, sadece betikle değiştir |
| Oyun mantığı (JS) | 958–1158 | Sabitler, ızgara, renk, sürükleme, kayıt, ekranlar |

(`<script>` 344'te açılır, `</body>` 1158'dedir; yani `<body>` aralığı script'i de kapsar.)

Yöntem: `grep -n "aranan" index.html` ile satırı bul → `Read` ile `offset`/`limit` vererek sadece o bölümü oku.
Küçük değişiklikler için `Edit` yeterli; dosyayı `Write` ile baştan yazma.

## Dosyalar

- `index.html` — oyunun tamamı (HTML+CSS+JS, gömülü font/görsel)
- `kelimehavuzu.txt` — 2788 adet 5 harfli Türkçe kelime (küçük harf, tek tek satır). Bulmacaların **tek** kaynağı.
- `logo.png` (5 MB), `baklava1.jpg`, `baklava2.jpg` — kaynak görseller. Oyunda kullanılanlar zaten `index.html` içine base64 gömülü; bu dosyaları oyun çalışırken okumaz.

## Bozulmaması gereken kurallar

**Bulmaca havuzu (611 adet, `PUZZLES` dizisi)** — her biri `{across:[3], down:[3], start:"21 harf"}`:
- Tüm kelimeler `kelimehavuzu.txt` içinde olmalı; bulmaca içinde 6 kelime de farklı.
- Kesişimler: `a[i][0]=d[0][2i]`, `a[i][2]=d[1][2i]`, `a[i][4]=d[2][2i]`.
- Bir bulmacada daha önceki bulmacalarda geçmiş **en fazla 2 kelime** olabilir (≥4 yeni). Aynı bulmaca iki kez olamaz.
- `start` = başlangıç dizilimi, aktif 21 hücre satır sırasına göre. Harf çokluğu çözümle **birebir aynı** olmalı.
- **Optimal çözüm her bulmacada tam 9 hamle.** (min takas = yanlış hücre − azami döngü; tekrar eden harfler için tüm geçerli eşleşmeler denenerek hesaplanır)
- Başlangıç renk tablosu (yeşil → izin verilen sarı aralığı), her satırdan ~102 bulmaca:
  `9→1-4`, `8→2-5`, `7→3-6`, `6→4-7`, `5→5-8`, `4→6-9`

**Sabitler:** `MAX_SWAPS=15`, boşluklar `(1,1)(1,3)(3,1)(3,3)`, `DAY1 = 1 Ağustos 2026` (arşiv başlangıcı), gün → bulmaca: `id % PUZZLES.length`.

**localStorage anahtarlarını DEĞİŞTİRME** (isimler eski, kasıtlı — değiştirmek oyuncuların verisini siler):
`petek-progress-v1` (günlük ilerleme), `waffle-stats-v1` (istatistik), `waffle-theme-v1`, `waffle-help-hidden-v1`, `petek-cb-v1`.
Arşiv günleri istatistiğe **işlenmez** (`recordStats` sadece bugünü kaydeder).

**Türkçe / metin:**
- Uzun çizgi (—) ve emoji **kullanma**; ikonlar satır içi SVG.
- Büyük harfe çevirmeyi CSS `text-transform` ile yapma → `trUpper()` kullan (yayınlanan sürümde `lang="tr"` korunmuyor, `i` → `I` olur).
- `font-variant-ligatures:none` kalmalı: `fi` ligatürü `i`'nin noktasını siliyor ("harfin" → "harfın").
- Yeşil/sarı/bal rengi iki temada da **aynı**; sadece nötr tonlar temaya göre değişir.

## Değişiklik akışı

1. `index.html` üzerinde `Edit` ile düzenle.
2. Playwright ile doğrula (aşağıdaki komut).
3. Artifact dosyasını üret: `<style>…</style>` + `<body>` içeriğini birleştir (`<html>/<head>/<body>` etiketleri **olmadan**), `Artifact` ile aynı URL'e yayınla.
4. `claude/selam-kanka-f32u76` dalına commit + `git push -u origin claude/selam-kanka-f32u76`.

## Test

Playwright kurulu değil, global yoldan çağır (npm ile kurma):

```js
import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
const {chromium} = pkg;
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
```

- Sayfa açılınca "Nasıl Oynanır" pop-up'ı gelir; test öncesi kapat:
  `page.evaluate(()=>document.getElementById('helpOverlay').classList.remove('show'))`
- Tüm oyun fonksiyonları global: `PUZZLES`, `buildSolution`, `startGrid`, `computeColors`, `activePositions`, `loadDay`, `todayId`, `cur`, `solution`, `swapsLeft`, `phase`. Doğrulamayı `page.evaluate` içinde bunlarla yap — böylece test, oyunun gerçek mantığını kullanır.
- Bulmaca/renk/zorluk değiştiyse **611'inin tamamını** doğrula (kesişim, harf çokluğu, renk tablosu, çözülebilirlik).

## Bulmaca üretimi

Üretim betikleri **depoda değil** (geçici klasörde kalır). Yeniden gerekirse Python ile kur:
oyunun `colorWord`/`computeColors` mantığını birebir taşı, minimum takası tam hesapla,
sonra hedef (yeşil, sarı, 9 hamle) tutana kadar döngü tabanlı karıştırma dene.
`wordfreq` (pypi) kurulu — kelimeleri yaygınlığa göre sıralamak için kullanılabilir.
Ağ kısıtlı: sadece paket kayıt sunucuları açık, TDK/genel internet kapalı.
