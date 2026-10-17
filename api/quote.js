// Quote request form -> email (Vercel serverless function, POST /api/quote).
//
// Sends each request to every address in QUOTE_TO through Resend (https://resend.com).
// Environment variables (set in Vercel > Project > Settings > Environment Variables):
//   RESEND_API_KEY  Resend API key (secret)
//   QUOTE_TO        recipients, comma-separated, e.g. "info@parawawa.lk, you@example.com"
//   QUOTE_FROM      sender, e.g. "Parawewa Website <quotes@parawawa.lk>" (domain must be verified in Resend).
//                   Until the domain is verified, leave it unset: Resend's test sender then only
//                   delivers to the email address that owns the Resend account.

const MODELS = {
  gravity: 'Option A: Gravity-Fed (no electricity)',
  pump: 'Option B: Seal Type Parawewa System (high water table)',
  consult: 'Not sure, needs engineering consultation',
};
const LIMITS = { name: 100, phone: 30, location: 120, message: 2000, page: 200 };

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);

function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') {
    try { return JSON.parse(req.body); } catch (e) { return {}; }
  }
  return {};
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method' });
  }

  const b = readBody(req);

  // Spam guards: a hidden field people never fill in, and a form that was filled in too fast.
  if (b.company) return res.status(200).json({ ok: true });
  const elapsed = Number(b.elapsed);
  if (Number.isFinite(elapsed) && elapsed >= 0 && elapsed < 2500) return res.status(200).json({ ok: true });

  const name = clean(b.name, LIMITS.name);
  const phone = clean(b.phone, LIMITS.phone);
  const location = clean(b.location, LIMITS.location);
  const model = MODELS[b.model] || MODELS.consult;
  const message = String(b.message == null ? '' : b.message).trim().slice(0, LIMITS.message);
  const page = clean(b.page, LIMITS.page);
  const lang = b.lang === 'si' ? 'Sinhala page' : 'English page';

  if (!name || !location || !/^[+\d][\d\s()-]{6,}$/.test(phone)) {
    return res.status(400).json({ ok: false, error: 'invalid' });
  }

  const key = process.env.RESEND_API_KEY;
  const to = (process.env.QUOTE_TO || '').split(',').map((s) => s.trim()).filter(Boolean);
  if (!key || !to.length) {
    console.error('quote: RESEND_API_KEY or QUOTE_TO is not set');
    return res.status(503).json({ ok: false, error: 'not-configured' });
  }

  const digits = phone.replace(/[^\d]/g, '');
  const wa = 'https://wa.me/' + (digits.startsWith('0') ? '94' + digits.slice(1) : digits);
  const rows = [
    ['Name', name], ['Phone / WhatsApp', phone], ['Location', location], ['System', model],
    ['Message', message || '(none)'], ['Sent from', `${page || '/'} (${lang})`],
  ];
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + `\n\nWhatsApp: ${wa}`;
  const html = `<h2 style="font-family:Arial,sans-serif;color:#0c3b21">New quote request</h2>
<table style="font-family:Arial,sans-serif;font-size:15px;border-collapse:collapse">
${rows.map(([k, v]) => `<tr><td style="padding:6px 14px 6px 0;color:#55655b;vertical-align:top"><b>${esc(k)}</b></td><td style="padding:6px 0;white-space:pre-wrap">${esc(v)}</td></tr>`).join('\n')}
</table>
<p style="font-family:Arial,sans-serif"><a href="tel:${esc(phone.replace(/\s/g, ''))}">Call ${esc(phone)}</a> &middot; <a href="${esc(wa)}">WhatsApp</a></p>`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.QUOTE_FROM || 'Parawewa Website <onboarding@resend.dev>',
        to,
        subject: `New quote request: ${name} (${location})`,
        text,
        html,
      }),
    });
    if (!r.ok) {
      console.error('quote: Resend error', r.status, await r.text());
      return res.status(502).json({ ok: false, error: 'send-failed' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('quote: request failed', err);
    return res.status(502).json({ ok: false, error: 'send-failed' });
  }
};
