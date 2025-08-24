import streamlit as st
import time
import random
import re
from datetime import datetime
import json

# Initialize session state
if 'balance' not in st.session_state:
    st.session_state.balance = 25000.0
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'enrolled_users' not in st.session_state:
    st.session_state.enrolled_users = {"demo_user": "enrolled"}

# Beneficiaries database
BENEFICIARIES = {
    "john doe": "johndoe@upi",
    "john": "johndoe@upi", 
    "jane smith": "janesmith@upi",
    "jane": "janesmith@upi",
    "alice": "alice@upi",
    "bob": "bob@upi",
    "mike": "mike@upi",
    "sarah": "sarah@upi"
}

def extract_amount_and_recipient(text):
    """Extract amount and recipient from voice command"""
    text = text.lower().strip()
    
    # Extract amount (numbers)
    amount_match = re.search(r'\b(\d+(?:\.\d+)?)\b', text)
    amount = float(amount_match.group(1)) if amount_match else None
    
    # Extract recipient name
    recipient = None
    # Look for patterns like "to John", "pay Alice", etc.
    for name in BENEFICIARIES.keys():
        if name in text:
            recipient = name
            break
    
    # Alternative extraction - words after "to", "pay", etc.
    if not recipient:
        words = text.split()
        trigger_words = ["to", "pay", "send"]
        for i, word in enumerate(words):
            if word in trigger_words and i + 1 < len(words):
                # Take next 1-2 words as recipient
                potential_recipient = " ".join(words[i+1:i+3]).strip()
                if potential_recipient:
                    recipient = potential_recipient
                break
    
    return amount, recipient

def simulate_voice_biometrics():
    """Simulate voice biometric verification"""
    # Simulate processing time
    time.sleep(1)
    
    # Random verification with high success rate for demo
    verification_score = random.uniform(0.85, 0.98)
    is_verified = verification_score > 0.82
    
    return is_verified, verification_score

def process_voice_command(command):
    """Main function to process voice commands"""
    command = command.lower().strip()
    
    if not command:
        return "❌ No command received. Please try again."
    
    # Check balance
    if any(word in command for word in ["balance", "check balance", "account balance"]):
        return f"💰 Your current balance is ₹{st.session_state.balance:,.2f}"
    
    # Transaction history
    if any(word in command for word in ["history", "transactions", "recent"]):
        if st.session_state.transactions:
            history_text = "📋 Recent Transactions:\n\n"
            for txn in st.session_state.transactions[-5:]:
                history_text += f"• ₹{txn['amount']:,.2f} to {txn['recipient']} - {txn['status']}\n"
                history_text += f"  {txn['timestamp']} (ID: {txn['id']})\n\n"
            return history_text
        else:
            return "📋 No transaction history found."
    
    # Send money / Transfer / Pay
    if any(word in command for word in ["send", "transfer", "pay"]):
        amount, recipient = extract_amount_and_recipient(command)
        
        if not amount:
            return "❌ Please specify the amount to transfer."
        
        if not recipient:
            return "❌ Please specify the recipient name."
        
        # Validate amount
        if amount <= 0:
            return "❌ Amount must be greater than zero."
        
        if amount > 50000:
            return "❌ Transaction limit exceeded. Maximum amount is ₹50,000."
        
        if amount > st.session_state.balance:
            return f"❌ Insufficient balance. Your current balance is ₹{st.session_state.balance:,.2f}"
        
        # Check if recipient exists
        recipient_upi = BENEFICIARIES.get(recipient.lower())
        if not recipient_upi:
            return f"❌ Recipient '{recipient}' not found in your contacts.\nAvailable contacts: {', '.join(BENEFICIARIES.keys())}"
        
        # Voice biometric verification
        st.info("🔊 Voice biometric verification in progress...")
        verification_progress = st.progress(0)
        
        for i in range(100):
            verification_progress.progress(i + 1)
            time.sleep(0.01)
        
        is_verified, score = simulate_voice_biometrics()
        
        if not is_verified:
            return f"❌ Voice verification failed (Score: {score:.2f}). Transaction cancelled for security."
        
        # Process transaction
        transaction_id = f"TXN{int(time.time())}{random.randint(100, 999)}"
        
        # Deduct amount
        st.session_state.balance -= amount
        
        # Log transaction
        transaction = {
            "id": transaction_id,
            "amount": amount,
            "recipient": recipient,
            "recipient_upi": recipient_upi,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS",
            "verification_score": score
        }
        
        st.session_state.transactions.append(transaction)
        
        return f"""✅ Transaction Successful!
        
💸 Amount: ₹{amount:,.2f}
👤 Recipient: {recipient} ({recipient_upi})
🔐 Voice Verified: {score:.2f}
📋 Transaction ID: {transaction_id}
💰 New Balance: ₹{st.session_state.balance:,.2f}
⏰ Time: {transaction['timestamp']}"""
    
    # Default response for unrecognized commands
    return f"❓ Command not recognized: '{command}'\n\nTry commands like:\n• 'Send 500 to John'\n• 'Check balance'\n• 'Show transaction history'"

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="Voice Banking Assistant", 
        page_icon="🏦",
        layout="wide"
    )
    
    # Header
    st.title("🏦 GenAI Voice Banking Assistant")
    st.subheader("🎤 Secure Voice-Activated Banking Prototype")
    
    # Sidebar
    with st.sidebar:
        st.header("👤 Account Info")
        st.metric("Current Balance", f"₹{st.session_state.balance:,.2f}")
        st.metric("Total Transactions", len(st.session_state.transactions))
        
        st.header("🔐 Security Status")
        st.success("✅ Voice Biometrics: Active")
        st.success("✅ Fraud Detection: Active")
        st.success("✅ Secure Channel: Active")
        
        st.header("👥 Available Contacts")
        for name, upi in BENEFICIARIES.items():
            st.text(f"• {name.title()}")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎤 Voice Command Interface")
        
        # Sample commands
        st.info("""
        **Try these voice commands:**
        • "Send 1500 to John Doe"
        • "Transfer 500 to Alice"
        • "Pay 2000 to Bob"
        • "Check my balance"
        • "Show transaction history"
        """)
        
        # Voice input (text simulation)
        voice_command = st.text_input(
            "🎙️ Voice Command (Type to simulate):",
            placeholder="e.g., Send 1000 to John",
            help="Type a command to simulate voice input"
        )
        
        # Action buttons
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            process_btn = st.button("🎯 Process Command", type="primary", use_container_width=True)
        
        with col1b:
            if st.button("💰 Quick Balance", use_container_width=True):
                st.success(f"Current Balance: ₹{st.session_state.balance:,.2f}")
        
        with col1c:
            if st.button("🔄 Reset Demo", use_container_width=True):
                st.session_state.balance = 25000.0
                st.session_state.transactions = []
                st.rerun()
        
        # Process voice command
        if process_btn and voice_command:
            with st.spinner("🔊 Processing voice command..."):
                response = process_voice_command(voice_command)
                
                st.write("### 🤖 Assistant Response:")
                if "✅" in response:
                    st.success(response)
                elif "❌" in response:
                    st.error(response)
                elif "❓" in response:
                    st.warning(response)
                else:
                    st.info(response)
    
    with col2:
        st.header("📊 System Demo")
        
        # Quick demo buttons
        demo_commands = [
            "Send 500 to John",
            "Transfer 1000 to Alice", 
            "Pay 250 to Bob",
            "Check balance"
        ]
        
        st.write("**Quick Demo Commands:**")
        for cmd in demo_commands:
            if st.button(f"🎤 {cmd}", key=f"demo_{cmd}", use_container_width=True):
                with st.spinner("Processing..."):
                    response = process_voice_command(cmd)
                    if "✅" in response:
                        st.success(response)
                    elif "❌" in response:
                        st.error(response)
                    else:
                        st.info(response)
    
    # Transaction History
    if st.session_state.transactions:
        st.header("📜 Transaction History")
        
        # Display recent transactions
        for txn in reversed(st.session_state.transactions[-10:]):
            with st.expander(f"₹{txn['amount']:,.2f} to {txn['recipient']} - {txn['timestamp']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Amount:** ₹{txn['amount']:,.2f}")
                    st.write(f"**Recipient:** {txn['recipient']}")
                with col2:
                    st.write(f"**Status:** {txn['status']}")
                    st.write(f"**Transaction ID:** {txn['id']}")
                with col3:
                    st.write(f"**Voice Score:** {txn['verification_score']:.2f}")
                    st.write(f"**UPI ID:** {txn['recipient_upi']}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🏦 GenAI Voice Banking Assistant Prototype<br>
        Secure • Fast • Conversational • Accessible
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
