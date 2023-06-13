export class VarState {
    name: string
    variable: any;
    allow_reassign: boolean;
    priority: number;
    history: Array<any>;
    updateCount: number;
    onUpdatePromises: Array<UpdatePromise>;
    expiry: number
    
    constructor(name, variable, allow_reassign, priority, lifetime=-1) {
        this.name = name
        this.variable = variable;
        this.allow_reassign = allow_reassign;
        this.priority = priority;
        this.history = [undefined];
        this.expiry = Infinity
        
        // Lifetime will be left as default unless infinity or seconds
        // Line-based lifetime will be done manually with kill()
        if (lifetime != -1) {
            if (lifetime === Infinity) {
                localStorage.setItem(name, variable);
                this.expiry = -1
            }
            else {
                this.expiry = Date.now() + (1000 * lifetime)
            }
        }

        this.updateCount = 0;
        this.onUpdatePromises = [];
    }

    get() {
        if (this.dead()) {
            this.kill()            
        }
        return this.variable;
    }

    dead() {
        return this.expiry !== -1 && Date.now() >= this.expiry
    }

    kill() {
        this.history.push(this.variable)
        this.variable = undefined        
    }

    assign(value, priority) {
        if (this.dead()) {
            this.kill()            
        }
        if (!this.allow_reassign || priority < this.priority) {
            return false;
        } else {
            this.history.push(this.variable);
            if (this.expiry == -1) {
                localStorage.setItem(this.name, value);
            }            
            this.variable = value;
            this.updateCount++;

            // Check all `next` calls
            const resolvedPromises: Array<UpdatePromise> = [];
            for (const promise of this.onUpdatePromises) {
                if (this.updateCount >= promise.targetCount) {
                    promise.resolve(this.variable);
                    resolvedPromises.push(promise);
                }
            }

            for (const promise of resolvedPromises) {
                const index = this.onUpdatePromises.indexOf(promise);
                if (index !== -1) {
                    this.onUpdatePromises.splice(index, 1);
                }
            }

            return true;
        }
    }

    previous(prev_iter = 1) {
        if (prev_iter > this.history.length) {
            console.log(`Soft Error: Attempting to access prehistoric value of ${this.name}.`)
            return Math.random() * Number.MAX_VALUE // Approximation of unassigned memory
        }
        return this.history[this.history.length - prev_iter];
    }

    next(count: number): Promise<any> {
        const targetCount = this.updateCount + count;

        if (targetCount <= this.updateCount) {
            console.log(`Variable already updated ${count} times. Current value: ${this.get()}`);
            return Promise.resolve(this.get());
        }

        return new Promise((resolve) => {
            const promise: UpdatePromise = {
                targetCount: targetCount,
                resolve: resolve,
            };
            this.onUpdatePromises.push(promise);
        });
    }
}

export interface UpdatePromise {
    targetCount: number;
    resolve: Function;
}
/// USED FOR WHEN BLOCKS
class ConditionBlockPair {
    condition: () => boolean;
    codeBlock: () => void;

    constructor(condition: () => boolean, codeBlock: () => void) {
        this.condition = condition;
        this.codeBlock = codeBlock;
    }
}

// Define a class to manage the conditions and code blocks
export class ConditionBlockManager {
    pairs: ConditionBlockPair[];

    constructor() {
        this.pairs = [];
    }

    addPair(condition: () => boolean, codeBlock: () => void) {
        const pair = new ConditionBlockPair(condition, codeBlock);
        this.pairs.push(pair);
    }

    checkConditions() {
        this.pairs = this.pairs.filter((pair) => {
            if (pair.condition()) {
                pair.codeBlock();
                return false; // Remove the pair from the list
            }
            return true; // Keep the pair in the list
        });
      }

    startCheckingRegularly(interval: number) {
        setInterval(() => {
        this.checkConditions();
        }, interval);
    }
}