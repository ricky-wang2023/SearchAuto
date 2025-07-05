import os
import chromadb
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Dict, Any
import json
import pickle
from datetime import datetime
import re
from transformers import pipeline

class AISearchEngine:
    def __init__(self, db_path="ai_search_db"):
        """Initialize AI search engine with SentenceTransformers and ChromaDB"""
        self.db_path = db_path
        self.model = None
        self.client = None
        self.collection = None
        self.summarizer = None
        self.initialized = False
        
    def initialize(self):
        """Initialize the AI search components"""
        try:
            # Initialize SentenceTransformer model (MiniLM for speed)
            print("Loading AI model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB
            print("Initializing ChromaDB...")
            self.client = chromadb.PersistentClient(path=self.db_path)
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection("file_content")
            except:
                self.collection = self.client.create_collection("file_content")
            
            # Initialize summarizer for document summarization
            print("Loading summarization model...")
            try:
                self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
            except:
                print("Summarization model not available, continuing without it...")
                self.summarizer = None
            
            self.initialized = True
            print("AI Search Engine initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Error initializing AI search: {e}")
            return False
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the AI search index"""
        if not self.initialized:
            if not self.initialize():
                return False
        
        try:
            # Prepare documents for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for doc in documents:
                file_path = doc['file_path']
                content = doc['content']
                file_type = doc['file_type']
                
                # Split content into chunks for better search
                chunks = self._split_content(content)
                
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{file_path}_{i}"
                    ids.append(chunk_id)
                    texts.append(chunk)
                    metadatas.append({
                        'file_path': file_path,
                        'file_type': file_type,
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    })
            
            # Add to ChromaDB in smaller batches to avoid batch size errors
            if ids:
                batch_size = 1000  # Smaller batch size
                for i in range(0, len(ids), batch_size):
                    batch_ids = ids[i:i+batch_size]
                    batch_texts = texts[i:i+batch_size]
                    batch_metadatas = metadatas[i:i+batch_size]
                    
                    self.collection.add(
                        documents=batch_texts,
                        metadatas=batch_metadatas,
                        ids=batch_ids
                    )
                    print(f"Added batch {i//batch_size + 1} ({len(batch_ids)} chunks)")
                
                print(f"Added {len(ids)} total document chunks to AI index")
                return True
                
        except Exception as e:
            print(f"Error adding documents to AI index: {e}")
            return False
    
    def search(self, query: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """Search documents using semantic similarity"""
        if not self.initialized:
            if not self.initialize():
                return []
        
        try:
            # Enhanced query processing
            enhanced_query = self._enhance_query(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_texts=[enhanced_query],
                n_results=n_results
            )
            
            # Process results
            processed_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    
                    # Generate summary if summarizer is available
                    summary = None
                    if self.summarizer and len(doc) > 100:
                        try:
                            summary_result = self.summarizer(doc[:1024], max_length=150, min_length=50, do_sample=False)
                            summary = summary_result[0]['summary_text']
                        except:
                            summary = None
                    
                    processed_results.append({
                        'file_path': metadata['file_path'],
                        'file_type': metadata['file_type'],
                        'content': doc,
                        'summary': summary,
                        'similarity_score': 1 - distance,  # Convert distance to similarity
                        'chunk_index': metadata['chunk_index'],
                        'total_chunks': metadata['total_chunks']
                    })
            
            return processed_results
            
        except Exception as e:
            print(f"Error in AI search: {e}")
            return []
    
    def _enhance_query(self, query: str) -> str:
        """Enhance query with synonyms and context"""
        # Add common synonyms and related terms
        synonyms = {
            'file': ['document', 'file', 'file'],
            'document': ['file', 'document', 'paper'],
            'search': ['find', 'look', 'seek', 'locate'],
            'open': ['access', 'view', 'read'],
            'save': ['store', 'keep', 'preserve'],
            'delete': ['remove', 'erase', 'clear'],
            'create': ['make', 'build', 'generate'],
            'update': ['modify', 'change', 'edit'],
            'error': ['problem', 'issue', 'bug', 'fault'],
            'help': ['support', 'assist', 'guide'],
            'test': ['check', 'verify', 'validate'],
            'install': ['setup', 'configure', 'deploy'],
            'download': ['get', 'fetch', 'retrieve'],
            'upload': ['send', 'transfer', 'submit'],
            'email': ['mail', 'message', 'correspondence'],
            'meeting': ['conference', 'appointment', 'session'],
            'project': ['task', 'assignment', 'work'],
            'budget': ['cost', 'expense', 'financial'],
            'report': ['summary', 'analysis', 'documentation'],
            'data': ['information', 'records', 'details']
        }
        
        enhanced_query = query.lower()
        
        # Add synonyms for better matching
        for word, syns in synonyms.items():
            if word in enhanced_query:
                enhanced_query += " " + " ".join(syns)
        
        return enhanced_query
    
    def clear_index(self):
        """Clear the AI search index"""
        try:
            if self.client:
                self.client.delete_collection("file_content")
                self.collection = self.client.create_collection("file_content")
                print("AI search index cleared")
                return True
        except Exception as e:
            print(f"Error clearing AI index: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the AI search index"""
        try:
            if not self.collection:
                return {'total_documents': 0, 'index_size': '0 MB'}
            
            # Get collection count
            count = self.collection.count()
            
            # Estimate size
            size_mb = os.path.getsize(self.db_path) / (1024 * 1024) if os.path.exists(self.db_path) else 0
            
            return {
                'total_documents': count,
                'index_size': f"{size_mb:.2f} MB"
            }
            
        except Exception as e:
            print(f"Error getting AI index stats: {e}")
            return {'total_documents': 0, 'index_size': '0 MB'}
    
    def _split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into chunks for better semantic search"""
        if len(content) <= max_chunk_size:
            return [content]
        
        # Split by sentences first, then by size
        sentences = content.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]

# Global AI search engine instance
ai_engine = AISearchEngine()

def initialize_ai_search():
    """Initialize the AI search engine"""
    return ai_engine.initialize()

def add_documents_to_ai_index(documents):
    """Add documents to AI search index"""
    return ai_engine.add_documents(documents)

def ai_search(query, n_results=10):
    """Perform AI semantic search"""
    return ai_engine.search(query, n_results)

def clear_ai_index():
    """Clear AI search index"""
    return ai_engine.clear_index()

def get_ai_index_stats():
    """Get AI index statistics"""
    return ai_engine.get_index_stats() 