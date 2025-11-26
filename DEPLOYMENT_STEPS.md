# Deployment Checklist - Follow These Steps!

## ✅ STEP 1: Download Required Files

Download these files to your `protocol-improver` folder:

1. **render.yaml** - Deployment configuration
2. **.gitignore** - Files to exclude from git
3. **README.md** - Repository description

Place them in your project root (same level as `backend` and `frontend` folders).

---

## ✅ STEP 2: Initialize Git Repository

Open terminal in VS Code (or Terminal app) and navigate to your project:

```bash
cd path/to/protocol-improver

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Protocol Improver ready for deployment"
```

**✓ You should see:** "X files changed" message

---

## ✅ STEP 3: Create GitHub Repository

1. **Go to:** https://github.com/new

2. **Fill in:**
   - Repository name: `protocol-improver`
   - Description: `AI-powered laboratory protocol analyzer`
   - Make it **Public** (important for free deployment!)
   - ❌ Don't check "Add README" (we already have one)

3. **Click:** "Create repository"

4. **Copy the commands** GitHub shows you (they look like this):
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/protocol-improver.git
   git branch -M main
   git push -u origin main
   ```

5. **Paste and run them** in your terminal

**✓ You should see:** Your files uploading to GitHub

**✓ Refresh GitHub page** - you should see all your files!

---

## ✅ STEP 4: Deploy Backend on Render

### 4.1: Sign Up on Render

1. **Go to:** https://render.com
2. **Click:** "Get Started for Free"
3. **Sign up with GitHub** (easiest option)
4. **Authorize Render** to access your GitHub

### 4.2: Create Web Service

1. **Click:** "New +" button (top right)
2. **Select:** "Web Service"
3. **Click:** "Build and deploy from a Git repository" → "Next"
4. **Find your repository:** `protocol-improver`
5. **Click:** "Connect"

### 4.3: Configure Service

Fill in these settings:

- **Name:** `protocol-improver` (or choose your own)
- **Region:** Oregon (or closest to you)
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** Free

### 4.4: Add Environment Variables

**Scroll down to "Environment Variables":**

1. **Click:** "Add Environment Variable"
2. **Key:** `ANTHROPIC_API_KEY`
3. **Value:** Your actual API key (starts with `sk-ant-`)
4. **Click:** "Add"

### 4.5: Deploy!

1. **Click:** "Create Web Service" (bottom)
2. **Wait 3-5 minutes** for deployment
3. **Watch the logs** - you'll see packages installing

**✓ Success when you see:**
```
==> Your service is live 🎉
```

4. **Copy your URL:** `https://protocol-improver-xxxx.onrender.com`

---

## ✅ STEP 5: Test Your Backend

1. **Visit:** `https://your-app.onrender.com/health`

**✓ You should see:**
```json
{
  "status": "healthy",
  "api_connection": "ok"
}
```

2. **Visit:** `https://your-app.onrender.com/docs`

**✓ You should see:** FastAPI documentation page with all your endpoints

**✅ If both work, your backend is LIVE!**

---

## ✅ STEP 6: Update Frontend Configuration

Now we need to connect your frontend to the deployed backend.

### 6.1: Edit index.html

In your `frontend/index.html` file:

**Find this line** (around line 374):
```javascript
const API_URL = 'http://localhost:8000';
```

**Replace with:**
```javascript
// Production API URL
const API_URL = 'https://your-app-name.onrender.com';  // Use your actual Render URL!
```

**Example:**
```javascript
const API_URL = 'https://protocol-improver-abc123.onrender.com';
```

### 6.2: Save and Push to GitHub

```bash
# Add the changed file
git add frontend/index.html

# Commit
git commit -m "Update API URL for production deployment"

# Push to GitHub
git push
```

---

## ✅ STEP 7: Deploy Frontend on GitHub Pages

### 7.1: Enable GitHub Pages

1. **Go to your repository** on GitHub
2. **Click:** "Settings" tab
3. **Click:** "Pages" in left sidebar
4. **Under "Source":**
   - Branch: `main`
   - Folder: `/frontend`
   - **Click:** "Save"

### 7.2: Wait for Deployment

1. **Wait 1-2 minutes**
2. **Refresh the page**
3. **You'll see:** "Your site is live at https://YOUR-USERNAME.github.io/protocol-improver/"

### 7.3: Update CORS in Backend

Your backend needs to allow requests from your GitHub Pages URL.

**In your `backend/main.py`, find the CORS section:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Currently allows all
```

**Update to be more specific (optional but more secure):**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://YOUR-USERNAME.github.io",
        "http://localhost:3000",
        "*"  # You can keep this for ease during demo
    ],
```

**If you change it, push to GitHub:**
```bash
git add backend/main.py
git commit -m "Update CORS for GitHub Pages"
git push
```

Render will automatically redeploy (wait 2-3 minutes).

---

## ✅ STEP 8: Test Everything End-to-End!

1. **Visit your GitHub Pages URL:**
   ```
   https://YOUR-USERNAME.github.io/protocol-improver/
   ```

2. **You should see:** Protocol Improver interface

3. **Test the full workflow:**
   - Upload a protocol file
   - Click "Analyze Protocol"
   - Wait 20-30 seconds
   - See suggestions appear
   - Click "Generate Improved Protocol"
   - See improved text
   - Click "Download"

**✅ If all steps work - YOU'RE LIVE! 🎉**

---

## 🎯 Your URLs

After deployment, you'll have:

**Backend API:**
```
https://protocol-improver-xxxx.onrender.com
```

**API Documentation:**
```
https://protocol-improver-xxxx.onrender.com/docs
```

**Frontend App:**
```
https://YOUR-USERNAME.github.io/protocol-improver/
```

---

## 🐛 Troubleshooting

### "Failed to connect to API"

**Check:**
1. Is backend running? Visit `/health` endpoint
2. Is API_URL in index.html correct?
3. Did you push changes to GitHub?
4. Wait 2 min for GitHub Pages to update

### "422 Error when generating"

**Check:**
1. Did you update both frontend AND backend?
2. Are you using the fixed files?
3. Check Render logs for errors

### "App is slow / times out"

**Free tier sleeps after 15 min!**
- First request takes 30 sec to wake up
- Solution: Visit site 5 min before demo
- Or upgrade to $7/month for always-awake

### "Health check fails"

**Check:**
1. Is ANTHROPIC_API_KEY set in Render?
2. Check Render logs for errors
3. Try redeploying (Manual Deploy button in Render)

---

## 🎪 Demo Day Preparation

### Day Before Event:

- [ ] Test full workflow 3 times
- [ ] Prepare 2-3 sample protocols
- [ ] Time each step (upload, analyze, generate)
- [ ] Write down your Render URL
- [ ] Create QR code to your app (optional)
- [ ] Test on phone/tablet

### 30 Minutes Before Demo:

- [ ] Visit your site (wake it up if free tier)
- [ ] Test upload → analyze → generate once
- [ ] Check Claude API has credits
- [ ] Have backup laptop with local version

### During Demo:

1. "Here's a typical lab protocol with issues..."
2. Upload file (shows in ~2 sec)
3. "AI analyzes it in 20 seconds..."
4. Review specific improvements found
5. "Now generate the improved version..." (15 sec)
6. "Download ready-to-use protocol!"
7. Mention: "Works on any device, mobile too!"

---

## 💡 Pro Tips

**Share Your App:**
- Create short URL: bit.ly/your-protocol-ai
- Make QR code for easy mobile access
- Add to your slide deck

**Monitor Usage:**
- Check Render logs to see requests
- Check Claude API usage in console

**Backup Plan:**
- Have local version ready on laptop
- Record video of it working
- In case of internet issues

---

## 🎉 You're Done!

**Your app is now live and ready for your event!**

Share your URL:
```
https://YOUR-USERNAME.github.io/protocol-improver/
```

**Good luck with your demo! 🚀**

---

## 📞 Need Help?

If you get stuck on any step:
1. Note which step number
2. Copy any error messages
3. Take screenshots
4. Ask for help!

Let's get you deployed successfully! 💪
