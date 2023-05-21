
to_turkish = {
    "Student ID" : "Öğrenci Numarası",
    "National ID" : "T.C Kimlik Numarası",
    "Name" : "İsim",
    "Surname" : "Soyisim",
    "Faculty / Department" : "Fakülte / Bölüm",
    "Program Name" : "Program Adı",
    "Language of Instruction" : "Öğretim Dili",
    "Student Status" : "Öğrenci Durumu",

    "Load" : "Yükle",
    "Save" : "Kaydet",
    "Load Data" : "Verileri Yükle",
    "Save Data" : "Verileri Kaydet",
    "Saving Data" : "Veriler Kaydediliyor",
    "Loading Data" : "Veriler Yükleniyor",
    "Exit" : "Çıkış",
    "Reset" : "Sıfırla",
    "Restart" : "Yeniden Başlat",
    "Export Data" : "Verileri Dışa Aktar",
    "Select a document to load" : "Yüklemek için bir belge seçin",
    "Cancel" : "İptal",
    "Enter a name for the document" : "Belge için bir isim girin",
    "Error" : "Hata",
    "Please enter a name for the document" : "Lütfen belge için bir isim girin",
    "A document with this name already exists" : "Bu isimde bir belge zaten var",
    "No data found for this user" : "Bu kullanıcı için veri bulunamadı",
    "Select Output Folder" : "Çıktı Klasörünü Seçin",
    "Exporting Data" : "Veriler Dışa Aktarılıyor",

    
}

def translate(text, language) :
    if language == "Turkish" :
        return to_turkish[text]
    else :
        return text