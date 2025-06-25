from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_engine import get_rag_engine
import traceback
import os

app = Flask(__name__)
CORS(app)  # Enable CORS so React can talk to Flask

# Initialize RAG engine
try:
    rag_engine = get_rag_engine()
    print("RAG engine initialized successfully")
except Exception as e:
    print(f"Error initializing RAG engine: {e}")
    rag_engine = None

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Missing question"}), 400

        if rag_engine:
            # Use RAG engine to get intelligent answer
            answer, sources = rag_engine.query(question)
            source_files = list(set([s['source'] for s in sources])) if sources else []
        else:
            # Fallback response if RAG engine is not available
            answer = "I'm currently experiencing technical difficulties. Please try again later or consult with a healthcare professional for immediate assistance."
            source_files = []

        return jsonify({
            "answer": answer, 
            "sources": source_files
        })
    
    except Exception as e:
        print(f"Error processing question: {e}")
        print(traceback.format_exc())
        return jsonify({
            "error": "An error occurred while processing your question. Please try again."
        }), 500

@app.route("/health-tips", methods=["GET"])
def get_health_tips():
    try:
        category = request.args.get("category")
        
        if rag_engine:
            tips = rag_engine.get_health_tips(category)
        else:
            tips = ["Stay hydrated", "Get regular exercise", "Maintain a balanced diet", "Get adequate sleep"]
        
        return jsonify({"tips": tips})
    
    except Exception as e:
        print(f"Error getting health tips: {e}")
        return jsonify({"error": "Failed to retrieve health tips"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "rag_engine_available": rag_engine is not None
    })

# ✅ This block is REQUIRED to start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(debug=False, host=host, port=port)
