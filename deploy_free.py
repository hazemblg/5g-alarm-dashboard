"""
🆓 FREE DEPLOYMENT ASSISTANT
Deploy your 5G Alarm Dashboard for FREE!
No Google Play Store fee required.
"""

import os
import socket
import subprocess
import webbrowser
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(number, text):
    print(f"\n{'='*60}")
    print(f"  STEP {number}: {text}")
    print(f"{'='*60}\n")

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def create_github_guide():
    """Create guide for GitHub deployment"""
    guide = """
# 🆓 FREE DEPLOYMENT GUIDE
## Deploy to Streamlit Cloud (15 minutes)

---

## STEP 1: Create GitHub Account

1. Go to https://github.com
2. Click "Sign up"
3. Create free account
4. Verify email

---

## STEP 2: Create Repository

### Option A: Using GitHub Website (Easiest)

1. Go to https://github.com/new
2. Repository name: `5g-alarm-dashboard`
3. Description: "Professional 5G Network Alarm Monitoring"
4. Public (FREE unlimited)
5. Click "Create repository"

### Option B: Using Git (Command Line)

```bash
cd C:\\Users\\t14\\PycharmProjects\\5g-alarm-dashbord

# Initialize git
git init

# Add files
git add main.py manifest.json service-worker.js requirements.txt

# Commit
git commit -m "Initial commit - DRS 5G Alarm Dashboard"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/5g-alarm-dashboard.git

# Push
git branch -M main
git push -u origin main
```

---

## STEP 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io

2. Click **"Sign up"** (use your GitHub account)

3. Click **"New app"**

4. Configure:
   - **Repository**: YOUR_USERNAME/5g-alarm-dashboard
   - **Branch**: main
   - **Main file path**: main.py

5. Advanced settings (optional):
   - Python version: 3.9+
   - Leave other settings default

6. Click **"Deploy!"**

7. Wait 2-5 minutes for deployment

8. ✅ **Your app is live!**

---

## STEP 4: Get Your App URL

Your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

Or custom subdomain:
```
https://5g-alarm-dashboard-YOUR_USERNAME.streamlit.app
```

---

## STEP 5: Share with Users

### Share URL via:
- Email
- WhatsApp
- SMS
- QR Code (already created)
- Company intranet

### Installation Instructions for Users:

**Android:**
1. Open Chrome
2. Visit: https://your-app.streamlit.app
3. Tap menu (⋮) → "Add to Home Screen"
4. Tap "Add"
5. ✅ App icon on home screen!

**iPhone:**
1. Open Safari
2. Visit: https://your-app.streamlit.app
3. Tap Share (📤) → "Add to Home Screen"
4. Tap "Add"
5. ✅ App icon on home screen!

---

## TROUBLESHOOTING

### "Module not found" error
✅ Solution: Check requirements.txt has all dependencies

### "File not found: alarms.xlsx"
✅ Solution: Either:
   - Add sample data to repository
   - Modify code to load from URL
   - Add file upload feature

### "Build failed"
✅ Solution: Check logs, usually missing dependency

---

## ⚠️ IMPORTANT: DATA FILE

Your app loads data from local Excel file. For cloud deployment:

### Option 1: Include Sample Data
```bash
git add alarms.xlsx
git commit -m "Add sample data"
git push
```

### Option 2: Use File Uploader
Add to main.py:
```python
uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Please upload alarm data file")
```

### Option 3: Load from Cloud Storage
```python
import requests
url = "https://your-storage.com/alarms.xlsx"
df = pd.read_excel(requests.get(url).content)
```

---

## 🎉 DONE!

Your app is now:
- ✅ Hosted on Streamlit Cloud (FREE)
- ✅ Accessible worldwide
- ✅ Installable as PWA
- ✅ Auto-updates when you push to GitHub
- ✅ HTTPS enabled
- ✅ No fees!

**Cost: $0** 💰
"""

    Path("STREAMLIT_CLOUD_GUIDE.md").write_text(guide, encoding='utf-8')
    print("✅ Created: STREAMLIT_CLOUD_GUIDE.md")

def create_download_page():
    """Create HTML download page"""
    local_ip = get_local_ip()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DRS 5G Alarm Management - Install</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0e1117, #1e293b, #0e1117);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .container {{
            max-width: 700px;
            width: 100%;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        
        .logo {{
            font-size: 64px;
            text-align: center;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        
        h1 {{
            background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 36px;
            text-align: center;
            margin-bottom: 10px;
            font-weight: 800;
        }}
        
        .subtitle {{
            text-align: center;
            color: #94a3b8;
            margin-bottom: 40px;
            font-size: 18px;
        }}
        
        .section {{
            margin: 30px 0;
        }}
        
        .section h2 {{
            color: #3b82f6;
            font-size: 24px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .section h2::before {{
            content: "▸";
            margin-right: 10px;
        }}
        
        .buttons {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin: 20px 0;
        }}
        
        .btn {{
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            border: none;
            padding: 18px 30px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
        }}
        
        .btn-secondary {{
            background: linear-gradient(135deg, #059669, #10b981);
        }}
        
        .qr-container {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 16px;
            margin: 20px 0;
        }}
        
        .features {{
            list-style: none;
            margin: 20px 0;
        }}
        
        .features li {{
            padding: 12px 0;
            display: flex;
            align-items: center;
            color: #cbd5e1;
        }}
        
        .features li::before {{
            content: "✓";
            color: #10b981;
            font-weight: bold;
            font-size: 20px;
            margin-right: 12px;
        }}
        
        .instructions {{
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .instructions h3 {{
            color: #3b82f6;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        
        .instructions ol {{
            color: #cbd5e1;
            margin-left: 20px;
        }}
        
        .instructions ol li {{
            margin: 8px 0;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(148, 163, 184, 0.2);
            color: #64748b;
            font-size: 14px;
        }}
        
        @media (max-width: 600px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 28px;
            }}
            
            .btn {{
                font-size: 16px;
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🚨</div>
        <h1>DRS 5G Alarm Management</h1>
        <p class="subtitle">Professional Network Monitoring Dashboard</p>
        
        <div class="section">
            <h2>📱 Install on Your Device</h2>
            <div class="buttons">
                <a href="http://{local_ip}:8502" class="btn" target="_blank">
                    🌐 Open Web App
                </a>
                <button class="btn btn-secondary" onclick="showInstructions()">
                    📥 Installation Guide
                </button>
            </div>
        </div>
        
        <div class="qr-container">
            <p style="color: #1e293b; font-weight: 600; margin-bottom: 10px;">
                Scan QR Code to Install
            </p>
            <img src="dashboard_qr_code.png" alt="QR Code" style="max-width: 250px;">
        </div>
        
        <div class="section">
            <h2>✨ Features</h2>
            <ul class="features">
                <li>4 Specialized Dashboards (Management, Radio, FH, Energy)</li>
                <li>Real-time Alarm Monitoring & Analysis</li>
                <li>Interactive Data Visualizations</li>
                <li>KPI Tracking (MTTR, Availability)</li>
                <li>Mobile-Responsive Design</li>
                <li>Offline Support (PWA)</li>
                <li>Professional Dark Theme for 24/7 Operations</li>
            </ul>
        </div>
        
        <div class="instructions" id="androidInstructions" style="display: none;">
            <h3>📱 Android Installation</h3>
            <ol>
                <li>Open the web app link in <strong>Chrome</strong></li>
                <li>Tap the menu icon (⋮) in the top right</li>
                <li>Select <strong>"Add to Home screen"</strong></li>
                <li>Tap <strong>"Add"</strong></li>
                <li>✅ The app icon will appear on your home screen!</li>
            </ol>
        </div>
        
        <div class="instructions" id="iosInstructions" style="display: none;">
            <h3>📱 iPhone Installation</h3>
            <ol>
                <li>Open the web app link in <strong>Safari</strong></li>
                <li>Tap the Share button (📤) at the bottom</li>
                <li>Scroll down and tap <strong>"Add to Home Screen"</strong></li>
                <li>Tap <strong>"Add"</strong></li>
                <li>✅ The app icon will appear on your home screen!</li>
            </ol>
        </div>
        
        <div class="section">
            <h2>🎯 Target Users</h2>
            <p style="color: #cbd5e1; line-height: 1.6;">
                Perfect for Network Operations Center (NOC) engineers, 5G network administrators, 
                telecom support teams, network managers, and field technicians.
            </p>
        </div>
        
        <div class="footer">
            <p>🆓 100% Free | 🔒 Secure | 📱 Mobile-Optimized</p>
            <p style="margin-top: 10px;">
                DRS - Direction Réseaux et Services
            </p>
        </div>
    </div>
    
    <script>
        function showInstructions() {{
            const android = document.getElementById('androidInstructions');
            const ios = document.getElementById('iosInstructions');
            
            if (android.style.display === 'none') {{
                android.style.display = 'block';
                ios.style.display = 'block';
            }} else {{
                android.style.display = 'none';
                ios.style.display = 'none';
            }}
        }}
        
        // Detect mobile device
        if (/Android/i.test(navigator.userAgent)) {{
            document.getElementById('androidInstructions').style.display = 'block';
        }} else if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {{
            document.getElementById('iosInstructions').style.display = 'block';
        }}
    </script>
</body>
</html>
"""

    Path("download_page.html").write_text(html, encoding='utf-8')
    print("✅ Created: download_page.html")
    return local_ip

def create_short_link_guide():
    """Create guide for creating short links"""
    guide = """# 🔗 CREATE SHORT LINKS (FREE)

Make your app URL easy to share!

## FREE URL Shorteners:

### 1. Bitly (Most Popular)
- Website: https://bitly.com
- Sign up: FREE
- Create: https://bit.ly/drs-alarms
- Features: Click tracking, QR codes

### 2. TinyURL
- Website: https://tinyurl.com
- No signup needed: FREE
- Create: https://tinyurl.com/drs-alarms
- Simple and fast

### 3. Rebrandly
- Website: https://www.rebrandly.com
- Free tier: 500 links/month
- Custom domain: Yes (paid)
- Analytics: Yes

### 4. Short.io
- Website: https://short.io
- Free tier available
- Custom domains
- Advanced analytics

## How to Create:

1. Deploy your app to Streamlit Cloud
2. Copy your URL: https://your-app.streamlit.app
3. Go to bitly.com or tinyurl.com
4. Paste your URL
5. Create short link: bit.ly/drs-alarms
6. Share everywhere!

## Benefits:

✅ Easy to remember
✅ Easy to type
✅ Professional looking
✅ Track clicks
✅ QR code generation
✅ Change destination URL later

## Example Short Links:

- bit.ly/drs-5g
- tinyurl.com/drs-dashboard
- bit.ly/install-drs
- tinyurl.com/5g-alarms

## Pro Tip:

Use the same short link in:
- Emails
- SMS
- WhatsApp
- QR codes
- Business cards
- Presentations

Makes distribution super easy! 🚀
"""

    Path("SHORT_LINKS_GUIDE.md").write_text(guide, encoding='utf-8')
    print("✅ Created: SHORT_LINKS_GUIDE.md")

def main():
    print_header("🆓 FREE DEPLOYMENT ASSISTANT")

    print("This will help you deploy your 5G Alarm Dashboard for FREE!")
    print("No Google Play Store fees required.")
    print("\nCreating deployment guides...")

    # Create guides
    create_github_guide()
    local_ip = create_download_page()
    create_short_link_guide()

    print_step(1, "Files Created Successfully")
    print("✅ STREAMLIT_CLOUD_GUIDE.md - Step-by-step Streamlit Cloud deployment")
    print("✅ download_page.html - Beautiful installation page")
    print("✅ SHORT_LINKS_GUIDE.md - Create easy-to-share links")
    print("✅ FREE_DISTRIBUTION.md - Complete free distribution guide")

    print_step(2, "Current Status")
    print(f"🌐 Local URL: http://{local_ip}:8502")
    print(f"📱 Download Page: file://{os.path.abspath('download_page.html')}")
    print(f"📋 QR Code: {os.path.abspath('dashboard_qr_code.png')}")

    print_step(3, "Next Actions")
    print("Choose your deployment strategy:\n")

    print("OPTION 1: PWA Only (Easiest) ⭐")
    print("  1. Deploy to Streamlit Cloud (follow STREAMLIT_CLOUD_GUIDE.md)")
    print("  2. Share URL with users")
    print("  3. Users install as PWA from browser")
    print("  → Time: 15 minutes | Cost: FREE\n")

    print("OPTION 2: PWA + Download Page (Professional)")
    print("  1. Deploy to Streamlit Cloud")
    print("  2. Host download_page.html on GitHub Pages")
    print("  3. Share download page URL")
    print("  → Time: 30 minutes | Cost: FREE\n")

    print("OPTION 3: PWA + APK (Maximum Compatibility)")
    print("  1. Deploy to Streamlit Cloud")
    print("  2. Create APK with PWA Builder")
    print("  3. Host APK on GitHub Releases")
    print("  → Time: 1 hour | Cost: FREE\n")

    print_step(4, "Quick Start Commands")
    print("# Open guides:")
    print("notepad STREAMLIT_CLOUD_GUIDE.md")
    print("notepad FREE_DISTRIBUTION.md")
    print()
    print("# View download page:")
    print("start download_page.html")
    print()
    print("# Start local server (for testing):")
    print("streamlit run main.py --server.port 8502 --server.address 0.0.0.0")

    print_step(5, "Resources")
    print("📚 Documentation:")
    print("  • FREE_DISTRIBUTION.md - Complete free distribution guide")
    print("  • STREAMLIT_CLOUD_GUIDE.md - Cloud deployment steps")
    print("  • SHORT_LINKS_GUIDE.md - Create share links")
    print()
    print("🌐 Useful Links:")
    print("  • Streamlit Cloud: https://share.streamlit.io")
    print("  • GitHub: https://github.com")
    print("  • PWA Builder: https://www.pwabuilder.com")
    print("  • Bitly: https://bitly.com")

    print_header("✅ SETUP COMPLETE!")

    print("🎉 Everything is ready for FREE deployment!")
    print()
    print("📋 RECOMMENDED PATH:")
    print("  1. Read: STREAMLIT_CLOUD_GUIDE.md (15 min)")
    print("  2. Deploy to Streamlit Cloud (15 min)")
    print("  3. Share URL with team")
    print("  4. Users install as PWA")
    print()
    print("💰 TOTAL COST: $0")
    print("⏱️  TOTAL TIME: ~30 minutes")
    print()
    print("🚀 Start now: Open STREAMLIT_CLOUD_GUIDE.md")

    # Ask if user wants to open guides
    print("\n" + "=" * 60)
    response = input("Open deployment guides now? (y/n): ").lower()

    if response == 'y':
        try:
            os.startfile("STREAMLIT_CLOUD_GUIDE.md")
            os.startfile("FREE_DISTRIBUTION.md")
            os.startfile("download_page.html")
            print("\n✅ Guides opened!")
        except:
            print("\n📂 Please open these files manually:")
            print("  - STREAMLIT_CLOUD_GUIDE.md")
            print("  - FREE_DISTRIBUTION.md")
            print("  - download_page.html")

    print("\n🎯 You're all set to deploy for FREE! Good luck! 🚀\n")

if __name__ == "__main__":
    main()

