from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from faqs import FAQS

app = Flask(__name__)

# Common questions dictionary
COMMON_QA = {
    "what is Artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.",
    "what is ai": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.",
    "what is a computer": "A computer is an electronic device that manipulates information, or data. It has the ability to store, retrieve, and process data.",
    "what is computer": "A computer is an electronic device that manipulates information, or data. It has the ability to store, retrieve, and process data.",
    "what is the internet": "The Internet is a global network of computers connected together that allows people to share information and communicate with each other.",
    "what is internet": "The Internet is a global network of computers connected together that allows people to share information and communicate with each other.",
    "what is software": "Software is a set of instructions, data or programs used to operate computers and execute specific tasks.",
    "what is hardware": "Hardware refers to the physical components of a computer system, such as the motherboard, CPU, memory, and storage devices.",
    "what is machine learning": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
    "what is data science": "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from data.",
    "what is programming": "Programming is the process of creating a set of instructions that tell a computer how to perform a task.",
    "what is python": "Python is a high-level programming language known for its simplicity and readability, widely used for web development, data analysis, artificial intelligence, and more.",
    "what is javascript": "JavaScript is a programming language that enables interactive web pages and is an essential part of web applications.",
    "what is html": "HTML (HyperText Markup Language) is the standard markup language for creating web pages and web applications.",
    "what is css": "CSS (Cascading Style Sheets) is a style sheet language used for describing the presentation of a document written in HTML.",
    "what is cloud computing": "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet to offer faster innovation, flexible resources, and economies of scale.",
    "what is cybersecurity": "Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These attacks are usually aimed at accessing, changing, or destroying sensitive information.",
    "what is blockchain": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, which are linked and secured using cryptography.",
    "what is deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model complex patterns in data, enabling advanced applications like image recognition and natural language processing.",
    "what is iot": "IoT (Internet of Things) refers to the network of physical devices, vehicles, home appliances, and other items embedded with sensors, software, and connectivity to enable data exchange.",
    "what is big data": "Big data refers to large, diverse sets of information that grow at ever-increasing rates. It encompasses the volume of information, the speed or velocity at which it is created and collected, and the variety or scope of the data points being covered.",
    "what is virtual reality": "Virtual reality (VR) is a simulated experience that can be similar to or completely different from the real world, created using computer technology.",
    "what is augmented reality": "Augmented reality (AR) is an interactive experience of a real-world environment where the objects that reside in the real world are enhanced by computer-generated perceptual information.",
    "what is quantum computing": "Quantum computing is a type of computation that harnesses the collective properties of quantum states, such as superposition and entanglement, to perform calculations.",
    "what is 5g": "5G is the fifth generation of wireless technology for digital cellular networks, offering faster speeds, lower latency, and more reliable connections than previous generations.",
    "what is tiktok": "TikTok is a social media platform for creating, sharing, and discovering short-form videos, popular among Gen Z for music, dance, and comedy content.",
    "what is a meme": "A meme is a humorous image, video, or text that spreads virally online, often used to express ideas or emotions in a relatable way.",
    "what is streaming": "Streaming refers to the continuous transmission of audio or video content over the internet, allowing real-time playback without downloading files.",
    "what is nft": "NFT (Non-Fungible Token) is a unique digital asset representing ownership of a specific item or piece of content, often used in art and collectibles.",
    "what is metaverse": "The metaverse is a collective virtual shared space, created by the convergence of virtually enhanced physical reality and physically persistent virtual reality.",
    "what is cancel culture": "Cancel culture refers to the practice of withdrawing support for public figures or companies after they have done or said something considered objectionable or offensive.",
    "what is ghosting": "Ghosting is the act of suddenly ceasing all communication with someone without explanation, often in the context of dating or friendships.",
    "what is fomo": "FOMO stands for Fear Of Missing Out, the anxiety that an exciting or interesting event may currently be happening elsewhere.",
    "what is influencer": "An influencer is a person who has the power to affect the purchasing decisions of others because of their authority, knowledge, or relationship with their audience.",
    "what is viral": "Viral refers to content that spreads rapidly and widely from one internet user to another, often through social media sharing.",
    "what is binge watching": "Binge watching is the practice of watching multiple episodes of a television program or web series in rapid succession.",
}

def find_faq_match(query):
    query_lower = query.lower()
    for question, answer in FAQS.items():
        if question.lower() in query_lower or query_lower in question.lower():
            return answer
    return None

def find_common_qa_match(query):
    query_lower = query.lower()
    for question, answer in COMMON_QA.items():
        if question.lower() in query_lower or query_lower in question.lower():
            return answer
    return None

def escalate_query(query):
    # Escalation without email (for demo purposes)
    return f"Query escalated to support team: {query}. Please contact support@example.com for further assistance."

def get_ai_response(query):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Answer the following question helpfully: {query}")
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {str(e)}")  # For debugging
        return f"I'm sorry, I couldn't generate a response right now. Please try again later or contact support."

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            # Check COMMON_QA first
            common_answer = find_common_qa_match(query)
            if common_answer:
                response = common_answer
            else:
                # Get AI response for other questions
                ai_response = get_ai_response(query)
                if ai_response and not ai_response.startswith("I'm sorry"):
                    response = ai_response
                else:
                    # Fallback if AI fails
                    response = "I'm sorry, I couldn't find an answer to your question. Please try rephrasing or contact support."
            return render_template('index.html', response=response)
        elif 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            # For demo purposes, just redirect to home
            return render_template('index.html', response="Signed in successfully!")
        else:
            return render_template('signin.html', error="Invalid request.")
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            # For demo purposes, just redirect to home
            return render_template('index.html', response="Signed in successfully!")
        else:
            return render_template('signin.html', error="Please provide email and password.")
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)

