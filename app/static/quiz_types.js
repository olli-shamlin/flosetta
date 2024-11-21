
let i = 1;
const Form = Object.freeze({
    ENGLISH:  i++,
    ROMAJI:   i++,
    KANA:     i++,
    KANJI:    i++,
    HIRAGANA: i++,
    KATAKANA: i++,
});

const valid_character_forms = Object.freeze([ElementForm.ROMAJI, ElementForm.HIRAGANA, ElementForm.KATAKANA]);
const valid_word_forms = Object.freeze([ElementForm.ENGLISH, ElementForm.ROMAJI, ElementForm.KANA, ElementForm.KANJI]);

class Item {
    constructor(key, values, prompt, choice, valid_element_forms) {
        for (let [k, v] of values) {
             if (!valid_element_forms.includes(k)) {
                throw `"${k}" is not a valid ElementForm value for ${this.constructor.name}`;
            }
        }

        this.key = key
        this.values = values
        this.prompt_form = prompt
        this.choice_form = choice
    }

    form_of(element_form) {
        return this.values.get(element_form)
    }

    prompt() { throw 'not implemented: Item.prompt()' }

    choice() { throw 'not implemented: Item.choice()' }
}

class Character extends Item {
    constructor(key, values, prompt, choice) {
        super(key, values, prompt, choice, valid_character_forms)
    }

    echo() {
        return `Romaji = ${this.form_of(ElementForm.ROMAJI)} ` +
               `Hiragana = ${this.form_of(ElementForm.HIRAGANA)} ` +
               `Katakana = ${this.form_of(ElementForm.KATAKANA)}}`
    }
}

class Word extends Item {
    constructor(key, values, prompt, choice) {
        super(key, values, prompt, choice, valid_word_forms)
    }

    echo() {
        return `English = ${this.form_of(ElementForm.ENGLISH)} ` +
               `Romaji = ${this.form_of(ElementForm.ROMAJI)} ` +
               `Kana = ${this.form_of(ElementForm.KANA)} ` +
               `Kanji = ${this.form_of(ElementForm.KANJI)}`
    }
}
