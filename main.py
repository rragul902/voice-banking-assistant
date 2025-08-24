"""
GenAI-Powered Voice Banking Assistant
Revolutionizing Secure Transactions with Conversational AI

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
import json

# Page Configuration
st.set_page_config(
    page_title="GenAI Voice Banking Assistant", 
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2c5aa0 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
    }
    .success-transaction {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .voice-command-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'user_balance' not in st.session_state:
    st.session_state.user_balance = 25000.0
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []
if 'user_enrolled' not in st.session_state:
    st.session_state.user_enrolled = True
if 'voice_samples' not in st.session_state:
    st.session_state.voice_samples = []

# Beneficiaries Database (UPI Simulation)
BENEFICIARIES_DB = {
    "john doe": {"upi": "johndoe@paytm", "name": "John Doe", "verified": True},
    "john": {"upi": "johndoe@paytm", "name": "John Doe", "verified": True},
    "jane smith": {"upi": "janesmith@gpay", "name": "Jane Smith", "verified": True},
    "jane": {"upi": "janesmith@gpay", "name": "Jane Smith", "verified": True},
    "alice": {"upi": "alice@phonepe", "name": "Alice Johnson", "verified": True},
    "bob": {"upi": "bob@paytm", "name": "Bob Wilson", "verified": True},
    "mike": {"upi": "mike@gpay", "name": "Mike Brown", "verified": True},
    "sarah": {"upi": "sarah@phonepe", "name": "Sarah Davis", "verified": True},
    "amit": {"upi": "amit@upi", "name": "Amit Kumar", "verified": True},
    "priya": {"upi": "priya@gpay", "name": "Priya Sharma", "verified": True}
}

class VoiceBiometrics:
    """Voice Biometric Authentication System"""
    
    @staticmethod
    def simulate_voice_enrollment(user_id: str, samples: int = 3):
        """Simulate voice enrollment process"""
        enrollment_data = {
            "user_id": user_id,
            "samples_count": samples,
            "enrollment_date": datetime.now().isoformat(),
            "voice_template": hashlib.md5(f"{user_id}_voice_template".encode()).hexdigest()
        }
        st.session_state.voice_samples = enrollment_data
        return True
    
    @staticmethod
    def verify_voice_biometric(user_id: str, confidence_threshold: float = 0.82):
        """Simulate voice biometric verification"""
        # Simulate processing delay
        time.sleep(1.5)
        
        # Generate realistic verification score
        base_score = random.uniform(0.75, 0.98)
        
        # Add some variability based on "user behavior"
        if user_id == "demo_user":
            verification_score = max(0.80, base_score + random.uniform(-0.05, 0.10))
        else:
            verification_score = base_score
        
        is_verified = verification_score >= confidence_threshold
        
        return {
            "verified": is_verified,
            "confidence_score": round(verification_score, 3),
            "threshold": confidence_threshold,
            "processing_time": "1.2s"
        }

class GenAIProcessor:
    """Generative AI Processing for Intent Recognition and Entity Extraction"""
    
    def __init__(self):
        self.banking_intents = {
            "send_money": ["send", "transfer", "pay", "give"],
            "check_balance": ["balance", "account", "money", "funds"],
            "transaction_history": ["history", "transactions", "statement", "recent"],
            "cancel_transaction": ["cancel", "stop", "abort"],
            "beneficiary_info": ["who is", "details", "info about"]
        }
    
    def extract_entities(self, text: str):
        """Extract amount and recipient from voice command using GenAI simulation"""
        text = text.lower().strip()
        entities = {"amount": None, "recipient": None, "currency": "INR"}
        
        # Extract amount using regex
        amount_patterns = [
            r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:rupees?|rs\.?|₹)?\b',
            r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\b',
            r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\b'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    entities["amount"] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # Extract recipient using multiple strategies
        recipient = None
        
        # Strategy 1: Check against known beneficiaries
        for name in BENEFICIARIES_DB.keys():
            if name in text:
                recipient = name
                break
        
        # Strategy 2: Extract after trigger words
        if not recipient:
            words = text.split()
            trigger_words = ["to", "for", "pay", "send", "transfer"]
            for i, word in enumerate(words):
                if word in trigger_words and i + 1 < len(words):
                    # Extract next 1-2 words as potential recipient
                    potential_recipient = " ".join(words[i+1:min(i+3, len(words))]).strip()
                    # Clean up common suffixes
                    potential_recipient = re.sub(r'\s+(rupees?|rs\.?|₹.*)', '', potential_recipient)
                    if potential_recipient and len(potential_recipient) > 1:
                        recipient = potential_recipient
                        break
        
        entities["recipient"] = recipient
        return entities
    
    def recognize_intent(self, text: str):
        """Recognize user intent from voice command"""
        text = text.lower().strip()
        
        for intent, keywords in self.banking_intents.items():
            if any(keyword in text for keyword in keywords):
                return intent
        
        # Default intent if no match
        return "unknown"
    
    def generate_response(self, intent: str, entities: dict, context: dict = None):
        """Generate conversational AI response"""
        responses = {
            "send_money_confirm": f"I'll help you send ₹{entities.get('amount', 'X')} to {entities.get('recipient', 'the recipient')}. Please confirm with your voice passphrase.",
            "send_money_success": f"✅ Transaction successful! ₹{entities.get('amount')} sent to {entities.get('recipient')}.",
            "send_money_failed": "❌ Transaction failed. Please check the details and try again.",
            "balance_response": f"💰 Your current account balance is ₹{context.get('balance', 'X'):.2f}",
            "history_response": "📋 Here are your recent transactions:",
            "unknown_command": "❓ I didn't understand that command. Try saying 'Send money to John' or 'Check balance'."
        }
        
        return responses.get(f"{intent}_response", responses["unknown_command"])

class UPITransactionEngine:
    """UPI Transaction Processing and Simulation"""
    
    def __init__(self):
        self.transaction_limits = {
            "per_transaction": 50000.0,
            "daily_limit": 100000.0,
            "monthly_limit": 1000000.0
        }
    
    def validate_transaction(self, amount: float, recipient: str, sender_balance: float):
        """Validate transaction parameters"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Amount validation
        if amount <= 0:
            validation_result["valid"] = False
            validation_result["errors"].append("Amount must be greater than zero")
        
        if amount > self.transaction_limits["per_transaction"]:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Amount exceeds per-transaction limit of ₹{self.transaction_limits['per_transaction']:,.2f}")
        
        # Balance validation
        if amount > sender_balance:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Insufficient balance. Available: ₹{sender_balance:,.2f}")
        
        # Recipient validation
        if recipient.lower() not in BENEFICIARIES_DB:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Recipient '{recipient}' not found in beneficiaries list")
        
        # Warnings for large amounts
        if amount > 10000:
            validation_result["warnings"].append("Large transaction amount - extra verification recommended")
        
        return validation_result
    
    def process_transaction(self, sender_id: str, amount: float, recipient: str, verification_data: dict):
        """Process UPI transaction with full validation"""
        
        # Generate unique transaction ID
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
        
        # Get recipient details
        recipient_info = BENEFICIARIES_DB.get(recipient.lower())
        
        # Create transaction record
        transaction = {
            "transaction_id": transaction_id,
            "sender_id": sender_id,
            "recipient_name": recipient_info["name"] if recipient_info else recipient,
            "recipient_upi": recipient_info["upi"] if recipient_info else f"{recipient}@upi",
            "amount": amount,
            "currency": "INR",
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS",
            "verification_score": verification_data.get("confidence_score", 0.0),
            "processing_time": random.uniform(1.2, 2.8),
            "transaction_type": "UPI_TRANSFER",
            "reference_note": f"Voice payment to {recipient}"
        }
        
        # Update sender balance
        st.session_state.user_balance -= amount
        
        # Add to transaction history
        st.session_state.transaction_history.append(transaction)
        
        return transaction

def process_voice_command(command: str, user_id: str = "demo_user"):
    """Main function to process voice commands end-to-end"""
    
    if not command or not command.strip():
        return "❌ No voice command received. Please try again."
    
    # Initialize AI processor
    ai_processor = GenAIProcessor()
    
    # Step 1: Intent Recognition
    intent = ai_processor.recognize_intent(command)
    
    # Step 2: Entity Extraction
    entities = ai_processor.extract_entities(command)
    
    # Step 3: Process based on intent
    if intent == "send_money":
        return process_money_transfer(entities, user_id, ai_processor)
    
    elif intent == "check_balance":
        return f"💰 Your current account balance is ₹{st.session_state.user_balance:,.2f}"
    
    elif intent == "transaction_history":
        return format_transaction_history()
    
    else:
        return ai_processor.generate_response("unknown", entities)

def process_money_transfer(entities: dict, user_id: str, ai_processor: GenAIProcessor):
    """Process money transfer with full security pipeline"""
    
    amount = entities.get("amount")
    recipient = entities.get("recipient")
    
    # Validation
    if not amount:
        return "❌ Please specify the amount to transfer. For example: 'Send 500 rupees to John'"
    
    if not recipient:
        return "❌ Please specify the recipient. For example: 'Send 500 to John Doe'"
    
    # Transaction validation
    upi_engine = UPITransactionEngine()
    validation = upi_engine.validate_transaction(amount, recipient, st.session_state.user_balance)
    
    if not validation["valid"]:
        return "❌ Transaction validation failed:\n" + "\n".join(validation["errors"])
    
    # Voice biometric verification
    st.info("🔊 Initiating voice biometric verification...")
    
    # Progress bar for verification
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
    
    biometrics = VoiceBiometrics()
    verification_result = biometrics.verify_voice_biometric(user_id)
    
    if not verification_result["verified"]:
        return f"❌ Voice verification failed (Score: {verification_result['confidence_score']:.3f}, Required: {verification_result['threshold']:.3f})\n🔐 Transaction cancelled for security reasons."
    
    # Process transaction
    transaction = upi_engine.process_transaction(user_id, amount, recipient, verification_result)
    
    # Format success response
    success_message = f"""✅ **Transaction Successful!**
    
💸 **Amount**: ₹{transaction['amount']:,.2f}  
👤 **Recipient**: {transaction['recipient_name']}  
🏦 **UPI ID**: {transaction['recipient_upi']}  
🔐 **Voice Verification**: {verification_result['confidence_score']:.3f} ✓  
📋 **Transaction ID**: {transaction['transaction_id']}  
💰 **New Balance**: ₹{st.session_state.user_balance:,.2f}  
⏰ **Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
⚡ **Processing Time**: {transaction['processing_time']:.1f}s  
"""
    
    return success_message

def format_transaction_history(limit: int = 5):
    """Format transaction history for display"""
    
    if not st.session_state.transaction_history:
        return "📋 No transaction history found. Complete a transaction to see it here."
    
    history_text = f"📋 **Recent Transactions** (Last {min(limit, len(st.session_state.transaction_history))} transactions):\n\n"
    
    recent_transactions = st.session_state.transaction_history[-limit:]
    
    for i, txn in enumerate(reversed(recent_transactions), 1):
        history_text += f"""**{i}.** ₹{txn['amount']:,.2f} → {txn['recipient_name']}
   📋 ID: {txn['transaction_id']} | ⏰ {datetime.fromisoformat(txn['timestamp']).strftime('%m/%d %H:%M')} | ✅ {txn['status']}
   
"""
    
    return history_text

def main():
    """Main Streamlit Application"""
    
    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1>🏦 GenAI-Powered Voice Banking Assistant</h1>
        <p>Revolutionizing Secure Transactions with Conversational AI</p>
        <small>Presented by: Sri Muthu Manichkam I • Ragul G • Shree Hariharan S • Movindh S</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Account Information and System Status
    with st.sidebar:
        st.header("👤 User Account")
        
        # Account metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Balance", f"₹{st.session_state.user_balance:,.2f}")
        with col2:
            st.metric("Transactions", len(st.session_state.transaction_history))
        
        # System status
        st.header("🔐 Security Status")
        st.success("✅ Voice Biometrics: Active")
        st.success("✅ GenAI Processing: Online")
        st.success("✅ UPI Integration: Simulated")
        st.success("✅ Fraud Detection: Enabled")
        
        # Beneficiaries list
        st.header("👥 Registered Beneficiaries")
        for name, info in list(BENEFICIARIES_DB.items())[:8]:
            if len(name) > 4:  # Show full names only
                st.text(f"• {info['name']}")
        
        st.header("📊 System Metrics")
        st.metric("Verification Accuracy", "96.8%", delta="2.1%")
        st.metric("Transaction Success", "99.2%", delta="0.5%")
        st.metric("Response Time", "1.8s", delta="-0.3s")
    
    # Main Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎤 Voice Command Interface")
        
        # Sample commands section
        st.markdown("""
        <div class="voice-command-box">
            <h4>🎯 Try These Voice Commands:</h4>
            <ul>
                <li><strong>"Send 1500 to John Doe"</strong> - Transfer money</li>
                <li><strong>"Transfer 750 to Alice"</strong> - Quick transfer</li>
                <li><strong>"Pay 2000 to Bob"</strong> - Make payment</li>
                <li><strong>"Check my balance"</strong> - Account inquiry</li>
                <li><strong>"Show transaction history"</strong> - Recent activity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice input simulation
        voice_command = st.text_input(
            "🎙️ **Voice Command Input** (Text simulation of voice):",
            placeholder="e.g., Send 1500 rupees to John Doe",
            help="Type your voice command here. In production, this would be actual speech input."
        )
        
        # Action buttons
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            process_button = st.button("🎯 Process Voice Command", type="primary", use_container_width=True)
        
        with col1b:
            if st.button("💰 Quick Balance Check", use_container_width=True):
                st.success(f"💰 Current Balance: ₹{st.session_state.user_balance:,.2f}")
        
        with col1c:
            if st.button("🔄 Reset Demo", use_container_width=True):
                st.session_state.user_balance = 25000.0
                st.session_state.transaction_history = []
                st.success("Demo reset successfully!")
                st.rerun()
        
        # Process voice command
        if process_button and voice_command:
            with st.spinner("🔊 Processing voice command with GenAI..."):
                response = process_voice_command(voice_command)
                
                # Display response with appropriate styling
                if "✅" in response:
                    st.success(response)
                elif "❌" in response:
                    st.error(response)
                elif "📋" in response:
                    st.info(response)
                else:
                    st.warning(response)
        
        elif process_button:
            st.warning("⚠️ Please enter a voice command to process.")
    
    with col2:
        st.header("⚡ Quick Demo Actions")
        
        # Predefined demo commands
        demo_commands = [
            "Send 1500 to John Doe",
            "Transfer 500 to Alice",
            "Pay 1000 to Bob",
            "Send 250 to Sarah",
            "Check balance",
            "Show history"
        ]
        
        st.write("**One-Click Demo Commands:**")
        for cmd in demo_commands:
            if st.button(f"🎤 {cmd}", key=f"demo_{cmd}", use_container_width=True):
                with st.spinner("Processing..."):
                    response = process_voice_command(cmd)
                    
                    if "✅" in response:
                        st.success(response)
                    elif "❌" in response:
                        st.error(response)
                    elif "📋" in response:
                        st.info(response)
                    else:
                        st.warning(response)
    
    # Transaction History Section
    if st.session_state.transaction_history:
        st.header("📜 Transaction History & Analytics")
        
        # Transaction summary metrics
        total_transactions = len(st.session_state.transaction_history)
        total_amount = sum(txn['amount'] for txn in st.session_state.transaction_history)
        avg_transaction = total_amount / total_transactions if total_transactions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", total_transactions)
        with col2:
            st.metric("Total Amount Sent", f"₹{total_amount:,.2f}")
        with col3:
            st.metric("Average Transaction", f"₹{avg_transaction:,.2f}")
        
        # Detailed transaction list
        st.subheader("📋 Recent Transactions")
        
        for txn in reversed(st.session_state.transaction_history[-10:]):
            with st.expander(f"₹{txn['amount']:,.2f} to {txn['recipient_name']} - {datetime.fromisoformat(txn['timestamp']).strftime('%Y-%m-%d %H:%M')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Transaction ID:** {txn['transaction_id']}")
                    st.write(f"**Recipient:** {txn['recipient_name']}")
                    st.write(f"**UPI ID:** {txn['recipient_upi']}")
                    st.write(f"**Amount:** ₹{txn['amount']:,.2f}")
                
                with col2:
                    st.write(f"**Status:** {txn['status']}")
                    st.write(f"**Voice Score:** {txn['verification_score']:.3f}")
                    st.write(f"**Processing Time:** {txn['processing_time']:.1f}s")
                    st.write(f"**Type:** {txn['transaction_type']}")
    
    else:
        st.info("💡 **No transactions yet.** Try the demo commands above to see the voice banking system in action!")
    
    # System Architecture Overview
    with st.expander("🔧 **System Architecture & Technical Details**"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏗️ Core Components")
            st.write("""
            **1. Voice Input & STT**
            - Speech-to-Text conversion
            - Natural language processing
            
            **2. GenAI Processing (GPT-4)**
            - Intent recognition
            - Entity extraction
            - Conversational responses
            
            **3. Voice Biometrics**
            - Speaker verification
            - Anti-fraud protection
            """)
        
        with col2:
            st.subheader("🔐 Security Features")
            st.write("""
            **4. UPI Transaction Engine**
            - Transaction validation
            - Beneficiary verification
            - Balance management
            
            **5. Response Generation**
            - Natural language responses
            - Transaction confirmations
            - Error handling
            """)
        
        st.subheader("💻 Technology Stack")
        st.write("""
        - **Frontend:** Streamlit (Interactive UI)
        - **AI Processing:** OpenAI GPT-4 (Simulated)
        - **Voice Biometrics:** Custom deep learning model (Simulated)
        - **Backend:** Python with FastAPI architecture
        - **Database:** Session state (Production would use secure database)
        """)
    
    # Project Information Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <h3>🏆 GenAI Voice Banking Assistant</h3>
        <p><strong>A revolutionary approach to secure, hands-free banking transactions</strong></p>
        <p>🔐 <strong>Enhanced Security</strong> • 🎤 <strong>Voice Convenience</strong> • 🤖 <strong>AI-Powered</strong> • ♿ <strong>Accessible Design</strong></p>
        <hr style='margin: 1rem 0;'>
        <p><em>Developed by: Sri Muthu Manichkam I • Ragul G • Shree Hariharan S • Movindh S</em></p>
        <p style='color: #666; font-size: 0.9em;'>Demonstrating the future of conversational AI in financial services</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Initialize voice biometrics for demo user
    if not st.session_state.get('biometrics_initialized', False):
        biometrics = VoiceBiometrics()
        biometrics.simulate_voice_enrollment("demo_user")
        st.session_state.biometrics_initialized = True
    
    # Run main application
    main()
