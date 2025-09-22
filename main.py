from flask import Flask, render_template, request, jsonify
import re
import random
import json
import os

app = Flask(__name__)

class CollegeChatbot:
    def __init__(self):
        self.responses = {
            # Admissions
            'admission': {
                'keywords': ['admission', 'admit', 'entry', 'join', 'enroll'],
                'response': '''Our admission requirements include: 📋
• High school diploma or equivalent
• Minimum 60% in 12th grade
• Entrance exam (if applicable)
• Application form with required documents
• Interview (for some programs)'''
            },
            'requirements': {
                'keywords': ['requirements', 'criteria', 'eligibility', 'qualify'],
                'response': '''Admission requirements vary by program:
• Undergraduate: 60% in 12th grade
• Graduate: Bachelor's degree with 55%
• Entrance exams may be required
• English proficiency for international students'''
            },
            'application': {
                'keywords': ['application', 'apply', 'form', 'process'],
                'response': '''Application process: 📝
1. Fill online application form
2. Submit required documents
3. Pay application fee
4. Appear for entrance exam (if required)
5. Attend interview
6. Wait for admission decision'''
            },
            
            # Courses
            'courses': {
                'keywords': ['courses', 'programs', 'study', 'degree', 'subjects'],
                'response': '''We offer various programs: 🎓
• Engineering (CS, IT, Mechanical, Civil)
• Business (MBA, BBA, Commerce)
• Arts & Sciences (English, Math, Physics)
• Medical (Nursing, Pharmacy)
• Law (LLB, LLM)'''
            },
            'engineering': {
                'keywords': ['engineering', 'engineer', 'technical', 'cs', 'computer'],
                'response': '''Engineering programs available:
• Computer Science & Engineering
• Information Technology
• Mechanical Engineering
• Civil Engineering
• Electrical Engineering
Duration: 4 years'''
            },
            'business': {
                'keywords': ['business', 'mba', 'bba', 'commerce', 'management'],
                'response': '''Business programs:
• MBA (2 years)
• BBA (3 years)
• B.Com (3 years)
• M.Com (2 years)
Specializations available in Marketing, Finance, HR'''
            },
            
            # Fees
            'fees': {
                'keywords': ['fees', 'cost', 'price', 'money', 'tuition'],
                'response': '''Fee structure (per year): 💰
• Engineering: ₹80,000 - ₹1,20,000
• Business: ₹60,000 - ₹1,00,000
• Arts & Sciences: ₹40,000 - ₹60,000
• Scholarships available for eligible students'''
            },
            'scholarship': {
                'keywords': ['scholarship', 'financial aid', 'discount', 'waiver'],
                'response': '''Scholarships available: 🏆
• Merit-based: Up to 50% fee waiver
• Need-based: Up to 30% fee waiver
• Sports quota: Up to 25% fee waiver
• Minority scholarships available'''
            },
            
            # Facilities
            'facilities': {
                'keywords': ['facilities', 'infrastructure', 'campus', 'building'],
                'response': '''Our facilities include: 🏫
• Modern classrooms with smart boards
• Well-equipped laboratories
• Central library with 50,000+ books
• Sports complex
• Hostel accommodation
• Cafeteria
• Medical center'''
            },
            'library': {
                'keywords': ['library', 'books', 'reading', 'study'],
                'response': '''Library facilities: 📚
• 50,000+ books
• Digital library with e-books
• Research journals and publications
• Computer lab with internet
• Reading rooms
• Study cubicles'''
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room', 'stay'],
                'response': '''Hostel facilities: 🏠
• Separate hostels for boys and girls
• 24/7 security
• Wi-Fi connectivity
• Mess facility
• Common rooms
• Laundry service
• Medical facility'''
            },
            
            # General Info
            'location': {
                'keywords': ['location', 'address', 'where', 'place'],
                'response': '''College Location: 📍
• Main Campus: College Street, City
• Well-connected by public transport
• Nearby metro station
• Bus stop at campus gate
• Parking facilities available'''
            },
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'reach'],
                'response': '''Contact Information: 📞
• Phone: +91-XXXXXXXXXX
• Email: info@college.edu
• Address: College Street, City
• Website: www.college.edu
• Office hours: 9 AM - 5 PM'''
            },
            
            # Greetings
            'hello': {
                'keywords': ['hello', 'hi', 'hey', 'greetings'],
                'response': 'Hello! 👋 Welcome to our college information system. How can I help you today?'
            },
            'help': {
                'keywords': ['help', 'assist', 'support'],
                'response': '''I can help you with information about:
• Admissions & Requirements
• Courses & Programs
• Fees & Scholarships
• Facilities & Services
• Contact Information

Just ask me anything!'''
            },
            'thanks': {
                'keywords': ['thanks', 'thank you', 'appreciate'],
                'response': "You're welcome! 😊 If you have any other questions about our college, feel free to ask anytime!"
            }
        }
        
        self.fallback_responses = [
            "I'm not sure about that specific question. Could you please ask about admissions, courses, fees, or facilities?",
            "That's an interesting question! I can help you with college programs, admission requirements, fees, and facilities.",
            "I don't have specific information about that. Try asking about our courses, admission process, or college facilities!",
            "I'm here to help with college-related questions. Ask me about admissions, courses, fees, or facilities!"
        ]
    
    def preprocess_input(self, user_input):
        """Clean and preprocess user input"""
        # Convert to lowercase and remove extra whitespace
        processed = user_input.lower().strip()
        # Remove punctuation
        processed = re.sub(r'[^\w\s]', ' ', processed)
        # Remove extra spaces
        processed = re.sub(r'\s+', ' ', processed)
        return processed
    
    def get_response(self, user_input):
        """Generate response based on user input"""
        processed_input = self.preprocess_input(user_input)
        
        # Calculate confidence scores for each response
        best_match = None
        highest_score = 0
        
        for key, data in self.responses.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in processed_input:
                    # Give higher score for exact matches
                    if keyword == processed_input:
                        score += 10
                    else:
                        score += 5
            
            if score > highest_score:
                highest_score = score
                best_match = key
        
        # Return best match if confidence is high enough
        if best_match and highest_score >= 5:
            return self.responses[best_match]['response']
        
        # Return random fallback response
        return random.choice(self.fallback_responses)

# Initialize chatbot
chatbot = CollegeChatbot()

@app.route('/')
def home():
    """Render the main chat interface"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>College Info Chatbot - Python</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            height: 700px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            margin: 20px;
        }

        .chat-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
            position: relative;
        }

        .chat-header h1 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .chat-header p {
            opacity: 0.9;
            font-size: 0.9rem;
        }

        .status-indicator {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            scroll-behavior: smooth;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.bot {
            justify-content: flex-start;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.4;
            white-space: pre-line;
        }

        .message.bot .message-content {
            background: #f1f3f4;
            color: #333;
            border-bottom-left-radius: 4px;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .chat-input-container {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }

        .chat-input-form {
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .chat-input:focus {
            border-color: #4facfe;
            box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        }

        .send-button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            font-size: 1.2rem;
        }

        .send-button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
        }

        .quick-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }

        .quick-question-btn {
            background: rgba(79, 172, 254, 0.1);
            color: #4facfe;
            border: 1px solid rgba(79, 172, 254, 0.3);
            border-radius: 20px;
            padding: 8px 12px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quick-question-btn:hover {
            background: rgba(79, 172, 254, 0.2);
            transform: translateY(-1px);
        }

        .typing-indicator {
            display: none;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: #f1f3f4;
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            max-width: 80px;
            margin-bottom: 15px;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: #999;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
            0%, 60%, 100% { transform: scale(1); opacity: 0.5; }
            30% { transform: scale(1.2); opacity: 1; }
        }

        @media (max-width: 640px) {
            .chat-container {
                height: 100vh;
                border-radius: 0;
                margin: 0;
            }

            .status-indicator {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>Ai ChatBoT GEC-V</h1>
            <p>Ask me anything about college information!</p>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span style="font-size: 0.8rem;">Online</span>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    👋 Hello! I'm your College Information Assistant powered by Python. I can help you with questions about admissions, courses, fees, facilities, and more. What would you like to know?
                    <div class="quick-questions">
                        <button class="quick-question-btn" onclick="askQuestion('courses')">Courses</button>
                        <button class="quick-question-btn" onclick="askQuestion('admission')">Admissions</button>
                        <button class="quick-question-btn" onclick="askQuestion('fees')">Fees</button>
                        <button class="quick-question-btn" onclick="askQuestion('facilities')">Facilities</button>
                    </div>
                </div>
            </div>
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>

        <div class="chat-input-container">
            <form class="chat-input-form" id="chatForm">
                <input type="text" class="chat-input" id="chatInput" placeholder="Type your question here..." autocomplete="off">
                <button type="submit" class="send-button">➤</button>
            </form>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const chatForm = document.getElementById('chatForm');
        const typingIndicator = document.getElementById('typingIndicator');

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const userInput = chatInput.value.trim();
            if (!userInput) return;
            
            // Add user message
            addMessage(userInput, 'user');
            chatInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            try {
                // Send message to Python backend
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userInput })
                });
                
                const data = await response.json();
                
                // Hide typing indicator and show response
                setTimeout(() => {
                    hideTypingIndicator();
                    addMessage(data.response, 'bot');
                }, 1000);
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        });

        function addMessage(content, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.insertBefore(messageDiv, typingIndicator);
            scrollToBottom();
        }

        function showTypingIndicator() {
            typingIndicator.style.display = 'flex';
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.style.display = 'none';
        }

        function scrollToBottom() {
            setTimeout(() => {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 100);
        }

        function askQuestion(question) {
            chatInput.value = question;
            chatForm.dispatchEvent(new Event('submit'));
        }
    </script>
</body>
</html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from chatbot
        bot_response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'response': 'Sorry, I encountered an error. Please try again.',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Chatbot is running!'})

if __name__ == '__main__':
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    
    # Enable debug mode for development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print("🤖 College Chatbot is starting...")
    print(f"📡 Server will run on http://localhost:{port}")
    print("💡 Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)