const $start = $('#start');
const $game = $('#game');
const $reward = $('#reward');
const $cards = $('.card');

$game.hide();

const deck = [
    'O',
    'M',
    'D',
    'A',
];

function shuffle(array) {
    let currentIndex = array.length;
    let temporaryValue;
    let randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}

function start() {
    $start.hide();
    $game.show();

    const contentContainer = $('#content-container').get(0);
    contentContainer.requestFullscreen && contentContainer.requestFullscreen();

    shuffle(deck);
    giveQuestion();
}

let question = null;

function giveQuestion() {
    $cards.prop('disabled', false).removeClass('selected');
    $reward.css('visibility', 'hidden');

    const cardsToShow = 2;
    const cards = deck.splice(0, cardsToShow);
    question = cards.map(card => ({ card, correct: false }))
    question.forEach(({ card }, index) => {
        $cards.eq(index).text(card);
    });

    const correctIndex = Math.floor(Math.random() * question.length);
    question[correctIndex].correct = true;
    // TODO: Say to select question[correctIndex].card
    alert(`select ${question[correctIndex].card}`);
}

function selected(index) {
    $cards.prop('disabled', true);
    $cards.eq(index).addClass('selected');

    if (question[index].correct) {
        deck.push(...question.map(({ card }) => card));
        $reward.css('visibility', 'visible');
        // TODO: Say correct
        alert('correct');
    }
    else {
        deck.push(...question.filter(({ correct }) => !correct).map(({ card }) => card));
        // TODO: Say you selected question[index].card
        alert(`you selected ${question[index].card}`);
    }

    giveQuestion();
}