# Launch Checklist

## 1. Test backend locally

```bash
cd cmu-sidequest-hw4-mvp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000/health
```

Then in another terminal:

```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"time":3,"distance":10,"budget":"free","group":"friends"}'
```

## 2. Create public GitHub backend repo

Create a new public repository, for example:

```text
cmu-sidequest-backend
```

Then from this folder:

```bash
git init
git add .
git commit -m "Build Sidequest backend MVP"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

## 3. Deploy backend on Render

Create a new Web Service connected to the backend repo.

Use:

```text
Build: pip install -r requirements.txt
Start: gunicorn app:app
```

After deployment, visit:

```text
https://YOUR-RENDER-SERVICE.onrender.com/health
```

## 4. Connect frontend

Open `frontend-demo/script.js`.

Change:

```js
const BACKEND_URL = "https://YOUR-RENDER-SERVICE.onrender.com";
```

to the actual Render URL.

Then copy the demo logic into your existing Sidequest / portfolio frontend, or temporarily publish the provided demo page in your frontend GitHub Pages repo.

## 5. Test error handling

Try:

- a valid recommendation
- backend URL typo / backend unavailable
- a request with values that produce no matches
- direct curl request missing a field

## 6. Before submitting

Verify:

- Render URL works
- GitHub backend repo is public
- GitHub frontend is public and deployed
- README is present
- prompt log is present
- video link works in incognito
- Google Form is submitted
