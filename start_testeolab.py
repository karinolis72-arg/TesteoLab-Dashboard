#!/usr/bin/env python3
"""
TesteoLab Startup Manager
Starts both the Notion API backend and the dashboard server
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        from notion_client import Client
        print("✓ All dependencies available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall dependencies with:")
        print("  pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")

    if not env_file.exists():
        print("\n⚠️  .env file not found. Creating from .env.example...")
        env_example = Path(".env.example")

        if env_example.exists():
            env_content = env_example.read_text()
            env_file.write_text(env_content)
            print("✓ Created .env file")
            print("\n📋 IMPORTANT: You need to configure Notion integration:")
            print("   1. Go to https://www.notion.com/my-integrations")
            print("   2. Create a new integration for TesteoLab")
            print("   3. Copy the API token")
            print("   4. Update the NOTION_TOKEN in .env file")
            print("   5. Share the TesteoLab TAREAS database with the integration")
            return False
        else:
            return True
    else:
        # Check if NOTION_TOKEN is set
        env_content = env_file.read_text()
        if "your_notion_integration_token_here" in env_content:
            print("\n⚠️  NOTION_TOKEN not configured in .env")
            print("   Please add your Notion integration token to continue")
            return False

    return True

def start_notion_api():
    """Start the Flask API server"""
    print("\n🚀 Starting Notion API Backend...")
    print("   → http://localhost:5000")

    proc = subprocess.Popen(
        [sys.executable, "notion_api.py"],
        cwd=Path(__file__).parent
    )

    time.sleep(2)  # Give server time to start
    return proc

def start_dashboard():
    """Start the dashboard server"""
    print("\n🎨 Starting Dashboard Server...")
    print("   → http://localhost:9000")

    proc = subprocess.Popen(
        [sys.executable, "run_dashboard.py"],
        cwd=Path(__file__).parent
    )

    return proc

def main():
    print("=" * 60)
    print("🎯 TesteoLab Control Center")
    print("=" * 60)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Setup environment
    if not setup_environment():
        print("\n⚠️  Configuration incomplete. Exiting.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("STARTING SERVICES...")
    print("=" * 60)

    try:
        # Start both services
        api_proc = start_notion_api()
        dashboard_proc = start_dashboard()

        # Wait a moment for both to start
        time.sleep(3)

        # Open browser
        print("\n🌐 Opening TesteoLab in browser...")
        webbrowser.open("http://localhost:9000")

        print("\n" + "=" * 60)
        print("✓ TesteoLab is ready!")
        print("=" * 60)
        print("\n📍 Access points:")
        print("   • Dashboard:    http://localhost:9000")
        print("   • API:          http://localhost:5000/api")
        print("   • Health Check: http://localhost:5000/api/health")
        print("\n📚 Available API endpoints:")
        print("   • GET /api/tasks/top-q1      - Top 4 Q1 tasks")
        print("   • GET /api/tasks/today       - Today's tasks")
        print("   • GET /api/tasks             - All tasks with filters")
        print("   • GET /api/habits            - All habits")
        print("   • GET /api/nauta/briefing    - NAUTA briefing data")
        print("\n⌨️  Shortcuts:")
        print("   • Ctrl+Shift+S              - Open Settings")
        print("   • ESC                       - Close modals")
        print("\n💡 To stop services:")
        print("   • Close this terminal window")
        print("   • Or press Ctrl+C")
        print("\n" + "=" * 60)

        # Keep processes running
        api_proc.wait()
        dashboard_proc.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down TesteoLab...")
        api_proc.terminate()
        dashboard_proc.terminate()
        api_proc.wait(timeout=5)
        dashboard_proc.wait(timeout=5)
        print("✓ TesteoLab stopped")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
