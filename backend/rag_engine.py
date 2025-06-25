import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import json

class HealthRAGEngine:
    def __init__(self, docs_path: str = None, index_path: str = None):
        # Use absolute paths for deployment
        if docs_path is None:
            docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
        if index_path is None:
            index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index_store")
        
        self.docs_path = docs_path
        self.index_path = index_path
        
        # Create directories if they don't exist
        os.makedirs(self.index_path, exist_ok=True)
        
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=self.index_path)
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection("health_docs")
        except:
            self.collection = self.client.create_collection("health_docs")
        
        # Initialize the knowledge base
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Load documents and create embeddings if not already done"""
        if self.collection.count() == 0:
            self._load_documents()
    
    def _load_documents(self):
        """Load documents from the docs directory and create embeddings"""
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        doc_id = 0
        
        # Check if docs directory exists
        if not os.path.exists(self.docs_path):
            print(f"Docs directory not found: {self.docs_path}")
            return
        
        # Load all text files from docs directory
        for filename in os.listdir(self.docs_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.docs_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split content into chunks (paragraphs)
                    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                    
                    for i, paragraph in enumerate(paragraphs):
                        if len(paragraph) > 50:  # Only include substantial paragraphs
                            documents.append(paragraph)
                            embeddings.append(self.model.encode(paragraph).tolist())
                            metadatas.append({
                                "source": filename,
                                "chunk_id": i,
                                "type": "health_guidance"
                            })
                            ids.append(f"{filename}_{i}")
                            doc_id += 1
                except Exception as e:
                    print(f"Error loading file {filename}: {e}")
                    continue
        
        # Add documents to collection
        if documents:
            try:
                self.collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Loaded {len(documents)} document chunks into knowledge base")
            except Exception as e:
                print(f"Error adding documents to collection: {e}")
        else:
            print("No documents were loaded")
    
    def query(self, question: str, top_k: int = 3) -> Tuple[str, List[Dict]]:
        """
        Query the knowledge base and return an answer with sources
        
        Args:
            question: The user's health question
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            Tuple of (answer, sources)
        """
        try:
            # Encode the question
            question_embedding = self.model.encode(question).tolist()
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=top_k
            )
            
            # Extract relevant information
            relevant_chunks = results['documents'][0] if results['documents'] else []
            sources = results['metadatas'][0] if results['metadatas'] else []
            
            # Generate answer based on retrieved information
            answer = self._generate_answer(question, relevant_chunks, sources)
            
            return answer, sources
        except Exception as e:
            print(f"Error in query: {e}")
            return "I'm experiencing technical difficulties. Please try again later.", []
    
    def _generate_answer(self, question: str, chunks: List[str], sources: List[Dict]) -> str:
        """
        Generate a comprehensive answer based on retrieved chunks
        """
        if not chunks:
            return "I don't have specific information about that health topic. Please consult with a healthcare professional for personalized medical advice."
        
        # Combine relevant information
        combined_info = "\n\n".join(chunks)
        
        # Create a structured response
        response_parts = []
        
        # Add disclaimer
        response_parts.append("Based on general health guidelines, here's what I can tell you:")
        
        # Add relevant information
        response_parts.append(combined_info)
        
        # Add source information
        if sources:
            source_files = list(set([s['source'] for s in sources]))
            response_parts.append(f"\n\nThis information is based on: {', '.join(source_files)}")
        
        # Add medical disclaimer
        response_parts.append("\n\n⚠️ IMPORTANT: This is general health information only. For personalized medical advice, please consult with a qualified healthcare professional.")
        
        return "\n".join(response_parts)
    
    def get_health_tips(self, category: str = None) -> List[str]:
        """Get general health tips by category"""
        tips = {
            "nutrition": [
                "Eat a rainbow of fruits and vegetables daily",
                "Stay hydrated with at least 8 glasses of water",
                "Include lean proteins in every meal",
                "Limit processed foods and added sugars"
            ],
            "exercise": [
                "Aim for 150 minutes of moderate activity weekly",
                "Include strength training 2-3 times per week",
                "Take regular breaks from sitting",
                "Find activities you enjoy to stay motivated"
            ],
            "sleep": [
                "Get 7-9 hours of quality sleep nightly",
                "Maintain a consistent sleep schedule",
                "Create a relaxing bedtime routine",
                "Keep your bedroom cool, dark, and quiet"
            ],
            "mental_health": [
                "Practice stress management techniques",
                "Maintain social connections",
                "Take regular breaks and practice self-care",
                "Seek professional help when needed"
            ]
        }
        
        if category and category in tips:
            return tips[category]
        else:
            # Return tips from all categories
            all_tips = []
            for category_tips in tips.values():
                all_tips.extend(category_tips)
            return all_tips

# Global instance
rag_engine = None

def get_rag_engine():
    """Get or create the RAG engine instance"""
    global rag_engine
    if rag_engine is None:
        rag_engine = HealthRAGEngine()
    return rag_engine
