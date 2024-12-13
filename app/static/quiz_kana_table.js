
class KanaTableQuestion extends Question {
    constructor(payload) {
        super();
        this.character = payload;
    }

    show() {
        document.getElementById('prompt-word').innerText = this.character.key;
    }
}

class KanaTableQuiz extends Quiz {
    constructor() {
        super();

        if (this.payload.questions.length !== 1) fatalError('KanaTableQuiz.constructor(): only one question expected')

        this.progress_bar.max = this.payload.questions[0].length;

        this.items = [];
        for (let i=0; i < this.payload.questions[0].length; i++)
            this.items.push(new KanaTableQuestion(this.payload.questions[0][i]))
        this.items[this.current_item].show();
    }
}