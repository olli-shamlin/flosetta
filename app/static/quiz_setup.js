
function fatalError(msg) {
    // Writes the given string to (1) the console log, (2) a browser alert box (provided the code is being run
    // inside a browser), and finally, (3) in an exception that is thrown.
    msg = `Fatal Error: ${msg}`
    console.log(msg);
    if (typeof window === 'object')
        alert(msg);
    throw new Error(msg);
}

// ===================================================================================================================
// ===================================================================================================================
// ===   Global Constants   ==========================================================================================
// ===================================================================================================================
// ===================================================================================================================

const MAX_STACK_SIZE = 5;
const C2S_VALUES_MAP = new Map();
C2S_VALUES_MAP.set('Multiple Choice', 'Multiple Choice');
C2S_VALUES_MAP.set('Match', 'Match');
C2S_VALUES_MAP.set('Mega Match', 'Mega Match');
C2S_VALUES_MAP.set('Kana Table', 'Kana Table');
C2S_VALUES_MAP.set('Fill in the Blank', 'Fill In The Blank');
C2S_VALUES_MAP.set('Vocabulary Words', 'Vocabulary');
C2S_VALUES_MAP.set('Kana Characters', 'Syllabary');
C2S_VALUES_MAP.set('English', 'English');
C2S_VALUES_MAP.set('Japanese', 'Kana');
C2S_VALUES_MAP.set('Romaji', 'Romaji');
C2S_VALUES_MAP.set('Hiragana', 'Hiragana');
C2S_VALUES_MAP.set('Katakana', 'Katakana');

// ===================================================================================================================
// ===================================================================================================================
// ===   Controls   ==================================================================================================
// ===================================================================================================================
// ===================================================================================================================

class UndoControl {
    constructor(parent_id) {
        let path1_el = document.createElement('path');
        path1_el.setAttribute('fill-rule', 'evenodd');
        path1_el.setAttribute('d', 'M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z');

        let path2_el = document.createElement('path');
        path2_el.setAttribute('d',
            'M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466');

        let svg_el = document.createElement('svg');
        svg_el.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        svg_el.setAttribute('width', '16');
        svg_el.setAttribute('height', '16');
        svg_el.setAttribute('fill', 'currentColor');
        svg_el.setAttribute('class', 'bi bi-arrow-counterclockwise');
        svg_el.setAttribute('viewBox', '0 0 16 16');
        svg_el.appendChild(path1_el);
        svg_el.appendChild(path2_el);

        let btn_el = document.createElement('button');
        btn_el.setAttribute('type', 'button');
        btn_el.setAttribute('class', 'btn btn-outline-secondary ms-2');
        btn_el.setAttribute('id', 'undo-btn');
        btn_el.setAttribute('onclick', 'undo()');
        btn_el.appendChild(svg_el);

        document.getElementById(parent_id).appendChild(btn_el);
    }

    remove() {
        document.getElementById('undo-btn').remove();
    }
}

class QuestionControl {
    constructor(id, prompt, options) {
        this._id = id;
        this._prompt = prompt;
        this._options = options;
    }

    get selection() {
        let radio_el;
        for (let i=0; i < this._options.length; i++) {
            radio_el = document.getElementById(`i-${this._id}-${i + 1}`);
            if (radio_el.checked)
                return this._options[i];
        }
        return null;
    }

    display() {
        // Injects into the DOM, HTML of the following form
        //      <div id='q-${id}'>
        //          <p></p>
        //          <p class="lead">${prompt}</p>
        //          <div class="btn-group" role="group", aria-label="Radio toggle button group">
        //              <input type="radio" class="btn-check" name="${id}" id="i-${id}-${i}" autocomplete="off" onclick="advance()">
        //              <label class="btn btn-outline-primary" for="${id}-${i}" id="l-${id}-${i}">[---]</label>
        //              ...<input> & <label> repeated for each option...
        //          </div>
        //      </div>
        let spacer_el = document.createElement('p');
        let prompt_el = document.createElement('p');
        prompt_el.setAttribute('class', 'lead');
        let prompt_tx = document.createTextNode(this._prompt);
        prompt_el.appendChild(prompt_tx);

        let radio_div_el = document.createElement('div');
        radio_div_el.setAttribute('class', 'btn-group');
        radio_div_el.setAttribute('role', 'group');
        radio_div_el.setAttribute('aria-label', 'Basic radio toggle button group');

        for (let i = 0; i < this._options.length; i++) {
            let option_id = `${this._id}-${i + 1}`;
            let input_el = document.createElement('input');
            input_el.setAttribute('type', 'radio');
            input_el.setAttribute('class', 'btn-check');
            input_el.setAttribute('name', this._id);
            input_el.setAttribute('id', `i-${option_id}`);
            input_el.setAttribute('autocomplete', 'off');
            input_el.setAttribute('onclick', 'advance()');

            let label_el = document.createElement('label');
            label_el.setAttribute('class', 'btn btn-outline-primary');
            label_el.setAttribute('for', `i-${option_id}`);
            label_el.setAttribute('id', `l-${option_id}`);
            label_el.innerText = this._options[i];

            radio_div_el.appendChild(input_el);
            radio_div_el.appendChild(label_el);
        }

        let q_div_el = document.createElement('div');
        q_div_el.setAttribute('id', this._id);
        q_div_el.appendChild(spacer_el);
        q_div_el.appendChild(prompt_el);
        q_div_el.appendChild(radio_div_el);

        let page_el = document.getElementById('page-content');
        page_el.appendChild(q_div_el);
    }

    remove() {
        document.getElementById(`${this._id}`).remove();
    }

    enable() {
        for (let i=0; i < this._options.length; i++)
            document.getElementById(`i-${this._id}-${i + 1}`).disabled = false;
    }

    disable() {
        for (let i=0; i < this._options.length; i++)
            document.getElementById(`i-${this._id}-${i + 1}`).disabled = true;
    }
}

// ===================================================================================================================
// ===================================================================================================================
// ===   Parameters   ================================================================================================
// ===================================================================================================================
// ===================================================================================================================

class Parameter {
    constructor(name, value) {

        // Verify input parameters.  "name" must be a string and "value" must be a string or an integer.
        if (! name instanceof String || typeof name !== 'string')
            fatalError('Parameter.constructor() "name" argument must be a string');
        if ((! value instanceof String || typeof value !== 'string') && (value !== parseInt(value, 10)))
            fatalError('Parameter.constructor() "value" argument must be a string or an integer');

        this.name = name;
        this.value = value;
    }

    get as_parameter() { return this; }

    get next() { return null; }
}

// ===================================================================================================================
// ===================================================================================================================
// ===   Questions   =================================================================================================
// ===================================================================================================================
// ===================================================================================================================

class Question {
    constructor(id, predecessor, prompt, options) {

        // Verify input parameters. Both "id" and "prompt" must be strings, "options" must be an array of strings,
        // and "predecessor" must either be null or a "Question" object.
        if (! id instanceof String || typeof id !== 'string')
            fatalError('Question.constructor() "name" argument must be a string');
        if (! prompt instanceof String || typeof prompt !== 'string')
            fatalError('Question.constructor() "name" argument must be a string');
        if ((! Array.isArray(options)) ||
            (! options.every(i => typeof i === "string") && ! options.every(i => i === parseInt(i, 10))))
            fatalError('Question.constructor() "options" argument must be an array of strings');
        if ((predecessor != null) && (! predecessor instanceof Question))
            fatalError('Question.constructor() "predecessor" argument must be an instance of Question');

        this.id = id;
        this.prompt = prompt;
        this.options = options;
        this.control = null;
        this.predecessor = predecessor;
    }

    get next() {
        // Returns the list of items (a Question and possibly one or more Parameters that go on the Collector
        // stack next.  If there are no more items to collect, then this method returns null.
    }

    get selection() {
        return this.control.selection;
    }

    get as_parameter() {
        let id = this.id;
        let val = this.selection;

        if (id.endsWith('-1'))
            id = id.replace('-1', '');
        else if (id.endsWith('-2'))
            id = id.replace('-2', '');
        else if (id.endsWith('-3'))
            id = id.replace('-3', '');

        if (typeof val === 'string' || val instanceof String)
            val = C2S_VALUES_MAP.get(val);

        return new Parameter(id, val);
    }

    display() {
        if (this.control) fatalError('Question.display() control already visible');
        this.control = new QuestionControl(this.id, this.prompt, this.options);
        this.control.display();
    }

    remove() {
        if (! this.control) fatalError('Question.hide() control already hidden');
        this.control.remove();
        this.control = null;
    }

    enable() { this.control.enable(); }
    disable() { this.control.disable(); }
}

class Size2Question extends Question {
    constructor(predecessor) {
        super('size-2', predecessor, 'How many rows/columns do you want in the quiz?', [4, 6, 8]);
    }

    get next () { return null; }
}

class Size1Question extends Question {
    constructor(predecessor) {
        super('size-1', predecessor, 'How many questions do you want in the quiz?', [5, 10, 15, 20]);
    }

    get next () { return null; }
}

class Prompt3Question extends Question {
    constructor(predecessor) {
        super('prompt-3', predecessor, 'Which character form do you want question prompts to be?',
            ['Hiragana', 'Katakana']);
    }

    get next() {
        // Find the kind question
        let kq = this;
        do {
            kq = this.predecessor;
        }
        while (! kq instanceof KindQuestion);

        switch (kq.selection) {
            case 'Mega Match':
                switch (this.selection) {
                    case 'Hiragana':
                        return [new Parameter('choice', 'Katakana'), new Size2Question(this)];
                    case 'Katakana':
                        return [new Parameter('choice', 'Hiragana'), new Size2Question(this)];
                }
                break;
            case 'Kana Table':
                switch (this.selection) {
                    case 'Hiragana':
                        return [new Parameter('choice', 'Katakana'), new Parameter('size', 1)];
                    case 'Katakana':
                        return [new Parameter('choice', 'Hiragana'), new Parameter('size', 1)];
                }
        }
    }
}

class Choice1Question extends Question {
    constructor(predecessor) {
        super('choice-1', predecessor, 'Which character form do you want question choices to be?',
            ['Hiragana', 'Katakana']);
    }

    get next () { return [new Size1Question(this)]; }
}

class Choice2Question extends Question {
    constructor(predecessor) {
        super('choice-2', predecessor, 'Which character form do you want question choices to be?',
            ['Romaji', 'Katakana']);
    }

    get next () { return [new Size1Question(this)]; }
}

class Choice3Question extends Question {
    constructor(predecessor) {
        super('choice-2', predecessor, 'Which character form do you want question choices to be?',
            ['Romaji', 'Hiragana']);
    }

    get next () { return [new Size1Question(this)]; }
}

class Prompt2Question extends Question {
    constructor(predecessor) {
        super('prompt-2', predecessor, 'Which character form do you want question prompts to be?',
              ['Romaji', 'Hiragana', 'Katakana']);
    }

    get next() {
        switch (this.selection) {
            case 'Romaji':
                return [new Choice1Question(this)];
            case 'Hiragana':
                return [new Choice2Question(this)];
            case 'Katakana':
                return [new Choice3Question(this)];
        }
    }
}

class Prompt1Question extends Question {
    constructor(predecessor) {
        super('prompt-1', predecessor, 'Which language do you want to be prompted in?', ['English', 'Japanese']);
    }

    get next() {
        switch (this.selection) {
            case 'English':
                return [new Parameter('choice', 'Kana'), new Size1Question(this)];
            case 'Japanese':
                return [new Parameter('choice', 'English'), new Size1Question(this)];
        }
    }
}

class TableQuestion extends Question {
    constructor(predecessor) {
        super('table', predecessor, 'What do you want to be quizzed on?',
            ['Vocabulary Words', 'Kana Characters']);
    }

    get next() {
        switch (this.selection) {
            case 'Vocabulary Words':
                return [new Prompt1Question(this)];
            case 'Kana Characters':
                return [new Prompt2Question(this)];
        }
    }
}

class KindQuestion extends Question {
    constructor() {
        super('kind', null, 'What kind of quiz would you like?',
              ['Multiple Choice', 'Match', 'Mega Match', 'Kana Table', 'Fill in the Blank']);
    }

    get next() {
        switch (this.selection) {
            case 'Multiple Choice':
            case 'Match':
                return [new TableQuestion(this)];
            case 'Mega Match':
            case 'Kana Table':
                return [new Parameter('table', 'Syllabary'), new Prompt3Question(this)];
            case 'Fill in the Blank':
                return [new Parameter('table', 'Vocabulary'), new Prompt1Question(this)];
        }
    }
}

// ===================================================================================================================
// ===================================================================================================================
// ===   Collector   =================================================================================================
// ===================================================================================================================
// ===================================================================================================================

class Collector {
    constructor() {
        this.stack = [new KindQuestion()];
        this.stack[this.stack.length - 1].display();
        this.undo = null;
    }

    get is_done() {
        if (this.stack.length === MAX_STACK_SIZE) {
            if (this.stack[this.stack.length - 1] instanceof Question)
                if (this.stack[this.stack.length - 1].selection == null)
                    return false;
            return true;
        }
        return false;
    }

    step_forward() {
        // if (this.is_done)
        //     fatalError('Collector.step_forward() called when eof is true');

        // Disable the current question's radio buttons and remove the undo button
        this.stack[this.stack.length - 1].disable();
        if (this.undo) {
            this.undo.remove();
            this.undo = null;
        }

        // Add the current question's next items to the stack
        let items_to_push = this.stack[this.stack.length - 1].next;
        if (! items_to_push) return;
        for (let i=0; i < items_to_push.length; i++)
            this.stack.push(items_to_push[i]);

        // It is possible for the collector to be done with a parameter at the top of the stack; this will be the
        // case when "Kana Table" is the selected quiz.  We need to detect that case before we attempt to display
        // the item on the top of the stack.
        if (this.stack[this.stack.length - 1] instanceof Parameter)
            if ((this.stack[0].selection === 'Kana Table') && (this.stack.length === MAX_STACK_SIZE))
                return;

        // Display the control for the question on the top of the stack
        let top_item = this.stack[this.stack.length - 1];
        if (! top_item instanceof Question)
            fatalError('Collector.step_forward() item on the top of the stack should be a Question object');
        top_item.display();
        if (this.undo != null)
            fatalError('Collector.step_forward() this.undo should be null');
        this.undo = new UndoControl(top_item.id);
    }

    step_backward() {
        if (this.stack.length === 1)
            fatalError('Collector.step_backward() called from beginning of stack');

        // Delete the undo button when it exists
        if (this.undo != null) {
            this.undo.remove();
            this.undo = null;
        }

        // Pop the top item from the stack and remove its controller from the screen
        let top_item = this.stack.pop();
        if (! top_item instanceof Question)
            fatalError('Collector.step_backward() top item on stack should be a Question object');
        top_item.remove();

        // Pop parameters from the stack until the first previous question is at the top of the stack.
        for (; this.stack[this.stack.length - 1] instanceof Parameter;) {
            this.stack.pop();
        }

        // Enable the question that is now on the top of the stack.
        this.stack[this.stack.length - 1].enable();

        // Add the undo button provided we are not back to the first question.
        if (this.stack.length !== 1)
            this.undo = new UndoControl(this.stack[this.stack.length - 1].id);
    }
}
