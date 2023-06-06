// Helper functions

class VarState {
    variable: any;
    allow_reassign: boolean;
    priority: number;
    history: Array<any>;
    updateCount: number;
    onUpdatePromises: Array<UpdatePromise>;

    constructor(variable, allow_reassign, priority) {
        this.variable = variable;
        this.allow_reassign = allow_reassign;
        this.priority = priority;
        this.history = [undefined];
        this.updateCount = 0;
        this.onUpdatePromises = [];
    }

    get() {
        return this.variable;
    }

    assign(value, priority) {
        if (!this.allow_reassign || priority < this.priority) {
            return false;
        } else {
            this.history.push(this.variable);
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
            return undefined;
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

interface UpdatePromise {
    targetCount: number;
    resolve: Function;
}

// Format: var_name -> VarState
const variables = {}

function set_var(name, value, priority) {
    variables[name].assign(value, priority)
}

