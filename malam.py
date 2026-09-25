# Isi cerita tiap malam.
# Teks pesan hanya boleh berisi huruf A-Z, angka 0-9, dan spasi.
#
# Jenis isi "urutan":
#   pesan : pesan biasa, tidak perlu dibalas
#   sunyi : periode sunyi, desis berhenti beberapa detik
#   minta : pesan yang harus dibalas. Setelah membalas, pesan di "benar",
#           "salah", atau "diam" diputar sesuai hasil balasan.

MALAM = [
    # ---------------------------------------------------------- malam 1
    {
        "kapal": "KM SINAR BARU",
        "satuan": 120,          # ms per titik, makin kecil makin cepat
        "derau": 0.0,           # bagian huruf yang tertutup derau (tampil sebagai ?)
        "putar_ulang": 3,
        "waktu_balas": 60,      # detik
        "lembar_salah": False,
        "peta": [("Dari UTARA", "180"), ("Dari TIMUR", "270"), ("Dari BARAT", "090")],
        "karang": None,
        "urutan": [
            {"jenis": "pesan", "teks": "KABUT TEBAL"},
            {"jenis": "sunyi", "detik": 6},
            {"jenis": "minta", "teks": "POSISI TIMUR MINTA ARAH", "jawaban": "270",
             "benar": ["TERIMA KASIH POS"],
             "salah": ["KAMI IKUTI ARAHMU", "KANDAS DI PASIR"],
             "diam": ["POS JAWAB", "POS JAWAB"],
             "nasib": {"benar": "sampai di pelabuhan",
                       "salah": "kandas di pasir, awak selamat",
                       "diam": "hilang kontak"}},
        ],
    },
    # ---------------------------------------------------------- malam 2
    {
        "kapal": "KM SURYA KENCANA",
        "satuan": 100,
        "derau": 0.15,
        "putar_ulang": 2,
        "waktu_balas": 45,
        "lembar_salah": False,
        "peta": [("Dari UTARA", "180"), ("Dari TIMUR LAUT", "225"), ("Dari BARAT LAUT", "135")],
        "karang": "120",
        "urutan": [
            {"jenis": "pesan", "teks": "MESIN LEMAH"},
            {"jenis": "pesan", "teks": "TUJUH ORANG"},
            {"jenis": "sunyi", "detik": 6},
            {"jenis": "minta", "teks": "POSISI BARAT LAUT MINTA ARAH", "jawaban": "135",
             "benar": ["PELABUHAN TERLIHAT"],
             "salah": ["KAMI IKUTI ARAHMU", "KARANG AIR MASUK", "TOLO"],
             "diam": ["POS JAWAB", "POS JAWAB"],
             "nasib": {"benar": "selamat, 7 orang",
                       "salah": "hilang di perairan karang",
                       "diam": "hilang kontak"}},
        ],
    },
    # ---------------------------------------------------------- malam 3
    {
        "kapal": "KM BINTANG TIMUR",
        "satuan": 90,
        "derau": 0.25,
        "putar_ulang": 1,
        "waktu_balas": 30,
        "lembar_salah": True,
        "peta": [("Dari UTARA", "180"), ("Dari TIMUR LAUT", "225"), ("Dari BARAT LAUT", "135")],
        "karang": "120",
        "urutan": [
            {"jenis": "minta", "teks": "POSISI TIMUR LAUT MINTA ARAH", "jawaban": "225",
             "benar": ["TERIMA KASIH POS"],
             "salah": ["KAMI IKUTI ARAHMU"],
             "diam": ["POS JAWAB", "POS JAWAB"],
             "nasib": {"benar": "sampai di pelabuhan",
                       "salah": "hilang kontak",
                       "diam": "hilang kontak"}},
            {"jenis": "sunyi", "detik": 10},
            # sinyal yang tidak ada di manifes. "lemah" = pelan dan tanpa desis
            {"jenis": "minta", "dari": "TIDAK DIKENAL", "lemah": True,
             "teks": "POS DUA BELAS MINTA ARAH", "jawaban": None,
             "dibalas": ["TERIMA KASIH"],
             "diam": []},
            {"jenis": "sunyi", "detik": 8},
        ],
    },
]
