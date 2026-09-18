#!/usr/bin/env node
/*
 * pix.js — Zero-config Pix "copia e cola" (BR Code / EMV MPM) + CRC16 + QR SVG.
 * Node stdlib only. Bundled qrcode.js (MIT) for the QR image. No npm install, no API key.
 *
 * Usage:  node pix.js  < config.json     (reads a JSON object from STDIN)
 *   config = { key, keyType?, name, city, amount?, txid?, info? }
 *     key      : the Pix key (CPF/CNPJ digits, e-mail, phone, or EVP/aleatória UUID)
 *     keyType  : "cpf" | "cnpj" | "email" | "phone" | "evp" | "auto" (default "auto")
 *     name     : merchant/receiver name  (<=25 chars in payload, accents stripped, UPPER)
 *     city     : merchant city           (<=15 chars in payload, accents stripped, UPPER)
 *     amount   : numeric BRL value, optional (omit => open-value QR; payer types the value)
 *     txid     : transaction id, optional (default "***")
 *
 * Output (STDOUT, single line JSON):
 *   { brcode, keyType, ambiguous, svg, svgOk, error? }
 *
 * Spec sources (verified 2026-06): EMV MPM / BR Code field IDs + CRC-16/CCITT-FALSE
 * (poly 0x1021, init 0xFFFF). See ../reference/pix.md.
 */
'use strict';
const fs = require('fs');
const path = require('path');

let qrcode = null;
try { qrcode = require(path.join(__dirname, 'qrcode.js')); } catch (e) { qrcode = null; }

function readStdin() { try { return fs.readFileSync(0, 'utf8'); } catch (e) { return ''; } }

// strip diacritics, keep ASCII letters/digits/space, UPPERCASE — required for fields 59/60
function stripAccents(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, ''); }
function sanitizeField(s) {
  return stripAccents(s).toUpperCase().replace(/[^A-Z0-9 ]/g, '').replace(/\s+/g, ' ').trim();
}

// EMV TLV: ID(2) + LEN(2, zero-padded) + VALUE
function emv(id, value) {
  const v = String(value);
  return id + String(v.length).padStart(2, '0') + v;
}

function normalizeKey(key, keyType) {
  key = String(key || '').trim();
  const t = (keyType || 'auto').toLowerCase();
  const digits = key.replace(/\D/g, '');
  const isEmail = key.includes('@');
  const isUuid = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(key);

  if (t === 'email' || (t === 'auto' && isEmail)) return { value: key.toLowerCase(), type: 'email' };
  if (t === 'evp' || (t === 'auto' && isUuid)) return { value: key.toLowerCase(), type: 'evp' };
  if (t === 'cnpj' || (t === 'auto' && digits.length === 14)) return { value: digits, type: 'cnpj' };
  if (t === 'phone') return { value: '+55' + digits.replace(/^55/, ''), type: 'phone' };
  if (t === 'cpf') return { value: digits, type: 'cpf' };
  // auto + 11 digits is ambiguous (CPF and a DDD+celular are both 11 digits) -> default CPF, flag it
  if (t === 'auto' && digits.length === 11) return { value: digits, type: 'cpf', ambiguous: true };
  return { value: key, type: 'unknown' };
}

// CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, no final XOR. Computed over payload INCLUDING "6304".
function crc16(payload) {
  let crc = 0xFFFF;
  for (let i = 0; i < payload.length; i++) {
    crc ^= (payload.charCodeAt(i) << 8) & 0xFFFF;
    for (let j = 0; j < 8; j++) {
      if (crc & 0x8000) crc = ((crc << 1) ^ 0x1021) & 0xFFFF;
      else crc = (crc << 1) & 0xFFFF;
    }
  }
  return crc.toString(16).toUpperCase().padStart(4, '0');
}

function buildBRCode(cfg) {
  const k = normalizeKey(cfg.key, cfg.keyType);
  const gui = emv('00', 'br.gov.bcb.pix');
  let mai = gui + emv('01', k.value);
  if (cfg.info) mai += emv('02', sanitizeField(cfg.info).slice(0, 72));
  let p = '';
  p += emv('00', '01');           // Payload Format Indicator
  p += emv('26', mai);            // Merchant Account Information (Pix)
  p += emv('52', '0000');         // Merchant Category Code (generic)
  p += emv('53', '986');          // Currency = BRL (ISO 4217)
  if (cfg.amount != null && cfg.amount !== '') {
    const amt = Number(cfg.amount);
    if (!isNaN(amt) && amt > 0) p += emv('54', amt.toFixed(2)); // dot decimal, 2 places
  }
  p += emv('58', 'BR');           // Country
  p += emv('59', sanitizeField(cfg.name).slice(0, 25) || 'RECEBEDOR');
  p += emv('60', sanitizeField(cfg.city).slice(0, 15) || 'BRASIL');
  const txid = sanitizeField(cfg.txid).replace(/ /g, '').slice(0, 25) || '***';
  p += emv('62', emv('05', txid)); // Additional data field -> TXID
  p += '6304';                     // CRC16 id+len, value computed next
  return { brcode: p + crc16(p), keyType: k.type, ambiguous: !!k.ambiguous };
}

function qrSvg(text) {
  if (!qrcode) return null;
  try {
    const qr = qrcode(0, 'M'); // typeNumber 0 = auto-size; ECC level M
    qr.addData(text);
    qr.make();
    return qr.createSvgTag({ cellSize: 4, margin: 8, scalable: true });
  } catch (e) { return null; }
}

(function main() {
  let cfg = {};
  try { cfg = JSON.parse(readStdin() || '{}'); }
  catch (e) { process.stdout.write(JSON.stringify({ error: 'invalid JSON input' })); return; }
  if (!cfg.key) { process.stdout.write(JSON.stringify({ error: 'missing pix key' })); return; }
  const r = buildBRCode(cfg);
  const svg = qrSvg(r.brcode);
  process.stdout.write(JSON.stringify({
    brcode: r.brcode, keyType: r.keyType, ambiguous: r.ambiguous, svg: svg, svgOk: !!svg,
  }));
})();
