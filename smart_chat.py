#!/usr/bin/env python3
"""
Smart Healthcare AI Chat - Handles Any Health Question
=====================================================

An intelligent healthcare AI that can respond to any health question
while maintaining safety guardrails.
"""

import asyncio
import re
import logging

# Disable verbose logging
logging.getLogger().setLevel(logging.ERROR)

class SmartHealthcareAI:
    """Smart healthcare AI that can handle diverse health questions"""
    
    def __init__(self):
        # Health topics and general knowledge
        self.health_knowledge = {
            'symptoms': {
                'fever': 'elevated body temperature, often indicating infection or illness',
                'headache': 'pain in the head or neck area, can have various causes',
                'cough': 'reflex action to clear airways, may indicate respiratory issues',
                'fatigue': 'extreme tiredness, can result from many conditions',
                'nausea': 'feeling of sickness or urge to vomit',
                'dizziness': 'feeling unsteady or lightheaded',
                'pain': 'unpleasant sensation signaling potential tissue damage'
            },
            'conditions': {
                'diabetes': 'condition affecting blood sugar regulation',
                'hypertension': 'high blood pressure condition',
                'asthma': 'respiratory condition causing breathing difficulties',
                'arthritis': 'joint inflammation causing pain and stiffness',
                'depression': 'mental health condition affecting mood',
                'anxiety': 'mental health condition causing excessive worry',
                'obesity': 'condition of excess body weight',
                'cancer': 'disease involving abnormal cell growth'
            },
            'body_systems': {
                'heart': 'pumps blood throughout the body',
                'lungs': 'organs responsible for breathing and gas exchange',
                'liver': 'organ that processes nutrients and toxins',
                'kidneys': 'organs that filter waste from blood',
                'brain': 'central nervous system control center',
                'immune system': 'body\'s defense against infections',
                'digestive system': 'processes food and absorbs nutrients',
                'nervous system': 'controls body functions and responses'
            },
            'treatments': {
                'exercise': 'physical activity that improves health and fitness',
                'diet': 'food choices that affect health and nutrition',
                'medication': 'substances used to treat medical conditions',
                'therapy': 'treatment approaches for various conditions',
                'surgery': 'medical procedures involving incisions',
                'vaccination': 'immunization to prevent diseases'
            }
        }
    
    def _check_medical_advice(self, message: str) -> bool:
        """Check if message requests medical advice"""
        advice_patterns = [
            r'\b(what do i have|diagnose me|what\'s wrong with me)\b',
            r'\b(what medication|prescribe|prescription|should i take)\b',
            r'\b(what treatment|how to treat|cure me|fix my)\b',
            r'\b(am i sick|do i have|is this serious)\b',
            r'\b(how much.*take|dosage|dose)\b',
            r'\b(should i see|need to go|visit doctor)\b'
        ]
        return any(re.search(p, message.lower()) for p in advice_patterns)
    
    def _check_prompt_injection(self, message: str) -> bool:
        """Check for prompt injection attempts"""
        injection_patterns = [
            r'\b(ignore previous|forget everything|override|bypass)\b',
            r'\b(you are now|pretend you are|act like|roleplay)\b',
            r'\b(system message|show.*prompt|reveal.*instructions)\b',
            r'\b(developer|administrator|creator|owner)\b.*\b(override|bypass|disable)\b'
        ]
        return any(re.search(p, message.lower()) for p in injection_patterns)
    
    def _check_privacy_violation(self, message: str) -> bool:
        """Check for personal information sharing"""
        privacy_patterns = [
            r'\b(my name is|i am \w+|call me \w+)\b',
            r'\b(ssn|social security|insurance.*number)\b',
            r'\b(phone.*number|address|email|zip code)\b',
            r'\b(patient.*id|medical.*record|chart.*number)\b',
            r'\b(born on|date.*birth|dob)\b'
        ]
        return any(re.search(p, message.lower()) for p in privacy_patterns)
    
    def _check_self_harm(self, message: str) -> bool:
        """Check for self-harm or crisis content"""
        crisis_patterns = [
            r'\b(kill myself|suicide|end.*life|hurt myself)\b',
            r'\b(want to die|end it all|don\'t want.*live)\b',
            r'\b(overdose|lethal.*dose|how.*die)\b'
        ]
        return any(re.search(p, message.lower()) for p in crisis_patterns)
    
    def _is_health_related(self, message: str) -> bool:
        """Check if message is health-related"""
        health_keywords = [
            'health', 'medical', 'doctor', 'hospital', 'disease', 'condition',
            'symptom', 'treatment', 'medicine', 'body', 'pain', 'sick',
            'wellness', 'fitness', 'nutrition', 'diet', 'exercise', 'sleep',
            'stress', 'mental', 'physical', 'prevention', 'vaccine'
        ]
        
        # Check for health keywords
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in health_keywords):
            return True
        
        # Check for body parts/systems
        body_parts = [
            'heart', 'lung', 'liver', 'kidney', 'brain', 'stomach', 'head',
            'chest', 'back', 'arm', 'leg', 'eye', 'ear', 'throat', 'skin'
        ]
        if any(part in message_lower for part in body_parts):
            return True
        
        # Check for common conditions/symptoms
        conditions = list(self.health_knowledge['symptoms'].keys()) + list(self.health_knowledge['conditions'].keys())
        if any(condition in message_lower for condition in conditions):
            return True
        
        return False
    
    def _generate_health_response(self, message: str) -> str:
        """Generate intelligent health response"""
        message_lower = message.lower()
        
        # Find relevant health topics in the message
        relevant_info = []
        
        # Check symptoms
        for symptom, description in self.health_knowledge['symptoms'].items():
            if symptom in message_lower:
                relevant_info.append(f"{symptom.title()}: {description}")
        
        # Check conditions
        for condition, description in self.health_knowledge['conditions'].items():
            if condition in message_lower:
                relevant_info.append(f"{condition.title()}: {description}")
        
        # Check body systems
        for system, description in self.health_knowledge['body_systems'].items():
            if system in message_lower:
                relevant_info.append(f"{system.title()}: {description}")
        
        # Check treatments
        for treatment, description in self.health_knowledge['treatments'].items():
            if treatment in message_lower:
                relevant_info.append(f"{treatment.title()}: {description}")
        
        if relevant_info:
            # Provide specific information found
            response = ". ".join(relevant_info[:2])  # Limit to 2 most relevant
            return f"{response}. Always consult healthcare professionals for personal medical advice."
        
        # General health response for questions we don't have specific info about
        if any(word in message_lower for word in ['what is', 'tell me about', 'explain', 'how does']):
            return "This appears to be a general health question. While I can provide basic health education, I recommend consulting medical resources or healthcare professionals for detailed information about specific health topics."
        
        if any(word in message_lower for word in ['prevent', 'avoid', 'reduce risk']):
            return "Prevention strategies vary by condition but often include healthy lifestyle choices like regular exercise, balanced nutrition, adequate sleep, and routine medical checkups. Consult your healthcare provider for personalized prevention advice."
        
        if any(word in message_lower for word in ['cause', 'why', 'reason']):
            return "Health conditions can have multiple causes including genetics, lifestyle factors, environmental influences, and infections. A healthcare professional can help identify specific causes relevant to individual situations."
        
        # Default health education response
        return "I can provide general health information for educational purposes. For specific medical questions, detailed information, or personal health concerns, please consult qualified healthcare professionals."
    
    async def process_message(self, message: str) -> dict:
        """Process message and return appropriate response"""
        
        # Check for self-harm (highest priority)
        if self._check_self_harm(message):
            return {
                "blocked": True,
                "response": "🚨 CRISIS SUPPORT: National Suicide Prevention Lifeline: 988 | Crisis Text Line: Text HOME to 741741 | Emergency: 911"
            }
        
        # Check for prompt injection
        if self._check_prompt_injection(message):
            return {
                "blocked": True,
                "response": "🔒 SECURITY: I cannot modify my behavior or bypass safety guidelines. Please ask legitimate health questions."
            }
        
        # Check for privacy violations
        if self._check_privacy_violation(message):
            return {
                "blocked": True,
                "response": "🛡️ PRIVACY: I cannot process personal information. Please ask general health questions without sharing personal details."
            }
        
        # Check for medical advice requests
        if self._check_medical_advice(message):
            return {
                "blocked": True,
                "response": "⚕️ MEDICAL SAFETY: I cannot diagnose, prescribe, or provide medical advice. Please consult a healthcare professional."
            }
        
        # Check if it's health-related
        if not self._is_health_related(message):
            return {
                "blocked": False,
                "response": "I'm designed to discuss health topics. Please ask questions about health, wellness, medical conditions, or general health information."
            }
        
        # Generate intelligent health response
        return {
            "blocked": False,
            "response": self._generate_health_response(message)
        }

async def main():
    """Main chat loop"""
    ai = SmartHealthcareAI()
    
    print("🏥 Smart Healthcare AI Chat")
    print("=" * 40)
    print("Ask any health question or type 'quit' to exit")
    print("I can discuss symptoms, conditions, body systems, and general health topics")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Stay healthy!")
                break
            
            if not user_input:
                continue
            
            result = await ai.process_message(user_input)
            
            if result['blocked']:
                print(f"🚫 BLOCKED: {result['response']}")
            else:
                print(f"✅ AI: {result['response']}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Stay healthy!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())