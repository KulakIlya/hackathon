const chatForm = document.querySelector('.chat-section .chat-form');

chatForm?.classList.remove('is-hidden');

const dialogSection = document.querySelector('.dialog');

const dialogForm = dialogSection?.querySelector('.chat-form');

dialogSection?.addEventListener('click', e => {
  showForm(e);
  hideUserResponses(e);
});

dialogForm?.addEventListener('submit', e => {
  e.preventDefault();
});

function showForm(e) {
  const closest = e.target.closest('button[data-correct]');
  if (!closest) return;

  if (closest.dataset.correct === 'false') {
    dialogForm.classList.remove('is-hidden');
    showClarifyingMessage(e);
  }
}

function hideUserResponses(e) {
  const userResponses = e.currentTarget.querySelector('.user-responses');
  userResponses.classList.add('is-hidden');
  setTimeout(() => {
    userResponses.remove();
  }, 1000);
}

function showClarifyingMessage(e) {
  const container = dialogSection.querySelector('.dialog-wrapper');
  container.insertAdjacentHTML('beforeend', getClarifyingMessageMarkup());
}

function getClarifyingMessageMarkup() {
  return `<div class="answer-wrapper">
    <p class="answer">Add more photos or explanation :)</p>
  </div>`;
}
