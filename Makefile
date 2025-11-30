.PHONY: help run test deploy clean refresh

help:
	@echo "ETA Guesser - Development Commands"
	@echo "==================================="
	@echo ""
	@echo "  make run       - Run backend server locally (http://localhost:5001)"
	@echo "  make frontend  - Open local frontend in browser"
	@echo "  make refresh   - Refresh and reopen game in Chrome"
	@echo "  make test      - Test the backend API locally"
	@echo "  make deploy    - Deploy to Heroku"
	@echo "  make clean     - Stop any running local servers"
	@echo ""

run:
	@echo "🚀 Starting backend server on http://localhost:5001"
	@echo "💡 Open index.local.html in your browser to test"
	@echo ""
	python3 app.py

frontend:
	@echo "🌐 Opening local frontend..."
	@open index.local.html || xdg-open index.local.html || start index.local.html

refresh:
	@echo "🔄 Refreshing and reopening in Chrome..."
	@open -a "Google Chrome" index.local.html
	@osascript -e 'tell application "Google Chrome" to activate' 2>/dev/null || true
	@echo "✅ Opened in Chrome!"

test:
	@echo "🧪 Testing backend API..."
	@echo ""
	@curl -s http://localhost:5001/ | python3 -m json.tool || echo "❌ Backend not running. Run 'make run' first."
	@echo ""

deploy:
	@echo "🚀 Deploying to Heroku..."
	git push heroku main
	@echo "✅ Deployed!"

clean:
	@echo "🧹 Stopping local servers..."
	@lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "No servers running on port 5001"
	@echo "✅ Clean!"