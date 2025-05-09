from flask import Flask, render_template, request, jsonify
import wikipedia
import random
import datetime
import re
import webbrowser
import subprocess
import platform
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'response': 'Invalid request data'}), 400
            
        query = data['query'].lower()
        
        
        response = generate_response(query)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'response': f'Server error: {str(e)}'}), 500

@app.route('/open_youtube', methods=['POST'])
def open_youtube():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = "https://www.youtube.com"
            
        
        open_browser(url)
        
        return jsonify({'response': f"Opening YouTube for '{query}'"})
    except Exception as e:
        print(f"Error opening YouTube: {str(e)}")
        return jsonify({'response': f'Could not open YouTube: {str(e)}'}), 500

def open_browser(url):
    """Attempt to open a URL in the default web browser based on the operating system"""
    try:
       
        webbrowser.open(url, new=2)
        
        
        system = platform.system().lower()
        if 'windows' in system:
            os.system(f'start {url}')
        elif 'darwin' in system:  # macOS
            subprocess.call(['open', url])
        elif 'linux' in system:
            subprocess.call(['xdg-open', url])
    except Exception as e:
        print(f"Failed to open browser: {e}")
        

def generate_response(query):
    
    if any(word in query for word in ['hello', 'hi', 'hey']):
        greetings = ["Hello! How can I help you?", "Hi there! What can I do for you?", 
                    "Hey! How can I assist you today?"]
        return random.choice(greetings)
    
    
    elif any(word in query for word in ['time', 'what time']):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        return f"The current time is {current_time}."
    
    
    elif any(word in query for word in ['date', 'day', 'today']):
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"Today is {current_date}."
        
   
    elif any(word in query for word in ['weather', 'temperature', 'forecast']):
        try:
            
            weather_conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy", "windy", "snowy"]
            temperatures = range(5, 35)
            condition = random.choice(weather_conditions)
            temp = random.choice(temperatures)
            
            return f"The current weather appears to be {condition} with a temperature of {temp}°C. For accurate weather information, you would need to integrate a real weather API with your key."
        except:
            return "I'm having trouble getting the weather information. You would need to integrate a weather API for real-time data."

    
    elif any(phrase in query for phrase in ['open youtube', 'play youtube', 'youtube video', 'youtube channel']):
        search_term = query
        for word in ['youtube', 'open', 'play', 'watch', 'channel', 'video', 'videos']:
            search_term = search_term.replace(word, '')
        search_term = search_term.strip()
        if search_term:
            
            try:
                url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                open_browser(url)
                return f"Opening YouTube for '{search_term}'. If it doesn't open automatically, <button class='youtube-button' onclick='openYouTube(\"{search_term}\")'>Click here</button>"
            except:
                return f"<button class='youtube-button' onclick='openYouTube(\"{search_term}\")'>Open YouTube: {search_term}</button>"
        else:
            try:
                url = "https://www.youtube.com"
                open_browser(url)
                return f"Opening YouTube. If it doesn't open automatically, <button class='youtube-button' onclick='openYouTube(\"\")'>Click here</button>"
            except:
                return f"<button class='youtube-button' onclick='openYouTube(\"\")'>Open YouTube</button>"
    elif any(phrase in query for phrase in ['programming language', 'coding language', 'programming languages']):
        return """
        Popular programming languages include:
        
        1. Python - Known for its readability and versatility
        2. JavaScript - The language of the web
        3. Java - Popular for enterprise applications
        4. C/C++ - Used for system programming and performance-critical applications
        5. C# - Microsoft's language for .NET development
        6. PHP - Common for web development
        7. Ruby - Known for Ruby on Rails framework
        8. Swift - Used for iOS and macOS development
        9. Kotlin - Modern language for Android development
        10. Go - Created by Google for efficient concurrent programming
        11. Rust - Focuses on safety and performance
        12. TypeScript - Typed superset of JavaScript
        
        Each language has its own strengths, weaknesses, and ideal use cases.
        """
    elif any(phrase in query for phrase in ['web technology', 'web technologies', 'front end', 'backend']):
        return """
        Common web technologies include:
        
        Frontend:
        - HTML5 - Structure of web pages
        - CSS3 - Styling and layout
        - JavaScript - Client-side functionality
        - React, Angular, Vue - Popular JavaScript frameworks
        - Bootstrap, Tailwind CSS - CSS frameworks
        
        Backend:
        - Node.js, Django, Flask, Ruby on Rails, Spring - Popular frameworks
        - Express.js, FastAPI - API frameworks
        - SQL and NoSQL databases (MySQL, PostgreSQL, MongoDB)
        
        Other web technologies:
        - REST and GraphQL APIs for data exchange
        - WebSockets for real-time communication
        - Progressive Web Apps (PWAs)
        - Web Assembly for high-performance web applications
        """
    elif any(phrase in query for phrase in ['new technology', 'new technologies', 'emerging technology', 'future tech']):
        return """
        Some emerging technologies to watch:
        
        1. Artificial Intelligence & Machine Learning - Including large language models like GPT and Claude
        2. Blockchain and Web3 technologies
        3. Quantum Computing
        4. Augmented and Virtual Reality (AR/VR)
        5. Internet of Things (IoT)
        6. 5G and future network technologies
        7. Edge Computing
        8. Robotics and automation
        9. Biotechnology and genetic engineering
        10. Sustainable energy technologies
        
        These technologies are reshaping industries and creating new opportunities across sectors.
        """
    elif 'elon musk' in query.lower():
        return """
        Elon Musk is a business magnate, industrial designer, and entrepreneur. He is the founder, CEO, and chief engineer of SpaceX; CEO and product architect of Tesla, Inc.; founder of The Boring Company; co-founder of Neuralink and OpenAI. He was born on June 28, 1971, in Pretoria, South Africa.
        
        Musk is known for his ambitious goals to reduce global warming through sustainable energy production and consumption, and his aim to reduce the risk of human extinction by establishing a human colony on Mars. As of 2023, he is one of the world's wealthiest individuals.
        """
    
    elif any(word in query for word in ['calculate', 'compute', 'plus', 'minus', 'times', 'multiply', 'divide']) or re.search(r'what\s+is\s+[\d\s\+\-\*/]+', query):
        try:
          
            prep_query = query.lower()
            prep_query = prep_query.replace('plus', '+')
            prep_query = prep_query.replace('minus', '-')
            prep_query = prep_query.replace('times', '*')
            prep_query = prep_query.replace('multiply by', '*')
            prep_query = prep_query.replace('multiplied by', '*')
            prep_query = prep_query.replace('divided by', '/')
            prep_query = prep_query.replace('divide by', '/')
            
            expression_match = re.search(r'(?:what\s+is\s+)?(\d+(?:\s*[\+\-\*/]\s*\d+)+)', prep_query)
            
            if not expression_match:
                numbers = re.findall(r'\d+', prep_query)
                if len(numbers) >= 2 and ('+' in prep_query or 'plus' in prep_query):
                    expression = f"{numbers[0]} + {numbers[1]}"
                    for i in range(2, len(numbers)):
                        if i < len(numbers):
                            expression += f" + {numbers[i]}"
                elif len(numbers) >= 2 and ('-' in prep_query or 'minus' in prep_query):
                    expression = f"{numbers[0]} - {numbers[1]}"
                    for i in range(2, len(numbers)):
                        if i < len(numbers):
                            expression += f" - {numbers[i]}"
                elif len(numbers) >= 2 and ('*' in prep_query or 'times' in prep_query or 'multiplied' in prep_query):
                    expression = f"{numbers[0]} * {numbers[1]}"
                    for i in range(2, len(numbers)):
                        if i < len(numbers):
                            expression += f" * {numbers[i]}"
                elif len(numbers) >= 2 and ('/' in prep_query or 'divided' in prep_query):
                    expression = f"{numbers[0]} / {numbers[1]}"
                    for i in range(2, len(numbers)):
                        if i < len(numbers):
                            expression += f" / {numbers[i]}"
                else:
                    return "I couldn't extract a mathematical expression from your question. Please try phrasing it differently."
            else:
                expression = expression_match.group(1)
            clean_expr = re.sub(r'\s+', '', expression)
            if re.match(r'^[\d\+\-\*/\(\)\.]+$', clean_expr):
                result = eval(clean_expr)
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 4) 
                return f"The result of {expression.strip()} is {result}."
            else:
                return "I can only process basic math operations with numbers."
            
        except Exception as e:
            print(f"Math calculation error: {str(e)}")
            return f"I had trouble with that calculation. Try rephrasing it more clearly."
    elif any(word in query for word in ['joke', 'funny']):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "I'm on a seafood diet. I see food and I eat it.",
            "Why did the bicycle fall over? Because it was two-tired.",
            "What do you call a fake noodle? An impasta.",
            "How does a penguin build its house? Igloos it together.",
            "Why don't eggs tell jokes? They'd crack each other up."
        ]
        return random.choice(jokes)
    elif "python libraries" in query or "python packages" in query:
        return """
        Some popular Python libraries include:
        
        1. NumPy - For numerical computing and array operations
        2. Pandas - For data manipulation and analysis
        3. Matplotlib and Seaborn - For data visualization
        4. TensorFlow, PyTorch, and scikit-learn - For machine learning
        5. Django and Flask - For web development
        6. Requests - For HTTP requests
        7. Beautiful Soup - For web scraping
        8. Pygame - For game development
        9. Pillow - For image processing
        10. SQLAlchemy - For database operations
        
        There are over 300,000 packages available in the Python Package Index (PyPI) for various purposes.
        """
    elif any(word in query for word in ['who', 'what', 'when', 'where', 'why', 'how']):
        try:
            if re.search(r'[\d\s\+\-\*/]+', query) and ('calculate' in query or 'compute' in query or 'what is' in query): 
                return generate_response(f"calculate {query}")  
            
            if any(phrase in query for phrase in ['weather', 'forecast', 'temperature']):
                return generate_response('weather')  
              
            if 'programming language' in query or 'coding language' in query:
                return generate_response('programming languages')
                
            if 'web technology' in query or 'web technologies' in query:
                return generate_response('web technologies')
                
            if 'new technology' in query or 'emerging technology' in query:
                return generate_response('new technologies')
            
            if 'elon musk' in query.lower():
                return generate_response('elon musk')
            
            search_terms = query.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
            
            wiki_summary = wikipedia.summary(search_terms, sentences=2)
            return wiki_summary
            
        except Exception as e:
            print(f"Wikipedia search failed: {str(e)}")
            return "I couldn't find specific information about that. Try asking in a different way or asking about something else."
    
    else:
        return "I'm not sure how to help with that. Try asking me about the time, date, weather, programming languages, web technologies, new technologies, a calculation, a fact, or for a joke."

if __name__ == '__main__':
    app.run(debug=True)