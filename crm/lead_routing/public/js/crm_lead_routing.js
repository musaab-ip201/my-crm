// Copyright (c) 2026, IP CRM and contributors
// Department-Based Lead Routing — UI Buttons for CRM Lead

frappe.ui.form.on("CRM Lead", {
    refresh(frm) {
        // Only show routing buttons if the lead has a department assigned
        if (!frm.doc.current_department) return;

        // Remove any previously added routing buttons to avoid duplicates
        frm.remove_custom_button(__("Mark Done"), __("Routing"));
        frm.remove_custom_button(__("Send Back"), __("Routing"));
        frm.remove_custom_button(__("Reject to Onboarding"), __("Routing"));
        frm.remove_custom_button(__("Manager Override"), __("Routing"));

        // ──── Current Department Info Banner ────
        let dept_html = `<div style="
      padding: 8px 14px;
      margin-bottom: 10px;
      border-radius: 8px;
      background: var(--subtle-accent);
      border-left: 4px solid var(--primary-color);
      font-size: 13px;
    ">
      <strong>🏢 Department:</strong> ${frm.doc.current_department}
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>🕐 Shift:</strong> ${frm.doc.current_shift || "Not Set"}
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>📋 Status:</strong> ${frm.doc.department_status || "—"}
    </div>`;

        // Set the intro with department info
        frm.set_intro(dept_html, "blue");

        // Don't show action buttons if lifecycle is already complete
        if (frm.doc.department_status === "Done") {
            // Check if current dept is terminal
            frappe.db.get_value("Department Pipeline Stage", frm.doc.current_department, "is_terminal")
                .then((r) => {
                    if (r.message && r.message.is_terminal) {
                        frm.set_intro(dept_html.replace("📋 Status:", "✅ Status:"), "green");
                    }
                });
            return;
        }

        // ──── 1. MARK DONE Button ────
        // Available to department users — moves lead to next stage
        frm.add_custom_button(
            __("Mark Done"),
            function () {
                frappe.confirm(
                    __("Mark this department's work as <b>Done</b> and move lead to the next department?"),
                    function () {
                        frappe.call({
                            method: "lead_routing.api.lead_transfer.mark_department_done",
                            args: { lead_name: frm.doc.name },
                            freeze: true,
                            freeze_message: __("Transferring lead..."),
                            callback: function (r) {
                                if (r.message) {
                                    if (r.message.status === "completed") {
                                        frappe.show_alert({
                                            message: __("🎉 Lead lifecycle completed!"),
                                            indicator: "green",
                                        });
                                    } else {
                                        frappe.show_alert({
                                            message: __("✅ Lead moved to {0}", [r.message.to]),
                                            indicator: "green",
                                        });
                                    }
                                    frm.reload_doc();
                                }
                            },
                            error: function(r) {
                                // Handle timestamp mismatch errors gracefully
                                if (r.message && r.message.includes("Document has been modified")) {
                                    frappe.show_alert({
                                        message: __("Document was updated. Refreshing..."),
                                        indicator: "orange",
                                    });
                                    frm.reload_doc();
                                } else {
                                    // Show the original error for other issues
                                    frappe.msgprint({
                                        title: __("Error"),
                                        message: r.message || __("An error occurred while transferring the lead."),
                                        indicator: "red"
                                    });
                                }
                            }
                        });
                    }
                );
            },
            __("Routing")
        );

        // ──── 2. SEND BACK Button ────
        // Automatically sends the lead back to to the previous department in sequence
        frm.add_custom_button(
            __("Send Back"),
            function () {
                frappe.confirm(
                    __("Send this lead back to its previous department?"),
                    function () {
                        frappe.call({
                            method: "lead_routing.api.lead_transfer.send_back_to_department",
                            args: { lead_name: frm.doc.name },
                            freeze: true,
                            freeze_message: __("Sending lead back..."),
                            callback: function (r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __("↩️ Lead sent back to {0}", [r.message.to]),
                                        indicator: "orange",
                                    });
                                    frm.reload_doc();
                                }
                            },
                            error: function(r) {
                                if (r.message && r.message.includes("Document has been modified")) {
                                    frappe.show_alert({
                                        message: __("Document was updated. Refreshing..."),
                                        indicator: "orange",
                                    });
                                    frm.reload_doc();
                                } else {
                                    frappe.msgprint({
                                        title: __("Error"),
                                        message: r.message || __("An error occurred while sending the lead back."),
                                        indicator: "red"
                                    });
                                }
                            }
                        });
                    }
                );
            },
            __("Routing")
        );

        // ──── 3. REJECT TO ONBOARDING Button ────
        frm.add_custom_button(
            __("Reject to Onboarding"),
            function () {
                frappe.confirm(
                    __("Reject this lead back to <b>Seller Onboarding</b>?<br>This is typically used when the lead needs to restart the process."),
                    function () {
                        frappe.call({
                            method: "lead_routing.api.lead_transfer.reject_to_onboarding",
                            args: { lead_name: frm.doc.name },
                            freeze: true,
                            freeze_message: __("Rejecting lead..."),
                            callback: function (r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __("🔄 Lead rejected back to {0}", [r.message.to]),
                                        indicator: "red",
                                    });
                                    frm.reload_doc();
                                }
                            },
                            error: function(r) {
                                if (r.message && r.message.includes("Document has been modified")) {
                                    frappe.show_alert({
                                        message: __("Document was updated. Refreshing..."),
                                        indicator: "orange",
                                    });
                                    frm.reload_doc();
                                } else {
                                    frappe.msgprint({
                                        title: __("Error"),
                                        message: r.message || __("An error occurred while rejecting the lead."),
                                        indicator: "red"
                                    });
                                }
                            }
                        });
                    }
                );
            },
            __("Routing")
        );

        // ──── 4. TRANSFER Button (formerly Manager Override) ────
        // Visible to all users — allows transfer to any department
        frm.add_custom_button(
            __("Transfer to Department"),
            function () {
                frappe.call({
                    method: "lead_routing.api.lead_transfer.get_transfer_targets",
                    args: { current_department: frm.doc.current_department },
                    callback: function (r) {
                        if (!r.message || r.message.length === 0) {
                            frappe.msgprint(__("No other departments available."));
                            return;
                        }

                        let options = r.message.map((d) => d.name);

                        let d = new frappe.ui.Dialog({
                            title: __("Transfer Lead to Department"),
                            fields: [
                                {
                                    fieldname: "target_stage",
                                    fieldtype: "Select",
                                    label: __("Transfer To"),
                                    options: options.join("\n"),
                                    reqd: 1,
                                },
                                {
                                    fieldname: "notes",
                                    fieldtype: "Small Text",
                                    label: __("Reason / Notes"),
                                },
                            ],
                            primary_action_label: __("Transfer"),
                            primary_action: function (values) {
                                frappe.call({
                                    method: "lead_routing.api.lead_transfer.manager_override_transfer",
                                    args: {
                                        lead_name: frm.doc.name,
                                        target_stage: values.target_stage,
                                        notes: values.notes || "",
                                    },
                                    freeze: true,
                                    freeze_message: __("Transferring lead..."),
                                    callback: function (r) {
                                        if (r.message) {
                                            frappe.show_alert({
                                                message: __("⚡ Lead transferred to {0}", [r.message.to]),
                                                indicator: "blue",
                                            });
                                            d.hide();
                                            frm.reload_doc();
                                        }
                                    },
                                    error: function(r) {
                                        if (r.message && r.message.includes("Document has been modified")) {
                                            frappe.show_alert({
                                                message: __("Document was updated. Refreshing..."),
                                                indicator: "orange",
                                            });
                                            d.hide();
                                            frm.reload_doc();
                                        } else {
                                            frappe.msgprint({
                                                title: __("Error"),
                                                message: r.message || __("An error occurred while transferring the lead."),
                                                indicator: "red"
                                            });
                                        }
                                    }
                                });
                            },
                        });
                        d.show();
                    },
                });
            },
            __("Routing")
        );
    },
});
