#!/usr/bin/env python3

import frappe

def create_missing_transitions():
    """Create missing transition rules for the lead routing system."""
    
    print("=== Creating Missing Department Transition Rules ===")
    
    # Get all enabled pipeline stages
    stages = frappe.get_all('Department Pipeline Stage', 
        filters={'enabled': 1},
        fields=['name', 'stage_name', 'stage_order'], 
        order_by='stage_order')
    
    if not stages:
        print("❌ No pipeline stages found!")
        return
    
    print(f"Found {len(stages)} enabled pipeline stages:")
    for stage in stages:
        print(f"  {stage.stage_order}: {stage.stage_name} ({stage.name})")
    
    created_count = 0
    
    # Create forward transitions (stage N → stage N+1)
    print("\n--- Creating Forward Transitions ---")
    for i in range(len(stages) - 1):
        current_stage = stages[i]
        next_stage = stages[i + 1]
        
        # Check if transition already exists
        exists = frappe.db.exists('Department Transition Rule', {
            'from_stage': current_stage.name,
            'to_stage': next_stage.name,
            'transition_type': 'Forward',
            'enabled': 1
        })
        
        if not exists:
            try:
                # Create the transition rule
                transition_rule = frappe.get_doc({
                    'doctype': 'Department Transition Rule',
                    'from_stage': current_stage.name,
                    'to_stage': next_stage.name,
                    'transition_type': 'Forward',
                    'enabled': 1
                })
                
                transition_rule.insert(ignore_permissions=True)
                created_count += 1
                print(f"✅ Created: {current_stage.stage_name} → {next_stage.stage_name} (Forward)")
                
            except Exception as e:
                print(f"❌ Failed to create {current_stage.stage_name} → {next_stage.stage_name}: {str(e)}")
        else:
            print(f"✓ Already exists: {current_stage.stage_name} → {next_stage.stage_name} (Forward)")
    
    # Create backward transitions (stage N → stage N-1)
    print("\n--- Creating Backward Transitions ---")
    for i in range(1, len(stages)):
        current_stage = stages[i]
        prev_stage = stages[i - 1]
        
        # Check if transition already exists
        exists = frappe.db.exists('Department Transition Rule', {
            'from_stage': current_stage.name,
            'to_stage': prev_stage.name,
            'transition_type': 'Backward',
            'enabled': 1
        })
        
        if not exists:
            try:
                # Create the transition rule
                transition_rule = frappe.get_doc({
                    'doctype': 'Department Transition Rule',
                    'from_stage': current_stage.name,
                    'to_stage': prev_stage.name,
                    'transition_type': 'Backward',
                    'enabled': 1
                })
                
                transition_rule.insert(ignore_permissions=True)
                created_count += 1
                print(f"✅ Created: {current_stage.stage_name} → {prev_stage.stage_name} (Backward)")
                
            except Exception as e:
                print(f"❌ Failed to create {current_stage.stage_name} → {prev_stage.stage_name}: {str(e)}")
        else:
            print(f"✓ Already exists: {current_stage.stage_name} → {prev_stage.stage_name} (Backward)")
    
    # Create reject transitions (all stages → first stage)
    print("\n--- Creating Reject Transitions ---")
    if stages:
        first_stage = stages[0]
        
        for stage in stages[1:]:  # Skip first stage (can't reject to itself)
            # Check if transition already exists
            exists = frappe.db.exists('Department Transition Rule', {
                'from_stage': stage.name,
                'to_stage': first_stage.name,
                'transition_type': 'Reject',
                'enabled': 1
            })
            
            if not exists:
                try:
                    # Create the transition rule
                    transition_rule = frappe.get_doc({
                        'doctype': 'Department Transition Rule',
                        'from_stage': stage.name,
                        'to_stage': first_stage.name,
                        'transition_type': 'Reject',
                        'enabled': 1
                    })
                    
                    transition_rule.insert(ignore_permissions=True)
                    created_count += 1
                    print(f"✅ Created: {stage.stage_name} → {first_stage.stage_name} (Reject)")
                    
                except Exception as e:
                    print(f"❌ Failed to create {stage.stage_name} → {first_stage.stage_name}: {str(e)}")
            else:
                print(f"✓ Already exists: {stage.stage_name} → {first_stage.stage_name} (Reject)")
    
    # Commit all changes
    if created_count > 0:
        frappe.db.commit()
        print(f"\n🎉 Successfully created {created_count} transition rules!")
    else:
        print("\n✅ All required transition rules already exist!")
    
    # Show final summary
    print("\n=== Final Transition Rules Summary ===")
    all_rules = frappe.get_all('Department Transition Rule', 
        fields=['name', 'from_stage', 'to_stage', 'transition_type', 'enabled'],
        order_by='from_stage, transition_type')
    
    for rule in all_rules:
        status = "✅" if rule.enabled else "❌"
        print(f"{status} {rule.from_stage} → {rule.to_stage} ({rule.transition_type})")

if __name__ == '__main__':
    create_missing_transitions()