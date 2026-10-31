// Runs api/quote.js (written as a Vercel function) as a small standalone server on the VPS.
// nginx proxies POST /api/quote to it. Needs Node 18+ (built-in fetch).
//
// Settings come from the environment (systemd EnvironmentFile=/etc/parawewa/quote.env):
//   PORT (default 3005), RESEND_API_KEY, QUOTE_TO, QUOTE_FROM  -- see deploy/quote.env.example

const http = require('http');
const path = require('path');
const handler = require(path.join(__dirname, '..', 'api', 'quote.js'));

const PORT = Number(process.env.PORT) || 3005;
const MAX_BODY = 16 * 1024;

const server = http.createServer((req, res) => {
  const url = (req.url || '').split('?')[0];
  if (url !== '/api/quote' && url !== '/api/quote/') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    return res.end('{"ok":false,"error":"not-found"}');
  }

  // Vercel-style helpers that api/quote.js expects
  res.status = (code) => { res.statusCode = code; return res; };
  res.json = (obj) => {
    if (!res.headersSent) res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify(obj));
    return res;
  };

  let size = 0;
  const chunks = [];
  req.on('data', (c) => {
    size += c.length;
    if (size > MAX_BODY) {
      res.status(413).json({ ok: false, error: 'too-large' });
      req.destroy();
      return;
    }
    chunks.push(c);
  });
  req.on('end', async () => {
    if (res.writableEnded) return;
    const raw = Buffer.concat(chunks).toString('utf8');
    try { req.body = raw ? JSON.parse(raw) : {}; } catch (e) { req.body = {}; }
    try {
      await handler(req, res);
    } catch (err) {
      console.error('quote-server: handler error', err);
      if (!res.writableEnded) res.status(500).json({ ok: false, error: 'server' });
    }
  });
});

server.listen(PORT, '127.0.0.1', () => console.log(`quote-server listening on 127.0.0.1:${PORT}`));
