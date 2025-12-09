"""
Refactored IT Operations Page - Using OOP with ITTicket and TicketService
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Import OOP classes
from services.database_manager import DatabaseManager
from services.ticket_service import TicketService

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Page configuration
st.set_page_config(
    page_title="IT Operations Dashboard",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

initialize_session_state()

# Authentication check
if not st.session_state.logged_in:
    st.error("🚫 You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Initialize services (OOP)
db = DatabaseManager(str(DB_PATH))
ticket_service = TicketService(db)

# Title
st.title("🖥️ IT Operations Dashboard")

# Get all tickets using the service
tickets = ticket_service.get_all_tickets()

# Get statistics
stats = ticket_service.get_ticket_statistics()

# System health metrics (placeholder)
st.header("System Health")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", "42%", delta="+3%")

with col2:
    st.metric("Memory", "63%", delta="-0.5%")

with col3:
    st.metric("Disk", "81%", delta="+1.5%")

# Ticket statistics
st.header("Ticket Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    open_count = stats['by_status'].get('Open', 0)
    st.metric("Open", open_count)

with col2:
    high_count = stats['by_priority'].get('High', 0)
    critical_count = stats['by_priority'].get('Critical', 0)
    st.metric("High Priority", high_count + critical_count)

with col3:
    st.metric("Avg Resolution", f"{stats['avg_resolution_hours']:.1f}h")

with col4:
    resolved_count = stats['by_status'].get('Resolved', 0)
    closed_count = stats['by_status'].get('Closed', 0)
    st.metric("Completed", resolved_count + closed_count)

# Chart selector for tickets
st.subheader("Charts")
ticket_chart = st.selectbox(
    "Select chart type",
    ["Tickets by Status (Bar)", "Tickets by Priority (Pie)", "Ticket Trend (Line)"]
)

if ticket_chart == "Tickets by Status (Bar)":
    status_counts = stats.get('by_status', {})
    if status_counts:
        import pandas as _pd
        df_status = _pd.DataFrame({'Status': list(status_counts.keys()), 'Count': list(status_counts.values())})
        st.bar_chart(df_status.set_index('Status'))
    else:
        st.info('No status data available')

elif ticket_chart == "Tickets by Priority (Pie)":
    prio_counts = stats.get('by_priority', {})
    if prio_counts:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.pie(list(prio_counts.values()), labels=list(prio_counts.keys()), autopct='%1.1f%%')
        ax.set_title('Tickets by Priority')
        st.pyplot(fig)
    else:
        st.info('No priority data available')

else:  # Ticket Trend (Line)
    if tickets:
        import pandas as _pd
        dates = []
        for t in tickets:
            try:
                dates.append(_pd.to_datetime(t.get_created_at()).date())
            except Exception:
                continue

        if dates:
            ts = _pd.Series(dates).value_counts().sort_index()
            df_ts = ts.rename_axis('date').reset_index(name='count')
            df_ts['date'] = _pd.to_datetime(df_ts['date'])
            st.line_chart(df_ts.set_index('date'))
        else:
            st.info('No ticket timestamps available for trend')
    else:
        st.info('No tickets found')

# Display tickets
st.header("IT Tickets")

if tickets:
    # Convert ticket objects to DataFrame for display
    ticket_data = []
    for ticket in tickets[:30]:  # Show first 30
        ticket_data.append({
            'ID': ticket.get_id(),
            'Priority': ticket.get_priority(),
            'Status': ticket.get_status(),
            'Description': ticket.get_description()[:40] + "...",
            'Assigned To': ticket.get_assigned_to() or "Unassigned",
            'Created': ticket.get_created_at()
        })
    
    df = pd.DataFrame(ticket_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No tickets found")

# Ticket Management
st.header("Ticket Management")

# CREATE - Add new ticket
with st.form("add_ticket"):
    st.subheader("Create New Ticket")
    
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Critical"]
    )
    
    description = st.text_area("Description")
    
    assigned_to = st.selectbox(
        "Assign To",
        ["IT_Support_A", "IT_Support_B", "IT_Support_C", "Unassigned"]
    )
    
    submitted = st.form_submit_button("Create Ticket")
    
    if submitted and description:
        # Use service to create ticket
        assign_value = None if assigned_to == "Unassigned" else assigned_to
        
        new_id = ticket_service.create_ticket(
            priority=priority,
            description=description,
            assigned_to=assign_value
        )
        st.success(f"✅ Ticket #{new_id} created successfully!")
        st.rerun()

# UPDATE - Modify ticket
st.subheader("Update Ticket")

if tickets:
    # Create selection list
    ticket_options = {
        f"Ticket {t.get_id()}: {t.get_description()[:40]}...": t
        for t in tickets[:15]
    }
    
    selected_key = st.selectbox("Select ticket to update", list(ticket_options.keys()))
    selected_ticket = ticket_options[selected_key]
    
    # Display current info
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Priority:** {selected_ticket.get_priority()}")
        st.write(f"**Status:** {selected_ticket.get_status()}")
    
    with col2:
        st.write(f"**Assigned To:** {selected_ticket.get_assigned_to() or 'Unassigned'}")
        st.write(f"**Created:** {selected_ticket.get_created_at()}")
    
    # Update form
    with st.form("update_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_status = st.selectbox(
                "New Status",
                ["Open", "In Progress", "Resolved", "Closed", "Waiting for User"]
            )
        
        with col2:
            new_assignee = st.selectbox(
                "Reassign To",
                ["Keep Current", "IT_Support_A", "IT_Support_B", "IT_Support_C"]
            )
        
        if st.form_submit_button("Update Ticket"):
            # Update status
            success_status = ticket_service.update_ticket_status(
                selected_ticket.get_id(),
                new_status
            )
            
            # Update assignee if changed
            if new_assignee != "Keep Current":
                success_assign = ticket_service.assign_ticket(
                    selected_ticket.get_id(),
                    new_assignee
                )
            
            if success_status:
                st.success("✅ Ticket updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update ticket")

# Tickets by status
st.subheader("Filter Tickets")

col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Open", "In Progress", "Resolved", "Closed", "Waiting for User"]
    )
    
    if status_filter != "All":
        filtered_tickets = ticket_service.get_tickets_by_status(status_filter)
        st.write(f"**{status_filter} Tickets:** {len(filtered_tickets)}")

with col2:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "Low", "Medium", "High", "Critical"]
    )
    
    if priority_filter != "All":
        filtered_tickets = ticket_service.get_tickets_by_priority(priority_filter)
        st.write(f"**{priority_filter} Priority Tickets:** {len(filtered_tickets)}")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    if st.button("🤖 Ask AI Assistant", use_container_width=True):
        st.switch_page("pages/6_AI_Assistant.py")

# Close database connection
db.close()