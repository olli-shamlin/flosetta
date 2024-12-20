
function fatalError(msg) {
    // Writes the given string to (1) the console log, (2) a browser alert box (provided the code is being run
    // inside a browser), and finally, (3) in an exception that is thrown.
    msg = `Fatal Error: ${msg}`
    console.log(msg);
    if (typeof window === 'object')
        alert(msg);
    throw new Error(msg);
}

// ======== Controls ======================

class ProgressBarControl {
    constructor(max) {
        this.max = max;
        this.current = 0;
    }
    increment() {
        let width = ((++this.current / this.max) * 100).toFixed() + '%';
        document.getElementById('progress-bar').setAttribute('style', `width: ${width}`);
    }
}

class PromptControl {
    constructor() {

    }
}

class ResponseControl {
    constructor() {

    }
}

class FeedbackControl {
    constructor() {

    }
}

class ContinueButtonControl {
    #element_id = 'continue-btn';
    #is_disabled = false;
    constructor(initial_state) {
        if (initial_state !== 'Check' && initial_state !== 'Next')
            fatalError(`ContinueButtonControl.state: bad value: ${initial_state}`);

        let el = document.getElementById(this.#element_id);
        this.#is_disabled = el.getAttribute('class').includes(' disabled');
        el.innerText = initial_state;
        let class_attr = ('Check' === initial_state) ? 'btn btn-outline-primary' : 'btn btn-primary';
        if (this.#is_disabled)
            class_attr += ' disabled';

        el.innerText = initial_state;
        el.setAttribute('class', class_attr);
    }

    get state() {
        return document.getElementById(this.#element_id).innerText;
    }

    set state(state) {
        if (state !== 'Check' && state !== 'Next')
            fatalError(`ContinueButtonControl.state: bad value: ${state}`);
        if (this._state === 'Next' && state === 'Next')
            fatalError(`ContinueButtonControl.state: state is already "Next"`);
        if (this._state === 'Check' && state === 'Check')
            fatalError(`ContinueButtonControl.state: state is already "Check"`);
        let class_attr = ('Next' === state) ? 'btn btn-primary' : 'btn btn-outline-primary';
        let el = document.getElementById(this.#element_id);
        el.setAttribute('class', class_attr);
        el.innerText = state;
    }

    show() { fatalError('ContinueButtonControl.show: not implemented'); }

    hide() {
        document.getElementById(this.#element_id).remove();
    }

    enable() {
        let el = document.getElementById(this.#element_id);
        let attr = el.getAttribute('class');
        if (! attr.includes(' disabled'))
            fatalError('ContinueButtonControl.enable(): already enabled');
        el.setAttribute('class', attr.replace(' disabled', ''));
    }

    disable() {
        let el = document.getElementById(this.#element_id);
        let attr = el.getAttribute('class');
        if (attr.includes('disabled'))
            fatalError('ContinueButtonControl.disable(): already disabled');
        el.setAttribute('class', attr + ' disabled');
    }
}

class SubmitButtonControl {
    #element_id = 'submit-btn';
    constructor() {
    }

    show() {
        let el = document.getElementById(this.#element_id);
        el.setAttribute('type', 'submit');
        el.setAttribute('size', 6);
    }

    hide() {
        document.getElementById(this.#element_id).setAttribute('type', 'hidden');
    }

    enable() { fatalError('SubmitButtonControl.enable(): not implemented'); }
    disable() { fatalError('SubmitButtonControl.disable(): not implemented'); }
}

// ======== Question ======================

class Question {
    show() { fatalError('Question.show(): must be implemented by subclass'); }
}

// ======== Quiz ==========================

class ServerPayload {
    constructor(payload) {
        this.params = null;
        this.questions = null;
    }
}

class ClientPayload {
    constructor() {
        this.answers = [];
    }
}

class Quiz {
    constructor() {
        this.payload;
        try {
            let json_obj = document.getElementById('transport').getAttribute('value');
            this.payload = JSON.parse(json_obj);
        } catch (error) {
            console.error('Quiz.constructor: failed to read transport');
        }

        this.progress_bar = new ProgressBarControl(this.payload.questions.length)
        this.submit_btn = new SubmitButtonControl();
        this.submit_btn.hide();
        this.continue_btn = new ContinueButtonControl('Next');
        this.continue_btn.enable();
        this.current_item = 0;
    }

    get questions() {
        fatalError('Quiz.question getter: subclass must implement')
    }

    get is_done() {
        return this.current_item === this.items.length - 1;
    }

    advance() {
        if (this.is_done)
            fatalError('Quiz.advance(): end of items list reached')
        this.items[++this.current_item].show();
        this.progress_bar.increment();
        if (this.is_done)
            // document.getElementById('transport').setAttribute('value', quiz.responses_encoded)
            this.progress_bar.increment();
            document.getElementById('transport').setAttribute('value', 'client-response-goes-here')
    }
}

// ======== Continue Button onclick ==================

function continueClick() {
    if (quiz.continue_btn.state === 'Check') {
        quiz.continue_btn.state = 'Next';
    } else { // Continue button is in 'Next' state
        if (quiz.is_done) {
            quiz.continue_btn.hide();
            quiz.submit_btn.show();
        } else { // Quiz is not done yet
            quiz.advance();
        }
    }
}

// ======== shuffleArray =============================

function shuffle(arr) { arr.sort(() => Math.random() - 0.5); }
