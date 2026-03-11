
import streamlit as st
import sqlite3
import pandas as pd
import os
from PIL import Image

conn = sqlite3.connect("tickets.db",check_same_thread=False)
c = conn.cursor()

st.title("Service Ticket Management System")

menu = st.sidebar.selectbox(
"Menu",
["Controller Dashboard","Technician Portal"]
)

# controller
if menu == "Controller Dashboard":

    password = st.sidebar.text_input("Password",type="password")

    if password == "admin123":

        ticket = st.number_input("Ticket Number",step=1)
        title = st.text_input("Title")
        desc = st.text_area("Description")
        tech = st.text_input("Assign Technician")

        if st.button("Create Ticket"):

            c.execute(
            "INSERT INTO tickets VALUES(?,?,?,?,?,?,?,?)",
            (ticket,title,desc,tech,"No","OPEN","","")
            )

            conn.commit()

            st.success("Ticket Created")

        df = pd.read_sql_query("SELECT * FROM tickets",conn)
        st.dataframe(df)

# technician
if menu == "Technician Portal":

    name = st.text_input("Technician Name")
    ticket = st.number_input("Ticket Number",step=1)

    if st.button("Login"):

        t = c.execute(
        "SELECT * FROM tickets WHERE ticket_no=?",
        (ticket,)
        ).fetchone()

        if t and name==t[3]:

            st.success("Access Granted")

            if st.button("Accept Ticket"):

                c.execute(
                "UPDATE tickets SET status=?,accepted_by=? WHERE ticket_no=?",
                ("IN PROGRESS",name,ticket)
                )

                conn.commit()

            if st.button("Close Ticket"):

                c.execute(
                "UPDATE tickets SET status=?,closed_by=? WHERE ticket_no=?",
                ("CLOSED",name,ticket)
                )

                conn.commit()

            photo = st.file_uploader("Upload Photo")

            if photo:

                path = os.path.join("uploads",photo.name)

                with open(path,"wb") as f:
                    f.write(photo.getbuffer())

                img = Image.open(path)
                st.image(img)

        else:

            st.error("Not assigned to this ticket")
