import { getMessages } from './store.js';

export default function handler(req, res) {
  const { device = 'kobo' } = req.query;
  const messages = getMessages().slice(-20);

  const buttons = `
    <button onclick="send('OK')">OK</button>
    <button onclick="send('Yes')">Yes</button>
    <button onclick="send('No')">No</button>
    <button onclick="send('Wait')">Wait</button>
    <button onclick="send('Coming')">Coming</button>
  `;

  res.setHeader('Content-Type', 'text/html');
  res.send(`
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="5">
<style>
body { font-family: sans-serif; font-size: 18px; }
button { display:block; width:100%; margin:6px 0; padding:12px; }
.box { border:1px solid black; padding:8px; height:200px; overflow:hidden; }
</style>
</head>
<body>
<h2>${device} chat</h2>
<div class="box">
${messages.map(m => `<div><b>${m.sender}</b>: ${m.text}</div>`).join('')}
</div>
${device === 'kindle' ? buttons : ''}

${device === 'kobo' ? `
<form onsubmit="sendInput(); return false;">
<input id="msg" style="width:100%" />
</form>
` : ''}

<script>
async function send(text) {
  await fetch('/api/send', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ sender: '${device}', text })
  });
}

async function sendInput() {
  const val = document.getElementById('msg').value;
  send(val);
}
</script>
</body>
</html>
  `);
}
