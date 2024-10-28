const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to set security headers
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' https://apis.google.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com https://www.youtube.com https://www.gstatic.com https://www.google-analytics.com https://js.stripe.com https://www.googletagmanager.com; style-src 'self' https://fonts.googleapis.com https://stackpath.bootstrapcdn.com; img-src 'self' data: https://www.google-analytics.com; frame-src 'self' https://www.youtube.com https://js.stripe.com; connect-src 'self' https://api.stripe.com https://*.supabase.co https://fineurai-9hjoe.ondigitalocean.app;");
  next();
});

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});