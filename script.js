document.addEventListener('DOMContentLoaded', () => {
  // Attach event listeners for 'About' buttons to flip the card
  const aboutButtons = document.querySelectorAll('.about-btn');
  aboutButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const cardContainer = btn.closest('.details-container');
      cardContainer.classList.toggle('flipped');
    });
  });

  // Attach event listeners for 'Back' buttons to flip the card back
  const backButtons = document.querySelectorAll('.flip-back-btn');
  backButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const cardContainer = btn.closest('.details-container');
      cardContainer.classList.toggle('flipped');
    });
  });
});