import sys
import requests
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QLineEdit, 
                           QPushButton, QTextEdit, QDateEdit, QTimeEdit,
                           QTabWidget, QTableWidget, QTableWidgetItem,
                           QMessageBox, QGroupBox, QDialog, QDialogButtonBox)
from PyQt6.QtCore import QTime, QDate, Qt
from PyQt6.QtGui import QFont

# İş sınıflarını içe aktar
from salon import Salon
from employee import Employee
from customer import Customer
from service import Service
from appointment import Appointment

class MusteriEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Müşteri Ekle")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form
        form_layout = QVBoxLayout()
        
        # İsim
        isim_layout = QHBoxLayout()
        isim_layout.addWidget(QLabel("İsim:"))
        self.isim_input = QLineEdit()
        isim_layout.addWidget(self.isim_input)
        form_layout.addLayout(isim_layout)
        
        # Telefon
        telefon_layout = QHBoxLayout()
        telefon_layout.addWidget(QLabel("Telefon:"))
        self.telefon_input = QLineEdit()
        telefon_layout.addWidget(self.telefon_input)
        form_layout.addLayout(telefon_layout)
        
        layout.addLayout(form_layout)
        
        # Butonlar - DÜZELTME: Iptal yerine Cancel kullan
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                    QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Buton metinlerini Türkçe yap
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        ok_button.setText("Tamam")
        cancel_button.setText("İptal")
        
        layout.addWidget(button_box)
    
    def get_musteri_data(self):
        return {
            'user_full_name': self.isim_input.text(),
            'phone': self.telefon_input.text()
        }

class BarberDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://localhost:8000/api"
        self.current_customer = None
        self.salonlar = []
        self.calisanlar = []
        self.hizmetler = []
        self.musteriler = []  # Yerel Customer nesneleri listesi
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle("SAÜ Kuaför Randevu Sistemi - Masaüstü Uygulama")
        self.setGeometry(100, 100, 1200, 800)
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana layout
        main_layout = QVBoxLayout(central_widget)
        
        # Başlık
        title_label = QLabel("SAÜ Kuaför Randevu Sistemi")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Randevu Oluşturma Tab'ı
        self.create_appointment_tab()
        
        # Randevu Görüntüleme Tab'ı
        self.create_view_appointments_tab()
        
        # Salon Bilgileri Tab'ı
        self.create_salon_info_tab()
    
    def create_appointment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Müşteri Bilgileri
        musteri_group = QGroupBox("Müşteri Bilgileri")
        musteri_layout = QVBoxLayout(musteri_group)
        
        musteri_form_layout = QHBoxLayout()
        musteri_form_layout.addWidget(QLabel("Müşteri Seç:"))
        self.musteri_combo = QComboBox()
        musteri_form_layout.addWidget(self.musteri_combo)
        
        self.btn_yeni_musteri = QPushButton("Yeni Müşteri")
        self.btn_yeni_musteri.clicked.connect(self.yeni_musteri)
        musteri_form_layout.addWidget(self.btn_yeni_musteri)
        
        self.btn_musterileri_yenile = QPushButton("Müşterileri Yenile")
        self.btn_musterileri_yenile.clicked.connect(self.load_musteriler)
        musteri_form_layout.addWidget(self.btn_musterileri_yenile)
        
        musteri_layout.addLayout(musteri_form_layout)
        layout.addWidget(musteri_group)
        
        # Salon ve Hizmet Seçimi
        hizmet_group = QGroupBox("Hizmet Seçimi")
        hizmet_layout = QVBoxLayout(hizmet_group)
        
        # Salon seçimi
        salon_layout = QHBoxLayout()
        salon_layout.addWidget(QLabel("Salon:"))
        self.salon_combo = QComboBox()
        self.salon_combo.currentTextChanged.connect(self.on_salon_degisti)
        salon_layout.addWidget(self.salon_combo)
        hizmet_layout.addLayout(salon_layout)
        
        # Hizmet seçimi
        hizmet_form_layout = QHBoxLayout()
        hizmet_form_layout.addWidget(QLabel("Hizmet:"))
        self.hizmet_combo = QComboBox()
        hizmet_form_layout.addWidget(self.hizmet_combo)
        hizmet_layout.addLayout(hizmet_form_layout)
        
        layout.addWidget(hizmet_group)
        
        # Çalışan Seçimi
        calisan_group = QGroupBox("Çalışan Seçimi")
        calisan_layout = QVBoxLayout(calisan_group)
        
        calisan_form_layout = QHBoxLayout()
        calisan_form_layout.addWidget(QLabel("Çalışan:"))
        self.calisan_combo = QComboBox()
        calisan_form_layout.addWidget(self.calisan_combo)
        calisan_layout.addLayout(calisan_form_layout)
        
        layout.addWidget(calisan_group)
        
        # Tarih ve Saat
        tarihsaat_group = QGroupBox("Tarih ve Saat")
        tarihsaat_layout = QHBoxLayout(tarihsaat_group)
        
        tarihsaat_layout.addWidget(QLabel("Tarih:"))
        self.tarih_edit = QDateEdit()
        self.tarih_edit.setDate(QDate.currentDate())
        self.tarih_edit.setCalendarPopup(True)
        tarihsaat_layout.addWidget(self.tarih_edit)
        
        tarihsaat_layout.addWidget(QLabel("Saat:"))
        self.saat_edit = QTimeEdit()
        self.saat_edit.setTime(QTime.currentTime())
        tarihsaat_layout.addWidget(self.saat_edit)
        
        layout.addWidget(tarihsaat_group)
        
        # Butonlar
        button_layout = QHBoxLayout()
        self.btn_randevu_olustur = QPushButton("Randevu Oluştur")
        self.btn_randevu_olustur.clicked.connect(self.nesnelerle_randevu_olustur)
        self.btn_randevu_olustur.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        self.btn_temizle = QPushButton("Formu Temizle")
        self.btn_temizle.clicked.connect(self.formu_temizle)
        self.btn_temizle.setStyleSheet("background-color: #f44336; color: white;")
        
        button_layout.addWidget(self.btn_randevu_olustur)
        button_layout.addWidget(self.btn_temizle)
        layout.addLayout(button_layout)
        
        # Durum mesajı
        self.durum_text = QTextEdit()
        self.durum_text.setMaximumHeight(100)
        layout.addWidget(QLabel("Durum:"))
        layout.addWidget(self.durum_text)
        
        self.tabs.addTab(tab, "Randevu Oluştur")
    
    def create_view_appointments_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Kontrol butonları
        control_layout = QHBoxLayout()
        self.btn_randevulari_yenile = QPushButton("Randevuları Yenile")
        self.btn_randevulari_yenile.clicked.connect(self.load_randevular)
        control_layout.addWidget(self.btn_randevulari_yenile)
        
        layout.addLayout(control_layout)
        
        # Randevu tablosu
        self.randevu_tablosu = QTableWidget()
        self.randevu_tablosu.setColumnCount(6)
        self.randevu_tablosu.setHorizontalHeaderLabels([
            "ID", "Müşteri", "Çalışan", "Hizmet", "Tarih/Saat", "Durum"
        ])
        layout.addWidget(self.randevu_tablosu)
        
        self.tabs.addTab(tab, "Randevuları Görüntüle")
    
    def create_salon_info_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.salon_bilgi_text = QTextEdit()
        layout.addWidget(self.salon_bilgi_text)
        
        self.tabs.addTab(tab, "Salon Bilgileri")
    
    def load_data(self):
        """Tüm verileri API'den yükle"""
        try:
            self.load_salonlar()
            self.load_calisanlar()
            self.load_musteriler()
            self.load_randevular()
            self.salon_bilgilerini_guncelle()
            self.durum_logu("Veriler başarıyla yüklendi")
        except Exception as e:
            self.durum_logu(f"Hata: {str(e)}")
    
    def load_salonlar(self):
        """Salonları API'den yükle"""
        try:
            response = requests.get(f"{self.api_base_url}/salons/")
            if response.status_code == 200:
                self.salonlar = response.json()
                self.salon_combo.clear()
                for salon in self.salonlar:
                    self.salon_combo.addItem(salon['name'], salon['id'])
        except Exception as e:
            self.durum_logu(f"Salon yükleme hatası: {str(e)}")
    
    def load_calisanlar(self):
        """Çalışanları API'den yükle ve nesneler oluştur"""
        try:
            response = requests.get(f"{self.api_base_url}/employees/")
            if response.status_code == 200:
                calisanlar_data = response.json()
                self.calisanlar = []
                self.calisan_combo.clear()
                
                for data in calisanlar_data:
                    # Employee nesnesi oluştur
                    calisan = Employee(data['user_full_name'], data.get('phone', ''), data['role'])
                    calisan.employee_id = data['id']
                    self.calisanlar.append(calisan)
                    
                    # ComboBox'a ekle
                    goruntuleme_adi = f"{calisan.name} ({calisan.role})"
                    self.calisan_combo.addItem(goruntuleme_adi, calisan.employee_id)
                    
        except Exception as e:
            self.durum_logu(f"Çalışan yükleme hatası: {str(e)}")
    
    def load_musteriler(self):
        """Müşterileri API'den yükle ve nesneler oluştur"""
        try:
            response = requests.get(f"{self.api_base_url}/customers/")
            if response.status_code == 200:
                musteriler_data = response.json()
                self.musteriler = []
                self.musteri_combo.clear()
                
                for data in musteriler_data:
                    # Customer nesnesi oluştur
                    musteri = Customer(data['user_full_name'], data['phone'])
                    musteri.customer_id = data['id']
                    self.musteriler.append(musteri)
                    
                    # ComboBox'a ekle
                    goruntuleme_adi = f"{musteri.name} - {musteri.phone}"
                    self.musteri_combo.addItem(goruntuleme_adi, musteri.customer_id)
                    
        except Exception as e:
            self.durum_logu(f"Müşteri yükleme hatası: {str(e)}")
    
    def load_randevular(self):
        """Randevuları API'den yükle"""
        try:
            response = requests.get(f"{self.api_base_url}/appointments/")
            if response.status_code == 200:
                randevular = response.json()
                self.randevu_tablosu.setRowCount(len(randevular))
                
                for satir, randevu in enumerate(randevular):
                    self.randevu_tablosu.setItem(satir, 0, QTableWidgetItem(str(randevu['id'])))
                    self.randevu_tablosu.setItem(satir, 1, QTableWidgetItem(randevu['customer_name']))
                    self.randevu_tablosu.setItem(satir, 2, QTableWidgetItem(randevu['employee_name']))
                    self.randevu_tablosu.setItem(satir, 3, QTableWidgetItem(randevu['service_name']))
                    self.randevu_tablosu.setItem(satir, 4, QTableWidgetItem(f"{randevu['date']} {randevu['time']}"))
                    self.randevu_tablosu.setItem(satir, 5, QTableWidgetItem(randevu['status']))
                    
        except Exception as e:
            self.durum_logu(f"Randevu yükleme hatası: {str(e)}")
    
    def on_salon_degisti(self):
        """Salon değiştiğinde hizmetleri güncelle"""
        try:
            salon_id = self.salon_combo.currentData()
            if salon_id:
                response = requests.get(f"{self.api_base_url}/salons/{salon_id}/services/")
                if response.status_code == 200:
                    hizmetler = response.json()
                    self.hizmet_combo.clear()
                    for hizmet in hizmetler:
                        goruntuleme_metni = f"{hizmet['name']} - {hizmet['duration']}dk - {hizmet['price']}TL"
                        self.hizmet_combo.addItem(goruntuleme_metni, hizmet['id'])
        except Exception as e:
            self.durum_logu(f"Hizmet yükleme hatası: {str(e)}")
    
    def yeni_musteri(self):
        """Yeni müşteri eklemek için diyalog açar"""
        dialog = MusteriEkleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            musteri_data = dialog.get_musteri_data()
            if musteri_data['user_full_name'] and musteri_data['phone']:
                # Customer nesnesi oluştur
                musteri = Customer(musteri_data['user_full_name'], musteri_data['phone'])
                
                # Backend'e gönder
                basarili = self.musteriyi_backende_gonder(musteri)
                if basarili:
                    # Müşteri listesini yenile
                    self.load_musteriler()
                    QMessageBox.information(self, "Başarılı", "Müşteri başarıyla eklendi!")
                else:
                    QMessageBox.warning(self, "Hata", "Müşteri eklenirken hata oluştu!")
    
    def musteriyi_backende_gonder(self, musteri):
        """Müşteriyi backend'e gönder"""
        try:
            musteri_data = {
                'user_full_name': musteri.name,
                'phone': musteri.phone
            }
            response = requests.post(f"{self.api_base_url}/customers/", json=musteri_data)
            return response.status_code == 201
        except Exception as e:
            print(f"Müşteri gönderme hatası: {e}")
            return False
    
    def nesnelerle_randevu_olustur(self):
        """Python nesnelerini kullanarak randevu oluştur"""
        try:
            # Form verilerini al
            musteri_id = self.musteri_combo.currentData()
            calisan_id = self.calisan_combo.currentData()
            hizmet_id = self.hizmet_combo.currentData()
            tarih = self.tarih_edit.date().toString("yyyy-MM-dd")
            saat = self.saat_edit.time().toString("HH:mm")
            tarihsaat_str = f"{tarih} {saat}"
            
            if not all([musteri_id, calisan_id, hizmet_id, tarih, saat]):
                QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
                return
            
            # İlgili nesneleri bul
            musteri = next((m for m in self.musteriler if m.customer_id == musteri_id), None)
            calisan = next((c for c in self.calisanlar if c.employee_id == calisan_id), None)
            
            if not all([musteri, calisan]):
                QMessageBox.warning(self, "Hata", "Geçersiz veri!")
                return
            
            # Service nesnesi oluştur (API'den gelen verilerle)
            hizmet_data = {
                'name': self.hizmet_combo.currentText().split(' - ')[0],
                'duration': 60,  # Varsayılan değer
                'base_price': 100  # Varsayılan değer
            }
            hizmet = Service(hizmet_data['name'], hizmet_data['duration'], hizmet_data['base_price'])
            hizmet.service_id = hizmet_id
            
            # Randevu nesnesi oluştur
            randevu = Appointment(
                datetime=tarihsaat_str,
                customer=musteri,
                employee=calisan,
                service=hizmet
            )
            
            # Çakışma kontrolü
            if randevu.check_collision():
                QMessageBox.warning(self, "Çakışma", "Bu çalışanın aynı saatte başka randevusu var!")
                return
            
            # Backend'e gönder
            sonuc = self.randevuyu_backende_gonder(randevu, hizmet_id)
            if "başarı" in sonuc.lower():
                QMessageBox.information(self, "Başarılı", "Randevu başarıyla oluşturuldu!")
                self.formu_temizle()
                self.load_randevular()
            else:
                QMessageBox.warning(self, "Hata", sonuc)
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")
    
    def randevuyu_backende_gonder(self, randevu, hizmet_id):
        """Randevuyu backend'e gönder"""
        try:
            randevu_data = {
                'customer': randevu.customer.customer_id,
                'employee': randevu.employee.employee_id,
                'service': hizmet_id,
                'date': randevu.datetime.split(" ")[0],
                'time': randevu.datetime.split(" ")[1],
                'status': 'pending'
            }
            
            response = requests.post(f"{self.api_base_url}/appointments/", json=randevu_data)
            
            if response.status_code == 201:
                # Yerel randevular listesine ekle
                Appointment.all_appointments.append(randevu)
                return "Randevu başarıyla oluşturuldu!"
            else:
                hata_mesaji = response.json().get('error', 'Bilinmeyen hata')
                return f"Hata: {hata_mesaji}"
                
        except Exception as e:
            return f"Bağlantı hatası: {str(e)}"
    
    def formu_temizle(self):
        """Formu temizle"""
        self.tarih_edit.setDate(QDate.currentDate())
        self.saat_edit.setTime(QTime.currentTime())
        self.durum_logu("Form temizlendi")
    
    def salon_bilgilerini_guncelle(self):
        """Salon bilgilerini güncelle"""
        bilgi_metni = "=== SALON BİLGİLERİ ===\n\n"
        
        for salon in self.salonlar:
            bilgi_metni += f"🔷 {salon['name']}\n"
            bilgi_metni += f"   🕒 Çalışma Saatleri: {salon['working_start']} - {salon['working_end']}\n"
            if salon['phone']:
                bilgi_metni += f"   📞 Telefon: {salon['phone']}\n"
            if salon['description']:
                bilgi_metni += f"   📝 Açıklama: {salon['description']}\n"
            bilgi_metni += "\n"
            
            # Hizmetleri getir
            try:
                response = requests.get(f"{self.api_base_url}/salons/{salon['id']}/services/")
                if response.status_code == 200:
                    hizmetler = response.json()
                    for hizmet in hizmetler:
                        bilgi_metni += f"   ✂️ {hizmet['name']} - {hizmet['duration']}dk - {hizmet['price']}TL\n"
            except:
                pass
            
            bilgi_metni += "\n" + "="*50 + "\n\n"
        
        self.salon_bilgi_text.setText(bilgi_metni)
    
    def durum_logu(self, mesaj):
        """Durum mesajını logla"""
        zaman_damgasi = datetime.now().strftime("%H:%M:%S")
        self.durum_text.append(f"[{zaman_damgasi}] {mesaj}")

def main():
    app = QApplication(sys.argv)
    
    # Uygulama stilini ayarla
    app.setStyle('Fusion')
    
    window = BarberDesktopApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()