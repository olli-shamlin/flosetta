
class ProgressBar {
    constructor(count) {
        this._n = 0;
        this._max = 0;
        this._control = document.getElementById('progress-bar');
    }
    increment() {
        width = (((this._n + 1) / this._max) * 100).toFixed() + '%';
        this._control.setAttribute('style', `width: ${width}`)
    }
}

class Feedback:
    constructor() {
        this._box = document.getElementById('feedback-box');
        this._text = document.getElementById('feedback-message');
    }
    post_success(msg) {
        this._box.setAttribute('class', 'container bg-success bg-opacity-10');
        this._text.setAttribute('class', 'text-success');
        this._text.innerHTML = msg;
    }
    post_error(msg) {
        this._box.setAttribute('class', 'container bg-danger bg-opacity-10');
        this._text.setAttribute('class', 'text-danger');
        this._text.innerHTML = msg;
    }
    clear() {
        this._box.setAttribute('class', 'container bg-white bg-opacity-10');
        this._text.innerHTML = '';
    }

class Button {
    constructor(id) {
        this._btn = document.getElementByID(id);
    }
    get label() { return this._btn.innerText; }
    set label(val) { this._btn.innerText = val; }
    get checked() { return this._btn.checked; }
    set checked(val) { this._btn.checked = val; }
    enable() {
        this._btn.disabled = false;
    }
    disable() {
        this._btn.disabled = true;
        // I do the following in handleNextButton
        this._btn.setAttribute('class', 'btn btn-secondary disabled');
    }
    hide() {
        // I hide the continue button in handleNextButton with the following line of code
        this._btn.remove();
        // I hide the submit button in DOMContentLoaded with the following
        this._btn.setAttribute('type', 'hidden');
    }
    reveal() {
        // I reveal the submit button with the following two lines of code
        this._btn.setAttribute('type', 'submit');
        this._btn.setAttribute('size', 6);
    }
    set style(val) {
        this._btn.setAttribute('class', 'btn btn-success');
        this._btn.setAttribute('class', 'btn btn-outline-success');
    }
}

class Page {
    constructor(quiz) {
        this.progress = new ProgressBar(quiz.questions.length);
        this.feedback = new Feedback();
        this.continue_btn = new Button('continue-btn');
        this.submit_btn = new Button('submit');
        this.choices = [new Button('C1'), new Button('C2'), new Button('C3'), new Button('C4'), new Button('C5')];
        this._prompt = document.getElementById('prompt-word');
    }
    get prompt() { return this._prompt.innerText; }
    set prompt(val) { this._prompt.innerText = val; }
}
