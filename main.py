from flask import Flask, render_template_string, request, jsonify, send_file
import requests
import json
import os
from datetime import datetime
import random

app = Flask(__name__)

# =====================================================
#  البيانات الثابتة
# =====================================================

ALL_SURAHS = [
    {"number":1, "name":"الفاتحة", "ayahs":7}, {"number":2, "name":"البقرة", "ayahs":286},
    {"number":3, "name":"آل عمران", "ayahs":200}, {"number":4, "name":"النساء", "ayahs":176},
    {"number":5, "name":"المائدة", "ayahs":120}, {"number":6, "name":"الأنعام", "ayahs":165},
    {"number":7, "name":"الأعراف", "ayahs":206}, {"number":8, "name":"الأنفال", "ayahs":75},
    {"number":9, "name":"التوبة", "ayahs":129}, {"number":10, "name":"يونس", "ayahs":109},
    {"number":11, "name":"هود", "ayahs":123}, {"number":12, "name":"يوسف", "ayahs":111},
    {"number":13, "name":"الرعد", "ayahs":43}, {"number":14, "name":"إبراهيم", "ayahs":52},
    {"number":15, "name":"الحجر", "ayahs":99}, {"number":16, "name":"النحل", "ayahs":128},
    {"number":17, "name":"الإسراء", "ayahs":111}, {"number":18, "name":"الكهف", "ayahs":110},
    {"number":19, "name":"مريم", "ayahs":98}, {"number":20, "name":"طه", "ayahs":135},
    {"number":21, "name":"الأنبياء", "ayahs":112}, {"number":22, "name":"الحج", "ayahs":78},
    {"number":23, "name":"المؤمنون", "ayahs":118}, {"number":24, "name":"النور", "ayahs":64},
    {"number":25, "name":"الفرقان", "ayahs":77}, {"number":26, "name":"الشعراء", "ayahs":227},
    {"number":27, "name":"النمل", "ayahs":93}, {"number":28, "name":"القصص", "ayahs":88},
    {"number":29, "name":"العنكبوت", "ayahs":69}, {"number":30, "name":"الروم", "ayahs":60},
    {"number":31, "name":"لقمان", "ayahs":34}, {"number":32, "name":"السجدة", "ayahs":30},
    {"number":33, "name":"الأحزاب", "ayahs":73}, {"number":34, "name":"سبأ", "ayahs":54},
    {"number":35, "name":"فاطر", "ayahs":45}, {"number":36, "name":"يس", "ayahs":83},
    {"number":37, "name":"الصافات", "ayahs":182}, {"number":38, "name":"ص", "ayahs":88},
    {"number":39, "name":"الزمر", "ayahs":75}, {"number":40, "name":"غافر", "ayahs":85},
    {"number":41, "name":"فصلت", "ayahs":54}, {"number":42, "name":"الشورى", "ayahs":53},
    {"number":43, "name":"الزخرف", "ayahs":89}, {"number":44, "name":"الدخان", "ayahs":59},
    {"number":45, "name":"الجاثية", "ayahs":37}, {"number":46, "name":"الأحقاف", "ayahs":35},
    {"number":47, "name":"محمد", "ayahs":38}, {"number":48, "name":"الفتح", "ayahs":29},
    {"number":49, "name":"الحجرات", "ayahs":18}, {"number":50, "name":"ق", "ayahs":45},
    {"number":51, "name":"الذاريات", "ayahs":60}, {"number":52, "name":"الطور", "ayahs":49},
    {"number":53, "name":"النجم", "ayahs":62}, {"number":54, "name":"القمر", "ayahs":55},
    {"number":55, "name":"الرحمن", "ayahs":78}, {"number":56, "name":"الواقعة", "ayahs":96},
    {"number":57, "name":"الحديد", "ayahs":29}, {"number":58, "name":"المجادلة", "ayahs":22},
    {"number":59, "name":"الحشر", "ayahs":24}, {"number":60, "name":"الممتحنة", "ayahs":13},
    {"number":61, "name":"الصف", "ayahs":14}, {"number":62, "name":"الجمعة", "ayahs":11},
    {"number":63, "name":"المنافقون", "ayahs":11}, {"number":64, "name":"التغابن", "ayahs":18},
    {"number":65, "name":"الطلاق", "ayahs":12}, {"number":66, "name":"التحريم", "ayahs":12},
    {"number":67, "name":"الملك", "ayahs":30}, {"number":68, "name":"القلم", "ayahs":52},
    {"number":69, "name":"الحاقة", "ayahs":52}, {"number":70, "name":"المعارج", "ayahs":44},
    {"number":71, "name":"نوح", "ayahs":28}, {"number":72, "name":"الجن", "ayahs":28},
    {"number":73, "name":"المزمل", "ayahs":20}, {"number":74, "name":"المدثر", "ayahs":56},
    {"number":75, "name":"القيامة", "ayahs":40}, {"number":76, "name":"الإنسان", "ayahs":31},
    {"number":77, "name":"المرسلات", "ayahs":50}, {"number":78, "name":"النبأ", "ayahs":40},
    {"number":79, "name":"النازعات", "ayahs":46}, {"number":80, "name":"عبس", "ayahs":42},
    {"number":81, "name":"التكوير", "ayahs":29}, {"number":82, "name":"الانفطار", "ayahs":19},
    {"number":83, "name":"المطففين", "ayahs":36}, {"number":84, "name":"الانشقاق", "ayahs":25},
    {"number":85, "name":"البروج", "ayahs":22}, {"number":86, "name":"الطارق", "ayahs":17},
    {"number":87, "name":"الأعلى", "ayahs":19}, {"number":88, "name":"الغاشية", "ayahs":26},
    {"number":89, "name":"الفجر", "ayahs":30}, {"number":90, "name":"البلد", "ayahs":20},
    {"number":91, "name":"الشمس", "ayahs":15}, {"number":92, "name":"الليل", "ayahs":21},
    {"number":93, "name":"الضحى", "ayahs":11}, {"number":94, "name":"الشرح", "ayahs":8},
    {"number":95, "name":"التين", "ayahs":8}, {"number":96, "name":"العلق", "ayahs":19},
    {"number":97, "name":"القدر", "ayahs":5}, {"number":98, "name":"البينة", "ayahs":8},
    {"number":99, "name":"الزلزلة", "ayahs":8}, {"number":100, "name":"العاديات", "ayahs":11},
    {"number":101, "name":"القارعة", "ayahs":11}, {"number":102, "name":"التكاثر", "ayahs":8},
    {"number":103, "name":"العصر", "ayahs":3}, {"number":104, "name":"الهمزة", "ayahs":9},
    {"number":105, "name":"الفيل", "ayahs":5}, {"number":106, "name":"قريش", "ayahs":4},
    {"number":107, "name":"الماعون", "ayahs":7}, {"number":108, "name":"الكوثر", "ayahs":3},
    {"number":109, "name":"الكافرون", "ayahs":6}, {"number":110, "name":"النصر", "ayahs":3},
    {"number":111, "name":"المسد", "ayahs":5}, {"number":112, "name":"الإخلاص", "ayahs":4},
    {"number":113, "name":"الفلق", "ayahs":5}, {"number":114, "name":"الناس", "ayahs":6}
]

# خريطة السور إلى أرقام الصفحات
SURAH_PAGE_MAP = [
    {"n":1, "name":"الفاتحة", "type":"مكية", "juz":1, "ayahs":7, "startPage":1},
    {"n":2, "name":"البقرة", "type":"مدنية", "juz":1, "ayahs":286, "startPage":2},
    {"n":3, "name":"آل عمران", "type":"مدنية", "juz":3, "ayahs":200, "startPage":50},
    {"n":4, "name":"النساء", "type":"مدنية", "juz":4, "ayahs":176, "startPage":77},
    {"n":5, "name":"المائدة", "type":"مدنية", "juz":6, "ayahs":120, "startPage":106},
    {"n":6, "name":"الأنعام", "type":"مكية", "juz":7, "ayahs":165, "startPage":128},
    {"n":7, "name":"الأعراف", "type":"مكية", "juz":8, "ayahs":206, "startPage":151},
    {"n":8, "name":"الأنفال", "type":"مدنية", "juz":9, "ayahs":75, "startPage":177},
    {"n":9, "name":"التوبة", "type":"مدنية", "juz":10, "ayahs":129, "startPage":187},
    {"n":10, "name":"يونس", "type":"مكية", "juz":11, "ayahs":109, "startPage":208},
    {"n":11, "name":"هود", "type":"مكية", "juz":11, "ayahs":123, "startPage":221},
    {"n":12, "name":"يوسف", "type":"مكية", "juz":12, "ayahs":111, "startPage":235},
    {"n":13, "name":"الرعد", "type":"مدنية", "juz":13, "ayahs":43, "startPage":249},
    {"n":14, "name":"إبراهيم", "type":"مكية", "juz":13, "ayahs":52, "startPage":255},
    {"n":15, "name":"الحجر", "type":"مكية", "juz":14, "ayahs":99, "startPage":262},
    {"n":16, "name":"النحل", "type":"مكية", "juz":14, "ayahs":128, "startPage":267},
    {"n":17, "name":"الإسراء", "type":"مكية", "juz":15, "ayahs":111, "startPage":282},
    {"n":18, "name":"الكهف", "type":"مكية", "juz":15, "ayahs":110, "startPage":293},
    {"n":19, "name":"مريم", "type":"مكية", "juz":16, "ayahs":98, "startPage":305},
    {"n":20, "name":"طه", "type":"مكية", "juz":16, "ayahs":135, "startPage":312},
    {"n":21, "name":"الأنبياء", "type":"مكية", "juz":17, "ayahs":112, "startPage":322},
    {"n":22, "name":"الحج", "type":"مدنية", "juz":17, "ayahs":78, "startPage":332},
    {"n":23, "name":"المؤمنون", "type":"مكية", "juz":18, "ayahs":118, "startPage":342},
    {"n":24, "name":"النور", "type":"مدنية", "juz":18, "ayahs":64, "startPage":350},
    {"n":25, "name":"الفرقان", "type":"مكية", "juz":18, "ayahs":77, "startPage":359},
    {"n":26, "name":"الشعراء", "type":"مكية", "juz":19, "ayahs":227, "startPage":367},
    {"n":27, "name":"النمل", "type":"مكية", "juz":19, "ayahs":93, "startPage":377},
    {"n":28, "name":"القصص", "type":"مكية", "juz":20, "ayahs":88, "startPage":385},
    {"n":29, "name":"العنكبوت", "type":"مكية", "juz":20, "ayahs":69, "startPage":396},
    {"n":30, "name":"الروم", "type":"مكية", "juz":21, "ayahs":60, "startPage":404},
    {"n":31, "name":"لقمان", "type":"مكية", "juz":21, "ayahs":34, "startPage":411},
    {"n":32, "name":"السجدة", "type":"مكية", "juz":21, "ayahs":30, "startPage":415},
    {"n":33, "name":"الأحزاب", "type":"مدنية", "juz":21, "ayahs":73, "startPage":418},
    {"n":34, "name":"سبأ", "type":"مكية", "juz":22, "ayahs":54, "startPage":428},
    {"n":35, "name":"فاطر", "type":"مكية", "juz":22, "ayahs":45, "startPage":434},
    {"n":36, "name":"يس", "type":"مكية", "juz":22, "ayahs":83, "startPage":440},
    {"n":37, "name":"الصافات", "type":"مكية", "juz":23, "ayahs":182, "startPage":446},
    {"n":38, "name":"ص", "type":"مكية", "juz":23, "ayahs":88, "startPage":453},
    {"n":39, "name":"الزمر", "type":"مكية", "juz":23, "ayahs":75, "startPage":458},
    {"n":40, "name":"غافر", "type":"مكية", "juz":24, "ayahs":85, "startPage":467},
    {"n":41, "name":"فصلت", "type":"مكية", "juz":24, "ayahs":54, "startPage":477},
    {"n":42, "name":"الشورى", "type":"مكية", "juz":25, "ayahs":53, "startPage":483},
    {"n":43, "name":"الزخرف", "type":"مكية", "juz":25, "ayahs":89, "startPage":489},
    {"n":44, "name":"الدخان", "type":"مكية", "juz":25, "ayahs":59, "startPage":496},
    {"n":45, "name":"الجاثية", "type":"مكية", "juz":25, "ayahs":37, "startPage":499},
    {"n":46, "name":"الأحقاف", "type":"مكية", "juz":26, "ayahs":35, "startPage":502},
    {"n":47, "name":"محمد", "type":"مدنية", "juz":26, "ayahs":38, "startPage":507},
    {"n":48, "name":"الفتح", "type":"مدنية", "juz":26, "ayahs":29, "startPage":511},
    {"n":49, "name":"الحجرات", "type":"مدنية", "juz":26, "ayahs":18, "startPage":515},
    {"n":50, "name":"ق", "type":"مكية", "juz":26, "ayahs":45, "startPage":518},
    {"n":51, "name":"الذاريات", "type":"مكية", "juz":26, "ayahs":60, "startPage":520},
    {"n":52, "name":"الطور", "type":"مكية", "juz":27, "ayahs":49, "startPage":523},
    {"n":53, "name":"النجم", "type":"مكية", "juz":27, "ayahs":62, "startPage":526},
    {"n":54, "name":"القمر", "type":"مكية", "juz":27, "ayahs":55, "startPage":528},
    {"n":55, "name":"الرحمن", "type":"مدنية", "juz":27, "ayahs":78, "startPage":531},
    {"n":56, "name":"الواقعة", "type":"مكية", "juz":27, "ayahs":96, "startPage":534},
    {"n":57, "name":"الحديد", "type":"مدنية", "juz":27, "ayahs":29, "startPage":537},
    {"n":58, "name":"المجادلة", "type":"مدنية", "juz":28, "ayahs":22, "startPage":542},
    {"n":59, "name":"الحشر", "type":"مدنية", "juz":28, "ayahs":24, "startPage":545},
    {"n":60, "name":"الممتحنة", "type":"مدنية", "juz":28, "ayahs":13, "startPage":549},
    {"n":61, "name":"الصف", "type":"مدنية", "juz":28, "ayahs":14, "startPage":551},
    {"n":62, "name":"الجمعة", "type":"مدنية", "juz":28, "ayahs":11, "startPage":553},
    {"n":63, "name":"المنافقون", "type":"مدنية", "juz":28, "ayahs":11, "startPage":554},
    {"n":64, "name":"التغابن", "type":"مدنية", "juz":28, "ayahs":18, "startPage":556},
    {"n":65, "name":"الطلاق", "type":"مدنية", "juz":28, "ayahs":12, "startPage":558},
    {"n":66, "name":"التحريم", "type":"مدنية", "juz":28, "ayahs":12, "startPage":560},
    {"n":67, "name":"الملك", "type":"مكية", "juz":29, "ayahs":30, "startPage":562},
    {"n":68, "name":"القلم", "type":"مكية", "juz":29, "ayahs":52, "startPage":564},
    {"n":69, "name":"الحاقة", "type":"مكية", "juz":29, "ayahs":52, "startPage":566},
    {"n":70, "name":"المعارج", "type":"مكية", "juz":29, "ayahs":44, "startPage":568},
    {"n":71, "name":"نوح", "type":"مكية", "juz":29, "ayahs":28, "startPage":570},
    {"n":72, "name":"الجن", "type":"مكية", "juz":29, "ayahs":28, "startPage":572},
    {"n":73, "name":"المزمل", "type":"مكية", "juz":29, "ayahs":20, "startPage":574},
    {"n":74, "name":"المدثر", "type":"مكية", "juz":29, "ayahs":56, "startPage":575},
    {"n":75, "name":"القيامة", "type":"مكية", "juz":29, "ayahs":40, "startPage":577},
    {"n":76, "name":"الإنسان", "type":"مدنية", "juz":29, "ayahs":31, "startPage":578},
    {"n":77, "name":"المرسلات", "type":"مكية", "juz":29, "ayahs":50, "startPage":580},
    {"n":78, "name":"النبأ", "type":"مكية", "juz":30, "ayahs":40, "startPage":582},
    {"n":79, "name":"النازعات", "type":"مكية", "juz":30, "ayahs":46, "startPage":583},
    {"n":80, "name":"عبس", "type":"مكية", "juz":30, "ayahs":42, "startPage":585},
    {"n":81, "name":"التكوير", "type":"مكية", "juz":30, "ayahs":29, "startPage":586},
    {"n":82, "name":"الانفطار", "type":"مكية", "juz":30, "ayahs":19, "startPage":587},
    {"n":83, "name":"المطففين", "type":"مكية", "juz":30, "ayahs":36, "startPage":587},
    {"n":84, "name":"الانشقاق", "type":"مكية", "juz":30, "ayahs":25, "startPage":589},
    {"n":85, "name":"البروج", "type":"مكية", "juz":30, "ayahs":22, "startPage":590},
    {"n":86, "name":"الطارق", "type":"مكية", "juz":30, "ayahs":17, "startPage":591},
    {"n":87, "name":"الأعلى", "type":"مكية", "juz":30, "ayahs":19, "startPage":591},
    {"n":88, "name":"الغاشية", "type":"مكية", "juz":30, "ayahs":26, "startPage":592},
    {"n":89, "name":"الفجر", "type":"مكية", "juz":30, "ayahs":30, "startPage":593},
    {"n":90, "name":"البلد", "type":"مكية", "juz":30, "ayahs":20, "startPage":594},
    {"n":91, "name":"الشمس", "type":"مكية", "juz":30, "ayahs":15, "startPage":595},
    {"n":92, "name":"الليل", "type":"مكية", "juz":30, "ayahs":21, "startPage":595},
    {"n":93, "name":"الضحى", "type":"مكية", "juz":30, "ayahs":11, "startPage":596},
    {"n":94, "name":"الشرح", "type":"مكية", "juz":30, "ayahs":8, "startPage":596},
    {"n":95, "name":"التين", "type":"مكية", "juz":30, "ayahs":8, "startPage":597},
    {"n":96, "name":"العلق", "type":"مكية", "juz":30, "ayahs":19, "startPage":597},
    {"n":97, "name":"القدر", "type":"مكية", "juz":30, "ayahs":5, "startPage":598},
    {"n":98, "name":"البينة", "type":"مدنية", "juz":30, "ayahs":8, "startPage":598},
    {"n":99, "name":"الزلزلة", "type":"مدنية", "juz":30, "ayahs":8, "startPage":599},
    {"n":100, "name":"العاديات", "type":"مكية", "juz":30, "ayahs":11, "startPage":599},
    {"n":101, "name":"القارعة", "type":"مكية", "juz":30, "ayahs":11, "startPage":600},
    {"n":102, "name":"التكاثر", "type":"مكية", "juz":30, "ayahs":8, "startPage":600},
    {"n":103, "name":"العصر", "type":"مكية", "juz":30, "ayahs":3, "startPage":601},
    {"n":104, "name":"الهمزة", "type":"مكية", "juz":30, "ayahs":9, "startPage":601},
    {"n":105, "name":"الفيل", "type":"مكية", "juz":30, "ayahs":5, "startPage":601},
    {"n":106, "name":"قريش", "type":"مكية", "juz":30, "ayahs":4, "startPage":602},
    {"n":107, "name":"الماعون", "type":"مكية", "juz":30, "ayahs":7, "startPage":602},
    {"n":108, "name":"الكوثر", "type":"مكية", "juz":30, "ayahs":3, "startPage":602},
    {"n":109, "name":"الكافرون", "type":"مكية", "juz":30, "ayahs":6, "startPage":603},
    {"n":110, "name":"النصر", "type":"مدنية", "juz":30, "ayahs":3, "startPage":603},
    {"n":111, "name":"المسد", "type":"مكية", "juz":30, "ayahs":5, "startPage":603},
    {"n":112, "name":"الإخلاص", "type":"مكية", "juz":30, "ayahs":4, "startPage":604},
    {"n":113, "name":"الفلق", "type":"مكية", "juz":30, "ayahs":5, "startPage":604},
    {"n":114, "name":"الناس", "type":"مكية", "juz":30, "ayahs":6, "startPage":604}
]

# =====================================================
#  القالب الرئيسي (HTML + CSS + JavaScript)
# =====================================================

TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>رمضان - موقع إسلامي شامل (نسخة بايثون)</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&family=Scheherazade+New:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
    <style>
        /* =====================================================
           رمضان - موقع إسلامي | النمط العام (مدمج)
           ===================================================== */

        :root {
            --primary: #1a6b3c;
            --primary-dark: #0f4726;
            --primary-light: #28a060;
            --gold: #c9a84c;
            --gold-light: #e8c97a;
            --gold-dark: #9a7a2c;
            --accent: #d4af37;

            --bg: #f4f0e8;
            --bg2: #ede7d9;
            --bg3: #e4dcc9;
            --surface: #ffffff;
            --surface2: #f9f5ed;
            --surface3: #f0ead8;
            --border: rgba(180,150,80,0.2);
            --border2: rgba(180,150,80,0.4);

            --text: #1a1208;
            --text2: #4a3a1a;
            --text3: #7a6a4a;
            --text-inv: #ffffff;

            --shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
            --shadow-md: 0 6px 24px rgba(0,0,0,0.1);
            --shadow-lg: 0 12px 40px rgba(0,0,0,0.14);
            --shadow-gold: 0 4px 20px rgba(201,168,76,0.25);

            --radius-sm: 10px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-xl: 32px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

            --header-h: 64px;
        }

        .dark-theme {
            --bg: #0d1117;
            --bg2: #111820;
            --bg3: #161e2a;
            --surface: #1a2332;
            --surface2: #1f2b3d;
            --surface3: #243040;
            --border: rgba(201,168,76,0.15);
            --border2: rgba(201,168,76,0.3);

            --text: #f0e8d0;
            --text2: #c8b890;
            --text3: #8a7a5a;
            --text-inv: #0d1117;

            --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
            --shadow-md: 0 6px 24px rgba(0,0,0,0.4);
            --shadow-lg: 0 12px 40px rgba(0,0,0,0.5);
            --shadow-gold: 0 4px 20px rgba(201,168,76,0.15);
        }

        *, *::before, *::after {
            margin: 0; padding: 0;
            box-sizing: border-box;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'Tajawal', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            transition: background 0.4s ease, color 0.4s ease;
            overflow-x: hidden;
        }

        /* الشريط العلوي */
        .header {
            position: sticky;
            top: 0;
            z-index: 1000;
            height: var(--header-h);
            background: var(--primary-dark);
            border-bottom: 2px solid var(--gold-dark);
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }

        .dark-theme .header {
            background: #080e16;
        }

        .header-inner {
            max-width: 1200px;
            margin: 0 auto;
            height: 100%;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon-wrap {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--gold), var(--gold-dark));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 12px rgba(201,168,76,0.4);
        }

        .logo-icon-wrap i {
            font-size: 1.4rem;
            color: #fff;
        }

        .logo-text {
            font-family: 'Scheherazade New', serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--gold-light);
            text-shadow: 0 2px 8px rgba(0,0,0,0.4);
            letter-spacing: 1px;
        }

        /* زر تبديل المظهر */
        .theme-toggle {
            position: relative;
            width: 64px;
            height: 34px;
            background: none;
            border: 2px solid var(--gold-dark);
            border-radius: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            padding: 0 4px;
            overflow: hidden;
            transition: var(--transition);
        }

        .theme-toggle:hover {
            border-color: var(--gold-light);
            box-shadow: 0 0 12px rgba(201,168,76,0.4);
        }

        .toggle-track {
            position: absolute;
            width: 26px;
            height: 26px;
            background: linear-gradient(135deg, var(--gold), var(--gold-dark));
            border-radius: 50%;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            right: 4px;
        }

        .dark-theme .toggle-track {
            transform: translateX(-30px);
        }

        .theme-icon {
            position: absolute;
            font-size: 0.8rem;
            transition: var(--transition);
            z-index: 1;
        }

        .light-icon { right: 8px; color: var(--gold-light); }
        .dark-icon  { left: 8px; color: #9ab3c8; }

        .dark-theme .light-icon { opacity: 0.4; }
        .light-theme .dark-icon { opacity: 0.4; }

        /* المحتوى الرئيسي والشاشات */
        .main-content {
            flex: 1;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 0 16px 120px;
        }

        .screen {
            display: none;
            animation: screenFadeIn 0.4s ease;
        }

        .screen.active {
            display: block;
        }

        @keyframes screenFadeIn {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* الشاشة الرئيسية - Hero */
        .hero-section {
            position: relative;
            overflow: hidden;
            border-radius: var(--radius-xl);
            margin: 24px 0 20px;
            background: linear-gradient(135deg, var(--primary-dark) 0%, #1a4a2e 50%, var(--primary) 100%);
            padding: 48px 32px;
            text-align: center;
        }

        .hero-decor {
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 20% 50%, rgba(201,168,76,0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 50%, rgba(201,168,76,0.08) 0%, transparent 50%);
            pointer-events: none;
        }

        .hero-decor::before, .hero-decor::after {
            content: '';
            position: absolute;
            border: 1px solid rgba(201,168,76,0.15);
            border-radius: 50%;
        }
        .hero-decor::before {
            width: 300px; height: 300px;
            top: -100px; right: -80px;
        }
        .hero-decor::after {
            width: 200px; height: 200px;
            bottom: -80px; left: -60px;
        }

        .bismillah {
            font-family: 'Scheherazade New', serif;
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            color: var(--gold-light);
            margin-bottom: 12px;
            opacity: 0.9;
            letter-spacing: 2px;
        }

        .hero-title {
            font-family: 'Scheherazade New', serif;
            font-size: clamp(1.8rem, 5vw, 3rem);
            color: #fff;
            margin-bottom: 12px;
            font-weight: 700;
            line-height: 1.3;
        }

        .hero-title span {
            color: var(--gold-light);
            text-shadow: 0 0 20px rgba(201,168,76,0.5);
        }

        .hero-subtitle {
            font-size: clamp(0.9rem, 2vw, 1.1rem);
            color: rgba(255,255,255,0.75);
            max-width: 500px;
            margin: 0 auto;
        }

        /* مشغل مدمج في الرئيسية */
        .home-player-wrap {
            margin-bottom: 16px;
        }

        .home-player-card {
            background: var(--surface);
            border: 1px solid var(--gold-dark);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            box-shadow: var(--shadow-gold);
            animation: screenFadeIn 0.3s ease;
        }

        .home-player-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
            min-width: 200px;
        }

        .player-now-icon {
            width: 44px; height: 44px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: var(--gold-light);
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        .player-now-text {
            display: flex; flex-direction: column; gap: 2px;
        }

        .player-now-text span {
            font-weight: 700;
            color: var(--text);
            font-size: 0.95rem;
        }

        .player-now-text small {
            color: var(--text3);
            font-size: 0.82rem;
        }

        .home-player-controls {
            flex: 1;
            min-width: 240px;
        }

        .home-player-controls audio {
            width: 100%;
            height: 36px;
            accent-color: var(--primary);
        }

        .home-player-close {
            background: none;
            border: 1px solid var(--border2);
            color: var(--text3);
            width: 32px; height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            transition: var(--transition);
            flex-shrink: 0;
        }

        .home-player-close:hover {
            background: rgba(220,50,50,0.1);
            border-color: #dc3232;
            color: #dc3232;
        }

        /* شبكة الأزرار الرئيسية */
        .main-buttons-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
            margin-bottom: 20px;
        }

        .main-card-btn {
            position: relative;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 22px 18px;
            cursor: pointer;
            text-align: right;
            display: flex;
            flex-direction: column;
            gap: 6px;
            transition: var(--transition);
            overflow: hidden;
            min-height: 120px;
            box-shadow: var(--shadow-sm);
        }

        .main-card-btn::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent 60%, rgba(201,168,76,0.06));
            pointer-events: none;
        }

        .main-card-btn:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
            border-color: var(--gold-dark);
        }

        .main-card-btn:active {
            transform: translateY(0);
        }

        .main-card-icon {
            width: 48px; height: 48px;
            border-radius: var(--radius-sm);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.4rem;
            margin-bottom: 4px;
            flex-shrink: 0;
        }

        .quran-icon  { background: rgba(26,107,60,0.12); color: var(--primary); }
        .hadith-icon { background: rgba(201,168,76,0.12); color: var(--gold-dark); }
        .radio-icon  { background: rgba(80,120,200,0.12); color: #4a7fc8; }
        .prayer-icon { background: rgba(180,80,80,0.12);  color: #b85050; }
        .azkar-icon  { background: rgba(120,80,200,0.12); color: #7850c8; }

        .main-card-label {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
        }

        .main-card-sub {
            font-size: 0.82rem;
            color: var(--text3);
        }

        .card-arrow {
            position: absolute;
            bottom: 16px;
            left: 18px;
            color: var(--border2);
            font-size: 0.9rem;
            transition: var(--transition);
        }

        .main-card-btn:hover .card-arrow {
            color: var(--gold-dark);
            transform: translateX(-4px);
        }

        /* زر خامس يأخذ عرض الشبكة كاملاً */
        .main-buttons-grid .main-card-btn:nth-child(5) {
            grid-column: 1 / -1;
            flex-direction: row;
            align-items: center;
            min-height: 80px;
            padding: 18px 22px;
        }

        .main-buttons-grid .main-card-btn:nth-child(5) .main-card-icon {
            margin-bottom: 0;
            margin-left: 16px;
        }

        /* آية اليوم */
        .verse-of-day {
            background: linear-gradient(135deg, var(--primary-dark), #1a4a2e);
            border-radius: var(--radius-lg);
            padding: 28px 24px;
            text-align: center;
            border: 1px solid rgba(201,168,76,0.2);
            margin-bottom: 16px;
        }

        .vod-label {
            font-size: 0.85rem;
            color: var(--gold-light);
            margin-bottom: 14px;
            display: flex; align-items: center; justify-content: center; gap: 6px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .vod-text {
            font-family: 'Scheherazade New', serif;
            font-size: clamp(1.2rem, 3.5vw, 1.7rem);
            color: #fff;
            line-height: 2;
            margin-bottom: 12px;
        }

        .vod-ref {
            font-size: 0.88rem;
            color: rgba(255,255,255,0.5);
        }

        /* رأس الشاشات الداخلية */
        .screen-header {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 20px 0 16px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 20px;
        }

        .back-btn {
            width: 40px; height: 40px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            color: var(--text2);
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 1rem;
            transition: var(--transition);
            flex-shrink: 0;
        }

        .back-btn:hover {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }

        .screen-title {
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            font-weight: 700;
            color: var(--text);
            display: flex; align-items: center; gap: 10px;
        }

        .screen-title i { color: var(--primary); }

        /* تبويبات القرآن */
        .quran-tabs {}

        .qtab-buttons {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .qtab-buttons::-webkit-scrollbar { height: 3px; }
        .qtab-buttons::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

        .qtab-btn {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 50px;
            padding: 10px 22px;
            color: var(--text2);
            font-family: 'Tajawal', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            display: flex; align-items: center; gap: 8px;
            transition: var(--transition);
        }

        .qtab-btn:hover {
            border-color: var(--primary-light);
            color: var(--primary);
        }

        .qtab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
        }

        .qtab-content { display: none; }
        .qtab-content.active { display: block; animation: screenFadeIn 0.3s ease; }

        /* مربع البحث */
        .search-box {
            position: relative;
            margin-bottom: 20px;
            max-width: 420px;
        }

        .search-box i {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text3);
            font-size: 0.9rem;
        }

        .search-box input {
            width: 100%;
            padding: 12px 40px 12px 16px;
            background: var(--surface2);
            border: 1px solid var(--border2);
            border-radius: 50px;
            font-family: 'Tajawal', sans-serif;
            font-size: 0.95rem;
            color: var(--text);
            transition: var(--transition);
            outline: none;
        }

        .search-box input:focus {
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px rgba(26,107,60,0.1);
        }

        .dark-theme .search-box input { background: var(--surface3); }

        /* شبكة البطاقات العامة */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 14px;
        }

        /* بطاقة القارئ */
        .reciter-card, .riwayah-card, .tafsir-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 20px 16px;
            cursor: pointer;
            text-align: center;
            transition: var(--transition);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            box-shadow: var(--shadow-sm);
        }

        .reciter-card:hover, .riwayah-card:hover, .tafsir-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-light);
        }

        .reciter-icon, .riwayah-icon, .tafsir-icon {
            width: 56px; height: 56px;
            border-radius: 50%;
            background: rgba(26,107,60,0.1);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem;
            color: var(--primary);
            border: 2px solid rgba(26,107,60,0.15);
        }

        .reciter-info h4, .riwayah-info h4, .tafsir-info h4 {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 4px;
            line-height: 1.4;
        }

        .reciter-info p, .riwayah-info p, .tafsir-info p {
            font-size: 0.82rem;
            color: var(--text3);
        }

        /* نظام الصفحات */
        .pagination-controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin-top: 24px;
            padding: 16px;
            background: var(--surface2);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
        }

        .pagination-info {
            font-size: 0.9rem;
            color: var(--text3);
            font-weight: 600;
            white-space: nowrap;
        }

        .page-btn {
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-family: 'Tajawal', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex; align-items: center; gap: 6px;
            transition: var(--transition);
        }

        .page-btn:hover:not(:disabled) {
            background: var(--primary-light);
            transform: translateY(-1px);
        }

        .page-btn:disabled {
            background: var(--border2);
            cursor: not-allowed;
            opacity: 0.6;
        }

        /* قسم السور */
        .suras-section {
            margin-top: 20px;
            animation: screenFadeIn 0.4s ease;
        }

        .section-subheader {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 20px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border);
        }

        .section-subheader h3 {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text);
            display: flex; align-items: center; gap: 8px;
        }

        .section-subheader h3 i { color: var(--primary); }

        .back-sub-btn {
            background: var(--surface2);
            border: 1px solid var(--border2);
            color: var(--text2);
            padding: 8px 16px;
            border-radius: 50px;
            font-family: 'Tajawal', sans-serif;
            font-size: 0.88rem;
            cursor: pointer;
            display: flex; align-items: center; gap: 6px;
            transition: var(--transition);
            white-space: nowrap;
        }

        .back-sub-btn:hover {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }

        .suras-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 10px;
        }

        .sura-item {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px 10px;
            cursor: pointer;
            text-align: center;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }

        .sura-item:hover {
            background: var(--primary);
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .sura-item:hover .sura-number,
        .sura-item:hover .sura-name {
            color: #fff;
        }

        .sura-number {
            font-size: 1rem;
            font-weight: 700;
            color: var(--gold-dark);
            margin-bottom: 6px;
        }

        .sura-name {
            font-family: 'Scheherazade New', serif;
            font-size: 1rem;
            color: var(--text);
            line-height: 1.3;
        }

        /* تحكم التفسير */
        .tafsir-controls {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            align-items: flex-end;
            flex-wrap: wrap;
        }

        .tafsir-result {
            background: var(--surface);
            border-radius: var(--radius-md);
            padding: 24px;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
            max-height: 500px;
            overflow-y: auto;
        }

        .tafsir-verse {
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
        }

        .tafsir-verse:last-child { border-bottom: none; }

        .verse-header-tafsir { margin-bottom: 12px; }

        .verse-number-tafsir {
            background: var(--primary);
            color: #fff;
            padding: 4px 14px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }

        .verse-arabic-tafsir {
            font-family: 'Scheherazade New', serif;
            font-size: 1.7rem;
            line-height: 2.2;
            color: var(--primary-dark);
            text-align: right;
            margin: 12px 0;
        }

        .dark-theme .verse-arabic-tafsir { color: var(--gold-light); }

        .verse-tafsir-text {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text2);
            padding-right: 14px;
            border-right: 3px solid var(--gold);
        }

        /* قسم الأحاديث */
        .hadith-controls {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-sm);
        }

        .control-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 16px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .control-group label {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text2);
            display: flex; align-items: center; gap: 6px;
        }

        .control-group label i { color: var(--primary); }

        .select-control, .input-control {
            padding: 11px 14px;
            background: var(--surface2);
            border: 1px solid var(--border2);
            border-radius: var(--radius-sm);
            font-family: 'Tajawal', sans-serif;
            font-size: 0.95rem;
            color: var(--text);
            outline: none;
            transition: var(--transition);
            width: 100%;
        }

        .select-control:focus, .input-control:focus {
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px rgba(26,107,60,0.1);
        }

        .dark-theme .select-control,
        .dark-theme .input-control {
            background: var(--surface3);
        }

        .control-buttons {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .btn-primary, .btn-secondary {
            padding: 12px 24px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-family: 'Tajawal', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            display: flex; align-items: center; gap: 8px;
            transition: var(--transition);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
            color: #fff;
            box-shadow: 0 4px 14px rgba(26,107,60,0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(26,107,60,0.4);
        }

        .btn-secondary {
            background: var(--surface2);
            color: var(--text2);
            border: 1px solid var(--border2);
        }

        .btn-secondary:hover {
            background: var(--gold);
            color: #fff;
            border-color: var(--gold);
        }

        /* بطاقة الحديث */
        .hadith-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 28px 24px;
            box-shadow: var(--shadow-sm);
            animation: screenFadeIn 0.4s ease;
        }

        .hadith-book-label {
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--primary);
            background: rgba(26,107,60,0.08);
            padding: 4px 14px;
            border-radius: 50px;
            display: inline-flex; align-items: center; gap: 6px;
            margin-bottom: 16px;
        }

        .hadith-arabic {
            font-family: 'Scheherazade New', serif;
            font-size: clamp(1.3rem, 3vw, 1.8rem);
            color: var(--primary-dark);
            line-height: 2.2;
            text-align: right;
            margin-bottom: 20px;
            padding: 20px;
            background: var(--surface2);
            border-radius: var(--radius-sm);
            border-right: 4px solid var(--gold);
        }

        .dark-theme .hadith-arabic {
            color: var(--gold-light);
            background: var(--surface3);
        }

        .hadith-translation, .hadith-explanation {
            font-size: 1rem;
            color: var(--text2);
            line-height: 1.7;
            padding: 14px 18px;
            background: var(--surface2);
            border-radius: var(--radius-sm);
            border-right: 3px solid var(--gold);
            margin-bottom: 14px;
        }

        .hadith-translation strong, .hadith-explanation strong {
            color: var(--primary);
            display: block;
            margin-bottom: 6px;
        }

        .hadith-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            margin-top: 14px;
        }

        .hadith-meta span {
            font-size: 0.82rem;
            color: var(--text3);
            display: flex; align-items: center; gap: 5px;
        }

        .hadith-meta i { color: var(--gold-dark); }

        /* إذاعات القرآن */
        .radio-search-box {
            margin-bottom: 20px;
        }

        .radio-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 14px;
        }

        .radio-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 20px 16px;
            text-align: center;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .radio-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-light);
        }

        .radio-image {
            width: 80px; height: 80px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid var(--gold-dark);
            box-shadow: 0 2px 12px rgba(201,168,76,0.2);
            background: var(--surface2);
            flex-shrink: 0;
        }

        .radio-image img {
            width: 100%; height: 100%;
            object-fit: cover;
        }

        .radio-no-img {
            width: 80px; height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            display: flex; align-items: center; justify-content: center;
            font-size: 1.8rem;
            color: var(--gold-light);
            border: 3px solid var(--gold-dark);
        }

        .radio-info {
            flex: 1;
            width: 100%;
        }

        .radio-info h4 {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 4px;
            line-height: 1.4;
        }

        .radio-desc, .radio-country {
            font-size: 0.8rem;
            color: var(--text3);
            display: flex; align-items: center; justify-content: center; gap: 5px;
        }

        .play-radio-btn {
            background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-family: 'Tajawal', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            display: flex; align-items: center; justify-content: center; gap: 8px;
            width: 100%;
            transition: var(--transition);
            box-shadow: 0 3px 10px rgba(26,107,60,0.25);
        }

        .play-radio-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 5px 16px rgba(26,107,60,0.4);
        }

        /* مواقيت الصلاة */
        .prayer-search-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: flex-end;
        }

        .prayer-search-bar .control-group {
            flex: 1;
            min-width: 140px;
        }

        .prayer-date-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 20px;
            background: var(--surface2);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 0.9rem;
            color: var(--text2);
            font-weight: 600;
        }

        .prayer-date-bar span {
            display: flex; align-items: center; gap: 8px;
        }

        .prayer-date-bar i { color: var(--gold-dark); }

        .prayer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
        }

        .prayer-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 22px 14px;
            text-align: center;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }

        .prayer-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
        }

        .prayer-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
        }

        .fajr-card::before    { background: linear-gradient(90deg, #2196f3, #64b5f6); }
        .sunrise-card::before { background: linear-gradient(90deg, #ff9800, #ffcc02); }
        .dhuhr-card::before   { background: linear-gradient(90deg, #4caf50, #81c784); }
        .asr-card::before     { background: linear-gradient(90deg, #ff5722, #ff8a65); }
        .maghrib-card::before { background: linear-gradient(90deg, #9c27b0, #ce93d8); }
        .isha-card::before    { background: linear-gradient(90deg, #607d8b, #b0bec5); }

        .prayer-card-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
            color: var(--gold-dark);
        }

        .prayer-name {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
        }

        .prayer-time {
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--primary);
            font-family: 'Tajawal', sans-serif;
            letter-spacing: 1px;
        }

        .dark-theme .prayer-time { color: var(--gold-light); }

        /* الأذكار */
        .azkar-tab-buttons {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 6px;
            margin-bottom: 20px;
        }

        .azkar-tab-buttons::-webkit-scrollbar { height: 3px; }
        .azkar-tab-buttons::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

        .azkar-tab {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 50px;
            padding: 9px 18px;
            color: var(--text2);
            font-family: 'Tajawal', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            display: flex; align-items: center; gap: 7px;
            transition: var(--transition);
        }

        .azkar-tab:hover { border-color: var(--primary-light); color: var(--primary); }

        .azkar-tab.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
        }

        .azkar-list { display: flex; flex-direction: column; gap: 14px; }

        .zekr-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 24px 20px;
            border-right: 4px solid var(--gold);
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
            animation: screenFadeIn 0.4s ease;
        }

        .zekr-card:hover {
            transform: translateX(-3px);
            box-shadow: var(--shadow-md);
            border-right-color: var(--primary);
        }

        .zekr-card .content {
            font-family: 'Scheherazade New', serif;
            font-size: clamp(1.2rem, 3vw, 1.6rem);
            line-height: 2.1;
            color: var(--text);
            text-align: right;
            margin-bottom: 14px;
        }

        .zekr-card .description {
            font-size: 0.88rem;
            color: var(--text3);
            font-style: italic;
            padding-right: 12px;
            border-right: 2px solid var(--border2);
            margin-bottom: 12px;
        }

        .zekr-card .count {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(26,107,60,0.1);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 700;
        }

        .dark-theme .zekr-card .count {
            background: rgba(26,107,60,0.2);
            color: var(--gold-light);
        }

        /* المشغل الثابت السفلي */
        .sticky-player {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 2000;
            background: var(--surface);
            border-top: 2px solid var(--primary);
            box-shadow: 0 -4px 24px rgba(0,0,0,0.2);
            animation: slideUpPlayer 0.3s ease;
        }

        .radio-sticky {
            border-top-color: var(--gold-dark);
        }

        @keyframes slideUpPlayer {
            from { transform: translateY(100%); }
            to   { transform: translateY(0); }
        }

        .sticky-player-inner {
            max-width: 1200px;
            margin: 0 auto;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }

        .sticky-player-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 0 0 auto;
            min-width: 180px;
        }

        .sp-icon {
            width: 42px; height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            display: flex; align-items: center; justify-content: center;
            color: var(--gold-light);
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        .radio-live-dot { background: linear-gradient(135deg, #c0392b, #8e1c10); }

        .sp-text { display: flex; flex-direction: column; gap: 2px; }

        .sp-title {
            font-weight: 700;
            color: var(--text);
            font-size: 0.9rem;
            max-width: 160px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .sp-sub {
            font-size: 0.78rem;
            color: var(--text3);
            display: flex; align-items: center; gap: 5px;
        }

        .live-badge {
            background: #c0392b;
            color: #fff;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            letter-spacing: 1px;
            animation: livePulse 1.5s infinite;
        }

        @keyframes livePulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.6; }
        }

        .sticky-player-audio {
            flex: 1;
            min-width: 200px;
        }

        .sticky-player-audio audio {
            width: 100%;
            height: 38px;
            accent-color: var(--primary);
        }

        .sp-close {
            background: none;
            border: 1px solid var(--border2);
            color: var(--text3);
            width: 34px; height: 34px;
            border-radius: 50%;
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            transition: var(--transition);
            flex-shrink: 0;
        }

        .sp-close:hover {
            background: rgba(220,50,50,0.1);
            border-color: #dc3232;
            color: #dc3232;
        }

        /* مؤشر التحميل */
        .loading-spinner {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 48px;
            text-align: center;
            gap: 16px;
        }

        .loading-spinner.active { display: flex; }

        .spinner {
            width: 48px; height: 48px;
            border: 4px solid var(--border2);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-spinner p {
            color: var(--text3);
            font-size: 1rem;
        }

        /* رسائل الخطأ */
        .error-message {
            background: rgba(220,50,50,0.07);
            border: 1px solid rgba(220,50,50,0.2);
            color: #c0392b;
            padding: 18px 20px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 14px;
            font-size: 0.95rem;
            margin: 12px 0;
        }

        .error-message i { font-size: 1.4rem; }

        /* الفوتر */
        .footer {
            background: var(--primary-dark);
            color: rgba(255,255,255,0.6);
            text-align: center;
            padding: 24px 20px;
            margin-top: auto;
        }

        .dark-theme .footer { background: #06090e; }

        .footer-ayah {
            font-family: 'Scheherazade New', serif;
            font-size: 1.2rem;
            color: var(--gold-light);
            margin-bottom: 8px;
        }

        .footer-copy { font-size: 0.85rem; }

        /* Responsive */
        @media (max-width: 640px) {
            .main-buttons-grid {
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }

            .main-card-btn {
                min-height: 110px;
                padding: 18px 14px;
            }

            .main-card-label { font-size: 0.95rem; }
            .main-card-sub   { font-size: 0.78rem; }

            .cards-grid {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            }

            .suras-grid {
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            }

            .prayer-grid {
                grid-template-columns: repeat(3, 1fr);
            }

            .radio-grid {
                grid-template-columns: 1fr 1fr;
            }

            .sticky-player-inner {
                padding: 8px 12px;
                gap: 10px;
            }

            .sp-title { max-width: 100px; }
            .sticky-player-info { min-width: 140px; }

            .hero-section { padding: 36px 20px; }

            .pagination-controls { gap: 10px; }
            .page-btn { padding: 8px 14px; font-size: 0.85rem; }
        }

        @media (max-width: 400px) {
            .main-buttons-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
            .radio-grid { grid-template-columns: 1fr; }
            .prayer-grid { grid-template-columns: repeat(2, 1fr); }
            .cards-grid { grid-template-columns: 1fr 1fr; }
            .suras-grid { grid-template-columns: repeat(3, 1fr); }
        }

        /* Scrollbar مخصص */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg2); }
        ::-webkit-scrollbar-thumb {
            background: var(--gold-dark);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        /* تحسينات إضافية */
        audio {
            border-radius: 8px;
            outline: none;
        }

        audio::-webkit-media-controls-panel {
            background: var(--surface2);
        }

        ::selection {
            background: rgba(26,107,60,0.2);
            color: var(--primary-dark);
        }

        /* نظام قراءة القرآن الكريم - صور المصحف */
        .qread-toprow {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .qread-stats-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .qstat {
            display: flex;
            align-items: center;
            gap: 6px;
            background: var(--surface2);
            border: 1px solid var(--border);
            padding: 7px 14px;
            border-radius: 50px;
            font-size: 0.85rem;
            color: var(--text2);
            font-weight: 600;
            white-space: nowrap;
        }

        .qstat i { color: var(--primary); }

        .page-jump-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 14px;
            background: linear-gradient(135deg, rgba(26,107,60,0.05), rgba(201,168,76,0.08));
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .dark-theme .page-jump-bar {
            background: linear-gradient(135deg, rgba(26,107,60,0.12), rgba(201,168,76,0.1));
        }

        .page-jump-label {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text2);
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: 'Tajawal', sans-serif;
        }

        .page-jump-label i {
            color: var(--gold-dark);
            font-size: 1.1rem;
        }

        .page-jump-input {
            width: 100px;
            padding: 10px 14px;
            border: 2px solid var(--border2);
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 700;
            text-align: center;
            font-family: 'Tajawal', sans-serif;
            color: var(--text);
            background: var(--surface);
            transition: var(--transition);
            outline: none;
        }

        .page-jump-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(26,107,60,0.1);
        }

        .page-jump-btn {
            padding: 10px 22px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border: none;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'Tajawal', sans-serif;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition);
            box-shadow: 0 3px 12px rgba(26,107,60,0.3);
        }

        .page-jump-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 18px rgba(26,107,60,0.4);
        }

        .page-jump-btn:active {
            transform: translateY(0);
        }

        .page-jump-reader {
            background: linear-gradient(135deg, rgba(26,107,60,0.08), rgba(201,168,76,0.1));
            margin-bottom: 10px;
        }

        .surahs-index-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(165px, 1fr));
            gap: 10px;
        }

        .surah-index-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 12px 10px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }

        .surah-index-card::after {
            content: '';
            position: absolute;
            right: 0; top: 0; bottom: 0;
            width: 3px;
            background: var(--gold);
            opacity: 0;
            transition: var(--transition);
        }

        .surah-index-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--gold-dark);
            background: var(--surface2);
        }

        .surah-index-card:hover::after { opacity: 1; }

        .surah-num-badge {
            min-width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 700;
            flex-shrink: 0;
            font-family: 'Tajawal', sans-serif;
        }

        .surah-index-info { flex: 1; min-width: 0; }

        .surah-index-name {
            font-family: 'Scheherazade New', serif;
            font-size: 1.05rem;
            color: var(--text);
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 2px;
        }

        .surah-index-sub {
            font-size: 0.72rem;
            color: var(--text3);
        }

        .surah-index-ayahs {
            font-size: 0.7rem;
            color: var(--gold-dark);
            font-weight: 700;
            background: rgba(201,168,76,0.1);
            padding: 2px 7px;
            border-radius: 10px;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .reader-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 16px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 14px;
            position: sticky;
            top: calc(var(--header-h) + 8px);
            z-index: 100;
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
        }

        .reader-center-info {
            flex: 1;
            text-align: center;
            min-width: 0;
        }

        .reader-surah-name {
            font-family: 'Scheherazade New', serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--primary);
            display: block;
            line-height: 1.2;
        }

        .dark-theme .reader-surah-name { color: var(--gold-light); }

        .reader-surah-meta {
            font-size: 0.78rem;
            color: var(--text3);
            display: block;
        }

        .reader-page-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            padding: 7px 14px;
            border-radius: 50px;
            font-size: 0.82rem;
            font-weight: 700;
            flex-shrink: 0;
            white-space: nowrap;
        }

        .reader-page-badge i { font-size: 0.8rem; opacity: 0.8; }

        .mushaf-zoom-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .zoom-btn {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            font-weight: 700;
            transition: var(--transition);
            flex-shrink: 0;
        }

        .zoom-btn-minus {
            background: var(--surface2);
            border: 2px solid var(--border2);
            color: var(--text2);
        }

        .zoom-btn-minus:hover { background: #e8e0d0; transform: scale(1.08); }
        .dark-theme .zoom-btn-minus:hover { background: #2a3a4a; }

        .zoom-btn-plus {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            box-shadow: 0 3px 12px rgba(26,107,60,0.35);
        }

        .zoom-btn-plus:hover { transform: scale(1.08); box-shadow: 0 5px 18px rgba(26,107,60,0.45); }

        .zoom-percent {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--primary);
            min-width: 62px;
            text-align: center;
            font-family: 'Tajawal', sans-serif;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 50px;
            padding: 8px 14px;
        }

        .dark-theme .zoom-percent { color: var(--gold-light); }

        .zoom-reset-btn {
            padding: 10px 18px;
            background: none;
            border: 2px solid var(--border2);
            border-radius: 50px;
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text3);
            cursor: pointer;
            font-family: 'Tajawal', sans-serif;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .zoom-reset-btn:hover {
            background: var(--gold);
            color: #fff;
            border-color: var(--gold);
        }

        .quran-ayahs-container {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 8px;
            margin-bottom: 16px;
            box-shadow: var(--shadow-md);
            min-height: 70vh;
            max-height: 85vh;
            overflow-x: auto;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }

        .dark-theme .quran-ayahs-container {
            background: #1a1f2e;
            border-color: rgba(201,168,76,0.2);
        }

        .mushaf-page-wrap {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-width: 100%;
        }

        .mushaf-page-img {
            display: block;
            margin: 0 auto;
            width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 6px 32px rgba(0,0,0,0.18);
            transition: width 0.2s ease;
            user-select: none;
            -webkit-user-drag: none;
        }

        .dark-theme .mushaf-page-img {
            box-shadow: 0 6px 36px rgba(0,0,0,0.55);
            filter: none;
            background: #ffffff;
            padding: 2px;
        }

        .reader-nav-btns {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 16px;
            flex-wrap: wrap;
        }

        .reader-nav-btn {
            background: var(--surface);
            border: 1px solid var(--border2);
            border-radius: 50px;
            padding: 11px 22px;
            color: var(--text2);
            font-family: 'Tajawal', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }

        .reader-nav-btn:hover:not(:disabled) {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .reader-nav-btn:disabled {
            opacity: 0.35;
            cursor: not-allowed;
        }

        .reader-nav-btn.go-to-list {
            background: linear-gradient(135deg, var(--gold), var(--gold-dark));
            color: #fff;
            border-color: var(--gold-dark);
        }

        .reader-nav-btn.go-to-list:hover {
            background: linear-gradient(135deg, var(--gold-dark), #7a5a1c);
        }

        .ayahs-error {
            text-align: center;
            padding: 40px 20px;
            color: var(--text3);
            width: 100%;
        }

        .ayahs-error i {
            font-size: 2.5rem;
            color: #c0392b;
            margin-bottom: 12px;
            display: block;
        }

        .ayahs-error p { margin: 4px 0; }

        @media (max-width: 640px) {
            .surahs-index-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
                gap: 8px;
            }

            .reader-topbar {
                padding: 10px 12px;
                position: relative;
                top: auto;
                gap: 8px;
            }

            .reader-nav-btns { gap: 8px; }
            .reader-nav-btn  { padding: 9px 14px; font-size: 0.82rem; }

            .qread-toprow { flex-direction: column; align-items: flex-start; }
            .qread-stats-row { width: 100%; }

            .mushaf-page-img { max-height: 70vh; }

            .surah-index-card { padding: 10px 8px; gap: 8px; }
            .surah-num-badge  { min-width: 30px; height: 30px; font-size: 0.75rem; }
            .surah-index-name { font-size: 0.95rem; }

            .reader-page-badge { padding: 6px 10px; font-size: 0.78rem; }
        }

        @media (max-width: 400px) {
            .surahs-index-grid { grid-template-columns: 1fr 1fr; }
            .reader-nav-btn { padding: 8px 12px; font-size: 0.8rem; }
        }
    </style>
</head>
<body class="light-theme">

    <!-- الشريط العلوي -->
    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-icon-wrap"><i class="fas fa-mosque"></i></div>
                <span class="logo-text">رمضان</span>
            </div>
            <button class="theme-toggle" id="theme-toggle" title="تبديل المظهر">
                <span class="theme-icon light-icon"><i class="fas fa-sun"></i></span>
                <span class="theme-icon dark-icon"><i class="fas fa-moon"></i></span>
                <span class="toggle-track"></span>
            </button>
        </div>
    </header>

    <main class="main-content">

        <!-- ==================== الشاشة الرئيسية ==================== -->
        <section id="home" class="screen active">
            <div class="hero-section">
                <div class="hero-decor"></div>
                <div class="hero-content">
                    <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
                    <h1 class="hero-title">مرحباً بكم في <span>رمضان</span></h1>
                    <p class="hero-subtitle">موقعكم الإسلامي الشامل للقرآن الكريم والأحاديث والأذكار ومواقيت الصلاة</p>
                </div>
            </div>

            <div class="home-player-wrap" id="home-player-wrap" style="display:none;">
                <div class="home-player-card">
                    <div class="home-player-info">
                        <div class="player-now-icon"><i class="fas fa-music"></i></div>
                        <div class="player-now-text">
                            <span id="home-player-title">—</span>
                            <small id="home-player-subtitle"></small>
                        </div>
                    </div>
                    <div class="home-player-controls">
                        <audio id="main-audio" controls></audio>
                    </div>
                    <button class="home-player-close" id="home-player-close"><i class="fas fa-times"></i></button>
                </div>
            </div>

            <div class="main-buttons-grid">
                <button class="main-card-btn" data-screen="quran">
                    <div class="main-card-icon quran-icon"><i class="fas fa-quran"></i></div>
                    <div class="main-card-label">القرآن الكريم</div>
                    <div class="main-card-sub">قراءة واستماع وتفسير</div>
                    <div class="card-arrow"><i class="fas fa-chevron-left"></i></div>
                </button>
                <button class="main-card-btn" data-screen="hadith">
                    <div class="main-card-icon hadith-icon"><i class="fas fa-book-open"></i></div>
                    <div class="main-card-label">الأحاديث النبوية</div>
                    <div class="main-card-sub">صحيح البخاري ومسلم</div>
                    <div class="card-arrow"><i class="fas fa-chevron-left"></i></div>
                </button>
                <button class="main-card-btn" data-screen="radio">
                    <div class="main-card-icon radio-icon"><i class="fas fa-broadcast-tower"></i></div>
                    <div class="main-card-label">إذاعات القرآن</div>
                    <div class="main-card-sub">بث مباشر من أشهر القراء</div>
                    <div class="card-arrow"><i class="fas fa-chevron-left"></i></div>
                </button>
                <button class="main-card-btn" data-screen="prayer">
                    <div class="main-card-icon prayer-icon"><i class="fas fa-clock"></i></div>
                    <div class="main-card-label">مواقيت الصلاة</div>
                    <div class="main-card-sub">لجميع المدن العربية</div>
                    <div class="card-arrow"><i class="fas fa-chevron-left"></i></div>
                </button>
                <button class="main-card-btn" data-screen="azkar">
                    <div class="main-card-icon azkar-icon"><i class="fas fa-hands-praying"></i></div>
                    <div class="main-card-label">الأذكار اليومية</div>
                    <div class="main-card-sub">أذكار الصباح والمساء</div>
                    <div class="card-arrow"><i class="fas fa-chevron-left"></i></div>
                </button>
            </div>

            <div class="verse-of-day">
                <div class="vod-label"><i class="fas fa-star"></i> آية كريمة</div>
                <div class="vod-text">﴿ وَاذْكُرِ اسْمَ رَبِّكَ وَتَبَتَّلْ إِلَيْهِ تَبْتِيلًا ﴾</div>
                <div class="vod-ref">سورة المزمل - آية 8</div>
            </div>
        </section>

        <!-- ==================== شاشة القرآن الكريم ==================== -->
        <section id="quran" class="screen">
            <div class="screen-header">
                <button class="back-btn" data-back="home"><i class="fas fa-chevron-right"></i></button>
                <h2 class="screen-title"><i class="fas fa-quran"></i> القرآن الكريم</h2>
            </div>

            <div class="quran-tabs">
                <div class="qtab-buttons">
                    <button class="qtab-btn active" data-tab="read-quran"><i class="fas fa-book-reader"></i> قراءة</button>
                    <button class="qtab-btn" data-tab="reciters"><i class="fas fa-microphone"></i> استماع</button>
                    <button class="qtab-btn" data-tab="riwayat"><i class="fas fa-book-open"></i> روايات</button>
                    <button class="qtab-btn" data-tab="tafsir"><i class="fas fa-search"></i> تفسير</button>
                </div>

                <!-- ======== تبويب قراءة القرآن ======== -->
                <div class="qtab-content active" id="read-quran">
                    <!-- قائمة السور -->
                    <div id="quran-surah-selector">
                        <div class="qread-toprow">
                            <div class="search-box">
                                <i class="fas fa-search"></i>
                                <input type="text" id="surah-list-search" placeholder="ابحث عن سورة...">
                            </div>
                            <div class="qread-stats-row">
                                <div class="qstat"><i class="fas fa-list-ol"></i><span>114 سورة</span></div>
                                <div class="qstat"><i class="fas fa-align-justify"></i><span>6236 آية</span></div>
                                <div class="qstat"><i class="fas fa-book"></i><span>30 جزء</span></div>
                            </div>
                        </div>
                        
                        <!-- البحث برقم الصفحة -->
                        <div class="page-jump-bar">
                            <label class="page-jump-label">
                                <i class="fas fa-file-alt"></i>
                                انتقل إلى الصفحة:
                            </label>
                            <input 
                                type="number" 
                                id="page-jump-input" 
                                class="page-jump-input" 
                                min="1" 
                                max="604" 
                                placeholder="1-604"
                            />
                            <button class="page-jump-btn" id="page-jump-btn">
                                <i class="fas fa-arrow-left"></i> انتقال
                            </button>
                        </div>
                        <div class="surahs-index-grid" id="surahs-index-grid"></div>
                    </div>

                    <!-- عارض صور صفحات المصحف -->
                    <div id="quran-reader-view" style="display:none;">
                        <div class="reader-topbar">
                            <button class="back-sub-btn" id="back-to-surah-list">
                                <i class="fas fa-th-list"></i> السور
                            </button>
                            <div class="reader-center-info">
                                <div class="reader-surah-name" id="reader-surah-name">—</div>
                                <div class="reader-surah-meta" id="reader-surah-meta"></div>
                            </div>
                            <div class="reader-page-badge">
                                <i class="fas fa-file-alt"></i>
                                <span id="reader-page-num">صفحة 1 / 604</span>
                            </div>
                        </div>

                        <div class="loading-spinner" id="quran-reader-loading">
                            <div class="spinner"></div>
                            <p>جاري تحميل صفحة المصحف...</p>
                        </div>

                        <!-- شريط التكبير والتصغير -->
                        <div class="mushaf-zoom-bar">
                            <button class="zoom-btn zoom-btn-minus" id="zoom-out-btn" title="تصغير">
                                <i class="fas fa-minus"></i>
                            </button>
                            <span class="zoom-percent" id="zoom-label">100%</span>
                            <button class="zoom-btn zoom-btn-plus" id="zoom-in-btn" title="تكبير">
                                <i class="fas fa-plus"></i>
                            </button>
                            <button class="zoom-reset-btn" id="zoom-reset-btn">
                                <i class="fas fa-expand-arrows-alt"></i> افتراضي
                            </button>
                        </div>

                        <!-- انتقال سريع أثناء القراءة -->
                        <div class="page-jump-bar page-jump-reader">
                            <label class="page-jump-label">
                                <i class="fas fa-file-alt"></i>
                                انتقل إلى صفحة:
                            </label>
                            <input 
                                type="number" 
                                id="page-jump-reader-input" 
                                class="page-jump-input" 
                                min="1" 
                                max="604" 
                                placeholder="1-604"
                            />
                            <button class="page-jump-btn" id="page-jump-reader-btn">
                                <i class="fas fa-arrow-left"></i> انتقال
                            </button>
                        </div>

                        <div class="quran-ayahs-container" id="quran-ayahs-container"></div>

                        <div class="reader-nav-btns">
                            <button class="reader-nav-btn" id="prev-surah-btn">
                                <i class="fas fa-chevron-right"></i> الصفحة السابقة
                            </button>
                            <button class="reader-nav-btn go-to-list" id="surah-list-btn-bottom">
                                <i class="fas fa-th"></i> قائمة السور
                            </button>
                            <button class="reader-nav-btn" id="next-surah-btn">
                                الصفحة التالية <i class="fas fa-chevron-left"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- ======== تبويب القراء ======== -->
                <div class="qtab-content" id="reciters">
                    <div class="search-box">
                        <i class="fas fa-search"></i>
                        <input type="text" id="reciter-search" placeholder="ابحث عن قارئ...">
                    </div>
                    <div class="loading-spinner" id="reciters-loading">
                        <div class="spinner"></div><p>جاري تحميل القراء...</p>
                    </div>
                    <div class="cards-grid" id="reciters-list-container"></div>
                    <div class="pagination-controls" id="reciters-pagination" style="display:none;">
                        <button class="page-btn" id="reciters-prev-btn" disabled><i class="fas fa-chevron-right"></i> السابق</button>
                        <span class="pagination-info" id="reciters-page-info">الصفحة 1 من 1</span>
                        <button class="page-btn" id="reciters-next-btn" disabled>التالي <i class="fas fa-chevron-left"></i></button>
                    </div>
                </div>

                <!-- ======== تبويب الروايات ======== -->
                <div class="qtab-content" id="riwayat">
                    <div class="search-box">
                        <i class="fas fa-search"></i>
                        <input type="text" id="riwayat-search" placeholder="ابحث عن رواية...">
                    </div>
                    <div class="loading-spinner" id="riwayat-loading">
                        <div class="spinner"></div><p>جاري تحميل الروايات...</p>
                    </div>
                    <div class="cards-grid" id="riwayat-list-container"></div>
                </div>

                <!-- ======== تبويب التفسير ======== -->
                <div class="qtab-content" id="tafsir">
                    <div class="loading-spinner" id="tafsir-loading">
                        <div class="spinner"></div><p>جاري تحميل التفاسير...</p>
                    </div>
                    <div class="cards-grid" id="tafsir-list-container"></div>
                </div>
            </div>

            <!-- قسم سور القارئ -->
            <div id="reciter-suras-section" class="suras-section" style="display:none;">
                <div class="section-subheader">
                    <button class="back-sub-btn" onclick="goBackToReciters()"><i class="fas fa-arrow-right"></i> عودة</button>
                    <h3><i class="fas fa-user-circle"></i> <span id="reciter-name-display"></span></h3>
                </div>
                <div class="suras-grid" id="reciter-suras-grid"></div>
            </div>

            <!-- قسم سور الرواية -->
            <div id="riwayah-suras-section" class="suras-section" style="display:none;">
                <div class="section-subheader">
                    <button class="back-sub-btn" onclick="goBackToRiwayat()"><i class="fas fa-arrow-right"></i> عودة</button>
                    <h3><i class="fas fa-book-quran"></i> رواية: <span id="riwayah-name-display"></span></h3>
                </div>
                <div class="suras-grid" id="riwayah-suras-grid"></div>
            </div>

            <!-- قسم التفسير التفصيلي -->
            <div id="tafsir-content-section" class="suras-section" style="display:none;">
                <div class="section-subheader">
                    <button class="back-sub-btn" onclick="goBackToTafsir()"><i class="fas fa-arrow-right"></i> عودة</button>
                    <h3><i class="fas fa-search"></i> تفسير: <span id="tafsir-name-display"></span></h3>
                </div>
                <div class="tafsir-controls">
                    <select id="surah-select-tafsir" class="select-control">
                        <option value="">اختر السورة</option>
                    </select>
                    <button id="get-tafsir-content" class="btn-primary"><i class="fas fa-eye"></i> عرض التفسير</button>
                </div>
                <div class="loading-spinner" id="tafsir-content-loading">
                    <div class="spinner"></div><p>جاري تحميل التفسير...</p>
                </div>
                <div id="tafsir-content-result" class="tafsir-result"></div>
            </div>
        </section>

        <!-- ==================== شاشة الأحاديث ==================== -->
        <section id="hadith" class="screen">
            <div class="screen-header">
                <button class="back-btn" data-back="home"><i class="fas fa-chevron-right"></i></button>
                <h2 class="screen-title"><i class="fas fa-book-open"></i> الأحاديث النبوية</h2>
            </div>
            <div class="hadith-controls">
                <div class="control-row">
                    <div class="control-group">
                        <label><i class="fas fa-book"></i> كتاب الحديث</label>
                        <select id="hadith-book" class="select-control">
                            <option value="bukhari">صحيح البخاري</option>
                            <option value="muslim">صحيح مسلم</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label><i class="fas fa-hashtag"></i> رقم الحديث (اختياري)</label>
                        <input type="number" id="hadith-number" class="input-control" placeholder="اتركه فارغاً للعشوائي">
                    </div>
                </div>
                <div class="control-buttons">
                    <button id="get-hadith" class="btn-primary"><i class="fas fa-search"></i> الحصول على حديث</button>
                    <button id="get-random-hadith" class="btn-secondary"><i class="fas fa-random"></i> حديث عشوائي</button>
                </div>
            </div>
            <div class="loading-spinner" id="hadith-loading"><div class="spinner"></div><p>جاري تحميل الحديث...</p></div>
            <div id="hadith-result"></div>
        </section>

        <!-- ==================== شاشة إذاعات القرآن ==================== -->
        <section id="radio" class="screen">
            <div class="screen-header">
                <button class="back-btn" data-back="home"><i class="fas fa-chevron-right"></i></button>
                <h2 class="screen-title"><i class="fas fa-broadcast-tower"></i> إذاعات القرآن الكريم</h2>
            </div>
            <!-- البحث عن إذاعة -->
            <div class="search-box radio-search-box">
                <i class="fas fa-search"></i>
                <input type="text" id="radio-search" placeholder="ابحث عن إذاعة بالاسم...">
            </div>
            
            <div class="loading-spinner" id="radio-loading"><div class="spinner"></div><p>جاري تحميل الإذاعات...</p></div>
            <div class="radio-grid" id="radio-list"></div>
            <div class="pagination-controls" id="radio-pagination" style="display:none;">
                <button class="page-btn" id="radio-prev-btn" disabled><i class="fas fa-chevron-right"></i> السابق</button>
                <span class="pagination-info" id="radio-page-info">الصفحة 1 من 1</span>
                <button class="page-btn" id="radio-next-btn" disabled>التالي <i class="fas fa-chevron-left"></i></button>
            </div>
        </section>

        <!-- ==================== شاشة مواقيت الصلاة ==================== -->
        <section id="prayer" class="screen">
            <div class="screen-header">
                <button class="back-btn" data-back="home"><i class="fas fa-chevron-right"></i></button>
                <h2 class="screen-title"><i class="fas fa-clock"></i> مواقيت الصلاة</h2>
            </div>
            <div class="prayer-search-bar">
                <div class="control-group">
                    <input type="text" id="city" class="input-control" value="Cairo" placeholder="المدينة">
                </div>
                <div class="control-group">
                    <input type="text" id="country" class="input-control" value="Egypt" placeholder="الدولة">
                </div>
                <button id="get-prayer-times" class="btn-primary"><i class="fas fa-search"></i> بحث</button>
            </div>
            <div class="loading-spinner" id="prayer-loading"><div class="spinner"></div><p>جاري تحميل المواقيت...</p></div>
            <div id="prayer-result">
                <div class="prayer-date-bar">
                    <span id="prayer-date"><i class="fas fa-calendar-alt"></i> --</span>
                    <span id="hijri-date"><i class="fas fa-moon"></i> --</span>
                </div>
                <div class="prayer-grid">
                    <div class="prayer-card fajr-card"    data-prayer="Fajr">    <div class="prayer-card-icon"><i class="fas fa-sun"></i></div>            <div class="prayer-name">الفجر</div>   <div class="prayer-time" id="fajr">--:--</div></div>
                    <div class="prayer-card sunrise-card" data-prayer="Sunrise"> <div class="prayer-card-icon"><i class="fas fa-cloud-sun"></i></div>        <div class="prayer-name">الشروق</div>  <div class="prayer-time" id="sunrise">--:--</div></div>
                    <div class="prayer-card dhuhr-card"   data-prayer="Dhuhr">   <div class="prayer-card-icon"><i class="fas fa-sun"></i></div>             <div class="prayer-name">الظهر</div>   <div class="prayer-time" id="dhuhr">--:--</div></div>
                    <div class="prayer-card asr-card"     data-prayer="Asr">     <div class="prayer-card-icon"><i class="fas fa-sun"></i></div>             <div class="prayer-name">العصر</div>   <div class="prayer-time" id="asr">--:--</div></div>
                    <div class="prayer-card maghrib-card" data-prayer="Maghrib"> <div class="prayer-card-icon"><i class="fas fa-cloud-sun-rain"></i></div>   <div class="prayer-name">المغرب</div>  <div class="prayer-time" id="maghrib">--:--</div></div>
                    <div class="prayer-card isha-card"    data-prayer="Isha">    <div class="prayer-card-icon"><i class="fas fa-moon"></i></div>             <div class="prayer-name">العشاء</div>  <div class="prayer-time" id="isha">--:--</div></div>
                </div>
            </div>
        </section>

        <!-- ==================== شاشة الأذكار ==================== -->
        <section id="azkar" class="screen">
            <div class="screen-header">
                <button class="back-btn" data-back="home"><i class="fas fa-chevron-right"></i></button>
                <h2 class="screen-title"><i class="fas fa-hands-praying"></i> الأذكار اليومية</h2>
            </div>
            <div class="azkar-tab-buttons">
                <button class="azkar-tab active" data-azkar="morning"><i class="fas fa-sun"></i> الصباح</button>
                <button class="azkar-tab" data-azkar="evening"><i class="fas fa-moon"></i> المساء</button>
                <button class="azkar-tab" data-azkar="sleep"><i class="fas fa-bed"></i> النوم</button>
                <button class="azkar-tab" data-azkar="waking"><i class="fas fa-bell"></i> الاستيقاظ</button>
                <button class="azkar-tab" data-azkar="prayer"><i class="fas fa-clock"></i> بعد الصلاة</button>
            </div>
            <div class="loading-spinner" id="azkar-loading"><div class="spinner"></div><p>جاري تحميل الأذكار...</p></div>
            <div id="azkar-content" class="azkar-list"></div>
        </section>

    </main>

    <!-- المشغل الثابت - القرآن -->
    <div class="sticky-player" id="sticky-player" style="display:none;">
        <div class="sticky-player-inner">
            <div class="sticky-player-info">
                <div class="sp-icon"><i class="fas fa-play-circle"></i></div>
                <div class="sp-text">
                    <div class="sp-title" id="sp-title">—</div>
                    <div class="sp-sub" id="sp-sub"></div>
                </div>
            </div>
            <div class="sticky-player-audio"><audio id="quran-audio" controls></audio></div>
            <button class="sp-close" id="sp-close"><i class="fas fa-times"></i></button>
        </div>
    </div>

    <!-- المشغل الثابت - الراديو -->
    <div class="sticky-player radio-sticky" id="radio-sticky-player" style="display:none;">
        <div class="sticky-player-inner">
            <div class="sticky-player-info">
                <div class="sp-icon radio-live-dot"><i class="fas fa-broadcast-tower"></i></div>
                <div class="sp-text">
                    <div class="sp-title" id="radio-title">—</div>
                    <div class="sp-sub"><span class="live-badge">LIVE</span></div>
                </div>
            </div>
            <div class="sticky-player-audio"><audio id="radio-audio" controls></audio></div>
            <button class="sp-close" id="radio-sp-close"><i class="fas fa-times"></i></button>
        </div>
    </div>

    <footer class="footer">
        <p class="footer-ayah">﴿ رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنتَ السَّمِيعُ الْعَلِيمُ ﴾</p>
        <p class="footer-copy">جميع الحقوق محفوظة &copy; <span id="current-year">2025</span> موقع رمضان</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script>
        // =====================================================
        //  رمضان - سكريبت التطبيق الكامل (مدمج)
        // =====================================================

        document.addEventListener('DOMContentLoaded', function () {
            document.getElementById('current-year').textContent = new Date().getFullYear();

            initThemeToggle();
            initNavigation();
            initHadith();
            initQuran();
            initPrayerTimes();
            initAzkar();
            initRadio();
            initPlayers();
            loadInitialData();
        });

        // =====================================================
        //  تبديل المظهر (فاتح / داكن)
        // =====================================================
        function initThemeToggle() {
            const btn = document.getElementById('theme-toggle');
            const saved = localStorage.getItem('ramadan_theme') || 'light';
            applyTheme(saved);

            btn.addEventListener('click', () => {
                const isDark = document.body.classList.contains('dark-theme');
                applyTheme(isDark ? 'light' : 'dark');
            });
        }

        function applyTheme(theme) {
            document.body.classList.remove('light-theme', 'dark-theme');
            document.body.classList.add(theme + '-theme');
            localStorage.setItem('ramadan_theme', theme);
        }

        // =====================================================
        //  التنقل بين الشاشات
        // =====================================================
        function initNavigation() {
            document.querySelectorAll('.main-card-btn[data-screen]').forEach(btn => {
                btn.addEventListener('click', () => switchScreen(btn.dataset.screen));
            });

            document.querySelectorAll('.back-btn[data-back]').forEach(btn => {
                btn.addEventListener('click', () => switchScreen(btn.dataset.back));
            });
        }

        function switchScreen(id) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            const target = document.getElementById(id);
            if (target) {
                target.classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                onScreenEnter(id);
            }
        }

        function onScreenEnter(id) {
            switch (id) {
                case 'hadith':  getRandomHadith(); break;
                case 'prayer':  getPrayerTimes();  break;
                case 'azkar':   loadAzkar('morning'); break;
                case 'radio':   loadAllRadioStations(); break;
                case 'quran':
                    if (allReciters.length === 0) loadAllReciters();
                    break;
            }
        }

        // =====================================================
        //  قائمة السور الكاملة (من بايثون)
        // =====================================================
        const ALL_SURAHS = {{ surahs | safe }};

        // =====================================================
        //  خريطة السور إلى الصفحات (من بايثون)
        // =====================================================
        const SURAH_PAGE_MAP = {{ surah_page_map | safe }};

        // =====================================================
        //  متغيرات الصفحات
        // =====================================================
        let currentRecitersPage = 1;
        let currentRadioPage    = 1;
        const itemsPerPage      = 12;

        // =====================================================
        //  الأحاديث النبوية
        // =====================================================
        let hadithCache = { bukhari: null, muslim: null };

        function initHadith() {
            document.getElementById('get-hadith').addEventListener('click', getSpecificHadith);
            document.getElementById('get-random-hadith').addEventListener('click', getRandomHadith);
        }

        async function loadHadithData(book) {
            if (hadithCache[book]) return hadithCache[book];
            showLoading('hadith');
            try {
                const response = await fetch(`/api/hadith/${book}`);
                if (!response.ok) throw new Error('fetch error');
                const data = await response.json();
                hadithCache[book] = data;
                return data;
            } catch (e) {
                console.error(e);
                return null;
            } finally {
                hideLoading('hadith');
            }
        }

        async function getSpecificHadith() {
            const book   = document.getElementById('hadith-book').value;
            const numVal = document.getElementById('hadith-number').value;
            if (!numVal) { Swal.fire({ icon:'warning', title:'أدخل رقم الحديث', text:'الرجاء إدخال رقم الحديث' }); return; }
            showLoading('hadith');
            try {
                const data = await loadHadithData(book);
                if (!data || !data.hadiths) throw new Error('no data');
                const hadiths = data.hadiths;
                const num = parseInt(numVal);
                if (num < 1 || num > hadiths.length) {
                    Swal.fire({ icon:'error', title:'رقم غير صالح', text:`الرجاء إدخال رقم بين 1 و ${hadiths.length}` });
                    return;
                }
                displayHadith(hadiths[num - 1], book, num);
            } catch (e) {
                showError('hadith-result', 'حدث خطأ في جلب الحديث');
            } finally {
                hideLoading('hadith');
            }
        }

        async function getRandomHadith() {
            const book = document.getElementById('hadith-book').value;
            document.getElementById('hadith-number').value = '';
            showLoading('hadith');
            try {
                const data = await loadHadithData(book);
                if (!data || !data.hadiths) throw new Error('no data');
                const hadiths = data.hadiths;
                const idx = Math.floor(Math.random() * hadiths.length);
                displayHadith(hadiths[idx], book, idx + 1);
            } catch (e) {
                showError('hadith-result', 'حدث خطأ في جلب الحديث العشوائي');
            } finally {
                hideLoading('hadith');
            }
        }

        function displayHadith(hadithData, book, number) {
            const el = document.getElementById('hadith-result');
            if (!hadithData) { showError('hadith-result', 'لم يتم العثور على حديث'); return; }
            const bookName = book === 'bukhari' ? 'صحيح البخاري' : 'صحيح مسلم';
            el.innerHTML = `
                <div class="hadith-card">
                    <div class="hadith-book-label">
                        <i class="fas fa-book"></i> ${bookName} - الحديث رقم ${number}
                    </div>
                    <div class="hadith-arabic">
                        ${hadithData.arabic || hadithData.text || 'لا يوجد نص عربي'}
                    </div>
                    ${hadithData.translation ? `<div class="hadith-translation"><strong>الترجمة:</strong>${hadithData.translation}</div>` : ''}
                    ${hadithData.explanation ? `<div class="hadith-explanation"><strong>الشرح:</strong>${hadithData.explanation}</div>` : ''}
                    <div class="hadith-meta">
                        <span><i class="fas fa-book"></i> ${bookName}</span>
                        <span><i class="fas fa-hashtag"></i> ${number}</span>
                        ${hadithData.grade ? `<span><i class="fas fa-star"></i> ${hadithData.grade}</span>` : ''}
                    </div>
                </div>`;
            el.style.display = 'block';
        }

        // =====================================================
        //  القرآن الكريم
        // =====================================================
        let allReciters = [], allRiwayat = [], allMoshaf = [], allTafsir = [];

        function initQuran() {
            setTimeout(initQuranReader, 200);
            document.querySelectorAll('.qtab-btn[data-tab]').forEach(btn => {
                btn.addEventListener('click', () => switchQuranTab(btn.dataset.tab));
            });

            const rs = document.getElementById('reciter-search');
            if (rs) rs.addEventListener('input', e => searchReciters(e.target.value));

            const rws = document.getElementById('riwayat-search');
            if (rws) rws.addEventListener('input', e => searchRiwayat(e.target.value));

            const gtc = document.getElementById('get-tafsir-content');
            if (gtc) gtc.addEventListener('click', getTafsirContent);

            initRecitersPagination();
        }

        function initRecitersPagination() {
            document.getElementById('reciters-prev-btn').addEventListener('click', () => {
                if (currentRecitersPage > 1) { currentRecitersPage--; displayReciters(allReciters); scrollToTop('reciters-list-container'); }
            });
            document.getElementById('reciters-next-btn').addEventListener('click', () => {
                const total = Math.ceil(allReciters.length / itemsPerPage);
                if (currentRecitersPage < total) { currentRecitersPage++; displayReciters(allReciters); scrollToTop('reciters-list-container'); }
            });
        }

        function scrollToTop(id) {
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function switchQuranTab(tabId) {
            document.querySelectorAll('.qtab-btn[data-tab]').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.qtab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`.qtab-btn[data-tab="${tabId}"]`)?.classList.add('active');
            document.getElementById(tabId)?.classList.add('active');

            document.getElementById('reciter-suras-section').style.display  = 'none';
            document.getElementById('riwayah-suras-section').style.display  = 'none';
            document.getElementById('tafsir-content-section').style.display = 'none';

            if (tabId === "reciters" && allReciters.length === 0) loadAllReciters();
            if (tabId === 'riwayat' && allRiwayat.length === 0)    { loadAllRiwayat(); loadAllMoshaf(); }
            if (tabId === 'tafsir'  && allTafsir.length === 0)     loadAllTafsir();
        }

        async function loadAllReciters() {
            showLoading('reciters');
            try {
                const res  = await fetch('https://mp3quran.net/api/v3/reciters?language=ar');
                if (!res.ok) throw new Error('fetch error');
                const data = await res.json();
                allReciters = data.reciters || [];
                if (allReciters.length === 0) allReciters = generateSampleReciters();
                displayReciters(allReciters);
            } catch (e) {
                console.error(e);
                allReciters = generateSampleReciters();
                displayReciters(allReciters);
            } finally {
                hideLoading('reciters');
            }
        }

        function generateSampleReciters() {
            return [
                { id:'1', name:'الشيخ عبد الباسط عبد الصمد',   rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/abdulbasit/murattal/', sura_total:'114'}] },
                { id:'2', name:'الشيخ محمد صديق المنشاوي',      rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/minshawi/murattal/', sura_total:'114'}] },
                { id:'3', name:'الشيخ محمود خليل الحصري',       rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/husary/murattal/', sura_total:'114'}] },
                { id:'4', name:'الشيخ محمد أيوب',               rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/ayyoub/murattal/', sura_total:'114'}] },
                { id:'5', name:'الشيخ مشاري العفاسي',           rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/affasi/murattal/', sura_total:'114'}] },
                { id:'6', name:'الشيخ ماهر المعيقلي',           rewaya:'حفص عن عاصم', count:114, moshaf:[{server:'https://server8.mp3quran.net/maher/murattal/', sura_total:'114'}] },
            ];
        }

        function displayReciters(reciters) {
            const container   = document.getElementById('reciters-list-container');
            const paginDiv    = document.getElementById('reciters-pagination');
            const pageInfo    = document.getElementById('reciters-page-info');
            const prevBtn     = document.getElementById('reciters-prev-btn');
            const nextBtn     = document.getElementById('reciters-next-btn');

            if (!reciters || reciters.length === 0) {
                container.innerHTML = '<p style="color:var(--text3);padding:20px;">لم يتم العثور على قراء</p>';
                paginDiv.style.display = 'none';
                return;
            }

            const totalPages = Math.ceil(reciters.length / itemsPerPage);
            const start = (currentRecitersPage - 1) * itemsPerPage;
            const slice = reciters.slice(start, start + itemsPerPage);

            container.innerHTML = slice.map(r => `
                <div class="reciter-card" onclick="showReciterSuras('${r.id}','${esc(r.name)}','${r.rewaya||'حفص عن عاصم'}','${r.moshaf&&r.moshaf[0]?r.moshaf[0].server:''}')">
                    <div class="reciter-icon"><i class="fas fa-user"></i></div>
                    <div class="reciter-info">
                        <h4>${r.name}</h4>
                        <p><i class="fas fa-book-open"></i> ${r.rewaya || 'حفص عن عاصم'}</p>
                        <p><i class="fas fa-list"></i> ${r.count || 114} سورة</p>
                    </div>
                </div>`).join('');

            pageInfo.textContent = `الصفحة ${currentRecitersPage} من ${totalPages}`;
            prevBtn.disabled = currentRecitersPage === 1;
            nextBtn.disabled = currentRecitersPage === totalPages;
            paginDiv.style.display = totalPages > 1 ? 'flex' : 'none';
            container.style.display = 'grid';
        }

        function searchReciters(q) {
            currentRecitersPage = 1;
            const filtered = q.trim() ? allReciters.filter(r => r.name.includes(q) || (r.rewaya && r.rewaya.includes(q))) : allReciters;
            displayReciters(filtered);
        }

        async function loadAllRiwayat() {
            showLoading('riwayat');
            try {
                const res  = await fetch('https://www.mp3quran.net/api/v3/riwayat?language=ar');
                const data = await res.json();
                allRiwayat = data.riwayat || [];
                displayRiwayat(allRiwayat);
            } catch (e) {
                showError('riwayat-list-container', 'حدث خطأ في جلب الروايات');
            } finally {
                hideLoading('riwayat');
            }
        }

        async function loadAllMoshaf() {
            try {
                const res  = await fetch('https://www.mp3quran.net/api/v3/moshaf?language=ar');
                const data = await res.json();
                allMoshaf  = data.riwayat || [];
            } catch (e) { console.error(e); }
        }

        function displayRiwayat(riwayat) {
            const c = document.getElementById('riwayat-list-container');
            if (!riwayat || riwayat.length === 0) { c.innerHTML = '<p style="color:var(--text3);padding:20px;">لم يتم العثور على روايات</p>'; return; }
            c.innerHTML = riwayat.map(r => `
                <div class="riwayah-card" onclick="showRiwayahSuras(${r.id},'${esc(r.name)}')">
                    <div class="riwayah-icon"><i class="fas fa-book-quran"></i></div>
                    <div class="riwayah-info"><h4>${r.name}</h4><p>انقر للاستماع</p></div>
                </div>`).join('');
            c.style.display = 'grid';
        }

        function searchRiwayat(q) {
            const filtered = q.trim() ? allRiwayat.filter(r => r.name.includes(q)) : allRiwayat;
            displayRiwayat(filtered);
        }

        async function loadAllTafsir() {
            showLoading('tafsir');
            try {
                const res  = await fetch('https://www.mp3quran.net/api/v3/tafasir?language=ar');
                const data = await res.json();
                allTafsir  = data.tafasir || [];
                displayTafsir(allTafsir);
            } catch (e) {
                showError('tafsir-list-container', 'حدث خطأ في جلب التفاسير');
            } finally {
                hideLoading('tafsir');
            }
        }

        function displayTafsir(list) {
            const c = document.getElementById('tafsir-list-container');
            if (!list || list.length === 0) { c.innerHTML = '<p style="color:var(--text3);padding:20px;">لم يتم العثور على تفاسير</p>'; return; }
            c.innerHTML = list.map(t => `
                <div class="tafsir-card" onclick="showTafsirContent('${t.url}','${esc(t.name)}')">
                    <div class="tafsir-icon"><i class="fas fa-search"></i></div>
                    <div class="tafsir-info"><h4>${t.name}</h4><p>انقر لعرض التفسير</p></div>
                </div>`).join('');
            c.style.display = 'grid';
        }

        function showReciterSuras(id, name, rewaya, server) {
            hideQuranTabs();
            document.getElementById('reciter-suras-section').style.display = 'block';
            document.getElementById('reciter-name-display').textContent = name;
            const g = document.getElementById('reciter-suras-grid');
            g.innerHTML = ALL_SURAHS.map(s => `
                <div class="sura-item" onclick="playSuraForReciter(${s.number},'${esc(name)}','${rewaya}','${server}')">
                    <div class="sura-number">${s.number}</div>
                    <div class="sura-name">${s.name}</div>
                </div>`).join('');
        }

        function showRiwayahSuras(id, name) {
            hideQuranTabs();
            document.getElementById('riwayah-suras-section').style.display = 'block';
            document.getElementById('riwayah-name-display').textContent = name;
            const g = document.getElementById('riwayah-suras-grid');
            g.innerHTML = ALL_SURAHS.map(s => `
                <div class="sura-item" onclick="playSuraForRiwayah(${s.number},${id},'${esc(name)}')">
                    <div class="sura-number">${s.number}</div>
                    <div class="sura-name">${s.name}</div>
                </div>`).join('');
        }

        function showTafsirContent(url, name) {
            hideQuranTabs();
            document.getElementById('tafsir-content-section').style.display = 'block';
            document.getElementById('tafsir-name-display').textContent = name;
            document.getElementById('tafsir-content-section').dataset.tafsirUrl = url;
            populateSurahListForTafsir();
        }

        function populateSurahListForTafsir() {
            const sel = document.getElementById('surah-select-tafsir');
            sel.innerHTML = '<option value="">اختر السورة</option>' +
                ALL_SURAHS.map(s => `<option value="${s.number}">${s.number}. ${s.name} (${s.ayahs} آية)</option>`).join('');
        }

        async function getTafsirContent() {
            const n = document.getElementById('surah-select-tafsir').value;
            if (!n) { Swal.fire({ icon:'warning', title:'اختر سورة', text:'الرجاء اختيار سورة' }); return; }
            const url = document.getElementById('tafsir-content-section').dataset.tafsirUrl;
            showLoading('tafsir-content');
            try {
                const res  = await fetch(`/api/proxy/tafsir?url=${encodeURIComponent(url)}&surah=${n}`);
                const data = await res.json();
                displayTafsirContent(data, n);
            } catch (e) {
                showError('tafsir-content-result', 'حدث خطأ في جلب التفسير');
            } finally {
                hideLoading('tafsir-content');
            }
        }

        function displayTafsirContent(data, num) {
            const c = document.getElementById('tafsir-content-result');
            const s = ALL_SURAHS.find(x => x.number === parseInt(num));
            if (!data || !data.tafsir || data.tafsir.length === 0) {
                c.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i><div><h3>لم يتم العثور على تفسير</h3></div></div>`;
                return;
            }
            c.innerHTML = data.tafsir.map((v, i) => `
                <div class="tafsir-verse">
                    <div class="verse-header-tafsir"><span class="verse-number-tafsir">آية ${i + 1}</span></div>
                    <div class="verse-arabic-tafsir">${v.text || ''}</div>
                    <div class="verse-tafsir-text">${v.tafsir || 'تفسير الآية...'}</div>
                </div>`).join('');
            c.style.display = 'block';
        }

        function hideQuranTabs() {
            document.querySelectorAll('.qtab-content').forEach(c => c.classList.remove('active'));
            document.getElementById('reciter-suras-section').style.display  = 'none';
            document.getElementById('riwayah-suras-section').style.display  = 'none';
            document.getElementById('tafsir-content-section').style.display = 'none';
        }

        function goBackToReciters() { switchQuranTab('reciters'); }
        function goBackToRiwayat()  { switchQuranTab('riwayat');  }
        function goBackToTafsir()   { switchQuranTab('tafsir');   }

        function playSuraForReciter(num, name, rewaya, server) {
            const s = ALL_SURAHS.find(x => x.number === num);
            if (!s) return;
            const fmt = String(num).padStart(3, '0');
            const url = server ? `${server}${fmt}.mp3` : `https://server8.mp3quran.net/husary/murattal/${fmt}.mp3`;
            playQuranAudio(url, `القارئ: ${name}`, `سورة ${s.name} - ${rewaya}`);
        }

        function playSuraForRiwayah(num, riwayahId, riwayahName) {
            const s = ALL_SURAHS.find(x => x.number === num);
            if (!s) return;
            const fmt = String(num).padStart(3, '0');
            let url;
            switch (riwayahId) {
                case 2:  url = `https://server8.mp3quran.net/warsh/murattal/${fmt}.mp3`; break;
                default: url = `https://server8.mp3quran.net/husary/murattal/${fmt}.mp3`;
            }
            playQuranAudio(url, `الرواية: ${riwayahName}`, `سورة ${s.name}`);
        }

        function playQuranAudio(url, title, subtitle) {
            const player  = document.getElementById('sticky-player');
            const audio   = document.getElementById('quran-audio');
            const spTitle = document.getElementById('sp-title');
            const spSub   = document.getElementById('sp-sub');

            audio.src = url;
            spTitle.textContent = title;
            spSub.textContent   = subtitle;
            player.style.display = 'block';

            audio.play().catch(e => {
                console.error(e);
                player.style.display = 'none';
                Swal.fire({ icon:'error', title:'خطأ في التشغيل', text:'تعذر تشغيل التلاوة' });
            });

            const homePWrap  = document.getElementById('home-player-wrap');
            const homeTitle  = document.getElementById('home-player-title');
            const homeSub    = document.getElementById('home-player-subtitle');
            const homeAudio  = document.getElementById('main-audio');
            if (homePWrap) {
                homeTitle.textContent = title;
                homeSub.textContent   = subtitle;
                homeAudio.src = url;
                homePWrap.style.display = 'block';
                homeAudio.play().catch(()=>{});
            }
        }

        // =====================================================
        //  مواقيت الصلاة
        // =====================================================
        function initPrayerTimes() {
            document.getElementById('get-prayer-times').addEventListener('click', getPrayerTimes);
        }

        async function getPrayerTimes() {
            const city    = document.getElementById('city').value.trim()    || 'Cairo';
            const country = document.getElementById('country').value.trim() || 'Egypt';
            showLoading('prayer');
            try {
                const res  = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}&method=8`);
                if (!res.ok) throw new Error('fetch error');
                const data = await res.json();
                displayPrayerTimes(data.data);
            } catch (e) {
                showError('prayer-result', 'حدث خطأ في جلب مواقيت الصلاة. تحقق من اسم المدينة.');
            } finally {
                hideLoading('prayer');
            }
        }

        function displayPrayerTimes(d) {
            const t = d.timings;
            const dt = d.date;
            document.getElementById('prayer-date').innerHTML  = `<i class="fas fa-calendar-alt"></i> ${dt.readable}`;
            document.getElementById('hijri-date').innerHTML   = `<i class="fas fa-moon"></i> ${dt.hijri.day} ${dt.hijri.month.ar} ${dt.hijri.year} هـ`;
            document.getElementById('fajr').textContent    = fmt(t.Fajr);
            document.getElementById('sunrise').textContent = fmt(t.Sunrise);
            document.getElementById('dhuhr').textContent   = fmt(t.Dhuhr);
            document.getElementById('asr').textContent     = fmt(t.Asr);
            document.getElementById('maghrib').textContent = fmt(t.Maghrib);
            document.getElementById('isha').textContent    = fmt(t.Isha);
            document.getElementById('prayer-result').style.display = 'block';
            highlightCurrentPrayer(t);
        }

        function fmt(s) { return s ? s.substring(0, 5) : '--:--'; }

        function highlightCurrentPrayer(timings) {
            const now = new Date();
            const cur = now.getHours() * 60 + now.getMinutes();
            const prayers = [
                { id:'fajr',    key:'Fajr'    },
                { id:'sunrise', key:'Sunrise' },
                { id:'dhuhr',   key:'Dhuhr'   },
                { id:'asr',     key:'Asr'     },
                { id:'maghrib', key:'Maghrib' },
                { id:'isha',    key:'Isha'    }
            ];
            let nextIdx = 0;
            prayers.forEach((p, i) => {
                const [h, m] = timings[p.key].split(':').map(Number);
                if (h * 60 + m <= cur) nextIdx = i + 1;
            });
            if (nextIdx >= prayers.length) nextIdx = 0;
            const cards = document.querySelectorAll('.prayer-card');
            cards.forEach((c, i) => {
                c.classList.toggle('next-prayer', i === nextIdx);
            });
        }

        // =====================================================
        //  الأذكار
        // =====================================================
        let currentAzkarType = 'morning';
        let allAzkar = {};

        function initAzkar() {
            document.querySelectorAll('.azkar-tab[data-azkar]').forEach(tab => {
                tab.addEventListener('click', () => {
                    document.querySelectorAll('.azkar-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    currentAzkarType = tab.dataset.azkar;
                    loadAzkar(currentAzkarType);
                });
            });
        }

        async function loadAzkar(type) {
            showLoading('azkar');
            try {
                const res  = await fetch('/api/azkar');
                if (!res.ok) throw new Error('fetch error');
                const data = await res.json();
                allAzkar = data;
                displayAzkar(type);
            } catch (e) {
                displayMockAzkar(type);
            } finally {
                hideLoading('azkar');
                document.getElementById('azkar-content').style.display = 'flex';
            }
        }

        function displayAzkar(type) {
            const c = document.getElementById('azkar-content');
            let azkar = [];
            if (allAzkar[type])                         azkar = allAzkar[type];
            else if (allAzkar.content && allAzkar.content[type]) azkar = allAzkar.content[type];
            else if (Array.isArray(allAzkar))            azkar = allAzkar.filter(x => x.category === type).slice(0, 15);
            if (!azkar || azkar.length === 0) { displayMockAzkar(type); return; }
            c.innerHTML = azkar.slice(0, 20).map(z => `
                <div class="zekr-card">
                    <div class="content">${z.zekr || z.content || z.text || ''}</div>
                    ${z.description ? `<div class="description">${z.description}</div>` : ''}
                    ${z.count ? `<div class="count"><i class="fas fa-redo"></i> ${z.count} مرة</div>` : ''}
                </div>`).join('');
        }

        function displayMockAzkar(type) {
            const c = document.getElementById('azkar-content');
            const azkarData = {
                morning: [
                    { zekr:'أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير', count:'1' },
                    { zekr:'اللهم بك أصبحنا، وبك أمسينا، وبك نحيا، وبك نموت، وإليك النشور', count:'1' },
                    { zekr:'اللهم ما أصبح بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر', count:'1' },
                    { zekr:'اللهم عافني في بدني، اللهم عافني في سمعي، اللهم عافني في بصري، لا إله إلا أنت', count:'3' },
                    { zekr:'حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم', count:'7' }
                ],
                evening: [
                    { zekr:'أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير', count:'1' },
                    { zekr:'اللهم بك أمسينا، وبك أصبحنا، وبك نحيا، وبك نموت، وإليك المصير', count:'1' },
                    { zekr:'أعوذ بكلمات الله التامات من شر ما خلق', count:'3' },
                    { zekr:'اللهم إني أسألك العفو والعافية في الدنيا والآخرة', count:'1' }
                ],
                sleep: [
                    { zekr:'باسمك اللهم أموت وأحيا', count:'1' },
                    { zekr:'اللهم قني عذابك يوم تبعث عبادك', count:'3' },
                    { zekr:'سبحان الله (33)، الحمد لله (33)، الله أكبر (34)', count:'100' },
                    { zekr:'آية الكرسي: اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...', count:'1' }
                ],
                waking: [
                    { zekr:'الحمد لله الذي أحيانا بعد ما أماتنا وإليه النشور', count:'1' },
                    { zekr:'لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير', count:'1' },
                    { zekr:'الحمد لله الذي عافاني في جسدي، ورد علي روحي، وأذن لي بذكره', count:'1' }
                ],
                prayer: [
                    { zekr:'أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه', count:'3' },
                    { zekr:'اللهم أنت السلام ومنك السلام تباركت يا ذا الجلال والإكرام', count:'1' },
                    { zekr:'لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير', count:'1' },
                    { zekr:'سبحان الله (33)، الحمد لله (33)، الله أكبر (33)، لا إله إلا الله وحده لا شريك له', count:'100' }
                ]
            };
            const list = azkarData[type] || azkarData.morning;
            c.innerHTML = list.map(z => `
                <div class="zekr-card">
                    <div class="content">${z.zekr}</div>
                    ${z.count ? `<div class="count"><i class="fas fa-redo"></i> ${z.count} مرة</div>` : ''}
                </div>`).join('');
        }

        // =====================================================
        //  إذاعات القرآن
        // =====================================================
        let allRadioStations = [];
        let filteredRadioStations = [];

        function initRadio() {
            initRadioPagination();
        }

        function initRadioPagination() {
            document.getElementById('radio-prev-btn').addEventListener('click', () => {
                if (currentRadioPage > 1) { currentRadioPage--; displayRadioStations(filteredRadioStations.length ? filteredRadioStations : allRadioStations); scrollToTop('radio-list'); }
            });
            document.getElementById('radio-next-btn').addEventListener('click', () => {
                const stations = filteredRadioStations.length ? filteredRadioStations : allRadioStations;
                const total = Math.ceil(stations.length / itemsPerPage);
                if (currentRadioPage < total) { currentRadioPage++; displayRadioStations(stations); scrollToTop('radio-list'); }
            });

            const radioSearch = document.getElementById('radio-search');
            if (radioSearch) {
                radioSearch.addEventListener('input', function() {
                    const query = this.value.trim().toLowerCase();
                    if (!query) {
                        filteredRadioStations = [];
                        currentRadioPage = 1;
                        displayRadioStations(allRadioStations);
                        return;
                    }
                    filteredRadioStations = allRadioStations.filter(r => r.name.toLowerCase().includes(query));
                    currentRadioPage = 1;
                    displayRadioStations(filteredRadioStations);
                });
            }
        }

        async function loadAllRadioStations() {
            if (allRadioStations.length > 0) { displayRadioStations(allRadioStations); return; }
            showLoading('radio');
            try {
                const response = await fetch('/api/radio-stations');
                const data = await response.json();
                allRadioStations = data;
                displayRadioStations(allRadioStations);
            } catch (e) {
                showError('radio-list', 'حدث خطأ في تحميل الإذاعات');
            } finally {
                hideLoading('radio');
            }
        }

        function displayRadioStations(stations) {
            const c       = document.getElementById('radio-list');
            const pagDiv  = document.getElementById('radio-pagination');
            const pgInfo  = document.getElementById('radio-page-info');
            const prevBtn = document.getElementById('radio-prev-btn');
            const nextBtn = document.getElementById('radio-next-btn');

            if (!stations || stations.length === 0) {
                c.innerHTML = '<p style="color:var(--text3);padding:20px;">لم يتم العثور على إذاعات</p>';
                pagDiv.style.display = 'none';
                return;
            }

            const total = Math.ceil(stations.length / itemsPerPage);
            const start = (currentRadioPage - 1) * itemsPerPage;
            const slice = stations.slice(start, start + itemsPerPage);

            c.innerHTML = '';
            slice.forEach(s => {
                const card = document.createElement('div');
                card.className = 'radio-card';

                if (s.img) {
                    card.innerHTML = `<div class="radio-image"><img src="${s.img}" alt="radio" onerror="this.parentElement.innerHTML='<div class=\\'radio-no-img\\'><i class=\\'fas fa-broadcast-tower\\'></i></div>'"></div>`;
                } else {
                    card.innerHTML = '<div class="radio-no-img"><i class="fas fa-broadcast-tower"></i></div>';
                }

                const infoDiv = document.createElement('div');
                infoDiv.className = 'radio-info';
                
                const title = document.createElement('h4');
                title.textContent = s.name || 'إذاعة';
                infoDiv.appendChild(title);

                if (s.description) {
                    const desc = document.createElement('p');
                    desc.className = 'radio-desc';
                    desc.textContent = s.description;
                    infoDiv.appendChild(desc);
                }

                if (s.country) {
                    const country = document.createElement('p');
                    country.className = 'radio-country';
                    country.innerHTML = '<i class="fas fa-globe"></i> ';
                    country.appendChild(document.createTextNode(s.country));
                    infoDiv.appendChild(country);
                }

                card.appendChild(infoDiv);

                const btn = document.createElement('button');
                btn.className = 'play-radio-btn';
                btn.innerHTML = '<i class="fas fa-play"></i> تشغيل البث';
                btn.onclick = () => playRadioStation(s.url, s.name);
                card.appendChild(btn);

                c.appendChild(card);
            });

            pgInfo.textContent = `الصفحة ${currentRadioPage} من ${total}`;
            prevBtn.disabled = currentRadioPage === 1;
            nextBtn.disabled = currentRadioPage === total;
            pagDiv.style.display = total > 1 ? 'flex' : 'none';
            c.style.display = 'grid';
        }

        function playRadioStation(url, name) {
            const player  = document.getElementById('radio-sticky-player');
            const audio   = document.getElementById('radio-audio');
            const rtitle  = document.getElementById('radio-title');

            audio.pause();
            audio.src = '';
            
            audio.src = url;
            rtitle.textContent = name || 'إذاعة';
            player.style.display = 'block';

            setTimeout(() => {
                const playPromise = audio.play();
                
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        console.log('Radio playing:', name);
                    }).catch(e => {
                        console.error('Radio error:', e);
                        
                        setTimeout(() => {
                            if (audio.paused && audio.readyState < 2) {
                                player.style.display = 'none';
                                Swal.fire({ 
                                    icon:'error', 
                                    title:'خطأ في التشغيل', 
                                    text:'تعذر تشغيل الإذاعة. قد تكون المحطة غير متاحة حالياً.',
                                    confirmButtonText: 'حسناً',
                                    confirmButtonColor: '#1a6b3c'
                                });
                            }
                        }, 3000);
                    });
                }
            }, 100);
        }

        // =====================================================
        //  تهيئة المشغلات
        // =====================================================
        function initPlayers() {
            document.getElementById('sp-close').addEventListener('click', () => {
                const audio = document.getElementById('quran-audio');
                audio.pause(); audio.src = '';
                document.getElementById('sticky-player').style.display = 'none';
                const hw = document.getElementById('home-player-wrap');
                if (hw) hw.style.display = 'none';
            });

            document.getElementById('radio-sp-close').addEventListener('click', () => {
                const audio = document.getElementById('radio-audio');
                audio.pause(); audio.src = '';
                document.getElementById('radio-sticky-player').style.display = 'none';
            });

            const hClose = document.getElementById('home-player-close');
            if (hClose) {
                hClose.addEventListener('click', () => {
                    const audio = document.getElementById('main-audio');
                    audio.pause(); audio.src = '';
                    document.getElementById('home-player-wrap').style.display = 'none';
                });
            }
        }

        // =====================================================
        //  تحميل البيانات الأولية
        // =====================================================
        function loadInitialData() {
            getPrayerTimes();
            loadAzkar('morning');
        }

        // =====================================================
        //  دوال مساعدة: تحميل / إخفاء / أخطاء
        // =====================================================
        function showLoading(id) {
            const el = document.getElementById(`${id}-loading`);
            if (el) el.classList.add('active');
            ['result','list','list-container','content'].forEach(suffix => {
                const t = document.getElementById(`${id}-${suffix}`);
                if (t) t.style.display = 'none';
            });
        }

        function hideLoading(id) {
            const el = document.getElementById(`${id}-loading`);
            if (el) el.classList.remove('active');
            const r = document.getElementById(`${id}-result`);
            if (r) r.style.display = 'block';
        }

        function showError(id, msg) {
            const el = document.getElementById(id);
            if (el) {
                el.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i><div><h3>حدث خطأ</h3><p>${msg}</p></div></div>`;
                el.style.display = 'block';
            }
        }

        function esc(s) {
            if (!s) return '';
            return s.replace(/['"]/g, '').replace(/&/g, 'و').replace(/</g, '').replace(/>/g, '');
        }

        // =====================================================
        //  نظام قراءة القرآن الكريم
        // =====================================================
        let currentPage = 1;
        let currentSurahNumber = 1;
        let mushafZoom = 100;
        const ZOOM_STEP = 20;
        const ZOOM_MIN  = 60;
        const ZOOM_MAX  = 300;

        function initQuranReader() {
            buildSurahsIndexGrid(SURAH_PAGE_MAP);

            const searchInput = document.getElementById('surah-list-search');
            if (searchInput) {
                searchInput.addEventListener('input', function () {
                    const q = this.value.trim();
                    const filtered = q
                        ? SURAH_PAGE_MAP.filter(s => s.name.includes(q) || String(s.n).includes(q))
                        : SURAH_PAGE_MAP;
                    buildSurahsIndexGrid(filtered);
                });
            }

            const pageJumpBtn = document.getElementById('page-jump-btn');
            const pageJumpInput = document.getElementById('page-jump-input');
            
            if (pageJumpBtn) {
                pageJumpBtn.addEventListener('click', jumpToPage);
            }
            
            if (pageJumpInput) {
                pageJumpInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') jumpToPage();
                });
            }

            document.getElementById('back-to-surah-list')?.addEventListener('click', showSurahSelector);
            document.getElementById('surah-list-btn-bottom')?.addEventListener('click', showSurahSelector);

            document.getElementById('prev-surah-btn')?.addEventListener('click', goToPrevPage);
            document.getElementById('next-surah-btn')?.addEventListener('click', goToNextPage);

            document.getElementById('zoom-in-btn')?.addEventListener('click', () => changeMushafZoom(ZOOM_STEP));
            document.getElementById('zoom-out-btn')?.addEventListener('click', () => changeMushafZoom(-ZOOM_STEP));
            document.getElementById('zoom-reset-btn')?.addEventListener('click', resetMushafZoom);

            initPinchZoom();

            const pageJumpReaderBtn = document.getElementById('page-jump-reader-btn');
            const pageJumpReaderInput = document.getElementById('page-jump-reader-input');
            
            if (pageJumpReaderBtn) {
                pageJumpReaderBtn.addEventListener('click', jumpToPageFromReader);
            }
            
            if (pageJumpReaderInput) {
                pageJumpReaderInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') jumpToPageFromReader();
                });
            }
        }

        function buildSurahsIndexGrid(list) {
            const grid = document.getElementById('surahs-index-grid');
            if (!grid) return;
            if (!list || list.length === 0) {
                grid.innerHTML = '<p style="color:var(--text3);padding:20px;grid-column:1/-1;text-align:center;">لم يتم العثور على سور مطابقة</p>';
                return;
            }
            grid.innerHTML = list.map(s => `
                <div class="surah-index-card" onclick="loadSurahForReading(${s.n})">
                    <div class="surah-num-badge">${s.n}</div>
                    <div class="surah-index-info">
                        <div class="surah-index-name">${s.name}</div>
                        <div class="surah-index-sub">${s.type} • ج${s.juz}</div>
                    </div>
                    <div class="surah-index-ayahs">${s.ayahs} آية</div>
                </div>`).join('');
        }

        function showSurahSelector() {
            document.getElementById('quran-surah-selector').style.display = 'block';
            document.getElementById('quran-reader-view').style.display = 'none';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function loadSurahForReading(surahNum) {
            const surahInfo = SURAH_PAGE_MAP.find(s => s.n === surahNum);
            if (!surahInfo) return;
            currentSurahNumber = surahNum;
            openPageViewer(surahInfo.startPage, surahInfo);
        }

        function openPageViewer(pageNum, surahInfo) {
            currentPage = Math.max(1, Math.min(604, pageNum));

            document.getElementById('quran-surah-selector').style.display = 'none';
            document.getElementById('quran-reader-view').style.display = 'block';

            updateReaderHeader();
            renderMushafPage(currentPage);

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function updateReaderHeader() {
            const surahInfo = getSurahByPage(currentPage);

            const nameEl = document.getElementById('reader-surah-name');
            const metaEl = document.getElementById('reader-surah-meta');
            const pageEl = document.getElementById('reader-page-num');

            if (nameEl) nameEl.textContent = surahInfo ? 'سورة ' + surahInfo.name : '—';
            if (metaEl) metaEl.textContent = surahInfo ? `${surahInfo.type} • الجزء ${surahInfo.juz}` : '';
            if (pageEl) pageEl.textContent = `صفحة ${currentPage} / 604`;

            const prevBtn = document.getElementById('prev-surah-btn');
            const nextBtn = document.getElementById('next-surah-btn');
            if (prevBtn) prevBtn.disabled = currentPage <= 1;
            if (nextBtn) nextBtn.disabled = currentPage >= 604;
        }

        function getSurahByPage(page) {
            let result = SURAH_PAGE_MAP[0];
            for (let i = 0; i < SURAH_PAGE_MAP.length; i++) {
                if (SURAH_PAGE_MAP[i].startPage <= page) {
                    result = SURAH_PAGE_MAP[i];
                } else {
                    break;
                }
            }
            return result;
        }

        function renderMushafPage(pageNum) {
            const container = document.getElementById('quran-ayahs-container');
            const loading   = document.getElementById('quran-reader-loading');

            if (!container) return;

            loading?.classList.add('active');
            container.style.display = 'none';
            container.innerHTML = '';

            if (pageNum < 1 || pageNum > 604) return;

            const pageUrl = `https://quran.ksu.edu.sa/png_big/${pageNum}.png`;

            container.innerHTML = `
                <div class="mushaf-page-wrap">
                    <img
                        class="mushaf-page-img"
                        src="${pageUrl}"
                        alt="صفحة ${pageNum} من المصحف الشريف"
                        onload="onMushafPageLoaded()"
                        onerror="onMushafPageError(${pageNum})"
                        draggable="false"
                    />
                </div>`;

            setTimeout(() => {
                loading?.classList.remove('active');
                container.style.display = 'block';
                applyMushafZoom();
            }, 200);
        }

        function onMushafPageLoaded() {
            const loading = document.getElementById('quran-reader-loading');
            loading?.classList.remove('active');
        }

        function onMushafPageError(pageNum) {
            const loading = document.getElementById('quran-reader-loading');
            loading?.classList.remove('active');

            const container = document.getElementById('quran-ayahs-container');
            if (container) {
                container.innerHTML = `
                    <div class="ayahs-error">
                        <i class="fas fa-exclamation-circle"></i>
                        <p>تعذّر تحميل صفحة ${pageNum}</p>
                        <p style="font-size:0.85rem;margin-top:6px;">يرجى التحقق من اتصال الإنترنت</p>
                        <button class="btn-primary" style="margin-top:16px;" onclick="renderMushafPage(${pageNum})">
                            <i class="fas fa-redo"></i> إعادة المحاولة
                        </button>
                    </div>`;
                container.style.display = 'block';
            }
        }

        function goToPrevPage() {
            if (currentPage > 1) {
                currentPage--;
                updateReaderHeader();
                renderMushafPage(currentPage);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        function goToNextPage() {
            if (currentPage < 604) {
                currentPage++;
                updateReaderHeader();
                renderMushafPage(currentPage);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        document.addEventListener('keydown', function(e) {
            const readerView = document.getElementById('quran-reader-view');
            if (!readerView || readerView.style.display === 'none') return;
            if (e.key === 'ArrowLeft'  || e.key === 'ArrowDown')  goToNextPage();
            if (e.key === 'ArrowRight' || e.key === 'ArrowUp')    goToPrevPage();
        });

        function jumpToPage() {
            const input = document.getElementById('page-jump-input');
            if (!input) return;

            const pageNum = parseInt(input.value);
            
            if (!pageNum || pageNum < 1 || pageNum > 604) {
                Swal.fire({
                    icon: 'warning',
                    title: 'رقم صفحة غير صحيح',
                    text: 'يرجى إدخال رقم صفحة بين 1 و 604',
                    confirmButtonText: 'حسناً',
                    confirmButtonColor: '#1a6b3c'
                });
                return;
            }

            const surahInfo = getSurahByPage(pageNum);
            
            openPageViewer(pageNum, surahInfo);
            input.value = '';
        }

        function jumpToPageFromReader() {
            const input = document.getElementById('page-jump-reader-input');
            if (!input) return;

            const pageNum = parseInt(input.value);
            
            if (!pageNum || pageNum < 1 || pageNum > 604) {
                Swal.fire({
                    icon: 'warning',
                    title: 'رقم صفحة غير صحيح',
                    text: 'يرجى إدخال رقم صفحة بين 1 و 604',
                    confirmButtonText: 'حسناً',
                    confirmButtonColor: '#1a6b3c'
                });
                return;
            }

            currentPage = pageNum;
            updateReaderHeader();
            renderMushafPage(currentPage);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            input.value = '';
        }

        function changeMushafZoom(delta) {
            mushafZoom = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, mushafZoom + delta));
            applyMushafZoom();
        }

        function resetMushafZoom() {
            mushafZoom = 100;
            applyMushafZoom();
        }

        function applyMushafZoom() {
            const img   = document.querySelector('.mushaf-page-img');
            const label = document.getElementById('zoom-label');
            const zoomIn  = document.getElementById('zoom-in-btn');
            const zoomOut = document.getElementById('zoom-out-btn');

            if (img) img.style.width = mushafZoom + '%';
            if (label) label.textContent = mushafZoom + '%';

            if (zoomIn)  zoomIn.disabled  = mushafZoom >= ZOOM_MAX;
            if (zoomOut) zoomOut.disabled = mushafZoom <= ZOOM_MIN;
        }

        function initPinchZoom() {
            let startDist = 0;
            let startZoom = mushafZoom;

            document.addEventListener('touchstart', function(e) {
                if (e.touches.length === 2) {
                    const dx = e.touches[0].clientX - e.touches[1].clientX;
                    const dy = e.touches[0].clientY - e.touches[1].clientY;
                    startDist = Math.hypot(dx, dy);
                    startZoom = mushafZoom;
                }
            }, { passive: true });

            document.addEventListener('touchmove', function(e) {
                const rv = document.getElementById('quran-reader-view');
                if (!rv || rv.style.display === 'none') return;
                if (e.touches.length !== 2) return;
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                const ratio = Math.hypot(dx, dy) / startDist;
                mushafZoom = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, Math.round(startZoom * ratio)));
                applyMushafZoom();
            }, { passive: true });
        }

        // تصدير للعالمي
        window.showReciterSuras    = showReciterSuras;
        window.goBackToReciters    = goBackToReciters;
        window.playSuraForReciter  = playSuraForReciter;
        window.showRiwayahSuras    = showRiwayahSuras;
        window.goBackToRiwayat     = goBackToRiwayat;
        window.playSuraForRiwayah  = playSuraForRiwayah;
        window.showTafsirContent   = showTafsirContent;
        window.goBackToTafsir      = goBackToTafsir;
        window.getTafsirContent    = getTafsirContent;
        window.playRadioStation    = playRadioStation;
        window.loadSurahForReading = loadSurahForReading;
        window.jumpToPage          = jumpToPage;
        window.jumpToPageFromReader = jumpToPageFromReader;
        window.showSurahSelector   = showSurahSelector;
        window.goToPrevPage         = goToPrevPage;
        window.goToNextPage         = goToNextPage;
        window.onMushafPageLoaded   = onMushafPageLoaded;
        window.onMushafPageError    = onMushafPageError;
        window.renderMushafPage     = renderMushafPage;

    </script>
</body>
</html>
"""

# =====================================================
#  بيانات الأذكار المحلية (احتياطي)
# =====================================================
AZKAR_DATA = {
    "morning": [
        {"zekr": "أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير", "count": "1"},
        {"zekr": "اللهم بك أصبحنا، وبك أمسينا، وبك نحيا، وبك نموت، وإليك النشور", "count": "1"},
        {"zekr": "اللهم ما أصبح بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر", "count": "1"},
        {"zekr": "اللهم عافني في بدني، اللهم عافني في سمعي، اللهم عافني في بصري، لا إله إلا أنت", "count": "3"},
        {"zekr": "حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم", "count": "7"}
    ],
    "evening": [
        {"zekr": "أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير", "count": "1"},
        {"zekr": "اللهم بك أمسينا، وبك أصبحنا، وبك نحيا، وبك نموت، وإليك المصير", "count": "1"},
        {"zekr": "أعوذ بكلمات الله التامات من شر ما خلق", "count": "3"},
        {"zekr": "اللهم إني أسألك العفو والعافية في الدنيا والآخرة", "count": "1"}
    ],
    "sleep": [
        {"zekr": "باسمك اللهم أموت وأحيا", "count": "1"},
        {"zekr": "اللهم قني عذابك يوم تبعث عبادك", "count": "3"},
        {"zekr": "سبحان الله (33)، الحمد لله (33)، الله أكبر (34)", "count": "100"},
        {"zekr": "آية الكرسي: اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...", "count": "1"}
    ],
    "waking": [
        {"zekr": "الحمد لله الذي أحيانا بعد ما أماتنا وإليه النشور", "count": "1"},
        {"zekr": "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير", "count": "1"},
        {"zekr": "الحمد لله الذي عافاني في جسدي، ورد علي روحي، وأذن لي بذكره", "count": "1"}
    ],
    "prayer": [
        {"zekr": "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه", "count": "3"},
        {"zekr": "اللهم أنت السلام ومنك السلام تباركت يا ذا الجلال والإكرام", "count": "1"},
        {"zekr": "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد، وهو على كل شيء قدير", "count": "1"},
        {"zekr": "سبحان الله (33)، الحمد لله (33)، الله أكبر (33)، لا إله إلا الله وحده لا شريك له", "count": "100"}
    ]
}

# =====================================================
#  بيانات الإذاعات المحلية
# =====================================================
RADIO_STATIONS = [
    {"id":1,  "name":"إذاعة أبو بكر الشاطري",           "url":"https://backup.qurango.net/radio/shaik_abu_bakr_al_shatri",          "img":"https://i1.sndcdn.com/artworks-000663801097-wb0y31-t200x200.jpg"},
    {"id":2,  "name":"إذاعة أحمد خضر الطرابلسي",         "url":"https://backup.qurango.net/radio/ahmad_khader_altarabulsi",           "img":"https://i.pinimg.com/564x/d3/c2/9c/d3c29cc03198c3c15d380af048b2d68b.jpg"},
    {"id":3,  "name":"إذاعة إبراهيم الأخضر",             "url":"https://backup.qurango.net/radio/ibrahim_alakdar",                    "img":"https://static.suratmp3.com/pics/reciters/thumbs/44_600_600.jpg"},
    {"id":4,  "name":"إذاعة خالد الجليل",                "url":"https://backup.qurango.net/radio/khalid_aljileel",                    "img":"https://i1.sndcdn.com/avatars-ubX3f7yLm5eGyphJ-A4ysyA-t500x500.jpg"},
    {"id":5,  "name":"إذاعة صلاح الهاشم",               "url":"https://backup.qurango.net/radio/salah_alhashim",                     "img":"https://i.pinimg.com/564x/e9/22/1b/e9221b5ffd484937dc70c3eabe350c6f.jpg"},
    {"id":6,  "name":"إذاعة صلاح بو خاطر",              "url":"https://backup.qurango.net/radio/slaah_bukhatir",                     "img":"https://pbs.twimg.com/profile_images/1306502829251624960/uHKIJQpq_200x200.jpg"},
    {"id":7,  "name":"إذاعة عبدالباسط عبدالصمد",        "url":"https://backup.qurango.net/radio/abdulbasit_abdulsamad_mojawwad",      "img":"https://cdns-images.dzcdn.net/images/talk/06b711ac6da4cde0eb698e244f5e27b8/300x300.jpg"},
    {"id":8,  "name":"إذاعة عبد العزيز سحيم",           "url":"https://backup.qurango.net/radio/a_sheim",                            "img":"https://i.pinimg.com/564x/a7/37/47/a73747375897de4897da372a0fd921a0.jpg"},
    {"id":9,  "name":"إذاعة فارس عباد",                  "url":"https://backup.qurango.net/radio/fares_abbad",                        "img":"https://static.suratmp3.com/pics/reciters/thumbs/15_600_600.jpg"},
    {"id":10, "name":"إذاعة ماهر المعيقلي",              "url":"https://backup.qurango.net/radio/maher",                              "img":"https://is1-ssl.mzstatic.com/image/thumb/Podcasts113/v4/4b/80/58/4b80582d-78ca-a466-0341-0869bc611745/mza_5280524847349008894.jpg/250x250bb.jpg"},
    {"id":11, "name":"إذاعة محمد صديق المنشاوي",         "url":"https://backup.qurango.net/radio/mohammed_siddiq_alminshawi_mojawwad","img":"https://i1.sndcdn.com/artworks-000284633237-7gdg9t-t200x200.jpg"},
    {"id":12, "name":"إذاعة محمود خليل الحصري",          "url":"https://backup.qurango.net/radio/mahmoud_khalil_alhussary_mojawwad",  "img":"https://watanimg.elwatannews.com/image_archive/original_lower_quality/18194265071637693809.jpg"},
    {"id":13, "name":"إذاعة محمود علي البنا",             "url":"https://backup.qurango.net/radio/mahmoud_ali__albanna_mojawwad",      "img":"https://i.pinimg.com/200x/29/67/b3/2967b3fbc1ce1f5a70874288d34317bf.jpg"},
    {"id":14, "name":"إذاعة مشاري العفاسي",              "url":"https://backup.qurango.net/radio/mishary_alafasi",                    "img":"https://i1.sndcdn.com/artworks-000019055020-yr9cjc-t200x200.jpg"},
    {"id":15, "name":"إذاعة ناصر القطامي",               "url":"https://backup.qurango.net/radio/nasser_alqatami",                    "img":"https://i1.sndcdn.com/artworks-000096282703-s9wldh-t200x200.jpg"},
    {"id":16, "name":"إذاعة نبيل الرفاعي",               "url":"https://backup.qurango.net/radio/nabil_al_rifay",                     "img":"https://i1.sndcdn.com/artworks-000161140408-wh6nhw-t200x200.jpg"},
    {"id":17, "name":"إذاعة هيثم الجدعاني",              "url":"https://backup.qurango.net/radio/hitham_aljadani",                    "img":"https://ar.islamway.net/uploads/authors/3948.jpg"},
    {"id":18, "name":"إذاعة ياسر الدوسري",               "url":"https://backup.qurango.net/radio/yasser_aldosari",                    "img":"https://www.almowaten.net/wp-content/uploads/2022/06/%D9%8A%D8%A7%D8%B3%D8%B1-%D8%A7%D9%84%D8%AF%D9%88%D8%B3%D8%B1%D9%8A.jpg"},
    {"id":19, "name":"إذاعة القرآن الكريم من القاهرة",   "url":"https://n0e.radiojar.com/8s5u5tpdtwzuv?rj-ttl=5&rj-tok=AAABjW7yROAA0TUU8cXhXIAi6g", "img":"https://apkdownmod.com/thumbnail?src=images/appsicon/2020/08/app-image-5f42ba68a61b1.jpg", "country":"مصر"},
    {"id":20, "name":"إذاعة السنة النبوية",               "url":"https://n01.radiojar.com/x0vs2vzy6k0uv?rj-ttl=5&rj-tok=AAABjW751GcA4NgCI8-5DCpCHQ",  "img":"https://i.pinimg.com/564x/55/16/ab/5516abd3744c3d0b0a7b28bedd5474c0.jpg"},
    {"id":21, "name":"إذاعة تلاوات خاشعة",               "url":"https://backup.qurango.net/radio/salma",                              "img":"https://pbs.twimg.com/profile_images/1396812808659079169/5ft2haLD_400x400.jpg"},
    {"id":22, "name":"إذاعة الرقية الشرعية",              "url":"https://backup.qurango.net/radio/roqiah",                             "img":"https://i1.sndcdn.com/artworks-zygACgAd2NKwuohE-UF2Piw-t500x500.jpg"},
    {"id":23, "name":"إذاعة تكبيرات العيد",               "url":"https://backup.qurango.net/radio/eid",                                "img":"https://i.pinimg.com/736x/3c/b3/fc/3cb3fc494b9f8332a7b7b3256e3d9822.jpg"},
    {"id":24, "name":"المختصر في تفسير القرآن",           "url":"https://backup.qurango.net/radio/mukhtasartafsir",                    "img":"https://areejquran.net/wp-content/uploads/2015/12/unnamed.jpg"},
    {"id":25, "name":"إذاعة توفيق المبايع",               "url":"https://backup.qurango.net/radio/tawfeeq_almubayeh",                  "img":""},
    {"id":26, "name":"إذاعة القرآن الكريم من الرياض",    "url":"https://qurango.net/radio", "country":"السعودية", "img":"https://apkdownmod.com/thumbnail?src=images/appsicon/2020/08/app-image-5f42ba68a61b1.jpg"},
    {"id":27, "name":"إذاعة القرآن الكريم من مكة",       "url":"https://qurango.net/radio", "country":"السعودية", "img":"https://apkdownmod.com/thumbnail?src=images/appsicon/2020/08/app-image-5f42ba68a61b1.jpg"},
    {"id":28, "name":"إذاعة القرآن الكريم من دبي",       "url":"https://qurango.net/radio", "country":"الإمارات", "img":"https://apkdownmod.com/thumbnail?src=images/appsicon/2020/08/app-image-5f42ba68a61b1.jpg"}
]

# =====================================================
#  دوال مساعدة للـ API
# =====================================================

def load_hadith_data(book):
    """تحميل بيانات الحديث من الملفات المحلية"""
    try:
        if book == 'bukhari':
            # استخدام بيانات تجريبية للبخاري
            return {
                "hadiths": [
                    {"arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ", "translation": "إنما الأعمال بالنيات", "explanation": "أي صحة الأعمال وقبولها عند الله تكون بالنية"},
                    {"arabic": "بُنِيَ الإِسْلاَمُ عَلَى خَمْسٍ", "translation": "بني الإسلام على خمس", "explanation": "شهادة أن لا إله إلا الله وأن محمداً رسول الله، وإقام الصلاة، وإيتاء الزكاة، وصوم رمضان، وحج البيت"}
                ]
            }
        else:
            # بيانات تجريبية لمسلم
            return {
                "hadiths": [
                    {"arabic": "الطُّهُورُ شَطْرُ الإِيمَانِ", "translation": "الطهور شطر الإيمان", "explanation": "أي نصف الإيمان أو جزء عظيم منه"},
                    {"arabic": "لاَ يَدْخُلُ الْجَنَّةَ مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ ذَرَّةٍ مِنْ كِبْرٍ", "translation": "لا يدخل الجنة من كان في قلبه مثقال ذرة من كبر", "explanation": "أي لا يدخلها مع الكافرين بل مع المؤمنين بعد تطهيره"}
                ]
            }
    except Exception as e:
        print(f"Error loading hadith: {e}")
        return None

# =====================================================
#  مسارات Flask
# =====================================================

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(
        TEMPLATE,
        surahs=json.dumps(ALL_SURAHS, ensure_ascii=False),
        surah_page_map=json.dumps(SURAH_PAGE_MAP, ensure_ascii=False)
    )

@app.route('/api/hadith/<book>')
def get_hadith(book):
    """API لجلب الأحاديث"""
    if book not in ['bukhari', 'muslim']:
        return jsonify({"error": "Invalid book"}), 400
    
    data = load_hadith_data(book)
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to load hadith"}), 500

@app.route('/api/azkar')
def get_azkar():
    """API لجلب الأذكار"""
    return jsonify(AZKAR_DATA)

@app.route('/api/radio-stations')
def get_radio_stations():
    """API لجلب الإذاعات"""
    return jsonify(RADIO_STATIONS)

@app.route('/api/proxy/tafsir')
def proxy_tafsir():
    """بروكسي لجلب التفسير من API خارجي"""
    url = request.args.get('url')
    surah = request.args.get('surah')
    
    if not url or not surah:
        return jsonify({"error": "Missing parameters"}), 400
    
    try:
        # محاكاة بيانات التفسير
        return jsonify({
            "tafsir": [
                {"text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "tafsir": "أبدأ قراءتي مستعيناً باسم الله"},
                {"text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "tafsir": "الثناء الكامل لله رب الخلائق أجمعين"}
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """تقديم الملفات الثابتة (إذا احتجناها)"""
    return send_file(filename), 200

# =====================================================
#  تشغيل التطبيق
# =====================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
