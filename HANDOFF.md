# Devir notu

> Önce `CLAUDE.md` oku — kalıcı kurallar ve `index.html` içinde nereye bakılacağı orada.
> Bu dosya sadece **bu ana özgü durum**dur; iş bitince güncelle veya sil.

## Durum

- **611 bulmacalık iş `main`'e girdi (PR #5 merged).** `main` = son bulmaca/renk/9-hamle çalışması. HANDOFF'un "29 commit merge bekliyor" notu artık geçersiz.
- Aktif dal: `claude/read-claude-handoff-md-4gslk1` (bu oturum). Eski dal `claude/selam-kanka-f32u76` merge edildi.
- Canlı önizleme (artifact, son sürüm yayında):
  `https://claude.ai/code/artifact/c7d969cf-cbf3-4263-9525-81130010a430`
- Eski artifact `2b0d231d-…` **kullanılmıyor** (herkese açık paylaşımı takılmıştı, yerine yenisi açıldı).

## Yapılanlar (özet)

- Oyun adı **Petek → Baklava**; yıldızlar yerine her yerde baklava görseli (sayaç, dağılım, sonuç ekranı, arşiv, yardım).
- Kelime havuzu kullanıcının `kelimehavuzu.txt` listesinden (2788 kelime).
- **611 bulmaca** (öncesi 249). Kural: bulmaca başına en fazla 2 tanıdık kelime, aynı bulmaca yok.
- **Her bulmacada optimal çözüm tam 9 hamle**; başlangıç dizilimleri (`start`) önceden üretilip gömüldü, çalışma anında rastgele karıştırma yok.
- Başlangıç renk tablosu sabitlendi (yeşil 4–9 ↔ sarı bandı), her satırdan ~102 bulmaca.
- Yeşil karolar kilitli; gölgeler karo rengiyle uyumlu ve karanlık modda görünür; seçili karoda çerçeve yok.
- İstatistik butonu hangi güne bakılırsa bakılsın **günün bulmacasını** açar; arşiv sonucunda istatistik/paylaşma yok; arşiv istatistiğe işlenmez.
- Paylaş butonu düzeltildi (doğru günün verisi + pano erişimi engelliyse elle kopyalama kutusu).
- "Nasıl Oynanır" yeniden yazıldı, sağ üstte kapatma çarpısı.
- Ayarlar: tema açılır menü + renk körü modu.

## Önemli kararlar (nedeni)

- **`start` dizilimleri gömülü.** Rastgele karıştırma zorluğu kontrol edilemez kılıyordu (bir bulmaca 3 hamlede bitiyordu, 94 bulmacada 5 baklava imkânsızdı). Artık zorluk/renk üretim anında garanti ediliyor.
- **localStorage anahtarları eski isimlerinde bırakıldı** (`petek-*`, `waffle-*`). Yeniden adlandırmak oyuncuların ilerlemesini/istatistiğini siler.
- **`fitsSolution()` koruması**: havuz değiştiğinde eski kayıtlı ilerleme yeni çözümle uyuşmuyorsa o gün baştan başlatılır (bozuk tahta oluşmasın diye).
- **Büyük harfe çevirme JS'te** (`trUpper`): yayınlanan sürümde `lang="tr"` korunmadığı için CSS `text-transform` ARŞİV'i ARŞIV yapıyordu.
- **Ligatürler kapalı**: `fi` ligatürü `i`'nin noktasını siliyordu ("harfin" → "harfın").
- **Üretim betikleri depoya konmadı** — geçici klasörde kaldılar, çıktı yolları oraya sabitli olduğu için depoda işe yaramazlardı.

## Kapatılan konu — hassas kelimeler

**47 bulmacada hassas/kaba kelimeler cevap olarak geçiyor** (`ZENCİ GAVUR IRKÇI APTAL SALAK FUHUŞ VULVA ALLAH KAFİR MÜMİN İSHAL` vb., toplam 35 farklı kelime / 47 bulmaca). 249'luk sürümdeki eleme listesi 611'e çıkarken düşmüştü.

**Karar (2026-08-21, kullanıcı): elenmeyecek. Olduğu gibi kalıyor.** Kelimeler kullanıcının kendi havuz dosyasında var; bir şey yapılmadı. Tekrar açılmasın diye üreticiye engel listesi EKLEME.

## Diğer açık başlıklar

- **Artifact'in herkese açık paylaşımı** hiç doğrulanmadı. Eski linkte "This version can't be shared publicly" hatası vardı; yeni link açıldı ama kullanıcı paylaşımın çalıştığını teyit etmedi. Sorarsa: gerçekten herkese açık bir adres gerekiyorsa GitHub Pages en sağlam yol (depo tek `index.html`, Pages'i açmak yeterli).
- **`logo.png` 5 MB** ve depoda duruyor. Oyunda kullanılan hâli zaten `index.html` içine gömülü; istenirse küçültülebilir/çıkarılabilir.
- Havuzdaki 2788 kelimenin **113'ü** hiçbir bulmacada kullanılmıyor (grid kuramadıkları için). Teorik tavan ~680, ulaşılan 611.

## Çalışma alışkanlıkları (kullanıcı beklentisi)

- Konuşma dili Türkçe, samimi ("kanka").
- Her değişiklikten sonra: Playwright ile doğrula → ekran görüntüsüyle bak → commit + push → artifact'i **aynı URL'e** yeniden yayınla.
- Kullanıcı sık sık "geri al" diyor; değişiklikleri küçük ve tek konuya odaklı commit'le ki geri alması kolay olsun.
