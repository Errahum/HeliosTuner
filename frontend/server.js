const express = require('express');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to set security headers
app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  res.setHeader('Content-Security-Policy', `default-src 'self'; script-src 'self' 'nonce-${nonce}' https://apis.google.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com https://www.youtube.com https://www.gstatic.com https://www.google-analytics.com https://js.stripe.com https://www.googletagmanager.com; style-src 'self' 'nonce-${nonce}' https://fonts.googleapis.com https://stackpath.bootstrapcdn.com; img-src 'self' data: https://www.google-analytics.com; font-src 'self' https://fonts.gstatic.com; frame-src 'self' https://www.youtube.com https://js.stripe.com; connect-src 'self' https://api.stripe.com https://*.supabase.co https://fineurai-9hjoe.ondigitalocean.app;`);
  res.locals.nonce = nonce; // Make nonce available to templates
  next();
});

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function (req, res) {
  const indexPath = path.join(__dirname, 'build', 'index.html');
  fs.readFile(indexPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).send('Error reading index.html');
    }
    const nonce = res.locals.nonce;
    const updatedData = data.replace('<head>', `<head><meta name="csp-nonce" content="${nonce}">`);
    res.send(updatedData);
  });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});