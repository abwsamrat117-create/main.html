import requests
import random
import json
import urllib3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# تجاهل تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== البروكسيات ==========
PROXIES_LIST = [
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_64082810_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_34335906_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_73076803_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_14455579_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_94476934_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_85567572_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_33914658_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_05078606_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_63400946_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_97298946_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_51982495_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_88605594_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_61251022_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_97312243_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_97983961_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_35211286_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_65108334_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_80090805_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_32311854_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_51678723_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_48908140_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_74940139_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_05204714_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_76244912_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_26287028_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_41259412_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_00070648_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_03581255_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_61327937_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_02892722_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_92981670_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_70540079_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_51018069_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_42258610_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_43170495_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_15803801_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_13528957_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_82699728_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_17349714_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_43846256_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_73852436_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_92243984_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_75861945_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_11967029_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_62024505_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_40292392_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_31864004_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_23771748_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_15015348_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_47256396_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_57722101_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_01815954_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_86982350_time_5:5108733@change4.owlproxy.com:7778",
    "http://jmeJorI4AM80_custom_zone_EG_st__city_sid_86130932_time_5:5108733@change4.owlproxy.com:7778",
]

class ProxyRotator:
    def __init__(self):
        self.proxies = PROXIES_LIST.copy()
        self.available = PROXIES_LIST.copy()
        self.used = []
    
    def get_new(self):
        if not self.available:
            self.available = self.proxies.copy()
            self.used = []
            random.shuffle(self.available)
        proxy = self.available.pop(0)
        self.used.append(proxy)
        return {"http": proxy, "https": proxy}

rotator = ProxyRotator()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/proxy':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            url = data.get('url')
            method = data.get('method', 'GET')
            headers = data.get('headers', {})
            body = data.get('body')
            
            proxies = rotator.get_new()
            print(f"\n📍 بروكسي: {proxies['http'][:60]}...")
            print(f"📤 URL: {url}")
            
            try:
                request_kwargs = {
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'proxies': proxies,
                    'timeout': 30,
                    'verify': False
                }
                if method in ['POST', 'PUT', 'PATCH']:
                    request_kwargs['json'] = body
                
                response = requests.request(**request_kwargs)
                
                try:
                    response_data = response.json()
                except:
                    response_data = {'text': response.text}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': response.status_code,
                    'data': response_data
                }).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 500,
                    'data': {'message': str(e)}
                }).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # صفحة HTML المضمنة
            html = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إرسال كود OTP</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #0f111a; color: #e0e0e0; }
        .card { background: #1a1d2e; padding: 30px; border-radius: 16px; width: 100%; max-width: 400px; text-align: center; border: 1px solid #2a2f42; }
        h1 { margin: 0 0 20px; font-size: 22px; background: linear-gradient(135deg, #c9a84c, #f0d080); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .input-group { margin: 20px 0; }
        input { width: 100%; padding: 14px; border-radius: 10px; border: 1px solid #2a2f42; background: #0f111a; color: #e0e0e0; font-size: 18px; text-align: center; }
        input:focus { outline: none; border-color: #c9a84c; }
        button { width: 100%; padding: 14px; border: none; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; background: linear-gradient(135deg, #c9a84c, #f0d080); color: #0f111a; margin-top: 10px; }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        #response { margin-top: 15px; padding: 12px; border-radius: 8px; display: none; font-weight: 700; }
        #response.success { display: block; background: rgba(45,212,164,0.1); border: 1px solid #2dd4a4; color: #2dd4a4; }
        #response.error { display: block; background: rgba(240,92,92,0.1); border: 1px solid #f05c5c; color: #f05c5c; }
        #loading { display: none; margin: 10px auto; width: 20px; height: 20px; border: 3px solid #2a2f42; border-top-color: #c9a84c; border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .status { margin-top: 10px; font-size: 14px; color: #7a8099; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📱 إرسال كود OTP</h1>
        <div class="input-group">
            <input type="tel" id="phone" placeholder="أدخل رقم الهاتف" maxlength="11">
        </div>
        <button id="sendBtn" onclick="sendOTP()">📨 إرسال رمز التحقق</button>
        <div id="loading"></div>
        <div id="response"></div>
        <div class="status" id="status">✅ جاهز</div>
    </div>

    <script>
        const PROXY_SERVER = '/proxy';
        const API_BASE = 'https://api.twistmena.com/music';

        function format_phone(phone) {
            let p = phone.replace(/[^0-9]/g, '');
            if (p.startsWith('01')) return '2' + p;
            if (p.startsWith('1')) return '20' + p;
            return p;
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('sendBtn').disabled = true;
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('sendBtn').disabled = false;
        }

        function showResponse(text, type) {
            const el = document.getElementById('response');
            el.className = type;
            el.textContent = text;
            el.style.display = 'block';
        }

        function updateStatus(text) {
            document.getElementById('status').textContent = text;
        }

        async function sendOTP() {
            const phoneInput = document.getElementById('phone').value.trim();
            if (!phoneInput || phoneInput.length < 10) {
                showResponse('❌ يرجى إدخال رقم صحيح', 'error');
                return;
            }

            const formatted = format_phone(phoneInput);
            showLoading();
            updateStatus('📨 جاري الإرسال...');
            showResponse('', '');

            const headers = {
                'User-Agent': 'Twist-Mobile/11.2.10 (Android; 14; SM-A235F; music; en-GB)',
                'app_version': '11.2.10',
                'appversion': '11.2.10',
                'channel': 'mobileapp',
                'content-type': 'application/json',
                'platform': 'android',
                'accept': 'application/json',
                'accept-language': 'en',
                'host': 'api.twistmena.com',
                'device_id': 'UP1A.231005.' + Math.floor(Math.random() * 999),
                'sessionid': Math.floor(Math.random() * 99999999) + '-' +
                              Math.floor(Math.random() * 9999) + '-' +
                              Math.floor(Math.random() * 9999) + '-' +
                              Math.floor(Math.random() * 9999) + '-' +
                              Math.floor(Math.random() * 999999999999),
                'X-Forwarded-For': '156.201.43.252',
                'X-Real-IP': '156.201.43.252',
                'customer-ip': '156.201.43.252'
            };

            const payload = {
                url: `${API_BASE}/Dlogin/sendCode`,
                method: 'POST',
                headers: headers,
                body: { dial: formatted }
            };

            try {
                const response = await fetch(PROXY_SERVER, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                hideLoading();

                if (result.status === 200) {
                    const data = result.data;
                    let success = false;
                    let message = '';

                    if (data && data.responseHeader) {
                        if (data.responseHeader.status === 'SUCCESS' || data.responseHeader.status === 'Success') {
                            success = true;
                            message = data.responseHeader.message || 'تم إرسال الكود بنجاح';
                        } else {
                            message = data.responseHeader.message || 'فشل في السيرفر';
                        }
                    } else if (data && data.firstTimeLogin !== undefined) {
                        success = true;
                        message = 'تم إرسال الكود بنجاح';
                    }

                    if (success) {
                        showResponse(`✅ ${message}`, 'success');
                        updateStatus('📱 تحقق من هاتفك');
                    } else {
                        showResponse(`❌ ${message}`, 'error');
                        updateStatus('⚠️ فشل الإرسال');
                    }
                } else {
                    const msg = result.data?.message || `خطأ ${result.status}`;
                    showResponse(`❌ ${msg}`, 'error');
                    updateStatus('⚠️ فشل الإرسال');
                }

            } catch (error) {
                hideLoading();
                showResponse('❌ خطأ في الاتصال', 'error');
                updateStatus('⚠️ خطأ في الشبكة');
            }
        }
    </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

# تشغيل الخادم
if __name__ == '__main__':
    PORT = 5000
    print("=" * 50)
    print(f"🚀 بوت يعمل على http://localhost:{PORT}")
    print(f"📡 إجمالي البروكسيات: {len(PROXIES_LIST)}")
    print("=" * 50)
    print("📌 افتح المتصفح على http://localhost:5000")
    print("=" * 50)
    server = HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    server.serve_forever()
