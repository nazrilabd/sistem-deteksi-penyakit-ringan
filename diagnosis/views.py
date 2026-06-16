import joblib
import pandas as pd
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ==========================================
# 1. LOAD MODEL ML & KONFIGURASI GLOBAL
# ==========================================
model = joblib.load("disease_model.pkl")
FITUR = list(model.feature_names_in_)

GEJALA = {
    "itching": "Gatal-gatal pada kulit",
    "skin_rash": "Ruam pada kulit",
    "nodal_skin_eruptions": "Benjolan kecil pada kulit",
    "continuous_sneezing": "Bersin terus-menerus",
    "shivering": "Tubuh menggigil",
    "chills": "Meriang / Kendinginan",
    "joint_pain": "Nyeri pada persendian",
    "stomach_pain": "Sakit / perih perut",
    "acidity": "Asam lambung meningkat",
    "ulcers_on_tongue": "Sariawan pada lidah",
    "muscle_wasting": "Penyusutan massa otot",
    "vomiting": "Muntah-muntah",
    "burning_micturition": "Sensasi terbakar saat buang air kecil",
    "spotting_ urination": "Bercak darah saat buang air kecil",  
    "fatigue": "Kelelahan ekstrem / lesu",
    "weight_gain": "Kenaikan berat badan drastis",
    "anxiety": "Rasa gelisah / cemas berlebih",
    "cold_hands_and_feets": "Sensasi dingin pada tangan dan kaki",
    "mood_swings": "Perubahan suasana hati mendadak",
    "weight_loss": "Penurunan berat badan drastis",
    "restlessness": "Gelisah / tidak bisa diam",
    "lethargy": "Lemmas / tidak bertenaga total",
    "patches_in_throat": "Bercak keputihan di tenggorokan",
    "irregular_sugar_level": "Kadar gula darah tidak stabil",
    "cough": "Batuk-batuk",
    "high_fever": "Demam tinggi",
    "sunken_eyes": "Mata cekung",
    "breathlessness": "Sesak napas / engap",
    "sweating": "Keringat berlebih tanpa aktivitas",
    "dehydration": "Gejala dehidrasi / kekurangan cairan",
    "indigestion": "Gangguan pencernaan / begah",
    "headache": "Sakit kepala",
    "yellowish_skin": "Kulit tampak menguning",
    "dark_urine": "Urine berwarna gelap pekat",
    "nausea": "Rasa mual",
    "loss_of_appetite": "Kehilangan nafsu makan",
    "pain_behind_the_eyes": "Nyeri di bagian belakang mata",
    "back_pain": "Nyeri punggung",
    "constipation": "Sembelit / susah buang air besar",
    "abdominal_pain": "Nyeri perut bagian dalam",
    "diarrhoea": "Diare / sering buang air besar cair",
    "mild_fever": "Demam ringan / sumeng",
    "yellow_urine": "Urine berwarna kuning cerah",
    "yellowing_of_eyes": "Bagian putih mata menguning",
    "acute_liver_failure": "Kerusakan / gagal hati akut",
    "fluid_overload": "Penumpukan cairan tubuh",
    "swelling_of_stomach": "Perut membengkak",
    "swelled_lymph_nodes": "Pembengkakan kelenjar getah bening",
    "malaise": "Rasa tidak enak badan secara umum",
    "blurred_and_distorted_vision": "Penglihatan kabur atau berbayang",
    "phlegm": "Batuk berdahak",
    "throat_irritation": "Tenggorokan terasa gatal / iritasi",
    "redness_of_eyes": "Mata memerah",
    "sinus_pressure": "Tekanan pada area sinus (wajah)",
    "runny_nose": "Hidung meler",
    "congestion": "Hidung tersumbat",
    "chest_pain": "Nyeri pada bagian dada",
    "weakness_in_limbs": "Kelemahan pada tangan / kaki",
    "fast_heart_rate": "Detak jantung berdegub cepat",
    "pain_during_bowel_movements": "Nyeri saat buang air besar",
    "pain_in_anal_region": "Nyeri di sekitar anus",
    "bloody_stool": "Feses berdarah",
    "irritation_in_anus": "Rasa gatal / iritasi pada anus",
    "neck_pain": "Nyeri pada leher",
    "dizziness": "Pusing / kliyengan / berputar",
    "cramps": "Kram pada otot",
    "bruising": "Kulit mudah memar",
    "obesity": "Obesitas / berat badan berlebih",
    "swollen_legs": "Pembengkakan pada kaki",
    "swollen_blood_vessels": "Pembengkakan pembuluh darah kulit",
    "puffy_face_and_eyes": "Wajah dan mata sembab",
    "enlarged_thyroid": "Pembesaran kelenjar tiroid (gondok)",
    "brittle_nails": "Kuku rapuh dan mudah patah",
    "swollen_extremeties": "Pembengkakan ujung jari tangan/kaki",
    "excessive_hunger": "Rasa lapar yang berlebihan",
    "extra_marital_contacts": "Riwayat kontak seksual berisiko",
    "drying_and_tingling_lips": "Bibir kering dan kesemutan",
    "slurred_speech": "Bicara ranyau / cadel mendadak",
    "knee_pain": "Nyeri pada lutut",
    "hip_joint_pain": "Nyeri pada sendi panggul",
    "muscle_weakness": "Kelemahan otot tubuh",
    "stiff_neck": "Leher kaku / sulit menengok",
    "swelling_joints": "Pembengkakan pada area sendi",
    "movement_stiffness": "Kekakuan saat menggerakkan tubuh",
    "spinning_movements": "Sensasi tubuh berputar",
    "loss_of_balance": "Kehilangan keseimbangan tubuh",
    "unsteadiness": "Tubuh sempoyongan saat berdiri",
    "weakness_of_one_body_side": "Kelemahan pada satu sisi tubuh",
    "loss_of_smell": "Kehilangan indra penciuman (anosmia)",
    "bladder_discomfort": "Rasa tidak nyaman di kandung kemih",
    "foul_smell_of urine": "Urine berbau menyengat / tidak sedap",  
    "continuous_feel_of_urine": "Sensasi ingin buang air kecil terus",
    "passage_of_gases": "Sering buang angin / kentut",
    "internal_itching": "Rasa gatal di bagian dalam tubuh",
    "toxic_look_(typhos)": "Wajah tampak pucat dan lesu khas tipus",
    "depression": "Suasana hati depresi / tertekan",
    "irritability": "Mudah marah atau tersinggung",
    "muscle_pain": "Nyeri pada otot",
    "altered_sensorium": "Penurunan/perubahan kesadaran medis",
    "red_spots_over_body": "Bintik-bintik merah di seluruh tubuh",
    "belly_pain": "Sakit perut bagian bawah",
    "abnormal_menstruation": "Siklus menstruasi tidak teratur",
    "dischromic _patches": "Bercak kulit yang berubah warna",  
    "watering_from_eyes": "Mata terus berair",
    "increased_appetite": "Nafsu makan melonjak",
    "polyuria": "Volume buang air kecil meningkat (poliuria)",
    "family_history": "Memiliki riwayat penyakit keluarga sejenis",
    "mucoid_sputum": "Dahak kental berlendir",
    "rusty_sputum": "Dahak berwarna kecokelatan seperti karat",
    "lack_of_concentration": "Sulit memusatkan konsentrasi",
    "visual_disturbances": "Gangguan pada penglihatan",
    "receiving_blood_transfusion": "Riwayat menerima transfusi darah",
    "receiving_unsterile_injections": "Riwayat menerima suntikan tidak steril",
    "coma": "Kondisi tidak sadarkan diri / koma",
    "stomach_bleeding": "Pendarahan pada lambung",
    "distention_of_abdomen": "Perut kembung / membesar",
    "history_of_alcohol_consumption": "Riwayat rutin mengonsumsi alkohol",
    "fluid_overload.1": "Kelebihan cairan sekunder",  
    "blood_in_sputum": "Batuk berdarah / ada darah di dahak",
    "prominent_veins_on_calf": "Urat menonjol jelas di betis",
    "palpitations": "Jantung berdebar-debar keras",
    "painful_walking": "Rasa nyeri saat berjalan",
    "pus_filled_pimples": "Jerawat meradang bernanah",
    "blackheads": "Komedo hitam pada kulit",
    "scurring": "Kerusakan tekstur kulit / bopeng",
    "skin_peeling": "Kulit mengelupas sendiri",
    "silver_like_dusting": "Sisik kulit keperakan (pola psoriasis)",
    "small_dents_in_nails": "Lekukan-lekukan kecil pada kuku",
    "inflammatory_nails": "Peradangan / infeksi pada kuku",
    "blister": "Lepuhan berisi cairan pada kulit",
    "red_sore_around_nose": "Luka kemerahan di sekitar hidung",
    "yellow_crust_ooze": "Cairan kuning yang mengering jadi kerak"
}

PENYAKIT = {
    "Fungal infection": "Infeksi Jamur",
    "Allergy": "Alergi",
    "GERD": "GERD (Asam Lambung)",
    "Chronic cholestasis": "Kolestasis Kronis",
    "Drug Reaction": "Reaksi Efek Samping Obat",
    "Peptic ulcer diseae": "Tukak Lambung",
    "AIDS": "AIDS / HIV",
    "Diabetes ": "Diabetes Melitus",  
    "Gastroenteritis": "Gastroenteritis (Flu Perut)",
    "Bronchial Asthma": "Asma Bronkial",
    "Hypertension ": "Hipertensi (Tekanan Darah Tinggi)",  
    "Migraine": "Migrain",
    "Cervical spondylosis": "Spondilosi Servikal",
    "Paralysis (brain hemorrhage)": "Paralisis (Stroke Pendarahan Otak)",
    "Jaundice": "Penyakit Kuning (Ikterus)",
    "Malaria": "Malaria",
    "Chicken pox": "Cacar Air",
    "Dengue": "Demam Berdarah (DBD)",
    "Typhoid": "Tifus (Demam Tifoid)",
    "hepatitis A": "Hepatitis A",
    "Hepatitis B": "Hepatitis B",
    "Hepatitis C": "Hepatitis C",
    "Hepatitis D": "Hepatitis D",
    "Hepatitis E": "Hepatitis E",
    "Alcoholic hepatitis": "Hepatitis Alkoholik",
    "Tuberculosis": "Tuberkulosis (TBC)",
    "Common Cold": "Flu Ringan (Common Cold)",
    "Pneumonia": "Pneumonia (Paru-Paru Basah)",
    "Dimorphic hemmorhoids(piles)": "Wasir / Ambeien",
    "Heart attack": "Serangan Jantung",
    "Varicose veins": "Varises",
    "Hypothyroidism": "Hipotiroidisme",
    "Hyperthyroidism": "Hipertiroidisme",
    "Hypoglycemia": "Hipoglikemia (Gula Darah Rendah)",
    "Osteoarthristis": "Osteoarthritis (Pengapuran Sendi)",
    "Arthritis": "Artritis (Radang Sendi)",
    "(vertigo) Paroymsal  Positional Vertigo": "Vertigo (BPPV)",
    "Acne": "Jerawat",
    "Urinary tract infection": "Infeksi Saluran Kemih (ISK)",
    "Psoriasis": "Psoriasis",
    "Impetigo": "Impetigo"
}


# ==========================================
# 2. VIEW PAGES (HOME & ABOUT)
# ==========================================
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


# ==========================================
# 3. VIEW PROSES DIAGNOSIS (POST & GET)
# ==========================================
def diagnosis(request):
    hasil = None
    top3 = None
    chart_labels = []
    chart_values = []

    nama = ""
    nik = ""
    gender = ""
    usia = ""
    no_hp = ""
    alamat = ""
    gejala_pasien = ""

    if request.method == "POST":
        # Data Pasien
        nama = request.POST.get("nama")
        nik = request.POST.get("nik")
        gender = request.POST.get("gender")
        usia = request.POST.get("usia")
        no_hp = request.POST.get("no_hp")
        alamat = request.POST.get("alamat")

        # Proses Gejala Terpilih
        gejala_dipilih = request.POST.getlist("gejala")
        
        # Penggabungan multi-gejala menjadi satu string teks
        gejala_terjemahan = [GEJALA.get(g, g) for g in gejala_dipilih]
        gejala_pasien = ", ".join(gejala_terjemahan) if gejala_terjemahan else "-"

        # Buat struktur dataframe untuk model
        data = {fitur: 0 for fitur in FITUR}
        for gejala in gejala_dipilih:
            if gejala in data:
                data[gejala] = 1

        df = pd.DataFrame([data])

        # Eksekusi Prediksi ML
        prediksi = model.predict(df)[0]
        probabilitas = model.predict_proba(df)[0]

        hasil = PENYAKIT.get(prediksi, prediksi)

        # Kelola Hasil Probabilitas Top 3
        hasil_list = list(zip(model.classes_, probabilitas))
        hasil_list.sort(key=lambda x: x[1], reverse=True)

        top3 = []
        for penyakit, nilai in hasil_list[:3]:
            nama_penyakit = PENYAKIT.get(penyakit, penyakit)
            persen = round(nilai * 100, 2)
            
            top3.append((nama_penyakit, persen))
            chart_labels.append(nama_penyakit)
            chart_values.append(persen)

    return render(
        request,
        "diagnosis.html",
        {
            "gejala": GEJALA,
            "hasil": hasil,
            "top3": top3,
            "chart_labels": chart_labels,
            "chart_values": chart_values,
            "nama": nama,
            "nik": nik,
            "gender": gender,
            "usia": usia,
            "no_hp": no_hp,
            "alamat": alamat,
            "gejala_pasien": gejala_pasien,
        }
    )


# ==========================================
# 4. ENGINE GENERATOR UNDUH LAPORAN PDF
# ==========================================
def download_pdf(request):
    # Mengambil parameter data pasien & rekam gejala dari URL GET
    nama = request.GET.get("nama", "-")
    nik = request.GET.get("nik", "-")
    gender = request.GET.get("gender", "-")
    usia = request.GET.get("usia", "-")
    no_hp = request.GET.get("no_hp", "-")
    alamat = request.GET.get("alamat", "-")
    gejala = request.GET.get("gejala", "-")

    hasil = request.GET.get("hasil", "-")
    top1 = request.GET.get("top1", "-")
    top2 = request.GET.get("top2", "-")
    top3 = request.GET.get("top3", "-")

    # Setup HttpResponse untuk Dokumen PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="laporan_diagnosis.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Header Dokumen
  # Header Dokumen
    elements.append(Paragraph("LAPORAN HASIL SKRINING GEJALA", styles["Title"]))
    elements.append(Paragraph("Sistem Triase Mandiri Berbasis Probabilitas Statistika", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # --- TABEL 1: IDENTITAS PASIEN ---
    elements.append(Paragraph("<b>IDENTITAS PASIEN</b>", styles["Heading2"]))
    
    data_pasien = [
        ["Nama", nama],
        ["NIK", nik],
        ["Jenis Kelamin", gender],
        ["Usia", f"{usia} Tahun"],
        ["No. HP", no_hp],
        ["Alamat", alamat],
    ]

    tabel_pasien = Table(data_pasien, colWidths=[120, 320])
    tabel_pasien.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabel_pasien)
    elements.append(Spacer(1, 20))

    # --- TABEL 2: GEJALA PASIEN (BARU) ---
    elements.append(Paragraph("<b>GEJALA YANG DIALAMI</b>", styles["Heading2"]))

    # Tetap gunakan paragraph agar teks wrap kebawah jika panjang
    gejala_paragraph = Paragraph(gejala, styles["Normal"])
    
    data_gejala = [
        ["Daftar Gejala", gejala_paragraph]
    ]
    
    # Kolom disamakan ukurannya dengan tabel pasien agar sejajar presisi
    tabel_gejala = Table(data_gejala, colWidths=[120, 320])
    tabel_gejala.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), # Dibuat rata atas agar rapi
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(tabel_gejala)
    elements.append(Spacer(1, 20))

    # --- TABEL 3: HASIL DIAGNOSIS ---
    elements.append(Paragraph("<b>HASIL DIAGNOSIS</b>", styles["Heading2"]))
    hasil_table = Table([["Penyakit Utama", hasil]], colWidths=[150, 290])
    hasil_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (0, 0), colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(hasil_table)
    elements.append(Spacer(1, 20))

    # --- TABEL 4: PREDIKSI TOP 3 ---
    elements.append(Paragraph("<b>TOP 3 KEMUNGKINAN PENYAKIT</b>", styles["Heading2"]))
    prediksi_table = Table([
        ["Peringkat", "Penyakit"],
        ["1", top1],
        ["2", top2],
        ["3", top3],
    ], colWidths=[80, 360])
    prediksi_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(prediksi_table)
    elements.append(Spacer(1, 30))

    # --- FOOTER ---
    # --- FOOTER ---
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")
    elements.append(Paragraph(f"Tanggal Skrining: {tanggal}", styles["Normal"]))
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Hasil ini merupakan prediksi awal untuk keperluan triase mandiri berdasarkan algoritma Bernoulli Naive Bayes, bukan pengganti diagnosis resmi dokter.", styles["Italic"]))
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Platform Triase Mandiri - Informatika | Fakultas sains Dan Teknologi | Universitas Indonesia Mandiri", styles["Normal"]))

    doc.build(elements)
    return response