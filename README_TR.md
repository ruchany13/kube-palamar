# ⚓️ Kube-Palamar Nedir?

`kube-palamar`, Kubernetes kümenizdeki Deployment, StatefulSet ve DaemonSet gibi kaynakları kolayca "bağlama" (0 replica'ya scale down) ve "çözme" (orijinal replica sayısına geri scale up) işlemlerini yapmanıza olanak sağlayan bir araçtır.

"Palamar" adı, gemileri iskeleye bağlamak için kullanılan halatın Türkçe karşılığından gelir ve uygulamalarınızı güvenle "park etme" işlemini sembolize eder.

## 🎯 Proje Durumu

**Mevcut Versiyon:** Python scriptler ile çalışan versiyon (aktif)  
**Gelecek Plan:** Go ile CLI aracı + Web UI geliştirme (planlama aşamasında)

Bu repo şu anda Kubernetes namespace'lerinde kaynakları up/down yapan Python scriptlerini içermektedir. İleride Go ile yazılmış bir CLI ve web arayüzü eklenecektir.

---

## 📋 Gereksinimler

- Python 3.x
- Kubernetes cluster erişimi (kubeconfig yapılandırılmış olmalı)
- Gerekli Python paketleri:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🚀 Kullanım

### 1. Kurulum
```bash
# Repository'yi klonlayın
git clone https://github.com/ruchany13/kube-palamar.git
cd kube-palamar

# Kurulum - Gerekli paketleri yükleyin
./cluster.sh setup
```

### 2. Annotation Ekleme (İsteğe Bağlı)
Kaynaklarınızı belirli bir sırayla başlatmak istiyorsanız, `order` annotation'ı ekleyin:

```bash
kubectl annotate deployment <deployment-name> -n <namespace> "order=<order_number>"
kubectl annotate statefulset <statefulset-name> -n <namespace> "order=<order_number>"
kubectl annotate daemonset <daemonset-name> -n <namespace> "order=<order_number>"
```

**Örnek:**
```bash
kubectl annotate deployment nginx-deployment -n production "order=1"
kubectl annotate statefulset mysql-sts -n production "order=2"
```

Alternatif olarak, tüm annotation komutlarını `order.txt` dosyasına yazıp şu komutu çalıştırabilirsiniz:
```bash
./cluster.sh annotate
```

### 3. Namespace'i Kapatma (Scale Down)

Namespace'teki tüm kaynakları 0 replica'ya çeker ve mevcut replica sayılarını annotation olarak saklar:

```bash
./cluster.sh down <namespace>
```

**Örnek:**
```bash
./cluster.sh down production
```

**Ne yapar?**
- Deployment'ları 0 replica'ya scale eder
- StatefulSet'leri 0 replica'ya scale eder
- DaemonSet'leri node selector ile devre dışı bırakır
- Her kaynağın mevcut replica sayısını `replica_annotate` annotation'ı olarak saklar

### 4. Namespace'i Açma (Scale Up)

Daha önce kapatılmış bir namespace'i orijinal replica sayılarına geri döndürür:

```bash
./cluster.sh up <namespace>
```

**Örnek:**
```bash
./cluster.sh up production
```

**Ne yapar?**
- `replica_annotate` annotation'ından orijinal replica sayılarını okur
- `order` annotation'ına göre sıralı şekilde kaynakları başlatır
- Deployment, StatefulSet ve DaemonSet'leri eski haline getirir

---

## 📁 Dosya Yapısı

```
kube-palamar/
├── cluster.sh              # Ana wrapper script - tüm işlemler için bunu kullanın
├── down_cluster.py         # Namespace'i kapatma scripti (Python)
├── up_cluster.py           # Namespace'i açma scripti (Python)
├── requirements.txt        # Python bağımlılıkları
├── order.txt               # Namespace sıralama dosyası (opsiyonel)
└── README.md
```

---

## 🔍 Özellikler

### ✅ Mevcut (Python)
- ✅ Deployment'ları scale down/up
- ✅ StatefulSet'leri scale down/up
- ✅ DaemonSet'leri devre dışı bırakma/aktifleştirme
- ✅ Replica sayılarını annotation olarak saklama
- ✅ Sıralı başlatma desteği (order annotation)
- ✅ Namespace bazlı işlem
- ✅ Kolay kullanım için shell wrapper

### 🔜 Gelecek (Go + Web UI)
- 🔜 Go ile yazılmış performanslı CLI
- 🔜 Web arayüzü ile görsel yönetim
- 🔜 Çoklu namespace desteği
- 🔜 Otomatik rollback
- 🔜 Zamanlama ve otomasyon özellikleri

---

## 🎯 Hızlı Başlangıç

```bash
# 1. Kurulum
./cluster.sh setup

# 2. Namespace'i kapat (mevcut durumu saklar)
./cluster.sh down production

# 3. Namespace'i aç (önceki duruma geri döner)
./cluster.sh up production
```

---

## ⚠️ Dikkat Edilmesi Gerekenler

1. **İlk Kullanımda:** Önce `./cluster.sh down <namespace>` çalıştırılarak mevcut replica sayıları kaydedilmeli, ardından `./cluster.sh up <namespace>` ile geri yüklenmelidir.
2. **Annotation Gerekliliği:** Up scripti için kaynakların `replica_annotate` annotation'ına ihtiyaç vardır (down scripti tarafından otomatik eklenir).
3. **DaemonSet Davranışı:** DaemonSet'ler replica sayısı yerine node selector ile yönetilir.
4. **Kubeconfig:** Script'ler varsayılan kubeconfig'i kullanır (`~/.kube/config`).

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.

---

## 👨‍💻 Geliştirici

**Ruchan Yalçın**  
- GitHub: [@ruchany13](https://github.com/ruchany13)
- Website: [www.ruchan.dev](https://www.ruchan.dev)
- Email: ruchany13@gmail.com

---

⭐️ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!