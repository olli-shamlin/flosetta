
class MegaMatchQuestion extends Question {
    constructor(payload) {
        super();
        this.word = payload;
    }

    show() {}
}

class MegaMatchQuiz extends Quiz {
    constructor() {
        super();

        if (this.payload.questions.length !== 1) fatalError('KanaTableQuiz.constructor(): only one question expected')

        this.progress_bar.max = this.payload.questions[0].length;

        this.items = [];
        for (let i=0; i < this.payload.questions[0].length; i++)
            this.items.push(new MegaMatchQuestion(this.payload.questions[0][i]))
    }
}