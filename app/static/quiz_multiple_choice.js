
const Format = {
    PROMPT: 0,
    CHOICE: 1,
}

class Choice {
    constructor(vals, a_prompt, b_prompt) {
        this._vals = vals;
        this._a_prompt = a_prompt;
        this._b_prompt = b_prompt;
    }
    get key() { return this._vals['key']; }
    get echo() {
        let parts = [];
        for (const [key, value] of Object.entries(this._vals)) {
            if (key != 'key' && value != null) {
                parts.push(key + ': ' + value);
            }
        }
        return parts.join('; ');
    }
    render(type) {
        if (type == Format.PROMPT) { return this._vals[this._a_prompt]; }
        else { return this._vals[this._b_prompt]; }
    }
    is_equal(other) { return this.key == other.key;}
    contains(form_str) {
        for (const [key, value] of Object.entries(this._vals)) {
            if (key != 'key' && value != null) {
                if (value == form_str) { return true; }
            }
        }
        return false;
    }
}

class Question {
    constructor(choices, prompt_a, prompt_b) {
        this._choices = [];
        for (let i = 0; i < choices.length; i++) {
            this._choices.push(new Choice(choices[i], prompt_a, prompt_b));
        }
        this._expected_answer_idx = Math.floor(Math.random() * this._choices.length);
        this._user_answer = null;
    }
    get choices() { return this._choices; }
    get answer() { return this._choices[this._expected_answer_idx]; }
    find(form_str) {
        for (let i = 0; i < this.choices.length; i++) {
            if (this.choices[i].contains(form_str)) {
                return this.choices[i];
            }
        }
        return null;
    }
    set user_choice(val_str) {
        if (this._user_answer != null) { throw 'Question.user_choice setter: already set'; }
        let choice = this.find(val_str);
        if (choice == null) { throw `Question.user_choice(): no choice matches "${val_str}"`; }
        this._user_answer = choice;
    }
    get user_choice() {
        if (this._user_answer == null) { throw 'Question.user_choice getter: called before value set'; }
        return this._user_answer;
    }
    get answered_correctly() {
        return this.answer.is_equal(this.user_choice)
    }
}

class Quiz {
    constructor(json_obj) {

        let payload;
        try {
            payload = JSON.parse(json_obj);
        } catch (error) {
            console.error('Quiz.constructor: failed to initialize quiz instance');
        }

        this._idx = 0;
        this._questions = [];
        for (let i = 0; i < payload['questions'].length; i++) {
            this._questions.push(new Question(payload['questions'][i], payload['a_prompt'], payload['b_prompt']));
        }
    }
    get is_done() { return this._idx == this._questions.length; }
    next() {
        if (this.is_done) { throw 'Quiz.next(): called when quiz is done'}
        this._idx++;
    }
    get current_question() {
        if (this.is_done) { throw 'Quiz.current_question: called after quiz is done'}
        return this._questions[this._idx];
    }
    // get answer() { return this.current_question.answer; }
    // set answer(value) { this.current_question.answer = value;}
    // get answered_correctly() { return this.current_question.answer_is_correct(); }
    get percent_complete() {
        // A note regarding the adding one (1) to this._idx in the calculation below.
        // This Quiz class method is used to update the progress bar on quiz pages; it
        // is currently called *before* Quiz.next() is called which causes the progress
        // bar's state to be "off by one."  A better solution would be to modify the calling
        // code so that Quiz.next() is called before Quiz.percent_complete.  (An effort for
        // another day.)
        return (((this._idx + 1) / this._questions.length) * 100).toFixed() + '%';
    }
    get responses_encoded() {
        let responses = [];
        for (let i = 0; i < this._questions.length; i++) {
            let next_question = this._questions[i];
            let next_expected = next_question.answer;
            let next_response = next_question.user_choice;
            let next_pair = {'expected': next_expected.key, 'actual': next_response.key};
            responses.push(next_pair);
        }
        return JSON.stringify(responses);
    }
}
