PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS</title>
<style>
  body { font-family: sans-serif; background: #0b0f1a; color: #e8f1ff;
         text-align: center; padding: 20px; }
  h1 { color: #4fc3f7; }
  input { width: 90%; padding: 10px; margin: 6px 0; border-radius: 8px; border: none; }
  button { font-size: 20px; padding: 18px 30px; border-radius: 50%; border: none;
           background: #4fc3f7; color: #0b0f1a; margin: 20px; }
  #log { text-align: right; white-space: pre-wrap; margin-top: 20px; }
</style>
</head>
<body>
<h1>JARVIS</h1>
<input id="token" type="password" placeholder="الرمز السري (JARVIS_TOKEN)">
<br>
<button id="mic">🎤</button>
<div id="log"></div>
<script>
const tokenInput = document.getElementById("token");
tokenInput.value = localStorage.getItem("jarvis_token") || "";
tokenInput.onchange = () => localStorage.setItem("jarvis_token", tokenInput.value);

const log = document.getElementById("log");
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const rec = new SR();
rec.lang = "ar-JO";
rec.onresult = async (e) => {
  const text = e.results[0][0].transcript;
  log.textContent += "\\nأنت: " + text;
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json", "X-Token": tokenInput.value},
    body: JSON.stringify({message: text})
  });
  const data = await res.json();
  const reply = data.reply || JSON.stringify(data);
  log.textContent += "\\nJARVIS: " + reply;
  const u = new SpeechSynthesisUtterance(reply);
  u.lang = "ar-JO";
  speechSynthesis.speak(u);
};
document.getElementById("mic").onclick = () => rec.start();
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE

