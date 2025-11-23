# RSA Kriptografi Projesi - Detaylı Açıklama

## 📋 Projenin Ana Fikri

Bu proje, **RSA şifreleme algoritmasının** performansını incelemek ve **Quadratic Sieve (İkinci Dereceden Elek)** algoritması kullanarak RSA anahtarlarını kırmayı amaçlamaktadır.

### RSA Nedir?

RSA, modern kriptografide en yaygın kullanılan asimetrik şifreleme algoritmasıdır. İki anahtar kullanır:
- **Public Key (Genel Anahtar)**: Herkesle paylaşılır, şifreleme için kullanılır
- **Private Key (Özel Anahtar)**: Gizli tutulur, şifre çözme için kullanılır

RSA'nın güvenliği, büyük sayıların çarpanlarına ayrılmasının (faktörizasyon) çok zor olmasına dayanır.

---

## 🎯 Projenin Amacı

1. **RSA şifreleme/şifre çözme performansını ölçmek**
2. **Quadratic Sieve algoritması ile RSA modüllerini çarpanlarına ayırmak**
3. **Farklı anahtar boyutlarında performans analizi yapmak**
4. **2048-bit RSA'nın güvenliğini tahmin etmek**

---

## 🔑 Verilen RSA Anahtarları

Projede üç farklı boyutta RSA anahtarı verilmiştir:

| Anahtar | p (asal) | q (asal) | N = p×q | e (genel üs) |
|---------|----------|----------|---------|--------------|
| key1 | 25,117 | 25,601 | 643,020,317 | 65,537 |
| key2 | 131,071 | 131,129 | 17,187,209,159 | 65,537 |
| key3 | 262,139 | 262,151 | 68,720,000,989 | 65,537 |

**N**: Modül (public key'in bir parçası)  
**e**: Genel üs (genellikle 65,537)  
**d**: Özel üs (private key - hesaplanması gereken)

---

## 💻 Yapılan İşlemler

### 1. Özel Anahtar (Private Key) Hesaplama

**Formül**: `d = e^(-1) mod φ(N)`

Burada:
- `φ(N) = (p-1) × (q-1)` (Euler totient fonksiyonu)
- `e^(-1) mod φ(N)` = e'nin modüler tersi

**Nasıl Hesaplanır?**
- **Extended Euclidean Algorithm (Genişletilmiş Öklid Algoritması)** kullanılır
- Bu algoritma, iki sayının en büyük ortak bölenini (EBOB) bulurken, modüler tersi de hesaplar

**Sonuçlar:**
- key1: d = 489,705,473
- key2: d = 15,834,271,793
- key3: d = 24,051,869,273

---

### 2. RSA Şifreleme ve Şifre Çözme

#### Şifreleme (Encryption):
```
Ciphertext = Message^e mod N
```

#### Şifre Çözme (Decryption):
```
Message = Ciphertext^d mod N
```

**Hızlı Üs Alma (Fast Exponentiation):**
- Normal üs alma çok yavaş olurdu (örn: 12345^65537)
- **Binary Exponentiation** kullanılır:
  - Üssü ikili (binary) formata çevir
  - Her bit için kare al, gerekirse çarp
  - Örnek: 2^13 = 2^8 × 2^4 × 2^1

**Performans Sonuçları:**
- Şifreleme: 2.9 - 8.4 mikrosaniye
- Şifre Çözme: 5.5 - 21.3 mikrosaniye
- Şifre çözme daha yavaş çünkü d, e'den çok daha büyük

---

### 3. Quadratic Sieve Faktörizasyon Algoritması

Bu, RSA'nın güvenliğini test etmek için kullanılan gerçek bir faktörizasyon algoritmasıdır.

#### Algoritmanın Adımları:

**Adım 1: Factor Base (Çarpan Tabanı) Oluşturma**
- Küçük asal sayılardan oluşan bir liste
- Sadece N'nin "quadratic residue" (ikinci dereceden kalan) olduğu asallar seçilir
- Legendre sembolü kullanılır: (N/p) = 1 olmalı

**Adım 2: Eleme (Sieving)**
- x değerleri için q(x) = x² - N hesaplanır
- q(x) değerlerinin factor base'deki asallarla tamamen çarpanlarına ayrılıp ayrılmadığı kontrol edilir
- Tamamen ayrılanlar "smooth numbers" (düzgün sayılar) olarak adlandırılır

**Örnek:**
- N = 643,020,317
- x = 25,370 için: q(x) = 25,370² - 643,020,317 = 1,283
- 1,283 = 1,283 (asal) → smooth değil
- x = 25,371 için: q(x) = 25,371² - 643,020,317 = 4,084
- 4,084 = 2² × 1,021 → smooth olabilir (eğer 1,021 factor base'deyse)

**Adım 3: Doğrusal Cebir (Linear Algebra)**
- Her smooth number için üslerin paritesi (çift/tek) bir matris satırı oluşturur
- GF(2) üzerinde Gaussian elimination (Gauss eliminasyonu) yapılır
- Doğrusal bağımlılıklar (linear dependencies) bulunur

**Adım 4: Çarpan Bulma (Factor Recovery)**
- Bağımlılık için: X = ∏x_i ve Y = ∏√(q(x_i)) mod N hesaplanır
- Eğer X² ≡ Y² (mod N) ve X ≠ ±Y (mod N) ise:
  - gcd(X - Y, N) veya gcd(X + Y, N) N'nin bir çarpanını verir

**Sonuçlar:**
- key1: 0.012 saniyede çarpanlarına ayrıldı
- key2: 0.008 saniyede çarpanlarına ayrıldı
- key3: 0.031 saniyede çarpanlarına ayrıldı

---

### 4. Performans Analizi ve 2048-bit Tahmini

**Gözlemlenen Veriler:**
- 30-bit N: 0.012 saniye
- 35-bit N: 0.008 saniye
- 37-bit N: 0.031 saniye

**Eğri Uydurma (Curve Fitting):**
- Faktörizasyon süresi bit sayısıyla üstel olarak artar
- log(zaman) = 0.096 × bit_sayısı - 7.524

**2048-bit RSA Tahmini:**
- Yaklaşık 2.78 × 10^82 saniye
- Yaklaşık 8.82 × 10^74 yıl

Bu, evrenin yaşından (13.8 milyar yıl) çok daha uzun bir süredir!

---

## 📊 Proje Sonuçları

### Özel Anahtarlar:
| Anahtar | Özel Anahtar (d) |
|---------|------------------|
| key1 | 489,705,473 |
| key2 | 15,834,271,793 |
| key3 | 24,051,869,273 |

### Şifreleme/Şifre Çözme Performansı:
| Anahtar | Şifreleme (μs) | Şifre Çözme (μs) |
|---------|----------------|------------------|
| key1 | 2.95 | 5.46 |
| key2 | 8.44 | 19.75 |
| key3 | 7.61 | 16.22 |

### Faktörizasyon Sonuçları:
| Anahtar | Bulunan p | Bulunan q | Süre (s) |
|---------|-----------|-----------|----------|
| key1 | 25,117 | 25,601 | 0.012 |
| key2 | 131,071 | 131,129 | 0.008 |
| key3 | 262,139 | 262,151 | 0.031 |

**Doğrulama:** Tüm çarpanlar doğru bulundu ve özel anahtarlar eşleşti! ✓

---

## 🔍 Kod Yapısı

### Ana Fonksiyonlar:

1. **`extended_gcd(a, b)`**: Genişletilmiş Öklid algoritması
2. **`mod_inverse(a, m)`**: Modüler ters hesaplama
3. **`calculate_private_key(p, q, e)`**: RSA özel anahtarı hesaplama
4. **`fast_power(base, exp, mod)`**: Hızlı modüler üs alma
5. **`rsa_encrypt(message, e, N)`**: RSA şifreleme
6. **`rsa_decrypt(ciphertext, d, N)`**: RSA şifre çözme
7. **`quadratic_sieve(n)`**: Quadratic Sieve faktörizasyon
8. **`factor_base(n, bound)`**: Çarpan tabanı oluşturma
9. **`gaussian_elimination_gf2(matrix)`**: GF(2) üzerinde Gauss eliminasyonu

---

## 🎓 Öğrenilenler ve Zorluklar

### Karşılaşılan Zorluklar:

1. **Smoothness Bound Seçimi**: 
   - Çok küçük → yeterli smooth relation bulunamaz
   - Çok büyük → hesaplama süresi artar
   - Optimal değer deneme-yanılma ile bulundu

2. **Doğrusal Cebir (Linear Algebra)**:
   - GF(2) üzerinde Gaussian elimination doğru implementasyonu zor
   - Bağımlılıkları doğru bulmak kritik

3. **İşaret (Sign) Yönetimi**:
   - Negatif smooth number'lar (x² < N durumunda) özel işlem gerektirir
   - Factor base'e -1 eklenmesi gerekir

### İlginç Gözlemler:

1. **Üstel Büyüme**: Bit sayısındaki küçük artışlar bile faktörizasyon süresini dramatik şekilde artırır
2. **Şifre Çözme Daha Yavaş**: Özel üs (d) genel üsten (e) çok daha büyük olduğu için
3. **Smooth Relations**: Factor base boyutundan biraz fazla smooth relation yeterli

---

## 🚀 Projenin Önemi

Bu proje şunları gösterir:

1. **RSA'nın Güvenliği**: Küçük anahtarlar (30-37 bit) kolayca kırılabilir, ancak 2048-bit anahtarlar pratik olarak kırılamaz
2. **Algoritma Karmaşıklığı**: Faktörizasyon algoritmalarının üstel karmaşıklığı
3. **Pratik Uygulama**: Gerçek dünyada kullanılan kriptografi tekniklerinin anlaşılması

---

## 📁 Dosya Yapısı

- **`rsa_project.py`**: Ana implementasyon
- **`generate_report.py`**: Rapor oluşturucu
- **`create_plots.py`**: Görselleştirme scripti
- **`README.md`**: Proje dokümantasyonu
- **`REPORT.md`**: Detaylı proje raporu
- **`requirements.txt`**: Python bağımlılıkları

---

## 🎯 Sonuç

Bu proje, RSA kriptografisinin temellerini, performansını ve güvenlik açıklarını anlamak için kapsamlı bir çalışmadır. Quadratic Sieve gibi gerçek faktörizasyon algoritmalarının implementasyonu, modern kriptografinin güvenliğini değerlendirmek için önemli bir araçtır.

**Ana Çıkarım**: 2048-bit RSA anahtarları, mevcut klasik bilgisayarlarla pratik olarak kırılamaz, bu da onları güvenli kılar. Ancak kuantum bilgisayarların gelişimi bu durumu değiştirebilir (Shor algoritması).

