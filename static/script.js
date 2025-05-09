document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('micButton');
    const responseArea = document.getElementById('responseArea');
    const listeningIndicator = document.getElementById('listeningIndicator');
    const voiceSelect = document.getElementById('voiceSelect');
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        responseArea.innerHTML = "<p>Your browser doesn't support speech recognition. Try Chrome or Edge.</p>";
        micButton.disabled = true;
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    const synth = window.speechSynthesis;
    let voices = [];
    
    function populateVoiceList() {
        voices = synth.getVoices();
        
        voiceSelect.innerHTML = '';
        
        voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.textContent = `${voice.name} (${voice.lang})`;
            option.setAttribute('data-lang', voice.lang);
            option.setAttribute('data-name', voice.name);
            option.value = index;
            voiceSelect.appendChild(option);
        });
        const defaultVoice = voices.findIndex(voice => voice.lang.includes('en-'));
        if (defaultVoice !== -1) {
            voiceSelect.value = defaultVoice;
        }
    }
    
    populateVoiceList();
    
    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = populateVoiceList;
    }
    
    window.openYouTube = (query) => {
        fetch('/open_youtube', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            console.log("YouTube response:", data);
            window.open(`https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`, '_blank');
        })
        .catch(error => {
            console.error('Error opening YouTube:', error);
            window.open(`https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`, '_blank');
        });
    };
    window.askQuestion = (query) => {
        
        responseArea.innerHTML = `<p><strong>You:</strong> ${query}</p>
                                 <p><strong>Assistant:</strong> <em>Processing...</em></p>`;
        
       
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            responseArea.innerHTML = `<p><strong>You:</strong> ${query}</p>
                                     <p><strong>Assistant:</strong> ${data.response}</p>`;
            
            const textToSpeak = data.response.replace(/<[^>]*>/g, '');
            const utterance = new SpeechSynthesisUtterance(textToSpeak);
            
            const selectedVoice = voices[voiceSelect.value];
            if (selectedVoice) {
                utterance.voice = selectedVoice;
            }
            
            utterance.rate = 1.0;  
            utterance.pitch = 1.0; 
            utterance.volume = 1.0; 
            
            synth.speak(utterance);
        })
        .catch(error => {
            console.error('Error:', error);
            responseArea.innerHTML = `<p><strong>You:</strong> ${query}</p>
                                     <p><strong>Error:</strong> Couldn't process your request. Technical details: ${error.message}</p>`;
        });
    };
    
    micButton.addEventListener('click', () => {
        micButton.style.backgroundColor = '#FF5252'; 
        listeningIndicator.classList.remove('hidden');
        
        responseArea.innerHTML = "<p><em>Listening...</em></p>";
        recognition.start();
       
        setTimeout(() => {
            if (recognition) {
                recognition.stop();
            }
        }, 6000);
    });
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        window.askQuestion(transcript);
    };
    
    recognition.onend = () => {
        
        micButton.style.backgroundColor = '#4CAF50';
        listeningIndicator.classList.add('hidden');
    };
    
    recognition.onerror = (event) => {
        console.error('Recognition error:', event.error);
        responseArea.innerHTML = `<p><strong>Error:</strong> ${event.error}</p>`;
        micButton.style.backgroundColor = '#4CAF50';
        listeningIndicator.classList.add('hidden');
    };
});