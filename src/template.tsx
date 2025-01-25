// Helper functions
import { VarState, ConditionBlockManager } from "../built/helper"

// Format: var_name -> VarState
const current_scope = new Map<any, VarState>()
const WHEN_BLOCK_MANAGER = new ConditionBlockManager();




// USER CODE HERE //