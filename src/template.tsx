// Helper functions
import { VarState, ConditionBlockManager } from "../built/helper"

// Format: var_name -> VarState
const variables = new Map<any, VarState>()
const WHEN_BLOCK_MANAGER = new ConditionBlockManager();

function assign(name, value, allow_reassign, priority, lifetime=-1) {
    const varState = variables.get(name);
  
    if (varState !== undefined) {
      // Update the existing object properties
      varState.assign(value, priority);
    } else {
      // Create a new object and store it in the map
      variables.set(name, new VarState(name, value, allow_reassign, priority, lifetime));
    }
}

function get_var(name) {
    if (variables.get(name) !== undefined) {
        return variables.get(name)!.get()
    }
    else {
        // Check for infinite lifetime variables
        let local_var = localStorage.getItem(name)
        if (local_var != null) {
            return local_var;
        }

        // TODO: 3const server


        // Return literal value only if all other possibilities are ruled out
        return name
    }
}


// USER CODE HERE //