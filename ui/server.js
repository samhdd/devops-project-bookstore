// server.js
const http = require('http');
const handler = require('serve-handler');
const { createProxyMiddleware } = require('http-proxy-middleware');

// Fix for deprecation warning
process.removeAllListeners('warning');


const API_URL = process.env.API_URL || 'http://localhost:5000';

const server = http.createServer((req, res) => {
  // Check if the request is for the API
  if (req.url.startsWith('/api/')) {
    // Set up proxy to your internal API
    const proxy = createProxyMiddleware({
      target: API_URL,
      changeOrigin: true,
    });
    
    return proxy(req, res);
  }
  
  // Otherwise serve static files
  return handler(req, res, {
    public: 'build',
    rewrites: [
      { source: '/**', destination: '/index.html' }
    ]
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});