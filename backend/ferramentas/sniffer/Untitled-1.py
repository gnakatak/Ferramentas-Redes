# Before (causing error):
st.write(f"   - {addr['type']}: {addr['address']}")

# After (flexible handling):
if isinstance(addr, dict):
    # Detailed format with type and address
    st.write(f"   - {addr.get('type', 'IP')}: {addr.get('address', 'N/A')}")
else:
    # Simple format (string of IP)
    st.write(f"   - IP: {addr}")