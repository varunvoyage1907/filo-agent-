"""
FILO TRUE AI DASHBOARD
Advanced dashboard for the Claude 4 Sonnet powered FILO system
"""

from flask import Flask, render_template_string, jsonify, request
import json
import logging
from datetime import datetime
from filo_true_ai import FiloTrueAI

# Initialize Flask app
app = Flask(__name__)

# Initialize TRUE AI FILO
filo_ai = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FILO_AI_DASHBOARD")

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(create_ai_dashboard_template())

@app.route('/api/start', methods=['POST'])
def start_filo():
    """Start TRUE AI FILO"""
    global filo_ai
    try:
        if not filo_ai:
            filo_ai = FiloTrueAI()
        
        result = filo_ai.start()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_filo():
    """Stop TRUE AI FILO"""
    global filo_ai
    try:
        if filo_ai:
            result = filo_ai.stop()
            return jsonify(result)
        return jsonify({'error': 'FILO not initialized'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get FILO status"""
    global filo_ai
    try:
        if filo_ai:
            return jsonify(filo_ai.get_status())
        return jsonify({'status': 'not_initialized'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Chat with Claude 4 Sonnet powered FILO"""
    global filo_ai
    try:
        if not filo_ai:
            return jsonify({'error': 'FILO not initialized'})
        
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'No message provided'})
        
        # Chat with TRUE AI FILO
        result = filo_ai.chat(user_message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/insights', methods=['GET'])
def get_ai_insights():
    """Get AI insights from Claude 4 Sonnet"""
    global filo_ai
    try:
        if not filo_ai:
            return jsonify({'error': 'FILO not initialized'})
        
        insights = filo_ai.get_ai_insights()
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/emergency_pause', methods=['POST'])
def emergency_pause():
    """Emergency pause all campaigns"""
    global filo_ai
    try:
        if not filo_ai:
            return jsonify({'error': 'FILO not initialized'})
        
        reason = request.json.get('reason', 'Emergency pause requested by user')
        result = filo_ai.emergency_pause(reason)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)})

def create_ai_dashboard_template():
    """Create the TRUE AI FILO dashboard template"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FILO TRUE AI - Claude 4 Sonnet Powered Marketing Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .header p {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            font-weight: 500;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #ff9800, #f57c00);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            font-size: 1.4rem;
            margin-bottom: 20px;
            color: #333;
            font-weight: 600;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-running { background: #4CAF50; }
        .status-stopped { background: #f44336; }
        .status-unknown { background: #9e9e9e; }
        
        .chat-container {
            height: 400px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8fafc;
        }
        
        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .user-message {
            background: #e6f3ff;
            text-align: right;
            margin-left: 20%;
        }
        
        .ai-message {
            background: #f0fff4;
            margin-right: 20%;
        }
        
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .ai-badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            
            .controls {
                flex-direction: column;
                align-items: center;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 FILO TRUE AI</h1>
        <p>Claude 4 Sonnet Powered Marketing Agent <span class="ai-badge">AI Powered</span></p>
    </div>
    
    <div class="container">
        <div class="controls">
            <button class="btn btn-primary" onclick="startFilo()">🚀 Start FILO AI</button>
            <button class="btn btn-danger" onclick="stopFilo()">⏹️ Stop FILO AI</button>
            <button class="btn btn-warning" onclick="emergencyPause()">🚨 Emergency Pause</button>
            <button class="btn btn-primary" onclick="getInsights()">🧠 Get AI Insights</button>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3><span class="status-indicator" id="status-indicator"></span>AI Agent Status</h3>
                <div id="status-content">
                    <div class="loading">Loading status...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 AI Metrics</h3>
                <div class="metrics-grid" id="metrics-content">
                    <div class="loading">Loading metrics...</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>💬 Chat with Claude 4 Sonnet</h3>
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages">
                    <div class="chat-message ai-message">
                        <strong>🧠 Claude:</strong> Hello! I'm Claude 4 Sonnet, your AI marketing expert. I can analyze your campaigns, make strategic decisions, and execute optimizations in real-time. What would you like to know about your Facebook ads?<br>
                        <small style="color: #666;">Powered by Claude 4 Sonnet • Real-time execution • Strategic intelligence</small>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" class="chat-input" id="chat-input" placeholder="Ask Claude anything about your campaigns..." onkeypress="handleChatKeypress(event)">
                    <button class="btn btn-primary" onclick="sendChatMessage()">Send</button>
                </div>
            </div>
        </div>
        
        <div class="card" id="insights-card" style="display: none;">
            <h3>🧠 AI Insights from Claude 4 Sonnet</h3>
            <div id="insights-content"></div>
        </div>
    </div>
    
    <script>
        let updateInterval;
        
        // Start auto-refresh
        function startAutoRefresh() {
            updateStatus();
            updateInterval = setInterval(() => {
                updateStatus();
            }, 10000); // Update every 10 seconds
        }
        
        // Update status
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const indicator = document.getElementById('status-indicator');
                    const content = document.getElementById('status-content');
                    
                    if (data.status === 'running') {
                        indicator.className = 'status-indicator status-running';
                        content.innerHTML = `
                            <p><strong>Status:</strong> 🟢 Running with Claude 4 Sonnet</p>
                            <p><strong>Monitoring Cycles:</strong> ${data.monitoring_cycles || 0}</p>
                            <p><strong>Actions Taken:</strong> ${data.actions_taken || 0}</p>
                            <p><strong>Last Check:</strong> ${data.last_check || 'Never'}</p>
                            <p><strong>AI Brain:</strong> ${data.ai_brain_active ? '🧠 Active' : '❌ Inactive'}</p>
                        `;
                    } else {
                        indicator.className = 'status-indicator status-stopped';
                        content.innerHTML = `
                            <p><strong>Status:</strong> 🔴 Stopped</p>
                            <p>Click "Start FILO AI" to begin intelligent monitoring</p>
                        `;
                    }
                    
                    // Update metrics
                    updateMetrics(data);
                })
                .catch(error => {
                    console.error('Status update error:', error);
                    document.getElementById('status-indicator').className = 'status-indicator status-unknown';
                });
        }
        
        // Update metrics
        function updateMetrics(data) {
            const metricsContent = document.getElementById('metrics-content');
            
            metricsContent.innerHTML = `
                <div class="metric-card">
                    <div class="metric-value">${data.monitoring_cycles || 0}</div>
                    <div class="metric-label">AI Cycles</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.actions_taken || 0}</div>
                    <div class="metric-label">AI Actions</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.status === 'running' ? 'ON' : 'OFF'}</div>
                    <div class="metric-label">AI Status</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">Claude</div>
                    <div class="metric-label">AI Model</div>
                </div>
            `;
        }
        
        // Start FILO
        function startFilo() {
            fetch('/api/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'started' || data.status === 'already_running') {
                        addChatMessage('🚀 FILO TRUE AI started successfully! Claude 4 Sonnet is now monitoring your campaigns.', 'ai');
                    } else {
                        addChatMessage('❌ Error starting FILO: ' + (data.error || 'Unknown error'), 'ai');
                    }
                    updateStatus();
                })
                .catch(error => {
                    addChatMessage('❌ Error starting FILO: ' + error.message, 'ai');
                });
        }
        
        // Stop FILO
        function stopFilo() {
            fetch('/api/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    addChatMessage('⏹️ FILO TRUE AI stopped. Session summary: ' + JSON.stringify(data.session_summary), 'ai');
                    updateStatus();
                })
                .catch(error => {
                    addChatMessage('❌ Error stopping FILO: ' + error.message, 'ai');
                });
        }
        
        // Emergency pause
        function emergencyPause() {
            if (confirm('Are you sure you want to emergency pause all campaigns?')) {
                fetch('/api/emergency_pause', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: 'Emergency pause from dashboard' })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        addChatMessage('🚨 Emergency pause executed by Claude 4 Sonnet. All campaigns paused.', 'ai');
                    } else {
                        addChatMessage('❌ Emergency pause failed: ' + (data.error || 'Unknown error'), 'ai');
                    }
                })
                .catch(error => {
                    addChatMessage('❌ Emergency pause error: ' + error.message, 'ai');
                });
            }
        }
        
        // Get AI insights
        function getInsights() {
            fetch('/api/insights')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('insights-card').style.display = 'block';
                        document.getElementById('insights-content').innerHTML = `
                            <div style="white-space: pre-wrap; line-height: 1.6;">${data.insights}</div>
                            <p style="margin-top: 15px; font-size: 0.9rem; color: #666;">
                                Generated by Claude 4 Sonnet at ${new Date(data.timestamp).toLocaleString()}
                            </p>
                        `;
                    } else {
                        addChatMessage('❌ Error getting insights: ' + (data.error || 'Unknown error'), 'ai');
                    }
                })
                .catch(error => {
                    addChatMessage('❌ Insights error: ' + error.message, 'ai');
                });
        }
        
        // Send chat message
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            addChatMessage(message, 'user');
            input.value = '';
            
            // Add typing indicator
            addChatMessage('Claude is thinking...', 'ai', 'typing-indicator');
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                const typingIndicator = document.querySelector('.typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                
                if (data.success) {
                    addChatMessage(data.response, 'ai');
                    
                    if (data.actions_executed && data.actions_executed.length > 0) {
                        addChatMessage(`⚡ Executed ${data.actions_executed.length} actions based on AI decision`, 'ai');
                    }
                } else {
                    addChatMessage('❌ Error: ' + (data.error || 'Unknown error'), 'ai');
                }
            })
            .catch(error => {
                // Remove typing indicator
                const typingIndicator = document.querySelector('.typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                addChatMessage('❌ Chat error: ' + error.message, 'ai');
            });
        }
        
        // Handle chat keypress
        function handleChatKeypress(event) {
            if (event.key === 'Enter') {
                sendChatMessage();
            }
        }
        
        // Add chat message
        function addChatMessage(message, sender, className = '') {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${sender}-message ${className}`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>👤 You:</strong> ${message}`;
            } else {
                messageDiv.innerHTML = `<strong>🧠 Claude:</strong> ${message.replace(/\\n/g, '<br>')}`;
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            startAutoRefresh();
        });
    </script>
</body>
</html>
    """

if __name__ == '__main__':
    logger.info("🚀 Starting FILO TRUE AI Dashboard with Claude 4 Sonnet...")
    app.run(debug=True, host='0.0.0.0', port=5000)
