import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import plotly.express as px
from PIL import Image
import io
import base64

# ====================
# 1. PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="ArogyaMitram - Medicine Redistribution",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. CUSTOM THEME & STYLING
# ====================
def apply_custom_theme():
    st.markdown("""
    <style>
        :root {
            --primary: #4361ee;       /* Modern blue */
            --primary-dark: #1e40af;
            --primary-light: #3b82f6;
            --secondary: #7c3aed;     /* Purple */
            --accent: #10b981;        /* Emerald */
            --danger: #ef4444;        /* Red */
            --warning: #f59e0b;       /* Amber */
            --dark: #1e293b;          /* Dark slate */
            --darker: #0f172a;
            --light: #f8fafc;         /* Lightest slate */
            --card-bg: rgba(255, 255, 255, 0.08);
            --sidebar-bg: rgba(30, 41, 59, 0.9);
        }
        
        /* Main container */
        .stApp {
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 100%);
            color: var(--light);
        }
        
        /* Glassmorphism cards */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Stats cards */
        .stat-card {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
            transition: all 0.3s ease;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
        }
        
        /* Header with gradient */
        .dashboard-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Modern buttons */
        .stButton>button {
            background: linear-gradient(to right, var(--primary), var(--primary-dark));
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            transition: all 0.3s;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            background: linear-gradient(to right, var(--primary-light), var(--primary));
        }
        
        /* Sidebar styling */
        .css-1vq4p4l {
            background: var(--sidebar-bg) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Form elements */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select,
        .stDateInput>div>div>input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;
        }
        
        .stTextInput>label, 
        .stTextArea>label,
        .stNumberInput>label,
        .stSelectbox>label,
        .stDateInput>label {
            font-weight: 500 !important;
            color: var(--light) !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }
        
        /* Status badges */
        .status-badge {
            padding: 0.35rem 0.7rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            font-weight: bold;
            color: white;
            display: inline-block;
            min-width: 80px;
            text-align: center;
        }
        .pending { background: var(--warning); }
        .approved { background: var(--accent); }
        .rejected { background: var(--danger); }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s;
            color: var(--light);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stTabs [aria-selected="true"] {
            background: var(--primary) !important;
            color: white !important;
            border-color: var(--primary-light);
        }
        
        /* Image preview */
        .image-preview {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 1rem;
        }
        
        /* WhatsApp button */
        .whatsapp-btn {
            background: #25D366 !important;
            color: white !important;
            border: none !important;
        }
        .whatsapp-btn:hover {
            background: #128C7E !important;
            transform: translateY(-2px) !important;
        }
        
        /* Login container */
        .login-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
        }
        
        /* College logo */
        .college-logo {
            width: 120px;
            height: 120px;
            object-fit: contain;
            margin: 0 auto 1rem;
            display: block;
            filter: drop-shadow(0 0 8px rgba(0,0,0,0.3));
        }
        
        /* Floating particles */
        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            animation: float 15s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
            100% { transform: translateY(-1000px) rotate(720deg); opacity: 0; }
        }
        
        /* Impact visualization */
        .impact-visual {
            width: 100%;
            height: 300px;
            background: linear-gradient(135deg, rgba(67,97,238,0.2) 0%, rgba(124,58,237,0.2) 100%);
            border-radius: 16px;
            position: relative;
            overflow: hidden;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .impact-icon {
            font-size: 5rem;
            opacity: 0.2;
            position: absolute;
        }
        
        /* Animated gradient border */
        .gradient-border {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            padding: 1px;
        }
        
        .gradient-border::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                rgba(67,97,238,0.8) 0%,
                rgba(124,58,237,0.8) 50%,
                rgba(16,185,129,0.8) 100%
            );
            animation: rotate 4s linear infinite;
            z-index: -1;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .gradient-border > div {
            background: var(--darker);
            border-radius: 15px;
            width: 100%;
            height: 100%;
            position: relative;
        }
    </style>
    """, unsafe_allow_html=True)

# ====================
# 3. DATA INITIALIZATION
# ====================
def init_session_state():
    if 'medicines' not in st.session_state:
        st.session_state.medicines = pd.DataFrame([
            {
                "id": 1, "name": "Paracetamol 500mg", "description": "For fever and pain relief", 
                "quantity": 50, "expiry": "2024-12-31", "donor": "Rahul Sharma", 
                "donor_contact": "919876543210", "location": "College Medical Room", "status": "approved", 
                "category": "Pain Relief", "image": "https://m.media-amazon.com/images/I/61tL6yTZf6L._AC_UF1000,1000_QL80_.jpg",
                "value": 2, "added_date": "2023-05-15", "prescription": False
            },
            {
                "id": 2, "name": "Amoxicillin 250mg", "description": "Antibiotic for bacterial infections", 
                "quantity": 30, "expiry": "2024-08-30", "donor": "Priya Patel", 
                "donor_contact": "919876543211", "location": "College Medical Room", "status": "approved", 
                "category": "Antibiotic", "image": "https://5.imimg.com/data5/SELLER/Default/2021/12/SE/BN/YK/3033203/amoxicillin-250mg-capsule-1000x1000.jpg",
                "value": 5, "added_date": "2023-06-20", "prescription": True
            },
            {
                "id": 3, "name": "Atorvastatin 20mg", "description": "Cholesterol lowering medication", 
                "quantity": 20, "expiry": "2025-03-15", "donor": "Amit Kumar", 
                "donor_contact": "919876543212", "location": "College Medical Room", "status": "pending", 
                "category": "Cardiovascular", "image": "https://5.imimg.com/data5/SELLER/Default/2023/7/318929384/QH/VS/GT/199470473/atorvastatin-20-mg-tablet-500x500.jpg",
                "value": 8, "added_date": "2023-07-10", "prescription": True
            }
        ])
    
    if 'users' not in st.session_state:
        st.session_state.users = {
            "admin": {"password": "admin123", "name": "Admin", "phone": "911234567890", "role": "admin", "org": "College Medical Center"},
            "donor1": {"password": "donor123", "name": "Rahul Sharma", "phone": "919876543210", "role": "donor", "org": "Student"},
            "donor2": {"password": "donor123", "name": "Priya Patel", "phone": "919876543211", "role": "donor", "org": "Faculty"},
            "recipient1": {"password": "recipient123", "name": "Medical Staff", "phone": "919876543213", "role": "recipient", "org": "College Health Center"}
        }
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_page = "impact"
    
    if 'impact_stats' not in st.session_state:
        st.session_state.impact_stats = {
            "total_medicines": 180,
            "total_value": 1200,
            "waste_prevented": 1500,
            "lives_impacted": 250,
            "carbon_footprint": 300
        }
    
    if 'analytics' not in st.session_state:
        st.session_state.analytics = {
            "monthly_donations": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
            "categories": {
                "Pain Relief": 45,
                "Antibiotics": 30,
                "Chronic Diseases": 15,
                "Vitamins": 8,
                "Other": 2
            }
        }

# ====================
# 4. UTILITY FUNCTIONS
# ====================
def img_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_img_from_upload(uploaded_file):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            return f"data:image/png;base64,{img_to_base64(image)}"
        except:
            return "https://via.placeholder.com/150?text=Medicine"
    return "https://via.placeholder.com/150?text=Medicine"

def create_particles():
    st.markdown("""
    <div class="particles">
        <div class="particle" style="width: 8px; height: 8px; top: 20%; left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="width: 6px; height: 6px; top: 60%; left: 25%; animation-delay: 2s;"></div>
        <div class="particle" style="width: 10px; height: 10px; top: 30%; left: 50%; animation-delay: 4s;"></div>
        <div class="particle" style="width: 5px; height: 5px; top: 70%; left: 75%; animation-delay: 6s;"></div>
        <div class="particle" style="width: 7px; height: 7px; top: 40%; left: 90%; animation-delay: 8s;"></div>
        <div class="particle" style="width: 9px; height: 9px; top: 80%; left: 30%; animation-delay: 10s;"></div>
    </div>
    """, unsafe_allow_html=True)

# ====================
# 5. AUTHENTICATION
# ====================
def show_login():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        with st.container():
            st.markdown("""
            <div class="login-container">
                <div style="text-align:center; margin-bottom:2rem;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2932/2932533.png" class="college-logo">
                    <h1 style="color: white; margin-bottom:0.5rem;">ArogyaMitram</h1>
                    <p style="color: rgba(255,255,255,0.7); margin-top:0;">College Medicine Redistribution Platform</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.subheader("🔐 Login to Continue")
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                if st.form_submit_button("Login", use_container_width=True, type="primary"):
                    authenticate_user(username, password)
            
            st.markdown("""
            </div>
            <div style="text-align:center; margin-top:1rem; color: rgba(255,255,255,0.7);">
                <p>Don't have an account? <a href="#" onclick="alert('Contact Admin at: medicaladmin@college.edu')" style="color: var(--accent); text-decoration: none;">Contact admin</a></p>
            </div>
            <script>
                function showAdminEmail() {
                    alert("Contact Admin at: medicaladmin@college.edu");
                    return false;
                }
            </script>
            """, unsafe_allow_html=True)
            
            create_particles()

def authenticate_user(username, password):
    if username in st.session_state.users:
        if st.session_state.users[username]["password"] == password:
            st.session_state.user = st.session_state.users[username]
            st.session_state.logged_in = True
            st.session_state.current_page = "impact"
            st.rerun()
        else:
            st.error("Incorrect password")
    else:
        st.error("User not found")

# ====================
# 6. SIDEBAR COMPONENT
# ====================
def create_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: -1rem -1rem 1rem -1rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        ">
            <img src="https://ui-avatars.com/api/?name={urllib.parse.quote(st.session_state.user['name'])}&background=random&color=fff" 
                 width="80" style="border-radius:50%; margin-bottom:1rem; border: 3px solid white;">
            <h3 style="color: white; margin-bottom:0;">{st.session_state.user['name']}</h3>
            <p style="color: rgba(255,255,255,0.8); margin-top:0.25rem;">{st.session_state.user['org']}</p>
            <div style="
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 0.25rem 0.5rem;
                border-radius: 1rem;
                font-size: 0.8rem;
                margin: 0.5rem auto;
                width: fit-content;
            ">{st.session_state.user['role'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation based on role
        pages = {
            "admin": [
                {"icon": "📊", "name": "Impact Dashboard", "id": "impact"},
                {"icon": "🛡️", "name": "Admin Console", "id": "admin"},
                {"icon": "📈", "name": "Analytics", "id": "analytics"}
            ],
            "donor": [
                {"icon": "📊", "name": "Impact Dashboard", "id": "impact"},
                {"icon": "💊", "name": "Donate Medicines", "id": "donate"},
                {"icon": "📋", "name": "My Donations", "id": "mydonations"}
            ],
            "recipient": [
                {"icon": "🔍", "name": "Find Medicines", "id": "find"},
                {"icon": "❤️", "name": "My Requests", "id": "requests"}
            ]
        }
        
        st.markdown("---")
        st.subheader("Navigation")
        for page in pages[st.session_state.user['role']]:
            if st.button(f"{page['icon']} {page['name']}", key=f"nav_{page['id']}", use_container_width=True):
                st.session_state.current_page = page['id']
        
        st.markdown("---")
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.rerun()
# ====================
# 7. DASHBOARD COMPONENTS
# ====================
def show_impact_dashboard():
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: white; margin-bottom:0.5rem;">Impact Dashboard</h1>
        <p style="color: rgba(255,255,255,0.8); margin:0;">Tracking medicine redistribution impact in our college</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        {"icon": "💊", "title": "Medicines Saved", "value": f"{st.session_state.impact_stats['total_medicines']:,}", "unit": "tablets"},
        {"icon": "💰", "title": "Value Saved", "value": f"₹{st.session_state.impact_stats['total_value']:,.0f}", "unit": "for college"},
        {"icon": "♻️", "title": "Waste Prevented", "value": f"{st.session_state.impact_stats['waste_prevented']}g", "unit": "of medical waste"},
        {"icon": "👥", "title": "Students Helped", "value": f"{st.session_state.impact_stats['lives_impacted']:,}", "unit": "students"}
    ]
    
    for i, metric in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{metric['icon']}</div>
                <h3 style="margin:0;">{metric['title']}</h3>
                <h1 style="margin:0.5rem 0; color:white;">{metric['value']}</h1>
                <p style="margin:0; opacity:0.8;">{metric['unit']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Impact visualization - FIXED THE FORMAT ISSUE HERE
    prescriptions_fulfilled = int(0.5 * st.session_state.impact_stats['total_medicines'])
    student_savings = int(0.3 * st.session_state.impact_stats['total_value'])
    st.markdown(f"""
    <div class="impact-visual">
        <div style="text-align: center; z-index: 1;">
            <h2>College Impact Visualization</h2>
            <p>This represents the amount of medicine waste we've prevented this semester</p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <div>
                    <div style="font-size: 2rem;">{prescriptions_fulfilled}</div>
                    <div style="font-size: 0.8rem;">Prescriptions Fulfilled</div>
                </div>
                <div>
                    <div style="font-size: 2rem;">₹{student_savings:,}</div>
                    <div style="font-size: 0.8rem;">Savings for Students</div>
                </div>
            </div>
        </div>
        <div class="impact-icon">💊</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualizations
    st.markdown("---")
    st.subheader("College Medicine Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            values=list(st.session_state.analytics['categories'].values()),
            names=list(st.session_state.analytics['categories'].keys()),
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Medicine Categories in College"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        monthly_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Donations": st.session_state.analytics['monthly_donations']
        })
        fig = px.bar(
            monthly_data,
            x="Month",
            y="Donations",
            color="Donations",
            color_continuous_scale="Blues",
            title="Monthly Donations in College"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def admin_dashboard():
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: white;">Admin Console</h1>
        <p style="color: rgba(255,255,255,0.8);">Manage medicine approvals for college</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Pending Approvals", "📦 All Medicines"])
    
    with tab1:
        pending_meds = st.session_state.medicines[st.session_state.medicines['status'] == 'pending']
        
        if pending_meds.empty:
            st.info("✨ No medicines pending approval")
        else:
            for _, med in pending_meds.iterrows():
                with st.container():
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    
                    cols = st.columns([1, 3, 1])
                    with cols[0]:
                        st.image(med['image'], width=150)
                    
                    with cols[1]:
                        st.subheader(med['name'])
                        st.caption(med.get('description', ''))
                        st.write(f"""
                        **Quantity:** {med['quantity']} | **Value:** ₹{med.get('value', 0)*med['quantity']:,}  
                        **Expiry:** {med['expiry']} | **Location:** {med['location']}  
                        **Donor:** {med['donor']} ({med['donor_contact']})
                        """)
                        if med['prescription']:
                            st.warning("⚠️ Prescription Required")
                    
                    with cols[2]:
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Approve", key=f"approve_{med['id']}"):
                                update_medicine_status(med['id'], 'approved')
                        with col2:
                            if st.button("❌ Reject", key=f"reject_{med['id']}"):
                                update_medicine_status(med['id'], 'rejected')
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.dataframe(
            st.session_state.medicines,
            use_container_width=True,
            column_config={
                "image": st.column_config.ImageColumn("Preview"),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["pending", "approved", "rejected"],
                    required=True
                )
            }
        )

def update_medicine_status(med_id, status):
    st.session_state.medicines.loc[st.session_state.medicines['id'] == med_id, 'status'] = status
    if status == 'approved':
        med = st.session_state.medicines[st.session_state.medicines['id'] == med_id].iloc[0]
        st.session_state.impact_stats['total_medicines'] += med['quantity']
        st.session_state.impact_stats['total_value'] += med.get('value', 0)*med['quantity']
    st.rerun()

# ====================
# 8. DONOR DASHBOARD
# ====================
def donor_dashboard(show_history=False):
    if not show_history:
        st.markdown("""
        <div class="dashboard-header">
            <h1 style="color: white;">Donate Medicines</h1>
            <p style="color: rgba(255,255,255,0.8);">Submit your unused medicines to college</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("➕ New Donation", expanded=True):
            with st.form("donate_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    name = st.text_input("Medicine Name*")
                    description = st.text_area("Description")
                    quantity = st.number_input("Quantity*", min_value=1)
                    expiry = st.date_input("Expiry Date*", min_value=datetime.date.today())
                with cols[1]:
                    category = st.selectbox("Category*", ["Pain Relief", "Antibiotic", "Chronic Disease", "Cardiovascular", "Vitamins", "Other"])
                    value = st.number_input("Approx. Value per Unit (₹)*", min_value=1)
                    location = st.selectbox("Location*", ["College Medical Room", "Hostel A", "Hostel B", "Faculty Block"])
                    prescription = st.checkbox("Requires Prescription")
                    image = st.file_uploader("Upload Medicine Image", type=["jpg", "png", "jpeg"])
                
                submitted = st.form_submit_button("Submit Donation", type="primary")
                if submitted:
                    if not (name and quantity and expiry and location and value):
                        st.error("Please fill all required fields (*)")
                    else:
                        new_id = max(st.session_state.medicines['id']) + 1 if not st.session_state.medicines.empty else 1
                        new_med = {
                            "id": new_id, "name": name, "description": description,
                            "quantity": quantity, "expiry": expiry.strftime("%Y-%m-%d"), 
                            "donor": st.session_state.user['name'], "donor_contact": st.session_state.user['phone'],
                            "location": location, "status": "pending", "category": category,
                            "value": value, "image": get_img_from_upload(image),
                            "prescription": prescription, "added_date": datetime.date.today().strftime("%Y-%m-%d")
                        }
                        st.session_state.medicines = pd.concat([
                            st.session_state.medicines,
                            pd.DataFrame([new_med])
                        ], ignore_index=True)
                        st.success("Donation submitted for approval!")
                        st.balloons()
        
        st.markdown("---")
        st.subheader("Your Recent Donations")
    else:
        st.markdown("""
        <div class="dashboard-header">
            <h1 style="color: white;">Your Donation History</h1>
            <p style="color: rgba(255,255,255,0.8);">Track all your medicine donations</p>
        </div>
        """, unsafe_allow_html=True)
    
    your_donations = st.session_state.medicines[
        st.session_state.medicines['donor'] == st.session_state.user['name']
    ]
    
    if your_donations.empty:
        st.info("You haven't donated any medicines yet")
    else:
        for _, med in your_donations.iterrows():
            status_class = med['status']
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>{med['name']}</h3>
                    <span class="status-badge {status_class}">{status_class.upper()}</span>
                </div>
                <p>Quantity: {med['quantity']} | Value: ₹{med.get('value', 0)*med['quantity']:,}</p>
                <p>Submitted on: {med.get('added_date', 'N/A')} | Expiry: {med['expiry']}</p>
                {f'<p style="color: var(--warning);">⚠️ Prescription Required</p>' if med['prescription'] else ''}
            </div>
            """, unsafe_allow_html=True)

# ====================
# 9. RECIPIENT DASHBOARD
# ====================
def recipient_dashboard():
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: white;">Available Medicines</h1>
        <p style="color: rgba(255,255,255,0.8);">Find and request medicines you need</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search medicines", key="search_meds")
    with col2:
        category = st.selectbox("🏷️ Filter by category", ["All"] + list(st.session_state.medicines['category'].unique()), key="filter_category")
    with col3:
        location = st.selectbox("📍 Filter by location", ["All"] + list(st.session_state.medicines['location'].unique()), key="filter_location")
    
    # Filter approved medicines
    approved_meds = st.session_state.medicines[st.session_state.medicines['status'] == 'approved']
    if search:
        approved_meds = approved_meds[approved_meds['name'].str.contains(search, case=False)]
    if category != "All":
        approved_meds = approved_meds[approved_meds['category'] == category]
    if location != "All":
        approved_meds = approved_meds[approved_meds['location'] == location]
    
    if approved_meds.empty:
        st.info("No medicines currently available matching your criteria")
    else:
        for _, med in approved_meds.iterrows():
            with st.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(med['image'], width=200)
                with cols[1]:
                    st.subheader(med['name'])
                    st.caption(f"**Category:** {med['category']}")
                    st.write(med.get('description', ''))
                    
                    st.write(f"""
                    **Quantity Available:** {med['quantity']}  
                    **Expiry Date:** {med['expiry']}  
                    **Location:** {med['location']}  
                    **Donated by:** {med['donor']}
                    """)
                    
                    if med['prescription']:
                        st.warning("⚠️ Prescription Required")
                    
                    whatsapp_url = f"https://wa.me/{med['donor_contact']}?text=" + urllib.parse.quote(
                        f"Hello {med['donor']}, I need {med['name']} from ArogyaMitram.\n"
                        f"My details:\nName: {st.session_state.user['name']}\n"
                        f"Organization: {st.session_state.user['org']}\n"
                        f"Phone: {st.session_state.user['phone']}\n"
                        f"Quantity needed: [Please specify]"
                    )
                    st.markdown(f"""
                    <a href="{whatsapp_url}" target="_blank">
                        <button class="whatsapp-btn" style="
                            padding:0.5rem 1.5rem;
                            border-radius:8px;
                            margin-top:0.5rem;
                            font-weight:bold;
                            transition: all 0.3s;
                        ">
                            📱 Contact Donor via WhatsApp
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ====================
# 10. ANALYTICS DASHBOARD
# ====================
def analytics_dashboard():
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: white;">Advanced Analytics</h1>
        <p style="color: rgba(255,255,255,0.8);">Platform insights and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Donation Status Distribution")
        status_counts = st.session_state.medicines['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig = px.pie(
            status_counts,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map={
                'approved': '#10b981',
                'pending': '#f59e0b',
                'rejected': '#ef4444'
            },
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Donations by Category")
        category_counts = st.session_state.medicines['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        fig = px.bar(
            category_counts,
            x='Category',
            y='Count',
            color='Category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Donation Timeline")
    donations_timeline = st.session_state.medicines.copy()
    donations_timeline['added_date'] = pd.to_datetime(donations_timeline['added_date'])
    timeline_data = donations_timeline.groupby(pd.Grouper(key='added_date', freq='M')).size().reset_index()
    timeline_data.columns = ['Month', 'Count']
    fig = px.line(
        timeline_data,
        x='Month',
        y='Count',
        markers=True,
        title="Monthly Donations Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

# ====================
# 11. MAIN APPLICATION FLOW
# ====================
def main():
    apply_custom_theme()
    init_session_state()
    
    if not st.session_state.logged_in:
        show_login()
        return
    
    create_sidebar()
    
    # Main content area
    with st.container():
        if st.session_state.current_page == "impact":
            show_impact_dashboard()
        elif st.session_state.current_page == "admin":
            admin_dashboard()
        elif st.session_state.current_page == "donate":
            donor_dashboard()
        elif st.session_state.current_page == "find":
            recipient_dashboard()
        elif st.session_state.current_page == "analytics":
            analytics_dashboard()
        elif st.session_state.current_page == "mydonations":
            donor_dashboard(show_history=True)
        elif st.session_state.current_page == "requests":
            st.markdown('<div class="dashboard-header"><h1>My Requests</h1></div>', unsafe_allow_html=True)
            st.info("Feature coming soon! Your request history will appear here.")

if __name__ == "__main__":
    main()

