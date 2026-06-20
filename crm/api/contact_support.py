import frappe

@frappe.whitelist(allow_guest=True)
def contact_support(name, email, message):
    try:
        # Create document
        doc = frappe.get_doc({
            "doctype": "Contact Support",
            "name1": name,
            "email": email,
            "message": message
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # ADMIN EMAIL 
    
        admin_email_content = f"""
        <div style="background:#f4f6f9; padding:30px; font-family: Arial;">
          <div style="max-width:600px; margin:auto; background:white; border-radius:12px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,0.1);">

            <div style="background:#3b82f6; color:white; padding:20px; text-align:center;">
              <h2>📩 New Support Request</h2>
              <p>IP CRM Support System</p>
            </div>

            <div style="padding:20px;">
              <p>A new support request has been submitted.</p>

              <div style="background:#eef2ff; padding:10px; border-radius:8px;">
                🎫 <b>Ticket ID:</b> {doc.name}
              </div>

              <p><b>Name:</b> {name}</p>
              <p><b>Email:</b> {email}</p>

              <div style="margin-top:15px;">
                <b>💬 Message:</b>
                <div style="background:#f9fafb; padding:10px; border-radius:8px; margin-top:5px;">
                  {message}
                </div>
              </div>
            </div>

            <div style="text-align:center; padding:15px;">
              <a href="http://crm.ipshopy.org/app/contact-support/{doc.name}"
                 style="background:#3b82f6; color:white; padding:10px 15px; border-radius:6px; text-decoration:none;">
                 View in CRM
              </a>
            </div>

          </div>
        </div>
        """

        frappe.sendmail(
            recipients=["support.ipcrm@gmail.com"],
            subject=f"New Support Request #{doc.name}",
            message=admin_email_content
        )

 
        # 📧 USER EMAIL
     
        user_email_content = f"""
        <div style="background:#f4f6f9; padding:30px; font-family: Arial;">
          <div style="max-width:600px; margin:auto; background:white; border-radius:12px; padding:20px; box-shadow:0 6px 20px rgba(0,0,0,0.1); text-align:center;">

            <h2 style="color:#16a34a;">✅ Request Submitted!</h2>

            <p>Your support request has been received successfully.</p>
            <p>Our team will get back to you soon.</p>

            <div style="background:#eef2ff; padding:10px; border-radius:8px; margin:15px 0;">
              🎫 <b>Ticket ID:</b> {doc.name}
            </div>

            <p style="font-size:12px; color:#666;">
              Please keep this ID for future reference.
            </p>

          </div>
        </div>
        """

        frappe.sendmail(
            recipients=[email],
            subject=f"Your Support Request #{doc.name}",
            message=user_email_content
        )

        return {
            "status": "success",
            "ticket": doc.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Contact Support API Error")
        return {"status": "error", "message": str(e)}

