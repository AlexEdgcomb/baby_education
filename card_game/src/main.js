// Hide everything.
const $cardsContainer = $('#cards-container');
const $cards = $('.card');
const $start = $('#start');
const $table = $('table');
const $resetStats = $('#resetStats');
const $rewardContainer = $('#reward-container');
const $audio = $('#audio');
const audio = $audio.get(0);

$start.hide();
$cardsContainer.hide();
$rewardContainer.hide();

// Load stats.
function loadStats() {
    const defaultResult = { truePositive: 0, falsePositive: 0, trueNegative: 0, falseNegative: 0 };
    const results = JSON.parse(localStorage.getItem('results'));

    if (results) {
        const matrix = results.reduce((accumulator, { cards, correct }) => {
            const correctWord = cards.find(({ correct }) => correct).word;
            const wrongWord = cards.find(({ correct }) => !correct).word;
            const correctResult = accumulator[correctWord] ?? { ...defaultResult };
            const wrongResult = accumulator[wrongWord] ?? { ...defaultResult };

            if (correct) {
                correctResult.truePositive++;
                wrongResult.trueNegative++;
            }
            else {
                correctResult.falseNegative++;
                wrongResult.falsePositive++;
            }

            accumulator[correctWord] = correctResult;
            accumulator[wrongWord] = wrongResult;

            return accumulator;
        }, {});

        for (const [word, { truePositive, falsePositive, trueNegative, falseNegative }] of Object.entries(matrix)) {
            $table.append(`<tr>
    <td>${word}</td>
    <td>${truePositive}</td>
    <td>${falsePositive}</td>
    <td>${trueNegative}</td>
    <td>${falseNegative}</td>
</tr>`);
        }
    }
}

loadStats();

function resetStats() {
    localStorage.clear();
    loadStats();
}

// Load player. Once loaded, show Start button.
let player;
function onYouTubeIframeAPIReady() {
    $start.show();
    player = new YT.Player('reward', {
        height: window.screen.height,
        playerVars: {
            controls: 0,
            modestbranding: 1,
            rel: 0,
        },
        videoId: 'isidNk0Ppkw',
        width: window.screen.width,
    });
}

// Start button clicked.
function start() {
    $start.hide();
    $table.hide();
    $resetStats.hide();

    // Randomize deck.
    shuffle(deck);

    const contentContainer = $('#content-container').get(0);

    contentContainer.requestFullscreen && contentContainer.requestFullscreen();
    giveCards();
}

function audioLoop() {
    audio.play();
    new Promise(resolve => audioResolve = resolve).then(() => {
        initialTimer = setTimeout(() => {
            audioLoop();
        }, 3000);
    });
}

// Generate cards and prompt.
const deck = [
    {
        src: 'mom.png',
        word: 'mom',
    },
    {
        src: 'dad.jpg',
        word: 'dad',
    },
    {
        src: 'bus.png',
        word: 'bus',
    },
    {
        src: 'ram.png',
        word: 'ram',
    },
    {
        src: 'fan.png',
        word: 'fan',
    },
    {
        src: 'sub.png',
        word: 'sub',
    },
    {
        src: 'bulb.png',
        word: 'bulb',
    },
    {
        src: 'nun.png',
        word: 'nun',
    },
];
let question = null;
let previousCorrect = true;
let initialTimer;
function giveCards() {
    $cardsContainer.show();
    $rewardContainer.hide();
    $cards.prop('disabled', false).removeClass('selected');

    // Pick question from slide deck.
    if (previousCorrect) {
        question = deck.splice(0, 2);
        deck.push(...question);
        question.forEach(item => {
            item.correct = false
        });

        const correctIndex = Math.floor(Math.random() * 2);
        question[correctIndex].correct = true;
    }
    else {
        // If wrong, give previously expected card + new incorrect card.
        question = question.filter(({ correct }) => correct);

        const next = deck.shift();

        next.correct = false;
        deck.push(next);
        question.push(next);
        shuffle(question);
    }

    // Show cards and give prompt.
    question.forEach(({ src }, index) => {
        $cards.eq(index).find('img').attr('src', `content/${src}`);
    });
    $audio.attr('src', `content/select_${question.find(({ correct }) => correct).word}.m4a`);
    audioLoop();
}

// Handle card selection.
function selected(cardIndex) {
    $cards.prop('disabled', true);
    $cards.eq(cardIndex).addClass('selected');

    audio.pause();
    clearTimeout(initialTimer);
    audioResolve = null;

    previousCorrect = question[cardIndex].correct;

    if (previousCorrect) {
        $cardsContainer.hide();
        $rewardContainer.show();
        player.setVolume(25);
        player.playVideo();
        setTimeout(() => {
            player.pauseVideo();
            giveCards();
        }, 10000);
    }
    else {
        const { word } = question.find(({ correct }) => !correct);

        $audio.attr('src', `content/you_selected_${word}.m4a`);
        audio.play();
        new Promise(resolve => audioResolve = resolve).then(() => setTimeout(giveCards, 2000));
    }

    // Tally confusion matrix.
    const results = JSON.parse(localStorage.getItem('results')) ?? [];

    results.push({
        cards: question.map(({ correct, word }) => ({ correct, word })),
        correct: previousCorrect,
    });
    localStorage.setItem('results', JSON.stringify(results));
}

let audioResolve = null;
audio.onended = () => {
    audioResolve && audioResolve();
};

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