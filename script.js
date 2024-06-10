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

document.addEventListener("DOMContentLoaded", () => {
  const roles = ["Material Scientist", "AI Developer", "Photonics", "Healthcare Analytics","Software Development"];
  let currentRoleIndex = 0;
  const roleElement = document.getElementById("role");
  const prefix = "|";

  function typeRole(role, callback) {
    let charIndex = 0;

    function typeChar() {
      if (charIndex < role.length) {
        roleElement.innerHTML = prefix + role.substring(0, charIndex + 1);
        charIndex++;
        setTimeout(typeChar, 20); // Faster typing speed
      } else {
        setTimeout(callback, 1000); // Delay before deleting
      }
    }

    typeChar();
  }

  function deleteRole(callback) {
    let charIndex = roleElement.innerHTML.length - prefix.length;

    function deleteChar() {
      if (charIndex > 0) {
        roleElement.innerHTML = prefix + roleElement.innerHTML.substring(prefix.length, charIndex + prefix.length - 1);
        charIndex--;
        setTimeout(deleteChar, 10); // Faster deleting speed
      } else {
        callback();
      }
    }

    deleteChar();
  }

  function startTypingAnimation() {
    typeRole(roles[currentRoleIndex], () => {
      setTimeout(() => {
        deleteRole(() => {
          currentRoleIndex = (currentRoleIndex + 1) % roles.length;
          startTypingAnimation();
        });
      }, 500); // Shorter delay before starting to type next role
    });
  }

  startTypingAnimation(); // Initial call to start the animation
});
