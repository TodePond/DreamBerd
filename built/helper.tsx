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
        return Date.now() >= this.expiry
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

export interface UpdatePromise {
    targetCount: number;
    resolve: Function;
}