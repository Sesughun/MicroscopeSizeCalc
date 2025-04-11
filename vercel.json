{
  "version": 2,
  "builds": [
    {
      "src": "api/calculate.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/calculate",
      "dest": "/api/calculate.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/index.html"
    }
  ]
}
