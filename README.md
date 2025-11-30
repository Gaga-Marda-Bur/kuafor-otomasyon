# Kuaför Otomasyon Sistemi

Bu proje, bir kuaför salonu için hem **masaüstü uygulama** hem de **Django web uygulaması** geliştirmeyi amaçlamaktadır.  
Masaüstü kısmı Python ile geliştirilmiştir, web kısmı ise Django framework kullanılarak hazırlanmıştır.

## Özellikler
- Müşteri kaydı ve yönetimi
- Randevu takibi
- Çalışan yönetimi
- Web ve masaüstü arayüz desteği

## Kurulum

### 1. Repo Klonlama
```bash
git clone https://github.com/Gaga-Marda-Bur/kuafor-otomasyon.git
cd kuafor-otomasyon
2. Virtual Environment Oluşturma
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

3. Gereksinimlerin Kurulumu
pip install -r requirements.txt

Masaüstü Uygulama Çalıştırma
cd oop
python main.py

Web (Django) Uygulama Çalıştırma
cd barber_system
python manage.py migrate
python manage.py runserver


Web uygulamasına tarayıcıdan http://127.0.0.1:8000 adresinden ulaşabilirsiniz.

