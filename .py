import streamlit as st
import time
import random
import re
from datetime import datetime
from difflib import get_close_matches

# Page config
st.set_page_config(
    page_title="Voice Banking Assistant", 
    page_icon="🏦",
    layout="wide"
)

# Initialize session state
if 'balance' not in st.session_state:
    st.session_state.balance = 25000.0
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

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

# Function: Fuzzy recipient match
def get_recipient(name):
    matches = get_close_matches(name.lower(), BENEFICIARIES.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function: Extract amount and recipient
def extract_amount_and_recipient(text):
    text = text.lower().strip()
    
    # Extract amount
    amount_match = re.search(r'\b(\d+(?:\.\d+)?)\b', text)
    amount = float(amount_match.group(1)) if amount_match else None
    
    # Extract recipient
    recipient = None
    for name in BENEFICIARIES.keys():
        if name in text:
            recipient = name
            break
    if not recipient:
        words = text.split()
        trigger_words = ["to", "pay", "send", "transfer"]
        for i, word in enumerate(words):
            if word in trigger_words and i + 1 < len(words):
                potential_recipient = " ".join(words[i+1:i+3]).strip()
                recipient = get_recipient(potential_recipient)
                break
    
    return amount, recipient

# Function: Simulate voice verification
def simulate_voice_verification():
    time.sleep(1)
    verification_score = random.uniform(0.85, 0.98)
    return verification_score > 0.82, verification_score

# Function: Process voice commands
def process_voice_command(command):
    command = command.lower().strip()
    
    if not command:
        return "❌ No command received."
    
    # Balance check
    if any(word in command for word in ["balance", "check balance"]):
        return f"💰 Your current balance is ₹{st.session_state.balance:,.2f}"
    
    # Transaction history
    if any(word in command for word in ["history", "transactions"]):
        if st.session_state.transactions:
            history_text = "📋 Recent Transactions:\n\n"
            for txn in st.session_state.transactions[-5:]:
                history_text += f"• ₹{txn['amount']:,.2f} to {txn['recipient']} - {txn['status']}\n"
            return history_text
        else:
            return "📋 No transaction history found."
    
    # Send money
    if any(word in command for word in ["send", "transfer", "pay"]):
        amount, recipient = extract_amount_and_recipient(command)
        
        if not amount:
            return "❌ Please specify the amount."
        if not recipient:
            return "❌ Please specify the recipient."
        if amount <= 0:
            return "❌ Amount must be greater than zero."
        if amount > 50000:
            return "❌ Maximum transaction limit is ₹50,000."
        if amount > st.session_state.balance:
            return f"❌ Insufficient balance. Current: ₹{st.session_state.balance:,.2f}"
        
        recipient_upi = BENEFICIARIES.get(recipient.lower())
        if not recipient_upi:
            return f"❌ Recipient '{recipient}' not found."
        
        # Voice verification
        is_verified, score = simulate_voice_verification()
        if not is_verified:
            return f"❌ Voice verification failed. Score: {score:.2f}"
        
        # Process transaction
        transaction_id = f"TXN{int(time.time())}{random.randint(100, 999)}"
        st.session_state.balance -= amount
        transaction = {
            "id": transaction_id,
            "amount": amount,
            "recipient": recipient,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS"
        }
        st.session_state.transactions.append(transaction)
        
        return f"""✅ Transaction Successful!
💸 Amount: ₹{amount:,.2f}
👤 To: {recipient}
🔐 Voice Score: {score:.2f}
📋 ID: {transaction_id}
💰 Balance: ₹{st.session_state.balance:,.2f}"""
    
    return f"❓ Command not recognized: '{command}'"

# Main App
def main():
    st.title("🏦 GenAI Voice Banking Assistant")
    st.subheader("🎤 Secure Voice-Activated Banking")
    
    # Sidebar
    with st.sidebar:
        st.header("👤 Account")
        st.metric("Balance", f"₹{st.session_state.balance:,.2f}")
        st.metric("Transactions", len(st.session_state.transactions))
        
        st.header("👥 Contacts")
        for name in ["John Doe", "Alice", "Bob", "Mike"]:
            st.text(f"• {name}")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎤 Voice Commands")
        st.info("""
        **Try these commands:**
        • "Send 1000 to John"
        • "Transfer 500 to Alice" 
        • "Check balance"
        • "Show history"
        """)
        
        voice_command = st.text_input("🎙️ Voice Command:", placeholder="e.g., Send 500 to John")
        
        if st.button("🎯 Process Command", type="primary"):
            if voice_command:
                with st.spinner("Processing..."):
                    response = process_voice_command(voice_command)
                    if "✅" in response:
                        st.success(response)
                    elif "❌" in response:
                        st.error(response)
                    else:
                        st.info(response)
            else:
                st.warning("Please enter a command.")
    
    with col2:
        st.header("⚡ Quick Actions")
        demo_commands = ["Send 500 to John", "Check balance", "Show history"]
        for cmd in demo_commands:
            if st.button(f"🎤 {cmd}", key=cmd):
                response = process_voice_command(cmd)
                if "✅" in response:
                    st.success(response)
                elif "❌" in response:
                    st.error(response)
                else:
                    st.info(response)
    
    # Transaction history
    if st.session_state.transactions:
        st.header("📜 Recent Transactions")
        for txn in reversed(st.session_state.transactions[-5:]):
            with st.expander(f"₹{txn['amount']:,.2f} to {txn['recipient']}"):
                st.write(f"**ID:** {txn['id']}")
                st.write(f"**Time:** {txn['timestamp']}")
                st.write(f"**Status:** {txn['status']}")
    
    # Reset button
    if st.button("🔄 Reset Demo"):
        st.session_state.balance = 25000.0
        st.session_state.transactions = []

if __name__ == "__main__":
    main()
