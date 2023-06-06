// Helper functions
import { VarState } from "../built/helper"

// Format: var_name -> VarState
const variables = {}

function set_var(name, value, priority) {
    variables[name].assign(value, priority)
}

function assign(name, value, allow_reassign, priority, lifetime=-1) {
    if (variables[name] !== undefined) {
        variables[name].assign(value, priority)
    }
    else {
        variables[name] = new VarState(name, value, allow_reassign, priority, lifetime=-1)
    }
}

function get_var(name) {
    if (variables[name] !== undefined) {
        return variables[name].get()
    }
    else {
        // Check for infinite lifetime variables
        let local_var = localStorage.getItem(name)
        if (local_var != null) {
            return local_var;
        }

        // TODO: 3const server

        return undefined
    }
}


// USER CODE HERE //