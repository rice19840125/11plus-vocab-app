// State
let currentDay = 1;
let currentPart = 1;
const TOTAL_PARTS = 8;
const PART_TITLES = [
    "Part 1: Story Time 📖",
    "Part 2: Vocabulary List 📚",
    "Part 3: Writing Practice ✍️",
    "Part 4: Picture Match 🖼️",
    "Part 5: Synonym Match 🔗",
    "Part 6: Antonym Match 🪞",
    "Part 7: Make a Sentence 📝",
    "Part 8: Yesterday's Review 🧠"
];

// DOM Elements
const daySelect = document.getElementById('day-select');
const partTitle = document.getElementById('part-title');
const mainContent = document.getElementById('main-content');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress-bar');

// Init
function init() {
    // Populate Day Selector
    const days = Object.keys(vocabularyData);
    days.forEach(day => {
        const option = document.createElement('option');
        option.value = day;
        option.textContent = `Day ${day}`;
        daySelect.appendChild(option);
    });

    daySelect.addEventListener('change', (e) => {
        currentDay = parseInt(e.target.value);
        currentPart = 1;
        render();
    });

    prevBtn.addEventListener('click', () => {
        if (currentPart > 1) {
            currentPart--;
            render();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentPart < TOTAL_PARTS) {
            currentPart++;
            render();
        }
    });

    render();
}

function render() {
    partTitle.textContent = PART_TITLES[currentPart - 1];
    progressBar.style.width = `${(currentPart / TOTAL_PARTS) * 100}%`;
    mainContent.innerHTML = ''; // clear

    prevBtn.style.display = currentPart === 1 ? 'none' : 'block';
    nextBtn.style.display = currentPart === TOTAL_PARTS ? 'none' : 'block';
    nextBtn.textContent = "Next Part ➡️";

    const dayData = vocabularyData[currentDay];
    
    if (!dayData) {
        mainContent.innerHTML = `<p>Data for Day ${currentDay} is not available yet.</p>`;
        return;
    }

    switch(currentPart) {
        case 1: renderStoryTime(dayData); break;
        case 2: renderVocabList(dayData); break;
        case 3: renderWritingPractice(dayData); break;
        case 4: renderMatch(dayData.words, 'picture'); break;
        case 5: renderMatch(dayData.words, 'synonym'); break;
        case 6: renderMatch(dayData.words, 'antonym'); break;
        case 7: renderMakeSentence(dayData); break;
        case 8: renderReviewMatch(); break;
    }
}

// -------------------------
// Render Functions
// -------------------------

function renderStoryTime(data) {
    const box = document.createElement('div');
    box.className = 'story-box';
    // Convert markdown bold to html bold for the story
    let htmlStory = data.story.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    box.innerHTML = htmlStory;
    mainContent.appendChild(box);
}

function renderVocabList(data) {
    data.words.forEach(w => {
        const card = document.createElement('div');
        card.className = 'vocab-card';
        
        let synonymsHtml = w.synonyms.map(s => `<span class="tag synonym">${s} <button class="speak-btn-small" data-word="${s}" title="Listen to pronunciation">🔊</button></span>`).join('');
        let antonymsHtml = w.antonyms.map(a => `<span class="tag antonym">${a} <button class="speak-btn-small" data-word="${a}" title="Listen to pronunciation">🔊</button></span>`).join('');
        let sentencesHtml = w.sentences.map(s => `<li>${s}</li>`).join('');

        card.innerHTML = `
            <div class="vocab-header">
                <span class="emoji-icon" style="margin:0;">${w.emoji}</span>
                <div>
                    <div class="vocab-word">
                        ${w.word} 
                        <span class="vocab-pronunciation">${w.pronunciation}</span>
                        <button class="speak-btn" data-word="${w.word}" title="Listen to pronunciation">🔊</button>
                    </div>
                </div>
            </div>
            <div class="vocab-meaning">${w.simpleMeaning}</div>
            <div class="vocab-tags">
                ${synonymsHtml}
                ${antonymsHtml}
            </div>
            <ul class="vocab-sentences">
                ${sentencesHtml}
            </ul>
        `;
        
        // Attach click listener for text-to-speech
        const speakBtn = card.querySelector('.speak-btn');
        speakBtn.addEventListener('click', () => {
            playAudio(speakBtn.dataset.word);
        });

        // Attach click listeners for small speak buttons
        const smallSpeakBtns = card.querySelectorAll('.speak-btn-small');
        smallSpeakBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent triggering any other click events
                playAudio(btn.dataset.word);
            });
        });

        mainContent.appendChild(card);
    });
}

function playAudio(word) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.lang = 'en-GB'; // British English for 11+
        utterance.rate = 0.9; // Slightly slower for clarity
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Sorry, your browser doesn't support text-to-speech!");
    }
}

function renderWritingPractice(data) {
    const description = document.createElement('p');
    description.textContent = "Type each word 5 times to practice your spelling!";
    description.style.marginBottom = "20px";
    description.style.fontWeight = "600";
    mainContent.appendChild(description);

    let allCorrect = true;
    const checkCompletion = () => {
        const inputs = document.querySelectorAll('.writing-input');
        let done = true;
        inputs.forEach(inp => {
            if (!inp.classList.contains('success')) done = false;
        });
        if (done) {
            showSuccess("Amazing spelling! 🎉");
        }
    };

    data.words.forEach(w => {
        const row = document.createElement('div');
        row.className = 'writing-row';
        row.innerHTML = `<div class="writing-word">${w.word} <button class="speak-btn-small" style="margin-left:8px;" data-word="${w.word}" title="Listen to pronunciation">🔊</button></div><div class="writing-inputs"></div>`;
        const inputsContainer = row.querySelector('.writing-inputs');

        const speakBtn = row.querySelector('.speak-btn-small');
        if (speakBtn) {
            speakBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                playAudio(speakBtn.dataset.word);
            });
        }

        for(let i=0; i<5; i++) {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'writing-input';
            input.placeholder = w.word;
            input.addEventListener('input', (e) => {
                if (e.target.value.trim().toLowerCase() === w.word.toLowerCase()) {
                    e.target.classList.add('success');
                } else {
                    e.target.classList.remove('success');
                }
                checkCompletion();
            });
            inputsContainer.appendChild(input);
        }
        mainContent.appendChild(row);
    });
}

function renderMakeSentence(data) {
    const description = document.createElement('p');
    description.textContent = "Write one sentence for each word!";
    description.style.marginBottom = "20px";
    description.style.fontWeight = "600";
    mainContent.appendChild(description);

    data.words.forEach(w => {
        const row = document.createElement('div');
        row.className = 'writing-row';
        row.innerHTML = `<div class="writing-word">${w.word}</div>`;
        const input = document.createElement('textarea');
        input.className = 'sentence-input';
        input.placeholder = `Use "${w.word}" in a sentence...`;
        
        // Load saved sentence from localStorage
        const storageKey = `sentence_${currentDay}_${w.word}`;
        const savedSentence = localStorage.getItem(storageKey);
        if (savedSentence) {
            input.value = savedSentence;
        }

        // Save sentence to localStorage on input
        input.addEventListener('input', (e) => {
            localStorage.setItem(storageKey, e.target.value);
        });

        row.appendChild(input);
        mainContent.appendChild(row);
    });

    // Add Submit to Google Forms Button
    const submitBtn = document.createElement('button');
    submitBtn.textContent = "Submit Sentences 🚀";
    submitBtn.style.marginTop = "20px";
    submitBtn.style.width = "100%";
    submitBtn.style.padding = "15px";
    submitBtn.style.fontSize = "18px";
    submitBtn.style.fontWeight = "bold";
    submitBtn.style.backgroundColor = "#4CAF50";
    submitBtn.style.color = "white";
    submitBtn.style.border = "none";
    submitBtn.style.borderRadius = "8px";
    submitBtn.style.cursor = "pointer";
    submitBtn.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)";
    submitBtn.style.transition = "background-color 0.2s";

    submitBtn.addEventListener('mouseover', () => submitBtn.style.backgroundColor = "#45a049");
    submitBtn.addEventListener('mouseout', () => submitBtn.style.backgroundColor = "#4CAF50");

    submitBtn.addEventListener('click', () => {
        const inputs = mainContent.querySelectorAll('.sentence-input');
        let submissionText = `[Day ${currentDay}] Part 7: Make a Sentence\n\n`;
        inputs.forEach((input, index) => {
            const word = data.words[index].word;
            submissionText += `${index + 1}. ${word}: ${input.value}\n`;
        });

        const formUrl = 'https://docs.google.com/forms/d/e/1FAIpQLSf_-bQu1lagHOknc2BoI8lRwK9-pUzGDCnz9FOXZ4sL9vnQpw/formResponse';
        const formData = new URLSearchParams();
        formData.append('entry.820079942', submissionText);

        // Change button state
        submitBtn.textContent = "Submitting... ⏳";
        submitBtn.disabled = true;

        fetch(formUrl, {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        }).then(() => {
            submitBtn.textContent = "Success! Sentences saved. ✅";
            submitBtn.style.backgroundColor = "#2E7D32";
            setTimeout(() => {
                submitBtn.textContent = "Submit Sentences 🚀";
                submitBtn.style.backgroundColor = "#4CAF50";
                submitBtn.disabled = false;
            }, 3000);
        }).catch((err) => {
            submitBtn.textContent = "Error submitting ❌";
            submitBtn.style.backgroundColor = "#d32f2f";
            setTimeout(() => {
                submitBtn.textContent = "Submit Sentences 🚀";
                submitBtn.style.backgroundColor = "#4CAF50";
                submitBtn.disabled = false;
            }, 3000);
        });
    });

    mainContent.appendChild(submitBtn);
}

function renderReviewMatch() {
    if (currentDay === 1) {
        const box = document.createElement('div');
        box.className = 'story-box';
        box.innerHTML = `<p>This is your first day, so there is no review from yesterday! Great job completing Day 1! 🎉</p>`;
        mainContent.appendChild(box);
        return;
    }
    
    const yesterdayData = vocabularyData[currentDay - 1];
    if (!yesterdayData) {
        mainContent.innerHTML = `<p>No data for yesterday found.</p>`;
        return;
    }

    const description = document.createElement('p');
    description.textContent = "Review yesterday's words by matching them to their picture & meaning!";
    description.style.marginBottom = "20px";
    mainContent.appendChild(description);
    
    renderMatch(yesterdayData.words, 'picture');
}

// -------------------------
// Matching Game Engine
// -------------------------

function renderMatch(words, mode) {
    let leftItems = [];
    let rightItems = [];

    words.forEach(w => {
        let displayLeft = w.word;
        let displayRight = "";
        
        if (mode === 'picture') {
            displayRight = `<span class="emoji-icon">${w.emoji}</span>${w.simpleMeaning}`;
        } else if (mode === 'synonym') {
            displayRight = `Synonyms:<br/>${w.synonyms.join(', ')}`;
        } else if (mode === 'antonym') {
            displayRight = `Antonyms:<br/>${w.antonyms.join(', ')}`;
        }

        leftItems.push({ id: w.word, content: displayLeft });
        rightItems.push({ id: w.word, content: displayRight });
    });

    // Shuffle
    leftItems = leftItems.sort(() => Math.random() - 0.5);
    rightItems = rightItems.sort(() => Math.random() - 0.5);

    const container = document.createElement('div');
    container.className = 'match-container';
    
    const leftCol = document.createElement('div');
    leftCol.className = 'match-column';
    
    const rightCol = document.createElement('div');
    rightCol.className = 'match-column';

    let selectedLeft = null;
    let selectedRight = null;
    let matchesFound = 0;

    const checkMatch = () => {
        if (selectedLeft && selectedRight) {
            if (selectedLeft.dataset.id === selectedRight.dataset.id) {
                // Correct
                selectedLeft.classList.add('correct');
                selectedRight.classList.add('correct');
                selectedLeft.classList.remove('selected');
                selectedRight.classList.remove('selected');
                matchesFound++;
                if (matchesFound === words.length) {
                    showSuccess("All matched perfectly! 🏆");
                }
            } else {
                // Wrong
                selectedLeft.classList.add('wrong');
                selectedRight.classList.add('wrong');
                setTimeout(() => {
                    selectedLeft.classList.remove('wrong', 'selected');
                    selectedRight.classList.remove('wrong', 'selected');
                    selectedLeft = null;
                    selectedRight = null;
                }, 500);
                return; // wait for timeout
            }
            selectedLeft = null;
            selectedRight = null;
        }
    };

    leftItems.forEach(item => {
        const div = document.createElement('div');
        div.className = 'match-item';
        div.innerHTML = item.content;
        div.dataset.id = item.id;
        div.addEventListener('click', () => {
            if (div.classList.contains('correct')) return;
            if (selectedLeft) selectedLeft.classList.remove('selected');
            selectedLeft = div;
            div.classList.add('selected');
            checkMatch();
        });
        leftCol.appendChild(div);
    });

    rightItems.forEach(item => {
        const div = document.createElement('div');
        div.className = 'match-item';
        div.innerHTML = item.content;
        div.dataset.id = item.id;
        div.addEventListener('click', () => {
            if (div.classList.contains('correct')) return;
            if (selectedRight) selectedRight.classList.remove('selected');
            selectedRight = div;
            div.classList.add('selected');
            checkMatch();
        });
        rightCol.appendChild(div);
    });

    container.appendChild(leftCol);
    container.appendChild(rightCol);
    mainContent.appendChild(container);
}

function showSuccess(msg) {
    let successDiv = document.querySelector('.success-message');
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        mainContent.appendChild(successDiv);
    }
    successDiv.textContent = msg;
    successDiv.style.display = 'block';
}

// Start
document.addEventListener('DOMContentLoaded', init);
