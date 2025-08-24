"""
GenAI-Powered Voice Banking Assistant
Fully Hands-Free Voice-Driven Banking Demo

Presented by:
- SRI MUTHU MANICHKAM I
- RAGUL G  
- SHREE HARIHARAN S
- MOVINDH S
"""

import streamlit as st
import time
import random
import re
from datetime import datetime
import hashlib
import speech_recognition as sr

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="GenAI Voice Banking Assistant", 
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------
# Initialize Session State
# ------------------------
if 'user_balance' not in st.session_state:
    st.session_state.user_balance = 25000.0
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []

# ------------------------
# Beneficiaries Database (UPI Simulation)
# ------------------------
BENEFICIARIES_DB = {
    "john doe": {"upi": "johndoe@paytm", "name": "John Doe", "verified": True},
    "jane smith": {"upi": "janesmith@gpay", "name": "Jane Smith", "verified": True},
    "alice": {"upi": "alice@phonepe", "name": "Alice Johnson", "verified": True},
    "bob": {"upi": "bob@paytm", "name": "Bob Wilson", "verified": True},
    "mike": {"upi": "mike@gpay", "name": "Mike Brown", "verified": True},
    "sarah": {"upi": "sarah@phonepe", "name": "Sarah Davis", "verified": True},
    "amit": {"upi": "amit@upi", "name": "Amit Kumar", "verified": True},
    "priya": {"upi": "priya@gpay", "name": "Priya Sharma", "verified": True}
}

# ------------------------
# Voice Command Function
# ------------------------
def get_voice_command():
    """Record audio from microphone and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak now")
        audio = r.listen(source, phrase_time_limit=5)  # listen 5 seconds
    try:
        command = r.recognize_google(audio)
        st.success(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio. Try again.")
        return None
    except sr.RequestError:
        st.error("❌ Speech Recognition service error")
        return None

# ------------------------
# GenAI Processor Simulation
# ------------------------
class GenAIProcessor:
    """Generative AI Processing for Intent Recognition and Entity Extraction"""
    def extract_entities(self, text: str):
        text = text.lower().strip()
        entities = {"amount": None, "recipient": None}
        # Extract amount
        match = re.search(r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\b', text)
        if match:
            entities["amount"] = float(match.group(1).replace(',', ''))
        # Extract recipient
        for name in BENEFICIARIES_DB.keys():
            if name in text:
                entities["recipient"] = name
                break
        return entities

# ------------------------
# UPI Transaction Engine
# ------------------------
class UPITransactionEngine:
    """Simulated UPI Transaction Engine"""
    def validate_transaction(self, amount: float, recipient: str, sender_balance: float):
        result = {"valid": True, "errors": []}
        if amount <= 0:
            result["valid"] = False
            result["errors"].append("Amount must be greater than zero")
        if amount > sender_balance:
            result["valid"] = False
            result["errors"].append(f"Insufficient balance. Available: ₹{sender_balance:,.2f}")
        if recipient.lower() not in BENEFICIARIES_DB:
            result["valid"] = False
            result["errors"].append(f"Recipient '{recipient}' not found")
        return result

    def process_transaction(self, sender_id: str, amount: float, recipient: str):
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
        recipient_info = BENEFICIARIES_DB.get(recipient.lower())
        transaction = {
            "transaction_id": transaction_id,
            "sender_id": sender_id,
            "recipient_name": recipient_info["name"] if recipient_info else recipient,
            "recipient_upi": recipient_info["upi"] if recipient_info else f"{recipient}@upi",
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS",
            "transaction_type": "UPI_TRANSFER"
        }
        st.session_state.user_balance -= amount
        st.session_state.transaction_history.append(transaction)
        return transaction

# ------------------------
# Hands-Free Transaction Function
# ------------------------
def process_money_transfer_handsfree(voice_command: str, user_id: str):
    ai_processor = GenAIProcessor()
    entities = ai_processor.extract_entities(voice_command)
    
    amount = entities.get("amount")
    recipient = entities.get("recipient")
    
    if not amount or not recipient:
        st.error("❌ Could not detect amount or recipient from voice command")
        return
    
    # Validate transaction
    upi_engine = UPITransactionEngine()
    validation = upi_engine.validate_transaction(amount, recipient, st.session_state.user_balance)
    
    if not validation["valid"]:
        st.error("❌ Transaction validation failed:\n" + "\n".join(validation["errors"]))
        return
    
    # Process transaction automatically
    transaction = upi_engine.process_transaction(user_id, amount, recipient)
    
    # Show success message
    success_message = f"""✅ Transaction Successful!
💸 Amount: ₹{transaction['amount']:,.2f}  
👤 Recipient: {transaction['recipient_name']}  
💰 New Balance: ₹{st.session_state.user_balance:,.2f}  
📋 Transaction ID: {transaction['transaction_id']}  
"""
    st.success(success_message)
    
    # Play confirmation sound
    st.audio("success_sound.mp3", format='audio/mp3')

# ------------------------
# Streamlit UI
# ------------------------
st.title("🏦 GenAI Voice Banking Assistant (Hands-Free Demo)")

st.sidebar.header("👤 Account Info")
st.sidebar.metric("Balance", f"₹{st.session_state.user_balance:,.2f}")
st.sidebar.metric("Transactions", len(st.session_state.transaction_history))

st.header("🎙️ Voice Command")
st.write("Click the button and speak your command (e.g., 'Send 1500 to John Doe')")

if st.button("🎤 Speak Command"):
    voice_command = get_voice_command()
    if voice_command:
        process_money_transfer_handsfree(voice_command, "demo_user")

# Transaction History
if st.session_state.transaction_history:
    st.header("📋 Recent Transactions")
    for txn in reversed(st.session_state.transaction_history[-10:]):
        st.write(f"✅ ₹{txn['amount']:,.2f} → {txn['recipient_name']} | ID: {txn['transaction_id']}")
else:
    st.info("No transactions yet. Speak a command to try!")

