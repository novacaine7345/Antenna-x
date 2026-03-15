machine_master
 -> id
 -> machine_name
operator_master
 -> id
 -> machine_name
 -> operator_name
 -> 
model_operator_master
 -> machine_name
 -> model_operation
	-> Turning
	-> Milling
	-> Grinding
	-> Hardening
	-> Molding



// for machine_1, tejas is responsible
// for machine_2, sudeep is responsible

Frontend:
1. Sidebar	
 -> Dropdown
    -> Machine Name
    //should show operator and work assigned
    
